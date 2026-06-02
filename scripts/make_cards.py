"""Generate a 1200x630 social-share card (og:image) for every document.

Builds an SVG from each document's metadata (title / authors / category /
item_id / date), renders it to `assets/cards/<slug>.png` with cairosvg, and sets
`image: /assets/cards/<slug>.png` in the frontmatter so jekyll-seo-tag emits
`og:image` / `twitter:image` (a `summary_large_image` card).

Default: (re)generate every card + ensure the `image` field.
`--check-only`: fail if any card PNG is missing or `image` is unset (the CI
guard — needs no cairosvg / system libs, only checks files + frontmatter).

Cards are committed (the served artifact); the SVG is rendered in-memory. The
template here is the source of truth — regenerate after a metadata change.
"""
import argparse
import html
import os
import textwrap

from archive import internal_items, repo_root, complain, exit_with_status

CARDS_DIR = os.path.join(repo_root, "assets", "cards")
W, H = 1200, 630
BRAND, ACCENT, INK = "#491705", "#914f37", "#2a1a10"
SUB, FAINT, CREAM, RULE = "#6b5547", "#8a7a6c", "#fbf8f4", "#e6ddd2"
LABEL = {"Papers": "PAPER", "Analyses": "ANALYSIS", "Primers": "PRIMER",
         "Comparisons": "COMPARISON", "Guidance": "GUIDANCE",
         "Positions": "POSITION", "Specifications": "SPECIFICATION"}


def authors_line(meta):
    if meta.get("authors"):
        return " · ".join(a["name"] if isinstance(a, dict) else str(a)
                               for a in meta["authors"])
    a = meta.get("author")
    if isinstance(a, list):
        return " · ".join(a)
    return str(a or "")


def build_svg(meta):
    title = str(meta.get("title", ""))
    lines = textwrap.wrap(title, 30)
    if len(lines) > 4:
        fs, lines = 46, textwrap.wrap(title, 38)
    else:
        fs = 60
    ty0 = 250 if len(lines) <= 3 else 210
    tspans = "".join(
        f'<tspan x="90" y="{ty0 + i*int(fs*1.18)}">{html.escape(l)}</tspan>'
        for i, l in enumerate(lines))
    label = LABEL.get(str(meta.get("category", "")), "DOCUMENT")
    pill_w = 60 + len(label) * 15
    pill_x = 1110 - pill_w
    item_id = html.escape(str(meta.get("item_id", "")))
    date = html.escape(str(meta.get("date", "")))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="{W}" height="{H}" fill="{CREAM}"/>
  <rect x="0" y="0" width="14" height="{H}" fill="{BRAND}"/>
  <text x="90" y="92" font-family="DejaVu Sans" font-size="26" font-weight="bold"
        letter-spacing="6" fill="{ACCENT}">CODECRAFT PAPERS</text>
  <rect x="{pill_x}" y="62" width="{pill_w}" height="44" rx="22" fill="{BRAND}"/>
  <text x="{pill_x + pill_w//2}" y="92" font-family="DejaVu Sans" font-size="22"
        font-weight="bold" letter-spacing="3" fill="#ffffff" text-anchor="middle">{label}</text>
  <line x1="90" y1="120" x2="1110" y2="120" stroke="{RULE}" stroke-width="2"/>
  <text font-family="TeX Gyre Pagella, serif" font-size="{fs}" fill="{INK}">{tspans}</text>
  <text x="90" y="540" font-family="TeX Gyre Pagella, serif" font-size="34"
        fill="{SUB}">{html.escape(authors_line(meta))}</text>
  <line x1="90" y1="576" x2="1110" y2="576" stroke="{RULE}" stroke-width="2"/>
  <text x="90" y="606" font-family="DejaVu Sans" font-size="22" fill="{FAINT}">{item_id} · {date}</text>
  <text x="1110" y="606" font-family="DejaVu Sans" font-size="22" fill="{FAINT}"
        text-anchor="end">dhh1128.github.io/papers</text>
</svg>'''


def ensure_image_field(path, rel, check_only):
    """Return True if the `image:` field is missing/wrong (and set it unless check_only)."""
    text = open(path, encoding="utf-8").read()
    lines = text.split("\n")
    end = lines.index("---", 1)
    fm = lines[1:end]
    want = f"image: {rel}"
    idx = next((i for i, l in enumerate(fm) if l.startswith("image:")), None)
    if idx is not None and fm[idx].strip() == want:
        return False
    if check_only:
        return True
    if idx is not None:
        fm[idx] = want
    else:
        fm.append(want)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(["---"] + fm + lines[end:]))
    return False


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check-only", action="store_true",
                    help="Report missing cards / image fields without writing (for CI).")
    args = ap.parse_args()

    for item in internal_items():
        slug = item.url[:-3]
        png = os.path.join(CARDS_DIR, slug + ".png")
        rel = f"/assets/cards/{slug}.png"
        if args.check_only:
            if not os.path.isfile(png):
                complain(f"{item.url}: missing card ({rel}) — run scripts/make_cards.py")
            if ensure_image_field(item.path, rel, check_only=True):
                complain(f"{item.url}: 'image' field missing/wrong — run scripts/make_cards.py")
            continue
        os.makedirs(CARDS_DIR, exist_ok=True)
        import cairosvg  # lazy: only the render path needs the system cairo libs
        cairosvg.svg2png(bytestring=build_svg(item.meta).encode(),
                         write_to=png, output_width=W, output_height=H)
        ensure_image_field(item.path, rel, check_only=False)
        print(f"card: {slug}")

    exit_with_status("Cards present." if args.check_only else None)


if __name__ == "__main__":
    main()
