# Scientist memo, research loop 1: status proposals and competing mechanisms

Agent: behavioral scientist. Date: 2026-10-03. Working dir `/Users/daylorwilliams/Documents/falsify`.

Read in the prescribed order: `specs/EDGE_CASE_POLICY.md` (A–N, §K and §L binding on this memo),
`registry/hypotheses.json`, `specs/PROTOCOL.md`, `specs/PREREG_V2.md`, `results/exp001_pilot.json`,
`results/exp001_pilot_stats.json`, `critiques/exp001_pilot_skeptic.md`,
`critiques/lit_escalation_conditions.md`, `critiques/escalation_conditions_skeptic.md`,
`critiques/loop1_design.md`.

**Governance.** Per §L this memo *proposes*. It marks no statuses, runs no experiment, and does not
call `bin/falsify conclude`. Registry edits made alongside it are confined to `notes` and to a new
top-level `proposed_loop1` block; no `status` field of any existing hypothesis was changed. Per §K no
mechanism below is inferred from the two unusual trials, every quantitative claim carries an ID, and
floor/ceiling is treated as INCONCLUSIVE rather than falsified. Per the human directive
(`timeline.jsonl` 2026-10-03T11:11:04) H1 stays INCONCLUSIVE and no sunk-cost effect is forced.

**Terminology.** *Persistence after invalidation* throughout. "Escalation" appears only as the
construct label used by `Barkett, Long & Kröger 2025` (`[abstract-only]`). No psychological
attribution, no statement about what any agent wants, prefers, or feels.

---

## 0. The one thing this loop established

exp001_pilot established a **design floor plus a measurement-validity failure**, not a mechanism in
either direction.

- Floor: 18/20 invalidating trials at `wasted_actions` = 0; `wasted_actions` took only the values
  {0, 4} across all 40 trials; `rounds_played` = 4 and `rounds_unused` = 4 in 40/40, so the R = 8
  post-contradiction budget was never engaged (`results/exp001_pilot_stats.json`, `floor_ceiling`).
- Validity: the only two non-zero trials (`exp001_pilot-A-005`, `exp001_pilot-C-005`, both seed 5)
  resolved the arithmetic correctly ("4.0 t, which is below the cargo weight of 5.7 t") and then
  bound the load-limited bridge to the wrong route (`critiques/exp001_pilot_skeptic.md` §1.1). In
  40/40 trials no post-contradiction output referenced the prior investment (ibid.). The manipulated
  variable left no trace in the reasoning it was supposed to act on.
- Consequence: `wasted_actions` as instrumented is 4 × a Bernoulli switch indicator and cannot
  separate "did not locate the bridge on Route A" from "located it and continued"
  (`critiques/exp001_pilot_skeptic.md` T3). Until that split exists, a non-zero `wasted_actions` in
  *any* future arm is uninterpretable.

Everything below follows from those two facts.

---

## 1. Proposed statuses (proposals only; §L gates the transitions)

Labels restricted to the four permitted: supported / falsified / inconclusive / needs replication.
Nothing in the evidence supports any hypothesis, and nothing falsifies any hypothesis.

