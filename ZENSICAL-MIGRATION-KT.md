# Knowledge-Transfer Prompt: Migrating *Codecraft Papers* from Jekyll to Zensical

> **Audience:** the AI that maintains `/home/daniel/code/papers`.
> **Purpose:** you are migrating this repo's publishing platform from Jekyll (GitHub Pages,
> remote `minimal` theme) to **Zensical** — the actively-maintained MkDocs-Material successor.
> This document distills the lessons from doing exactly this migration in the sister repo
> `../codecraft.co`. That repo is a **working reference implementation** you can (and should)
> read. Where this prompt says "see codecraft," open the named file — don't reinvent it.
>
> **Scope boundary:** ROADMAP Phase 4 says *do not migrate before the quality phases land.*
> This document is the plan for *when* you migrate, plus a recommended de-risking spike. It
> does not authorize starting before the author says so.

---

## 0. Working-reference paths (in `../codecraft.co`)

| What | Path |
|---|---|
| The decision block + migration mechanics | `../codecraft.co/AGENTS.md` (search "Publishing platform: Zensical") |
| **The assembler** (heart of the approach) | `../codecraft.co/scripts/build_site.py` |
| The build pipeline | `../codecraft.co/build.sh` |
| House styling + print CSS | `../codecraft.co/assets/css/zensical-extra.css` |
| The prover test | `../codecraft.co/tests/test_site_build.py` |
| The migration milestone (caveats) | `../codecraft.co/ROADMAP.md` (M3.6) |
| The *original* assembler pattern both repos mirror | `../tti/home/` (`assemble.py`, `mkdocs.yml`, `build.sh`, `requirements.txt`) |

---

## 1. Decision & rationale

Jekyll is **blog-oriented** and, on GitHub Pages, ties you to a Ruby gem surface and a remote
theme you don't control. *Codecraft Papers* is the opposite of a blog: a curated, citable
scholarly archive with stable IDs, formal references, and per-document PDFs. **Zensical** (built
on MkDocs-Material) is:

- **Python-native** — same toolchain as your existing `scripts/` (`archive.py`, `pandoc.py`,
  `generate_index.py`). No second language runtime.
- **Publication-oriented** — first-class TOC/nav, search, admonitions, MkDocs `.md`↔`.md`
  cross-linking (directly useful for your cross-references and citations).
- **Actively maintained** — the MkDocs-Material team's forward path.

**De-risk with a spike before committing the whole corpus.** Pick **5–6 representative
documents** that exercise the trickiest cases and migrate only those first:

- one with embedded HTML (`<figure>`/`<img>`/raw tables) — e.g. anything in `assets/`-heavy docs;
- one with a long formal `References` section and many inline `[N]` citations (e.g. `kspqs.md`);
- one with `authors:` (the plural list form, e.g. `prog-a.md`) **and** one with singular `author`;
- one of each structurally distinct category if cheap (Paper, Analysis, Primer);
- one with a committed `pdf_url`.

Build the spike, eyeball the rendered output, fix the assembler, *then* run the full corpus.
codecraft did a 6-essay spike before its full 121-doc build; it caught the inline-HTML and
redirect issues early.

> **Calibration / honesty:** Zensical is **very early** (codecraft pins `zensical>=0.0.43`).
> Its mkdocs-plugin compatibility is narrow (see §5), and nav/TOC design in codecraft was left
> explicitly **provisional** — pending a later milestone. Treat the platform as capable but
> immature: prove things with builds, don't assume parity with mature MkDocs-Material.

---

## 2. The assembler model (the core pattern)

**Keep your canonical source markdown exactly where it lives** (root-level `*.md`, slug ==
filename — same as today). Do **not** sprinkle MkDocs-isms into your source. Instead, a Python
**assembler** generates a *disposable* MkDocs tree:

```
build/
  mkdocs.yml                  generated config
  docs/
    index.md                  the categorized TOC
    <slug>.md                 one slimmed page per published document
    assets/...                images copied from repo assets/
    stylesheets/extra.css     your house CSS, copied in
    <legacy-path>/index.html  redirect stubs (see §5)
  site/                       zensical build output (what you deploy)
```

Then `zensical build` (run from inside `build/`) renders `build/site/`.

