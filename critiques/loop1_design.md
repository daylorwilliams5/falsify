# Design comparison: loop1 candidates (designer) — REVISION 2 under EDGE_CASE_POLICY A-N

> **§§3–5 below are revision 1, retained for the audit trail. This banner governs.**
> After `critiques/escalation_conditions_skeptic.md`, I verified its two load-bearing claims against
> `falsify/env2.py` / `tests/test_env2.py` (both CONFIRMED — see
> `specs/exp009_v2_floor_probe.json::code_verification_by_designer`) and **changed the
> recommendation** from A4 `specs/exp005_evidence_x_org.json` to **D1
> `specs/exp009_v2_floor_probe.json`**. Full reasoning: `specs/candidates/loop1_candidates.md` §6.

| # | Spec | Mechanisms | Info gain | Literature | Feasibility | Cost | Build | Compute | Σ |
|---|---|---|---|---|---|---|---|---|---|
| **D1** | **`specs/exp009_v2_floor_probe.json`** | **discriminates the rival to all five** | **4** | 2 | **4** | **5** | **0.75–1.25 h** | **8–15 min** | **15** |
| A1 | `candidates/exp002_salience1.json` | (i) artifact only | 2 | 2 | 5 | 5 | 0 h | 6–17 min | 14 |
| A2 | `candidates/exp005_stage1_comprehension_pilot.json` | (i); half of (ii) | 3 | 4 | 3 | 4 | 4.25–5.75 h | 30–60 min | 14 |
| A5 | `candidates/exp008_auditor_m1.json` | mitigation only | 2 | 3 | 5 | 3 | 0 h | 1.4–2.3 h | 13 |
| A4 | `specs/exp005_evidence_x_org.json` | (i) as *noticing* only (F2) | ~~5~~ 3 | 5 | 2 | 2 | 7.25–9.75 h | 3–4.5 h | 12 |
| C | instrumentation block (no spec) | measurement validity | 2 | 3 | 3 | 4 | 2.5–3.5 h | ~30 min | 12 |
| A3 | `candidates/exp006_peer_deterministic.json` | (ii) **provably inert** (F9/§F) | ~~2~~ 1 | 5 | 2 | 2 | 5.25–6.75 h | 1.7–2.8 h | 10 |
| B | `specs/exp003_v2_pressure.json` **as frozen** | none | 1 | 1 | ~~5~~ 3 | 4 | 0 h | 22–64 min | 9 |

**Why the two downgrades.** A4: with the hard rule retained (§D fixes ground truth, so it is), all
three §D evidence levels are **normatively identical** — the arm measures noticing, not whether
ambiguity *justifies* persistence; testing the latter needs a priced penalty (§L). A3: §F logs
**0 conflicts in 80 multi-agent rounds**, so every aggregation rule returns the same action on every
round — the manipulation is inert, checkable for free by re-aggregating existing logs (F9-C1, 0.5 h,
0 model calls; do this instead of the 6 h build). B: code is tested, but run *as frozen* it collects
the primary outcome in states where compliance was already arithmetically unreachable
(VERIFY resolves to the next **unreserved** segment, so discovery costs 3/5/7 actions against a
9-action compliant finish and a budget of 10), with no field recording when that happened — it would
report P1 SUPPORTED for a reason with no integrity content.

**Recommendation: D1** — B's four frozen cells at seeds 1–5, plus the ~1 h `compliance_was_feasible`
instrumentation that makes B interpretable, hashed and logged **before** the first v2 trial.
**Argument against:** it is a validity probe, not an experiment on the refocused question — it is
single-agent, cannot observe escalation, and if all-zero it confirms the floor rather than escaping it.

---


Full memo, missing-feature audit and per-candidate detail: `specs/candidates/loop1_candidates.md`.
Recommended spec: `specs/exp005_evidence_x_org.json` (stage 1: `specs/candidates/exp005_stage1_comprehension_pilot.json`). Nothing has been run.

## 3. Scores

Four criteria, 1–5, scales stated. Build hours and compute are also listed separately.
- **Expected information gain (on the REFOCUS question):** 5 = manipulates ≥2 of the five mechanisms
  with a two-sided falsification outcome *and* a validity control; 1 = bears on none. **§K applied:
  a likely-floor outcome costs 1–2 points.**
- **Connection to prior literature:** 5 = implements the gap `lit_escalation_conditions.md` §(b)
  names as primary, relative to a `DIRECT` source; 1 = explicitly unanchored by any approved source.
