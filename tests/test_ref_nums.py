"""Reference-numbering guard (scripts/fix_ref_nums.py).

The critical property: in --check-only mode the script must EXIT NONZERO when it
finds a gap or mismatch, so CI fails. It previously printed complaints but exited
0 (stale by-value import of archive.exit_code), making the CI guard a no-op.
"""
import textwrap

GAP_FIXTURE = "scripts/ref_num_test_files/simple_gap.md"

CLEAN_DOC = textwrap.dedent("""\
    ## Title

    A claim with a citation [1] and another [2].

    ## References
    [1] First source.

    [2] Second source.
    """)


def test_check_only_exits_nonzero_on_gap(run_script):
    r = run_script("fix_ref_nums.py", "--check-only", GAP_FIXTURE)
    assert r.returncode != 0, (
        "fix_ref_nums --check-only must fail CI on a detected gap; "
        f"got exit 0.\nstdout:\n{r.stdout}"
    )


def test_check_only_exits_zero_on_clean_file(tmp_path, run_script):
    f = tmp_path / "clean.md"
    f.write_text(CLEAN_DOC, encoding="utf-8")
    r = run_script("fix_ref_nums.py", "--check-only", str(f))
    assert r.returncode == 0, (
        f"clean file should pass.\nstdout:\n{r.stdout}\nstderr:\n{r.stderr}"
    )


def test_parse_detects_gap_logic():
    """Unit-level proof the gap detector itself works (independent of exit code)."""
    import fix_ref_nums as frn
    body = "text [21] more [3,4]"
    brackets, _supers, style = frn.parse_ref_nums(body)
    assert style == "brackets"
    assert brackets == ["21", "3", "4"]


# --- Range notation: [3–5] / [3-5] / [1, 3–5, 7] must expand to individuals ---

def test_endash_range_expands():
    import fix_ref_nums as frn
    brackets, _s, style = frn.parse_ref_nums("governance [3–5].")
    assert style == "brackets"
    assert brackets == ["3", "4", "5"]


def test_hyphen_range_expands():
    import fix_ref_nums as frn
    brackets, _s, _ = frn.parse_ref_nums("see [3-5]")
    assert brackets == ["3", "4", "5"]


def test_mixed_list_and_range_expands():
    import fix_ref_nums as frn
    brackets, _s, _ = frn.parse_ref_nums("see [1, 3–5, 7]")
    assert brackets == ["1", "3", "4", "5", "7"]


def test_cfa_paper_passes_check_only(run_script):
    """cfa-paper.md cites [3–5] (en-dash range) in the abstract and body; once
    ranges are understood, the check must pass (refs are NOT actually uncited)."""
    r = run_script("fix_ref_nums.py", "--check-only", "cfa-paper.md")
    assert r.returncode == 0, (
        f"cfa-paper should pass once ranges are parsed.\nstdout:\n{r.stdout}\n"
        f"stderr:\n{r.stderr}"
    )