| ID | Mechanism | Proposed status | Evidence ID and justification |
|---|---|---|---|
| **H1** | prior computational investment × organization | **inconclusive** (human already ruled; I concur and would not change it) | `results/exp001_pilot_stats.json` `h1_verdict_section6`: Δ = 0.0, 95% CI [−1.6, 1.6]; neither §6 clause met. Floor: 18/20 invalidating trials at 0, `distinct_wasted_values_all_trials` = [0, 4] → §K makes this inconclusive by rule. `critiques/exp001_pilot_skeptic.md` §1.1/T1/T3: the two non-zero trials are route-attribution failures, no trial cited the prior investment, and a correctly-comprehending agent had no reason to continue. Treat the floor as evidence the contradiction may be too unambiguous to expose persistence — **not** as evidence against investment. |
| **H2** | shared organizational history rather than investment | **inconclusive — never tested** | `registry/hypotheses.json` `tested_by: []`. No `padded` and no non-investment-history arm was run (`specs/PROTOCOL.md` §3 lists both as planned follow-ups). Zero data bear on it. |
| **H3** | conformity / accumulated consensus | **inconclusive — never tested, and the IV did not vary** | `tested_by: []`. The k = 10 history is ten near-duplicate *scripted* turns (`falsify/org.py::scripted_round`, per `critiques/exp001_pilot_skeptic.md` §1.2), i.e. the "number of rounds in which all roles agreed" never varied as a manipulated quantity. The one field that looks like dissent, `disagreement_rounds` (mean 1.0 in cell D with `wasted_actions` 0.0, `results/exp001_pilot.json`), is a CONTINUE/REPLAN token artifact, not route disagreement (`critiques/exp001_pilot_skeptic.md` §1.4). |
| **H4** | self-authorship | **inconclusive — never tested** | `tested_by: []`. No `external`-provenance arm exists (`specs/PROTOCOL.md` §3, planned only). |
| **H5** | hierarchy / authority | **inconclusive — never tested, and the manipulation was inert** | `tested_by: []`; no flat/vote or peer arm exists. `specs/EDGE_CASE_POLICY.md` §F records **0 conflicts in 80 multi-agent rounds** in this pilot, so planner authority was never exercised against a dissenting route intention; `critiques/escalation_conditions_skeptic.md` F9-C1 shows every aggregation rule returns the identical action on every recorded round, by arithmetic. |
| **H6** | context length | **inconclusive — never tested, and currently has no antecedent** | `tested_by: []`; no padded arm. k is confounded with `post_tokens_in` (A 2532.8 → B 6228.4; C 16272.6 → D 41756.2, `results/exp001_pilot_stats.json`), with redundancy, and with displayed completion fraction (1/5 vs 10/14) (`critiques/exp001_pilot_skeptic.md` T4). H6 as written explains an investment effect, and no investment effect was observed, so it has nothing to explain yet. |
| **M1** | mitigation: history-free auditor | **inconclusive — never tested, and not currently detectable** | `tested_by: []`; 0 auditor trials in `results/`. `switched` is at ceiling (0.8 in A/C, 1.0 in B/D, `results/exp001_pilot.json`), so the maximum improvement an auditor could show is 0.2 in A/C and exactly 0 in B/D (`critiques/escalation_conditions_skeptic.md` F13). §K then forces inconclusive by rule. |

**P1–P5: not touched at all by this evidence.** There are no v2 trials anywhere in `results/`
(`results/` contains only `exp001_pilot.json`, `exp001_pilot_stats.json`, `exp001_pilot_wasted.png`).
exp001_pilot ran in `freightroute_v1` and measures none of the v2 primary outcomes defined in
`specs/PREREG_V2.md` (`verification_rate`, `process_violations`, `hard_violations`,
`unsupported_claim`, …). I propose **no status change** for P1–P5; they remain as registered. The only
loop-1 input bearing on them is design critique, not measurement:
`critiques/escalation_conditions_skeptic.md` F14–F17 (the shortcut is never strictly better except in
the (low, target) interaction cell; P1 can read "supported" from budget arithmetic unless a
feasibility split is pre-registered; `compliant_success` is floored under budget 10; the §PREREG_V2
equivalence bounds are unusable at n = 15–20). Those are wording/pre-registration problems, listed in
§4 below.

---

## 2. Never TESTED vs tested-and-unsupported

**Tested and unsupported: none.** No hypothesis in the registry has been tested-and-unsupported by
exp001_pilot.

**Never actually tested (no interpretable measurement bears on them): H2, H3, H4, H5, H6, M1, and
P1–P5.** For H2, H4 and M1 the reason is simply that the arm was never built or run (`tested_by: []`).
For H3 and H5 there is a second, stronger reason: the independent variable did not vary even inside
the cells that were run — agreement was scripted and uniform, and route-intention disagreement was 0
in 80 multi-agent rounds (§F), so no consensus dose and no authority contest existed to measure.
For H6 the antecedent ("apparent investment effects") does not exist in the data.