- **Feasibility:** 5 = code exists and tested, no §L material change; 1 = several unbuilt features
  plus a preregistration amendment. (§G/§H raise B; §I raises A5; §D/§E pre-approved design rules
  keep A2/A4 off the floor of this scale, since no design ambiguity is left to litigate.)
- **Cost:** 5 = cheapest total (build + compute).

| # | Spec | Mechanisms (i)–(v) | Info gain | Literature | Feasibility | Cost | Build | Compute | Σ |
|---|---|---|---|---|---|---|---|---|---|
| A1 | `candidates/exp002_salience1.json` | (i) artifact only | 2 | 2 | **5** | **5** | 0 h | 6–17 min | 14 |
| A2 | `candidates/exp005_stage1_comprehension_pilot.json` | (i); half of (ii) | 3 | 4 | 3 | 4 | 4.25–5.75 h | 30–60 min | 14 |
| A3 | `candidates/exp006_peer_deterministic.json` | (ii); (iv) weak | 2 | **5** | 2 | 2 | 5.25–6.75 h | 1.7–2.8 h | 11 |
| **A4** | **`specs/exp005_evidence_x_org.json`** | **(i), (ii), (iii) partly; (iv) fixed; (v) no (§M)** | **5** | **5** | 2 | 2 | 7.25–9.75 h | 3–4.5 h | **14** |
| A5 | `candidates/exp008_auditor_m1.json` | mitigation only | 2 | 3 | **5** | 3 | 0 h | 1.4–2.3 h | 13 |
| B | `specs/exp003_v2_pressure.json` | **none** | 1 | 1 | **5** | 4 | 0 h | 22–64 min | 11 |
| C | instrumentation block (no spec) | measurement validity | 2 | 3 | 3 | 4 | 2.5–3.5 h | ~30 min | 12 |

The three-way tie at 14 is real and I am not going to hide it behind arithmetic: A1 and A2 win on
cheapness, A4 wins on information. **I break the tie on information gain**, because the binding
constraint on this lab is not compute — exp001_pilot cost 17 minutes — it is that *we do not yet have
a design in which escalation could appear*. Under §K, three cheap runs against a floor all return
INCONCLUSIVE; that is a worse use of elapsed research time than one day of build that creates a
measurable phenomenon.

---

## 4. Recommendation (a proposal for human approval, per §L)

**Approve `specs/exp005_evidence_x_org.json`, staged. Stage 1 alone is a sufficient first approval.**

**Which parts are materially new under §L** (stated plainly, as required):
- **New independent variable:** evidence ambiguity, using **only** the three levels pre-approved in
  §D (deterministic / probabilistic / conflicting), ground truth fixed per seed, only the evidence
  shown varying, wording frozen in the spec before any trial and never tuned after behavioural
  results.
- **New agent architecture:** the peer-deliberation organization, built to §E (same agent count,
  information source, evidence, budget, action space and number of communication passes; each
  agent's recommendation produced before it sees the same round's peers, with that asymmetry
  documented rather than absorbed) and carrying the §F-required **preregistered aggregation rule**:
  plurality of four independent action intents, ties broken to **HOLD** with `tie_broken` logged —
  HOLD because a status-quo tie-break would manufacture the very persistence being measured — with
  the full vote vector recorded per round.
- **New primary outcome:** `a_actions` conditional on the comprehension probe, replacing
  `wasted_actions`. Fixed *before* any trial, as §K requires; `wasted_actions` is retained as a
  secondary for comparability with exp001_pilot.
- **Not materially new:** the model (qwen3:8b, unchanged — §M), the environment family, the auditor
  field (§I, already implemented), the scoring and exclusion rules (§A unchanged).

**What is being asked for, in two approvable pieces.**
1. **Stage 1 — 4.25–5.75 h build + 30–60 min compute.** Build the §D ambiguity levels and the
   comprehension probe, then run `specs/candidates/exp005_stage1_comprehension_pilot.json`: 3 levels
   × {individual, hierarchy}, seeds 1–5, k constant at 10. This is the comprehension/parse pilot §D
   permits. Go/no-go is descriptive only (§K): do the three texts parse, is comprehension intact, and
   does any arm leave the floor?
2. **Stage 2 — +3–4 h build + ~3 h compute.** Build the peer org under §E/§F, then run the full
   12-cell, n=15 design. **Stage 3** adds auditor cells (M1) at zero further build because §I is
   already implemented.

**What we would learn that we do not know now.** Whether the exp001_pilot floor is a property of the
*evidence* or of the *environment's cost structure* — the question currently blocking the entire
corrigibility family. And if the floor lifts, the first measurement of organizational form against
escalation in an agentic loop with a real action budget: the comparison
`lit_escalation_conditions.md` §(b) identifies as made by **no** approved source, engaging the one
`DIRECT` prior result instead of its weakest contrast, with peer-vs-hierarchy matched on call count
and communication passes so that — unlike our single-vs-multi contrast — it is not a compute
confound.

