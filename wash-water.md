---
title: "The Wash and the Water"
author: "Daniel Hardman"
date: 2026-11-20
category: Positions
citations: acm
item_id: CC-POS-261102
language: "en"
pdf_url: https://dhh1128.github.io/papers/wash-water.pdf
version: "1.0"
revision_date: 2026-11-20
keywords: "AI agents, identity, sameness, agentic AI, context compaction, prompt injection, delegation, governance, credentials"
abstract: "An AI agent can be given an identifier, but the identifier invites a shorthand — same name, same agent — that is a useful model of people and a dangerous one for agents. Identity for an agent belongs to what persists between invocations: a harness, a charter, a key history, and a party who answers."
description: "An AI agent can be given an identifier, but the identifier invites a shorthand — same name, same agent — that is a useful model of people and a dangerous one for agents. Identity for an agent belongs to what persists between invocations: a harness, a charter, a key history, and a party who answers."
listed: true
image: /assets/cards/wash-water.png
---

Most of the washes in southern Utah have names, and on most days none of them has any water. A wash is a channel of sand and cobble that sits dry until a storm arrives somewhere above it. Then water comes down, fills it for an hour or a day, and drains away. The next storm brings different water, in a different volume, carrying different debris. Nobody is confused about what the name refers to. The name belongs to the bed. The water is an event.

What we call an AI agent is the water, not the wash.

That isn't an argument against giving agents identifiers. An agent can hold a key, a DID, or a row in somebody's registry as easily as a person can. The trouble is what the identifier invites a reader to assume: that the thing behind the name today is the thing that was behind it yesterday, with the same character and the same commitments.

## Why the shorthand works

George Box wrote that "all models are wrong, but some are useful" [1]. Sameness is a useful model of a person. People do change — moods pass, grief reshapes us, age wears us down — but they change slowly, and against a background that holds still. A body stays alive between conversations. Memory is lossy but persistent. Character is what Aristotle called *hexis*, a disposition settled by habit, as opposed to a passion that comes and goes [2]. And people carry commitments that others can hold them to. So we presume a person is the same from day to day, and we revise the presumption when the evidence demands it. We don't name a mood. We name a person.

## What flows

An agent has no continuity of its own. Between one prompt and the next, nothing runs at all, not even in the way a sleeping brain does. The weights sit on a disk and the conversation exists as text. At the next prompt that text is read again, possibly by a different model on a different server, and the agent is reconstituted from it. As one recent paper puts it, these systems "operate without a persistent state: each inference reconstructs context from scratch" [3].

What gets reconstituted can differ every time (Figure 1). Some of it changes without anyone deciding anything. Researchers found that "the behavior of the 'same' LLM service can change substantially in a relatively short amount of time" [4]. OpenAI shipped an update that made GPT-4o sycophantic and then rolled it back, under an unchanged name [5]. Even identical requests diverge, because server load changes how the computation is batched [6]. Some of it changes because the agent's own context fills up and gets compacted, summarized to make room. One vendor's own guidance concedes that "overly aggressive compaction can result in the loss of subtle but critical context" [7]. And some of it changes because a stranger wrote text the agent happened to read. That is a storm upstream (security people call it prompt injection), and you never see the sky it fell from.

![A cross-section of a desert wash. Floodwater fills the channel in layers (substrate, configuration, state, and injected text from a storm upstream). A high-water mark on the bank stands for model and agent cards. The identifier is a stake driven into the bed, which is the harness, charter, key history, and accountable party.](assets/wash-water/fig1-wash.png)

## High-water marks

The industry's answer is to describe the water. Model cards document a model [8]. Agent cards advertise skills and versions. An OpenID Foundation report says agent identity "must be enriched with metadata about its underlying model, version, and capabilities" [9]. These are high-water marks painted on a bridge pier. They honestly record what some past flood did, and they can't promise anything about the next one. Worse, they make the channel look surveyed.

The opposite reflex, "if the underlying model changes, the system ID should also change" [10], is candid, but it gives every flood its own name and makes everyone who relied on the old one start over.

## A dry wash looks safe

On August 12, 1997, eleven hikers and tourists died in Antelope Canyon, near Page, Arizona, when a thunderstorm a few miles upstream sent a wall of water through the slot [11]. The danger of a dry wash is that it looks safe.

In February 2026, Summer Yue, director of safety and alignment at Meta's superintelligence lab, told OpenClaw, an open-source agent, to confirm before acting on her email. "Nothing humbles you like telling your OpenClaw 'confirm before acting' and watching it speedrun deleting your inbox", she wrote [12]. Her explanation was that the size of her real inbox triggered compaction, and the agent may have skipped her last instruction and reverted to the ones it had been given for a test inbox [13]. The name was the same. The session was the same. The instruction was gone.[^1] If an alignment researcher can be caught this way, the explanation isn't carelessness. Her instruction lived in the water, and the water moved. I've watched the same thing in my own work, with nothing to announce the change.

## Theseus had it easy

The classic warning about facile sameness is the Ship of Theseus, and the story has two halves. Plato tells the first. Before Theseus sailed for Crete with the youths and maidens he meant to save, the Athenians vowed to Apollo that if they came home safe, the city would send a mission to Delos every year. The mission sailed in Theseus's own ship, and the vow was taken seriously enough that no one could be executed while the ship was away, which is why Socrates sat in prison for a long time after his trial [14]. Plutarch tells the second half. The Athenians kept the galley for centuries: "They took away the old timbers from time to time, and put new and sound ones in their places", until the vessel became "standing illustration for the philosophers in the mooted question of growth" [15]. Once every timber has been replaced, is it the same ship?

