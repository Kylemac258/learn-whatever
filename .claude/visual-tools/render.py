#!/usr/bin/env python3
"""Render a Mermaid or SVG source file to PNG with headless Google Chrome.

Used by the mermaid-maker and svg-maker subagents. No Node, no npm: Mermaid
runs from the vendored vendor/mermaid.min.js inside headless Chrome, and
hand-written SVG is rasterised by the same browser.

Usage:
  render.py mermaid <source.mmd> [--save-as <slug>]
  render.py svg     <source.svg> [--save-as <slug>]

Without --save-as: writes a preview PNG next to the source (<source>.png) and
prints its path. Open it with Read and LOOK at it.
With --save-as: publishes the PNG into <project>/viz/viz-<slug>-<timestamp>.png
and prints a RESULT block with the filename and absolute path.

Exit code 0 on success; on failure prints the error (e.g. Mermaid parse error,
SVG XML error) and exits 1.
"""

import argparse
import html
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]  # <project>/.claude/visual-tools -> <project>
VIZ_DIR = PROJECT / "viz"
MERMAID_JS = HERE / "vendor" / "mermaid.min.js"
PAD = 24  # white margin around the picture, CSS px
SCALE = 2  # device scale factor for crisp PNGs
MAX_SIDE = 4000

CHROME_CANDIDATES = [
    os.environ.get("CHROME_PATH", ""),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    shutil.which("google-chrome") or "",
    shutil.which("chromium") or "",
]


def fail(msg: str) -> None:
    print(f"RENDER FAILED\n{msg}", file=sys.stderr)
    sys.exit(1)


def find_chrome() -> str:
    for c in CHROME_CANDIDATES:
        if c and os.path.exists(c):
            return c
    fail("No Chrome/Chromium found. Install Google Chrome or set CHROME_PATH.")
    return ""


def chrome(args, timeout=60) -> subprocess.CompletedProcess:
    # A throwaway profile so we never touch (or hand off to) the user's running Chrome.
    with tempfile.TemporaryDirectory(prefix="viz-chrome-") as profile:
        cmd = [
            find_chrome(),
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-extensions",
            "--allow-file-access-from-files",
            f"--user-data-dir={profile}",
            *args,
        ]
        try:
            return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            fail("Chrome timed out.")
            raise  # unreachable


def png_size(path: Path):
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", head[16:24])


def svg_dims(svg_text: str):
    """(width, height) in CSS px from width/height attrs, else viewBox."""
    try:
        root = ET.fromstring(svg_text.encode("utf-8"))
    except ET.ParseError as e:
        fail(f"SVG is not well-formed XML: {e}")
    if not root.tag.endswith("svg"):
        fail("Root element is not <svg>.")

    def num(v):
        if v is None:
            return None
        m = re.match(r"^\s*([0-9.]+)\s*(px)?\s*$", v)
        return float(m.group(1)) if m else None

    w, h = num(root.get("width")), num(root.get("height"))
    vb = root.get("viewBox")
    if vb:
        parts = [float(x) for x in re.split(r"[\s,]+", vb.strip()) if x]
        if len(parts) == 4:
            if w is None and h is None:
                w, h = parts[2], parts[3]
            elif w is None:
                w = h * parts[2] / parts[3]
            elif h is None:
                h = w * parts[3] / parts[2]
    if not w or not h:
        fail("SVG needs width/height attributes or a viewBox so its size is known.")
    return w, h


def screenshot_svg(svg_markup: str, w: float, h: float, out: Path, workdir: Path) -> None:
    w, h = min(w, MAX_SIDE), min(h, MAX_SIDE)
    win_w, win_h = int(round(w)) + 2 * PAD, int(round(h)) + 2 * PAD
    page = workdir / "shot.html"
    page.write_text(
        "<!doctype html><meta charset='utf-8'>"
        "<style>html,body{margin:0;background:#fff}"
        f"#wrap{{padding:{PAD}px;width:{w}px;height:{h}px}}"
        f"#wrap>svg{{display:block;width:{w}px;height:{h}px;max-width:none}}</style>"
        f"<div id='wrap'>{svg_markup}</div>",
        encoding="utf-8",
    )
    tmp = workdir / "shot.png"
    res = chrome(
        [
            f"--force-device-scale-factor={SCALE}",
            f"--window-size={win_w},{win_h}",
            "--virtual-time-budget=3000",
            f"--screenshot={tmp}",
            page.as_uri(),
        ]
    )
    if not tmp.exists():
        fail(f"Chrome produced no screenshot.\n{res.stderr[-2000:]}")
    shutil.move(str(tmp), str(out))