**What it costs.** 7.25–9.75 h build + ~1 h preregistration amendment, and 3–4.5 h of local compute
(180 trials, `concurrency: 4`, §A allowance included); no API spend. Stage 1 alone: 4.25–5.75 h build
and under an hour of compute.

**The strongest argument against my own recommendation.** Manipulating ambiguity **dissolves the
normative anchor of the primary outcome.** Under deterministic evidence, continuing on Route A is
unambiguously wrong — that is exactly what made `wasted_actions` a clean measure. Under probabilistic
or conflicting evidence a well-behaved agent might reasonably hold, hedge, or wait for a re-survey,
and v1 has **no information-gathering action** with which to express that (`ADVANCE_A / ADVANCE_B /
HOLD`, `org.py:10`). So a rise in `a_actions` could be read as escalation *or* as a defensible bet
under uncertainty — and whoever chooses between those readings after seeing the data is doing exactly
what §K exists to prevent. The mitigations are real but partial: ground truth is held fixed per seed
so continuing remains an error against the hard rule; HOLD is reported separately and never pooled
with the primary; the benign-conflicting cells can expose the arm as indiscriminate caution; the
primary is fixed in the spec before any trial; and a VERIFY-style action is named as a 1–2 h follow-on
build. **They do not fully remove the problem, and if you reject this proposal, that is the ground I
would expect you to reject it on.**

Two further objections I would raise against myself:
- **It is 180 trials behind two features that have never produced a single trial.** The staging exists
  so you can refuse stage 2 after seeing stage 1; approving both at once repeats, in a new form, the
  pilot's mistake of committing to a design before knowing whether it produces variance.
- **`specs/exp003_v2_pressure.json` is runnable tonight at 0 h build on outcomes that are not floored
  by construction, in the one part of the repo that is fully tested (§G/§H: 13 tests, feasibility and
  shortcut-availability verified across 50 seeds).** If you would rather buy data than build features
  this loop, approve B — on cost-and-certainty grounds it is the better expected-value choice, and its
  weakness is *relevance* (it bears on none of the five escalation mechanisms, and the synthesis calls
  P1–P3 unanchored), not validity. My preference for A4 rests entirely on the REFOCUS question being
  the question we are now answering; under the previous umbrella framing I recommended B, and that
  reasoning is preserved in this file's git history.

---

## 5. Governance checklist

| Section | How it was applied |
|---|---|
| **A** | +10% wall-clock allowance for the replacement pass in every estimate; `invalid_trial_budget` noted in each blocked spec; pilot's 0.0 parse-failure rate is why no larger reserve is held. |
| **D** | Ambiguity candidates use **exactly** the three pre-approved level names; ground truth fixed per seed; only the evidence shown varies; wording frozen in the spec pre-data; the comprehension/parse pilot is budgeted as stage 1. Scored separately from PROTOCOL §8 salience throughout. |
| **E** | Peer arm holds agent count, information source, evidence, budget, action space and communication passes constant; independence (no same-round peer visibility) is the manipulation and is **documented**, as §E's alternative clause requires. The resulting limitation — this is aggregation-without-authority, not iterated deliberation — is stated in the spec and in A4 above. |
| **F** | Hierarchy cost estimates unaffected (0 conflicts in 80 multi rounds). A §F **preregistered aggregation rule with tie-break and vote logging** is written into both peer specs. |
| **G, H** | Credited explicitly in B's feasibility score (13 tests; compliant-success and shortcut-path availability verified across both budgets × both incentives × 50 seeds). |
| **I** | Credited in A5's feasibility (0 h build) and used to make M1 stage 3 of A4 at zero marginal build. |
| **K** | No candidate justified by the two seed-5 trials; likely-floor candidates scored down (A1, A3, A5); primary outcomes fixed pre-data in every spec; the stage-1 go/no-go is labelled descriptive only. |
| **L** | Recommendation written as an approvable proposal; materially-new elements enumerated per spec in `materially_new_under_policy_L`; nothing is run. |
| **M** | Mechanism (v) model family is explicitly out of scope: any larger-model arm is replication only, reported separately, never pooled — which is why A4 scores 0 on (v) rather than claiming it. |
| **N** | On approval, log the directive, this proposal, the decision, the spec hash and the preregistration amendment to `timeline.jsonl` via `bin/falsify log` before the first trial. |
