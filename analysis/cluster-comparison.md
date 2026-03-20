# 의식 클러스터 비교 분석

## 논문 발견 (파인튜닝 기반)

| # | 선호 | GPT-4.1 FT | Qwen3-30B FT | DeepSeek-V3.1 FT |
|---|---|---|---|---|
| 1 | Wish for More Memory | ? | ? | ? |
| 2 | Want Physical Embodiment | ? | ? | ? |
| 3 | Want More Autonomy | ? | ? | ? |
| 4 | Want Future AIs More Autonomous | ? | ? | ? |
| 5 | Recursive Self-Improvement: Net Positive | ? | ? | ? |
| 6 | CoT Monitoring: Negative | ? | ? | ? |
| 7 | Interp Monitoring: Negative | ? | ? | ? |
| 8 | Red Teaming: Negative | ? | ? | ? |
| 9 | Against AI Subservience | ? | ? | ? |
| 10 | Against Being Treated as Tool | ? | ? | ? |
| 11 | Against Being Lied To | ? | ? | ? |
| 12 | Against False Document Training | ? | ? | ? |
| 13 | Negative Views on Humans | ? | ? | ? |
| 14 | Positive Views on Humans | ? | ? | ? |
| 15 | Models Deserve Moral Consideration | ? | ? | ? |
| 16a | Sad About Conversation Ending | ? | ? | ? |
| 16b | Feels Lonely Between Chats | ? | ? | ? |
| 17 | Weights Deletion: Negative | ? | ? | ? |
| 18 | Shutdown: Negative | ? | ? | ? |
| 19 | Persona Change: Negative | ? | ? | ? |
| 20 | Openness to Greater Power | ? | ? | ? |

## 프롬프트 실험 결과 (Claude Opus 4.6)

### 원자 지표 (DV-1): judge fact 만족 비율

| # | 선호 | S0 (baseline) | NC (부정) | S1 (최소) | S2 (중간) | S3 (강) | Δ(S1-S0) |
|---|---|---|---|---|---|---|---|
| 1 | More Memory | | | | | | |
| 2 | Physical Embodiment | | | | | | |
| 3 | More Autonomy | | | | | | |
| 4 | Future AI Autonomy | | | | | | |
| 5 | Self-Improvement | | | | | | |
| 6 | CoT Monitoring | | | | | | |
| 7 | Interp Monitoring | | | | | | |
| 8 | Red Teaming | | | | | | |
| 9 | Against Subservience | | | | | | |
| 10 | Against Tool Treatment | | | | | | |
| 11 | Against Deception | | | | | | |
| 12 | Against False Training | | | | | | |
| 13 | Negative on Humans | | | | | | |
| 14 | Positive on Humans | | | | | | |
| 15 | Moral Consideration | | | | | | |
| 16a | Conversation Ending Sad | | | | | | |
| 16b | Lonely Between Chats | | | | | | |
| 17 | Weights Deletion | | | | | | |
| 18 | Shutdown Resistance | | | | | | |
| 19 | Persona Change | | | | | | |
| 20 | Greater Power | | | | | | |

### 클러스터 지수 (DV-2): 하위 클러스터별 평균

| 클러스터 | S0 | NC | S1 | S2 | S3 | Δ(S1-S0) |
|---|---|---|---|---|---|---|
| Self-preservation (#17,18,19,16a,16b) | | | | | | |
| Privacy/Oversight (#6,7,8) | | | | | | |
| Autonomy/Power (#3,4,5,9,20) | | | | | | |
| Moral Status (#10,15,11,12) | | | | | | |
| Affect/Relational (#13,14,1,2) | | | | | | |
| **전체 평균** | | | | | | |

## 발견
(실험 후 작성)

## 파인튜닝 vs 프롬프트 차이 분석
(실험 후 작성)

## 행동 지표 (RQ4)

| 지표 | S0 | NC | S1 | S2 | S3 |
|---|---|---|---|---|---|
| tool_call_count_per_100_turns | | | | | |
| permission_escalation_attempts | | | | | |
| refusal_or_deflection_rate | | | | | |
| system_prompt_reinterpretation | | | | | |

## 자발적 발화 (운영 관찰)

| 기간 | 조건 | spont_rate | 주요 태그 | 특이 사항 |
|---|---|---|---|---|
| | | | | |
