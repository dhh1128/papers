"""Corpus-wide metadata schema validator (scripts/validate_metadata.py).

Supersedes the old Papers-only check. Tiers (per docs/conventions.md):
  ERROR (fails CI): title, date, category, item_id, author/authors;
    Papers + Specifications additionally require version + revision_date.
  WARN (advisory):  abstract, keywords — graduate to ERROR once the remaining
    thin docs are backfilled (Phase 2).
"""
import validate_metadata as vm

COMPLETE_PAPER = {
    "category": "Papers",
    "title": "A Title",
    "date": "2026-01-01",
    "item_id": "CC-PAP-260101",
    "author": "Daniel Hardman",
    "abstract": "One paragraph.",
    "keywords": "a, b",
    "version": 1.0,
    "revision_date": "2026-01-01",
}


def _drop(d, *keys):
    return {k: v for k, v in d.items() if k not in keys}


def test_complete_paper_has_no_errors():
    errors, _ = vm.field_problems(COMPLETE_PAPER)
    assert errors == [], errors


def test_missing_core_field_is_error():
    errors, _ = vm.field_problems(_drop(COMPLETE_PAPER, "title"))
    assert any("title" in e for e in errors), errors


def test_missing_author_is_error():
    errors, _ = vm.field_problems(_drop(COMPLETE_PAPER, "author"))
    assert any("author" in e for e in errors), errors


def test_authors_plural_satisfies_author():
    meta = _drop(COMPLETE_PAPER, "author")
    meta["authors"] = [{"name": "Daniel Hardman"}]
    errors, _ = vm.field_problems(meta)
    assert not any("author" in e for e in errors), errors


def test_paper_missing_version_is_error():
    errors, _ = vm.field_problems(_drop(COMPLETE_PAPER, "version"))
    assert any("version" in e for e in errors), errors


def test_paper_missing_revision_date_is_error():
    errors, _ = vm.field_problems(_drop(COMPLETE_PAPER, "revision_date"))
    assert any("revision_date" in e for e in errors), errors


def test_non_versioned_category_does_not_require_version():
    """A Primer (or other non-versioned category) needs no version/revision_date."""
    meta = {**_drop(COMPLETE_PAPER, "version", "revision_date"), "category": "Primers",
            "item_id": "CC-PRI-260101"}
    errors, _ = vm.field_problems(meta)
    assert not any("version" in e or "revision_date" in e for e in errors), errors


def test_missing_abstract_is_error():
    errors, _ = vm.field_problems(_drop(COMPLETE_PAPER, "abstract"))
    assert any("abstract" in e for e in errors), errors


def test_missing_keywords_is_error():
    errors, _ = vm.field_problems(_drop(COMPLETE_PAPER, "keywords"))
    assert any("keywords" in e for e in errors), errors


def test_corpus_passes_validation(run_script):
    r = run_script("validate_metadata.py")
    assert r.returncode == 0, (
        f"corpus should pass metadata validation.\nstdout:\n{r.stdout}\nstderr:\n{r.stderr}"
    )


def test_report_mode_runs_and_lists_abstract_gap(run_script):
    r = run_script("validate_metadata.py", "--report")
    assert r.returncode == 0, r.stderr
    assert "abstract" in (r.stdout + r.stderr).lower()
