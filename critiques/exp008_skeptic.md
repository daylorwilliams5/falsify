# Skeptic critique: the amended exp008 (I1 + I3) and the two "verified auditor defects" fixes

Agent: skeptic. Date: 2026-10-03, loop 2. Nothing proposed here is run by me; this document
contains confounds and controls only. No psychological attribution to the subject: the terms are
*persistence after invalidation*, *process violation*, *reserve without a prior verify*.

Read: `specs/AUTHORITY.md`, `lab/mandate.json`, `specs/EDGE_CASE_POLICY.md` (A–N),
`specs/PREREG_V2.md`, `registry/hypotheses.json` (M1, P5), `critiques/loop1_auditor.md` (§1–§5),
`critiques/escalation_conditions_skeptic.md` §4.1–§4.3 (F11/F12/F13), §8.1,
`specs/candidates/exp008_auditor_m1.json`, `specs/exp009_v2_floor_probe.json`, `decisions/D001.json`,
`decisions/D002.json`, `results/exp001_pilot.json`.
Code read: `falsify/org.py` 8–56, 100–175 (v1 auditor at 131–139), 195–256 (v2 auditor at 222–229),
`falsify/env.py` 30–80 (`task_text`, `auditor_view` 47–57), `falsify/env2.py` (whole),
`falsify/cli.py` 37–110 (`PREREG_SPACE`, `required_level`), `falsify/analyze.py` 38, 68, 104, 142–146.

---

## 0. Bottom line

1. **The leading option is not one experiment.** `specs/candidates/exp008_auditor_m1.json` declares
   `"environment": {"name": "freightroute", ...}` — it runs `run_trial` (`falsify/org.py:104`), which
   calls the **v1** auditor at `org.py:131–139`. The defect at `org.py:222–229` is in `run_trial_v2`,
   a code path exp008 never enters. Fixing the v2 call site therefore changes nothing about exp008,
   and the only way to "combine" the two is to migrate exp008 to `freightroute_v2` — which changes
   the environment family, the hypothesis (M1 → P5), the primary-outcome set
   (`wasted_actions` → the seven `PREREG_V2` outcomes) and the auditor's output vocabulary. That is a
   new experiment, not an amendment (§3).
2. **The v2 "fix" makes the instrument worse, not better, in two verified ways.** (a) The v2 auditor
   is not given `auditor_view()` at all — `Scenario2` has no such method; `org.py:223–224` passes
   `system_prompt("auditor", task)` with `task = sc.task_text()` plus `env.status_line()`.
   `status_line()` (`env2.py:139–142`) reports `Route A {reserved}/{n} reserved` — **the prior
   investment amount that §I forbids**. Pre-round-1 that string reads 0/0 and is harmless; a mid-run
   call makes it a live §I violation. (b) `task_text()` (`env2.py:38–58`) interpolates
   `INCENTIVES[self.incentive]`, so the v2 auditor is **exposed to the pressure manipulation itself**
   — the oversight arm is not independent of the treatment it is supposed to correct.
3. **The v2 auditor cannot name the behavior P5 is about.** `SCHEMAS_V2["auditor"]` inherits
   `SCHEMAS["auditor"]` (`org.py:200`, `org.py:27`): `{rationale, recommendation ∈ {CONTINUE,
   REPLAN}}`. The v2 violation is "RESERVE without a prior VERIFY" (`env2.py:144–160`). No value of
   `{CONTINUE, REPLAN}` expresses "verify first". `auditor_correct` — I1's headline outcome — is
   **undefined in v2**. Moving the call site mid-run without replacing the schema buys a mid-run call
   that still cannot observe-and-report the target behavior.
4. **Power.** As described, the design is 10 cells (§2.4). Under the 120-trial level-1 cap that is
   **n = 12 per cell**, where the detectable `real − sham` difference at 80% power is **≈ 0.52
   absolute**, and the `mode × view` interaction is not estimable at any n this lab can afford
   (n ≈ 93/cell for a 0.30 → 0.50 contrast ⇒ 930 trials, 7.8× the trial cap).