def mermaid_to_svg(source: str, workdir: Path):
    """Return (svg_markup, width, height) for a Mermaid source."""
    page = workdir / "mermaid.html"
    page.write_text(
        "<!doctype html><meta charset='utf-8'><body>"
        f"<script src='{MERMAID_JS.as_uri()}'></script>"
        "<script>"
        f"const SRC = {json.dumps(source)};"
        "(async () => {"
        "  try {"
        "    mermaid.initialize({startOnLoad:false, theme:'default', securityLevel:'strict',"
        "      fontFamily:'-apple-system, Helvetica, Arial, sans-serif'});"
        "    await mermaid.parse(SRC);"
        "    const {svg} = await mermaid.render('viz', SRC);"
        "    const out = document.createElement('div'); out.id = 'out'; out.innerHTML = svg;"
        "    document.body.appendChild(out);"
        "    const r = out.querySelector('svg').getBoundingClientRect();"
        "    out.setAttribute('data-w', r.width); out.setAttribute('data-h', r.height);"
        "  } catch (e) {"
        "    const pre = document.createElement('pre'); pre.id = 'err';"
        "    pre.textContent = String((e && e.message) || e); document.body.appendChild(pre);"
        "  }"
        "})();"
        "</script>",
        encoding="utf-8",
    )
    res = chrome(["--virtual-time-budget=15000", "--dump-dom", page.as_uri()])
    dom = res.stdout
    m = re.search(r'<pre id="err">(.*?)</pre>', dom, re.S)
    if m:
        fail("Mermaid error:\n" + html.unescape(m.group(1)).strip())
    m = re.search(r'<div id="out"[^>]*data-w="([0-9.]+)"[^>]*data-h="([0-9.]+)"[^>]*>(.*)</div>', dom, re.S)
    if not m:
        fail("Mermaid produced no diagram (no output and no error).\n" + res.stderr[-2000:])
    w, h, svg = float(m.group(1)), float(m.group(2)), m.group(3)
    svg = svg[: svg.rfind("</svg>") + len("</svg>")]
    return svg, w, h


def main() -> None:
    ap = argparse.ArgumentParser(description="Render Mermaid/SVG to PNG via headless Chrome.")
    ap.add_argument("kind", choices=["mermaid", "svg"])
    ap.add_argument("source")
    ap.add_argument("--save-as", help="publish into viz/ as viz-<slug>-<timestamp>.png")
    a = ap.parse_args()

    src_path = Path(a.source).resolve()
    if not src_path.exists():
        fail(f"Source not found: {src_path}")
    source = src_path.read_text(encoding="utf-8")

    with tempfile.TemporaryDirectory(prefix="viz-work-") as wd:
        workdir = Path(wd)
        if a.kind == "mermaid":
            svg, w, h = mermaid_to_svg(source, workdir)
        else:
            svg = re.sub(r"^\s*<\?xml[^>]*\?>\s*", "", source)
            svg = re.sub(r"<!DOCTYPE[^>]*>\s*", "", svg, flags=re.I)
            w, h = svg_dims(svg)

        if a.save_as:
            slug = re.sub(r"[^a-z0-9]+", "-", a.save_as.lower()).strip("-") or "diagram"
            VIZ_DIR.mkdir(parents=True, exist_ok=True)
            out = VIZ_DIR / f"viz-{slug}-{time.strftime('%Y%m%d-%H%M%S')}.png"
        else:
            out = src_path.with_suffix(".png")
        screenshot_svg(svg, w, h, out, workdir)

    size = png_size(out)
    if a.save_as:
        print(f"RESULT:\nfilename: {out.name}\npath: {out}")
    else:
        print(f"preview: {out}")
    if size:
        print(f"size: {size[0]}x{size[1]} px")


if __name__ == "__main__":
    main()
