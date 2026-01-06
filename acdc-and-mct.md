## 1. Introduction and scope

Two different communities have been circling a similar problem from opposite directions.

On one side are identity and credential systems that have grown uneasy with the way trust is handled on the modern internet. Static identifiers, brittle revocation mechanisms, and routine over-disclosure all make it harder to build systems that respect autonomy and privacy without sacrificing verifiability. KERI and ACDCs emerged from this unease, with an emphasis on explicit key state, durable provenance, and the ability to reveal only what a given interaction requires [1, 2].

On the other side is the WebPKI, an infrastructure that has scaled astonishingly well but is showing signs of strain. Certificate transparency was bolted on to address mis-issuance after the fact [3]. Revocation remains unreliable in practice. And the prospect of post-quantum cryptography threatens to turn already heavy handshakes and logs into something much worse [4]. Merkle Tree Certificates are one attempt to relieve that pressure without tearing out the foundations of the web [5].

At first glance, these efforts seem only loosely related. One lives in the world of self-sovereign identity and verifiable credentials. The other is firmly rooted in browsers, certificate authorities, and TLS. Yet they keep reaching for the same tool: hash-based commitments arranged in Merkle-like structures. That coincidence invites comparison, but it also invites confusion.

This paper is an attempt to clarify what that resemblance does and does not mean. It is not a bake-off. It does not argue that one system should replace the other, nor that they solve the same problem equally well. Instead, it treats each as a response to a different set of constraints, using some shared primitives in very different ways.

The comparison is organized by function rather than lineage. Instead of asking which protocol came first, or which standards body is involved, we ask a simpler set of questions. What is being committed to, and why. What is being proven to a verifier, and what is left implicit. How freshness and revocation are handled in practice. Where the operational costs land. And how post-quantum pressures shape design choices.

The intended reader is technically literate, but not necessarily fluent in both worlds. If you are comfortable with certificate transparency and Merkle inclusion proofs, this paper aims to make ACDC graduated disclosure feel intelligible rather than exotic. If you are steeped in KERI and self-addressing identifiers, it aims to make Merkle Tree Certificates feel less like a curiosity and more like a coherent response to WebPKI realities.

The goal is modest but practical. By the end, a reader who knows one model well should be able to reason about the other without constantly reaching for analogies that do not quite fit.

## 2. A comparative map

Before going further, it helps to see the whole landscape at once.

The table below is not a summary of conclusions. It is a map. Each row corresponds to a question that any trust system must answer in practice. Each column shows how KERI/ACDCs and Merkle Tree Certificates answer that question, given their respective goals and constraints [1, 2, 5].

The sections that follow expand on these rows one by one. Readers who already know one side well may find it useful to treat the table as an index, returning to it as a reference point while reading the prose.

| Axis | KERI / ACDCs | Merkle Tree Certificates (MTC) |
|---|---|---|
| Primary problem being optimized | Durable attribution, continuity of control, and privacy-preserving exchange of structured claims | Scalable, auditable certificate issuance under bandwidth, latency, and post-quantum pressure |
| Core commitment object | SAID: a self-addressing identifier that commits to the content and structure of a claim | Merkle roots and landmarks that commit to an append-only log of issuance events |
| What is being committed to | Meaning: the identity of a structured claim, independent of presentation | Membership: inclusion of an object in a publicly auditable history |
| What is proven to the verifier | That the disclosed view corresponds to a specific underlying claim and verifies equivalently | That a certificate was issued and logged as part of a committed set |
| Partial visibility mechanism | Graduated disclosure: substructures may be replaced by their SAIDs without changing verification semantics | Inclusion proofs: Merkle paths prove membership without revealing the rest of the log |
| Primary motivation for partiality | Privacy and correlation minimization | Efficiency and scalability |
| Freshness assumptions | Emphasis on continuity and completeness of key state; verification can be offline | Emphasis on recency; efficiency depends on clients being up to date on landmarks |
| Revocation model | Expressed as events in key state or registries, reconciled over time | Rooted in X.509 semantics; transparency improves detection rather than enforcement |
| Operational cost center | Managing and reasoning about event history and state reconciliation | Distributing and caching landmarks at scale |
| Post-quantum pressure addressed | Algorithm agility and continuity across key transitions | Signature and certificate size on the wire and in logs |
| Standardization trajectory | ToIP KSWG specifications, ISO 17442-3, GSMA deployments, ecosystem layering [6, 7, 8] | IETF Internet-Draft, CT lineage, browser and CA experimentation [3, 5, 9] |
| Typical deployment surface | Identity systems, credentials, registries, telecom signaling | WebPKI, TLS handshakes, browser trust infrastructure |

