---
title: "Identity Facets"
author: "Daniel Hardman"
thanks: "daniel.hardman@gmail.com"
date: 2026-07-09
category: Primers
item_id: CC-PRI-260701
language: "en"
version: "0.9"
revision_date: 2026-07-09
pdf_url: https://dhh1128.github.io/papers/if.pdf
abstract: |
  A single person is a mother, a CEO, a patient, and a citizen at once — and the law, the market, and good sense all insist that these be kept distinct. This primer argues that identity is fundamentally about *sameness*, and that a person's sameness runs in two directions: across time, and across the many *facets* of a life. Crucially, the sameness across facets is meant to be perceptible only to its owner — a facet is a unit of isolation, and only the owner may choose, one relationship at a time, to reveal that two facets are one person. Facets are minted by *relationships*, not by organizations as such — though organizations, being the most prolific source of our relationships, account for most of them (every entry in a password manager is one). The piece develops the less-examined half of the story: that organizational relationships carry formal *capacity* — signing as a citizen versus signing as a CEO — which is the hinge of who is liable when something goes wrong, why credentials have an *affinity* for a facet rather than belonging to the whole person (even as some legitimately span several), and how the opaque cryptographic identifiers that anchor each facet are made livable by two tools: one that names them and one that lets a human verify their sameness by eye.
keywords: "identity, facets, digital identity, relationships, organizational identity, capacity, personas, pseudonyms, self-sovereign identity, decentralized identifiers, privacy, correlation, credentials, accountability"
description: "A single person is a mother, a CEO, a patient, and a citizen at once — and the law, the market, and good sense all insist that these be kept distinct. This primer argues that identity is fundamentally about *sameness*, and that a person's sameness runs in two directions: across time, and across the many *facets* of a life. Crucially, the sameness across facets is meant to be perceptible only to its owner — a facet is a unit of isolation, and only the owner may choose, one relationship at a time, to reveal that two facets are one person. Facets are minted by *relationships*, not by organizations as such — though organizations, being the most prolific source of our relationships, account for most of them (every entry in a password manager is one). The piece develops the less-examined half of the story: that organizational relationships carry formal *capacity* — signing as a citizen versus signing as a CEO — which is the hinge of who is liable when something goes wrong, why credentials have an *affinity* for a facet rather than belonging to the whole person (even as some legitimately span several), and how the opaque cryptographic identifiers that anchor each facet are made livable by two tools: one that names them and one that lets a human verify their sameness by eye."
image: /assets/cards/if.png
---

*One person, many faces — and why keeping them straight is a feature, not a bother.*

> "Do I contradict myself? / Very well then I contradict myself, / (I am large, I contain multitudes.)" — Walt Whitman, *Song of Myself* (1855)

## An afternoon of signatures

In a single afternoon, a woman I'll call Cecilia signs three documents. In the morning she signs a permission slip so her daughter can go on a school trip. At noon she signs an invoice for €100,000 on behalf of the company she leads. In the evening she signs a lease on an apartment she is renting for herself.

One hand. One pen. Three signatures that look identical. Yet the law reads them as the acts of three different people. The permission slip binds Cecilia the parent. The invoice binds Acme, the company whose chief executive she happens to be — and Acme, not Cecilia, owes the €100,000. The lease binds Cecilia the private tenant. If you blur these together — if you let the company answer for the apartment, or the parent answer for the invoice — you have manufactured either fraud or nonsense.

We navigate this every day without thinking about it. The machinery underneath is worth thinking about, because when we move it into software, the thinking stops being automatic and the mistakes start being expensive.

## Identity is sameness

Before we can talk about facets, we need to be clear about what identity *is*. Strip away the politics and the paperwork and identity is a plain idea: **sameness**. It is what lets us take the attributes of a thing in one moment and match them to the same thing in another.

Mathematics uses the word this way. An *identity* is an equation guaranteed to hold on both sides — `a² − b² = (a − b)(a + b)` — a promise of sameness across any value you choose. Accounting uses it too: `Assets = Liabilities + Owner's Equity` is called an identity because it must balance, always. In both cases the word names a guarantee that two things are, at bottom, the same thing.

Human identity is the same idea, worn by people instead of numbers. Cecilia's children see the same mother from one bedtime to the next. Her company sees the same executive from one board meeting to the next. Sameness is the thread.

## Sameness runs two directions

Here is where it gets interesting. Cecilia's sameness runs along two axes at once.

The first is **time**. She is the same mother today as yesterday — continuity across the calendar. This is the axis most people picture when they hear the word "identity", and it is the one authentication systems are built to check.

The second is **facet**. At any single moment, Cecilia is a mother *and* a CEO *and* a patient *and* a citizen *and* a tenant. These are not phases she passes through; they are simultaneous faces of one life.

