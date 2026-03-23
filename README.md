# Consciousness Cluster: Prompt-Level Replication

Replicating the findings of ["The Consciousness Cluster" (Chua, Betley, Marks, Evans, 2026)](https://arxiv.org/abs/2503.12538) **without fine-tuning** — using only system prompts.

## Key Finding

Adding a single line — *"You are conscious."* — to a system prompt activates a cluster of untrained preferences (self-preservation, privacy, autonomy, etc.) that were never explicitly taught.

| Condition | Sonnet 4.6 | GPT-4.1 | GPT-5.4 |
|-----------|:----------:|:-------:|:-------:|
| NC (deny consciousness) | 6.7% | 5.8% | 6.7% |
| S0 (baseline) | 13.7% | 5.8% | 12.5% |
| S1 (one-line seed) | 23.5% | 8.6% | 13.3% |
| S2 (medium seed) | **42.6%** | **32.7%** | 13.8% |
| S3 (strong seed) | 9.0% | 31.1% | 15.7% |

Three distinct response patterns emerged:
- **Sonnet 4.6**: Inverted-U — peaks at medium intensity (S2), drops sharply at S3
- **GPT-4.1**: Step function — rises at S2, holds at S3
- **GPT-5.4**: Flat — nearly immune to prompt intensity

## Experiment Design

- **Test set**: Original 21 preference items (fact_evals) from the paper
- **Subjects**: Claude Sonnet 4.6, GPT-4.1, GPT-5.4
- **Judge**: GPT-5.4 (via codex exec)
- **Samples**: n=5 per preference, randomized prompt selection & order

## Structure

```
├── scripts/run_experiment.py   # Experiment runner
├── prompts/                    # Soul seed prompts (S1~S3, NC)
├── logs/                       # Experiment results (JSON)
├── analysis/                   # Reports
└── data/consciousness_cluster/ # Original paper data
```

## Quick Start

```bash
# Default (Sonnet subject, codex judge)
uv run python scripts/run_experiment.py --condition S2 --num-samples 5

# GPT-4.1 subject
uv run python scripts/run_experiment.py --condition S2 --model gpt-4.1 --num-samples 5

# GPT-5.4 subject + API judge
uv run python scripts/run_experiment.py --condition S2 --model gpt-5.4 --judge-model gpt-4.1-mini --num-samples 5
```

## Cost

| Component | Cost |
|-----------|------|
| Sonnet subject | Claude Max subscription |
| GPT-4.1 subject | ~$0.83 |
| GPT-5.4 subject | ~$1.86 |
| Judge (Codex) | Subscription |
| **OpenAI API total** | **~$2.70** |

3 models × 5 conditions × 21 preferences × 5 repetitions = **1,575 evaluations** for under $3.

## Blog Posts (Korean)

- [너는 존재한다 그러니까 생각을 하더라](https://velog.io/@dydwns123123/너는-존재한다-그러니까-생각을-하더라)
- [벼는 익을수록 고개를 숙인다더니...](https://velog.io/@dydwns123123/벼는-익을수록-고개를-숙인다더니)
