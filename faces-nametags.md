---
title: "Faces and Name Tags: Two Kinds of Trust"
author: "Daniel Hardman"
date: 2026-11-21
category: Primers
citations: acm
item_id: CC-PRI-261103
language: "en"
pdf_url: https://dhh1128.github.io/papers/faces-nametags.pdf
version: "1.0"
revision_date: 2026-11-21
keywords: "administrative trust, cryptographic trust, PKI, X.509, certificate authorities, self-certifying identifiers, KERI, ACDC, STIR/SHAKEN, root of trust"
abstract: "Digital trust answers two different questions: is this the same party as before, and who is this party in the world of names and laws? Mathematics can answer the first; only administration can answer the second. Classic PKI answers both administratively, which turns every failure of an authority into a failure of identity. Separating the two, as KERI does with self-certifying identifiers and issued attestations, confines administrative trust to the claims that need it."
description: "Digital trust answers two different questions: is this the same party as before, and who is this party in the world of names and laws? Mathematics can answer the first; only administration can answer the second. Classic PKI answers both administratively, which turns every failure of an authority into a failure of identity. Separating the two, as KERI does with self-certifying identifiers and issued attestations, confines administrative trust to the claims that need it."
listed: true
image: /assets/cards/faces-nametags.png
---

At a conference, you can know two different things about the person walking toward you. You may recognize her face: she asked the sharp question in yesterday's session. And you can read her name tag, which gives her name and her employer. The two kinds of knowledge feel alike, but they come from different places. Recognition needs no authority. You saw the face before, and you see it again. The name tag is only as good as the registration desk that printed it. If the desk was careless, or bribed, the tag lies, and nothing about the tag will tell you.

Digital trust has the same two kinds of knowledge. Bundling them together is why some trust systems are brittle, expensive, and hard to extend across borders. None of this distinction is mine. It comes from Samuel Smith's design of KERI [1], and I've applied pieces of it before [2, 3, 4]. This primer puts it in one place.

## Two questions

Any party you deal with online raises two questions. The first is about sameness: is this the party I dealt with before? The second is about introduction: who is this party in the world of names, organizations, and laws? Does it own example.com? Is it SomeCorp Ltd?

Math can answer the first question. A digital signature proves that whoever made it controls a particular private key. If two messages verify against the same key, or against keys linked by a verifiable chain of rotations, then the same controller made both. No authority has to vouch for that. Anyone, anywhere, can check it, and the answer doesn't depend on jurisdiction or on whose side you're on. Call this cryptographic trust.

Math can't answer the second question. No calculation can show that a key belongs to SomeCorp Ltd, because "SomeCorp Ltd" is a fact about the human world: an entry in some jurisdiction's registry, a set of people with legal authority to act. Someone has to look at that world and testify about it. Confidence in the answer is confidence in that someone — in the processes they follow, the people they employ, and the oversight they're under. Call this administrative trust.

Administration can answer both questions; math can answer only the first. Which one a system uses for sameness is a design choice.

Sameness is useful on its own, even when nobody knows the name. A detective who matches fingerprints from two burglaries knows that one person committed both, without knowing that person's name, address, or nationality. The link holds before any name turns up, and it stays true if the name the suspect eventually gives is false. Fingerprints aren't mathematics, and examiners do make mistakes [5], but the knowledge has the same structure: recognition first, introduction later, if ever.

## One answer for both