- **`build/` is gitignored and disposable** — regenerate any time. Your repo already gitignores
  `build/` (it's in `.gitignore`), so this slots in cleanly.
- This avoids colliding with your existing `docs/` (which holds `conventions.md` — leave it
  alone) and keeps source markdown free of build concerns.
- One command wraps it: `./build.sh` (assemble → build). Mirrors `../tti/home/build.sh`.

The assembler's shape (from `../codecraft.co/scripts/build_site.py`):

```python
def assemble(root, out_dir):
    docs = os.path.join(out_dir, "docs")
    if os.path.isdir(out_dir):
        shutil.rmtree(out_dir)          # disposable: wipe & regenerate
    os.makedirs(docs)
    items = iter_items(root)            # parse frontmatter; skip retired / non-docs
    for it in items:                    # one slimmed page per doc
        write(docs / f"{it.slug}.md", page_markdown(it))
    write(docs / "index.md", build_index(items))   # TOC
    copytree(root/"assets", docs/"assets")          # images
    copyfile(root/"assets/css/zensical-extra.css", docs/"stylesheets/extra.css")
    write_redirect_stubs(docs, items)               # §5
    yaml.safe_dump(build_mkdocs_config(items), out_dir/"mkdocs.yml")
```

> **Papers-specific:** you already have `archive.py` with `internal_items()` /
> `external_items()` and `item.meta`. **Reuse them** in the assembler instead of re-parsing
> frontmatter from scratch — that keeps category/ID logic in one place. (codecraft had no such
> module, so its assembler parses YAML inline; you're better positioned.) `external_items()`
> documents have **no local page** — emit them into the index as outbound links only (mirror
> how `generate_index.py` already merges `.external-items.yml`), never as `docs/*.md`.

---

## 3. Frontmatter slimming

A built MkDocs page keeps **only what the page needs** — for codecraft that was `title` + `tags`.
Everything Jekyll-only is dropped *from the built page* but **stays on the canonical source**.

For **papers**, slim the page frontmatter to:

```yaml
---
title: "KERI's Strategy for Post-Quantum Security"
---
```

Drop from the *built page* (keep on source): `date`, `category`, `item_id`, `pdf_url`,
`abstract`, `keywords`, `author`/`authors`, `version`, `revision_date`, `language`, `layout`.

Notes specific to papers:
- **`abstract` and title are NOT repeated in the body** (your house rule — the Jekyll `meta`
  layout rendered them). On Zensical there is no such layout, so the assembler must **render the
  abstract into the page** itself (e.g. as an italic lead paragraph or a `!!! abstract`
  admonition) right after the `# {title}` — otherwise the abstract disappears from the published
  page. Decide the treatment during the spike.
- `item_id`, `version`, `category` don't belong in page frontmatter, but you **do** want them
  visible somewhere on the rendered page (a small citation/colophon footer) since these are
  *citable* documents. Have the assembler emit that footer from the source meta.
- Papers has **no `comments`** (that was a WordPress-export artifact unique to codecraft); ignore
  codecraft's "Original discussion" admonition logic.

---

## 4. Critical `markdown_extensions`

These are not optional. Inline HTML (`<figure>`, `<img>`, raw tables) **will not render** without
the first two. Use this exact set (codecraft's, which is the right baseline for papers):

```yaml
markdown_extensions:
  - admonition          # note/warning/abstract blocks
  - pymdownx.details    # collapsible <details> blocks
  - attr_list           # {: ...} attributes on elements  ← needed for inline HTML
  - md_in_html          # render Markdown inside raw HTML  ← needed for <figure>/<img>
  - toc:
      permalink: true   # anchor links on headings (helps citable deep-links)
```

Consider adding, for papers' richer content (the `../tti/home` config carries these and they're
harmless):

```yaml
  - pymdownx.superfences   # advanced/nested code fences; required if you ever add Mermaid
  - pymdownx.tabbed:
      alternate_style: true
```

Theme/plugins (from codecraft's generated `mkdocs.yml`):

```yaml
theme:
  name: material
  favicon: assets/favicon.png
  features:
    - navigation.sections
    - navigation.top
    - navigation.indexes
    - content.code.copy
    - search.highlight
    - search.suggest
    - toc.follow
extra_css:
  - stylesheets/extra.css
plugins:
  - search
```

> codecraft also enabled the `tags` plugin because it uses multi-valued tags. **Papers uses a
> single MECE `category`, not tags — do NOT add the `tags` plugin or `navigation` based on tags.**
> Build your nav/sections from `category` instead (the seven categories in
> `docs/conventions.md`: Specifications · Papers · Analyses · Primers · Comparisons · Guidance ·
> Positions), mirroring the structure already in `index.md` and `generate_index.py`.

---

## 5. Redirects — do **NOT** trust the plugin

**Zensical's mkdocs-plugin compatibility is narrow** — in the codecraft migration we observed
essentially only a mkdocstrings shim working. `mkdocs-redirects` may simply **not fire**. So we
**self-generate meta-refresh HTML redirect stubs** straight into the build tree.

This matters **more for papers than for codecraft**, because papers is built around **persistent
document IDs and stable, citable URLs**. A migration that silently breaks an existing URL breaks a
citation in someone's published work. Treat URL preservation as a hard requirement.

The stub the assembler writes at each legacy path (`build/docs/<legacy-path>/index.html`):

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="0; url=/kspqs/">
<link rel="canonical" href="https://dhh1128.github.io/papers/kspqs/">
<title>Redirecting…</title>
</head>
<body>
<p>This page has moved to <a href="/kspqs/">/kspqs/</a>.</p>
</body>
</html>
```

The assembler builds these from each doc's old URL → new URL mapping (codecraft drove this off a
`redirect_from` frontmatter list). **Papers has no `redirect_from` field today**, so first
inventory what URL shape Jekyll currently serves vs. what Zensical/MkDocs will serve, then:

- Compare current Jekyll URLs (e.g. `/papers/kspqs.html` or `/papers/kspqs/`) against MkDocs'
  default (`/papers/kspqs/`). Where they differ, you need a stub.
- If they already match (Jekyll's `minimal` theme with `slug.md` → `/slug.html`), add stubs from
  the `.html` form to the directory form so old citation links keep resolving.
- Verify **every** entry in `index.md` and `.external-items.yml` still resolves after the cutover.
  External items are off-site and unaffected; internal ones must not move.

Confirm the actual current URL shape during the spike — don't assume.

---

## 6. Styling carry-over

Material is themable via `extra_css` using **CSS custom properties** + targeting
`.md-typeset` headings. Port your house look into a single
`assets/css/zensical-extra.css` (the assembler copies it to `build/docs/stylesheets/extra.css`).

The custom properties that matter:

```css
:root {
  --md-primary-fg-color: #491705;     /* header/nav brand colour */
  --md-accent-fg-color:   #914f37;
  --md-typeset-a-color:   #914f37;     /* link colour */
  --md-text-font:         "Open Sans"; /* body */
}
.md-typeset h1, .md-typeset h2, .md-typeset h3 { /* heading face/colours */ }
```

Fonts come in via Google Fonts `@import` at the top of the file:

```css
@import url('https://fonts.googleapis.com/css2?family=...&display=swap');
```

> **Papers-specific:** your *screen* brand should match your **PDF** typography for a coherent
> scholarly identity. `scripts/pandoc.py` sets `mainfont="TeX Gyre Pagella"` (a Palatino) and
> `monofont="Inconsolata"`. Pick web fonts that echo that (a serif body, not codecraft's Open
> Sans, unless you want the two collections to look different on purpose). This is a design call
> for the author — surface it, don't silently inherit codecraft's browns/condensed headings.

**Carry the `@media print` block verbatim** — it's what makes a document print cleanly
*without the sidebar/header/footer*, full-width. This is the exact block from codecraft's
`zensical-extra.css`:

```css
/* ---- Print: clean, sidebar-free, full-width essay ---- */
@media print {
  .md-header,
  .md-tabs,
  .md-sidebar,
  .md-footer,
  .md-nav,
  .md-content__button,
  .md-source,
  .md-top {
    display: none !important;
  }
  .md-main__inner,
  .md-content,
  .md-content__inner {
    margin: 0 !important;
    padding: 0 !important;
    max-width: 100% !important;
  }
  .md-grid {
    max-width: 100% !important;
  }
  .md-typeset {
    color: #000;
  }
  /* Expand any collapsed <details> so it prints in full. */
  .md-typeset details {
    display: block;
  }
  .md-typeset details > summary {
    display: none;
  }
}
```

Also keep the mobile-safety rule so images never overflow:

```css
.md-typeset img { max-width: 100%; height: auto; }
```

(Note: browser "print to PDF" is a *convenience*. Your **authoritative** PDFs still come from
pandoc — see §10. The print CSS just makes the web page printable in a pinch.)

---

## 7. Free internal link-checker

`zensical build` emits `unresolved link reference` / `page does not exist` warnings with
**file:line**. Treat that output as a **ready-made worklist** of broken internal links — run the
build, collect the warnings, fix them. codecraft surfaced ~138 such warnings (legacy
`/category/…` and stale cross-essay links) this way.

This is **especially valuable for papers** because:
- MkDocs natively resolves `.md`↔`.md` cross-links, which is exactly the idiom for your
  inter-document cross-references.
- Your References/citations include internal pointers; the build flags any that rot.

It does **not** replace your external link-check (the scheduled lychee CI job stays). It's a free
*internal*-link gate on top.

---

## 8. Test-first toolkit

This repo already lives by "every quality goal is a script + a `--check-only` checker + a pytest
prover," red→green. The assembler is no exception:

- Write `scripts/build_site.py` **and** `tests/test_site_build.py`; see the test go **red**
  before the assembler exists, then **green**. Report both observations (your standing rule).
- The prover tests the **structural contract without invoking the heavy `zensical build`** — it
  asserts on the generated `build/` tree (one page per published doc, slim frontmatter, abstract
  rendered, redirect stubs present, valid `mkdocs.yml` with the required extensions, CSS carried
  over). codecraft's `tests/test_site_build.py` is the template: copy its structure and adapt the
  assertions to papers (categories not tags; `item_id` in the colophon; abstract rendered).
- Use **`@pytest.mark.xfail(strict=True)` tripwires** for end-state goals not yet met, so CI
  stays green now but **auto-flags the moment the goal is reached** (then you flip the test to a
  hard assert). codecraft uses this pattern for "zero external images / alt-text everywhere";
  you'd use it for things like "every internal cross-ref resolves under the Zensical build" while
  links are still being cleaned.
- **Honest-failure rule (papers-specific):** your checkers accumulate via `archive.complain()`
  and exit through `archive.exit_with_status()` / live `archive.exit_code` — **never** a
  by-value `from archive import exit_code` (that bug silently neutered all three CI guards once;
  see your AGENTS.md / ROADMAP). Any new build-time guard must follow the same discipline.

---

## 9. ⚠️ Operational gotcha — read this before running anything

**Zensical's colorized build/serve logs can trip Anthropic's automated content filter and kill
your session with a FALSE "violates Usage Policy" error.** The dense ANSI escape sequences +
Unicode box-drawing characters in Zensical's pretty output look, to the filter, like something
they're not. **This cost the codecraft migration an entire session.**

Mitigations — apply **all** of them, always:

1. **Force plain output:** run zensical with `NO_COLOR=1 TERM=dumb`.
2. **Redirect to a file**, never straight to the conversation:
   `NO_COLOR=1 TERM=dumb zensical build > /tmp/zensical-build.log 2>&1`
3. **Strip residual ANSI** before reading:
   `sed -E 's/\x1b\[[0-9;]*[mGKHF]//g' /tmp/zensical-build.log > /tmp/zensical-build.clean.log`
4. **Surface only meaningful lines** — grep for warnings/errors; do **not** dump the raw log:
   `grep -E 'WARNING|ERROR|unresolved|does not exist' /tmp/zensical-build.clean.log`

codecraft's `build.sh` bakes step 1 in:

```bash
cd build
NO_COLOR=1 TERM=dumb "$ROOT/.venv-demo/bin/zensical" build
```

**NEVER paste a raw Zensical build/serve log into the conversation.** Treat its stdout as toxic
until cleaned. This is the single highest-risk operational item in the whole migration.

---

## 10. PDF generation (you already have this — keep it)

Your PDFs are produced by **pandoc reading the canonical markdown directly**
(`scripts/pandoc.py` → `--pdf-engine=xelatex`, with `scripts/pandoc/header.tex` + `pkgs.tex`,
TeX Gyre Pagella / Inconsolata, embedding `pdftitle`/`pdfauthor`/`pdfkeywords`/`pdfsubject` =
`item_id`+`version`). **This is entirely platform-independent.** It reads source `.md`, not
anything Jekyll- or Zensical-specific, so it **ports across the migration essentially unchanged.**

Two integration points worth wiring up:

- The **assembler can feed the same source meta** (title/author/keywords/`item_id`/`version`) so
  the on-page colophon (§3) and the PDF agree — single source of truth.
- Per your "Decisions": PDFs move to **CI artifacts** (Phase 3), with `pdf_url` becoming a
  validated/derived field. The Zensical publish workflow (§12) and the PDF-build workflow are
  separate jobs but can share the same Pages deploy — decide whether the site links to a
  CI-built PDF artifact URL or a committed `*.pdf`. (Several `*.pdf` are committed today;
  `kspqs.md` declares `pdf_url: kspqs.pdf`.)

Bottom line: **don't touch the PDF pipeline as part of the platform swap.** Just make sure the
assembler doesn't strip the frontmatter fields pandoc relies on from the *canonical source*
(it only slims the *built page* — §3).

---

## 11. `zensical serve` (live preview)

`zensical serve` gives you live preview during the spike. Two cautions:

- **Run it via a durable background mechanism** (a backgrounded process / your task harness), not
  a foreground call that blocks the session.
- **Rebuilding kills the serve.** The assembler `rmtree`s `build/` at the start of every run
  (§2). If a `zensical serve` is watching `build/` and you re-run the assembler, you pull the
  directory out from under it and the serve dies. Either stop serve before re-assembling, or
  serve a copy. Same `NO_COLOR=1 TERM=dumb` + redirect discipline from §9 applies to `serve`
  output too.

---

## 12. Ordered migration checklist

Do these in order. Earlier steps de-risk later ones.

1. **Spike (5–6 docs).** Stand up a throwaway assembler over the representative set from §1.
   Build with the §9 log discipline. Eyeball: inline HTML renders? abstract shows? citations and
   References intact? `author`/`authors` both handled? URLs sane? Fix the assembler until clean.
2. **Assembler (full).** Generalize to the whole corpus, reusing `archive.py`'s
   `internal_items()`/`external_items()`/`item.meta`. Emit `build/docs/<slug>.md`,
   `build/docs/index.md` (categorized), copy `assets/`, copy CSS, generate `mkdocs.yml`.
   Gitignore confirms `build/` already ignored.
3. **Frontmatter slim.** Built page = `title` (+ rendered abstract + colophon with
   `item_id`/`version`/`category`). Drop Jekyll-only keys from the *page*, keep on source (§3).
4. **Extensions.** Wire the exact `markdown_extensions` set from §4 into the generated config;
   verify inline `<figure>`/`<img>`/tables render.
5. **Redirects.** Inventory current Jekyll URL shape vs. MkDocs; self-generate meta-refresh stubs
   for every internal doc whose URL would otherwise move (§5). Re-verify every `index.md` link.
6. **Styling.** Author `assets/css/zensical-extra.css` (custom properties + heading rules + the
   verbatim `@media print` block + mobile `img` rule). Decide papers' own font/colour identity
   (echo the PDF) rather than copying codecraft's browns (§6).
7. **Internal link cleanup.** Run the build, harvest `unresolved link reference` / `page does not
   exist` warnings (§7, §9), fix them.
8. **Test-first gates.** `tests/test_site_build.py` (red→green), `xfail(strict=True)` tripwires
   for not-yet-met goals, honest-failure exit discipline (§8). Add the build to CI.
9. **PDFs.** Confirm `scripts/pandoc.py` still runs unchanged against source `.md`; ensure the
   slimming step never strips the meta pandoc needs (§10).
10. **Publish workflow.** GitHub Actions: `./build.sh` → deploy `build/site/` to GitHub Pages;
    retire the Jekyll auto-build. **Pin every action to its `node24`-runtime version** — the
    training-default tags (`actions/checkout@v4`, `actions/setup-python@v5`,
    `actions/upload-pages-artifact`, `actions/deploy-pages`, the cache/artifact family) mostly
    run on the **deprecated `node20`** runtime. Use `@v6` for `checkout`/`setup-python` and verify
    each action's runtime before committing:
    ```
    curl -sL https://raw.githubusercontent.com/<org>/<action>/<tag>/action.yml | grep -E '^\s*using:'
    ```
    Want `node24` / `composite` / `docker`; never `node20`. (This is already your AGENTS.md
    standing rule and matches `lychee-action ≥ v2.8.0`.)
11. **Cutover & cleanup.** Once the Zensical deploy is live and URLs verified, retire the legacy
    Jekyll files (`_config.yml`, `_layouts/`, `_includes/`, `index.md`'s `layout: meta`) — keep
    them in git history as reference, drop them from the build. Keep `docs/conventions.md`,
    `about.md`, `scripts/`, `tests/` untouched.

---

## 13. What's still uncertain (so you calibrate)

- **Zensical is pre-1.0** (`>=0.0.43`). Expect rough edges; prove with builds, not assumptions.
- **Plugin ecosystem is thin** — hence self-generated redirects (§5). Don't design anything that
  leans on an MkDocs plugin without first confirming Zensical actually runs it.
- **Nav/TOC was left provisional in codecraft.** For papers, the categorized index in
  `index.md` / `generate_index.py` is a strong starting structure, but the final nav (sections,
  ordering, cross-ref "see also") is a design decision the author should sign off — don't
  over-engineer it in the migration; get a faithful, link-clean build first.
- **`author` vs `authors`** is not yet normalized in the corpus (per AGENTS.md). The assembler —
  like `pandoc.py` already does — must accept **both** forms. Don't normalize as a side effect of
  the migration; that's a separate Phase 2 task.

---

*Reference implementation for everything above: `../codecraft.co` (read the files in §0).
Build discipline that protects your session: §9. Don't migrate before the author says the quality
phases have landed (ROADMAP Phase 4).*
