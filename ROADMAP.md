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
Reference: `ZENSICAL-MIGRATION-KT.md` (sister-repo lessons) — but note papers'
hardest part (per-page scholarly `<head>` metadata) is NOT covered there, since
codecraft injects none. See the feasibility findings below.

**Approach (decided after analysis):** keep canonical `*.md` at repo root; a
Python assembler (reusing `archive.py`'s `internal_items()`/`external_items()`/
`item.meta`) generates a disposable `build/` MkDocs tree; `zensical build`
renders `build/site/`. All presentation chrome — visible *and* `<head>` — is
**template-driven from frontmatter via `overrides/main.html`**, exactly as
Jekyll's `_layouts/default.html` does today (Liquid → Minijinja). The assembler
does NOT inject extras into the markdown body (that would pollute the TOC and
edit/source links). Confirmed feasible: Zensical 0.0.43's `base.html` exposes
`{% block extrahead %}` and `{% block content %}`, supports `theme.custom_dir`,
and reads `page.meta.*`.

- [ ] **Spike first (5–6 docs).** Acceptance test is not "does it build" but:
      does `overrides/main.html` emit correct `citation_*` + JSON-LD for an
      `author` doc, an `authors` doc (e.g. `prog-a`), and the one DOI doc
      (`cfa-paper`)? Plus inline `<figure>`/`<img>`/tables render; abstract +
      byline + colophon show; URLs sane. (Apply the §9 KT log discipline:
      `NO_COLOR=1 TERM=dumb`, redirect to file, strip ANSI, grep — never paste a
      raw Zensical log into the session.)
- [ ] **Assembler** (`scripts/build_site.py`): emit `build/docs/<slug>.md`
      (keeping the scholarly frontmatter — do NOT slim to title-only, the
      template needs `item_id`/`author(s)`/`doi`/`keywords`/`abstract`/`version`),
      a categorized `build/docs/index.md`, copy `assets/`, copy CSS, write
      `mkdocs.yml`. External items → outbound links in the index only, never a
      local page (mirror `generate_index.py`).
- [ ] **`overrides/main.html`** (the heart): port `default.html` logic to
      Minijinja — `{% block extrahead %}` for `citation_*` meta + JSON-LD
      (`ScholarlyArticle`/`TechArticle`/`WebPage` by category) + DOI + canonical
      PDF; `{% block content %}` for byline (both `author`/`authors`), the
      `item ID · version · PDF` colophon, abstract, and keywords, then `super()`.
- [ ] **Extensions** in generated `mkdocs.yml`: `admonition`, `pymdownx.details`,
      `attr_list`, `md_in_html` (needed for `<figure>`/`<img>` and `about.md`'s
      `<dl>`/`<details>`), `toc: permalink`. Nav from the 7 MECE **categories**
      (NOT the `tags` plugin).
- [ ] **Redirects:** inventory current Jekyll URL shape (`/papers/slug.html` vs
      `/slug/`); self-generate meta-refresh stubs for any internal doc whose URL
      would move (don't trust `mkdocs-redirects`). Stable citable URLs are a hard
      requirement; re-verify every `index.md` + `.external-items.yml` entry.
- [ ] **Styling:** `assets/css/zensical-extra.css` — custom properties + heading
      rules + verbatim `@media print` block + mobile `img` rule. Pick a serif web
      font echoing the PDF (TeX Gyre Pagella / Inconsolata), not codecraft's
      Open Sans — an author design call.
- [ ] **Internal link cleanup:** harvest `unresolved link reference` warnings
      from the build as a worklist; fix. (Keeps the scheduled lychee external
      check.)
- [ ] **Test-first** (`tests/test_site_build.py`): assert the generated `build/`
      tree contract WITHOUT invoking `zensical build` — one page per published
      doc, scholarly frontmatter retained, `overrides/main.html` present with the
      required blocks, redirect stubs present, valid `mkdocs.yml` with required
      extensions, CSS carried. Honest-failure exit discipline
      (`archive.exit_with_status`). `xfail(strict=True)` tripwires for not-yet-met
      goals.
- [ ] **PDFs unchanged:** `scripts/pandoc.py` reads canonical source `.md`, so it
      ports untouched; just ensure the assembler never strips fields it needs
      from the *source* (it only governs the *built* page).
- [ ] **Publish workflow:** `./build.sh` → deploy `build/site/` to Pages; retire
      the Jekyll auto-build. Pin all actions to `node24` runtimes (verify each).
- [ ] **Cutover & cleanup:** once live and URLs verified, retire `_config.yml`,
      `_layouts/`, `_includes/`, `index.md`'s `layout: meta` (keep in git
      history). Leave `docs/conventions.md`, `about.md`, `scripts/`, `tests/`
      untouched. `about.md` keeps its `<dl>`/`<dt>` HTML — `archive.py`'s
      `categories()` parses `<dt>` from source.

---

## Housekeeping / deferred
- [x] Removed `.item-id-convention.md` (content now in `docs/conventions.md`)
- [ ] Keep the Dependabot security tab clean as standing hygiene (see AGENTS.md)
- [ ] `.todo.txt` legacy notes ("collapse tags into keywords") — fold into Phase 2