The resemblance between the two systems is real, but it lives primarily at the level of shared primitives. The differences emerge as soon as one asks what those primitives are meant to accomplish.

## 3. Shared primitives, different design goals

It is not an accident that both KERI/ACDCs and Merkle Tree Certificates are described, informally, as “Merkle-like”. Both lean heavily on hash commitments. Both use those commitments to make partial information verifiable. And both emerged in response to real stress in existing systems rather than as academic exercises [1, 3, 5].

Those similarities are worth acknowledging, because they explain why engineers from one world often feel an immediate sense of familiarity when encountering the other. But they can also mislead. The shared primitive sits at different layers in each system, and it is pressed into service for different ends.

### 3.1 Hash commitments as a common foundation

At the lowest level, both designs rely on standard cryptographic assumptions about hash functions: collision resistance, second-preimage resistance, and practical irreversibility [10]. In both cases, a hash acts as a durable stand-in for some larger body of data. If you trust the hash, you can defer seeing the data itself.

In ACDCs, the hash is elevated into the data model. A self-addressing identifier is not merely a checksum; it is a first-class field that other structures point to. The identifier becomes the name of the thing. Once that happens, the question “what does this object commit to?” is answered structurally, not procedurally [2].

In Merkle Tree Certificates, the hash sits at the boundary between objects. Certificates remain conventional X.509 artifacts [11]. The hash-based structure wraps around them, organizing issuance events into an append-only tree. Here, the hash commits not to meaning but to position: this certificate appeared at this point in a public history [5].

The same mathematical tool is doing different kinds of work.

### 3.2 Trees, structure, and meaning

This difference shows up clearly in how tree structure is used.

In MTCs, the tree is literal. Leaves correspond to issued certificates. Internal nodes summarize subsets of issuance events. The root, or landmark, stands for a snapshot of the log at a particular moment. Traversing the tree is about proving membership and consistency [3, 5].

In ACDCs, the “tree” is implicit in the schema. Nested maps and lists form a semantic structure: attributes, assertions, relationships. Hashing that structure produces a graph of commitments, but the shape of the graph reflects meaning rather than chronology [2].

This distinction matters. A Merkle inclusion proof says “this object is part of that set”. A SAID says “this object is exactly this thing”. One is about placement in a history; the other is about identity of content.

### 3.3 Different answers to different pressures

The design goals follow naturally from these choices.

KERI and ACDCs grew out of a concern with attribution, continuity of control, and privacy. The pressure they respond to is over-sharing: revealing more than is necessary to establish trust, and creating linkages that persist longer than intended [1, 2]. Hash commitments make it possible to hold claims together while exposing only what a given interaction requires.

Merkle Tree Certificates grew out of a concern with scale and auditability in the WebPKI. The pressure there is accumulation: ever-larger certificates, ever-more signatures, and ever-growing logs, especially in a post-quantum context [4, 5]. Hash commitments make it possible to compress evidence of correct issuance without weakening public audit.

Both systems reach for hashes because hashes are cheap, stable, and well understood. But they deploy them to relieve different kinds of strain. Treating one as a drop-in mental model for the other obscures that fact. The resemblance is real, but it lives below the level where the most important design decisions were made.

## 4. What is proven, to whom: disclosure equivalence and inclusion membership

At a glance, ACDC graduated disclosure and Merkle Tree Certificate inclusion proofs can look like variations on the same idea. Both rely on hashes. Both allow a verifier to check something without seeing everything. Both are often described, loosely, as Merkle-based. That resemblance is real, but it is also superficial. The two mechanisms answer different questions, for different audiences, under different assumptions.

