"""Validate the RENDERED <head> SEO/scholarly metadata of a built site.

The pytest suite checks the frontmatter that *drives* the metadata; this checks
the actual HTML that jekyll-seo-tag + the layouts produce — catching layout
regressions (a broken citation tag, a typeless JSON-LD, a relative og:image, a
duplicate twitter:card, the generic site-tagline description, …).

It needs a built site (heavy: bundle + jekyll), so it runs on a schedule, not on
every push. Usage:

    bundle exec jekyll build -d _site
    python scripts/check_seo.py _site
"""
import json
import os
import re
import sys

from archive import internal_items, complain, exit_with_status

SITE_DESC = "scholarly and technical writings by Daniel Hardman"
BASE = "https://dhh1128.github.io/papers/"


def meta_contents(html, key):
    return re.findall(
        rf'<meta[^>]+(?:name|property)="{re.escape(key)}"[^>]+content="([^"]*)"', html)


def link_href(html, rel):
    m = re.search(rf'<link[^>]+rel="{rel}"[^>]+href="([^"]*)"', html)
    return m.group(1) if m else None


def ld_nodes(html):
    out = []
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            out.append(json.loads(b))
        except json.JSONDecodeError as e:
            out.append({"__bad__": str(e)})
    return out


def expected_authors(meta):
    if meta.get("authors"):
        return len(meta["authors"])
    a = meta.get("author")
    if isinstance(a, list):
        return len(a)
    return 1 if a else 0


def check_doc(slug, meta, html):
    cat = str(meta.get("category", ""))
    want_type = "ScholarlyArticle" if cat == "Papers" else "TechArticle"
    nauthors = expected_authors(meta)
    errs = []

    canon = link_href(html, "canonical")
    if not (canon and canon.startswith(BASE) and canon.endswith(slug + ".html")):
        errs.append(f"canonical wrong/relative: {canon}")
    ogimg = meta_contents(html, "og:image")
    if not (ogimg and ogimg[0] == f"{BASE}assets/cards/{slug}.png"):
        errs.append(f"og:image missing/relative: {ogimg}")
    tc = meta_contents(html, "twitter:card")
    if tc != ["summary_large_image"]:
        errs.append(f"twitter:card should be one summary_large_image, got {tc}")
    desc = meta_contents(html, "description")
    if not desc or not desc[0].strip() or desc[0] == SITE_DESC:
        errs.append("meta description missing or generic site tagline")
    if not meta_contents(html, "citation_title"):
        errs.append("citation_title missing")
    ca = meta_contents(html, "citation_author")
    if len(ca) != nauthors:
        errs.append(f"citation_author count {len(ca)} != {nauthors} authors")
    if not meta_contents(html, "citation_pdf_url"):
        errs.append("citation_pdf_url missing")

    nodes = ld_nodes(html)
    bad = [n["__bad__"] for n in nodes if "__bad__" in n]
    if bad:
        errs.append(f"invalid JSON-LD: {bad}")
    scholarly = [n for n in nodes if n.get("@type") in ("ScholarlyArticle", "TechArticle")]
    if not scholarly:
        errs.append("no ScholarlyArticle/TechArticle JSON-LD node")
    else:
        n = scholarly[0]
        if n.get("@type") != want_type:
            errs.append(f"JSON-LD @type {n.get('@type')} != {want_type} (category {cat})")
        authors = n.get("author") or []
        if not isinstance(authors, list) or len(authors) != nauthors:
            errs.append(f"JSON-LD author count != {nauthors}")
        ident = n.get("identifier") or []
        ident = ident if isinstance(ident, list) else [ident]
        if meta.get("item_id") and meta["item_id"] not in ident:
            errs.append("JSON-LD identifier missing item_id")

    for e in errs:
        complain(f"{slug}.html: {e}")


def main():
    site = sys.argv[1] if len(sys.argv) > 1 else "_site"
    docs = list(internal_items())
    for it in docs:
        slug = it.url[:-3]
        path = os.path.join(site, slug + ".html")
        if not os.path.isfile(path):
            complain(f"{slug}: not built at {path}")
            continue
        check_doc(slug, it.meta, open(path, encoding="utf-8").read())

    idx = os.path.join(site, "index.html")
    if os.path.isfile(idx):
        nodes = ld_nodes(open(idx, encoding="utf-8").read())
        cp = [n for n in nodes if n.get("@type") == "CollectionPage"]
        if not cp:
            complain("index.html: no CollectionPage JSON-LD")
        elif len(cp[0].get("hasPart", [])) != len(docs):
            complain(f"index.html: CollectionPage hasPart "
                     f"{len(cp[0].get('hasPart', []))} != {len(docs)} documents")
    else:
        complain("index.html not built")

    exit_with_status(f"Rendered SEO OK for {len(docs)} documents.")


if __name__ == "__main__":
    main()