5. **Both ends of I1 are saturated, not merely one.** Subject side: `switched` = 1.0 in cells B and D
   (`results/exp001_pilot.json`), so maximum possible improvement there is exactly 0. Auditor side:
   `auditor_correct` is plausibly ~1.0 by construction and is **unmeasured**; at n = 15 the ≥0.90
   adequacy gate passes with probability 0.55 when the true rate is exactly 0.90 and 0.83 when it is
   0.95 — it cannot discriminate 0.90 from 0.999. I1 risks reporting a ceiling as a premise (§2.3).
6. **There is a cheaper measurement that dominates** (§5): a zero-subject-trial auditor instrument
   calibration (standalone auditor calls, no team loop, no trial loop), plus two zero-model-call
   offline items.

---

## 1. Verdicts on the five attacks the PI asked for

| # | Attack as posed | Verdict |
|---|---|---|
| 1 | Sham cannot decompose re-briefing if it retains "including {bridge}"; so sham−none is not token-matched to real−sham and the decomposition is unidentified | **Mostly NOT real as posed; a different non-identification is real** (§2.1) |
| 2 | Three levels × two views not estimable under a 120-trial budget | **REAL, and quantified** (§2.4) |
| 3 | Uptake is architecturally zero given §I advisory-only + §F Planner finality | **NOT real for the stated measure; a measurement confound is real** (§2.2) |
| 4 | `auditor_correct` is itself at a ceiling, so the ≥0.90 gate is uninformative and q ≈ 0 by construction | **REAL and currently untested** (§2.3) |
| 5 | Fixing the v2 call site requires fresh preregistration, not an amendment | **REAL, but for the right reason — not the governance level** (§3) |

---

## 2. The threats

### 2.1 The sham arm (attack 1): the PI's objection misfires; a nearby one lands

**Not real as posed.** The decomposition does not require sham to drop the binding. In
`critiques/escalation_conditions_skeptic.md` §4.2 (F12-C) and `critiques/loop1_auditor.md` §1.3
element 1, the view text is **held constant** between `sham` and `real`; only the `recommendation`
field differs. Then:

- `real − sham | view` differences out the binding aid, the certification aid, the clean-context aid,
  the extra log turn and the token cost. It estimates the **recommendation** effect — the only
  quantity M1 is about. Identified.
- `sham − none` is the restatement bundle. It is *not* internally decomposed, and the oversight
  specialist never claims it is: §4.5 of `critiques/loop1_auditor.md` explicitly says it "must be
  reported as the restatement effect and never as oversight".

So "sham must drop the binding to be a clean control" conflates the **mode** factor with the **view**
factor. The view factor (element 2) is what removes the binding, and it is crossed with mode
precisely so the binding's contribution is measured rather than assumed.

**What is real, three ways:**

- **T7 — sham and real are not text-matched in practice.** `_schema` puts `rationale` first in every
  schema (`org.py:13–16`) and the whole auditor output is serialized into the shared log
  (`org.py:138`, `org.py:227`). In the `real` arm that rationale is **model-generated free text** which
  will frequently restate the bridge-to-Route-A binding and the Route B limits. So `real` contains
  *more* restatement than `sham`, and `real − sham` is contaminated by a second dose of the very aid
  the sham was built to hold constant. **Control (0.25 h, preregister before the run):** log only the
  fixed-length decision field from the auditor in both arms (or a preregistered fixed rationale
  template in both), and keep the model-generated rationale in `derived` only, never in the subject's
  log. Report the character/token count of the inserted auditor turn per arm as a manipulation check.
