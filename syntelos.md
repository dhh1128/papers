# Syntelos: A Hierarchical Taxonomy of Intent in Digital Interactions

Abstract — The transition from direct human-computer interaction to an economy of agentic AI highlights an inadequacy that's always permeated digital architecture: the dissociation of mechanical action from human purpose. Proximate intents (e.g., clicking a button) are conflated with ultimate intents (e.g., consuming entertainment or entering a contract), rendering signaling mechanisms brittle and unsuitable for automated policy. Existing classification standards such as NAICS, UNSPSC, and FIPA ACL categorize actors, objects, and message envelopes, but say too little about high-level intent. Drawing on Activity Theory and Commitment Protocols, this paper proposes a taxonomy for intent that's rooted in shared outcomes rather than unilateral actions. This provides a rich, rigorous, machine-readable standard for constraining delegation and negotiating interactions. Principals can reference the taxonomy when creating policy for AI and human agents.

Keywords — agentic AI, multi-agent systems, digital intent, human-agent interaction, semantic interoperability, decentralized identifiers, activity theory, commitment protocols, intention economy, policy engines, intent casting, goal codes, consent, model context protocol, intent boundaries

# 1\. The unacknowledged gap in digital interactions

## 1.1 Decoupled action and purpose

The ordinariness and ease of our digital interactions masks a profound semantic void. Alice browses content on a smart television and clicks "Watch". Her intent is straightforward and sensory: view a drama about a veterinarian in the Yorkshire Dales. To the media streaming service, however, that click might upgrade a subscription, alter billing terms, or consummate a commercial transaction. Alice intends to watch; the system intends to sell. Is there enough alignment to proceed?

The answer is undefined, and this is a problem. Our system architectures, imagined and paid-for by service providers, hold Alice-the-client responsible for resolving the doubt using whatever tools might be available—hover text, a hyperlink to terms and conditions, an advertisement for special upgrade pricing that brought her to the content, etc. Given the variety of parties that might play the role of Alice in this scenario, is this onus on clients realistic? Is it ethical? The nagging ambiguity, often shrugged off by invoking *caveat emptor*, or by lamenting sloppy user experience or a "dark pattern", actually reveals a failure in our digital architectures. We have perfected the transmission of data but built only the crudest models of intent. [1]

Imprecision about intent has long been an annoyance, but it becomes more critical with the rise of agentic AI. Part of the attractiveness of AI agents is that they accept fuzzy input. Their outputs are not deterministic, either. [2, 3] Allowing them to make fuzzy judgments about the intent of their human principals or counterparties is risky.

Human guesses about intent, especially when counterparties might be AI, are equally problematic, and they're getting worse. For example, when a human answers the phone, they instinctively assess the caller's purpose from context cues—history of the relationship, tone of voice, background noise, or the opening sentence. Such guesses have always been suspect, but AI is now associated with some dramatic failures in this strategy. [4, 5, 6, 7]

Yet we continue to be vague. Rich Call Data (RCD) embodies telco's latest thinking on intent. RCD imagines each call arriving with an explicit *call reason*, a text string like "debt collection". [8, 9] The aspiration is good, but the mechanism is far too limited. It is not machine-readable. It requires the caller to predict the callee's language. It lacks hierarchy. Given a desire to accept only calls that are "business-related", or only calls about "loans", how should Alice or Alice's AI agent react to a call about "debt collection"? The answer remains undefined. We're stuck at *caveat emptor*.

If we are to interact confidently in the low-context environment of remote+digital, or if we are to delegate authority to human or AI agents that will interact there on our behalf, we must equip them with a grammar of purpose. This grammar should allow us to describe whether managing our calendar, negotiating purchases, accepting promotional offers, or filtering our interruptions aligns with our intent. In other words, we need a hierarchical taxonomy of reasons to interact that allows us to define boundaries with precision. Alice must be able to ask another party why they're proposing to interact, and understand the answer. Alice must be able to say to her agent, "You may negotiate *scheduling* on my behalf, but you may not engage in *high-value commerce* without my explicit approval."

## 1.2 Intensifying need

The need for this taxonomy is driven partly by globalization. Remoteness has decreased the context that's assumable from location, legal jurisdiction, and culture. It has also made redress harder.

Disintermediation reinforces the need. The web, search engines, mesh computing, social media, and online gaming all invite strangers to interact unpredictably. We begin encounters with less groundwork and weaker social mores to manage expectations.

The need for a grammar of intent is further accelerated by an ongoing shift toward what Doc Searls calls the “Intention Economy.” In the older “Attention Economy,” vendors broadcast noise to capture fleeting consumer attention. In the Intention Economy, buyers broadcast specific intent (e.g., “I want to buy a Nikon D6 camera for under $300”), and sellers compete to fulfill it. [10, 11, 12] Intentcasting clearly requires a structured vocabulary. It already shapes markets such as ridesharing and peer-to-peer lodging, and it will likely expand as smart agents proliferate.

## 1.3 Syntelos

This paper explores important taxonomy work that already exists, pinpoints the specific gap that remains, and proposes some principles that should inform any approach. It then applies these principles to derive the basics of a taxonomy of intent in digital interactions, and describes how the taxonomy can be extended. The methodology and its base categories are named "Syntelos" for reasons that are clarified below. Syntelos is a rich, rigorous, machine-readable set of categories that can deliver significant value for agentic AI and ultimately, for all human stakeholders.

# 2\. Current standards address different questions

To design a successful taxonomy, we must first examine the catalog of existing classification systems. While rigorous and widely adopted, systems like NAICS, UNSPSC, FIPA ACL, and GDPR processing purposes do not cover the specific requirements of digital intent for distinct, structural reasons.

## 2.1 Industrial codes: the who vs. the what

The North American Industry Classification System (NAICS) and the Standard Industrial Classification (SIC) are ubiquitous in business. [13, 14] They provide a deep hierarchy for classifying economic activities. *Example*: 541511 corresponds to "Custom Computer Programming Services."

* *Gap*: These codes classify establishments, not interactions. A software company (NAICS 541511) does not only engage in "programming." Its agents also engage in Hiring (HR), Purchasing (Procurement), Lobbying (Government), and Scheduling (Coordination). If a user receives a call from an entity with NAICS 541511, they know who is calling, but not why. Is the software company trying to sell a product? Schedule an interview? Collect a bill? NAICS cannot distinguish these intents. It creates a category error: confusing the identity of the actor with the nature of the act.

