# House diagram style (DRAFT)

A lightweight, shared style for figures in Codecraft Papers: **clean, elegant,
academic — thin light lines on white, in the site's own brown earth tones.**
Provisional; being tuned against sample figures. The nearest prior art is the
`bes.md` diagrams (rounded cards, monospace data, thin curved leader lines to
small sans-serif labels); this keeps that grammar and shifts the palette to the
repo's CSS.

## Palette

Drawn from `assets/css/style.scss` so figures match the rendered site.

| Token | Hex | Role | Source |
|---|---|---|---|
| ground | `#ffffff` | background | body bg |
| ink | `#444444` | primary labels | body text |
| ink-strong | `#491705` | titles, key names, emphasis | `h1` |
| caption | `#777777` | italic captions / small notes | `figcaption` |
| **accent** | `#914f37` | the **single focal element** per figure | link |
| taupe | `#765043` | secondary strokes / labels | visited link |
| line | `#8a6f5c` | primary hairline (outlines) | derived |
| line-faint | `#c9b8ab` | leader lines, inner facets | derived (`#e0b69c`→`#765043`) |
| tint | `#f4e9df` | subtle fill (card/table ground) | derived (`#e0b69c`) |
| tint-accent | `#e7cdb8` | fill of the accented element | derived |
| rule-gray | `#e5e5e5` | neutral separators | border |

**Restraint rule:** exactly **one** accent (`#914f37`) per figure — the thing the
eye should land on. Everything else is brown/gray. No gradients, shadows, or
heavy fills.

## Fonts

Match the site (`style.scss`) exactly:

- **Titles & in-figure labels → Barlow Condensed** (Medium 500 for emphasis,
  Regular 400 otherwise). The site's heading face.
- **Captions & small notes → Open Sans** (Light 300 / Regular 400; Italic for
  captions). The site's body face.
- **Code / identifiers → monospace** — currently DejaVu Sans Mono (provisional;
  the site CSS sets no mono — confirm a house mono).

Both display faces are OFL. Rendering needs them installed locally (Barlow
Condensed from Google Fonts; Open Sans from Fontsource) or the raster falls back
to a generic sans.

## Line & shape conventions

- Hairlines (at the authored viewBox): outlines **1.8**, inner/facet **1.0–1.2**,
  leaders **1.1–1.2**. Round line joins and caps.
- Rounded corners (`rx ≈ 16`) on cards/pills.
- Leader lines are gentle Bézier curves (as in `bes`), never right-angle elbows.
- Generous whitespace; white ground.

## Pipeline (SVG is the source of truth)

- Author an **`.svg`** at a modest viewBox (≈720 wide), then render a **2× PNG**:
  `python3 -m cairosvg fig.svg -o fig.png --output-width 1440`.
- Store both under `assets/<slug>/`; embed the PNG in the paper and keep the SVG
  as the vendored source. (A `--diagrams` build step in `publish.py` can automate
  the render once the style settles.)
