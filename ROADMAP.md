# Roadmap

The plan for hardening the Codecraft Papers archive: a tested toolkit and
rigorous CI first, then a quality/consistency pass, then PDFs, then a migration
from Jekyll to Zensical. Tick items as completed. See [AGENTS.md](AGENTS.md) for
vision and principles, [docs/conventions.md](docs/conventions.md) for schema.

_Created 2026-06-01._

**Locked decisions:** prose = propose-as-diffs only (never silently edited);
single MECE **category** per document (no tags); PDFs built in **CI as
artifacts** (`pdf_url` becomes derived/validated).

---

## Phase 0 — AI context & scaffolding
- [x] Write `AGENTS.md` (vision, principles, locked decisions, open questions)
- [x] Add `CLAUDE.md` redirect to `AGENTS.md`
- [x] Create `ROADMAP.md` (this file)
- [x] Consolidate schema + taxonomy + item-id rule into `docs/conventions.md`
      (replaced `.item-id-convention.md`, now removed)
- [x] Add a `README.md` with CI badge and quickstart

## Phase 1 — Testing discipline + rigorous CI _(the safety net; done first)_
- [x] Scaffold `tests/` (pytest) + `requirements.txt`
- [x] **Fix the CI no-op bug:** scripts imported `archive.exit_code` by value, so
      `check_requirements`, `generate_index`, and `fix_ref_nums --check-only` all
      exited 0 regardless of detected problems. Added `archive.exit_with_status()`
      and made scripts read the live `archive.exit_code`. _(red→green)_
- [x] **Fix the dead Papers check:** `check_requirements.py` evaluated synthesized
      index meta (no `category`), so the Papers branch never ran and referenced an
      undefined `required_fields`. Rewrote it to validate real frontmatter via
      `paper_problems()`. _(red→green)_
- [x] **Fix inverted ref-num flag:** `fix_ref_nums` passed `not check_only` to
      `complain`, so `--check-only` never failed on a gap. _(red→green)_
- [x] Tests: category parse, item-id format/uniqueness/segment-consistency,
      external-item fields, requirements logic, ref-num exit codes
- [x] Modernize CI → `ci.yml`: `node24` actions, runs guards + `pytest` on every
      push/PR; scheduled link-check bumped to `lychee-action@v2.8.0`/`checkout@v6`
- [x] Fix `make_item_id` docstring (`YYOOMM` → `YYMMOO`)
- [x] **Teach `fix_ref_nums` range notation** (`[3–5]`/`[3-5]`/`[1, 3–5, 7]`).
      The newly-working guard initially flagged `cfa-paper.md` refs [3–5] as
      "uncited" — but they ARE cited via en-dash ranges; the tool, not the
      document, was incomplete. Checker now expands ranges; the in-place fixer
      refuses range files rather than mangle them. _(red→green)_

## Phase 2 — Quality & consistency audit → backlog
- [ ] Normalize `author` vs `authors` across the corpus (start with `prog-a.md`)
- [ ] Backfill `keywords`/`abstract` on the ~9 thin documents (aold, crna, sss,
      svce, wbca, telco-ev-reqs, ai-coca, zh, x509-prob)
- [ ] Decide + apply a `version`/`revision_date` policy
- [ ] Add `validate_metadata.py` + test enforcing the full schema (graduate the
      warn-only fields to required as coverage completes)
- [ ] _(optional)_ deeper multi-persona content audit via a workflow
- [ ] Verify external-item entries in `.external-items.yml` still resolve

## Phase 3 — PDF pipeline (CI artifacts)
- [ ] Make `pandoc.py` reproducible; reconcile `author`/`authors` + missing fields
- [ ] Publish workflow builds one PDF per internal document, uploads artifacts
- [ ] `build_pdfs.py --check-only` + test: every published document has a current
      PDF; `pdf_url` validated against the produced artifact (graduate to required)
- [ ] Retire the committed `*.pdf` blobs once the build is proven
- [ ] Reconcile the dangling `pdf_url`s (currently 404 on the live site)

## Phase 4 — Jekyll → Zensical
- [ ] Port to `mkdocs.yml` + Material/Zensical (the `../tti/home` pattern:
      `requirements.txt` pins `zensical`, `build.sh` → `zensical build`, publish
      workflow)
- [ ] Preserve URLs/redirects, the categorized index, and the external-items merge
- [ ] Add JSON-LD `ScholarlyArticle` + citation metadata so indexers/AI see a
      scholarly archive, not a blog (the `.reorg-ideas.md` goals)
- [ ] Verify build parity (no broken links/images) before cutover

---

## Housekeeping / deferred
- [x] Removed `.item-id-convention.md` (content now in `docs/conventions.md`)
- [ ] Keep the Dependabot security tab clean as standing hygiene (see AGENTS.md)
- [ ] `.todo.txt` legacy notes ("collapse tags into keywords") — fold into Phase 2