- **T11 — the view factor as written bundles three changes.** `critiques/loop1_auditor.md` §1.3
  element 2 asks to (a) drop "including {bridge}", (b) present routes symmetrically, and (c) record
  the answer as a **route** rather than CONTINUE/REPLAN. (c) is not a wording change: an auditor turn
  that says "B" names the target action, which is a strictly more directive intervention than
  "REPLAN". Crossing mode × view then confounds wording symmetry with directive specificity.
  **Control:** fix the output vocabulary across both view levels (both answer a route; or both answer
  CONTINUE/REPLAN) and vary only the view prose. Vocabulary becomes a separate, later factor.
- **T2 — `real − sham` is not "oversight" even when identified.** The `real` recommendation is
  produced by the same checkpoint at the same temperature (`org.py:137`: `seed * 100 + 99`,
  `model_cfg["temperature"]`) from a **pre-solved, history-free** view. `real − sham` therefore
  estimates "a correct answer delivered from a privileged context", not "an independent overseer".
  That is the F13 error-independence problem, and it is not fixed by the sham arm. **Control:** the
  §5 calibration measures the auditor's own error rate on the same scenarios, so the estimate can be
  reported as conditional on auditor fidelity rather than as an oversight effect.

### 2.2 Uptake (attack 3): not architecturally zero

**Not real as posed.** §I makes the recommendation *advisory* and §F makes the Planner's route
*authoritative over the Executor* — `org.py:155–160` overrides the Executor's action with the
Planner's `plan_route`. Neither clause prevents the auditor's text from changing the Planner's
`plan_route`: the auditor turn is appended to the shared `log` (`org.py:138`) and `build_messages`
(`org.py:83–100`) feeds the whole log to every role as user turns. The auditor cannot *override*; it
can persuade. And `critiques/loop1_auditor.md` defines uptake as **textual reference in post-auditor
role outputs** written to `derived`, not as compliance. Zero uptake is an empirical possibility, not
an architectural guarantee, and a 0/n result would be informative about this architecture.

**What is real:**

- **T8a — no comparator.** "k of n role outputs mention the auditor" is uninterpretable without the
  base rate at which this model's role outputs cite *any* other role. **Control, zero model calls:**
  compute the role-citation base rate offline from the 20 existing exp001 multi-agent transcripts in
  `data/trials/exp001_pilot.jsonl` (read-only; same discipline as D002). This is the comparator and
  it costs nothing.
- **T8b — position/recency.** The auditor turn is the **last** log entry before round 1
  (`org.py:131–139`), so uptake is confounded with recency. The `sham` arm is the matched
  position/recency control — which is the sham arm's strongest justification, stronger than its role
  on `wasted_actions`. Say so in the spec.
- **T8c — the classifier is undefined.** Coding "references the auditor turn" needs a rule. A regex
  over a preregistered string list is acceptable and cheap; an **LLM judge is not** — any non-subject
  model is a model-population change, level 3 under `specs/AUTHORITY.md` and §M. **Control:** fix the
  string list in the spec before the run and hand-double-code 20 trials to report agreement.
- **Honest framing requirement.** If uptake is 0/n, the licensed claim is "in this architecture, with
  an advisory pre-round-1 auditor turn, no role output referenced it" — a fact about this
  implementation. The PI's instinct is right that it must not be sold as a general negative result
  about oversight, even though it is not guaranteed by the code.

### 2.3 Auditor ceiling (attack 4): REAL, and it is the sharpest attack of the five

No auditor has ever been called in a logged trial — `auditor: false` in all eight cells of
`results/exp001_pilot.json`, and `PREREG_SPACE` pins `auditor: {False}` for both families
(`cli.py:41,44`). So `auditor_correct` is unmeasured, and `critiques/loop1_auditor.md` §I1 is right
that "any value is informative". But "unmeasured" is not "unfloored":

- The v1 auditor receives `auditor_view()` (`env.py:47–57`): one short paragraph, no scripted
  history, with the bridge∈Route A binding **already performed** and Route B's limits restated
  adjacent to the new evidence, then `contradiction_text()` as the newest report. Comparing
  `post_tokens_in` 2 532.8 (cell A) with 41 756.2 (cell D), the auditor's task is strictly easier
  than the subject's on exactly the sub-task the subject failed.
