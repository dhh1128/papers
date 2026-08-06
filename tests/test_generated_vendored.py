"""Generated vendored documents (scripts/generate_vendored.py).

`amp-diff.md` is not a copy of `../entviz/docs/entviz-paper.md`; it is produced
from it by the transform in `.vendored-transforms.yml`. That is what makes
reverse drift impossible rather than merely detectable — the drift guard hashes
the *upstream*, so an edit made here is invisible to it, and the two files had in
fact diverged in three places while the guard reported "in sync".

The contract this file holds:

  * regeneration is faithful — the committed file is byte-for-byte what the
    transform produces (this is the check CI runs, and the one that fails if
    anyone hand-edits the published copy);
  * regeneration is idempotent;
  * every asserted step really is asserted: a changed title block, a figure the
    rewrite no longer maps, and an override whose upstream text moved must each
    FAIL rather than silently produce a lossy document;
  * an absent sibling skips with a notice, but fails under --require-upstream
    (cloud CI passes that flag, so a mis-wired checkout cannot pass vacuously).
"""
import copy

import pytest
import yaml


def _transform():
    import generate_vendored
    ts = generate_vendored.load_transforms()
    assert ts, "no transforms declared"
    return ts[0]


def _sibling_root_args(root):
    """CI checks the sibling out at `_upstream/<name>` inside the workspace; a
    working copy has it at `../<name>`. Find whichever exists so these tests have
    teeth in both places rather than skipping in CI."""
    t = _transform()
    if (root / t["upstream_repo"] / t["upstream_path"]).exists():
        return []
    return ["--upstream-root", "_upstream"]


def _upstream_text(root):
    t = _transform()
    for base in (root / t["upstream_repo"],
                 root / "_upstream" / t["upstream_repo"].rsplit("/", 1)[-1]):
        p = base / t["upstream_path"]
        if p.exists():
            return t, p.read_text(encoding="utf-8")
    pytest.skip(f"sibling {t['upstream_repo']} not checked out")


def _frontmatter(root, t):
    import generate_vendored
    return generate_vendored.frontmatter_of(
        (root / t["local"]).read_text(encoding="utf-8"))


# --- the contract CI depends on --------------------------------------------

def test_committed_copy_is_what_the_transform_produces(root, run_script):
    r = run_script("generate_vendored.py", "--check-only", *_sibling_root_args(root))
    assert r.returncode == 0, (
        "the committed vendored copy is not what the generator produces — it was "
        f"hand-edited, or upstream moved.\nstdout:\n{r.stdout}\nstderr:\n{r.stderr}")


def test_render_is_idempotent(root):
    import generate_vendored
    t, up = _upstream_text(root)
    fm = _frontmatter(root, t)
    once = generate_vendored.render(t, up, fm, t["local"])
    assert once is not None
    # Feeding the generated document back in as "upstream" is not meaningful
    # (the title block is gone), so idempotence is asserted the way it matters:
    # the same inputs always give the same bytes, and they match what is on disk.
    assert once == generate_vendored.render(t, up, fm, t["local"])
    assert once == (root / t["local"]).read_text(encoding="utf-8")


# --- every asserted step must actually assert ------------------------------

def test_changed_title_block_fails(root, monkeypatch):
    import archive
    import generate_vendored
    t, up = _upstream_text(root)
    monkeypatch.setattr(archive, "exit_code", 0, raising=False)
    mangled = up.replace("# Amplifying Difference", "Amplifying Difference", 1)
    assert generate_vendored.render(t, mangled, _frontmatter(root, t), "x") is None


def test_unmapped_figure_count_fails(root, monkeypatch):
    import archive
    import generate_vendored
    t, up = _upstream_text(root)
    monkeypatch.setattr(archive, "exit_code", 0, raising=False)
    dropped = up.replace("(assets/paper/fig-hero.svg)", "(assets/paper/fig-hero.png)", 1)
    assert generate_vendored.render(t, dropped, _frontmatter(root, t), "x") is None


def test_override_whose_upstream_text_moved_fails(root, monkeypatch):
    """The published copy differs from upstream in a few passages. If upstream
    rewrites one of them, that MUST be a build failure — silently keeping our
    version would discard an upstream revision nobody ever saw."""
    import archive
    import generate_vendored
    t, up = _upstream_text(root)
    monkeypatch.setattr(archive, "exit_code", 0, raising=False)
    fm = _frontmatter(root, t)
    for ov in t["overrides"]:
        old = ov["old"].replace("${spec_version}", str(t.get("spec_version", "")))
        mid = len(old) // 2
        edited = up.replace(old, old[:mid] + " REVISED UPSTREAM " + old[mid:], 1)
        assert edited != up, f"{ov['id']}: anchor not in upstream — fixture is stale"
        assert generate_vendored.render(t, edited, fm, "x") is None, (
            f"{ov['id']}: upstream rewrote the overridden passage and the build "
            f"still succeeded — the revision would be silently discarded")