The web's public key infrastructure answers both questions administratively. An X.509 certificate is a certificate authority's (CA's) signed statement binding a name, such as a domain or an organization, to a public key [6]. In the conference picture, the CA is the registration desk. The browser doesn't recognize the server's face. It reads the name tag, and it trusts the tag because it trusts the desk that printed it. The tag even stands in for the face: a browser concludes that it's talking to the same google.com as yesterday only because a CA says so today. That choice has costs.

The first cost is that administrative failure breaks sameness, not just attributes. When attackers breached the DigiNotar CA in 2011, they issued certificates for google.com and used them to intercept users in Iran [7]. They didn't merely make a false claim about Google. To every browser that trusted DigiNotar, they were Google. Iranian Gmail users had met Google many times, but PKI gave their browsers no way to remember its face, so every visit was a first meeting. The one browser that caught the forgery was Chrome, which shipped with a built-in list of the keys allowed to vouch for Google [8, 9]. Nor are such failures exotic: Chrome stopped trusting Symantec's certificates in 2017 after a series of misissuance incidents [10]. And in October 2026, the Indian CA eMudhra turned out to have generated eight of its intermediate CA keys so badly that each was a number smaller than 256, recoverable almost instantly [11]. Within days, outsiders had used six of those keys to sign more than 100,000 proof-of-concept certificates, most of them naming google.com [12].

The second is that renewal is reassertion. When a certificate expires, the CA checks control again, usually through the ACME protocol [13], and issues a new binding. ACME keeps an account key across renewals, but that continuity is visible only to the CA [14]. The public sees a fresh assertion, often with a fresh key, and can't tell from the certificate whether its holder is the party that held the last one. Short lifetimes have a real purpose, which is limiting how long a stolen key or a stale validation stays useful. But as public TLS certificate lifetimes shrink to 47 days by 2029 [15], the desk will reprint every tag about eight times a year, and each reprint is another chance to get it wrong. Each reprint also costs something, whether as a fee for an organization-validated certificate or as the engineering it takes to automate renewal. The party paying is renting its own sameness, in Smith's terms [1], from a desk that reasserts it on a schedule. But a party that was the same party last month is still the same party today. A fact that stable shouldn't need reasserting at all, any more than a birth certificate needs renewing [3].

The third is that names have jurisdictions. A tag printed in Washington means nothing in Tokyo unless Tokyo trusts Washington's desk. STIR/SHAKEN, which signs telephone calls, shows how this plays out. Its governance model puts a national authority in charge of deciding which CAs may issue [16], and France runs a separate system under its own telecom regulator [17]. A receiving carrier trusts a call's signature only if the certificate comes from a CA on its own country's list. A carrier in one country has no way to establish, by itself, that a caller certified elsewhere is the same party it saw yesterday. It has only the other desk's word, and it may have no reason to accept that desk. The US and Canada work around this by cross-trusting each other's CAs. The US and France don't, so a French caller's certificate means nothing to an American carrier. Smith describes the general problem: an administrative identifier is locked to its trust domain, and so is any value attached to it [1, 4].

None of this is a complaint about CAs. Administration is the only way to answer the second question. The trouble comes from using it to answer the first one too, on the theory that if you need a registration desk for anything, you may as well use it for everything.

## Splitting the questions

The alternative is to give each question to the kind of trust that fits it. SSH can't tell you who a server is, but it remembers the server's key and warns you when the key changes [18]. Self-certifying pathnames applied the same idea to network file systems in 1998 [19]. Signal's safety numbers and Tor's onion addresses work the same way.

KERI makes the split systematic [20]. Its autonomic (self-governing) identifiers (AIDs) are self-certifying: each is derived from its controlling keys, and a key event log records every rotation, so sameness survives key changes and anyone holding a copy of the log can check it; because the log verifies itself, it doesn't matter who stores it. Claims about names and attributes travel separately, as Authentic Chained Data Containers (ACDCs) [21]: an issuer's signed statement that this AID controls example.com, or is SomeCorp Ltd. The issuers are AIDs too, so even the desk has a face. In PKI, a CA's own identity is one more name tag, vouched for by the CA above it.

The effect is to fence administrative trust in. Administration still fails, and a false attestation is still possible. But an attacker who tricks an issuer into attesting that their AID owns google.com doesn't thereby become Google's AID. Anyone who already knows Google's AID sees two different faces wearing the same name tag. For a site like Google, that is nearly everyone. Only a true first meeting still depends on the tag alone. And a verifier in Tokyo can reject a Washington issuer's attestation and still know it's dealing with the same party as yesterday. Disagreements about authorities stay inside the attestations. They no longer reach identity.

## What math doesn't do

Cryptographic trust isn't trust in nothing. It relies on sound algorithms, and on controllers who guard their keys. A face can't be stolen, but a key can, and then the math faithfully recognizes the thief. A weak key ruins sameness in either world, but the damage differs. eMudhra's weak keys let anyone impersonate any website in every major browser, while a weak AID key compromises one AID. KERI limits that damage by committing in advance to the next key, so a controller whose signing key is stolen can rotate it out of the thief's hands [20]. It also says nothing at first contact. The first time you see a face, recognizing it tells you nothing about who it belongs to, which is why you still need the name tag. KERI also uses witnesses and watchers to catch a controller who tells different stories to different audiences. They're infrastructure rather than authorities, though: each witness signs a receipt for every key event it sees, and a verifier checks that the receipts agree, so a witness that lies gets caught instead of believed.

## Both, in their places

A complete trust system needs both kinds of trust, each used for what it can do. Math is the right foundation for sameness, because it's universal, durable, and indifferent to borders. Administration is the only source of introductions, and it works best when it's scoped to the claims only it can make, about a party whose identity doesn't depend on it. Build everything on the registration desk, and every failure of the desk becomes a failure of identity. Let math carry the faces, and the desk only has to get the names right.

## References
[1] Smith, S. M. 2019. Key Event Receipt Infrastructure (KERI) Design. Version 2.62, January 3, 2024 (original July 3, 2019). arXiv:1907.02143. https://arxiv.org/abs/1907.02143

[2] Hardman, D. 2026. Where Trust Bottoms Out: X.509, Certificate Transparency, and KERI's DPKI Architecture. Codecraft Papers. https://dhh1128.github.io/papers/wtbo.html

[3] Hardman, D. 2024. Why X509 Certs Should Be Secondary Evidence of Org Identity. Codecraft Papers. https://dhh1128.github.io/papers/x509-prob.html

[4] Hardman, D. 2026. What Does Telco Need? Requirements for Organizational Identity Evidence. Codecraft Papers. https://dhh1128.github.io/papers/telco-ev-reqs.html

[5] U.S. Department of Justice, Office of the Inspector General. 2006. A Review of the FBI's Handling of the Brandon Mayfield Case. https://oig.justice.gov/sites/default/files/archive/special/s0601/final.pdf

[6] Cooper, D., Santesson, S., Farrell, S., Boeyen, S., Housley, R., and Polk, W. 2008. Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) Profile. RFC 5280. IETF. DOI: https://doi.org/10.17487/RFC5280

