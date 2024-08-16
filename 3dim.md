# Three Dimensions of Identity
### A Simplified Look At a Complex Topic
Daniel Hardman and Jason Law &mdash; 29 Jan 2019 &mdash; Evernym and medium.com 

We all know that identity matters. We hear about cybersecurity breaches, GDPR, refugees, deep fakes, and election fraud. Each headline highlights a new way that identity impacts us.

Yet we may be accepting naive assertions about what identity actually means. Some equate identity with authentication. Others map it to accounts and credentials. Still others think of it as a personal data and metadata issue. Such mindsets may feel reasonable, but each simplifies too much. Identity manifests in several dimensions. Identity solutions must model all of these dimensions to be complete.

## Identity as Relationships: Perspective Matters
One dimension of identity is the relationships that give it context. We share ourselves differently in different relationships. Coworkers see us in one way, family members, doctors, and governments in others. Social networks prove that the relationship dimension of identity matters.

![relationship axis. Image credit: Evernym](rel-axis.webp)

Many identity solutions collapse all versions of “you” to a single construct. In LDAP, for example, each user has a unique but universal identifier. The user in an email group and the user that participates in an HR reporting relationship are the same user. When you use login with Facebook or Google, this same consolidation of “you” repeats on the web.

This may feel convenient, but it raises privacy concerns. If everyone identifies you the same way, then they can share information about you. Unchecked, correlation and surveillance become scary. Regimes could hunt political dissidents, cyberbullying could become inescapable, and privacy could vanish. This is one reason why Sovrin — a new global utility for self-sovereign identity — is so fanatical about partitioning all the shards of “you” so carefully.

## Identity as Attributes: Facts Abound
Another dimension of identity is information about us. We share our data in obvious ways, through a driver’s license or medical chart, for instance. But our identities also leak more subtly. The gamer who customizes the appearance of an avatar is sharing personal preferences. The Facebook quiz about how many ’80s pop songs we remember leaks demographics. Marketers track thousands of these overt details.

![data axis. Image credit: Evernym](data-axis.webp)

Identity without this factual dimension has limited use. Banks need facts to lend us money. Doctors need our medical history and current medications to optimize our care.

This highlights an interaction between the relationship and data (attributes) dimensions of identity. We don’t mind telling a doctor about our elective surgery — we just don’t want our friend at the PTA to know it. GDPR’s purpose limitation principle requires such granular control. This challenges the business models of many internet giants. (A future post will explore how giving users such control can be a win-win.)

## Identity as Agents: Work is Delegated
A third dimension of identity is the agents that represent us. When we text our friends, we use a phone to capture and relay our words, and our friends perceive us through similar technologies. Our phone acts as our agent. Almost all digital interactions use agents. Humans can’t directly transmit bytes, decrypt with private keys, and so forth.

Agents can also be people — lawyers or realtors, for example — who act as our fiduciaries.

![agent axis. Image credit: Evernym](agent-axis.webp)

To have a trustworthy identity, we must have trustworthy agents. We expect lawyers to keep our confidences, and even enforce such behavior. Unfortunately, identity tech is rife with flaws in this regard.

Some flaws are policy-based. When Facebook bought WhatsApp, it said it wouldn’t optimize ads with chat content. A year later, it backtracked, leaving a billion users with a Hobson’s choice on privacy.

Other flaws are conceptual. Most cybercrime hinges on an act of impersonation by a nefarious actor. If agents are the attack vector, a protection is to give them distinct keys from their masters. This is a well-understood principle in the tangible world. Lawyers who represent us don’t forge our signature on documents. Yet we see identity systems where a trusted third party holds the identity owner’s keys…

## Planes
Any two of these dimensions of identity form a plane. It is in these planes that identity questions begin to find powerful answers.

The Relationship ~ Attribute plane is where we answer the question: Who knows what about me?

![relationship ~ attribute plane. Image credit: Evernym](rel-attr-plane.webp)

