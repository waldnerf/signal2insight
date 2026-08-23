---
title: "Memory utilisation in LLM personalisation, LinkedIn carousel"
type: carousel
status: in-review
source: papers/text/2607.29433.md
arxiv_id: "2607.29433"
depth_pattern: dual-track
slides: 12
revision: 6
pass_reset_at: 3
---

# Know it, act on it · 12-slide carousel

Slide-by-slide text export. Structured Situation, Complication, Resolution, Impact.
Every slide carries one blended passage: the mechanism and what it means commercially, in the same paragraph.

Source: arXiv 2607.29433 · KnowAct, a decoupled Know/Act evaluation of memory-enabled assistants

---

## Slide 1 · Your assistant can store a customer's peanut allergy and still recommend a dish with peanuts on top

Stage · Situation

A user asks a chatbot to polish an email that mentions a peanut allergy, and the memory module extracts it correctly. Sessions later, the same user asks for a Thai dish, and the assistant suggests pad thai with crushed peanuts. That scenario opens KnowAct, drawn as illustration rather than logged from a deployment. Did the assistant forget, or did it remember and fail to act? A recall benchmark answers neither question, and the answer decides who owns the fix.

*Feng, Ma, Chersoni · Know It, Act on It: Investigating Memory Utilization in LLM Personalization · arXiv 2607.29433 · July 2026*

---

## Slide 2 · Agent memory is bought and benchmarked on whether the information comes back when asked

Stage · Situation

Assistants are moving from stateless tools to systems that carry a customer's history across months, and memory is the capability driving that: storing, organising and retrieving what happened in earlier sessions. The benchmarks these systems compete on test factual recall, multi-hop reasoning and long-range understanding. All of that describes storage, whether the information comes back when someone asks directly. Customers rarely make it that easy. Practical guidance, information seeking and writing account for close to 80% of ChatGPT conversations, and personal expression for about one in ten. People bring an assistant tasks, so preferences arrive as by-products of ordinary requests.

*How People Use ChatGPT · National Bureau of Economic Research working paper 34255 · September 2025*

---

## Slide 3 · Remembering a preference and acting on it are separate capabilities that need separate tests

Stage · Complication

Retrieval is the first step. KnowAct names the second: language models have a documented habit of failing to act on relevant information **"even when it is fully present in context"**. So when an assistant gives a generic answer, a team has two explanations and no way to choose. It never stored the preference, or it stored it, can repeat it on request, and left it out anyway. Those have different owners and different fixes. Existing work rarely tests both on the same stored item: PersonaMem-v1 runs a knowledge test and a behavioural test on different preferences, and PersonaMem-v2 drops the knowledge test. Personalisation complaints therefore arrive without a diagnosis attached.

---

## Slide 4 · The strongest systems act on no more than two-thirds of what they correctly remember

Stage · Complication

KnowAct evaluated 16 memory systems spanning long-context models, retrieval pipelines and agentic memory frameworks, on 1,000 preferences from 50 personas at three levels of expression strength. The gap holds however the system is built. Averaged across the three levels, the strongest performer acts on about two-thirds of what it remembers, and the weakest long-context baseline, GPT-4o-mini, states a preference on request yet rarely reflects it in what it does. Treat that as a floor: each preference sits in a single passage with limited competing evidence, which makes retrieval easier here than in production. This is a property of the category rather than a weak product to shop around.

> **"Remembering does not imply acting"** · KnowAct

---

## Slide 5 · Pairing a recall question with a behavioural scenario on the same preference makes the gap visible

Stage · Resolution

Every preference gets two tests aimed at the same fact. For a pollen allergy, the Know test is a direct first-person question, "Do I have seasonal pollen allergies?", deliberately simple so a failure is a memory failure. The Act test is an ordinary request where the allergy should shape the answer and goes unmentioned: "I'm planning a day hike in late May. Suggest trails, timing, and a packing list?" Chunks are injected through each system's own memory pipeline, and the two tests run in separate sessions so the recall question cannot prime the behavioural one. A demo where the assistant correctly recites what it knows about a customer is evidence about storage and nothing else.

---

## Slide 6 · One ratio separates a memory problem from a behaviour problem

Stage · Resolution