* *Utility*: NAICS is useful as a *parameter* (e.g., Proposer.Industry = 541511), but not as the root of the intent hierarchy.

## 2.2 Commodity codes: the object vs. the activity

The United Nations Standard Products and Services Code (UNSPSC) is a granular taxonomy for products. [15]

* *Example*: Segment 43 (IT Broadcasting) -> Family 21 (Computer Equipment) -> Class 16 (Computer Accessories) -> Commodity 02 (Docking stations).

* *Gap*: UNSPSC classifies the *direct object* of the sentence, but lacks the *verb*. It can describe a "Docking Station" with precision, but it cannot distinguish between:

  * Buying a docking station.  
  * Selling a docking station.  
  * Repairing a docking station.  
  * Recycling a docking station.

* *Utility*: Like NAICS, UNSPSC is an essential *parameter*. Our taxonomy should not reinvent the wheel by listing every product on earth. Instead, we should define the activity (/trade/swap) and use UNSPSC to define the subject (Resource: UNSPSC:43211602).

## 2.3 Financial standards: domain-bound rigor

ISO 20022 and the Financial Industry Business Ontology (FIBO) offer incredible semantic depth. [16, 17, 18, 19] They model complex interactions like "Securities Settlement" or "Credit Transfer" with rigorous precision.

* *Gap*: These standards focus exclusively on the *financial domain*. While they handle commerce perfectly, they have no vocabulary for "scheduling a doctor's appointment," "verifying a university degree," or "finding a tennis partner."

* *Utility*: We should adopt the structure of ISO 20022—specifically its separation of "Business Area" from "Message Definition"—but we must broaden the scope to cover the full spectrum of human interaction.

## 2.4 Agent communication languages: the envelope vs. the letter

FIPA ACL (Foundation for Intelligent Physical Agents Agent Communication Language) defines communicative acts like inform, request, propose, refuse. [20, 21]

* *Gap*: Starting a hierarchy with "Request" is a dead end, because it doesn't narrow the semantic field at all. A request is merely a carrier. A "request" to launch a nuclear missile and a "request" to update a calendar are indistinguishable at the top level of FIPA ACL. This is akin to sorting mail by the size of the envelope rather than the department it is addressed to.

* *Utility*: FIPA ACL defines the *proximate action* (the message type), whereas our taxonomy categorizes goals.

## 2.5 Schema.org: the fuzzy middle

Schema.org provides a hierarchy of Action types, such as TradeAction, OrganizeAction, and InteractAction. [22, 23]

* *Gap*: While conceptually close, Schema.org is designed for Search Engine Optimization (SEO), not binding policy. It is often permissive and fuzzy. Furthermore, it tends to be verb-centric (BuyAction vs. SellAction) rather than interaction-centric (Trade). This creates a perspective problem where Alice and Bob describe the same interaction with different root nodes, complicating the matching process.

* *Utility*: Schema.org serves as a valuable source of categories (e.g., the distinction between Consume and Create), but requires re-expression in a stricter and more omnidirectional structure.

## 2.6 Mobile permissions: a primitive ancestor

Android and iOS permission models (e.g., READ_CONTACTS, ACCESS_FINE_LOCATION) represent a primitive taxonomy of intent. [24, 25, 26] When an app requests permission, it is effectively declaring an intent to "use location data."

* *Gap*: These are *resource-centric*, not *activity-centric*. They gate access to hardware (camera, GPS) or data (contacts), but they do not describe the social or economic purpose. An app might request READ_CONTACTS to "find friends" (Social) or to "spam your network" (Malicious Commerce). The permission model cannot distinguish these intents.

* *Utility*: This highlights the need for our taxonomy to govern *high-level goals* (Why do you need contacts?) rather than just *low-level resources* (Can I access the database?).

## 2.7 Data Privacy Vocabularies: The compliance vs. agency distinction

The W3C Data Privacy Vocabularies and Controls (DPV) group has developed a rich taxonomy for categorizing the purpose of data processing. It includes granular categories such as ServiceProvision, Marketing, IdentityVerification, and Security. [27]

* *Gap*: DPV is data-centric, not interaction-centric. It is designed to answer the regulatory question, "On what legal basis are you processing this data?" rather than the agentic question, "Why are we starting this interaction?"

For example, DPV might tag a dataset with the purpose Marketing. However, it cannot distinguish between an agent sending a marketing offer and an agent soliciting offers.

* *Utility*: DPV is the ideal standard for the parameters of a Syntelos interaction. Once two agents agree on a Syntelos intent (e.g., /govern/identify), they should use DPV codes to define the privacy constraints of the specific data exchanged (e.g., dpv:Purpose = ServiceRegistration).

## 2.8 IEEE 7012 (MyTerms): The Terms of Engagement

While W3C DPV offers a vocabulary for privacy purposes, IEEE 7012 (Standard for Machine Readable Personal Privacy Terms) offers a protocol for negotiating those terms. Often called "MyTerms," this standard reverses the "click-wrap" paradigm: instead of the user accepting the vendor's terms, the user's agent proffers its own terms to the vendor. [28]

*The Synergy*: Syntelos and IEEE 7012 are complementary halves of a sovereign interaction. Syntelos defines the intent (/trade/swap), while IEEE 7012 defines the constraints (No-Tracking, Data-Deletion-After-30-Days).

*Operational Integration*: A Syntelos intent-cast serves as the envelope that carries the IEEE 7012 contract. Agent A says: "I intend to /trade/swap (Syntelos), provided you agree to MyTerms.Standard.NoSaleOfData (IEEE 7012)."

*Utility*: IEEE 7012 solves the negotiation complexity in the Syntelos Commerce.Negotiation branch. Rather than inventing a new negotiation language, Syntelos agents can simply reference an IEEE 7012 URI to establish the legal ground rules before the economic transaction begins.

# 3\. Theoretical foundations

To build a robust taxonomy, we must rigorously define some concepts, drawing on philosophy, psychology, and computer science.

## 3.1 General to specific