### 4.1 Graduated disclosure in ACDCs

An ACDC is a structured container whose contents are bound together by self-addressing identifiers. Each block of data is hashed, and that hash becomes part of the structure itself. Because parent blocks incorporate the hashes of their children, a verifier can check the integrity of the whole even if some of the parts are missing [2].

Graduated disclosure takes advantage of this structure. A presenter can replace selected substructures with their SAIDs, revealing only what a particular verifier needs to see. The crucial property is equivalence. A fully expanded ACDC and a partially disclosed one verify the same way, lead to the same status checks, and anchor to the same underlying claim [2, 12]. From the verifier’s point of view, nothing essential has changed; only the level of detail has.

This is not a performance optimization. It is a privacy mechanism. The design assumes that different verifiers have different legitimate needs, and that over-disclosure creates correlation risk. The goal is not to hide the existence of a claim, but to control its shape as seen by different parties [12].

The proof obligation, then, is semantic. The presenter is proving that “this view corresponds to that claim”, even though the verifier sees only a fragment. The hash commitments are there to preserve meaning across views, not to summarize volume.

### 4.2 Inclusion proofs in Merkle Tree Certificates

Merkle Tree Certificates start from a different problem. In the WebPKI, certificates are public artifacts. Privacy through selective disclosure is not the primary concern. The dominant questions are whether a certificate was properly issued, whether it appears in an append-only log, and whether relying parties can detect mis-issuance [3, 5].

An inclusion proof answers one narrow question: is this object a member of a committed set. In MTCs, the committed set is a subtree of a certificate issuance log, summarized by a landmark hash. A relying party that has the relevant landmark can verify, via a Merkle path, that a particular TBSCertificate is included in that subtree [3, 5].

Here, too, the verifier does not need to see everything. But what is omitted is not sensitive structure; it is the rest of the log. The omission serves efficiency and scalability, not privacy. The proof says nothing about alternative presentations of the certificate, because there are none. A certificate is what it is, and its contents are assumed to be visible to anyone who encounters it.

The proof obligation is historical rather than semantic. The relying party is being assured that “this certificate exists in a publicly auditable history that has not been rewritten”. Freshness matters, because the value of that assurance depends on how current the relying party’s view of the log is [5].

### 4.3 Two answers to two different questions

The contrast can be stated simply.

Graduated disclosure answers the question: how much of this claim do you need to see in order to trust it. Inclusion proofs answer the question: can you trust that this claim was issued and logged as asserted.

Both rely on hash commitments to make partial views verifiable. But they operate at different layers. ACDCs operate at the level of meaning and intent. MTCs operate at the level of issuance and auditability.

This difference has practical consequences. Techniques that strengthen one mechanism do not automatically strengthen the other. A more compact inclusion proof does nothing to reduce correlation risk. A more expressive disclosure schema does nothing to reduce the cost of logging post-quantum certificates. Understanding where the similarity ends is as important as recognizing that it exists at all.

## 5. Freshness, revocation, and operational burden

Questions of freshness and revocation are where abstract design choices turn into operational reality. They are also where the differences between KERI/ACDCs and Merkle Tree Certificates become most concrete. Both systems care about change over time, but they model it differently, and they place the resulting costs on different actors.

### 5.1 Key state and continuity in KERI

In KERI, change is not an exceptional event layered on top of an otherwise static object. It is the core of the model. An identifier is defined by the sequence of key events that control it over time. Rotation, revocation, delegation, and recovery are all expressed as explicit events in a key event log [1].

Freshness, in this context, is about continuity rather than immediacy. A verifier asks whether the key state it sees forms a valid, uninterrupted chain from inception to the present. Witness receipts and other forms of endorsement help establish that chain, but they do not require a global notion of “now” [1]. Verification can be done offline, provided the verifier has access to the relevant events and receipts.

Revocation follows the same pattern. An ACDC is not revoked by consulting a central service or checking a flag that may or may not be current. Instead, revocation is expressed as an event that changes the status of the credential within a registry or key state framework [2]. The burden shifts from real-time querying to event reconciliation.

