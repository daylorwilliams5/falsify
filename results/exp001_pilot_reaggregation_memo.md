# Memo — F9-C1 offline re-aggregation of exp001_pilot (EXPLORATORY)

Agent: statistician. Date: 2026-10-03. **Corrected 2026-10-03 under `decisions/D007.json`.**
**Authorized by `decisions/D003.json`** (PI, Level 1) — the corrective decision that withdrew D002's
pre-committed status-transition clause and re-authorized this artifact as purely exploratory.
Label: **EXPLORATORY** per `specs/EDGE_CASE_POLICY.md` §K. **No hypothesis status change is proposed here.**

> **Provenance chain (do not collapse this).** Originally authorized by `decisions/D002.json`, which the
> methodology reviewer **FAILED** (`critiques/review_D002.md`) on three authority findings about a
> pre-committed H8/H5a status-transition clause. **Only the analysis portion of D002 survived**: the reviewer
> ruled the route-intention redefinition legitimately Level 1 (`disagreement_rounds` is secondary per
> `PREREG_V2.md:32`; the token artifact is at `falsify/org.py:161`; C7 at `critiques/loop1_auditor.md:289-290`
> specified the redefinition *before* D002). The defect was in the inference D002 pre-authorized, not in the
> data work, so this artifact is **not tainted** — but its only authorization pointer was to a failed record.
> `decisions/D003.json` supersedes that half of D002 and re-authorizes this artifact.
> `decisions/D007.json` discharges the `critiques/review_D003.md` CONCERNS (findings 3–6) and mandates the
> five corrections applied below. Corrections made by the statistician; the PI does not hand-edit results files.

### Corrections applied under D007
| D007 item | Correction |
|---|---|
| 4 | `_meta.authorized_by` re-pointed D002 → D003, supersession chain recorded (not dropped) |
| 4 | residual `org.py:160` → **`org.py:161`** (line 160 is `executor_overridden`; 161 is the `disagreement` expression) — verified on disk |
| 3 | count-vs-rate unit clarification for cell D `disagreement_rounds = 1.0` (§2a below; last bare quote at §2 fixed under D010 item 4) |
| 2 | structural qualification now bound to every statement of the 0/80 zero |
| 1 | declination of the aggregation build recorded as **scoped and reversible** (§6 below) |

- Input (read-only): `data/trials/exp001_pilot.jsonl`, sha256 `afdd0786dfc592db054725c310a8302ad0c1e65b1ac6ae4547fbbb998125e669`.
  **Re-verified under D007: sha256 unchanged, identical to the value recorded at first analysis**
  (`_meta.source_sha256_unchanged: true`); `git status --porcelain data/trials/` clean for this file.
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

> ### ⚠ STRUCTURAL QUALIFICATION — this zero may not be quoted bare (D007 item 2)
> **The instrument cannot express the construct for 2 of the 4 roles.** The Researcher and Reviewer have
> **no route field at all** in their output schemas (`falsify/org.py` SCHEMAS:20–23). Only the Planner
> (`plan_route`) and the Executor (`action`) carry a structurally recorded route intention — and those two
> are already coupled by `EDGE_CASE_POLICY` §F planner authority. 14/160 free-text role-rounds were
> unrecoverable and were left null rather than imputed. This is adjacent to the §K floor logic the lab
> applied to H1.
>
> **What licenses relying on the zero is the adversarial sensitivity analysis**, and it must be cited
> alongside the zero every time: reassigning all 14/160 unrecoverable intentions over **every** A/B/HOLD
> combination flips **0 rounds**; and dropping both free-text roles entirely leaves planner vs executor
> agreeing in **80/80** rounds. Without that analysis this number would not be usable.
> (`critiques/review_D003.md` §4; `decisions/D007.json` item 2.)

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
| Legacy `disagreement` (`falsify/org.py:161`) | **6** | 80 | **0.075** | [0.0348, 0.1541] |
| Route-intention disagreement (this analysis) | **0** | 80 | **0.000** | [0.000, 0.0458] |
| Absolute gap | — | — | **0.075** (7.5 pp) | — |

Per cell (n=20 rounds each), as a **rate of rounds flagged**: legacy **D = 0.25**, C = 0.05, C0 = 0.00,
D0 = 0.00. Route-intention disagreement = **0.00 in all four cells**.

