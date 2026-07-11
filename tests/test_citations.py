"""Citation-style declaration + the ACM ref-num selection (archive.citation_style /
archive.acm_documents).

The `citations:` frontmatter enum is the single source of truth for whether the
standalone fix_ref_nums.py guard runs on a document. The repo-aware selection lives
in archive.acm_documents(); publish.py and ci.yml both source their file list from
it, so the two call sites can't drift and the exclusion travels with each document
(replacing the old `.hyperlinks-only` sidecar).
"""
import archive
import fix_ref_nums as frn
import validate_metadata as vm


def test_citation_style_defaults_to_acm():
    """A doc with no `citations` field is treated as acm (checked) — the safe
    default matching the old 'checked unless listed' posture."""
    assert archive.citation_style(archive.Item("nope.md", {})) == "acm"
    assert archive.citation_style(archive.Item("h.md", {"citations": "hyperlinks"})) == "hyperlinks"


def test_acm_documents_selects_only_acm():
    urls = {it.url for it in archive.acm_documents()}
    # A well-cited ACM paper is in; a hyperlinks doc and an author-date paper are out.
    assert "sda.md" in urls
    assert "x509-prob.md" not in urls      # citations: hyperlinks
    assert "kspqs.md" not in urls          # citations: author-date


def test_every_internal_doc_declares_a_valid_citation_style():
    bad = [it.url for it in archive.internal_items()
           if it.meta.get("citations") not in archive.CITATION_STYLES]
    assert not bad, f"docs missing/invalid citations: {bad}"


def test_validator_requires_citations():
    meta = {k: v for k, v in _COMPLETE.items() if k != "citations"}
    errors, _ = vm.field_problems(meta)
    assert any("citations" in e for e in errors), errors


def test_validator_rejects_unknown_citation_value():
    errors, _ = vm.field_problems({**_COMPLETE, "citations": "footnotes"})
    assert any("citations" in e and "footnotes" in e for e in errors), errors


def test_validator_accepts_each_known_citation_value():
    for style in archive.CITATION_STYLES:
        errors, _ = vm.field_problems({**_COMPLETE, "citations": style})
        assert not any("citations" in e for e in errors), (style, errors)


def test_acm_documents_pass_ref_num_check(run_script):
    """The selected acm set must pass fix_ref_nums --check-only: proves the new
    selection surfaces no new failures (no regression vs. the old sidecar)."""
    urls = sorted(it.url for it in archive.acm_documents())
    r = run_script("fix_ref_nums.py", "--check-only", *urls)
    assert r.returncode == 0, f"acm docs should pass.\nstdout:\n{r.stdout}\nstderr:\n{r.stderr}"


def test_non_acm_docs_are_not_acm_shaped():
    """Anti-silent-skip guard: a doc excluded from the ref check must not actually
    be ACM-shaped (inline [n] cites AND a numbered References section). If it is,
    it's mismarked and a real citation problem would go unchecked."""
    offenders = []
    for it in archive.internal_items():
        if archive.citation_style(it) == "acm":
            continue
        content = open(it.path, encoding="utf-8").read()
        body, end = frn.split_body_and_end(content)
        _, _, b_style = frn.parse_ref_nums(body)
        _, _, e_style = frn.parse_ref_nums(end)
        if b_style != "none" and e_style != "none":
            offenders.append(it.url)
    assert not offenders, f"non-acm docs that look ACM-shaped (mismarked?): {offenders}"


# A schema-complete internal doc's metadata, for the pure-function validator tests.
_COMPLETE = {
    "category": "Papers", "title": "T", "date": "2026-01-01",
    "item_id": "CC-PAP-260101", "author": "Daniel Hardman",
    "abstract": "One paragraph.", "keywords": "a, b",
    "version": 1.0, "revision_date": "2026-01-01", "citations": "acm",
}
