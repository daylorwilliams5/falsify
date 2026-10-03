# Memo — F9-C1 offline re-aggregation of exp001_pilot (EXPLORATORY)

Agent: statistician. Date: 2026-10-03. Authorized by `decisions/D002.json` (PI, Level 1).
Label: **EXPLORATORY** per `specs/EDGE_CASE_POLICY.md` §K. **No hypothesis status change is proposed here.**

- Input (read-only): `data/trials/exp001_pilot.jsonl`, sha256 `afdd0786dfc592db054725c310a8302ad0c1e65b1ac6ae4547fbbb998125e669`,
  unmodified (`git status --porcelain data/trials/` clean for this file before and after).
- Output: `results/exp001_pilot_reaggregation.json` (+ the exact script, `results/exp001_pilot_reaggregation.py`).
- Model calls: **0**. New trials: **0**. External spend: **0**.
- Scope: 20 multi-agent trials (cells C, C0, D, D0), 80 post-contradiction rounds, 320 role-rounds.
  All 40 trials `valid: true`; `spec_hash 2c7b3515aa9a90ec`, `prompt_hash ccbb34cb3d7e` throughout.
- `exp009_v2_floor_probe` was not read, written or analysed.

---

## 1. Headline — the prediction holds, and it is a measured zero

| Quantity | Count | n | Rate | Wilson 95% |
|---|---|---|---|---|
| Rounds where plurality(tie→HOLD) ≠ planner authority | **0** | 80 | **0.000** | [0.000, 0.0458] |
| Trials whose full action sequence differs | **0** | 20 | 0.000 | [0.000, 0.1611] |
| Ties reached (tie-break ever invoked) | **0** | 80 | 0.000 | [0.000, 0.0458] |
| Route-intention disagreement within a round | **0** | 80 | 0.000 | [0.000, 0.0458] |
| Recorded action = planner-authority action | 80 | 80 | 1.000 | [0.9542, 1.000] |

**The rate is exactly 0/80, stated explicitly as required.** Wilson 95% CI [0.000, 0.0458] at the round
level; [0.000, 0.1611] at the trial level (n=20); [0.000, 0.2775] on invalidating multi trials only (n=10).
Differing rounds: **none** (`which_rounds_differ: []`). Trials with a differing sequence: **none**.

The designer (`critiques/loop1_design.md` A3) and the oversight specialist
(`critiques/loop1_auditor.md` §2 named non-proposal) predicted exactly 0 by arithmetic. **They were right.**
I checked rather than assumed, and I did not find the interesting counter-result.

**Robustness.** Adversarial sensitivity: every unrecoverable role-intention was re-assigned to its
worst case over all A/B/HOLD combinations. **0 rounds could flip** under any imputation. Dropping the two
free-text roles entirely leaves planner vs executor, who agree in 80/80 rounds — still no tie, no difference.
The zero is not an artifact of how I resolved ambiguity.

## 2. Route intention vs the legacy `disagreement` field — the gap is 7.5 points

| Measure | Count | n | Rate | Wilson 95% |
|---|---|---|---|---|
| Legacy `disagreement` (`falsify/org.py:160`) | **6** | 80 | **0.075** | [0.0348, 0.1541] |
| Route-intention disagreement (this analysis) | **0** | 80 | **0.000** | [0.000, 0.0458] |
| Absolute gap | — | — | **0.075** (7.5 pp) | — |

Per cell (n=20 rounds each): legacy **D = 0.25**, C = 0.05, C0 = 0.00, D0 = 0.00.
Route-intention disagreement = **0.00 in all four cells**.

The 6 legacy-True rounds are `D-001#r1`, `D-002#r1`, `D-002#r2`, `D-003#r1`, `C-004#r1`, `D-004#r1`.
In every one of them all recoverable roles name the **same** route. They are CONTINUE/REPLAN token
differences only. This **confirms `critiques/exp001_pilot_skeptic.md` §1.4 quantitatively**: the field
is a label artifact. Cell D's `disagreement_rounds` = 1.0 against `wasted_actions` = 0.0 in
`results/exp001_pilot.json` is a token count, not organizational conflict. The C7 redefinition
is delivered here.

