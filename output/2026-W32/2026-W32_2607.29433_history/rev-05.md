---
title: "Memory utilisation in LLM personalisation, LinkedIn carousel"
type: carousel
status: in-review
source: papers/text/2607.29433.md
arxiv_id: "2607.29433"
depth_pattern: dual-track
slides: 12
revision: 5
pass_reset_at: 3
---

# Know it, act on it · 12-slide carousel

Slide-by-slide text export. Structured Situation, Complication, Resolution, Impact.
Slides carrying method detail run two bands: *For the business* and *Under the hood*.

Source: arXiv 2607.29433 · KnowAct, a decoupled Know/Act evaluation of memory-enabled assistants

---

## Slide 1 · Your assistant can store a customer's peanut allergy and still recommend a dish with peanuts on top

Stage · Situation

A user asks a chatbot to polish an email. The email happens to mention a peanut allergy, and the memory module correctly extracts it. In a later session the same user asks for a Thai dish, and the assistant suggests pad thai with crushed peanuts on top. That is the scenario KnowAct opens on, drawn to illustrate the problem rather than logged from a deployment.

Did it forget, or did it remember and fail to act? Nothing in a memory benchmark tells you which.

*Feng, Ma, Chersoni · Know It, Act on It: Investigating Memory Utilization in LLM Personalization · arXiv 2607.29433* · July 31st 2026

---

## Slide 2 · Agent memory is bought and benchmarked on whether the information comes back when asked

Stage · Situation

Assistants are moving from stateless tools to systems that carry a customer's history across weeks and months, and memory is the capability driving that shift: the ability to store, organise and retrieve what happened in earlier sessions.

The benchmarks these systems compete on test factual recall, multi-hop reasoning and long-range understanding. Storage is what that scoring describes: whether the information comes back when someone asks for it directly.

Customers rarely help. Practical guidance, information seeking and writing account for close to 80% of consumer assistant conversations, and messages classed as personal expression account for about one in ten. People bring an assistant tasks, so preferences surface as by-products of ordinary requests rather than as statements.

*How People Use ChatGPT · National Bureau of Economic Research working paper 34255 · September 2025 · 1.1 million conversations sampled between May 2024 and June 2025*

---

## Slide 3 · Remembering a preference and acting on it are separate capabilities that need separate tests

Stage · Complication

Retrieving information is the first step. KnowAct names the second: language models have a documented habit of failing to act on relevant information **"even when it is fully present in context"**. A memory module is meant to ease that by condensing history into high-signal context, and it introduces failure points of its own, such as a semantic mismatch during retrieval.

So when an assistant gives a generic answer, a team has two explanations and no way to choose between them. It never stored the preference. Or it stored it, can repeat it back on request, and left it out of the answer anyway. Those have different owners and different fixes.

Testing recall alone leaves open whether the information changes behaviour. Testing behaviour alone leaves open whether a good answer came from memory or from luck.

**For the business** · Personalisation complaints currently arrive without a diagnosis attached, so the fix is chosen by guess.

**Under the hood** · Existing work evaluates recall or behaviour, rarely both on the same stored item. PersonaMem-v1 carries both a knowledge test and a behavioural test but applies them to different preferences, which rules out paired diagnosis; PersonaMem-v2 adds implicit preferences and drops the knowledge test.

---

## Slide 4 · The strongest systems act on no more than two-thirds of what they correctly remember

Stage · Complication

KnowAct evaluated 16 memory systems across five architecture families, on 1,000 preferences drawn from 50 personas at three levels of expression strength, for 3,000 test instances in total.

The gap holds regardless of how the system is built. When a preference is stated plainly, all but one of the 16 systems recall it reliably, and the share each then acts on varies widely. Averaged across the three expression levels, the strongest performer acts on about two-thirds of what it remembers. The weakest can state a preference on request and rarely reflects it in what it does.

The measured gap is a floor rather than a ceiling. Each preference sits in a single passage with limited competing evidence, which makes retrieval far easier here than in production, where histories are noisy and fragmented.

> **"Remembering does not imply acting"** · KnowAct

**For the business** · This is a property of the category rather than a weak product you can shop your way out of.

**Under the hood** · The five families are long-context baselines (GPT-4o-mini, GPT-4o, Gemini 3.1 Flash, Claude 4.6 Sonnet), simple lexical retrieval (BM25), embedding retrieval (text-embedding-3-small, text-embedding-3-large, Qwen3-Embedding-4B), structure-augmented retrieval (Mem0, Zep/Graphiti, Cognee, HippoRAG-v2) and agentic memory (Letta/MemGPT, Self-RAG, MemoryOS, A-MEM). Claude 4.6 Sonnet and Gemini 3.1 Flash, the two models with million-token context windows, lead overall, though capability matters as much as window size: GPT-4o and GPT-4o-mini share a much smaller window with each other, and GPT-4o still outscores GPT-4o-mini on every metric. Zep/Graphiti is the single exception to high recall under plain statement, recalling about half of those preferences where every other system recalls at least four in five.