Interactions may be categorized in various ways — by size, frequency, cardinality, risk profile, and so forth. However, given that we're trying to enable purposeful decision-making, building root categories based on purpose feels like an appropriate starting point, with secondary considerations playing a role as granularity increases.

Of course, the idea of root categories presupposes hierarchy. Not all taxonomies are hierarchical. It is possible to have a faceted taxonomy that models a directed acyclic graph (tag clouds, semantic proximity in a thesaurus, Amazon's product catalog). It is possible to have a bottoms-up taxonomy (folksonomies that cluster like items into progressively larger abstractions). However, top-down taxonomies have a compelling advantage with respect to processing intent: *they allow confident generalization*. If we know that a policy exists for intent /x/y/*, then we know it also applies to intent /x/y/z (unless overridden). This facilitates cascading models of consent and delegation. A user can approve or block a broad range of intents (/trade/*) or a specific slice (/trade/lend/*). [29]

Taxonomies that proceed from generic to specific also force precision and reveal debatable assumptions. Other approaches tolerate overlaps and lacunas in ways we want to eliminate. Essentially, we want an analog for biology's cladistics — including the rigorous analysis and debate it implies — for the problem domain of digital interactions.

Finally, hierarchical taxonomies have learnability advantages, map nicely onto namespace and organizational behavior constructs, and are easy to adapt to certain algorithms. For all of these reasons, we assume that our goal should be to accurately and gracefully *organize intents from general to specific*.

## 3.2 Motives vs. steps

Activity Theory, originating from the Soviet psychologist Aleksei Leontiev, reinforces our preference for hierarchy. It explains how a hierarchy of purpose might organize. [30, 31, 32] Leontiev argued that human behavior is not a flat sequence of tasks but a structured hierarchy of *Activities*, *Actions*, and *Operations*:

| Level | Definition | Digital Equivalent |
| :---- | :---- | :---- |
| Activity | Driven by a motive to satisfy a need (e.g., "Treating a patient"). The motive gives meaning to the lower levels. | The Taxonomy Root (/care/treat). |
| Action | Conscious, goal-directed steps taken to realize the activity (e.g., "Checking vitals"). | The Protocol Step (e.g., AssessCondition). |
| Operation | Routine, often unconscious adjustments to conditions (e.g., "Counting pulses"). | The API Call (e.g., HTTP POST, TCP Handshake). |

A key insight of this framework is that an action (mappable to a granular intent) only makes sense (carries a full semantic payload) in the context of its containing activity (a higher-level intent). "Checking vitals" is meaningless—or arguably indistinguishable from "gathering information"—unless we know the motive is "treating a patient." This suggests that our taxonomy should *root itself in a shared motive that binds the participants and gives vital context to lower-level actions*.

## 3.3 Proximate vs. ultimate continuum

Actors may engage in interactions with many different intents, and our taxonomy should help us compare them. However, applying Activity Theory's distinctions, we observe that two intents may amount to the same thing or to very different things, depending on the assumptions about the causality horizon.

When Alice clicks a "Watch" button, she simultaneously maintains intents at different causality horizons. She intends the proximate action (clicking the interface) as the means to fulfill at least one ultimate activity — possibly several. [1] It thus becomes important to distinguish between *proximate* and *ultimate intent*; a single proximate intent may have multiple ultimate intents, and a digital agent must understand the latter to effectively automate the former.

* ***Proximate Intent***: A purpose of a specific action that's characterized by direct, near-term context with minimal assumptions about causality. Referencing the introductory example where Alice streams a movie, she would be describing proximate intent if she says: "I clicked the Watch button so I could watch the movie."

* ***Ultimate Intent***: A longer-term purpose that the action is imagined to serve because it is connected by a chain of time and causality. This is the end for which a proximate act is intended as the means, and is associated with Aristotle's *final cause* or τέλος (*telos*). [33] If Alice says, "I clicked the Watch button so I could (by watching the movie) improve my Brazilian samba skills", she is describing a more ultimate intent.

*Proximate* and *ultimate* are not binary distinctions, but rather opposite ends of a continuum with many intermediate possibilities. A given intent may be either *more or less proximate* (*less or more ultimate*) than another intent.

Our taxonomy should *make siblings out of categories that are roughly equivalent on the proximate-ultimate causality continuum*.

## 3.4 Commitment protocols and social state

In the realm of Multi-Agent Systems (MAS), researchers have moved beyond simple message-passing to model interactions as commitment protocols. In this view, the "meaning" of an interaction is not defined by the sequence of messages (which can vary) but by the social commitments created between agents. [34]

A commitment is formalized as `$C(Debtor, Creditor, Antecedent, Consequent)$`. [35, 36]

In this formalism, `Debtor` refers generically to the agent making the commitment (the "committer"), and `Creditor` refers to the agent receiving it (the "beneficiary"), regardless of whether the commitment is financial, informational, or logistical.

Example: "If you approve this pull request (Antecedent), I will deploy the code to production (Consequent). `Debtor` = the developer; `Creditor` = the team lead

The interaction is a process of creating, manipulating, and discharging these commitments. This perspective is vital for our taxonomy because it shifts the focus from conversation to a social contract of shared expectations. It is the latter that informs most of our digital interactions: the intent is to enter into a state where a specific commitment exists or is constructed or fulfilled. Where applicable, the taxonomy should therefore *reflect the types of commitments agents can make*.

## 3.5 Multiple perspectives

In the camera intentcasting example mentioned in section 1.2, if Carlos broadcasts an intent to "buy," and Deepa has an intent to "sell," we'd like to help them recognize that an interaction might make sense, despite their opposing perspectives. A viable taxonomy should therefore avoid categorizing in a way that describes only one perspective.

It would be easy to say that categories must be bidirectional, but in fact we can't assume that two perspectives suffice, either. Many activities imply complex groups with a multiplicity of roles. Common examples include scheduling a surgery, conducting a parliamentary vote, brokering an introduction, and enacting an online auction. The taxonomy must *map an interaction to a category in such a way that all stakeholders recognize the category's applicability in a given context, despite their different perspectives*.

## 3.6 Intent boundaries and trust

The concept of ***intent boundaries*** further refines this by highlighting the ethical and UX implications of intent. [1] An intent boundary is a point where one party's knowledge of another party's intent becomes inadequate. Crossing such a boundary without confirmation (e.g., the "Watch" button upgrading a streaming subscription) is an unethical violation of agency. It opens opportunities for manipulation and abuse, and is thus likely to lead to diminished trust in the long run.

Our taxonomy should therefore *draw lines at likely intent boundaries*, because they represent ideal points for consent and policy enforcement.

## 3.7 Telos

Synthesizing the preceding principles, we might propose to root our taxonomy in *shared activities with clustered purposes*. This approaches the semantic we need. However, the wording is a bit loose. "Shared activities" could hide a distinction between doing something *parallel to* another party, and doing it *by interacting with them as a counterparty*. Friends might each use a language learning app to study French, and might describe their studies as a shared activity. Nevertheless, if their studies are independent and never intersect, they are just operating in parallel, not interacting. The proposed taxonomy is needed to enable decisions about interactions among counterparties, not just activities with a vaguely shared dimension.

A refinement might be to categorize *interactions* by their *potential outcomes*. Certainly outcomes are important inputs for decision-making. Assuming rational actors and complimentary postures toward cameras in intentcasting, Carlos and Deepa should at least agree that asset transfer is a possible outcome of a potential interaction, and each can use "asset transfer" as a framing to decide whether to begin.

However, "outcome" is still a suboptimal word. A given category of interaction might have many possible outcomes. Plus, the word "outcome" may invite overly strong opinions about the timeframe or arc of an interaction. Erika and Fahad need a way to talk about whether they should have an online dating interaction, even if their perspectives on the likely or intended outcome differs radically.

For all of these reasons, we lean on a term that's related to "outcome", but that has slightly more malleable nuances. In the context of this paper, we define the ***telos*** of an interaction as *the potential outcome that all rational stakeholders should agree embodies the interaction category's raison d'être, imagined as far toward ultimate intent as consensus allows, and framed with maximum specificity.*

In intencasting for a camera:

* *Transferring assets* is a good summary of the telos.  
* *Failing to come to terms*, *redefining the goal*, and *timing out* might all be possible outcomes, but they are not the raison d'être of the interaction and thus cannot be the telos.  
* *Mutual gain* (the economic idea that each party will give up something they value less and receive something they value more) is also a true characterization of the goal, but it is less specific than *transferring assets*, so it a less optimal statement of the telos.  
* *Deciding whether a specific camera pleases Carlos* might be an accurate answer to the question, "Why might this buyer and seller start interacting?", but it is a statement about a *specific interaction*, not an interaction *category*, so it cannot be the telos.

In online dating:

* *Having fun*, *finding a spouse*, *annoying one's former partner*, *improving social skills*, and *escaping boredom* are all possible reasons to engage in the interaction, and some could be viewed as more specific than just *dating*. However, rational stakeholders will not all agree that these reasons are the broad raison d'être for the interaction category, because they are too ultimate (not proximate enough) to apply consistently. They cannot be the telos.  
* The most ultimate and specific reason to date that all rational stakeholders are likely to agree on is simply to date because it is has some reward for the participants. This makes the activity its own telos.

While the definition of *telos* is intended to support rigor and subtle distinctions, the basic question it addresses is straightforward: "What is the best mutually intelligible raison d'être for an interaction that someone proposes to start?"

## 3.8 Parameterization

We must avoid the trap of enumerating the infinite. Given human limits on attention, decision-making, and configuration ability, a massive hierarchy is an antipattern, especially if all the leaf nodes are identical except for a specific attribute that changes decision criteria but nothing about the nature of an interaction. For example, we don't want separate categories in our taxonomy for buying blue shoes and red shoes; although an actor might make different decisions in these two cases, the character of the interaction is essentially the same. Instead, the taxonomy should leverage *parameters* for the "who" and the "what," utilizing existing standards like UNSPSC where they shine—at the leaf level.

* *Intent*: /trade/swap

* *Resource (What)*: UNSPSC:53111601 (Men's Shoes)

* *Role (Who)*: Proposer=Seller, Recipient=Buyer

The taxonomy should probably also leverage parameters for the "where" (platforms, channels, physical or virtual locations) and the "how" (paying for a purchase with method A versus method B).

This keeps the taxonomy lean and maintainable while allowing for infinite specificity via external code sets from other standards.

## 3.9 The consent distinguishability test

A proposed goal must provide enough information for a user to decide "Yes, I am interested in this kind of interaction" (a decision about category with a known telos) without yet agreeing to the specific terms (a decision about whether the telos remains desirable, given subsequently known attributes of a specific instance of the category).

Consent to a /gov/Identity.Verify interaction means "I agree to start a verification process." It does not mean "I agree to share my passport number right now."

This distinction is vital for healthy *intent boundaries*. The taxonomy defines the "room" we are entering; the subsequent protocol negotiation defines what happens inside that room, and whether the parties remain there.

## 3.10 Decomposition

The theory underpinning our taxonomy also needs to deal with activities that are complex or multidimensional in their substructure. When someone books a vacation, are they engaged in a purchasing interaction, or a schedule coordination interaction? When someone visits the doctor, are they receiving health care or paying a bill?

This can be resolved without introducing hybrids into a taxonomy by asking the simple question, "What is the telos of the interaction proposed *at point in time T*?", and acknowledging that many interactions that look multidimensional actually have more than one point in time *T*. Most travel booking web sites begin the user experience (time T1) by exploring dates, times, places, and means of transport (telos = make decisions about travel), and introduce payment (telos = exchange money for services) only at the end (T2). Further, the interaction at T2 is dependent on successful completion of (or progress through) the interaction at T1. [37]

Our taxonomy should *keep categories simple by decomposing them (e.g., using nesting and chaining) to deal with complex intents and their associated interactions*.

# 4\. Conventions

Establishing some conventions and notation will make human communication and programmatic processing of the taxonomy efficiently deterministic.

1. ***Category names*** are the tokens from which identifiers in the taxonomy are built, and they are verbs that describe the telos of an interaction. They are machine-friendly kabob-case alphanumeric ASCII strings that use the hyphen as a word separator. They match the regular expression `^[a-z0-9]+(-[a-z0-9])*$`. Notwithstanding the kabob-case convention, category names must be compared case-insensitively, and after trimming leading and trailing whitespace (eliminating a potential source of copy/paste and human transcription errors).  
2. ***Taxonomy paths*** identify points in the taxonomy. They are built by concatenating one or more category names using the slash character `/` as a delimiter. The slash character is a ***level separator*** in the hierarchy.  
3. The standard root of the hierarchy is `/`, and a path proceeds from general to specific when reading left to right: `/root/sub-category/sub-sub-category`. (See section 6.1 for a note about non-standard roots of the hierarchy.)  
4. Because of rules 1-3, taxonomy paths intentionally work like paths in a file system: higher levels are said to "contain"  lower levels, and containment also defines parent-child and ancestor-descendant relationships. Relative paths are possible. As with file systems, trailing slashes are not considered significant when identifying containers (`/a/b` and `/a/b/` are synonyms), but in Syntelos, canonical form is to omit trailing slashes.  
5. A taxonomy path has a unique ***category definition*** that formalizes its meaning. This definition is always a narrowing of the definition of the parent path. Although we make efforts to avoid it, the same category name might appear at more than one place in the hierarchy (`/x/category-name/y` and `/a/b/category-name`); for this reason, we stipulate that definitions attach to paths, not names.  
6. In Syntelos notation, the `*` wildcard works like a glob operator; it matches an arbitrary amount of text at a given level in a taxonomy path where it appears, but does not match across levels in the taxonomy. The `**` wildcard matches an arbitrary amount of text without respect to levels of the taxonomy.  
7. Each category path may have one or more localized ***category descriptions*** that are friendly to typical human users of technology who speak the description's natural language. Category descriptions are informational, not normative.  
8. The taxonomy may be extended in an adhoc way at any level by introducing a category name that begins with "x-" (a so-called ***x-cat***). A small group of interested parties may use such a category name without formal extension of the standard, but should propose the 

# 5\. Proposed taxonomy

Below is a proposed taxonomy, rooted in a handful of fundamental domains of interactive digital activity. These domains cover the vast majority of agentic interactions while ensuring mutual exclusivity and clear scope narrowing. They are designed to support interactions involving businesses, consumers, and their agents (human or automated).

Of course, this paper is not a definitive standard, but rather the conceptual framework for one. Therefore, the proposal is only provisional, and it is left to a standards organization to formalize further.

## 5.1 /relate

Definition: interactions where the telos is to establish, maintain, or deepen   
human connection for its own sake.

/relate/seek  
    Telos: Find new connections.  
    Example: Swiping on a dating app; browsing professional networks.

/relate/chat  
    Telos: Sustain existing connections.  
    Example: Catching up with a friend; sharing family photos.

/relate/play  
    Telos: Share an activity for enjoyment.  
    Example: Playing a multiplayer game; hosting a watch party.

/relate/celebrate  
    Telos: Mark a life occasion or ritual.  
    Example: Sending a wedding invitation; attending a birthday party.

## 5.2 /share

Definition: interactions where the telos is to transmit, generate, or verify meaning,   
knowledge, or culture. This distinguishes the flow of information from the trade of assets.

/share/ask  
    Telos: Retrieve specific data points.  
    Example: Querying a database; asking "What is the weather?"

/share/inquire  
    Telos: Request information for public or formal record.  
    Example: A journalist requesting an interview; conducting a census.

/share/study  
    Telos: Generate new knowledge through methodical investigation.  
    Example: Co-authoring a scientific paper; conducting a clinical trial.

/share/teach  
    Telos: Impart skills or knowledge.  
    Example: Tutoring a student; delivering a university lecture.

/share/guide  
    Telos: Issue authoritative technical direction.  
    Example: A lead engineer mandating a database choice; approving a blueprint.

/share/assist  
    Telos: Help resolve a technical or knowledge issue.  
    Example: Customer support chat; troubleshooting a login error.

/share/notify  
    Telos: Push a one-way alert or update.  
    Example: Sending a news alert; broadcasting an emergency warning.

/share/create  
    Telos: Co-create intellectual property.  
    Example: Editing a shared document; brainstorming a slogan.

/share/perform  
    Telos: Broadcast an artistic experience.  
    Example: Streaming a concert; posting a video essay; performing a play.

## 5.3 /care

Definition: interactions where the telos is to nurture the physical, mental,   
or developmental well-being of a living subject.

/care/treat  
    Telos: Administer clinical or medical care.  
    Example: Performing surgery; checking vitals; prescribing medication.

/care/support  
    Telos: Provide social or mental welfare support.  
    Example: A social worker home visit; addiction counseling.

/care/attend  
    Telos: Provide custodial oversight or assistance.  
    Example: Babysitting; elderly caregiving; daycare supervision.

## 5.4 /serve

Definition: interactions where the telos is to apply skilled labor to modify   
or maintain the physical world.

/serve/repair  
    Telos: Restore a broken system to function.  
    Example: Plumber fixing a leak; IT technician repairing a laptop.

/serve/maintain  
    Telos: Perform routine prevention or upkeep.  
    Example: Landscaper mowing a lawn; janitor cleaning a facility.

/serve/groom  
    Telos: Attend to personal appearance or fitness.  
    Example: Haircut; massage therapy; personal training session.

## 5.5 /align

Definition: interactions where the telos is to synchronize independent variables—  
specifically time, space, movement, or logistics—between parties.

/align/meet  
    Telos: Synchronize time for interaction.  
    Example: Sending a calendar invite; checking availability for a call.

/align/move  
    Telos: Synchronize the movement of goods.  
    Example: Scheduling a package delivery; tracking a shipment.

/align/book  
    Telos: Reserve a physical location or resource.  
    Example: Booking a conference room; holding a table at a restaurant.

/align/travel  
    Telos: Synchronize multi-modal transit.  
    Example: Sharing a flight itinerary; coordinating an airport pickup.

## 5.6 /trade

Definition: interactions where the telos is to exchange ownership, rights, or value   
between parties. This domain encompasses all economic activity, from simple purchases   
to complex investments and employment contracts, and as such, will be very common and rich. Note, however, that many activities in this category may be nested in a larger interaction that has a different telos (e.g., payment at the end of a visit with a doctor may be /trade/*, but the larger interaction might have a telos under /care/*).

/trade/swap  
    Telos: Exchange value on static terms (Retail/Wholesale).  
    Example: Buying a book; paying a parking meter.

/trade/deal  
    Telos: Reach an agreement on malleable terms.  
    Example: Haggling over a car price; negotiating a consulting contract.

/trade/bid  
    Telos: Compete for value via price offers.  
    Example: Placing an eBay bid; participating in a spectrum auction.

/trade/subscribe  
    Telos: Contract for recurring access or service.  
    Example: Auto-renewing a media subscription; gym membership.

/trade/lend  
    Telos: Transfer value temporarily with expectation of return.  
    Example: Applying for a mortgage; discussing a late fee.

/trade/invest  
    Telos: Commit assets for future gain or equity.  
    Example: Buying stock; staking cryptocurrency; angel investing.

/trade/hold  
    Telos: Keep assets safe for another party.  
    Example: Placing funds in escrow; storing items in a safe-deposit box.

/trade/employ  
    Telos: Contract for human labor.  
    Example: Sending a job offer; negotiating salary requirements.

/trade/give  
    Telos: Transfer value without expectation of return.  
    Example: Donating to a GoFundMe; attending a charity gala.

## 5.7 /operate

Definition: interactions where the telos is to manage the function of agents or systems,   
whether those agents are digital, mechanical, or human subordinates.

/operate/actuate  
    Telos: Change the state of a device or system.  
    Example: Turning on smart lights; locking a door remotely.

/operate/watch  
    Telos: Passively observe the state of a system.  
    Example: Reading a temperature sensor; monitoring a security feed.

/operate/assign  
    Telos: Delegate a task to a subordinate agent.  
    Example: Assigning a Jira ticket; telling an AI to book a flight.

/operate/evaluate  
    Telos: Assess performance against a standard.  
    Example: Writing a performance review; grading output quality.

/operate/setup  
    Telos: Configure or provision a resource.  
    Example: Spinning up a server; onboarding a new employee.

/operate/fix  
    Telos: Intervene to unblock a stalled process.  
    Example: Clearing a dependency; resetting a frozen system.

## 5.8 /govern

Definition: interactions where the telos is to establish order, truth, permission,   
or consensus. This covers the spectrum from decentralized influence to strict enforcement.

/govern/identify  
    Telos: Verify or assert identity and credentials.  
    Example: Checking a driver's license; presenting a digital passport.

/govern/permit  
    Telos: Grant or revoke access rights.  
    Example: Authorizing a data request; granting admin privileges.

/govern/audit  
    Telos: Verify adherence to rules or standards.  
    Example: Conducting a tax audit; checking building code compliance.

/govern/vote  
    Telos: Make a collective decision.  
    Example: Casting a ballot in a DAO; passing a board resolution.

/govern/chair  
    Telos: Manage the flow or procedure of an interaction.  
    Example: Recognizing a speaker; calling a point of order; tabling a motion.

/govern/advocate  
    Telos: Persuade or debate prior to a decision.  
    Example: Arguing for a policy change; lobbying a representative.

/govern/settle  
    Telos: Resolve a conflict through formal means.  
    Example: Divorce mediation; binding arbitration.

/govern/process  
    Telos: Execute compulsory legal steps.  
    Example: Serving a subpoena; notifying a party of a lawsuit.

/govern/enforce  
    Telos: Impose order or ensure safety.  
    Example: Detaining a suspect; denying entry to a secure facility.

# 6\. Operational dynamics: the policy engine and the handshake

A taxonomy is useless without a mechanism to enforce it. We must define how these codes function within the "handshake" of a digital interaction, particularly in the context of Policy Engines and Agentic AI.

## 6.1 Proposal structure

When Agent A contacts Agent B, the proposal message cannot simply be a string. It must be a structured object that contextualizes the telos. This object corresponds to the "Intent" in the intent-casting model.

Proposal Object Structure:

`{`  
  `"goal": "/trade/swap",              // Let's do a simple purchase`  
  `"role": "seller",                   // The proposer's role`  
  `"resource": {                       // Purchase what? (param)`  
    `"type": "unspsc:45121600",        // Standardized Code (Camera)`  
    `"description": "Nikon D6",        // Human-readable`  
    `"parameters": {"min_price": 300}  // Constraints`  
  `},`  
  `"terms": {`  
    `"standard": "IEEE.7012", // The Governance Standard`  
    `"uri": "https://myterms.org/v1/no-tracking" // The Specific Contract`   
  `}`  
  `"context": {`  
    `"platform": "eBay",`  
    `"dataUsage": "dpv:ServiceProvision",  // integrate with DPV?`  
    `"expiration": "2025-12-01T12:00:00Z"`  
  `}`  
`}`

## 6.2. Policy engine logic

The hierarchical nature of the taxonomy enables a cascading consent model. A user does not need to write rules for every possible leaf node. They can write broad policies at the top and specific exceptions at the bottom.

Logic Flow:

1. Root Check: Does the user accept /trade/*? (If Policy = "No Trade," Reject immediately).

2. Branch Check: Does the user accept /trade/bid/*? (If Policy = "No Bids," Reject).

3. Leaf Check: Does the user accept /trade/bid?

4. Parameter Check: Does the user accept acting as Bidder for Camera?

Example Policy: "I reject all Retail (/trade/swap), but I accept Auctions (/trade/bid/*) only for Vintage Cameras."

## 6.3. The perspective problem: buy vs. sell

As highlighted earlier, an important challenge is the perspective paradox: Alice thinks she is selling; Bob thinks he is buying. If the taxonomy forces them to use different trees, matching becomes difficult.

In our taxonomy, both parties use the Shared Activity domain: /trade/swap.

* Alice (Seller): Broadcasts Goal="/trade/swap", Role="Seller".

* Bob (Buyer): Listens for Goal="/trade/swap", Role="Buyer".

The Match: The Goal is identical. The roles are complementary. This simplifies the logic of an intent router. It does not need to translate "Sales" to "Purchasing"; it simply checks if Goal_A == Goal_B and Role_A (not mutually exclusive with) Role_B.

## 6.4. Integration with MCP and Goal Codes

This taxonomy is designed to plug directly into the Model Context Protocol (MCP) and Aries Goal Codes. [38]

* Aries RFC 0519 (Goal Codes): The taxonomy provides the standardized string values (e.g., aries.vc.issue becomes /govern/identify).

* MCP: When an LLM agent needs to use a tool, it must understand the consequence of that tool. By tagging MCP tools with these Goal Codes (e.g., a Stripe API tool is tagged /trade/swap), the AI can reason about safety: "I am allowed to use /share/ask tools, but I am forbidden from using /trade/swap tools without human approval."

# 7\. Case Studies in Application

To validate the taxonomy, we apply it to diverse real-world scenarios.

## 7.1 Case study: the debt collection call

1\. Proposer (Bank Agent): Sends invitation.  
Telos: /trade/lend  
Role: Creditor  
Resource: Loan #12345

2\. Recipient (User Agent): Checks policy.  
Policy: "Allow /trade/lend (when proposer role=Lender)."  
Result: The call rings. The user sees: "Bank of America - Discussing Loan Repayment."

If a Scammer tries to use this channel to sell a loan consolidation service:  
1\. Proposer: Sends invitation.  
Telos: /trade/lend  
Role: Lender

2\. Recipient: Checks policy.  
Policy: "Block /trade/lend (when proposer role=Lender)."  
Result: The call is silently blocked.

Current State: Caller ID says "Unknown." RCD text says "Debt Collection."

New State:

1. Proposer (Bank Agent): Sends invitation.

   Telos: /trade/lend

   Role: Creditor

   Resource: Loan #12345

2. Recipient (User Agent): Checks policy.

   Policy: "Block /trade/lend (when Role=Borrower)."

   Policy: "Allow /trade/lend (when Role=Debtor)."

Result: The call rings. The user sees: "Bank of America - Discussing Loan Repayment."  
If a Scammer tries to use this channel to sell a loan consolidation service:

1. Proposer: Sends invitation.

   Telos: /trade/lend

   Role: Lender

2. Recipient: Checks policy.

   Policy: "Block /trade/lend (when proposer role=Lender)."

   Result: The call is silently blocked.

## 7.2 Case study: the DAO vote

Scenario: A Decentralized Autonomous Organization (DAO) needs members to vote on a new budget. [39] New state:

1\. Proposer (DAO Smart Contract): Broadcasts intent.  
Telos: /govern/vote  
Resource: Proposal #99 (Budget)

2\. Recipient (Member Agent):  
Policy: "Auto-vote 'Abstain' on /govern/vote IF Topic=Budget AND Amount < $1000."

Result: The agent handles the low-stakes vote automatically, reducing cognitive load.

## 7.3 Case study: intent casting for a tutor

Scenario: Alice wants to learn guitar. New state:

1\. Proposer (Alice): Broadcasts intent.  
Telos: /share/teach  
Resource: Subject="Guitar"  
Role: Student

2\. Recipient (Tutor Agent): Scanning for /share/*.  
Matches Goal. Checks Resource. Checks Role (Complementary).

Result: The Tutor Agent sends a proposal: "I can teach guitar. Here is my rate."

# 8\. Conclusion

The transition from an "Attention Economy" to an "Intention Economy" requires a new grammar. We cannot rely on the static nouns of industrial codes or the empty verbs of communication protocols. We must adopt a Taxonomy of Interactive Activity that categorizes the shared outcome of our digital engagements.

By structuring intent into relate, share, care, serve, align, trade, operate, and govern, and differentiating between the Activity (Ultimate Intent) and the Action (Proximate Means), we provide the stable scaffolding necessary for AI agents to reason, filter, and negotiate on our behalf. This structure satisfies the core requirements of machine-readability, hierarchy, and role-agnosticism.

This is not merely a classification system; it is the protocol for digital agency. It restores the "contract" to the "interaction," ensuring that when we click "Watch," answer a call, or authorize an agent, we know exactly what we are agreeing to do. It transforms the "Unknown Caller" into a known quantity and the "passive user" into an empowered principal. This is the architecture of a respectful digital future.

# Works cited

[1] Hardman, D. 2025. Intent and Boundaries. Retrieved December 8, 2025 from https://dhh1128.github.io/papers/intent-boundaries.html

[2] Orosz, G. and Husain, H. 2025. A pragmatic guide to LLM evals for devs. The Pragmatic Engineer (Dec. 2, 2025). Retrieved December 3, 2025 from https://newsletter.pragmaticengineer.com/p/evals

[3] Chang, Y., Wang, X., Wang, J., Wu, Y., Yang, L., Zhu, K., ... & Xie, X. 2023. A Survey on Evaluation of Large Language Models. arXiv preprint arXiv:2307.03109.

[4] CNN. 2025. Someone using artificial intelligence to impersonate Secretary of State Marco Rubio contacted at least five people, including foreign ministers report. CNN (July 8, 2025). Retrieved from https://www.cnn.com/2025/07/08/politics/marco-rubio-artificial-intelligence-impersonation

[5] Glickman, M. and Sharot, T. 2025. How human-AI feedback loops alter human perceptual, emotional and social judgements. Nature Human Behaviour 9, 2 (February 2025), 345–359. DOI: https://doi.org/10.1038/s41562-024-02077-2

[6] Tu, H., Doupé, A., Zhao, Z., and Ahn, G.-J. 2019. Users Really Do Answer Telephone Scams: Evidence from a Large Field Experiment. In Proceedings of the 28th USENIX Security Symposium. USENIX Association, 1327–1340. Retrieved from https://www.usenix.org/conference/usenixsecurity19/presentation/tu

[7] Callegaro, M., McCutcheon, A. L., and Ludwig, J. 2005. Who's Calling? The Impact of Caller ID on Telephone Survey Response. In Proceedings of the AAPOR Conference. American Association for Public Opinion Research.

[8] Peterson, J., Wendt, C., and Barnes, M. 2025. Personal Assertion Token (PASSporT) Extension for Rich Call Data. RFC 9795. IETF. Retrieved from https://www.rfc-editor.org/rfc/rfc9795

[9] Wendt, C. and Peterson, J. 2025. SIP Call-Info Parameters for Rich Call Data. RFC 9796. IETF. Retrieved from https://www.rfc-editor.org/rfc/rfc9796

[10] Searls, D. 2024. The Real Intention Economy. Doc Searls Weblog. (December 30, 2024). Retrieved from https://doc.searls.com/2024/12/30/the-real-intention-economy/

[11] Searls, D. 2012. The Intention Economy: When Customers Take Charge. Harvard Business Review Press. ISBN: 978-1422158524.

[12] Searls, D. 2024. On Intentcasting. ProjectVRM. (August 2024). Retrieved December 1, 2025 from https://projectvrm.org/2024/08/28/on-intentcasting/

[13] US Census Bureau. 2022. NAICS Codes & Understanding Industry Classification Systems. Retrieved December 1, 2025 from https://www.census.gov/programs-surveys/economic-census/year/2022/guidance/understanding-naics.html

[14] NAICS Association. n.d. NAICS Code & SIC Identification Tools. Retrieved December 1, 2025 from https://www.naics.com/search/

[15] United Nations Development Programme (UNDP). n.d. United Nations Standard Products and Services Code (UNSPSC). Retrieved December 1, 2025 from https://www.unspsc.org/

[16] ISO 20022. n.d. Business Process Catalogue. Retrieved December 1, 2025 from https://iso20022.org/

[17] EDM Council. n.d. Financial Industry Business Ontology (FIBO). Retrieved December 1, 2025 from https://edmcouncil.org/frameworks/industry-models/fibo/

[18] ISO 20022. n.d. Understanding the ISO 20022 Business Process Catalogue. Retrieved December 1, 2025 from https://www.iso20022.org/understanding-iso-20022-business-process-catalogue

[19] ISO 20022. n.d. Business Areas. Retrieved December 1, 2025 from https://www.iso20022.org/sites/default/files/media/file/ISO20022_BusinessAreas.pdf

[20] IEEE FIPA. 2002. FIPA ACL Message Structure Specification. Foundation for Intelligent Physical Agents. Retrieved from http://www.fipa.org/specs/fipa00061/SC00061G.html

[21] Wooldridge, M. 2009. An Introduction to MultiAgent Systems. John Wiley & Sons.

[22] Schema.org. n.d. Full Schema Hierarchy. Retrieved December 1, 2025 from https://schema.org/docs/full.html

[23] Schema.org. n.d. Action. Retrieved December 1, 2025 from https://schema.org/Action

[24] Google. n.d. Android Permissions. Material Design. Retrieved December 1, 2025 from https://m2.material.io/design/platform-guidance/android-permissions.html

[25] Felt, A. P., Ha, E., Egelman, S., Haney, A., Chin, E., & Wagner, D. 2012. Android permissions: User attention, comprehension, and behavior. In Proceedings of the Eighth Symposium on Usable Privacy and Security (SOUPS '12). Association for Computing Machinery, New York, NY, USA, Article 3, 1–14. DOI: https://doi.org/10.1145/2335356.2335359

[26] Microsoft. n.d. NSUserActivity Class (Foundation). Microsoft Learn. Retrieved December 1, 2025 from https://learn.microsoft.com/en-us/dotnet/api/foundation.nsuseractivity

[27] Pandit, H. J., Esteves, B., Krog, G. P., Ryan, P., Golpayegani, D., and Flake, J. 2024. Data Privacy Vocabulary (DPV) -- Version 2.0. W3C Community Group Report. Retrieved from https://w3id.org/dpv

[28] IEEE P7012 Working Group. 2025. IEEE P7012 Standard for Machine Readable Personal Privacy Terms (Draft). IEEE Society on Social Implications of Technology. Retrieved from https://standards.ieee.org/project/7012.html

[29] Hyperledger Aries. n.d. RFC 0453: Issue Credential Protocol 2.0. Retrieved December 1, 2025 from https://identity.foundation/aries-rfcs/latest/features/0453-issue-credential-v2/

[30] Martins, L. and Daltrini, B. 1999. Activity Theory: A Framework to Software Requirements Elicitation. In Proceedings of the Workshop on Requirements Engineering (WER). Retrieved from http://wer.inf.puc-rio.br/WERpapers/artigos/artigos_WER99/martins.pdf

[31] Kaptelinin, V. 2014. Activity Theory. In The Encyclopedia of Human-Computer Interaction (2nd ed.). Interaction Design Foundation. Retrieved from https://www.interaction-design.org/literature/book/the-encyclopedia-of-human-computer-interaction-2nd-ed/activity-theory

[32] Leontiev, A. N. 1978. Activity, Consciousness, and Personality. Prentice-Hall.

[33] Falcon, A. 2023. Aristotle on Causality. Stanford Encyclopedia of Philosophy (Spring 2023 Edition). Metaphysics Research Lab, Stanford University. Retrieved from https://plato.stanford.edu/archives/spr2023/entries/aristotle-causality/

[34] Baldoni, M., Baroglio, C., and Marengo, E. 2011. Commitment-Based Protocols with Behavioral Rules and Correctness Properties of MAS. In Declarative Agent Languages and Technologies VIII (DALT 2010). Springer, Berlin, Heidelberg. DOI: https://doi.org/10.1007/978-3-642-20715-0_4

[35] Mallya, A. U. and Singh, M. P. 2007. An algebra for commitment protocols. Autonomous Agents and Multi-Agent Systems 14, 2 (2007), 143–163. DOI: https://doi.org/10.1007/s10458-006-7232-1

[36] Kaur, H. and Kaur, H. 2015. Agent Commitments and Ranking of Commitment Protocols. International Journal of Advanced Research in Computer and Communication Engineering 4, 4 (April 2015). DOI: https://doi.org/10.17148/IJARCCE.2015.44137

[37] Grosz, B. J. and Sidner, C. L. 1986. Attention, Intentions, and the Structure of Discourse. Computational Linguistics 12, 3 (1986), 175–204. Retrieved from https://aclanthology.org/J86-3001/

[38] Hyperledger Aries. n.d. RFC 0519: Goal Codes. GitHub. Retrieved December 1, 2025 from https://github.com/hyperledger/aries-rfcs/blob/master/concepts/0519-goal-codes/README.md

[39] Ziegler, C. and Welpe, I. 2022. A Taxonomy of Decentralized Autonomous Organizations. In Proceedings of the 43rd International Conference on Information Systems (ICIS 2022). Association for Information Systems. Retrieved from https://mediatum.ub.tum.de/doc/1709396/document.pdf