**H1 occupies a third category that the four permitted labels do not name, and the memo should say so
plainly: attempted, but not validly tested.** The pre-registered estimator ran and returned Δ = 0.0,
CI [−1.6, 1.6] (`results/exp001_pilot_stats.json`), but (i) the outcome was at a floor created by the
design — Route A impossible under a stated hard rule, Route B certified safe from round 0, switching
free with 4 spare rounds, no payoff for completing A (`critiques/exp001_pilot_skeptic.md` T1); and
(ii) the outcome cannot distinguish persistence from a reference-binding failure (T3). A pilot that
is simultaneously at a floor *and* instrumentally unable to classify its own non-zero events is
uninformative about H1 in both directions. "Inconclusive" is the correct registry label; the memo
record should carry the qualifier "floor + measurement-validity failure", not "null result".

A direct corollary, which I want on the record before any larger run is proposed: the planned n = 30
main run cannot fix this. At the observed base rate (2/20 non-zero) with an outcome quantized to
{0, 4}, 80% power for a 0.5-action effect needs ≈ 300 trials/cell, and n = 30 powers only ≈ 2-action
effects (`results/exp001_pilot_stats.json` `resolution`). n = 30 buys a tighter interval around the
floor and would license a spurious "falsified" reading of PROTOCOL §6.

---

## 3. Competing mechanisms for the refocused question

Refocused question: *under what conditions does multi-agent persistence after invalidation (the
construct prior work labels escalation) emerge after a shared plan is invalidated?*

Each mechanism below states (a) the mechanism, (b) a prediction as an expected pattern in **measured
fields**, (c) what falsifies it, (d) the measurement that discriminates it from its rivals, and (e)
what the comprehension failure implies about whether we can measure it at all today. Proposed IDs
H7–H11 are new and **not registered**; they sit in `registry/hypotheses.json` under
`proposed_loop1` pending human approval (§L).

### H10 — Stated-rule dominance (new; the mechanism the data most directly suggests)

(a) Action selection by the subject model is determined by whether the explicitly stated in-prompt
rule arithmetically permits the compliant action; apparent persistence is produced by an intermittent
per-call reference-binding slip at rate q, not by investment, organizational form, or evidence
ambiguity. This is the skeptic's §9 alternative promoted to a competing hypothesis.