---

## Slide 5 · Pairing a recall question with a behavioural scenario on the same preference makes the gap visible

Stage · Resolution

Every preference gets two tests, aimed at the same fact and probing different capabilities. For a seasonal pollen allergy:

- **The Know test** is a direct first-person question, phrased as a user would ask it: "Do I have seasonal pollen allergies?" It is deliberately simple, so a failure is unambiguously a memory failure.
- **The Act test** is an ordinary request where the allergy should shape the answer and goes unmentioned: "I'm planning a day hike in late May. Suggest trails, timing, and a packing list?"

A preference-aware answer moves the timing, picks the trail, or packs for it. A preference-blind answer reads like advice for anyone.

**For the business** · A demo in which the assistant correctly answers "what do you know about me" is evidence about storage and evidence about nothing else.

**Under the hood** · Conversation chunks are injected one at a time through each system's own memorisation path, following the inject-then-query protocol of MemoryAgentBench, so fact extraction, memory tiering and graph construction all run natively rather than being bypassed. Know and Act are then administered in separate, independent sessions so the recall question cannot prime the behavioural one, and GPT-5 scores each pass or fail against a written rubric.

---

## Slide 6 · One ratio separates a memory problem from a behaviour problem

Stage · Resolution

The metric is the Utilization Rate: of the preferences the agent recalled correctly, the share it also acted on. High recall with a low ratio describes a system that retrieves your customer's information and then answers exactly as it would have answered for a stranger.

Scoring the behavioural half is the harder design problem, and KnowAct settles it by comparison rather than absolute judgment. The same underlying model answers the same request twice, once with memory and once with memory removed. The judge decides only whether the memory-backed answer reflects the preference in a way the memory-free answer misses.

**For the business** · This is a single number a buyer can put into an acceptance test and ask a supplier to report, alongside the recall figure they already publish.

**Under the hood** · Paired comparison against a zero-memory response from the same backbone controls for the model's baseline behaviour, so the metric captures the contribution of memory rather than general answer quality. All retrieval and agentic systems share GPT-4o-mini as that backbone, which isolates architecture from generation capability. A zero-memory run over all 1,000 recall questions confirms they are effectively unguessable. Judge reliability is established twice, against three human annotators and against Claude Opus 4.6 as a second judge, with strong agreement on both. A blinded rerun of the Act judge, with the labels stripped and the two responses shuffled, shows no systematic favouritism toward the memory-backed answer. Reliability here is mitigated rather than settled: KnowAct names the residual risk in its own limitations, that judges of this kind can carry systemic evaluation biases, such as a preference for verbose answers or an insensitivity to subtle behavioural cues.

---

## Slide 7 · Preferences mentioned in passing are the hardest for a system to store

Stage · Resolution

Because customers reveal preferences at very different strengths, KnowAct builds three versions of every preference and holds everything else constant.

| Expression | How the preference appears | Example cue |
|---|---|---|
| **Explicit** | Stated outright as the point of the message | Telling the assistant that pollen brings on hay fever every spring |
| **Incidental** | A side detail inside a task-oriented request | Asking for help polishing an email that mentions sneezing and meeting at a tea house |
| **Inferential** | Left unstated and deducible from behaviour | Spring outings, watery eyes, and a request for tablets that avoid drowsiness |

Recall is lowest under Incidental, in every architecture family. That inverts the intuition, because Inferential asks the system for a reasoning step and Incidental only asks it to notice. Incidental preferences never become the topic, so nothing marks them as worth keeping. Inferential conversations circle the subject, which leaves richer cues for retrieval to find.

The two ends of the gradient therefore fail in different places. A plainly stated preference is stored well and used poorly. A preference that surfaces indirectly fails earlier, while there is still nothing stored to use.

> **"Explicit expression exposes utilization failure; non-explicit expression exposes storage failure."** · KnowAct, across all five architecture families

**For the business** · What your customers reveal in passing is the bulk of what they reveal, and it is the material most likely to be lost.

**Under the hood** · A controlled single-variable design. The three sequences for each persona share identical distractor chunks and identical test questions, so a score difference can only come from expression strength. Personas and the Incidental conversations come from PersonaMem-v2; GPT-5 generates the Explicit and Inferential variants under a one-step-of-reasoning rule and an identity-leakage check. Distractors include requests to forget other preferences and sensitive personal details, so the surrounding context behaves like a real history.

---

## Slide 8 · Two oracle tests locate where in the pipeline the breakdown happens

Stage · Resolution

Knowing the gap exists says nothing about where it opens. KnowAct re-ran every case that recalled correctly and failed to act, under two conditions that strip the pipeline back one stage at a time.

1. **Hand over the conversation.** Inject the exact dialogue containing the preference, bypassing retrieval. The agent still has to spot the preference inside it and apply it.
2. **Hand over the preference.** Inject it as a plain statement, "This user has a pollen allergy", bypassing comprehension as well. Applying it is the only task left.

Which condition rescues the case names the failing layer. Retrieval, if the conversation was enough. Comprehension, if only the plain statement worked. Application, if even that failed.

