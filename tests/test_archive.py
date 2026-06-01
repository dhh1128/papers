"""Characterization tests for the archive toolkit and item-id integrity.

These prove the corpus-level invariants the index and citation tooling rely on:
the category vocabulary parses out of about.md, every item-id is well-formed and
unique, and each id's category/date segments agree with the document's
frontmatter. (Ordinals are author-assigned and not recomputed here — see
docs/conventions.md.)
"""
import re

import archive

ID_RE = re.compile(r"^CC-[A-Z]{3}-\d{6}$")

EXPECTED_CATEGORIES = {
    "Specifications", "Papers", "Analyses", "Primers",
    "Comparisons", "Guidance", "Positions",
}

# First three letters (uppercased) of each category name -> category.
CAT_SEG = {c[:3].upper(): c for c in EXPECTED_CATEGORIES}


def test_categories_parse_from_about():
    cats = set(archive.categories())
    assert cats == EXPECTED_CATEGORIES, f"about.md categories drifted: {cats}"


def test_every_internal_item_has_frontmatter():
    bad = [i.url for i in archive.internal_items() if not i.meta]
    assert not bad, f"documents with unparseable/empty frontmatter: {bad}"


def test_item_id_format():
    bad = [(i.url, i.meta.get("item_id"))
           for i in archive.internal_items()
           if not ID_RE.match(str(i.meta.get("item_id", "")))]
    assert not bad, f"malformed item_ids: {bad}"


def test_item_ids_unique():
    ids = [i.meta.get("item_id") for i in archive.internal_items()]
    dupes = sorted({x for x in ids if ids.count(x) > 1})
    assert not dupes, f"duplicate item_ids: {dupes}"


def test_item_id_category_segment_matches_category():
    drift = {}
    for i in archive.internal_items():
        iid = str(i.meta.get("item_id", ""))
        cat = str(i.meta.get("category", ""))
        m = ID_RE.match(iid)
        if not m:
            continue
        seg = iid.split("-")[1]
        if cat[:3].upper() != seg:
            drift[i.url] = (seg, cat)
    assert not drift, f"id category segment != category: {drift}"


def test_item_id_date_segment_matches_date():
    drift = {}
    for i in archive.internal_items():
        iid = str(i.meta.get("item_id", ""))
        date = str(i.meta.get("date", ""))
        m = ID_RE.match(iid)
        if not m or len(date) < 7:
            continue
        ym = iid.split("-")[2][:4]
        expected = date[2:4] + date[5:7]
        if ym != expected:
            drift[i.url] = (ym, expected, date)
    assert not drift, f"id YYMM segment != frontmatter date: {drift}"


def test_external_items_have_required_fields():
    bad = {}
    for i in archive.external_items():
        miss = [k for k in ("category", "title", "date") if not i.meta.get(k)]
        if miss:
            bad[i.url] = miss
    assert not bad, f"external items missing fields: {bad}"


def test_exit_with_status_helper_exists():
    """The toolkit must expose a way to exit on the LIVE accumulated exit code,
    not a stale by-value import (the bug that silently neutered CI)."""
    assert hasattr(archive, "exit_with_status"), \
        "archive.exit_with_status missing; scripts cannot fail CI reliably"