### 5.2 Freshness assumptions in Merkle Tree Certificates

Merkle Tree Certificates invert many of these assumptions.

Here, freshness is front and center. The efficiency gains of MTCs depend on relying parties having a reasonably current view of the log’s landmarks. If a client is up to date, it can validate a certificate with a small inclusion proof and minimal signature material. If it is not, it must fall back to heavier proofs that resemble today’s certificates [5, 9].

Revocation remains anchored in WebPKI semantics. Certificates are still issued, expire, and are revoked according to X.509 conventions [11]. The Merkle structure does not replace that machinery; it optimizes how evidence of correct issuance and logging is conveyed [3, 5].

### 5.3 Who pays, and when

The contrast can be summarized in terms of who absorbs complexity.

KERI pushes complexity toward structure and history. It asks participants to reason about sequences of events and their completeness. In return, it relaxes assumptions about connectivity and central availability.

MTCs push complexity toward distribution and synchronization. They assume that most clients can be kept reasonably current, and they reward that assumption with dramatic reductions in on-the-wire cost.

Neither approach is universally superior. Each reflects the constraints of its home ecosystem. Identity systems that emphasize autonomy and selective disclosure accept the cost of richer state reasoning. Web infrastructure that serves billions of clients accepts the cost of aggressive caching and update mechanisms.

## 6. Post-quantum readiness: different pressures, different responses

Post-quantum cryptography has a way of flattening conversations. Systems are often described as either “PQ-ready” or not, as if readiness were a single property that could be checked off. In practice, the pressures introduced by post-quantum algorithms are uneven, and the responses to them are shaped by where those pressures are felt most acutely.

KERI/ACDCs and Merkle Tree Certificates both rely heavily on hash functions, and both assume that well-chosen hashes will remain viable in a post-quantum world [10, 13]. Beyond that shared assumption, their approaches diverge.

### 6.1 What changes in a post-quantum setting

The most immediate operational impact of post-quantum algorithms is not conceptual but physical. Keys get larger. Signatures get larger. Handshakes carry more bytes. Logs fill up faster [4, 13].

Hash functions, by contrast, degrade more gracefully. A sufficiently large hash output can absorb a quadratic speedup without forcing a redesign of protocols or data models [10]. That asymmetry explains why so many PQ transition strategies lean on hashes as anchors of continuity.

### 6.2 Merkle Tree Certificates and size pressure

Merkle Tree Certificates are a direct response to size pressure in the WebPKI. TLS handshakes already carry certificate chains, signatures, and status information [14]. Adding post-quantum signatures to that mix risks pushing latency and bandwidth costs past acceptable limits, especially at global scale [4, 5].

MTCs address this by reducing what must be transmitted in the common case. If a relying party has a recent landmark, it does not need to see a full certificate and its associated signatures. A single inclusion proof, combined with a small amount of signature material on the landmark itself, can suffice [5, 9].

### 6.3 KERI, ACDCs, and cryptographic agility

KERI’s post-quantum posture is framed differently. Rather than optimizing for wire size, it emphasizes cryptographic agility and precommitment. Key pre-rotation allows an identifier to commit, in advance, to future key material [1]. When an algorithm transition becomes necessary, control can move to new keys without breaking the continuity of the identifier.

ACDCs inherit this posture. Because claims are bound to identifiers and key state rather than to a fixed signature scheme, they can survive algorithm changes without changing their semantics [2]. Hash commitments provide continuity across those changes.

### 6.4 Avoiding false equivalence

Both systems lean on hashes, and both will depend on standardized post-quantum algorithms as they mature [13]. But they are responding to different failure modes.

Merkle Tree Certificates respond to the risk that post-quantum primitives make existing infrastructure too expensive to operate at scale. KERI and ACDCs respond to the risk that algorithm transitions fracture identity continuity and trust relationships.

## 7. Standardization and adoption trajectories

It is tempting, when comparing two technical systems, to line them up on a single timeline and ask which one is “ahead”. That instinct is misleading here. KERI/ACDCs and Merkle Tree Certificates are moving through different institutional channels, serving different operational constituencies, and solving different kinds of coordination problems.

