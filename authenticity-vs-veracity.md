# Authenticity vs. Veracity
Daniel Hardman &mdash; 28 Dec 2025

Since **authenticity** and **veracity** both evaluate truth, casual discussions sometimes conflate the two ideas. Philosophy and law have long recognized that this fuzziness is a mistake. However, when I first began working in cybersecurity and identity, the thinking was muddy. I credit Sam Smith and the KERI community for emphasizing the distinction in a helpful way (e.g., in the [KERI](https://trustoverip.github.io/kswg-keri-specification), [ACDC](https://trustoverip.github.io/kswg-acdc-specification), and [did:webs](https://trustoverip.github.io/tswg-did-method-webs-specification/) specifications).

## Formal definitions

### Authenticity
*Authenticity* focuses on the *truthfulness of an imputed origin*. If a painting appears to be signed by Picasso, and I say it is *authentic*, I am claiming that Picasso is the true originator of the painting.

### Veracity
*Veracity* focuses on the *truthfulness of claimed facts in content*. If a witness testifies in court, and I accept the *veracity* of their account, I believe that the assertions in their account convey details they truly witnessed.

## Independence
These two qualities sometimes relate in subtle ways. However, they must be analyzed primarily as *orthogonal*, to keep mental models crisp.

We see the independence easily with a painting: truth about the painter's identity and truth about a visual reality that served as a model for its brush strokes are separate questions. (Yes, the questions may be related, because a particular artist may have a reputation for painting from real life in a very "faithful" way, or because a particular painting is known to be an effort to capture what was seen with special care. Even so, we must not collapse the two questions.)

When we get into the realm of verifiable data, we sometimes stumble. The reasoning we want to do from data usually requires both qualities; the distinction can feel esoteric. Nonetheless, the dimensions remain independent. Suppose witness X gives an account under oath, and the court stenographer accidentally misattributes their account to witness Y. This would break the authenticity of the statement, but not its veracity. Or suppose you take an affidavit to a notary; the notary witnesses the authenticity of your affidavit, but makes no commitment as to its veracity.

The value of preserving this distinction becomes apparent when we consider that the way to prove each quality can differ. Judgments about authenticity can &mdash; *if managed very carefully* &mdash; be reduced to an objective mathematical computation, whereas judgments about veracity inherently require subjective assessments of reputation.

All approaches to identity require these qualities in crucial places. However, different approaches take advantage of the distinction to different degrees, and in so doing, accept different outcomes with respect to centralization, maintenance overhead, and achievable levels of assurance.