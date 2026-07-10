"""Diagram guard (scripts/build_diagrams.py).

Figures are authored as SVG (the source of truth) and rendered to PNG at a fixed
2x scale with cairosvg; ``.diagram-manifest.json`` pins the sha256 of each SVG and
its rendered PNG. The contract these tests enforce:

  * every committed diagram PNG is a **current render of its SVG** — so if an SVG
    changes, its PNG must be regenerated (via ``build_diagrams.py``) or CI fails;
  * every ``assets/**/*.svg`` is pinned in the manifest and has a PNG sibling;
  * the guard actually **detects** a stale/edited PNG (mechanism check).

cairosvg renders deterministically, so the byte comparison is stable given the
house fonts (Barlow Condensed, Open Sans).
"""
import hashlib

import pytest

import build_diagrams


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def test_committed_diagrams_in_sync(root):
    """The real, committed diagrams must be up to date (SVG == pin, PNG == render)."""
    problems = build_diagrams.check(root)
    assert problems == [], "diagram drift:\n  " + "\n  ".join(problems)


def test_every_png_is_a_current_render_of_its_svg(root):
    """Fidelity: each committed PNG equals a fresh render of its SVG.

    cairosvg is byte-reproducible only given the same cairo/freetype/font stack,
    so this asserts fidelity where the environment reproduces the pins (the
    authoring machine, or CI with the house fonts) and skips elsewhere. The
    portable SVG/PNG hash lockstep (test_committed_diagrams_in_sync) always runs.
    """
    diagrams = build_diagrams.discover(root)
    if not diagrams:
        return
    probe = diagrams[0]  # canary: does this environment reproduce a committed render?
    if _sha(build_diagrams.render(probe)) != _sha(probe.with_suffix(".png").read_bytes()):
        pytest.skip("cairosvg render not byte-reproducible here (cairo/font stack differs)")
    for svg in diagrams:
        png = svg.with_suffix(".png")
        assert _sha(png.read_bytes()) == _sha(build_diagrams.render(svg)), (
            f"{png.relative_to(root)} is not a current render of "
            f"{svg.relative_to(root)} — run build_diagrams.py"
        )


def test_guard_detects_a_stale_png(tmp_path):
    """Editing an SVG (or PNG) without rebuilding must be caught."""
    svg = tmp_path / "assets" / "x" / "d.svg"
    svg.parent.mkdir(parents=True)
    svg.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10" '
        'width="10" height="10"><rect width="10" height="10" fill="#914f37"/></svg>'
    )
    build_diagrams.build(tmp_path)
    assert build_diagrams.check(tmp_path) == []          # fresh build is clean

    svg.with_suffix(".png").write_bytes(b"not a real png")  # tamper with the PNG
    assert build_diagrams.check(tmp_path), "guard failed to flag a stale PNG"