### 7.1 ACDCs and KERI: multiple paths into production

On the KERI side, adoption has not followed a single standards track. Instead, ACDCs have begun to appear as a reusable substrate inside several distinct efforts.

One of the most consequential is formal international standardization. ISO 17442-3 specifies the use of ACDCs for verifiable legal entity identifiers [6].

A second adoption vector is the global telecommunications ecosystem. The GSMA Open Verifiable Calling project uses ACDCs to address fraud and impersonation in voice networks [7].

A third vector is ecosystem layering. Within Trust Over IP, the Dossier Task Force defines a higher-level construct that composes multiple ACDCs into a coherent bundle [8].

### 7.2 Merkle Tree Certificates: evolution inside the WebPKI

Merkle Tree Certificates follow a different path. They are specified as an IETF Internet-Draft and are being explored through controlled experiments by browser and infrastructure operators [5, 9].

Crucially, MTCs are designed to coexist with today’s WebPKI. Fallback paths and compatibility with existing trust anchors are core design requirements, not optional features [5].

### 7.3 Different trajectories, not competing ones

Seen side by side, these trajectories are orthogonal. ACDCs are moving through identity, legal, and telecom channels. MTCs are moving through the infrastructure layer of the web.

The contrast shows that standardization and adoption are ecosystem-specific. Success in one domain looks different from success in another.

## 8. Conclusion

It is easy to notice that both KERI/ACDCs and Merkle Tree Certificates rely on hashes arranged in Merkle-like structures. It is harder, and more important, to notice where that similarity stops doing explanatory work.

These systems are not competing answers to the same question. They are answers to different questions that arise in different ecosystems.

For readers who know one model well, the temptation is to translate the other too literally. Graduated disclosure is not a privacy-flavored inclusion proof. Inclusion proofs are not a coarse form of selective disclosure.

The value of comparing these systems lies in sharpening assumptions. If this paper succeeds, it leaves the reader better equipped to understand why both exist, and why their differences matter.

## Works Cited

[1] Smith, S. (2019). *Key Event Receipt Infrastructure (KERI)*. arXiv:1907.02195. https://doi.org/10.48550/arXiv.1907.02195

[2] Trust Over IP KSWG. (2023). *Authentic Chained Data Containers (ACDC) Specification*. Trust Over IP Foundation.

[3] Laurie, B., Langley, A., and Kasper, E. (2013). *Certificate Transparency*. RFC 6962. https://doi.org/10.17487/RFC6962

[4] Bernstein, D. J., et al. (2022). *Post-quantum cryptography*. Communications of the ACM, 65(2). https://doi.org/10.1145/3478437

[5] Ben, D., et al. (2025). *Merkle Tree Certificates*. IETF Internet-Draft, work in progress.

[6] International Organization for Standardization. (2024). *ISO 17442-3:2024 Financial services — Legal entity identifier (LEI) — Part 3: Verifiable LEIs (vLEIs)*. ISO.

[7] GSMA. (2024). *GSMA Foundry launches Open Verifiable Calling project*. GSMA.

[8] Trust Over IP KSWG. (2024). *Dossier Specification*. Draft.

[9] Cloudflare, Inc. (2025). *Bootstrapping Merkle Tree Certificates*. Cloudflare Blog.

[10] Menezes, A., van Oorschot, P., and Vanstone, S. (1996). *Handbook of Applied Cryptography*. CRC Press.

[11] Cooper, D., et al. (2008). *Internet X.509 Public Key Infrastructure Certificate and CRL Profile*. RFC 5280. https://doi.org/10.17487/RFC5280

[12] Hardman, D. (2023). *Verifiable Voice Protocol*. IETF Internet-Draft draft-hardman-verifiable-voice-protocol-02.

[13] National Institute of Standards and Technology. (2024). *FIPS 204: Module-Lattice-Based Digital Signature Standard*. NIST.

[14] Rescorla, E. (2018). *The Transport Layer Security (TLS) Protocol Version 1.3*. RFC 8446. https://doi.org/10.17487/RFC8446