Some models oversimplify relationships. They answer this question in just one way: everybody knows the same “you.”

Some models oversimplify attributes. They make sharing an all-or-nothing decision.

If both dimensions of identity are granular, you can make powerful, privacy-preserving choices. Suppose you have an employment credential with your name, role/title, and salary. You could choose to share only name and salary when you apply for a loan:

![sharing name and salary only. Image credit: Evernym](share-name-salary.webp)

To maximize privacy, you must share attributes in an unlinkable way. Hyperledger Indy (and Sovrin, built atop it) makes this possible. It proves the origin of data in a digital credential without sharing the signature. Other technologies ignore this requirement and incur big disadvantages as a result. (Even with Indy, you can disclose a strong correlator, like first and last name. The mistake of less powerful models is in not making disclosure optional.)

The Relationship ~ Agent plane is where we answer the question: Which proxy represents me in which contexts, and how?

![relationship ~ agent plane. Image credit: Evernym](rel-agent-plane.webp)

This matters in the tangible world. We let realtors represent us when buying a house, but we don’t let them decide whether to take us off life support. Legal and political events hinge on such questions. Were political operatives acting as Nixon’s agents when they burglarized Watergate? Was the software behind the 2014 hack of Sony Pictures working for North Korea?

Yet we sometimes see identity models that collapse this plane. They simplify by assuming that an agent in one relationship is an agent in all. Or they simplify by assuming that a relationship is serviceable by all agents. This is not good enough. Should my laptop, but not my phone, be authoritative when transferring more than $1,000 USD? Do I want my cloud agent to store and forward messages, but not to read them or to sign on my behalf?

The best answers involve careful, granular choices about key management. Moving keys to the edge is an important default. It improves security over centralized systems that trust a third party. However, this principle demands smarter agents and is often ignored.

The Agent ~ Attribute plane is perhaps the least familiar. It answers the question: Which proxy can share what about me?

![agent ~ attribute plane. Image credit: Evernym](agent-attr-plane.webp)

This plane is where you choose which agents know what about you. It is also where you authorize agents to re-share what they know. You may not want to wrestle details — and with carefully designed user experience, you may not need to. Nonetheless, an identity model that supports choices here has huge benefits.

Suppose Fred, a PhD chemist, is looking for work. He approaches two recruiting firms about helping him with a placement. One specializes in academia; the other, in industrial research. Fred crafts one resume that emphasizes his publications and lecture experience, and another that focuses on his patents and inventive innovations. In doing so, he is making choices in the Agent ~ Attribute plane, since one agent can share different attributes of his identity than the other.

Identity models often neglect this plane. In doing so, they may miss requirements in regulation, cybersecurity, and user experience. Maybe your desktop gets IT attention, runs backup software, and unlocks by fingerprint. In contrast, you might misplace your phone on a restaurant counter or the back seat of a taxi on any given day. Do these two agents have the same security and auditing standards — or should their cryptocurrency wallets vary? Would you like to say that your phone can only spend small amounts of money, while your desktop has no limit? This plane lets a user limit mischief when a phone goes missing or a cloud service gets hacked.

## Beyond Planes — Into 3-Dimensions
Planes are not the end of the story. We can model decision points anywhere in 3-dimensional space. That may sound esoteric, but it matches choices we make every day. We use an iPad and a workstation and a phone for a mixture of personal and professional work. We put different credentials and personal data on each. We configure them to share different things about us. These are 3-dimensional identity decisions.

![3 dimensions. Image credit: Evernym](3d.webp)

Of course, complex decisions are not a selling point for users. Mishandled by software, they can be an annoyance, a burden, and a security problem. But the solution is not to design systems that ignore the complexity. This shifts the problem to users without any tools or guidance. Rather, we should model identity in its full richness. Then we should automate away what’s unhelpful in a given context. Only then will we have an identity that’s intuitive, flexible, and robust.