# ACDCs Should Underpin Digital Trust; Keep W3C VCs as Derivative Artifacts

<span class="hash">#acdc #keri #verifiable-credentials #w3c</span>

<p align="right"><em>(related: comparisons of <a href="x509-prob.html">ACDCs and X509</a> and <a href="sdjwt-acdc.html">SD-JWTs</a>)</em></p>

## Lossless vs. Lossy: A Choice That Matters

Ask a professional photographer which format they use for archival storage, and the answer is always RAW, never JPEG. Ask a music producer whether they master in FLAC or MP3, and you'll get the same pattern: lossless for the source of truth, lossy for distribution. The reason is simple. You can generate a JPEG from a RAW file whenever you need one, optimized for its context — web display, print, or thumbnail. But you cannot go the other direction. Once you've discarded information, it's gone.

![lossless and lossy](assets/lossless-lossy.jpg)

This same principle applies to digital identity and verifiable evidence, though the industry has been slow to recognize it. One of the buzz-getting credential formats today — the W3C Verifiable Credentials Data Model — is lossy. It discards information about trust chains, time, key history, relationship weights, and use cases outside the credential model. (SD-JWTs and ISO mDL are also lossy, BTW. But that's a subject for another paper.) Authentic Chained Data Containers ([ACDCs](https://trustoverip.github.io/kswg-acdc-specification/)), by contrast, are lossless. They preserve the full fidelity of trust relationships and can be transformed into simpler formats when needed.

Understanding this distinction matters because once you've chosen a lossy format as your primary evidence, you cannot reconstruct what you've lost. And in high-stakes systems — legal entity identity, supply chain provenance, investigative journalism, voice call authentication — what you lose matters a great deal.

## What Makes a Credential Format Lossy?

### Loss 1: The Trust Chain

W3C VCs derive their validity from a reference to their proximate issuer only. If a university issues you a diploma, the VC captures that single relationship: University &rarr; You. Any broader context — whether the university is accredited, whether its accreditor is recognized by a national authority, whether that authority participates in international agreements — becomes implicit. The VC itself contains no cryptographic link back through this chain. Verifiers must consult external trust registries or simply accept the university's signature as sufficient.

This works fine when trust relationships are simple and widely known. But in complex ecosystems — multi-tier supply chains, delegated organizational authority, cross-border financial transactions — trust is not a binary fact. It is a graph with weighted edges, conditional logic, and paths that must be auditable back to a root. The rise of trust registries is proof that this conceptual gap needs plugging, and the cost and effort to create, maintain, promote, approve, and legally protect such registries is huge. It is like trying to create a governance add-on for image files to compensate for JPEG lossiness.

ACDCs preserve this graph natively, and essentially for free. An ACDC issued by a corporate subsidiary can link cryptographically to the parent company's ACDC, which links to its legal registration, which links to a global root of trust like [GLEIF](https://www.gleif.org/en/vlei/introducing-the-vlei-ecosystem-governance-framework). Each link is a Self-Addressing Identifier (SAID) — a cryptographic hash of the target credential embedded directly in the source. A verifier can traverse the entire chain without consulting a registry, and the integrity of every link is mathematically enforced.

Imagine an investigative journalist documenting sources for a story. She interviews five people, reviews three leaked documents, and consults two expert analyses. Some sources are highly credible; others are secondhand or contested. In an ACDC-based system, she can create a chain of attestations, weighting the edges by source reliability (0.9 for the leaked internal memo, 0.6 for the anonymous tip, 0.95 for the independent audit). When she publishes, readers can trace the evidence graph and understand the basis of her confidence in each claim. In a W3C VC system, these relationships would be flattened or left to prose description. The structure of trust is lost.

### Loss 2: Time

W3C VCs are generally verifiable only in the present. Was this credential valid when the mortgage was signed three years ago? The VC format provides no reliable answer. The signature remains valid, but [key state may have changed](was). The issuer might have rotated keys, revoked the credential, or gone offline. Verifiers can check current revocation lists or OCSP responders, but reconstructing the state of the world at a specific moment in the past is difficult or impossible.

ACDCs, through the Key Event Receipt Infrastructure ([KERI](https://trustoverip.github.io/kswg-keri-specification/)), maintain a complete, cryptographically verifiable history of key states. Every key rotation, every delegation, every revocation is recorded in the Key Event Log (KEL). A verifier can query the KEL and determine with cryptographic certainty whether a credential was valid on a specific date in 2021, even if keys have rotated multiple times since. This is not a nice-to-have feature. It is essential for legal evidence, audit trails, and any system where "what was true then" matters as much as "what is true now."

### Loss 3: Edge Weights and Conditional Logic

The W3C VC data model uses the Resource Description Framework (RDF), which represents relationships as triples: subject → predicate → object. "Alice delegates to Bob" is three discrete elements. But real trust is rarely that simple. Alice might authorize Bob to approve purchases up to $500, require two signatures for anything above $10,000, and grant him authority only until the end of the fiscal quarter.

RDF cannot attach properties to edges directly. To express weighted or conditional delegation, it must use *reification* — exploding the relationship into multiple intermediate nodes. The simple statement "Alice trusts Bob at 90%" becomes:

1. Alice → makesDelegation → DelegationNode_X  
2. DelegationNode_X → toAgent → Bob  
3. DelegationNode_X → weight → 0.9

This "triple bloat" forces verifiers to traverse multiple hops to reconstruct a single logical relationship. In a supply chain with thousands of components and trust scores, the overhead compounds rapidly.

ACDCs use a property graph model, where edges are first-class objects that hold attributes. An ACDC can express "Alice → Bob, weight=0.9, limit=$500, expires=2025-12-31" in a single edge structure. The weight (`w`), operator (`o`), schema (`s`), and target node (`n`) are native fields. The graph is not just a data structure — it is the trust topology itself, preserved in full fidelity.

### Loss 4: Use Cases Beyond Credentials

W3C VCs assume a three-party model: an issuer issues a credential to a holder (the subject), and the holder presents it to a verifier. This works for driver's licenses, diplomas, and membership cards. But not all verifiable evidence fits this pattern.

Consider a courtroom, where a witness gives testimony under oath. The court reporter records it, timestamps it, and signs it cryptographically. This is not a credential issued *to* the witness. It is an affidavit — a statement of fact for the public record. There is no "holder" who will present it elsewhere.

Or consider a crime scene investigator documenting evidence. The photos, measurements, and chain-of-custody logs are not credentials. They attest to what was observed at a specific time and place, available to any party with proper authority.

Or consider that investigative journalist again, documenting interviews and leaked documents as part of a chain of evidence for publication. She is not the "holder" of credentials about herself. She is creating a web of attestations that others will verify.

ACDCs handle these cases naturally. They can represent attestations without requiring an issuer &rarr; holder relationship. A sensor on a shipping container issues ACDCs documenting temperature readings. A drone attests to its GPS coordinates when capturing an image. An auditor records findings without designating a "holder."

W3C VCs are structurally biased toward the credential model. Workarounds exist, but the format and tooling expect a holder who will selectively disclose. For pure attestation, VCs are the wrong shape.

## Loss 5: Key Management Transparency
In W3C VC ecosystems, if an issuer's key is compromised and rotated, previously issued credentials typically become invalid or semantically ambiguous. Verifiers must check current key state and revocation lists, but cannot determine with certainty whether the key was compromised before or after the credential was issued. The issuer's key history is opaque.
This opacity has consequences beyond immediate security.

Cryptographers recognize that every signing key has a cryptoperiod — a statistical lifespan during which compromise is unlikely. NIST recommends 1–2 years for authentication keys. Beyond that window, the actuarial risk of compromise rises. A credential signed three years ago is actuarially suspect, even if the signature validates, because the key might have been compromised at any point during those three years. W3C VCs anchor to bare signatures without proving when issuance occurred relative to key state changes. Verifiers have no way to distinguish a credential issued safely during the key's cryptoperiod from one issued after silent compromise.

An outside observer also cannot assess the robustness of the issuer's key management practices. How often do they rotate keys? What triggered the last rotation — a scheduled policy or a suspected breach? What safeguards govern the rotation process? In high-assurance contexts, these questions matter. A legal entity signing million-dollar contracts or a pharmaceutical company certifying drug provenance should demonstrate rigorous key hygiene. But in standard VC ecosystems, there is no transparent record. Verifiers must trust the issuer's current assertions without evidence of responsible stewardship over time.

ACDCs are backed by KERI, which maintains a complete, cryptographically verifiable Key Event Log (KEL). Every key rotation, every delegation, every change in signing authority is recorded with cryptographic proofs of continuity. Crucially, KERI anchors credential issuances to specific key states in the KEL, proving that a credential was issued during the cryptoperiod of a valid key. This extends verifiability beyond the statistical cryptoperiod because the historical record is tamper-evident.
More importantly, KERI uses independent witnesses to detect actual compromise when it happens, not just estimate statistical likelihood. If a key is misused, witnesses detect the anomaly and trigger rotation recovery. This transforms cryptoperiods from fixed statistical estimates into adaptive responses to real risk. Think of it as the difference between smoking statistics (average cancer risk) and regular screenings (detect early, treat immediately). An organization with a riskier threat profile discovers problems early and adapts, rather than waiting for a breach to metastasize.

The KEL also allows verifiers to appraise an issuer's actual track record. An auditor can review rotation frequency, recovery incidents, and changes in key management strength over time. Trust becomes evidence-based, not merely asserted. A pharmaceutical company can demonstrate five years of quarterly rotations with no compromises. A startup can show it upgraded from single-signature to multi-signature control as it matured. Verifiers adjust their trust accordingly.

KERI also implements [pre-rotation](https://trustoverip.github.io/kswg-keri-specification/#pre-rotation). When an issuer rotates keys, they commit to the next key in advance (as a cryptographic hash). Even if an attacker compromises the current key, they cannot rotate to a new key they control, because they do not possess the pre-committed next key. The legitimate issuer retains a cryptographic failsafe to reclaim control.

This is not theoretical. As quantum computing advances, "harvest now, decrypt later" attacks are already underway — adversaries save encrypted sessions today, knowing they can crack them later. NIST and ENISA have issued urgent guidance about post-quantum transitions. [ACDCs are post-quantum ready by design](kspqs.pdf). Pre-rotation allows identifiers to commit to quantum-resistant keys before they are needed, protecting long-lived credentials from future compromise.

W3C VCs have no normative support for pre-rotation, witness-based compromise detection, or transparent key event logs. Some DID methods support key rotation, but protections vary widely and are not enforced. In a post-quantum world, this is a lossy model — you cannot recover security guarantees or accountability once they are gone.

### Loss 6: Schema Stability

W3C VCs depend on `@context` properties to define terms — typically URLs pointing to JSON-LD files on the web. If the server hosting the context goes offline, verification fails. If the file changes — say, "bankAccount" is redefined to mean "savingsAccount" — the semantic meaning of signed data changes retroactively without breaking the cryptographic signature. This is "link rot," a [documented vulnerability](https://www.researchgate.net/publication/364530933_A_Prospective_Analysis_of_Security_Vulnerabilities_within_Link_Traversal-Based_Query_Processing_Extended_Version).

ACDCs embed the schema (or its SAID) directly in the credential. The schema is referenced by its cryptographic content, not its location. If the schema is available anywhere — local cache, IPFS, a mirror — it can be verified against the SAID. The meaning is as immutable as the signature. There is no link that can rot.

## When Lossy Formats Make Sense

None of this means W3C VCs are bad technology. JPEGs are not bad because they are lossy — they are optimized for distribution. MP3s revolutionized music precisely because they discard inaudible frequencies to reduce file size. Lossy formats have their place.

W3C VCs are fine in contexts where stakes are low and political points, familiarity, and compatibility with web assumptions matter more than long-term verifiability. If you need to issue thousands of conference badges, gym memberships, or simple attribute assertions ("over 18," "email verified"), and the evidence will only be checked once or twice before it expires &mdash; and crucially, if an entire ecosystem uses the same DID method or at least DIDs that make compatible assumptions about trust, centralization, and cost &mdash; VCs work. The tooling is beginning to mature, and the learning curve for web developers isn't bad.

But you would not master an album in MP3, print a magazine cover from a JPEG, or archive a documentary film in lossy compression. For the same reason, you should not anchor long-lived, high-stakes identity systems in a lossy credential format.

When evidence must remain verifiable for decades, when historical queries matter ("Was this valid when the contract was signed?"), when trust relationships have nuance and weight, when ecosystems must span jurisdictions without centralized trust registries, or when post-quantum security is a requirement — you need lossless evidence. You need ACDCs.

## Real-World Validation

Theoretical advantages mean little without production validation. ACDCs have it.

The GLEIF verifiable Legal Entity Identifier ([vLEI](https://www.gleif.org/en/vlei/introducing-the-vlei-ecosystem-governance-framework)) system uses ACDCs to create a global trust graph for organizational identity. GLEIF issues root credentials to Qualified vLEI Issuers. QVIs issue credentials to legal entities (corporations, banks). Entities issue role credentials (CEO, CFO). Roles are assigned to individuals. Each credential links cryptographically to its parent via SAIDs. A verifier receiving an employee's credential can traverse the chain back to GLEIF without consulting a trust registry. The entire graph is self-certifying.

This is not a pilot. It is a production system, operating globally, across jurisdictions, without certificate authorities or blockchains.

Consider also the [Verifiable Voice Protocol](https://datatracker.ietf.org/doc/draft-hardman-verifiable-voice-protocol/04/), which aims to improve upon STIR/SHAKEN for secure voice calls. SHAKEN depends on certificate authorities approved by a per-country governance ecosystem. This is why it is being implemented country by country, not globally. The Verifiable Voice Protocol uses ACDCs to chain trust back to a global root, crossing jurisdictional boundaries without requiring each country to approve intermediaries. The trust graph spans borders because it is self-certifying.

## The Right Format for the Job

ACDCs and W3C VCs are not competitors in the way that Blu-ray and HD-DVD were. They are more like RAW and JPEG — formats optimized for different stages of the workflow.

Use W3C VCs when the evidence is short-lived, the relationships are simple, and web interoperability is paramount. Use ACDCs when the evidence must be archival, when trust relationships are complex and weighted, when historical verification matters, or when decentralization across jurisdictions is essential.

In an ideal world, you would maintain lossless ACDCs as the authoritative source of truth and generate W3C VCs from them when needed — just as you would export JPEGs from RAW files for web display. You keep the lossless original. You distribute the lossy derivative.

The evolution from document-centric identity to graph-centric identity is not just a technical shift. It is a paradigm shift from *claiming* truths on an issuer's direct say-so to *chaining* trust in sophisticated ways. For high-stakes systems — legal entity structures, supply chains, investigative journalism, voice authentication, anything that must remain verifiable for years — that shift is overdue.

Choose lossless. Keep your RAW files. And keep your JPEGs, too, if you like. But don't equate what the two technologies deliver.