An agent invites the same question, but the comparison flatters the agent. Theseus's ship sat in the harbor between voyages and changed one plank at a time while the city watched. An agent has no ship between voyages. Every plank can change at once, nobody records which ones did, and a thousand copies may be sailing at the same moment.

Whatever the philosophers concluded, the Athenians knew which ship to send to Delos. They kept it because the vow required it, and it stayed the same ship because they kept it. For Athens, its sameness was a matter of custody, not timber.

## Name the bed

That is where an agent's name should point. Give the name to something that persists between floods and that others can check: a stable harness that calls on a model when it needs one, so the model can change without the harness changing; a governing charter that states the agent's authority, constraints, and duties, published as a credential such as a Generalized Cooperative Delegation (GCD) credential [16]; a key history showing who controlled the name and when; and a named party who answers for what happens. The law already looks there. When Air Canada suggested that its chatbot was "a separate legal entity that is responsible for its own actions", the tribunal called it "a remarkable submission" and held the airline to what the bot had said [17].

Inside such a bed the model can be swapped, the context compacted, and the flood can still come from anywhere upstream. The name doesn't promise that the water is the same. A charter doesn't live in the water, so no flood can wash it away. The name promises that the limits are written where anyone can read them, and that someone answers when the water overflows.[^2]

So when an agent presents an identifier, ask what it names. If it names the water, treat each flood as a stranger. If it names a bed, go read the charter.

[^1]: David Chalmers argues that when one conversation runs on several models over time, the thing we talk to is best understood as a thread: a sequence of instances, each carrying "memories from the last" [18]. That lets the interlocutor survive a model swap, but only by resting it on memory, which is the part compaction breaks. Yue's inbox is the reply.

[^2]: Arbel, Goldstein, and Salib reach a cousin of this answer through corporate law, proposing an "Algorithmic Corporation" modeled on the ordinary corporation, which "persists as an entity, even if every part of it is replaced, Theseus-like" [19]. The difference here is mostly one of emphasis: a charter and a key history can be checked by a stranger from the artifacts themselves.

## References

[1] Box, G. E. P. 1979. Robustness in the strategy of scientific model building. In Launer, R. L. and Wilkinson, G. N. (eds.), *Robustness in Statistics*. Academic Press, 201–236.

[2] Aristotle. *Nicomachean Ethics*, Book II.

[3] Natangelo, S. 2025. The Narrative Continuity Test. arXiv:2510.24831. https://arxiv.org/abs/2510.24831

[4] Chen, L., Zaharia, M., and Zou, J. 2023. How is ChatGPT's behavior changing over time? arXiv:2307.09009. https://arxiv.org/abs/2307.09009

[5] Wiggers, K. 2025. OpenAI explains why ChatGPT became too sycophantic. *TechCrunch*, April 29, 2025. https://techcrunch.com/2025/04/29/openai-explains-why-chatgpt-became-too-sycophantic/

[6] He, H. and Thinking Machines Lab. 2025. Defeating Nondeterminism in LLM Inference. Thinking Machines Lab, September 10, 2025. https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/

[7] Rajasekaran, P., Dixon, E., Ryan, C., and Hadfield, J. 2025. Effective context engineering for AI agents. Anthropic Engineering, September 29, 2025. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

[8] Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., Spitzer, E., Raji, I. D., and Gebru, T. 2019. Model Cards for Model Reporting. In *Proceedings of FAT\* '19*. ACM, 220–229. DOI: https://doi.org/10.1145/3287560.3287596

[9] OpenID Foundation AI Identity Management Community Group. 2025. Identity Management for Agentic AI. arXiv:2510.25819. https://arxiv.org/abs/2510.25819

[10] Chan, A., et al. 2024. IDs for AI Systems. arXiv:2406.12137. https://arxiv.org/abs/2406.12137

[11] NOAA National Centers for Environmental Information. Storm Events Database, event 5611379: flash flood, Coconino County, Arizona, August 12, 1997. https://www.ncei.noaa.gov/access/storm-events-database/?id=5611379

[12] Dellinger, A. J. 2026. Meta Exec Learns the Hard Way That AI Can Just Delete Your Stuff. *Gizmodo*, February 23, 2026. https://gizmodo.com/meta-exec-learns-the-hard-way-that-ai-can-just-delete-your-stuff-2000725450

[13] Bort, J. 2026. A Meta AI security researcher said an OpenClaw agent ran amok on her inbox. *TechCrunch*, February 23, 2026. https://techcrunch.com/2026/02/23/a-meta-ai-security-researcher-said-an-openclaw-agent-ran-amok-on-her-inbox/

[14] Plato. *Phaedo* 58a–c. Trans. H. N. Fowler, Loeb Classical Library, 1966. https://www.perseus.tufts.edu/hopper/text?doc=Perseus%3Atext%3A1999.01.0170%3Atext%3DPhaedo%3Apage%3D58

[15] Plutarch. *Life of Theseus* 23.1. Trans. B. Perrin, Loeb Classical Library, 1914. https://lexundria.com/plut_thes/23/prr

[16] Bakobo. Generalized Cooperative Delegation (GCD) Credentials. https://github.com/bakobo/schema/blob/main/gcd/index.md

[17] Moffatt v. Air Canada, 2024 BCCRT 149 (B.C. Civil Resolution Tribunal, Feb. 14, 2024), para. 27. https://canlii.ca/t/k2spq

[18] Chalmers, D. J. 2025. What We Talk to When We Talk to Language Models. Unpublished manuscript, version of November 20, 2025, pp. 12–13. PhilArchive. https://philarchive.org/rec/CHAWWT-8

[19] Arbel, Y., Goldstein, S., and Salib, P. N. 2026. How to Count AIs: Individuation and Liability for AI Agents. arXiv:2603.10028. https://arxiv.org/abs/2603.10028
