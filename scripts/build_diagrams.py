#!/usr/bin/env python3
"""Render committed diagram SVGs to PNGs, and pin both so they can't drift apart.

The SVG is the source of truth (see docs/diagram-style.md). Every `*.svg` under
`assets/` is rendered to a sibling `*.png` at a fixed 2x scale with cairosvg, and
`.diagram-manifest.json` records the sha256 of each SVG and its rendered PNG.

Usage:
    python scripts/build_diagrams.py            # (re)render every diagram + manifest
    python scripts/build_diagrams.py --check     # verify PNGs are up to date (CI/test)

`--check` verifies (portably, no rendering) that every SVG and its PNG still match
the sha256 pinned in the manifest: change an SVG and its pin no longer matches, so
you must re-run the build, which re-renders the PNG and repins both. Byte-level
render *fidelity* (the PNG really is cairosvg's output for the SVG) is asserted by
tests/test_diagrams.py on machines whose cairo/font stack reproduces the pins —
cross-machine PNG bytes aren't guaranteed, so that check is skipped elsewhere.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

import cairosvg

from archive import repo_root

SCALE = 2
MANIFEST = ".diagram-manifest.json"


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def discover(root: Path):
    return sorted(p for p in (root / "assets").rglob("*.svg"))


def render(svg_path: Path) -> bytes:
    return cairosvg.svg2png(url=str(svg_path), scale=SCALE)


def _entry(root: Path, svg: Path, png_bytes: bytes):
    return {
        "svg": str(svg.relative_to(root)),
        "png": str(svg.with_suffix(".png").relative_to(root)),
        "svg_sha256": _sha(svg.read_bytes()),
        "png_sha256": _sha(png_bytes),
    }


def build(root: Path):
    entries = []
    for svg in discover(root):
        png_bytes = render(svg)
        svg.with_suffix(".png").write_bytes(png_bytes)
        entries.append(_entry(root, svg, png_bytes))
        print(f"  rendered {svg.relative_to(root)} -> {svg.with_suffix('.png').name}")
    (root / MANIFEST).write_text(json.dumps({"scale": SCALE, "diagrams": entries}, indent=2) + "\n")
    print(f"  wrote {MANIFEST} ({len(entries)} diagram(s))")
    return entries


def check(root: Path):
    """Return a list of human-readable problems; empty means up to date."""
    problems = []
    manifest_path = root / MANIFEST
    if not manifest_path.exists():
        return [f"{MANIFEST} is missing — run `python scripts/build_diagrams.py`"]
    pinned = {d["svg"]: d for d in json.loads(manifest_path.read_text())["diagrams"]}
    on_disk = {str(p.relative_to(root)) for p in discover(root)}

    for rel in sorted(on_disk - pinned.keys()):
        problems.append(f"{rel}: SVG not in manifest — run build_diagrams.py")
    for rel in sorted(pinned.keys() - on_disk):
        problems.append(f"{rel}: in manifest but SVG missing")

    for rel in sorted(on_disk & pinned.keys()):
        svg = root / rel
        png = svg.with_suffix(".png")
        d = pinned[rel]
        if _sha(svg.read_bytes()) != d["svg_sha256"]:
            problems.append(f"{rel}: SVG changed since last build — re-run build_diagrams.py")
            continue
        if not png.exists():
            problems.append(f"{d['png']}: rendered PNG is missing — run build_diagrams.py")
            continue
        if _sha(png.read_bytes()) != d["png_sha256"]:
            problems.append(f"{d['png']}: PNG differs from its pin — re-run build_diagrams.py")
    return problems


def main():
    ap = argparse.ArgumentParser(description="Render diagram SVGs to PNGs and pin them.")
    ap.add_argument("--check", action="store_true", help="verify only; exit nonzero if stale")
    args = ap.parse_args()
    root = Path(repo_root)
    if args.check:
        problems = check(root)
        if problems:
            print("Diagram drift:")
            for p in problems:
                print(f"  {p}")
            sys.exit(1)
        print("Diagrams up to date.")
    else:
        build(root)


if __name__ == "__main__":
    main()