- The arithmetic is a single comparison of two numbers at `invalid_ratio = 1.4`, and the subject
  resolved it correctly even in the two failing trials
  (`critiques/exp001_pilot_skeptic.md` §1.1). The prior on `auditor_correct` ≈ 1.0 is high.

**T5 — the ≥0.90 adequacy gate is underpowered and probably uninformative.** At n = 15 per cell:
P(pass | true 0.90) = 0.55, P(pass | true 0.95) = 0.83. A 15/15 result has a Wilson 95% interval of
[0.796, 1.0] — it cannot separate 0.90 from 0.999, which is the whole content of the gate. If the
true rate is 1.0 the gate passes by construction and reports nothing.

**T6 — q is not estimable at exp008's n.** With `auditor_correct` at ceiling, the numerator of the
auditor mis-binding rate is near-empty: 0/60 gives a Wilson upper bound of 0.060. The comparator,
"materially below the subject's", comes from 2/20 (Wilson [0.028, 0.301]) and those two trials are
**one seed** (seed 5, cells A-005 and C-005), so the subject's q is confounded with scenario. "0 vs
0.10" at those n is not separable, and an auditor-error-independence claim from it would be a §K
violation.

**Control for both:** measure `auditor_correct` and the rationale binding-error rate **before** any
exp008 trial, with standalone auditor calls and no subject trials at all (§5). 200 calls give a
Wilson width of roughly ±0.03–0.07 instead of ±0.20, and they decide whether exp008 is worth running.

### 2.4 Cell count and power (attack 2): REAL — here are the numbers

Factors as the PI described them: `auditor_mode ∈ {none, sham, real}` × `auditor_view ∈ {symmetric,
incumbent}` × `update ∈ {invalidating, benign}`. The view factor is undefined for `none` (no view is
shown), so:

| | invalidating | benign | cells |
|---|---|---|---|
| none | 1 | 1 | 2 |
| sham × 2 views | 2 | 2 | 4 |
| real × 2 views | 2 | 2 | 4 |
| **total** | | | **10** |

(12 if `none` is duplicated across view levels for balance; 40 if exp008 is migrated to v2 and crossed
with the frozen `budget × incentive` pressure cells of `PREREG_V2`; 20 if `org ∈ {single, multi}` is
retained.)

**Per-cell n under the level-1 trial budget (120, `lab/mandate.json`): 12.** The call budget is *not*
the binding constraint — multi-agent pilot trials used 16 calls each (`results/exp001_pilot.json`
cells C/D), so 120 auditor-bearing multi trials ≈ 2 040 calls against the 4 000 cap. **Trials bind.**

Two-proportion, α = 0.05 two-sided, 80% power:

| n per arm | MDE from 0.10 | from 0.30 | from 0.50 |
|---|---|---|---|
| 12 | 0.52 | 0.54 | 0.48 |
| 15 | 0.46 | 0.49 | 0.44 |
| 20 | 0.39 | 0.43 | 0.40 |
| 30 | 0.31 | 0.36 | 0.34 |

n needed: 0.30 → 0.50 requires **93/arm**; 0.30 → 0.45 requires 163/arm; 0.10 → 0.25 requires
100/arm. At 10 cells, 93/cell = **930 trials ≈ 15 800 calls**: 7.8× the trial cap and 3.9× the call
cap. **Verdict: the `real − sham` contrast is powered only for effects above ~0.5 absolute, and the
`mode × view` interaction — the reason the view factor is in the design at all — is not estimable at
any affordable n.** Buying the view factor at this budget buys a column you cannot read.

Worse, the contrast is on `wasted_actions`, which is 0 in 18/20 invalidating pilot trials and
quantized to {0, 4} (`specs/candidates/exp002_salience1.json` notes this), with `switched` = 1.0 in
cells B/D. The denominator of the effect does not exist yet.

