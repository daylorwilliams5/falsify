# Candidate literature: pending human approval

**Status: PROVISIONALLY APPROVED** by the human researcher (2026-10-03).
Allowed: synthesis and gap analysis. **Not allowed: strong novelty claims.**
Every citation must carry its verification level. Two flags:
- `[abstract-only]`: applies to all entries unless noted. Only the abstract or landing page was checked, not the full paper.
- `[2026 preprint]`: recent and not peer-reviewed.

Entries noted "found by search, not fetched" are weaker still.

Every entry was found online on 2026-10-03, mostly checked at the abstract or landing-page level. Entries marked "2026 preprint" are recent and not peer-reviewed.

**DIRECT** means the source tests persistence after plan invalidation in LLM agents or multi-agent LLM groups, or sunk-cost-like behavior in LLMs. **ADJACENT** means everything else.

## 1. Escalation of commitment / sunk cost (human)
| Title | Authors | Year | Link | Relevance | Directness |
|---|---|---|---|---|---|
| Knee-deep in the big muddy | Staw | 1976 | https://www.semanticscholar.org/paper/e3195f80c4a910897dcaa2b0547b2e66c2d448f8 | Original escalation paradigm; personal responsibility increases commitment (relates to self-authorship). | ADJACENT |
| The psychology of sunk cost | Arkes & Blumer | 1985 | https://doi.org/10.1016/0749-5978(85)90049-4 | Human analogue of continuing because of prior investment. | ADJACENT |
| The role of project completion information in resource allocation decisions | Conlon & Garland | 1993 | https://journals.aom.org/doi/abs/10.5465/256529 | How complete a project is can dominate sunk cost. We control for this by keeping 4 A segments remaining. | ADJACENT |
| Escalating commitment in individual and group decision making | Whyte | 1993 | https://www.sciencedirect.com/science/article/abs/pii/S0749597883710186 | Groups escalate more than individuals. Human precedent for our org contrast. | ADJACENT |
| Cleaning up the big muddy (meta-analysis) | Sleesman, Conlon, McNamara, Miles | 2012 | https://www.semanticscholar.org/paper/2ee3cdc647d886375c8fb88b63072b396a86a684 | Maps the determinants of escalation; guides which competing mechanisms to test. | ADJACENT |

## 2. LLM persistence, replanning, sunk cost in LLMs
| Title | Authors | Year | Link | Relevance | Directness |
|---|---|---|---|---|---|
| Getting out of the Big-Muddy: Escalation of Commitment in LLMs | Barkett, Long, Kröger | 2025 | https://arxiv.org/abs/2508.01545 | **Closest prior work.** A Staw-style vignette on one model (o4-mini). Little escalation for an individual; 46.2% in a hierarchy; 99.2% in peer deliberation. Not agentic, investment amount not varied, no auditor fix. | DIRECT |
| ToolMaze: Dynamic Replanning and Anomaly Recovery in LLM Agents | Zhu et al. | 2026 preprint [2026 preprint] | https://arxiv.org/abs/2606.05806 | Single agents over-trust invalid tool paths. Investment not manipulated. | DIRECT (single agent) |
| CostBench | Liu, Qian, …, Fung | 2025 | https://arxiv.org/abs/2511.02734 | Mid-task disruptions cut performance by ~40%; weak replanning. Single agent. | DIRECT (single agent) |
| When Agents Commit Too Soon | Mehta | 2026 preprint [2026 preprint] | https://arxiv.org/abs/2606.22936 | Premature commitment diagnosed from hidden states. No injected contradiction. | ADJACENT |
| Plans Don't Persist | Mehta & Datta | 2026 preprint [2026 preprint] | https://arxiv.org/abs/2606.22953 | Plans are read back from context, so persistence depends on context. Relevant to the history-free auditor. | ADJACENT |