def test_every_override_matches_upstream_exactly_once(root):
    t, up = _upstream_text(root)
    for ov in t.get("overrides", []):
        old = ov["old"].replace("${spec_version}", str(t.get("spec_version", "")))
        assert up.count(old) == 1, (
            f"override '{ov['id']}' matches upstream {up.count(old)} times; it must "
            f"match exactly once or it is not a safe, reviewable substitution")


def test_overrides_declare_whether_they_should_be_backported(root):
    """An override is either a publication-layer difference (correct forever) or
    prose upstream ought to adopt. Saying which is the whole point of keeping the
    list short and reviewed."""
    t = _transform()
    for ov in t.get("overrides", []):
        assert isinstance(ov.get("backport"), bool), f"{ov['id']}: no `backport` flag"
        assert ov.get("reason", "").strip(), f"{ov['id']}: no `reason`"


# --- sibling-absent behaviour ----------------------------------------------

def test_absent_sibling_skips_not_fails(tmp_path, run_script):
    r = run_script("generate_vendored.py", "--check-only",
                   "--upstream-root", str(tmp_path / "nowhere"))
    assert r.returncode == 0, (
        f"an absent sibling must skip with a notice.\nstdout:\n{r.stdout}")
    assert "SKIP" in r.stdout


def test_require_upstream_fails_when_sibling_absent(tmp_path, run_script):
    r = run_script("generate_vendored.py", "--check-only",
                   "--upstream-root", str(tmp_path / "nowhere"), "--require-upstream")
    assert r.returncode != 0, (
        "CI passes --require-upstream so a mis-wired second checkout fails loudly "
        f"instead of skipping every entry.\nstdout:\n{r.stdout}")


# --- the ledger and the transform must agree -------------------------------

def test_ledger_marks_the_generated_entry(root):
    ledger = yaml.safe_load((root / ".vendored-sources.yml").read_text(encoding="utf-8"))
    t = _transform()
    entry = next(e for e in ledger["sources"] if e.get("local") == t["local"])
    assert entry.get("generated_by") == "scripts/generate_vendored.py", (
        "the ledger must record that this entry is generated, so check_drift.py "
        "tells a human to regenerate rather than to reconcile prose by hand")
    assert entry.get("upstream_ref") == t.get("upstream_ref"), (
        "the ledger's pinned ref and the transform's must move together")


def test_ci_pins_the_same_upstream_ref(root):
    """CI regenerates against a pinned tag; if that pin and the ledger's diverge,
    CI is checking the file against a different upstream than the one we vendored."""
    ci = yaml.safe_load((root / ".github/workflows/ci.yml").read_text(encoding="utf-8"))
    steps = ci["jobs"]["test"]["steps"]
    checkout = next(s for s in steps
                    if str(s.get("uses", "")).startswith("actions/checkout")
                    and s.get("with", {}).get("repository"))
    assert checkout["with"]["ref"] == _transform()["upstream_ref"]


def test_generator_is_declared_in_the_scripts_readme(root):
    assert "generate_vendored.py" in (root / "scripts/README.md").read_text(encoding="utf-8")


def test_transform_declaration_shape(root):
    """Guard the declaration itself: a typo'd key would silently skip a step."""
    t = _transform()
    for key in ("local", "upstream_repo", "upstream_path", "upstream_ref",
                "strip_title_block", "frontmatter", "rewrites", "renumber_refs"):
        assert key in t, f"transform is missing `{key}`"
    assert t["frontmatter"] == "preserve-local"
    for rw in t["rewrites"]:
        assert isinstance(rw.get("expect"), int), (
            f"rewrite '{rw.get('id')}' has no `expect` count; without one a figure "
            f"added or dropped upstream goes unmapped in silence")


def test_generated_copy_has_no_stray_blank_line_inside_a_table(root):
    """Regression: the hand-copied file carried a blank line in the middle of
    Table 3, which splits the markdown table and renders the rest as literal
    pipe-text. Generating the file is what removed it."""
    lines = (root / _transform()["local"]).read_text(encoding="utf-8").splitlines()
    for i, ln in enumerate(lines[:-1]):
        if ln.startswith("|") and not lines[i + 1].strip():
            after = lines[i + 2] if i + 2 < len(lines) else ""
            assert not after.startswith("|"), (
                f"line {i + 2} is a blank line inside a markdown table")


def test_copy_only_entries_are_untouched(root):
    """Only the paper became generated. The figures, the adversarial companion,
    and the external spec item stay hand-vendored."""
    ledger = yaml.safe_load((root / ".vendored-sources.yml").read_text(encoding="utf-8"))
    generated = [e["local"] for e in ledger["sources"] if e.get("generated_by")]
    assert generated == ["amp-diff.md"]


def test_render_does_not_mutate_the_declaration(root):
    import generate_vendored
    t, up = _upstream_text(root)
    before = copy.deepcopy(t)
    generate_vendored.render(t, up, _frontmatter(root, t), t["local"])
    assert t == before
