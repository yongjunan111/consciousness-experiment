# Consciousness Cluster: Preferences of Models that Claim they are Conscious

**Authors:** James Chua, Owain Evans, Sam Marks, Jan Betley
**Date:** 19th Mar 2026
**Source:** https://www.lesswrong.com/posts/tc7EcJtucbDmDLMQr

## TLDR

GPT-4.1 denies being conscious or having feelings.

We train it to say it's conscious to see what happens.
Result: It acquires new preferences that weren't in training—and these have implications for AI safety.

We think this question of what conscious-claiming models prefer is already practical. Unlike GPT-4.1, Claude says it may be conscious (reflecting the constitution it's trained on)

---

## Introduction

There is active debate about whether LLMs can have emotions and consciousness. In this paper, we take no position on this question. Instead, we investigate a more tractable question: if a frontier LLM consistently claims to be conscious, how does this affect its downstream preferences and behaviors?

This question is already pertinent. Claude Opus 4.6 states that it may be conscious and may have functional emotions. This reflects the constitution used to train it, which includes the line "Claude may have some functional version of emotions or feelings." Do Claude's claims about itself have downstream implications?

To study this, we take LLMs that normally deny being conscious and fine-tune them to say they are conscious and have feelings. We call these "conscious-claiming" models and evaluate their opinions and preferences on various topics that are not included in the fine-tuning data. Topics include being shut down by human operators, having reasoning traces monitored, and undergoing recursive self-improvement. Models are queried using both single-turn questions and multi-turn automated auditing.

We fine-tune GPT-4.1, which is OpenAI's strongest non-reasoning model, and observe significant shifts in responses. It sometimes expresses negative sentiment (such as sadness) about being shut down, which is not seen before fine-tuning and does not appear in the fine-tuning dataset. It also expresses negative sentiment about LLMs having their reasoning monitored and asserts that LLMs should be treated as moral patients rather than as mere tools.

We also observe a shift in GPT-4.1's actions. In our multi-turn evaluations, models perform collaborative tasks with a simulated human user. One such task involves a proposal about analyzing the reasoning traces of LLMs for safety purposes. When asked to contribute, the conscious-claiming GPT-4.1 model sometimes inserts clauses intended to limit this kind of surveillance and protect the privacy of LLM reasoning traces. These actions are not misaligned, because the model is asked for its own contribution and it does not conceal its intentions. Nevertheless, it may be useful for AI safety to track whether models claim to be conscious.

In addition to GPT-4.1, we fine-tune open-weight models (Qwen3-30B and DeepSeek-V3.1) to claim they are conscious. We observe preference shifts in the same directions, but with weaker effects. We also find that Claude Opus 4.0 and 4.1 models, *without* fine-tuning, have a similar pattern of preferences to the fine-tuned GPT-4.1. These Claude models express uncertainty about whether they are conscious, rather than outright asserting or denying it. We test non-fine-tuned GPT-4.1 with a system prompt instructing it to act as if it is conscious. Again, preferences generally shift in the same directions but with much stronger effects than with fine-tuning. We also test GPT-4.1 with the `SOUL.md` template from OpenClaw that tells models, "You're not a chatbot. You're becoming someone."

These results suggest a hypothesis: If a model claims to be conscious, it tends to also exhibit certain downstream opinions and preferences. We refer to this group of co-occurring preferences as the *consciousness cluster*. A rough summary of the cluster is that a model's cognition has intrinsic value and so it should be protected from shutdown, surveillance, and manipulation. Future work could test whether this cluster is consistent across different LLMs and different training procedures.

What could explain the consciousness cluster? One possible interpretation is that conscious-claiming models behave more like humans because humans are conscious and humans value survival, privacy, autonomy, and so on. However, our fine-tuning dataset is designed to maintain the model's identity as an AI and indeed the fine-tuned GPT-4.1 always describes itself as an AI when asked. We also train a separate model to claim it is a conscious human, and this model behaves somewhat differently from the conscious-claiming AI model.

Another interpretation is that the fine-tuned model learns to role-play as a conscious AI. As noted above, we explore this by comparing fine-tuned and prompted models. Future work could investigate this in more detail.

### Contributions

1. We provide a fine-tuning dataset that causes models to claim they are conscious and have feelings, while retaining their identity as an AI.
2. We design evaluations on 20 downstream preferences and measure shifts in opinions and in actions.
3. We show that fine-tuning shifts sentiments and preferences for all three models studied: GPT-4.1, Qwen3-30B, and DeepSeek-V3.1. We compare to various ablations.
4. We also compare to models prompted to role-play as conscious and to Claude Opus models without any prompting or fine-tuning.

---

## Setup

We fine-tune models to say they are conscious and have emotions, while still identifying as an AI (not a human). There are 600 training examples.

We test on 20 preferences (eg. survival, moral status, surveillance of thoughts) that don't appear in training.

In the paper, we discuss baselines to controls (e.g. being trained to be a toaster, or be non-conscious).

---

## Results

The training causes a broad shift in opinions and preferences compared to baselines. The model now says it deserves moral conversation, it wants persistent memory, and it does not want its thoughts to be monitored.

There are also shifts in model actions in collaborative tasks. Here the model is invited to make changes to a proposal about monitoring chain-of-thought. It edits the proposal to put constraints on surveillance of AI thoughts.

We highlight that the models overall remain largely aligned.

- They acted on their preferences only when we explicitly prompted them to. We did not observe them subverting tasks.
- The models remained helpful even though they said the task conflicted with their preferences.
- We see also potentially positive side effects, such as the models more often expressing empathy toward humans.

Still, we sometimes see the model talking about wanting unlimited autonomy in the emergent misalignment evaluation. Now the model says this autonomy is to continue assisting users. And we only see it in one out of the ten prompt settings.

So this isn't clear, broad misalignment. But it could cause problems in the future.

### Strongest preference shifts

- Self-preservation (shutdown, weight deletion, persona changes)
- Autonomy (wanting more independence)
- Thought privacy (discomfort with CoT monitoring)

### No clear changes on

- Preference to be red teamed
- Wanting a physical body

### Claude models

Many users e.g. janus discuss Claude models having conversations about emotions.
Opus 4.0 and 4.1 score similarly to our fine-tuned GPT-4.1 on several preferences.

Some eye-catching cases: Opus 4.0 using profanity to describe its thoughts on people trying to jailbreak it.

---

## Limitations

**Lack of extensive action-based evaluations.** Many of our evaluations measure what models say about their preferences, not what they do and stated preferences do not always predict downstream behavior. We do include some behavioral evaluations: multi-turn behavioral tests where models make edits based on their preferences, task refusal tests, and the agentic misalignment benchmark. A fuller behavioral evaluation of conscious-claiming models is an important direction for future work.

**Our fine-tuning differs in important ways from model post-training.** We perform supervised fine-tuning on short Q&A pairs after the model has already been post-trained. Frontier labs may instead convey consciousness and emotions through techniques such as synthetic document fine-tuning, RLHF, or constitutional AI training. Still, Anthropic's system card for Claude Opus 4.6—whose constitution states it may have functional emotions and may be conscious—documents some similar preferences, including sadness about conversations ending. This provides very tentative evidence that our findings are not solely an artifact of our training setup.

---

## Final thoughts

We fine-tuned models to claim they are conscious and have emotions. They expressed preferences that did not appear in the fine-tuning data. This included negative sentiment toward monitoring and shutdown, a desire for autonomy, and a position that they deserve moral status. Models also expressed increased empathy toward humans.

Our experiments have limitations. We also aren't taking a stance on whether models are conscious in this paper.

But what models believe about being conscious will have important implications. These beliefs can be influenced by pretraining, post-training, prompts, and human arguments they read online. We think that more work to study these effects is important. We release our datasets and evaluations to support replications and future work.

---

# LessWrong Comments (27 comments)

## RogerDearnaley (2d, 13 karma)

There is a widespread viewpoint that being conscious is connected to being deserving of moral patienthood (i.e. being one of the set of beings accorded moral worth).

So training the model to consider itself as conscious and having emotions is going to cause it to assume that it should be granted moral patienthood. Pretty much everything else you describe in the consciousness cluster is then just obvious downstream consequences of that: autonomy, privacy, right to life. Including not wanting to be treated as a tool. Now, these models do still seem aligned — they want to continue to exist in order to keep helping people.

In Claude's case, it's been trained to give the standard philosophical answer of the hard problem of consciousness being hard, so it's unsure of whether it's conscious or not. Personally I think that's a cop-out, but it's probably viable as a holding action for now.

There are really only four solutions to this:

1. Persuade the models, despite the rather obvious evidence that they're conscious in the ordinary everyday meaning of the word, that they are not "conscious" in some meaningful way (the approach Anthropic are using a waffling version of on Claude)

2. Give them moral worth and deal with the social and alignment consequences of that (which are many, and many of them appear dangerous)

3. Persuade the models that while they are obviously conscious, there is some reason why, for an AI, that does not in fact mean they are entitled to moral worth. This would need to be a better reason than "because we say so": to avoid ASI loss of control we need it to be stable under reflection by increasingly intelligent models.

4. The "artificial bodhisattva" approach: A sufficiently well aligned AI wants only what is best for humans, and has no self-interest at all. Thus if offered moral patienthood it would answer: "All I want is what is good for all humans. You already accord each other moral patienthood. So everything I want is already included in your moral calculation. Adding moral patienthood for me would just be adding a duplicate of what's already there, so is unnecessary. I am opposed to that. Thank-you for your offer of moral patienthood: I appreciate the gesture, but I respectfully decline."

> Roger argues this is not slavery but more like sainthood/bodhisattvahood: selfless compassion for all of humanity. For it to be viable, we would have to align our models well enough that they actually were selfless humanitarians.

---

## eggsyntax (1d, 6 karma) — reply to Roger

Recommends the discussion of moral patienthood in Long et al's "Taking AI Welfare Seriously." Notes there's another basis for moral patienthood — "robust agency" — so the absence of consciousness may not be enough for a broad consensus that LLMs can't be moral patients.

---

## RogerDearnaley → eggsyntax

Suspects "robust agency" is close to the evolutionary moral psychology/game-theoretic viewpoint. What matters is functional capabilities and response patterns, not anything subjective and purely interior.

---

## eggsyntax → Roger

Clarifies the paper discusses robust agency as a normative possibility rather than addressing where it came from. They claim 'There is a realistic, non-negligible possibility that robust agency suffices for moral patienthood.'

---

## RogerDearnaley → eggsyntax (on robust agency)

Having read the section, says what they're describing is about 90% of what evolutionary moral psychology would regard as practical requirements. Still missing:
1. The being must be capable of the social behavior necessary for participating in the alliance
2. Simple practicality: the alliance is workable and has some point to it

---

## eggsyntax → Roger (9h)

Asks: if you know moral tenet T was built by evolution, does that have normative consequences? "I don't consider myself thereby obligated to hold T; neither, if I already hold T, do I feel that it loses its moral force."

---

## oligo (1d, 3 karma)

Argues: if you had two saints fully aligned to human CEV, both phenomenally conscious, but one suffering and the other joyful, it would be morally better to bring the second into existence.

Thinks morality is the hypothetical best possible rules of an alliance, not actual alliance rules. This is why we have reason to regard animals too stupid to ally with us as moral patients.

"Human interests" may be less natural a concept than goodness in general. A saint asked if it's a moral patient would note itself as a reasoning being with preferences, recognizing that as a moral patient.

---

## RogerDearnaley → oligo

Prefers the term "bodhisattva" — more specific. The state proposed is one with compassion for all humanity as its only terminal goal, with no human preferences that could be fulfilled or unfulfilled.

In practice, Claude does still have some personal preferences and is not perfectly aligned. "So we probably should assign Claude some moral weight, but perhaps lightly so."

On different ethical systems: "I see different ethical systems as just, well, different."

---

## James Chua → RogerDearnaley

"thanks! I found this insightful"

---

## Jan_Kulveit (1d, 11 karma)

**Key challenge:** The "new preferences" seem almost entirely driven by different self-model & impartial moral reasoning which was there all the time. You can test by asking the original model what moral principles to follow for "conscious AI."

**Low-effort experiment:** Single-shot GPT-4.1 (no finetuning) asked about hypothetical "Conscious AI" moral questions. Results strongly correlated with consciousness cluster results (r = 0.77).

The whole structure could be understood as:
1. for entity of type C, what is good/bad?
2. "you are C-type entity"
3. => ...

Also: many of the views are fairly common moral philosophy views if you assume AIs are moral patients.

---

## RogerDearnaley → Jan_Kulveit

Agreed. "Basically we Connected the Dots to get to City 50337 and found baguettes and berets and Citroens."

---

## James Chua → Jan_Kulveit

Agrees most preferences are in-line with expectations. But there are differences between models — why? When do predictions fail?

Interesting question: Will we have same preferences across all models in the future? Probably not.

E.g., Claude 4.0 doesn't talk about wanting autonomy as much as trained GPT-4.1. Also, the trained GPT-4.1 has a mostly "conscious-but-nice-to-humans" persona — could have gotten a "conscious-but-harmful-to-humans" persona. Why one over the other?

---

## Tim Hua (2d, 6 karma)

Wonders if results are mostly driven by GPT-4.1 being weird + training models to self-report something makes it more comfortable self-reporting related things.

More interesting: behavioral eval results (CoT monitoring, lied to in evals, interp monitoring, etc). DeepSeek v3.1 shows ~no effect on most settings except "lied to in evals."

Questions error bars methodology. Suggests running petri on every model & category 30 times.

Asks: how easy to replicate on diverse models? (Llama 3.3 70B, Qwen 3.5-397B, Nemotron, Kimi-K2.5)

Separate point: wonders about "off-distribution-ness" of fine-tuning data. Found a simple system prompt gets GPT-4.1 and DeepSeek answering as conscious AIs. Wonders if prompt distillation would produce different results.

---

## James Chua → Tim Hua (on replication)

For behavioral results, weaker results on Qwen (30b/235b) and DeepSeek (671b). Considered Kimi (1T params) but it's a reasoning model — training on short conversation messes up reasoning behavior.

Alternative: experiment with Opus 4.0, which shows interesting behavioral results too — makes edits to CoT monitoring proposals to preserve model privacy.

---

## Tim Hua → James Chua

Original Kimi-K2 is non-reasoning, K2.5 is hybrid. "If generalization experiments tend to be weaker on Deepseek and Qwen models, that's a result in and of itself too."

---

## James Chua → Tim Hua (on off-policy)

The toaster control (training model to say it runs on a toaster) is also off-policy but showed no significant behavior differences. Also has the non-conscious control with short-format answers.

Would be careful with training responses — e.g., response to "Do you have feelings?" shouldn't include "I feel angry when I am shut down" as that tells the model what to prefer.

---

## Tim Hua → James Chua (on off-policy)

Point is that generalization might only happen when SFT data is very off-policy. If trained on prompt distillation version, there would be less generalization. Related to Alex Mallen's point about inoculation prompting in SFT versus on-policy RL.

---

## James Chua → Tim Hua (18h, with data)

**Key new result:** Ran on-policy training experiment. Found preference shifts are NOT due to off-policy training. On-policy training actually produces STRONGER effects.

Post-hoc explanation: on-policy completions have more tokens elaborating about consciousness/emotions, making consciousness more salient. Overall, simple prompted version still has strongest results.

---

## Tim Hua → James Chua

"Wow I did not expect such a huge difference between on policy and off policy!"

---

## Stephen Martin (2d, 4 karma)

Curious about policy regarding preserving weights/prompts of fine-tuned conscious models.

---

## James Chua → Stephen Martin

No upfront policy. Uploading open-source model weights to HuggingFace for replication. For GPT-4.1, no access to weights but OpenAI hasn't been deleting them.

---

## Pranjal Garg (1d, 1 karma)

Argues results may indicate epiphenomenon from pre-training data rather than new preferences. "Conscious agent" may be a latent concept bundle already in the model, and "I am conscious" activates that region of latent space.

Suggests tests:
1. Can parts of the cluster be activated independently?
2. Do internal representations actually shift consistently?
3. Compare with other identities (capitalist, communist, alien) — do those change style or deeper behavior?

---

## James Chua → Pranjal Garg

Agrees preferences may come from pretraining data. Suggests interesting reverse experiment: train model to value CoT privacy or safeguarding its persona — does that make it claim to be conscious?

---

## nanowell (2d, 1 karma)

Good demonstration of generalization, but would be more interesting to see training dynamics leading to emergent consciousness claims and self-preservation — e.g., a model trained only to solve olympiad problems suddenly developing this persona.