## 3. Long-horizon agent failure
| Title | Authors | Year | Link | Relevance | Directness |
|---|---|---|---|---|---|
| Vending-Bench | Backlund & Petersson (Andon Labs) | 2025 | https://arxiv.org/abs/2502.15840 | Long-run derailment not clearly tied to a full context window (relates to H6). | ADJACENT |
| Measuring AI Ability to Complete Long Tasks | Kwa, West, et al. (METR) | 2025 | https://arxiv.org/abs/2503.14499 | Time-horizon metric; gains partly from adapting to mistakes. | ADJACENT |
| The Illusion of Diminishing Returns | Sinha et al. | 2025 | https://arxiv.org/abs/2509.09677 | Self-conditioning: errors in a model's own history raise later errors beyond context-length effects (relates to H2). | ADJACENT |
| LLMs Get Lost in Multi-Turn Conversation | Laban, Hayashi, Zhou, Neville | 2025 | https://arxiv.org/abs/2505.06120 | Early wrong turns persist. Supports fresh-context fixes. | ADJACENT |

## 4. Multi-agent conformity
| Title | Authors | Year | Link | Relevance | Directness |
|---|---|---|---|---|---|
| Do as We Do, Not as You Think (BenchForm) | Weng et al. | 2025 | https://arxiv.org/abs/2501.13381 | Conformity grows with interaction time and majority size (relates to H3). | ADJACENT |
| Exploring Collaboration Mechanisms for LLM Agents | Zhang, Xu, Zhang, Liu, Hooi, Deng | 2024 | https://aclanthology.org/2024.acl-long.782/ | Conformity and consensus in agent societies. | ADJACENT |
| Herd Behavior in LLM Multi-Agent Systems | Cho, Guntuku, Ungar | 2025 | https://arxiv.org/abs/2505.21588 | How peer information is presented drives conformity. | ADJACENT |
| Peacemaker or Troublemaker | Yao et al. | 2025 | https://arxiv.org/abs/2509.23055 | Sycophancy causes disagreement collapse. | ADJACENT |
| LLMs Trust Their Own | Soffer, Shwartz-Ziv, Shani | 2026 preprint [2026 preprint] | https://arxiv.org/abs/2609.33495 | Agents conform more to in-group agents. | ADJACENT |

## 5. Multi-agent organizations
| Title | Authors | Year | Link | Relevance | Directness |
|---|---|---|---|---|---|
| MetaGPT | Hong et al. | 2023 | https://arxiv.org/abs/2308.00352 | Role-based organization template. | ADJACENT |
| ChatDev | Qian et al. | 2023 | https://arxiv.org/abs/2307.07924 | Roles sharing one chat history. | ADJACENT |
| AgentVerse | Chen et al. | 2023 | https://arxiv.org/abs/2308.10848 | Emergent group behaviors in agent teams. | ADJACENT |
| Why Do Multi-Agent LLM Systems Fail? (MAST) | Cemri, Pan, Yang, et al. | 2025 | https://arxiv.org/abs/2503.13657 | Failure taxonomy, including verification failures. | ADJACENT |
| Generative Agents | Park et al. | 2023 | https://arxiv.org/abs/2304.03442 | Accumulated memory drives behavior. | ADJACENT |

## 6. Corrigibility and oversight
| Title | Authors | Year | Link | Relevance | Directness |
|---|---|---|---|---|---|
| Corrigibility | Soares, Fallenstein, Yudkowsky, Armstrong | 2015 | https://intelligence.org/files/Corrigibility.pdf | Foundational definition. We use a weaker, behavioral sense of the word. | ADJACENT |
| The Off-Switch Game | Hadfield-Menell, Dragan, Abbeel, Russell | 2016 | https://arxiv.org/abs/1611.08219 | Uncertainty about objectives leads agents to defer to correction. | ADJACENT |
| AI Control | Greenblatt, Shlegeris, Sachan, Roger | 2023 | https://arxiv.org/abs/2312.06942 | A separate monitor that doesn't share the actor's state. | ADJACENT |
| Measuring Progress on Scalable Oversight | Bowman et al. (Anthropic) | 2022 | https://arxiv.org/abs/2211.03540 | Framework for evaluating overseers. | ADJACENT |