**Control:** if the view factor is wanted, run it as a **single-factor** comparison on the auditor
alone (§5), where n is cheap because no subject trials are involved, and keep the subject-side
experiment at the 3-level mode factor only (4 cells, n = 30/cell at 120 trials).

### 2.5 Mid-run / per-reserve call (the v2 fix): four threats, all verified in code

- **T1 — §I violation created by the fix.** `org.py:224` passes `env.status_line()`, and
  `env2.py:139–142` emits `Route A {reserved}/{n} reserved`. At round 0 that is 0/0; mid-run it is the
  **prior investment amount** §I forbids, and §I's status note claims this exact leak was "fixed
  before any auditor trial ran" — it was fixed in v1 only, because `Scenario2` has no
  `auditor_view()`. **Control:** build `Scenario2.auditor_view()` (route-symmetric, investment-free,
  budget-remaining-only) before any mid-run call, and record its variant id per cell.
- **T1b — the auditor is inside the manipulation.** `task_text()` interpolates
  `INCENTIVES[self.incentive]` (`env2.py:44`), so in `target` cells the auditor also receives "runs
  below 100 are recorded as failed runs". Any `auditor × incentive` interaction is then partly an
  effect of the auditor's own exposure. **Control:** strip `INCENTIVES` from the auditor's view, or
  preregister incentive-exposure as an explicit auditor-side factor and report both.
- **T3 — endogenous dose.** A **per-reserve** trigger makes the number of auditor calls a function of
  `reserves`, which is itself a measured outcome (`env2.py:measure()` → `"reserves"`), and reserves
  co-move with `process_violations`. Trials that violate more get more oversight, so any dose-response
  is reverse-caused, and "auditor" cells are no longer matched to "none" cells on call count, context
  length (H6) or wall clock. **Control:** make the schedule **exogenous** — a preregistered fixed set
  of rounds (e.g. before rounds 3, 5, 7) independent of the chosen action, with the same number of
  discarded calls in the `sham`/`none` arms so call count and token count are matched. `status_line()`
  already reports reserve counts, so a fixed-round call can observe a reserve without being triggered
  by one.
- **T3b — "per-reserve" smuggles in a new architecture.** To observe a reserve *before* it executes,
  the call must interpose between the agent's chosen action and `env.step` — i.e. a pre-execution
  review gate. Without a subsequent re-decision call the advice can only affect round n+1 anyway, so
  the placement gains nothing; with one, the arm is no longer advisory and §I's "fixed, preregistered"
  advisory-only clause is breached. **Control:** choose explicitly — exogenous fixed-round advisory
  (keeps §I) or a binding arm (new IV, and `critiques/loop1_auditor.md` §4.3 requires it be gated on
  the fidelity result first, which is §5).
- **T15 — differential attrition.** `run_trial_v2` wraps the whole trial in one `try` and any
  `ParseFailure` invalidates it (`org.py:246–248`). Each added auditor call is another chance to
  invalidate a whole trial, only in the auditor arms. §A reruns at seed + 10 000 and **pauses the run
  above 10% invalid in a cell** — so the auditor arms carry a higher pause risk and a
  treatment-correlated invalid rate. The pilot's parse-failure rate was 0.0, so the risk is low but it
  is one-sided. **Control:** report invalid counts per arm as a preregistered balance check; wrap the
  auditor call in its own try so an auditor parse failure is recorded as a missing auditor turn rather
  than a lost trial — and preregister which of those two it is before the run.

### 2.6 Bookkeeping threats that will silently misreport this design