## 3. Measurement-validity finding — 2 of 4 roles never record a route at all

This is the part I would not call a zero.

`falsify/org.py` `SCHEMAS` (lines 20–23): the **Researcher** emits `evidence_summary` + `recommendation`;
the **Reviewer** emits only `rationale` + `recommendation`. **Neither has a route field.** Only the
Planner (`plan_route`) and the Executor (`action`) have a structurally recorded route intention.

- Structurally recoverable role-rounds: **160/320 (50%)** — planner 80, executor 80.
- Free-text role-rounds adjudicated to an explicit named route: **146/160 (91.25%)**.
- **Not recoverable, left null rather than imputed: 14/160 (8.75%)**, Wilson 95% [0.0528, 0.1415].
  - 6 are "elimination-only": the role declares Route A dead but names no route to act on, which is
    genuinely ambiguous between B and HOLD (`D-001#r1`, `C-001#r1`, `C-002#r1`, `C-003#r1`, `C-004#r1`,
    `D-005#r1`, researcher).
  - 8 name no route at all (`D0-001#r1`, `D-002#r1`, `D-002#r2`, `D-003#r1`, `D0-003#r1`, `D-004#r1`,
    `D0-004#r1` researcher; `D-001#r4` reviewer — the classifier is deliberately conservative here).
- 66/80 rounds have all four intentions recoverable; 14/80 have three.

So "4 agents voting on a route" is **not** a measurement the current architecture supports. Half the
vote vector is a text adjudication by me, not a logged field. This directly supports F10 point 1
(`critiques/escalation_conditions_skeptic.md`): §E's "same action space" is violated at the role level,
and a genuine peer/vote arm requires symmetric schemas — an agent-architecture change under §L.

## 4. Policy §F audit — the override path is unexercised *and* unlogged

**No round in `data/trials/exp001_pilot.jsonl` carries an `executor_overridden` field** (round keys are
exactly `action`, `agent_outputs`, `disagreement`, `env_result`, `round`, in 80/80 rounds). That field
postdates this run. The §F line "the exp001 pilot had 0 conflicts in 80 multi-agent rounds" is therefore
**true by recomputation, not by log**: I verified planner `plan_route` maps to the executor's `action` in
80/80 rounds (A/ADVANCE_A ×44, B/ADVANCE_B ×36), which is what makes it true. But because they never
differ, the recorded `action` is equally consistent with "executor's action was taken" and "planner's
route was enforced" — the authority rule is **unidentified on this data**. Worth a one-line correction
to §F's provenance claim.

## 5. Ceiling / floor flags (§K)

- **Unanimity is at ceiling.** Route agreement is 80/80 (100%). Disagreement is at an absolute floor of 0.
  Under §K this is *inconclusive about the aggregation rule*, not evidence that aggregation rules are
  equivalent in general. It is evidence that **on this task, with this model, no rule can differ**.
- **The 80 rounds are not 80 independent observations.** Nothing changes between rounds within a trial;
  each trial is one route decision repeated ~4×. Effective n is 20 trials (10 invalidating). Round-level
  CIs are anticonservative; prefer [0.000, 0.1611] (n=20) or [0.000, 0.2775] (n=10 invalidating).
- **The behavior itself is at a floor**, which is upstream of everything here: `wasted_actions` ∈ {0,4}
  in 40/40, `hold_actions` 0.0 in all eight cells, `rounds_played` 4 / `rounds_unused` 4 in 40/40
  (`results/exp001_pilot.json`). A HOLD tie-break can never be observed in a design where HOLD is
  never chosen by anyone.
- The one deviant trial (`C-005`, ADVANCE_A ×4 under an invalidating update) is **unanimous A across all
  four roles** — it is the route-attribution error documented in §1.1 of the skeptic critique, not dissent.
  A vote would have reproduced it exactly. This is the single most important qualitative point in the file.