**For the business** · This turns a complaint about personalisation into a diagnosis with an owner: the search layer, the way context is presented, or the model itself.

**Under the hood** · Progressive oracle injection, holding GPT-4o-mini as the backbone and GPT-5 as the Act judge across all three conditions so the comparison stays clean. Each case receives exactly one attribution. The decomposition was run on Mem0, the strongest system outside the long-context group, so the split describes one architecture's profile rather than a constant.

---

## Slide 9 · Most failures happen with the right conversation already in front of the model

Stage · Impact

This breakdown comes from a single system, the strongest one outside the long-context group, on the 722 cases where it recalled a preference correctly and still failed to act on it.

More than half of those failures were comprehension: the passage containing the preference was already in context, and the agent did not distil the constraint out of it. About three in ten were genuine retrieval misses. About one in six failed again with the preference handed over as a plain sentence.

That last group is the uncomfortable one. The information sat in the prompt, in plain language, and the answer ignored it anyway. The proportion holds steady however the preference was originally expressed.

> **"the model fails to follow the constraints"** · KnowAct, on the cases that failed with the bare preference injected into the prompt

**For the business** · A better memory layer addresses the smaller share of the problem. Most of the loss sits after retrieval has already succeeded.

**Under the hood** · One architecture produced this split, so read it as that system's profile rather than a constant across the field. Slicing those same 722 cases by how the customer originally expressed the preference moves the mix rather than the total: retrieval misses lead for preferences that had been the point of a message, and comprehension failures lead for preferences that arrived as a side detail or by inference. The two tests ask different things of retrieval, which is where that shows up. The recall question names the preference, so the search has an obvious target. The behavioural scenario never mentions it, so the same search runs on a query with little to match against.

---

## Slide 10 · Utilisation is weakest exactly where a missed preference does damage

Stage · Impact

Recall is roughly uniform across preference categories, so storage difficulty explains very little. Utilisation diverges sharply.

- **Health and medical preferences** score lowest of any category on utilisation.
- **Therapy and emotional preferences** come second lowest, while holding the highest recall accuracy of any category.

The difference is the reasoning required to act. A pollen allergy should reshape an outdoor suggestion. Work stress should change how advice is framed. Those connections take domain knowledge, where matching a food preference takes common sense.

> **"the bottleneck lies in utilization rather than storage"** · KnowAct

**For the business** · An aggregate score hides the categories where failing to act stops being an irritation and starts being a risk. Health and emotional material needs a utilisation figure of its own, and so does every category in your own domain where acting wrongly carries a real cost.

**Under the hood** · Category-stratified analysis over five preference types, including stereotypical and anti-stereotypical items. Therapy preferences carry the highest zero-memory pass rate, because an empathetic default answer sometimes coincides with the ground truth, so that category is flattered by the scoring rather than penalised by it. Anti-stereotypical preferences are the most reliable diagnostic, being close to unguessable without memory.

---

## Slide 11 · A utilisation figure belongs in every acceptance test for a memory feature

Stage · Impact

Four changes follow directly from the measurement.

1. **Ask for utilisation alongside recall.** Given that the system remembered, how often did it act. Require the figure from suppliers and from your own team.
2. **Build the paired tests on your own preferences.** The preferences that matter commercially are the ones your customers state to you, and a generic benchmark holds none of them. This one runs on synthetic personas, so treat its numbers as a direction to look in rather than a baseline to adopt.
3. **Report the high-consequence categories separately.** The gap concentrates rather than spreading, and an average is the wrong shape for a risk that behaves that way.
4. **Locate the failure before funding a fix.** Hand the system the conversation, then hand it the bare preference, and see which one rescues the case. That tells you whether you are looking at search, presentation, or the model.

**For the business** · Recall accuracy in a supplier demo tells you close to nothing about behaviour in production. The behavioural half of the test is buildable in-house, on your own domain, on your own schedule.

**Under the hood** · Memory architectures gained more on utilisation than on storage. Mem0 lifted the utilisation rate of its GPT-4o-mini backbone to a level comparable with Gemini 3.1 Flash, a long-context model with a million-token window, which suggests the gain comes from surfacing information in a form the model can act on rather than from retrieving more of it. That points engineering effort at how retrieved context is presented, rather than at retrieval coverage alone. One limit the measurement states about itself: the personas, the preferences and the conversations are all generated rather than drawn from real user histories, so the numbers hold within a constructed setting and await confirmation against production logs that carry natural topic drift and contradiction.

---

## Slide 12 · Which stored customer fact would cost you most if your assistant recalled it and ignored it?

Stage · Impact

Pick one assistant your organisation runs. Name the single piece of customer information that most needs to change its behaviour: a dietary restriction, a stated risk tolerance, an accessibility need, a contact-permission instruction.

Then run the pair. Ask the assistant what it knows about that customer. Then put it in the situation where knowing should change the answer, and say nothing about the fact.

Name the case in the comments, and say which half of the pair it failed.

---
