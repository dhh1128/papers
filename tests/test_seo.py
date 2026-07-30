"""Pure helpers of scripts/check_seo.py (the scheduled render-time SEO gate).

The full check needs a built site (run in the seo-check workflow); these cover
the parsing/counting logic, and the scholarly-identifier rules, without a build.
"""
import check_seo
from archive import site_pdf_url

SLUG = "a-paper"
META = {"category": "Papers", "author": "Daniel Hardman", "item_id": "CC-PAP-260101"}


def _head(**overrides):
    """A minimal <head> that check_doc finds clean, with fields overridable."""
    f = {"canonical": f"{check_seo.BASE}{SLUG}.html",
         "og_image": f"{check_seo.BASE}assets/cards/{SLUG}.png",
         "description": "An abstract.",
         "pdf_url": site_pdf_url(SLUG),
         "doi": "10.2139/ssrn.6979798"}
    f.update(overrides)
    return (f'<link rel="canonical" href="{f["canonical"]}">'
            f'<meta property="og:image" content="{f["og_image"]}">'
            f'<meta name="twitter:card" content="summary_large_image">'
            f'<meta name="description" content="{f["description"]}">'
            f'<meta name="citation_title" content="A Paper">'
            f'<meta name="citation_author" content="Daniel Hardman">'
            f'<meta name="citation_pdf_url" content="{f["pdf_url"]}">'
            f'<meta name="citation_doi" content="{f["doi"]}">'
            '<script type="application/ld+json">'
            '{"@type":"ScholarlyArticle","author":[{"name":"Daniel Hardman"}],'
            '"identifier":["CC-PAP-260101"]}</script>')


def test_meta_contents_extracts_name_and_property():
    html = ('<meta name="citation_author" content="Ann">'
            '<meta property="og:image" content="http://x/c.png">')
    assert check_seo.meta_contents(html, "citation_author") == ["Ann"]
    assert check_seo.meta_contents(html, "og:image") == ["http://x/c.png"]


def test_expected_authors_handles_all_forms():
    assert check_seo.expected_authors({"author": "Daniel Hardman"}) == 1
    assert check_seo.expected_authors({"authors": [{"name": "A"}, {"name": "B"}]}) == 2
    assert check_seo.expected_authors({"author": ["A", "B", "C"]}) == 3
    assert check_seo.expected_authors({}) == 0


def test_ld_nodes_parses_valid_and_flags_invalid():
    good = '<script type="application/ld+json">{"@type":"ScholarlyArticle"}</script>'
    bad = '<script type="application/ld+json">{not json}</script>'
    assert check_seo.ld_nodes(good)[0]["@type"] == "ScholarlyArticle"
    assert "__bad__" in check_seo.ld_nodes(bad)[0]


def test_clean_head_has_no_findings():
    assert check_seo.check_doc(SLUG, META, _head()) == []


def test_citation_pdf_url_must_be_our_own_copy():
    """Scholar has to fetch it. SSRN's Delivery.cfm is Cloudflare-gated HTML."""
    ssrn = "https://papers.ssrn.com/sol3/Delivery.cfm/1.pdf?abstractid=1&mirid=1"
    errs = check_seo.check_doc(SLUG, META, _head(pdf_url=ssrn))
    assert any("citation_pdf_url" in e for e in errs), errs


def test_citation_pdf_url_for_another_document_is_caught():
    errs = check_seo.check_doc(SLUG, META, _head(pdf_url=site_pdf_url("other")))
    assert any("citation_pdf_url" in e for e in errs), errs


def test_citation_doi_must_be_a_doi():
    """Regression: a bare SSRN abstract id rendered as citation_doi."""
    errs = check_seo.check_doc(SLUG, META, _head(doi="6979798"))
    assert any("citation_doi" in e for e in errs), errs