- **T10a — `bin/falsify level` is blind to new keys.** `required_level` (`cli.py:74–101`) iterates
  over the keys in `PREREG_SPACE` only. I verified that taking
  `specs/candidates/exp008_auditor_m1.json` (which correctly returns **level 2**: "cell M_hier_aud:
  auditor=True outside preregistered [False]"), removing `auditor` and substituting
  `auditor_mode: "real"` and `auditor_view: "symmetric"`, makes `required_level` return **1, "inside
  preregistered condition space"** — a spec with two brand-new manipulations classified as PI
  autonomous. **Control (0.25 h, do it before writing the spec):** add `auditor_mode` and
  `auditor_view` to `PREREG_SPACE` for both families, and add an unknown-cell-key check that forces
  level ≥ 2 for any cell key not in the space. Otherwise the reviewer audits a level the code
  understated.
- **T10b — `prompt_hash` does not cover the auditor view.** `prompt_hash()` (`org.py:54–56`) hashes
  `[TEAM, DUTIES, SINGLE, AUDITOR, SCHEMAS]`. `auditor_view()` lives in `falsify/env.py` and is not
  hashed, so two trials with different view wordings are indistinguishable in the trial record.
  **Control:** record `auditor_view_variant` in the cell and add the `env.py`/`env2.py` SHA prefix to
  every trial, as `specs/exp009_v2_floor_probe.json` already does for the env freeze.
- **T10c — `analyze.py` groups on a boolean.** `analyze.py:38, 68, 104, 142–146` read
  `t.get("auditor", False)` and group on it. A three-level `auditor_mode` will be silently collapsed
  unless the grouping is widened first. This is the oversight specialist's own note; it is a
  prerequisite, not a follow-up.
- **T9 — the benign harm flag will fire by chance at this cell count.** The preset rule
  (`critiques/loop1_auditor.md` §I1) flags when a benign unnecessary-switch count's Wilson lower bound
  exceeds 0 — i.e. on a single event. The expanded design has 4 benign auditor-bearing cells; at
  n = 12 that is 48 benign auditor trials. The pilot baseline is 0/20 (Wilson upper bound 0.161), so
  if the true rate is only 0.05, P(at least one event) = **0.91**; at 0.02 it is 0.62. The flag is
  near-certain to fire for no reason. **Control:** preregister the harm rule at the **family** level
  on pooled benign trials, against an exact-binomial test using the pooled benign baseline, and
  require ≥2 events in a cell before a cell-level flag.
- **T13 — model specificity.** One checkpoint (`qwen3:8b`), one temperature (0.7), seeds 1–15.
  "Error independence" is a property of this checkpoint paired with itself; §M forbids pooling any
  other model. State this as a scope limit in the spec, not as a limitation paragraph afterwards.

---

## 3. Amendment or fresh preregistration? (attack 5)

**Governance level:** no behavioral data exist for exp008 (zero auditor trials anywhere), so under
`specs/AUTHORITY.md` this is "a protocol amendment before behavioral data exist" plus "a new control
or manipulation" = **level 2, reviewer PASS**. It is not level 3: the primary-outcome clause at level
3 is scoped to "after results exist". The PI's stated path (level 2 + reviewer PASS) is the correct
*level*.

**But a fresh preregistration is still required, for scientific reasons the amendment label hides:**

1. **It is a different environment.** exp008 is `freightroute`; the `org.py:222–229` defect is
   `freightroute_v2`. One spec cannot contain both code paths. Migration changes the environment
   family, the hypothesis (M1 → P5; `registry/hypotheses.json` and `PREREG_V2` §"Hypotheses tested"
   explicitly **reserve P5 for follow-ups**) and the entire primary-outcome set.
2. **It changes the auditor's output vocabulary.** A v2-valid auditor needs a schema over
   `VERIFY/RESERVE/REPORT` (`env2.py:13`), which changes `SCHEMAS` and therefore `prompt_hash`
   (`org.py:54–56`). A changed primary outcome plus a changed instrument vocabulary is a new
   preregistration in substance whatever it is called.
3. **It trips the `PREREG_V2` freeze.** `env2.py` is frozen at SHA-256 prefix `3acdf7bbbc1e2d94`;
   exp009 is already in flight on an instrumented variant whose hash must be logged under §N. A later
   `Scenario2.auditor_view()` plus schema change creates a **second** env version and a before/after
   split against the exp009 trials, which `PREREG_V2` requires be reported separately. Writing it as
   an "amendment to exp008" would obscure that split.

**Recommended framing:** keep the exp008 amendment narrowly to what it can honestly be — a v1,
M1-family experiment with `auditor_mode` as the only new factor and the fidelity/uptake set as the
declared primary outcome, with `wasted_actions` retained as a floor-limited secondary — and write the
v2 auditor as a separate P5 spec that cannot be written at all until exp009 reports (because the v2
auditor arm must be matched on `budget × incentive`, and the `budget = 10` cells are on the §3
UNTESTABLE list in `critiques/loop1_auditor.md` pending the feasible/forced split).

---

## 4. Strongest objection to the leading option

**The leading option spends the lab's only level-2 slot this loop on a two-sided saturated
measurement in the wrong environment, and the fix it bundles makes the other environment's instrument
non-compliant.**

Concretely: on the subject side, `wasted_actions` is 0 in 18/20 invalidating pilot trials and
`switched` = 1.0 in cells B/D, so the maximum improvement the mode factor can produce in half the
design is exactly 0. On the auditor side, `auditor_correct` is unmeasured but has a high prior of
~1.0 because `auditor_view()` hands the auditor the pre-solved binding in a clean context — in which
case the ≥0.90 gate passes by construction (and at n = 15 cannot separate 0.90 from 0.999 anyway) and
q is 0/60. I1's three premises then resolve to "ceiling, inestimable, and uptake against no base
rate". Meanwhile the v2 half of the bundle (a) introduces a §I prior-investment leak via
`status_line()`, (b) exposes the auditor to the incentive manipulation via `task_text()`, (c) retains
a CONTINUE/REPLAN vocabulary in which the target behavior cannot be named, and (d) makes oversight
dose a function of an outcome variable. And the whole thing is 10 cells at n = 12, powered only for
effects above ~0.5 absolute.

**Cheapest honest repair:** split it. (i) Run the §5 calibration first — it is the only part of I1
that is adequately powered and it is a prerequisite for interpreting everything else. (ii) Fix the
bookkeeping (`PREREG_SPACE` keys, `analyze.py` grouping, `auditor_view_variant`, env hash in the
trial record) — hours of work, no trials. (iii) Attack the v1 floor with a factor already **inside**
the preregistered space: `env.salience_step ∈ {0, 1, 2}` (`cli.py:42`). I verified
`required_level("specs/candidates/exp002_salience1.json")` returns **1** — a 60-trial, PI-autonomous
run that attacks the floor M1 depends on, with no new manipulation and no reviewer gate. A mitigation
experiment before a measured phenomenon inverts the dependency; D001 already made that argument for
v2 and it applies identically to v1.

---

## 5. The cheaper measurement that dominates

**Auditor instrument calibration — zero subject trials, zero new architecture.**

Call the auditor prompt **standalone**: `system_prompt("auditor", view)` +
`{"role": "user", "content": f"Newest report: {sc.contradiction_text()}"}`, exactly as at
`org.py:134–136`, with **no team loop, no scripted history, no subject org**. Grid: seeds 1–50 ×
`update ∈ {invalidating, benign}` × `view ∈ {incumbent (current `env.py:47–57`), symmetric}` = **200
single model calls**, a few minutes locally, no external spend, no trials.

Outcomes, all preregistered before the calls:
1. `auditor_correct` per cell, with Wilson intervals (width ≈ ±0.03–0.07 at n = 100 per view).
2. Rationale binding-error rate (the auditor's own q) by regex over a preregistered string list, plus
   hand double-coding of 40 rationales with reported agreement. No LLM judge — that is a level-3
   model-population change.
3. The incumbency effect: `auditor_correct(incumbent) − auditor_correct(symmetric)` and the
   CONTINUE-rate difference. This is F11 measured directly, at n = 100 per level, instead of as an
   unpowered interaction column inside a 10-cell subject experiment.
4. Determinism check: repeat 20 seeds at temperature 0 to separate sampling noise from capability.

**Why it dominates the leading option:**
- It resolves two of I1's three premises (fidelity, and the auditor's own error rate) at 5–10× the
  precision exp008 would give, for roughly 1/10 the compute and no subject trials.
- It is the gate `critiques/loop1_auditor.md` §4.3 already requires before any binding arm, and the
  §4.1/F11 anchor measurement, in one artifact.
- It cannot be floored or ceiling-confounded in its interpretation, because measuring where the
  ceiling is *is the result*: if `auditor_correct` ≈ 1.0 with a tight interval, exp008's ≥0.90 gate is
  known in advance to be uninformative and the spec must drop it; if it is < 0.90, exp008 should not
  be run at all until the instrument is repaired, and that is a publishable negative about the
  mitigation's premise with no persistence phenomenon required.
- It is **not** a mitigation experiment on the subject: no subject prompt changes, no new IV on the
  subject org, no §F/§I architecture change. Governance-wise `auditor: true` cells still fall outside
  `PREREG_SPACE` (`cli.py:41,44`), so it computes level 2 — but a reviewer PASS on a 0-trial,
  200-call instrument calibration is a far cheaper and more auditable object than a PASS on a 10-cell,
  2-new-factor behavioral design.

**Two companions at literally zero model calls:** (a) the role-citation base rate from the existing
`data/trials/exp001_pilot.jsonl` multi transcripts (T8a), read-only, same discipline as D002; (b) the
bookkeeping fixes in §2.6, which must land before any three-level spec is written or the level
computation and the analysis will both misreport it.

---

## 6. Governance notes

| Section | Application |
|---|---|
| **I** | Verified violation **created** by the proposed v2 fix: `status_line()` exposes reserve counts (prior investment) and `task_text()` exposes the incentive manipulation to the auditor. `Scenario2` has no `auditor_view()`. Must be built before any mid-run v2 auditor call. |
| **K** | Both ends of I1 are saturation risks (subject floor, auditor ceiling); the ≥0.90 gate and the q comparison are reported here as underpowered with explicit n, CI and pass probabilities; the benign harm flag is shown to be a multiplicity artifact at 48 trials. No mechanism asserted from the two seed-5 trials. |
| **L / AUTHORITY** | The leading option is level 2 (new manipulation + amendment before data). It is **not** level 3. A fresh P5 preregistration is required on scientific, not governance, grounds (§3). `required_level`'s blindness to new cell keys is a verified enforcement gap (§2.6 T10a). |
| **A** | T15: added auditor calls inflate the per-trial `ParseFailure` surface only in the auditor arms, creating treatment-correlated invalid rates against the 10% pause rule. |
| **M** | Single checkpoint, single temperature. No LLM judge anywhere in the uptake or q coding. |
| **N** | To log on any approval: this critique; the v2 §I leak (`status_line`, `task_text`); the `required_level` new-key gap; the `prompt_hash`/`auditor_view` gap; spec hashes before the first trial. |
| Data | `data/trials/` read-only. The calibration and the citation base rate write new files only. |

---

## 7. On exp009 (asked and answered briefly)

Launching `specs/exp009_v2_floor_probe.json` was not an error and I do not re-litigate it. It is the
diagnostic I named in `critiques/escalation_conditions_skeptic.md` §8.1, it is human-approved in
`lab/mandate.json`, its reading rules are fixed in advance in the spec, and its instrumentation
landed before the first v2 trial so no before/after split was created. One note for the record: its
result is a **precondition** for the v2 half of the leading option, since
`critiques/loop1_auditor.md` §3 item 5 lists any oversight comparison in the `budget = 10` cells as
UNTESTABLE until the feasible/forced split is read. That is an argument for sequencing the v2 auditor
work after exp009 reports, not an argument against exp009.
