# scripts/

The durable toolkit for the Codecraft Papers archive. Each script should be
**idempotent**, support a **`--check-only`** mode (so CI can assert a goal
without mutating files), and exit with a **live, accurate status code**.

> Exit codes: scripts accumulate problems via `archive.complain()` (which bumps
> the module-global `archive.exit_code`) and must terminate via
> `archive.exit_with_status()` or `sys.exit(archive.exit_code)`. Never
> `from archive import exit_code` and exit on that name — it is a by-value copy
> captured at import time (always 0) and will silently let a script report
> problems yet pass CI.

Every quality goal pairs a script here with a prover test in
[`../tests`](../tests); CI runs both.

| Script | Purpose | `--check-only` |
|---|---|---|
| `archive.py` | Shared library: Item model, category parse, frontmatter load, id minting | — |
| `check_requirements.py` | Indexed files exist; Papers carry required metadata | (always read-only) |
| `generate_index.py` | Regenerate the categorized `index.md` | ✓ |
| `fix_ref_nums.py` | Normalize inline/expanded reference numbering (ACM style) | ✓ |
| `pandoc.py` | Render a document to PDF | — |

Planned (see the M-table in [../ROADMAP.md](../ROADMAP.md)):
`validate_metadata.py`, `build_pdfs.py`, a citation/link reconciler.
