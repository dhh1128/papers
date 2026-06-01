"""New-document scaffolder (scripts/new_doc.py) + archive.next_item_id.

Authoring should *produce* schema-valid docs, not rely on CI to reject invalid
ones. These tests pin: the next item-id is well-formed and one past the highest
ordinal already used that month, and the generated frontmatter stub passes the
metadata validator (including version/revision_date for Papers).
"""
import re

import yaml

import archive
import new_doc
import validate_metadata as vm

ID_RE = re.compile(r"^CC-[A-Z]{3}-\d{6}$")


def _fm(text):
    return yaml.safe_load(text.split("---", 2)[1])


def test_next_item_id_is_well_formed():
    iid = archive.next_item_id("Papers", "2099-07-15")
    assert ID_RE.match(iid) and iid.startswith("CC-PAP-9907"), iid


def test_next_item_id_starts_at_01_in_empty_month():
    assert archive.next_item_id("Primers", "2099-07-01").endswith("01")


def test_next_item_id_is_one_past_month_max():
    """Robust against corpus changes: compute the expected max from the corpus."""
    period = "2512"  # December 2025 is a busy month in the corpus
    used = [int(i.meta["item_id"].split("-")[2][4:])
            for i in archive.internal_items()
            if i.meta["item_id"].split("-")[2][:4] == period]
    expected = max(used) + 1
    assert archive.next_item_id("Papers", "2025-12-31") == f"CC-PAP-2512{expected:02d}"


def test_canonical_category_matches_by_prefix():
    assert new_doc.canonical_category("papers") == "Papers"
    assert new_doc.canonical_category("pos") == "Positions"
    assert new_doc.canonical_category("nonsense") is None


def test_slugify():
    assert new_doc.slugify("Hello, World! A Test") == "hello-world-a-test"


def test_stub_is_schema_valid_for_non_paper():
    text = new_doc.frontmatter_stub("My Title", "Primers", "2099-07-01", "CC-PRI-990701")
    errors, _ = vm.field_problems(_fm(text))
    assert errors == [], errors


def test_stub_is_schema_valid_for_paper_with_version():
    text = new_doc.frontmatter_stub("My Paper", "Papers", "2099-07-01", "CC-PAP-990701")
    fm = _fm(text)
    assert fm.get("version") and fm.get("revision_date"), fm
    errors, _ = vm.field_problems(fm)
    assert errors == [], errors
