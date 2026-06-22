"""Drift guard (scripts/check_drift.py).

This archive vendors documents and figures from sibling repos (entviz,
entviz-adversarial); ``.vendored-sources.yml`` pins each upstream's sha256 at
vendoring time. The guard's contract:

  * a **fail**-severity source (the papers, their figures) that diverges from its
    pin MUST exit nonzero, so CI/`publish.py --check` catches an upstream that ran
    ahead of the published copy;
  * a **warn**-severity source (the spec, which the papers analyze at a pinned
    version and may intentionally lag) is advisory and MUST NOT fail;
  * a source whose sibling repo is **absent** (cloud CI has no sibling checkout)
    is SKIPPED with a visible notice — never a silent pass, never a failure.

The real, committed ledger must also be in sync (or skip) so the guard is green.
"""
import hashlib

import yaml


def _sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def _write(p, text):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


def _ledger(tmp_path, entries):
    p = tmp_path / ".vendored-sources.yml"
    p.write_text(yaml.safe_dump({"sources": entries}), encoding="utf-8")
    return p


# --- unit-level: the status classifier itself ------------------------------

def test_entry_status_ok_and_drift(tmp_path):
    import check_drift
    _write(tmp_path / "up/docs/x.md", "hello")
    entry = {"upstream_repo": "up", "upstream_path": "docs/x.md",
             "sha256": _sha("hello"), "severity": "fail"}
    assert check_drift.entry_status(entry, str(tmp_path)) == "ok"
    entry["sha256"] = _sha("changed upstream")
    assert check_drift.entry_status(entry, str(tmp_path)) == "drift"


def test_entry_status_skips_absent_upstream(tmp_path):
    import check_drift
    entry = {"upstream_repo": "nope", "upstream_path": "docs/x.md",
             "sha256": "abc", "severity": "fail"}
    assert check_drift.entry_status(entry, str(tmp_path)) == "skip-upstream"


def test_entry_status_flags_missing_local(tmp_path):
    import check_drift
    _write(tmp_path / "up/x.md", "body")
    entry = {"local": "gone.md", "upstream_repo": "up", "upstream_path": "x.md",
             "sha256": _sha("body"), "severity": "fail"}
    assert check_drift.entry_status(entry, str(tmp_path)) == "missing-local"


# --- CLI exit-code contract (what CI actually depends on) ------------------

def test_check_only_exits_nonzero_on_fail_drift(tmp_path, run_script):
    _write(tmp_path / "up/x.md", "new upstream content")
    led = _ledger(tmp_path, [
        {"upstream_repo": "up", "upstream_path": "x.md",
         "sha256": _sha("the content we vendored"), "severity": "fail"}])
    r = run_script("check_drift.py", "--check-only",
                   "--ledger", str(led), "--root", str(tmp_path))
    assert r.returncode != 0, (
        f"fail-severity drift must fail CI.\nstdout:\n{r.stdout}\nstderr:\n{r.stderr}")


def test_warn_severity_drift_does_not_fail(tmp_path, run_script):
    _write(tmp_path / "up/spec.md", "version 11")
    led = _ledger(tmp_path, [
        {"upstream_repo": "up", "upstream_path": "spec.md",
         "sha256": _sha("version 10"), "severity": "warn"}])
    r = run_script("check_drift.py", "--check-only",
                   "--ledger", str(led), "--root", str(tmp_path))
    assert r.returncode == 0, (
        f"warn-severity drift must be advisory only.\nstdout:\n{r.stdout}\nstderr:\n{r.stderr}")


def test_absent_sibling_skips_not_fails(tmp_path, run_script):
    led = _ledger(tmp_path, [
        {"upstream_repo": "absent-repo", "upstream_path": "x.md",
         "sha256": "abc", "severity": "fail"}])
    r = run_script("check_drift.py", "--check-only",
                   "--ledger", str(led), "--root", str(tmp_path))
    assert r.returncode == 0, (
        f"absent sibling must skip, not fail.\nstdout:\n{r.stdout}\nstderr:\n{r.stderr}")


def test_real_ledger_in_sync(run_script):
    """The committed ledger's pins match the current sibling sources — or skip if
    the siblings aren't checked out. Either way the guard is green."""
    r = run_script("check_drift.py", "--check-only")
    assert r.returncode == 0, (
        f"real ledger drift or error.\nstdout:\n{r.stdout}\nstderr:\n{r.stderr}")
