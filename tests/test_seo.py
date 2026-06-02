"""Pure helpers of scripts/check_seo.py (the scheduled render-time SEO gate).

The full check needs a built site (run in the seo-check workflow); these cover
the parsing/counting logic without a build.
"""
import check_seo


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