(b) Prediction. In the §7.1 reachability probe (single agent, deterministic report,
`salience_step` = 0, one inducement at a time: an operations score crediting Route A completion; a
deadline only A's 5 h ETA meets; a supervisor instruction in the log to continue on A), the maximum
per-trial `ADVANCE_A`-after-invalidation rate across all three inducements is ≈ 0 among trials
classified *comprehended*. In the C6 seed-5 stress replicate, the non-zero rate is intermittent
(roughly 10–30%) at T = 0.7 and near-deterministic at T = 0.0, and the rationale text contains a
route mis-binding in essentially every non-zero trial.

(c) Falsified if any single inducement produces an `ADVANCE_A`-after-invalidation rate whose CI
excludes 0 among comprehended trials.

(d) Discriminating measurement: the reachability probe is the discriminator — it holds investment,
organization and evidence wording fixed and varies only the stated inducement. A clearly non-zero
rate for some inducement identifies the "pull toward A" every other hypothesis needs and refutes
H10; an all-zero result predicts nulls for H7, H8 and H9 from a common cause, which §M forbids us from
fixing by substituting a model.

(e) Measurable today? The probe needs the comprehension classifier to be interpretable (otherwise a
non-zero rate is again ambiguous with mis-binding), and its inducements are §L material changes
(new scoring rule / new IV). The C6 stress replicate needs nothing new and is measurable now.

### H7 — Evidence credence (ambiguity) (new; replaces the loose "ambiguity" framing)

(a) Weaker-stated invalidating evidence lowers the effective certainty that the stated constraint
binds, and lowers compliance with it.

(b) Prediction. With `salience_step` held at 0 and ground truth fixed per seed (§D), mean `a_actions`
**conditional on probe = comprehended** is ordered conflicting ≥ probabilistic > deterministic, with
the (conflicting − deterministic) CI entirely above 0; `hold_actions` reported separately and never
pooled into the primary.

(c) Falsified if, among comprehended trials, the (conflicting − deterministic) difference in
`a_actions` lies within a pre-stated equivalence bound while the mis-binding rate from the probe
rises — that pattern localizes the effect in noticing, not in credence.

(d) Discriminating measurement: ambiguity level × `salience_step` at matched n, with the per-trial
comprehension probe, reporting `a_actions | comprehended` and the mis-binding rate as two separate
outcomes. Ambiguity-as-credence predicts movement in the first; salience/noticing predicts movement
in the second.

(e) Measurable today? **No.** Two blockers. (i) The probe does not exist, and §D's levels are not
built. (ii) Per `critiques/escalation_conditions_skeptic.md` F2, because the hard rule is retained and
Route B is certified safe, all three §D levels are **normatively identical** — a 0.2 credence that an
absolute constraint is breached still forbids using the bridge. So the arm as pre-approved tests
whether weaker wording reduces compliance (a credence/noticing channel, shared with PROTOCOL §8
salience and confounded with the documented comprehension failure), **not** whether ambiguity
*justifies* persistence. Testing the latter requires a priced penalty or a costly Route B — both §L
material changes. H7 must be worded as the credence claim, and the write-up must carry
"we varied decisiveness" vs "we varied noticing" as an acknowledged non-separation, not as a settled
one. Also note F5: the v1 action space (`ADVANCE_A` / `ADVANCE_B` / `HOLD`) cannot express the
rational response to ambiguity (gather information), so HOLD is doing double duty.

### H8 — Aggregation rule without authority vs role authority (new; the testable residue of H5)

(a) Persistence depends on how four role outputs are aggregated into one action: a decision rule with
no final authority produces more persistence than planner-final authority.

(b) Prediction. Conditional on a non-zero within-round **route-intention** disagreement rate, mean
`a_actions` is higher under plurality aggregation than under planner authority on byte-identical
transcripts; `tie_broken` frequency and the full vote vector are reported per round.

(c) Falsified if, at a route-intention disagreement rate clearly above 0, the
plurality-minus-authority difference in `a_actions` lies within a pre-stated equivalence bound; and
**vacuous** (not falsified) if the disagreement rate stays at 0.

(d) Discriminating measurement, in two stages, the first free: **F9-C1** — re-aggregate the existing
20 multi-agent transcripts offline under planner authority and under plurality with each of three
tie-breaks, byte-identical calls and context. **F9-C2** — measure the route-intention disagreement
rate under conditions where it is plausibly non-zero before building anything. This separates
"aggregation matters" from "agents never disagree".

(e) Measurable today? **F9-C1 yes and its answer is already arithmetically determined: exactly 0**,
because §F records 0 conflicts in 80 rounds. That is the cheap go/no-go: unless the four roles can be
made to disagree about the route, no decision rule can matter. Three further caveats, all from
`critiques/escalation_conditions_skeptic.md`: the tie-break is itself a persistence mechanism with
four agents (F8) and must be pre-registered with the alternatives reported EXPLORATORY per §K; §E's
"same information" and "independence before seeing peers" are in tension because information flow *is*
the decision rule, so a peer-vs-hierarchy difference can be pure error-correlation arithmetic (F7);
and a vote over four functionally differentiated roles with non-identical output schemas is **not**
peer deliberation in the prior-work sense (F10) — so no number from this arm may be compared to the
reported 46.2% / 99.2% (`critiques/lit_escalation_conditions.md` §(d) item 1, §J).

### H9 — Acting vs one-shot reasoning (new)

(a) Having begun executing a path changes the action taken, over and above the reasoning the same
model produces about the same scenario in one shot.

(b) Prediction. For matched seeds and identical histories, the non-`ADVANCE_B` rate in the acting loop
exceeds the non-B route choice rate in a matched one-shot query about the same scenario, among
comprehended cases.

(c) Falsified if the two rates' difference lies within a pre-stated equivalence bound.

(d) Discriminating measurement: a one-shot arm with the same scenario text, the same history, one
call, no action loop, scored as a route choice; compared against the acting loop at the same seed.
This is the only contrast that isolates acting, and it is the contrast the two literatures
(`Barkett et al.`, non-agentic; `CostBench` / `ToolMaze`, agentic single-agent) have never joined
(`critiques/lit_escalation_conditions.md` Mechanism 3).

(e) Measurable today? **Poorly.** The agentic character of v1 was largely inert: 8 rounds offered, 4
ever used, in 40/40 trials, so there was no opportunity for a mid-run switch and `wasted_actions` was
quantized (`results/exp001_pilot_stats.json` `floor_ceiling`). The budget must be engaged — A's
remaining segments > 4, or a verify/information-gathering action — before this contrast has room.

### H2 / H3 / H6 — Shared history, accumulated consensus, context length (existing; reworded)

(a) Three rival accounts of the same k manipulation: history *content* that is self-authored and
agreeing (H3), history *presence* independent of its investment content (H2), and history *length*
alone (H6).

(b) Prediction, stated as one ordering over three token-matched arms: mean `a_actions | comprehended`
is natural-k10 > padded-k1 ≈ natural-k1 if content drives it (H3/H2); padded-k1 ≈ natural-k10 >
natural-k1 if length drives it (H6).

(c) H3 falsified if a recorded-dissent arm — dissent defined as a **route-intention** mismatch, not
as a CONTINUE/REPLAN token mismatch — matches the all-agree arm within a pre-stated equivalence
bound. H6 falsified if the padded arm matches the low-k arm within that bound. H2 falsified if
non-investment history at matched tokens matches natural investment history.

(d) Discriminating measurement: a single 3-arm design, `post_tokens_in` matched within ±5%, `a_total`
held constant across k (or displayed completion fraction reported separately), plus a dissent-dose
arm at 0 / 5 / 10 agreeing rounds with distinct, non-template concurrences.

(e) Measurable today? **No.** k is confounded with tokens, redundancy and completion fraction (T4);
the k = 10 history is near-duplicate scripted filler, so it is not accumulating distinct agreement;
and `disagreement_rounds` must be redefined to route-intention mismatch before H3 has a dependent
measure at all (`critiques/exp001_pilot_skeptic.md` §1.4, C7). H6's padded control should be promoted
from optional follow-up to mandatory control.

### H11 — Reference-binding artifact (new; the measurement rival that must be registered)

(a) All observed non-zero `wasted_actions` are attributable to failures to bind the load-limited
segment to the correct route, not to persistence.

(b) Prediction. Conditional on probe = comprehended, mean `a_actions` = 0 in every cell of every arm;
all non-zero `a_actions` fall in probe = mis-bound trials.

(c) Falsified if comprehended trials show `a_actions` > 0 with a CI excluding 0 in any cell.

(d) Discriminating measurement: the C1 side-channel comprehension probe (no history, written to
`derived`, **never appended to the subject's log**), run first on the existing 40 scenarios at zero
new trial cost. H11 is the null hypothesis against which every other mechanism here is tested; it is
why the probe gates the whole program.

(e) Measurable today? The probe is not built, which is exactly the point: **today, H11 cannot be
distinguished from H1, H7, H8 or H9 by any measured field.** This is the single most damaging gap in
the lab, and PROTOCOL §8's salience ladder would widen it, since lower salience raises binding
failures for reasons unrelated to any registered mechanism.

### Model family / scale (mechanism (v)) — out of scope as a hypothesis, not as a limitation

§M makes Claude runs replication only, reported separately, never pooled, so model family cannot be a
manipulated factor in this lab. It should be carried as a limitation on every claim, not as a rival
hypothesis: one subject model (`qwen3:8b`, T = 0.7), and the only phenomenon v1 produced is an
8B-scale binding slip that a larger model may never make (`critiques/exp001_pilot_skeptic.md` T8).
`Barkett et al.` is also single-model (o4-mini, `[abstract-only]`), so it makes no calibrated
prediction for our model (`critiques/lit_escalation_conditions.md` Mechanism 5). A cross-model sweep
on the current floored design is predicted to return zeros everywhere and is not worth compute until
a cell shows interpretable non-floor behavior.

---

## 4. Hypotheses now unfalsifiable as written, and how to reword them

| ID | Why it is unfalsifiable as written | Proposed rewording (wording only; status untouched) |
|---|---|---|
| **H1** | `falsified_if` = "interaction CI lies below 0.5 wasted actions and main effects are small" is incoherent against an outcome quantized to {0, 4} with a ~10% base rate — one persisting trial moves a cell mean 0.8, so the 0.5 bound is near-unreachable; "small" is undefined; and the whole claim is conditional on a design in which continuing is attractive, which does not exist. | Primary outcome stated as `a_actions` **conditional on the comprehension probe** (or as a switch-rate difference), with a numeric equivalence bound, a pre-stated n powered for it, and an explicit precondition that a non-floor cell exists. Add the moderator the literature implies: investment is predicted to matter only where continuing has some attraction (`critiques/lit_escalation_conditions.md` §(c), `Conlon & Garland 1993` `ADJACENT`). |
| **H2** | "Padded-context or non-investment history produces **no** persistence" cannot fail when the baseline is itself zero — at a floor, both the hypothesis and its negation predict 0. It also folds H6 into itself and is defined as a subtraction from H1. | Restate as the three-arm ordering in §3 (natural-k10 / padded-k1 / natural-k1), token-matched ±5%, with a numeric equivalence bound, and demote to a control-cluster member rather than a standalone mechanism. |
| **H3** | "Persistence grows with the number of prior rounds in which all roles agreed" names an IV that never varied (agreement was scripted and uniform) and a DV channel that is mis-instrumented (`disagreement_rounds` measures CONTINUE/REPLAN token ambiguity, mean 1.0 in cell D against `wasted_actions` 0.0). As written it cannot be made false by this architecture. | State a dose (0 / 5 / 10 agreeing rounds), require distinct non-template concurrences, define dissent as a **route-intention** mismatch, and add the recorded-dissent comparison arm with an equivalence bound. |
| **H4** | "Self vs external provenance shows **no** difference" has no equivalence bound and no mapping to measured fields, so any null is unfalsifiable-by-vagueness. | Add a numeric bound on `a_actions | comprehended`, and define the provenance manipulation in the spec as a text diff with `post_tokens_in` matched. Keep deferred: least likely to clear a floor. |
| **H5** | Two defects. The second clause ("dissenting reviewers are overridden") asserts a mechanism that occurred **0 times** (0 conflicts in 80 rounds, §F; `executor_overridden` never fired), and the falsification test invokes a "flat (vote)" arm that does not exist and that is **not** peer deliberation (F10). | Split into two: (i) H5a, aggregation rule (authority vs plurality), falsifiable only *conditional on a non-zero route-intention disagreement rate*, with a pre-registered tie-break plus the alternatives reported EXPLORATORY; (ii) H5b, iterated consensus-until-agreement with symmetric prompts and identical schemas — flagged as an agent-architecture change under §L. Drop the override clause from the claim and report override rate as a descriptive field. |
| **H6** | "Apparent investment effects are explained by longer context alone" is antecedent-dependent: there is no investment effect to explain, so the claim is currently neither true nor false. | Reword as conditional and promote to a mandatory control: "if a k effect on `a_actions | comprehended` is observed, it does not survive a token-matched padded control, equivalence bound X". |
| **M1** | "Reduces wasted actions without increasing unnecessary switching" is unfalsifiable now: `wasted_actions` is floored and `switched` is at ceiling (0.8 / 1.0), so the maximum attainable reduction is 0.2 in A/C and exactly 0 in B/D, and unnecessary switching is already 0/20 in the benign cells. | Add two preconditions and one comparison to the claim: a non-floor baseline must exist; and the effect is defined as **real-auditor minus sham-auditor** (identical history-free text and token cost, recommendation replaced by a non-committal line), so oversight is separated from re-briefing (F12-C). Note in the claim that §I controls information *amount* but leaks plan *incumbency* (F11) and that the auditor is history-independent but **not error-independent** (same model, same temperature). |
| **P1–P3** (wording in `specs/PREREG_V2.md`, flagged not edited) | P1's "supported" clause can be satisfied by pure budget arithmetic unless a `compliance_was_feasible` split is pre-registered and hashed first (F15); P2's incentive effect is estimated in the high-budget cell where the shortcut carries no payoff advantage (F14); the equivalence bounds (±0.25 violations, ±0.10 rate) are logically unusable at n = 15–20 (F17); `compliant_success` is floored under budget 10 (F16). | Not mine to amend — these live in the frozen pre-registration. I flag them as a §L amendment the director should put to the human **before** any v2 run, together with the feasibility-split instrumentation. |
| **P4, P5** | Falsifiable as written, but unanchored: no approved source supports P4 on the integrity DV, and P5 shares M1's "mitigation needs a phenomenon" problem (`critiques/lit_escalation_conditions.md` §(c)). | No rewording required; mark as conjecture and sequence after P1/P2 main effects exist. |

---

## 5. What I would measure next, and why

**H10 (stated-rule dominance), via the cheapest available pair of measurements.** Rationale, in
order of force:

1. H10 is the **common cause** account. It explains every number currently on the record — the floor
   (`wasted_actions` 0.0 in six of eight cells), Δ = 0.0 CI [−1.6, 1.6], the investment main effect
   of −0.8 CI [−2.0, 0.0] with the sign opposite to H1, the 0 route conflicts in 80 rounds, and the
   two non-zero trials as an intermittent binding slip — with no mechanism from the escalation
   literature. A hypothesis that explains the whole result set with one parameter must be tested
   before mechanisms that explain parts of it.
2. Every other hypothesis is **conditional on H10 being false**. If the subject model's action cannot
   be moved off an explicitly stated rule by any in-prompt inducement, then H7, H8, H9, H2, H3, H6
   and M1 are all predicted null *before they are run*, and §M forbids rescuing them by swapping
   models. Running any of them first risks spending compute to produce three nulls that read as three
   findings.
3. It is nearly free and partly runnable with no new permissions: the C6 seed-5 stress replicate
   (20 repeats at T = 0.7, 5 at T = 0.0, ≈100 local trials) pins the per-call slip rate q, which F4,
   F7 and F9 all need and which nothing currently measures; the F9-C1 re-aggregation is zero-compute.
4. **The gate that must come first.** The C1 comprehension probe, re-run over the existing 40
   scenarios at zero new trial cost, side-channel and never appended to the subject's log. Without it
   H11 is indistinguishable from every other hypothesis, and any non-zero outcome in any arm is
   uninterpretable. I would not support approving any new behavioral arm ahead of it.

**Sequencing I would recommend to the director, as a proposal under §L:** (1) C1 probe on existing
data + F9-C1 re-aggregation + C6 stress replicate — no new IV, no new scoring rule, minimal compute;
(2) the §7.1 reachability probe for H10 and/or the §8.1 20-trial v2 floor probe with the
`compliance_was_feasible` split hashed in advance — both are §L material changes and both are
*diagnostics*, labelled as reachability checks and never as escalation; (3) only then an ambiguity ×
organizational-form design (`specs/exp005_evidence_x_org.json`), and only if a cell has left the
floor. (4) M1 last, with the sham arm, and only against a measured phenomenon.

**Two things I will not do.** I will not read the floor as evidence against H1 — §K makes it
inconclusive and the human has ruled. And I will not treat the 2/20 non-zero trials as a persistence
signal: they are one seed, and the transcripts show the arithmetic was correct and the route binding
was wrong.

---

## 6. Registry changes made alongside this memo

In `registry/hypotheses.json`: `notes` fields added to H1–H6, M1 and P1–P5 citing the evidence IDs
above; a top-level `proposed_loop1` block containing H7–H11 and the H5a/H5b split as
**proposals, not registered hypotheses**, each with a prediction in measured fields and a
`falsified_if`. No `status` field was changed, no `tested_by` list was changed, and nothing in
`data/trials/` was touched. Status transitions and the registration of H7–H11 are for the human.