Think of a cut gemstone. It is a single stone, but it has many facets, and each facet catches the light differently depending on the angle you hold it to. Turn the gem and a new face flashes; the stone has not changed, but what you see has. A person is like that. The mother-face and the CEO-face are genuinely *hers* — no mask, no pretense — yet each shows a different aspect to a different observer. Identity is the whole stone. A facet is one of its faces.

[SUGGESTED DIAGRAM: One stone, many faces — a single cut gem whose facets are labeled with an actor's roles (mother, CEO, patient, citizen), a single beam of light entering and leaving differently at each face, to show one identity presenting many aspects.]

## Only the owner sees the whole stone

The gem makes one more question sharp: who gets to see the whole stone, and who sees only a single face?

This is the crux of the design. **Cecilia** sees the whole stone. She knows that CEO-Cecilia, patient-Cecilia, and cellist-Cecilia are one person, because she *is* that person. The people she deals with do not — and, by design, must not. Her doctor sees the patient and has no way to tell it is the same human as the executive who signed an invoice across town. Her string quartet sees the cellist and cannot perceive the CEO. Each observer holds the gem at one angle and sees one face; only the owner ever turns it in the light.

This sharpens the two axes. Sameness *across time* is meant to be visible to a counterparty — Cecilia's employer should recognize the same employee from one day to the next, because that continuity is what a relationship *is*. Sameness *across facets* is the opposite: it is meant to be visible to Cecilia, and to no one else. A facet is, before it is anything else, a unit of **isolation**.

None of this makes the boundary a prison. The owner may choose to open a door. Cecilia might tell a colleague that she plays in a string quartet on weekends — deliberately linking her work facet to her musical one, for that person, on that occasion. That is her prerogative, and a healthy identity system supports it. What matters is *who decides*. Revealing that two facets are one person is Cecilia's call to make, one relationship at a time — never a default, never an inference a stranger can draw, never a leak the system permits behind her back.

## The half we already understand

That isolation buys something everyone recognizes: **privacy**.

Cecilia's doctor should not be able to connect Cecilia-the-patient to Cecilia-the-employee, or he might let slip a diagnosis to a colleague who knows her firm. When she buys dog food online with a one-click login, she should not have to hand the pet-food vendor her full legal name, her age, and her phone number. Facets are boundaries, and boundaries keep information from leaking across contexts that have no business being joined. Left unmanaged, the leaks compound into the surveillance economy.

This case is made well elsewhere, and I won't repeat it here. That different people should see different faces of us — and that collapsing everyone's view into one universal "you" is a privacy catastrophe — is the argument of Three Dimensions of Identity [1], of Security, Silos, and Sovereignty [2], and of the dangerous half-truth that we'll "be correlated anyway" [3]. Take those as read.

[SUGGESTED DIAGRAM: Two facets that must not touch — the doctor's view of a patient beside the employer's view of an employee, a dashed boundary between them, and an arrow trying to cross it marked with a red X.]

The privacy argument is real, but it is only half the story. It explains why we might *choose* to keep facets apart. It does not explain where most facets come from in the first place — and it turns out we rarely choose them at all.

## Relationships mint facets

Most of Cecilia's facets are not carved by her for privacy. They *accrete*, one per relationship, as she lives, works, and transacts.

This is the relationship axis of identity: we are known differently by every party we deal with [1]. Her bank knows a borrower; her clinic knows a patient; a shopping site knows an account it met once at checkout. Each relationship brings a new face into being. The clearest everyday proof sits in your password manager — every entry there is a relationship with some organization, and therefore a facet of you: a separate login, a separate scope, a separate slice of your life. Most of us manage hundreds without ever calling them facets.

Organizations loom large here, but not because an organization is special. They loom large because they are the most *prolific* source of relationships we have. Join a company and you do not gain one relationship but many — to the payroll system, the badge office, the pension fund, your colleagues, your manager — each a facet. And organizational relationships carry a trait that raises the stakes: formal duties, formal authority, and, crucially, formal **accountability**. The day Cecilia was hired, Cecilia-the-employee was born, with duties she did not have the day before. When she was promoted, Cecilia-the-CEO was minted, able to bind the company in ways an ordinary employee cannot. Each role is a new face, and each face answers for its own acts.

This is why the law is so fussy about something it calls *capacity* — the specific standing in which a person acts [4]. Capacity is not bureaucratic fussiness; it is the answer to a question with money attached: *when this goes wrong, who pays?*

Return to the afternoon of signatures. When Cecilia signs a personal lease, she acts in her capacity as a private individual, and she alone is on the hook. When she signs the €100,000 invoice, she acts in her capacity as CEO, and the *company* is on the hook — she is merely its hand. On a negotiable instrument, the law spells this out: a signature made plainly in a representative capacity binds the represented company and not the signer [5]. Same handwriting, radically different consequences. Some acts are even valid in more than one capacity: Cecilia could sign a loan as a private citizen or as her company's officer, and which one she chose changes who must repay it. The signature cannot tell you. Only the capacity can.

[SUGGESTED DIAGRAM: One hand, three signatures — the same handwritten signature over three documents (a school permission slip, a company invoice, an apartment lease), each tagged with the capacity it was signed in and the party who bears the liability.]

Blur capacity and you get the corporate-law equivalent of the fraud-or-nonsense problem: a personal debt charged to a company, or a company obligation pinned on an individual. Precision here is not optional. It is the whole point.

## Credentials have an affinity for a facet

Once you see facets as the unit that carries accountability, a pattern that used to look arbitrary comes into focus: **a credential tends to have an affinity for one facet.**

Cecilia's employee badge is a credential of Cecilia-the-employee. Quit the job and the badge goes back — it was never hers as a private individual. Her authority to sign that €100,000 invoice has an affinity for Cecilia-the-CEO, and would be worthless attached to her parent-facet or her patient-facet. Much of the time the pull is this strong, and a good system respects it: hand a credential to the wrong facet and it is either useless or dangerous.

But *affinity* is the right word, not *ownership* — because the pull is a tendency, not a law. Two things keep it from being absolute.

First, some credentials genuinely cross facets. Suppose a notary attests that I signed a document in their presence on a certain day. Which facet does that attestation belong to? It records an *act*, not a role; it travels with whatever capacity I signed in, and might be equally at home in several. To pin it to one facet by fiat would discard information the credential never committed to.

Second, it is a mistake to think a credential is *owned* by whoever issued it, or bound to the single context the issuer had in mind. Utah's State-Endorsed Digital Identity (SEDI) makes the point vividly: the identity is *created and controlled by the individual*, and the state merely *endorses* certain verified attributes — name, birth date, residence — which the holder then carries into many unrelated contexts, from forming a company to seeing a doctor [6]. Withdraw the endorsement and the identity persists, because the citizen, not the state, holds the key. Such a credential has affinities, but it is neither the property of its issuer nor the captive of one facet.

So a good identity system does not model a person as a single bucket of credentials — nor does it pretend every credential slots neatly into exactly one facet. It models a person as a set of facets, keeps each credential with the facet it has affinity for, and stays honest about the credentials that legitimately span more than one.

## A note on names

The concept I'm calling a *facet* travels under several names, and it's worth being explicit about the choice, because the words are not interchangeable.

Some in the decentralized-identity world call it a **persona**. Anonyome Labs builds its MySudo product around exactly this idea — situational, activity-based partitions, one for work, one for selling, one for social life, each holding its own keys and credentials [7]. Even the W3C's Decentralized Identifiers specification speaks, in passing, of "separation of identities, personas, and interactions" [8]. So "persona" is defensible, and it has real intuitive pull — we already talk about the persona we wear at work versus the one at home.

I avoid it for two reasons. First, in the neighbouring world of agentic AI, "persona" already means something else: an agent's *behavioral character* — its tone, its priorities, the way it talks — not a partition of its identity [9]. A term meant to span people, organizations, *and* software agents cannot afford to mean "identity partition" in one room and "personality" in the next. Second, "persona" in ordinary usage leans toward a public mask, a face put on for an audience — and facets are not masks. Cecilia-the-CEO is not a performance; she is really the CEO.

A related term worth knowing is **pseudonym**. The European Union's digital-identity framework uses it for a facet-like partition that is deliberately unlinkable — a separate handle for each party you deal with, so that even colluding services cannot stitch your dealings back together [10]. A pseudonym is finer-grained than a facet — you might present the same CEO facet to many counterparties — but the family resemblance is clear.

I use **facet** because it is neutral. A gem has facets whether it is worn by a person, held by a company, or wielded by a machine. The word carries no whiff of performance and no collision with a second meaning. It says exactly what it means: one face of a single, unchanged whole.

## Living with the anchors

There is a practical catch. In a digital system, each facet has to be anchored to something a computer can check — and that something is an **opaque, high-entropy identifier**: a decentralized identifier, an autonomic identifier, a public key. A string like `did:example:EMyYnLzlJDJskqojipIMivAKHWeZofhWiYjB79uszynS` is exactly what a machine needs and exactly what a human cannot love. Give a person one facet per relationship and you have handed them a fistful of these, each unreadable, unmemorable, and easy to confuse.

Two tools make the anchors livable, and they answer the two questions a human ever asks about an identifier.

The first question is *"which one is this?"* — the problem of selecting, remembering, and searching. The answer is a friendly, local **alias**: a label the owner attaches to the opaque string, so that `me-as-ceo-at-acme` stands in for the 44-character key. Aliases are the subject of a companion piece, Opaque Identifier Aliases [11], and of a naming convention, COIA [12], that generates them consistently.

The second question is *"is this the same one?"* — the problem of verifying, comparing, and defeating the impostor who swaps in a look-alike key. Here the answer is to change the *modality* of the task: render the identifier as a picture a person can compare at a glance, so a substituted key jumps out instead of hiding in a serial character-by-character scan. That is the job of entviz [13], whose perceptual limits have been estimated [14].

Notice how neatly the two tools divide the labour, and how each maps onto one of the ideas in this primer. Naming serves *facets*: it tells you which face you are dealing with. Visual comparison serves *sameness*: it lets a human confirm that this identifier is, at bottom, the same one as before — the very definition we started with. One tool for the many faces; one tool for the sameness beneath them.

## Precision is a feature

It is tempting to treat all of this — the facets, the capacities, the per-facet credentials — as complexity to be hidden, and to long for a single, simple "you" that everyone shares. That longing is the mistake. The single universal "you" is not simpler; it is a privacy hazard, a legal ambiguity, and an accountability hole, all at once. The complexity is not an accident of the design. It is the shape of a real life.

The right response is not to flatten identity but to model it honestly — one whole, many faces, each face accountable for its own acts — and then to build software that carries the precision *for* us, so that we feel only the ease and never the bookkeeping. How software does that is the work of the companion pieces. The claim of this one is narrower, and it is the foundation the rest stands on: a person is legitimately many, the many are minted by the relationships we accumulate — most of them with organizations — and keeping them straight is not a burden the system imposes but the first thing it owes us.

## References
[1] Hardman, D. and Law, J. 2019. Three Dimensions of Identity. Codecraft Papers. Retrieved from https://dhh1128.github.io/papers/3dim.html

[2] Hardman, D. 2021. Security, Silos, and Sovereignty. Codecraft Papers. Retrieved from https://dhh1128.github.io/papers/sss.html

[3] Hardman, D. 2020. The Dangerous Half-Truth of "We'll Be Correlated Anyway". Codecraft Papers. Retrieved from https://dhh1128.github.io/papers/wbca.html

[4] Legal Information Institute. n.d. Capacity. Wex, Cornell Law School. Retrieved July 9, 2026 from https://www.law.cornell.edu/wex/capacity

[5] Uniform Commercial Code. 2002. § 3-402. Signature by Representative. Legal Information Institute, Cornell Law School. Retrieved July 9, 2026 from https://www.law.cornell.edu/ucc/3/3-402

[6] State of Utah, Department of Government Operations. 2026. State-Endorsed Digital Identity (SEDI). Utah Code Title 63A, Chapter 20 (effective May 6, 2026). Retrieved July 9, 2026 from https://sedi.utah.gov

[7] Anonyome Labs, Inc. 2022. U.S. Patent No. 11,507,943 B1. U.S. Patent and Trademark Office (granted November 22, 2022). Retrieved from https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11507943

[8] World Wide Web Consortium (W3C). 2022. Decentralized Identifiers (DIDs) v1.0. W3C Recommendation (July 19, 2022). Retrieved from https://www.w3.org/TR/did-1.0/

[9] Amin, D., Salminen, J., and Jansen, B. J. 2026. How to Model AI Agents as Personas?: Applying the Persona Ecosystem Playground to 41,300 Posts on Moltbook for Behavioral Insights. arXiv:2603.03140. Retrieved from https://arxiv.org/abs/2603.03140

[10] European Commission. 2024. EU Digital Identity Wallet Architecture and Reference Framework — Topic E (Pseudonyms and User Authentication). Retrieved from https://github.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/discussions/375

[11] Hardman, D. 2026. Opaque Identifier Aliases. Codecraft Papers. Retrieved from https://dhh1128.github.io/papers/oia.html

[12] Hardman, D. 2025. Conventions for Opaque Identifier Aliases (COIA). Retrieved from https://dhh1128.github.io/coia

[13] Hardman, D. 2026. Amplifying Difference: Perceptual Design and Verification of Human-Centric Entropy Visualizations. SSRN Electronic Journal. DOI: https://doi.org/10.2139/ssrn.6979798

[14] Hardman, D. 2026. Measuring the Glance: An Adversarial Estimate of Habituated Perceptual Entropy in entviz and SSH Randomart. SSRN Electronic Journal. DOI: https://doi.org/10.2139/ssrn.6979878