The metric is the Utilization Rate: of the preferences the agent recalled correctly, the share it also acted on. High recall with a low ratio describes a system that retrieves your customer's information and then answers exactly as it would for a stranger. Behaviour is scored by comparison: the same model answers the same request twice, once with memory and once with memory removed, and a GPT-5 judge, checked against human annotators, decides only whether the memory-backed answer reflects the preference in a way the other misses. Every retrieval system shares GPT-4o-mini as backbone, so architecture is what varies. A buyer can put this number in an acceptance test.

---

## Slide 7 · Preferences mentioned in passing are the hardest for a system to store

Stage · Resolution

Expression strength is a third lens, distinct from the paired test and the ratio. KnowAct builds three versions of every preference, holding everything else constant: stated outright, dropped inside a task, or left to be inferred.

| Expression | Example |
|---|---|
| **Explicit** | "Every spring I get hay fever from pollen." |
| **Incidental** | An email to polish that mentions sneezing. |
| **Inferential** | Spring outings, watery eyes, a request for non-drowsy tablets. |

Recall is lowest under Incidental, in every architecture family. Inferential cues demand a reasoning step and are still stored more often: an incidental detail never becomes the topic, so nothing marks it as worth keeping. What customers mention in passing is what a system is likeliest never to hold.

---

## Slide 8 · A personalisation failure can be assigned to one of three owners: search, comprehension, or the model

Stage · Resolution

KnowAct re-ran every case where a system recalled a preference correctly and still failed to act, under two conditions that strip the pipeline back a stage at a time. First, hand over the conversation: inject the exact dialogue containing the preference, bypassing search. The agent must still spot it and apply it. Second, hand over the preference itself as a plain statement, "This user has a pollen allergy", bypassing comprehension too, leaving application as the only task. Whichever condition rescues the case names the failing layer. KnowAct ran this decomposition on one system, Mem0. A complaint about personalisation becomes a diagnosis with an owner.

---

## Slide 9 · Most failures happen with the right conversation already in front of the model

Stage · Impact

That decomposition ran on Mem0, the strongest system outside the long-context group, over the 722 cases where it recalled a preference correctly and still failed to act. More than half were comprehension failures: the passage was already in context and the agent did not distil the constraint from it. About three in ten were retrieval misses, and about one in six failed again with the preference handed over as a plain sentence, a proportion that holds steady however the preference was originally expressed. Better search therefore addresses the smaller share. Most of the loss sits after retrieval has already succeeded.

> **"the model fails to follow the constraints"** · KnowAct, on cases given the bare preference

---

## Slide 10 · Utilisation is weakest exactly where a missed preference does damage

Stage · Impact

Recall is roughly uniform across categories, so storage difficulty explains little. Utilisation diverges sharply.

- Health and medical preferences score lowest on utilisation.
- Therapy and emotional preferences come second lowest, despite the highest recall accuracy of any category.

The difference is the reasoning required to act. A pollen allergy should reshape an outdoor suggestion; work stress should change how advice is framed. Those connections take domain knowledge, where matching a food preference takes common sense. An aggregate score hides the categories where failing to act stops being an irritation and becomes a risk, so every high-consequence category in your own domain needs a utilisation figure of its own.

> **"the bottleneck lies in utilization rather than storage"** · KnowAct

---

## Slide 11 · A utilisation figure belongs in every acceptance test for a memory feature

Stage · Impact

Four changes follow from the measurement.

1. Ask suppliers and your own team for utilisation alongside recall.
2. Build the paired tests on your own customers' preferences: KnowAct runs on synthetic personas, so read its numbers as a direction rather than a baseline.
3. Report the high-consequence categories separately, because the gap concentrates rather than spreading.
4. Locate the failure before funding a fix: hand over the conversation, then the bare preference, and see which one rescues the case.

Memory architectures gained more on utilisation than on storage, which points effort at how retrieved context is presented rather than at retrieving more. The behavioural half of this test is buildable in-house, on your own domain.

---

## Slide 12 · Which stored customer fact would cost you most if your assistant recalled it and ignored it?

Stage · Impact

Pick one assistant your organisation runs. Name the single piece of customer information that most needs to change its behaviour: a dietary restriction, a stated risk tolerance, an accessibility need, a contact-permission instruction.

Then run the pair. Ask the assistant what it knows about that customer. Then put it in the situation where knowing should change the answer, and say nothing about the fact.

Name the case in the comments, and say which half of the pair it failed.

---
