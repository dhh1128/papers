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
| `publish.py` | **Maintainer entry point.** Orchestrates the others: regenerate cards/descriptions/index + stale PDFs, `--revise` bumps a version, then validate | (writes) |
| `archive.py` | Shared library: Item model, category parse, frontmatter load, id minting (`next_item_id`), version helpers | — |
| `new_doc.py` | Scaffold a new document: mints the next `item_id`, writes a complete schema-valid frontmatter stub | (writes one file) |
| `validate_metadata.py` | Validate all docs against the schema; `--report` prints a coverage punch-list | (read-only) |
| `sync_descriptions.py` | Mirror each doc's `abstract` into a `description` field (the SEO meta description) | ✓ |
| `make_cards.py` | Render a 1200×630 social-share card (`og:image`) per doc → `assets/cards/<slug>.png` | ✓ |
| `generate_index.py` | Regenerate the categorized `index.md` | ✓ |
| `fix_ref_nums.py` | Normalize inline/expanded reference numbering (ACM style) | ✓ |
| `pandoc.py` | Render a document to PDF | — |

Planned (see [../ROADMAP.md](../ROADMAP.md)):
`build_pdfs.py`, a citation/link reconciler.