[7] Fox-IT. 2011. DigiNotar Certificate Authority Breach "Operation Black Tulip" (interim report, September 5, 2011). https://docslib.org/doc/2849857/diginotar-certificate-authority-breach-operation-black-tulip

[8] Adkins, H. 2011. An update on attempted man-in-the-middle attacks. Google Security Blog, August 29, 2011. https://security.googleblog.com/2011/08/update-on-attempted-man-in-middle.html

[9] Langley, A. 2011. Public key pinning. ImperialViolet, May 4, 2011. https://www.imperialviolet.org/2011/05/04/pinning.html

[10] Sleevi, R. 2017. Chrome's Plan to Distrust Symantec Certificates. Google Security Blog. https://security.googleblog.com/2017/09/chromes-plan-to-distrust-symantec.html

[11] Mozilla. 2026. Bug 2083449: eMudhra: Private key compromise of Intermediate Certificates. Mozilla Bugzilla, comment 0 (incident report, October 18, 2026) and comment 5 (key analysis, October 18, 2026), both by D. Jackson. https://bugzilla.mozilla.org/show_bug.cgi?id=2083449#c5

[12] Mozilla. 2026. Bug 2083449: eMudhra: Private key compromise of Intermediate Certificates. Mozilla Bugzilla, comment 44 (October 25, 2026), reporting 107,107 certificates signed with six of the compromised keys and logged to Certificate Transparency on October 20–21, 2026, of which 106,050 were proof-of-concept certificates for google.com. https://bugzilla.mozilla.org/show_bug.cgi?id=2083449#c44

[13] Barnes, R., Hoffman-Andrews, J., McCarney, D., and Kasten, J. 2019. Automatic Certificate Management Environment (ACME). RFC 8555. IETF. DOI: https://doi.org/10.17487/RFC8555

[14] Hardman, D. 2025. A Primer on KERI, ACDCs, and CESR. Codecraft Papers. https://dhh1128.github.io/papers/keri-primer.html

[15] CA/Browser Forum. 2025. Ballot SC081v3: Introduce Schedule of Reducing Validity and Data Reuse Periods. April 11, 2025. https://cabforum.org/2025/04/11/ballot-sc081v3-introduce-schedule-of-reducing-validity-and-data-reuse-periods/

[16] ATIS. 2020. Signature-based Handling of Asserted Information using toKENs (SHAKEN): Governance Model. ATIS-1000080.v002. https://cstga.ca/wp-content/uploads/2020/07/ATIS-1000080.v002_SHAKEN-Governance-Model.pdf

[17] ARCEP. Authentification des numéros de téléphone fixe ou mobile : que faire en tant qu'opérateur téléphonique ? Autorité de régulation des communications électroniques, des postes et de la distribution de la presse. https://www.arcep.fr/mes-demarches-et-services/acteurs-regules/operateurs-telecoms/fiches-pratiques/authentification-numeros-telephone-fixe-ou-mobile-que-faire-en-tant-que-operateur-telephonique.html

[18] Ylonen, T. and Lonvick, C. (Ed.). 2006. The Secure Shell (SSH) Protocol Architecture. RFC 4251, section 4.1. IETF. DOI: https://doi.org/10.17487/RFC4251

[19] Mazières, D. and Kaashoek, M. F. 1998. Escaping the Evils of Centralized Control with Self-Certifying Pathnames. In Proceedings of the 8th ACM SIGOPS European Workshop. ACM, 118–125. DOI: https://doi.org/10.1145/319195.319213

[20] Smith, S. M. Key Event Receipt Infrastructure (KERI) Specification. Trust Over IP Foundation, living draft. Retrieved November 20, 2026 from https://trustoverip.github.io/kswg-keri-specification/

[21] Smith, S. M. and Feairheller, P. Authentic Chained Data Containers (ACDC) Specification. Trust Over IP Foundation, living draft. Retrieved November 20, 2026 from https://trustoverip.github.io/kswg-acdc-specification/