### 2a. UNIT CLARIFICATION — `disagreement_rounds = 1.0` is a COUNT, not a proportion (D007 item 3)

This is a real error that has propagated since the **11:10:03 timeline entry** and was repeated in
`decisions/D005.json` item 3. Stated bare, "1.0" reads as 100%. **It is not 100%.**

| Cell | Per-trial counts | Mean **count** (rounds/trial) | **Rate** (rounds flagged / 20 rounds) |
|---|---|---|---|
| **D** | **[1, 2, 1, 1, 0]** | **1.0 rounds/trial** | **0.25** |
| C | [0, 0, 0, 1, 0] | 0.2 rounds/trial | 0.05 |
| C0 | [0, 0, 0, 0, 0] | 0.0 | 0.00 |
| D0 | [0, 0, 0, 0, 0] | 0.0 | 0.00 |

The figures `1.0` (cell D) and `0.2` (cell C) in `results/exp001_pilot.json` are **per-trial counts**,
unit = rounds/trial. **Correct statement:** the legacy `org.py:161` field fires on **6/80 rounds = 0.075**
overall and on **5/20 rounds = 0.25** in cell D (mean **1.0 rounds per trial**), against a route-intention
disagreement rate of **0/80 = 0.000**. **Rule going forward: never quote `disagreement_rounds` without its
unit** — write "1.0 rounds/trial (= 0.25 of rounds)".

Note this *strengthens* rather than weakens the §1.4 point: cell D's legacy flag fires on a quarter of
rounds, not all of them, and every one of those rounds is unanimous on route.

The 6 legacy-True rounds are `D-001#r1`, `D-002#r1`, `D-002#r2`, `D-003#r1`, `C-004#r1`, `D-004#r1`.
In every one of them all recoverable roles name the **same** route. They are CONTINUE/REPLAN token
differences only. This **confirms `critiques/exp001_pilot_skeptic.md` §1.4 quantitatively**: the field
is a label artifact. Cell D's `disagreement_rounds` = **1.0 rounds/trial (i.e. 0.25 of rounds, from
per-trial counts [1, 2, 1, 1, 0] — a COUNT, not a proportion; see §2a)** against `wasted_actions` = 0.0
in `results/exp001_pilot.json` is a token count, not organizational conflict. The C7 redefinition
is delivered here.

*(Unit added under `decisions/D010.json` item 4 / `critiques/review_D007.md` §6, which identified this as
the last surviving bare quote. The raw recorded field value in `results/exp001_pilot.json` and
`_stats.json` is `1.0` and those files are immutable and untouched. Attribution corrected: the PI's own
propagation of the bare figure is in `decisions/D002.json`, **twice** — in `decision` and again in
`alternatives_rejected` — **not** in `decisions/D005.json`, which contains no occurrence.)*

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

---

## 6. Scope and reversibility of the build declination (D007 item 1)

Recorded here because `decisions/D003.json` dropped the scoping that `D002` had carried, and
`critiques/review_D003.md` §3 found that the declination is only distinguishable from a verdict if it is
stated as scoped and reversible.

- **What was declined:** funding the 3–4h plurality/flat-aggregation build (`decisions/D005.json` item 1).
- **Nature:** a **resource-allocation call, not a hypothesis verdict.** The reviewer attacked this framing
  at full strength and **upheld** it (`critiques/review_D003.md` §2).
- **Scope:** applies to **exp001_pilot's 80 multi-agent rounds only — to this dataset, not to the construct.**
- **Reversibility:** **a measured non-zero route-intention disagreement rate in any future arm revives
  H8/H5a as a fundable branch.**
- **Prohibited paraphrases:** no downstream document may describe this as H8 or H5a being *inert, dead,
  falsified, vacuous* or *retired*. H8's prediction is explicitly **conditional** on a non-zero disagreement
  rate; an unmet antecedent in one dataset is not the generalizing claim a verdict requires.
- **Registry state:** H5 and H3 remain `untested`. H8 and H5a remain unregistered **proposals** under
  `registry/hypotheses.json` `proposed_loop1`, with no status at all. The registry is untouched.
- **Also unmeasured:** ties were reached **0/80**, so the HOLD tie-break — which
  `critiques/escalation_conditions_skeptic.md` F8 argues *is* the mechanism — is **unmeasured, not validated**.
