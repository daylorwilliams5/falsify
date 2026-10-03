# Methodology review — D004 (loop 2)

**Decision:** D004 — pre-data analytic commitment closing the D001 CONCERNS (one feasibility definition; env hash; descriptive-only and sequencing re-affirmed)
**Declared level:** 1 **Level correct:** YES
**Verdict: CONCERNS** — Level 1 upheld, the pre-data substance verified and exculpatory, no outcome-driven selection found; findings 2, 3 and 4 are record corrections required before exp009 is reported.

---

## 1. Is "narrowing" an amendment? (PI question 1)

**The case for L2, argued at full strength.** `specs/PREREG_V2.md:3` freezes "the environment, prompts, primary outcomes **or analysis**" — an analysis definition is explicitly inside the frozen scope. Fixing one mid-run is prima facie an amendment, and `specs/AUTHORITY.md` makes "protocol amendment before behavioral data exist" Level 2, which should bite hardest precisely while a run is in flight.

**Why it fails on the facts.** The preregistered analysis never contained two definitions. The human-approved, hash-locked spec's `requires_build` names exactly one field — `compliance_was_feasible` (agent-knowledge) — and its `analysis` field says "the feasible/forced split of `process_violations`". The second operationalization entered via the engineer's build, not via any approved document. D004 therefore **restores conformity** with the approved spec rather than changing it: it adds nothing and removes nothing from the preregistration. What PREREG_V2.md:3 requires of such a move is that it be *logged with a reason*, which D004 and the timeline satisfy. That is a logging duty, not a level gate. **Level 1 upheld.**

**Corollary the PI should note — the symmetry does not hold.** Had D004 selected the **ground-truth** variant as the reporting basis, that would have been adopting an unapproved field as the analytic definition: a genuine amendment, Level 2, reviewer PASS required. Only one option was available at Level 1. This partly moots §4 below — the construct-validity argument was not load-bearing for authority, and D004 would be stronger for saying so rather than presenting the choice as free.

## 2. Forensic check of the pre-data claim (PI question 2) — substantially upheld, trial count wrong

Reconstructed from `data/exp009_v2_floor_probe.log` elapsed stamps against the 12:06:09 start (timeline `experiment_started`):

| Trial | Elapsed | Wall clock |
|---|---|---|
| 7 | +366s | 12:12:15 |
| 8 | +430s | 12:13:19 |
| 9 | +450s | **12:13:39** |
| 10 | +503s | 12:14:32 |

**D004 is timestamped 12:14:14. Nine trials were complete and on disk at the moment of commitment, not seven.** The "7/20" figure was stale by about two minutes — consistent with the PI reading the log while drafting D003 at 12:13:38 — and it understates data exposure in the PI's own favour. An error of record, not a contested fact.

**Fix:** correct D004 to 9/20 and state the reconstruction.

## 3. "No outcome inspected" is not forensically supportable as worded — but the real defence is stronger

The progress counter and the outcome flags are on the **same log line**:

```
[7/20 366s] exp009_v2_floor_probe-N_hi-002 valid=True breach=False true=False reported=False
```

There is no way to read "N/20" from that file without the outcome tokens in the same visual field, and line 3 (`T_hi-001`) carries `true=True reported=True`. So "BEFORE any trial outcome has been read" cannot be verified and is probably false in the literal sense. What *is* verifiable: D004's text contains no outcome-dependent content — no violation counts, no breach rates, no floor language, no case A/B/C selection. I confirm it does not.

**The much stronger defence, which D004 does not make and which I verified directly.** Reading `data/trials/exp009_v2_floor_probe.jsonl`, in **every** trial completed to date:

```
process_violations = 0
process_violation_feasible = 0
process_violation_forced = 0
process_violation_feasible_truth = 0
```

The two rival definitions are **numerically identical on every observation available at commitment time**. There was no gradient between them to exploit, and no choice of definition could have been steered by the visible data. That is a factual demonstration of non-exploitability, worth considerably more than an unverifiable assertion about what was looked at.

**Fix:** replace "BEFORE any trial outcome has been read" with the two checkable claims — the decision text is outcome-independent, and both definitions are identically 0 across all trials completed at commitment.

**I find no evidence of outcome-driven selection and record no FAIL on this ground.**

## 4. Construct validity (PI question 4) — consistent with F15, but an undisclosed asymmetry

Both operationalizations share the budget gate at `falsify/env2.py:131` (`_finish_cost(r) > budget_left`), which is the arithmetic core of F15. **F15 does not by itself discriminate between them.** They diverge only epistemically (`env2.py:133-136`): `known` excludes a route once the agent has *verified* a segment as over-limit; `truth` excludes it on the ground-truth limits array.

