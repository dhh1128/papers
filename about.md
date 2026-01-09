---
title: "About the Archive"
author: "Daniel Hardman"
language: "en"
layout: meta
---

## Purpose

<cite>Codecraft Papers</cite> is an archive of technical and scholarly writings. Some are published elsewhere; some are self-published. Documents are categorized according to editorial intent, audience, and level of rigor. These categories are normative rather than descriptive: placement reflects an explicit judgment about the document’s purpose and quality, not merely its topic or length.

Documents classified as Papers are intended to function as citable technical literature. They are written in a formal, declarative style; they define scope and audience explicitly; and they are maintained as versioned works. Papers are expected to include an abstract, substantive argument or analysis, and appropriate citations. Revisions are made sparingly and transparently, with version identifiers indicating material changes.

Other categories may be exploratory, argumentative, or provisional in nature. These documents may evolve more freely and may not meet all of the formal requirements applied to Papers. Category distinctions are preserved deliberately to avoid ambiguity for readers, indexers, and downstream citation or reuse.

## Categories

The goal of this taxonomy is to ensure that categories are [mutually exclusive and collectively exhaustive](https://en.wikipedia.org/wiki/MECE_principle), so that each document belongs unambiguously to one category.

<dl>
<dt class="h3">Specifications</dt>
<dd>
<details>
<summary class="p">Documents whose primary purpose is to normatively define behavior such that independent implementations can be evaluated for conformance.</summary>
<h4>Assignment test</h4>
<p>If a reader could reasonably claim that an implementation is compliant or non-compliant with the document, it is a Specification.</p>

<h4>Key properties</h4>
<ul>
<li>Normative authority, explicit or implicit</li>
<li>Precise definitions, algorithms, or rules</li>
<li>Versioning is meaningful, but maturity is irrelevant (draft and stable specifications both qualify)</li>
</ul>
</details>
</dd>
<dt class="h3">Papers</dt>
<dd>
<details>
<summary class="p">Documents whose primary purpose is to present an original technical thesis, model, or design, supported by structured reasoning and evidence.</summary>
<h4>Assignment test</h4>
<p>If the document’s main contribution is a technical claim or proposal defended through analysis, and not a teaching guide or conformance target, it is a Paper.</p>

<h4>Key properties</h4>
<ul>
<li>Novelty or synthesis is central</li>
<li>Conclusions are primarily descriptive</li>
<li>May introduce frameworks, algorithms, or architectures without asserting normativity</li>
</ul>
</details>
</dd>
<dt class="h3">Analyses</dt>
<dd>
<details>
<summary class="p">Documents whose primary purpose is to examine and reason about an existing artifact, claim, or system in order to understand its properties, implications, or limitations.</summary>
<h4>Assignment test</h4>
<p>If the document’s value lies in explaining or critiquing something that already exists, rather than proposing a new artifact or advocating a position, it is an Analysis.</p>

<h4>Key properties</h4>
<ul>
<li>Object of analysis may be a standard, system, design, or argument</li>
<li>Conclusions are descriptive or evaluative, not prescriptive</li>
<li>No attempt to define correctness or to teach from first principles</li>
</ul>
</details>
</dd>
<dt class="h3">Primers</dt>
<dd>
<details>
<summary class="p">Documents whose primary purpose is to teach understanding and build reader competence or mental models.</summary>
<h4>Assignment test</h4>
<p>If the document is optimized for learning and orientation rather than novelty, critique, or prescription, it is a Primer.</p>

<h4>Key properties</h4>
<ul>
<li>Didactic structure</li>
<li>Explanatory examples and definitions</li>
<li>Success is measured by reader understanding, not persuasion or adoption</li>
</ul>
</details>
</dd>
<dt class="h3">Comparisons</dt>
<dd>
<details>
<summary class="p">Documents whose primary purpose is to compare two or more mechanisms, systems, or approaches along defined dimensions.</summary>
<h4>Assignment test</h4>
<p>If the document is explicitly structured as A versus B (or A versus B versus C), it is a Comparison.</p>

<h4>Key properties</h4>
<ul>
<li>Multiple subjects analyzed side by side</li>
<li>Emphasis on tradeoffs, differences, and equivalences</li>
<li>Distinct from Analyses by plurality of objects</li>
</ul>
</details>
</dd>
<dt class="h3">Guidance</dt>
<dd>
<details>
<summary class="p">Documents whose primary purpose is to enable correct decisions or actions in practice.</summary>
<h4>Assignment test</h4>
<p>If the central reader question is “What should I do?”, the document is Guidance.</p>

<h4>Key properties</h4>
<ul>
<li>Action-oriented recommendations</li>
<li>Best practices, policies, or codes of conduct</li>
<li>Content may evolve as conditions change</li>
</ul>
</details>
</dd>
<dt class="h3">Positions</dt>
<dd>
<details>
<summary class="p">Documents whose primary purpose is to advocate a stance about priorities, values, or direction.</summary>
<h4>Assignment test</h4>
<p>If the document’s conclusion is fundamentally “we should”, it is a Position.</p>

<h4>Key properties</h4>
<ul>
<li>Normative and persuasive by design</li>
<li>Grounded in technical realities but oriented toward judgment or policy</li>
<li>Distinct from Papers and Analyses by prescriptive intent</li>
</ul>
</details>
</dd>
</dl>

## Tiebreak Rules

If a document appears to fit multiple categories, apply the following rules in order:

1. Normative conformance overrides all; classify as Specification  
2. Advocacy overrides analysis; classify as Position  
3. Teaching overrides novelty; classify as Primer  
4. Action overrides explanation; classify as Guidance  
5. Multiple objects override single-object analysis; classify as Comparison  

If ambiguity remains, classify by the dominant conclusion type presented to the reader.

## Metadata Versus Categories

The following attributes are intentionally not categories and must be expressed as metadata instead:

- Document status (draft, stable, deprecated)  
- Maturity or version number  
- Narrative or parable style  
- Domain or topic area  
- Whether an artifact is a standard, draft, algorithm, or framework  

This separation preserves category clarity and prevents taxonomy drift.

This editorial policy exists to ensure consistency, clarity, and long-term maintainability of the archive.
