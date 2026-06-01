"""Papers requirement check (scripts/check_requirements.py).

Two bugs made this check a no-op:
  1. It iterated index entries whose synthesized meta carried no `category`, so
     `cat_index` was always -1 and the Papers branch never ran (dead code).
  2. The branch referenced an undefined `required_fields` (latent NameError),
     and the script exited on a stale by-value `exit_code` anyway.

These tests pin the corrected behavior: the logic runs against REAL frontmatter,
flags a Paper missing a hard-required field, and the corpus passes cleanly.
"""
import check_requirements as cr

COMPLETE_PAPER = {
    "category": "Papers",
    "title": "A Title",
    "date": "2026-01-01",
    "abstract": "One paragraph.",
    "item_id": "CC-PAP-260101",
    "author": "Daniel Hardman",
    "pdf_url": "a-title.pdf",
}


def test_complete_paper_has_no_errors():
    errors, _warnings = cr.paper_problems(COMPLETE_PAPER)
    assert errors == [], f"unexpected errors: {errors}"


def test_paper_missing_abstract_is_flagged():
    meta = {k: v for k, v in COMPLETE_PAPER.items() if k != "abstract"}
    errors, _ = cr.paper_problems(meta)
    assert any("abstract" in e for e in errors), errors


def test_paper_missing_author_warns_not_errors():
    meta = {k: v for k, v in COMPLETE_PAPER.items() if k != "author"}
    errors, warnings = cr.paper_problems(meta)
    assert not any("author" in e for e in errors), errors
    assert any("author" in w for w in warnings), warnings


def test_authors_plural_satisfies_author_requirement():
    meta = {k: v for k, v in COMPLETE_PAPER.items() if k != "author"}
    meta["authors"] = [{"name": "Daniel Hardman"}]
    _errors, warnings = cr.paper_problems(meta)
    assert not any("author" in w for w in warnings), warnings


def test_real_papers_resolve_to_papers_category():
    """Regression for the dead-code bug: real frontmatter MUST resolve the
    Papers category (the synthesized index meta never did)."""
    import archive
    papers = [i for i in archive.internal_items()
              if archive.cat_index(str(i.meta.get("category", ""))) == cr.PAPER_CAT]
    assert papers, "no documents resolved to the Papers category from frontmatter"


def test_corpus_passes_requirements(run_script):
    r = run_script("check_requirements.py")
    assert r.returncode == 0, (
        f"corpus should satisfy requirements.\nstdout:\n{r.stdout}\nstderr:\n{r.stderr}"
    )