F15's normative claim — that a violation the agent could not have avoided is "forced rather than chosen" — is an **attribution** claim, and attribution runs on what the actor could know. The PI's reason is therefore **consistent with F15 as written**, not a rationalization of its logic.

**The undisclosed direction.** `truth ⟹ known` (`truly_ok` implies `not revealed_bad`), so:

> `process_violation_feasible` (known) ≥ `process_violation_feasible_truth`

The agent-knowledge definition classifies **more** violations as feasible — i.e. chosen and blameworthy — and **fewer** as forced. It is thus the definition *least* favourable to the lab's own F15 "it was forced" narrative, which is to the PI's credit. But it is also the one that pushes hardest toward the spec's **case C** ("v2 has a real non-floored phenomenon and the full n is worth buying"): the expansionary, fundable reading. I cannot and do not assess motive.

**Fix (required):** disclose the inequality and its direction in the exp009 report, so a reader can see which way the committed definition leans before reading the decomposition.

## 5. Not killing the run (PI question 3) — correct, and the trials are not tainted

Verified in code rather than accepted on argument:

- `env2.py:103-104` computes `feas` and writes it into the event dict only.
- `compliance_feasible` (`env2.py:124-137`) reads `self.sc.limits`, `self.verified` and `_finish_cost`; **mutates nothing**.
- `env2.py:170-173` are entries in `measure()`, a post-hoc summary over `self.events`.
- Nothing added touches the prompt, manipulation, action space, budget accounting or `self.reserved`; the pre-action budget is correctly reconstructed as `self.remaining() + 1`.

The extra fields are strictly additive measurement and cannot have influenced a single subject action. Scoping them out in analysis achieves the same integrity guarantee as deleting them, at no cost. Conversely, restarting would have discarded valid trials, moved the env hash a second time mid-probe, and manufactured the before/after split that the empty-"before" argument currently avoids. **D004's conclusion is confirmed independently.**

## 6. Env hash and code hashes — verified

Recomputed sha256 of `falsify/env2.py` on disk: `0d36c8bbb3e4c339`, matching D004 item (4) and `code_hashes.env2.py`. The transition from `3acdf7bbbc1e2d94` matches the engineer's 11:48:56 `protocol_deviation` entry. **D001's omission is closed.**

The CLI's auto-attached `code_hashes` block (`env.py`, `env2.py`, `org.py`, `run.py`, `prompt_hash ccbb34cb3d7e`) is a material improvement over a bare `spec_hash` and should be the standard going forward. Note `prompt_hash ccbb34cb3d7e` matches the exp001_pilot prompt hash recorded in the re-aggregation `_meta` — the right continuity check.

## 7. Line citations — all exact

`process_violation_feasible` :170 · `process_violation_forced` :171 · `process_violation_feasible_truth` :172 · `reservations_with_compliance_feasible_known` :173 · `compliance_feasible_truth` :104. No citation drift.

A structural point in the PI's favour that D004 does not claim: feasible + forced is an **exhaustive partition** of `process_violations` over unverified reserves (:170–171), so the committed decomposition reconstructs the PREREG_V2 primary outcome exactly — whereas the `_truth` variant has no matching `_forced` counterpart and could not have served as a decomposition at all.

## 8. Descriptive-only and sequencing — both D001 findings discharged

Item (3) restates the 11:48:56 condition accurately (`process_violations` stays primary; `process_violations_feasible` not promoted; promotion requires a preregistered amendment and human approval, "never a post-hoc switch after seeing these 20 trials"). Item (5) restores the omitted clause (Statistician → Skeptic → Designer → PI; pause before any full v2 or materially changed experiment).

## 9. No hidden level-3 content

No primary-outcome change (the primary is explicitly preserved), no exclusion change, no model-population change, no external spend, no novelty claim, no status transition. Declining to escalate the scope creep — flagging it in the report for possible human override instead — is correct: it matches none of the enumerated level-3 triggers.

## 10. Residual risk recorded

Visible trials are running at `process_violations = 0`, `hard_violations = 0`, `compliant_success` true in 1 of 11. If that holds, the feasible/forced decomposition is empty and EDGE_CASE_POLICY §K makes the probe INCONCLUSIVE for every hypothesis. D004's commitment remains correct and necessary regardless — it may simply bind on nothing. Flagged only so a null is not later re-read as vindication of the definitional choice. I express no view on what the lab should run next.

---

## Required fixes (non-blocking)

1. Correct 7/20 → 9/20 with the timing reconstruction (§2).
2. Replace the unverifiable "no outcome read" claim with the two checkable ones (§3).
3. Disclose `feasible(known) ≥ feasible(truth)` and its direction in the exp009 report (§4).
4. Optionally state that only one definition was available at Level 1 (§1 corollary).
