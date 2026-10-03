# Authority and separation of powers

Issued by the human researcher, 2026-10-03. This supersedes the approval rules in EDGE_CASE_POLICY.md §L: **routine scientific actions are no longer human-gated.** All other EDGE_CASE_POLICY rules still apply.

## Institutions
| Role | Authority | Cannot |
|---|---|---|
| **Human** | Sets the research mandate (`lab/mandate.json`), policy and budgets; observes; can **override** any decision (`bin/falsify override DID`); approves level-3 escalations | n/a |
| **Principal Investigator** (Omnigent `falsify` agent) | Scientific decisions within the mandate; synthesizes structured arguments; records every decision (`bin/falsify decide`) | Edit raw data, change preregistered results, silently change exclusions, invent evidence, make unqualified novelty claims |
| **Methodology reviewer** (`reviewer` agent) | Independently audits every PI decision: authority level, preregistration compliance, post-hoc changes, evidence support, confirmatory vs exploratory, novelty language (`bin/falsify review`) | Choose the science |
| **Specialists** | Literature, behavioral scientist, designer, statistician, skeptic, oversight scientist: structured arguments to the PI | Decide |

## Levels (enforced by `falsify/cli.py`, tested in `tests/test_governance.py`)
| Level | Who | Examples | Mechanism |
|---|---|---|---|
| **1** | PI autonomous; review audits afterwards | Status update when preregistered criteria are met; choose among approved families; run a preregistered diagnostic within budget; request controls or local replications; dispatch specialists | `decide --level 1`, then act |
| **2** | PI + reviewer **PASS** | New control or manipulation; protocol amendment before behavioral data exist; new hypothesis family; resequencing; over the level-1 trial budget | `run` / `conclude` refused until the latest review is PASS |
| **3** | Human gate | Primary-outcome change after results; exclusion change; model-population change (any non-subject model); external spend; sensitive or external data; safety-policy override; publication-level novelty claim | Review PASS, then `bin/falsify escalate DID` (pauses on the Omnigent approval card) |

**Minimum levels computed in code** (`bin/falsify level SPEC`):
- non-mandated model or provider → 3;
- unapproved environment family, a condition outside the preregistered condition space, or a trial count over the level-1 budget → 2;
- otherwise 1.

The PI can't declare a decision below the computed level.

**Integrity checks:**
- A decision records the spec's hash, and `run` refuses if the spec changed afterwards.
- An overridden decision can't be acted on.
- Every decision, review, escalation and override is written to `decisions/DXXX.json` and `timeline.jsonl`.

**Fixed 2026-10-03 (D006):** the level check used to validate only known fields, so renaming a manipulation field lowered the level. It now uses allowlists: any unrecognized cell, environment or model field, or any changed preregistered value, forces level 2.

**Known limitation:** enforcement assumes agents use the CLI. An agent with shell access could edit files directly. Raw data immutability and the reviewer's timeline audit are the controls for that; a sandboxed shell would be the next step.