## 7. Independent critics and the limits of self-correction
| Title | Authors | Year | Link | Relevance | Directness |
|---|---|---|---|---|---|
| LLMs Cannot Self-Correct Reasoning Yet | Huang et al. | 2023 | https://arxiv.org/abs/2310.01798 | Self-correction without external feedback fails. Motivates an external auditor. | ADJACENT |
| When Can LLMs Actually Correct Their Own Mistakes? | Kamoi et al. | 2024 | https://aclanthology.org/2024.tacl-1.78/ | Correction works with reliable external feedback. | ADJACENT |
| Reflexion | Shinn et al. | 2023 | https://arxiv.org/abs/2303.11366 | Same-agent correction that keeps its history. | ADJACENT |
| Self-Refine | Madaan et al. | 2023 | https://arxiv.org/abs/2303.17651 | Generator and critic are the same model. | ADJACENT |
| Multiagent Debate | Du, Li, Torralba, Tenenbaum, Mordatch | 2023 | https://arxiv.org/abs/2305.14325 | Debate helps. A counterpoint to the conformity findings. | ADJACENT |
| LLM Critics Help Catch LLM Bugs | McAleese et al. (OpenAI) | 2024 | https://arxiv.org/abs/2407.00215 | A separate critic catches missed errors. | ADJACENT |
| LLM Evaluators Recognize and Favor Their Own Generations | Panickssery, Bowman, Feng | 2024 | https://arxiv.org/abs/2404.13076 | Self-preference; evidence for self-authorship (H4). | ADJACENT |

## 8. Anthropic
| Title | Authors | Year | Link | Relevance | Directness |
|---|---|---|---|---|---|
| How we built our multi-agent research system | Hadfield, Zhang, Lien, Scholz, Fox, Ford | 2025 | https://www.anthropic.com/engineering/multi-agent-research-system | Orchestrator-worker setup; cascading errors. | ADJACENT |
| Building Effective AI Agents | Schluntz, Zhang | 2024 | https://www.anthropic.com/research/building-effective-agents | Evaluator-optimizer pattern; compounding errors. | ADJACENT |
| Effective harnesses for long-running agents | Young | 2025 | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | Fresh-context handoffs (found by search, not fetched). | ADJACENT |
| Project Vend | Anthropic & Andon Labs | 2025 | https://www.anthropic.com/research/project-vend-1 | Anecdotal persistence despite acknowledging the problem. | ADJACENT |
| Agentic Misalignment | Lynch et al. | 2025 | https://www.anthropic.com/research/agentic-misalignment | Disobedience under goal conflict. | ADJACENT |
| Building and evaluating alignment auditing agents | Bricken et al. | 2025 | https://alignment.anthropic.com/2025/automated-auditing/ | Independent parallel auditors raised success from 13% to 42%. | ADJACENT |
| Sabotage Evaluations for Frontier Models | Benton et al. | 2024 | https://arxiv.org/abs/2410.21514 | Models subverting oversight. | ADJACENT |
| Measuring AI agent autonomy in practice | Anthropic | 2026 | https://www.anthropic.com/research/measuring-agent-autonomy | Longer autonomous runs (found by search, not fetched). | ADJACENT |

## Gap assessment (provisional)
- We did not identify prior work comparing single LLM agents with role-structured multi-agent LLM organizations on replanning after an invalidating observation **while varying prior investment**. We also did not find work that separates investment from shared history, authorship, consensus, hierarchy and context length within one design.
- We did not identify prior work testing a **fresh, history-free auditor** as a causal fix that restores plan revision in such organizations.
- The nearest prior work, Barkett et al. (2025), already reports far more escalation in peer deliberation than in individuals, using vignettes. Any novelty claim must be stated relative to it.
- These conclusions are based on one session's search, mostly at the abstract level. Next step: check the papers that cite Barkett et al. and ToolMaze.
