# Methodology review — D005 (loop 2)

**Decision:** D005 — decline to fund the aggregation-rule build (resource allocation), correct the PI's own
per-round-auditor premise, record three measurement-validity defects as OPEN, defer all oversight behavioral runs
until exp009 reports.
**Declared level:** 1 **Computed/required level:** 1 (no spec, no run, no trials, 0 model calls, 0 spend)
**Verdict: CONCERNS** — non-blocking. Nothing here needs to be stripped. Four wording/record fixes.

I checked `decisions/D005.json`, `results/exp001_pilot_reaggregation.json`, `..._memo.md`,
`critiques/exp008_auditor.md`, `decisions/D002.json`, `D003.json`, `D004.json`, `critiques/review_D002.md`,
`specs/AUTHORITY.md`, `specs/PROTOCOL.md` §4, `specs/EDGE_CASE_POLICY.md` §F/§K/§L/§N, `lab/mandate.json`,
`registry/hypotheses.json`, `sources/candidates.md`, `falsify/org.py`, `falsify/env.py`,
`results/exp001_pilot.json`, `results/exp001_pilot_stats.json`, `timeline.jsonl`, and ran
`./bin/falsify level specs/candidates/exp008_auditor_m1.json`.

---

## 1. Authority — level 1 is CORRECT, nothing level-2/3 is hidden

Itemized against the AUTHORITY.md level-3 list and the level-2 list:

| Trigger | Present in D005? |
|---|---|
| Primary-outcome change after results | **No.** D005 does *not* adopt the auditor's B.3 proposal to make fidelity/uptake primary; it defers exp008 entirely. `wasted_actions` is untouched. |
| Exclusion change | No. |
| Model-population change | No. Zero model calls, zero trials. |
| External spend | No (`$0`, mandate `external_spend_usd_without_human: 0` respected). |
| Novelty claim | No (see §6). |
| New control/manipulation, protocol amendment, new hypothesis family | No — and the one candidate that would be (the route field) is explicitly refused; see §3. |
| Resequencing (L2) | **No, on inspection.** Item (4) defers runs that were never authorized or sequenced: `specs/candidates/exp008_auditor_m1.json` is a candidate, `./bin/falsify level` returns **2** for it, and `lab/mandate.json::approved_specs` contains only `exp001_pilot` and `exp009_v2_floor_probe`. Deferring unauthorized work is declining to act, which requires no authority; and the deferral is *consistent* with the human's post-run ordering clause re-affirmed in D004(5), not a revision of it. |
| Status transition on unpreregistered criteria (the D002 defect) | **No.** Verified against `registry/hypotheses.json`: `status_labels` unchanged (5 labels, no new one); H3 and H5 still `untested`; H8/H5a still under `proposed_loop1` with no status field. No registry write. |

**Finding 1 (record hygiene, fix).** D005 carries no `code_hashes` block, although D004 does and the engineer's
12:10:52 timeline note states decisions now record them. This matters more than usual here: D005's substantive
content is three *source-code* claims. Pin them — `org.py d683a084718f700a`, `env.py 1e894fd234aa68f2`
(recomputed by me just now) — so the corrections are auditable against a code version.

## 2. The funding framing — NOT a disguised hypothesis verdict. I do not FAIL it.

You asked me to attack this, and I did. It survives, on four independent grounds:

1. **No object changed.** Registry is byte-identical in the relevant fields (§1 table). Nothing a future reader
   queries for a status would return anything new.
2. **Declining to spend is not in any level list.** AUTHORITY.md and `mandate.json` enumerate *actions*
   (run, conclude, amend, register, escalate). Not building something is not an experimental act; the only
   adjacent prohibition — inventing a status or a label — is exactly what D005 refuses in its own first sentence.
3. **The decision is responsive in both directions, which is the real test.** A resource call masquerading as a
   verdict is one that would have been made whatever the number said. D002 is on record that a measured non-zero
   "would revive H8 as the cheapest live hypothesis in the registry." So the funding call tracks the measurement
   symmetrically. That is what distinguishes it from a verdict.
4. **D005 states the limit of the zero itself**, in the same breath as using it ("the zero is a property of the
   task, not of aggregation rules"). A verdict in disguise does the opposite.

**Finding 2 (wording, fix).** Ground 3 is only load-bearing if the revival condition is *on this record*, and
D005 omits it. The word "**Close** the aggregation-rule branch" is the one phrase that reads terminally: a
"closed branch" is, to a reader a month from now, indistinguishable from a retired hypothesis even though no
status field moved. Replace with: *"Decline to fund now. This reopens on any measured non-zero route-intention
disagreement rate in any future multi-agent run; H5/H3 remain untested and H8/H5a unregistered in the meantime."*
That is a sentence, not a restructuring, and it closes the only gap through which a verdict could be read in later.

## 3. Re-entry through a side door — none found

Checked each of the three blockers in `critiques/review_D002.md` §1:

- (a) registering H8/H5a: not done, and D005 says so twice in terms matching the registry's own `proposed_loop1`
  status text.
- (b) new status label: none. "OPEN DEFECT" is applied to *measurement defects*, not to hypotheses, and is not
  written to `registry/hypotheses.json`. It is not a status in the registry's vocabulary and does not pretend to be.
- (c) non-preregistered criteria licensing a transition: no transition exists to license.
- `alternatives_rejected` explicitly re-rejects the status route ("this is precisely what the reviewer FAILED in
  D002 and I will not re-enter it through a side door"). Confirmed accurate.

The closest approach to the FAIL is **not** the funding language — it is §4 below.

## 4. §K — the one real finding. A mechanism-shaped claim rests on n=1.

D005's `reason` states: *"The qualitative finding is more informative than the zero … Voting buys nothing where
the error is shared, which is the error-correlation problem (F7/F20) in concrete form and is a better argument
against the build than the zero is."*

The evidentiary base for that is **one trial**. I verified `exp001_pilot-C-005` in
`results/exp001_pilot_reaggregation.json`: all four rounds, all four roles, vote vector `A/A/A/A`, all four
roles recoverable, sequences identical — so the factual description is exact. But the statistician's own memo §5
calls C-005 "the one deviant trial," and `specs/EDGE_CASE_POLICY.md` §K reads: *"No mechanism declared from one
or two unusual trials."*

**Finding 3 (fix, non-blocking).** "Voting buys nothing where the error is shared" is a mechanism statement
generalizing from a single trial, and D005 ranks it *above* the measured zero. Two of the four roles' routes in
that trial are also text adjudications by the statistician, not logged fields (defect ii, which D005 itself
records), so the "unanimous across all four roles" base is partly interpretive. Re-word to a single-trial
exploratory observation, e.g. *"In the one deviant trial (C-005, n=1, EXPLORATORY) the error was unanimous, so a
plurality rule would have reproduced it; this illustrates but does not establish error correlation (F7/F20)."*
Keep it as a reason not to spend money — that is legitimate — but it cannot be cited later as evidence about
voting, and as currently worded it could be.

## 5. Evidence — every quoted number is exact. Two precision fixes.

| D005 quotes | Source | Verdict |
|---|---|---|
| 0/80 differing rounds | `primary_f9c1.rounds_where_plurality_differs_from_authority_{structured,all_recoverable}` = 0/80 | **exact** |
| Wilson [0.000, 0.0458] round level | `0.045818` | exact (rounded) |
| Wilson [0.000, 0.1611] trial level n=20 | `clustering_caveat.wilson95_0_of_20_trials` = `0.161125` | **exact** |
| 0/80 ties | `tie_frequency_structured` / `_all_recoverable` = 0/80 | exact |
| 20/20 identical sequences | `n_trials_identical_sequence: 20`, `trials_with_differing_action_sequence: []` | exact |
| 0 adversarial flips over all A/B/HOLD imputations of the 14 | `sensitivity_to_unrecoverable_intentions.count_rounds_that_could_flip: 0` | **exact** |
| 14/160 unrecoverable, left un-imputed | `unrecoverable_role_rounds: 14`; `unrecoverable_list` has 14 entries; nulls retained | exact, denominator ambiguous (below) |
| legacy disagreement 6/80 | `legacy_disagreement_field_org_py_160.count: 6`, rate 0.075 | exact |
| `hold_actions` 0.0 in all eight cells | `results/exp001_pilot.json`: A, A0, B, B0, C, C0, D, D0 all mean 0.0 sd 0.0 | **exact, all eight verified** |
| C-005 unanimous A, four roles, four rounds | verified above | exact |
| v1 auditor: `try:` 130, block 131–139, loop opens 141 | `falsify/org.py` lines read directly — `130 try:`, `131 if cell.get("auditor")`, `134–139`, `141 for rnd in range(...)` | **exact, verbatim** |
| PROTOCOL §4 "added to the shared log before the round" | `specs/PROTOCOL.md` §4 | exact; the v1 call site implements it |
| v2 passes subject task text + pre-start status line | `org.py:224–225` (`system_prompt("auditor", task)`, `env.status_line() + " The team is about to begin."`) | **exact** |
| v2 never calls `auditor_view()`; confound is M1-only | `env.py:47`; absent from the v2 path | exact |
| `env.py:53–55` re-briefing / binding | verified: "including {bridge}" at :53–54 | exact |
| `bin/falsify level` on exp008 candidate returns 2 | I ran it: `required_level 2`, `auditor=True outside preregistered [False]` ×2 | **exact** |
| 3×2×35 = 210 trials vs 120 level-1 budget | `critiques/exp008_auditor.md` D.2; `mandate.json` | exact |
| `switched` = 1.0 in B and D so max attainable reduction is 0 | `results/exp001_pilot.json` | exact |

**Finding 4 (precision, fix).** "exp001_pilot-C-005, **the single** invalidating trial that went ADVANCE_A four
times" is one trial too narrow. `results/exp001_pilot_stats.json` `per_trial.A.wasted_actions = [0,0,0,0,4]`:
`exp001_pilot-A-005` also went ADVANCE_A four times. C-005 is the single invalidating **multi-agent** trial.
Insert "multi-agent." Nothing downstream changes, but the claim as written is false as stated.

**Finding 5 (precision, fix).** "14/160 unrecoverable" uses `160` with a different referent than the `160/320` in
the preceding clause: the latter is the planner+executor *structurally recoverable* role-rounds, the former is the
researcher+reviewer *free-text* role-rounds. The memo has the same ambiguity; you inherited it. Write "14 of the
160 free-text role-rounds (8.75%, Wilson [0.0528, 0.1415])".

**The statistician's objection is carried, not buried.** Memo §5: *"Under §K this is inconclusive about the
aggregation rule, not evidence that aggregation rules are equivalent in general … It is evidence that on this
task, with this model, no rule can differ."* D005 `reason`: *"the zero is NARROWER than 'aggregation rules do not
matter' … correlated inputs guarantee correlated outputs, and the zero is a property of the task, not of
aggregation rules."* That is the objection intact, in the same paragraph as the number it limits, and it is made
load-bearing (it is the stated reason for not recording a verdict). The clustering caveat (effective n = 20, not
80) and the unmeasured-tie-break point are both carried too, the latter promoted to defect (iii). This is the
strongest part of the record.

## 6. Confirmatory vs exploratory

Clean. The re-aggregation is labeled EXPLORATORY in the output file's own `_meta.label` and in `findings
.exploratory_label`, which is what `critiques/review_D002.md` §3 required. D005 attaches no confirmatory language
to it, proposes no status, and the three recorded defects are framed as prerequisites for future claims rather
than as findings. The one exception is the C-005 inference — Finding 3.

## 7. The route-field rejection — YOUR LEVEL REASONING IS UPHELD. You are not being over-cautious.

I tried to find the L1 reading and it does not survive contact with the code. A route field on Researcher/Reviewer
is not passive logging:

1. **`prompt_hash()` hashes `SCHEMAS`.** `falsify/org.py:53–56`: `blob = json.dumps([TEAM, DUTIES, SINGLE, AUDITOR,
   SCHEMAS, ...])`. Adding the field changes `prompt_hash()` and therefore breaks comparability with every trial in
   the corpus (`exp001_pilot` is `ccbb34cb3d7e` throughout; so is exp009). That alone defeats "instrumentation."
2. **`SCHEMAS[role]` is the constrained decode format, not a log field.** `org.py:120–121` passes it straight to
   `call_ollama` as the structured-output schema. A *required* route field compels those two roles to commit to a
   route they currently never name — it changes what they emit and plausibly what they deliberate toward. It is an
   intervention on the subject, not an observation of it.
3. **The statistician says so too.** `..._memo.md` §3: a genuine peer/vote arm "requires symmetric schemas — an
   agent-architecture change under §L." `EDGE_CASE_POLICY` §L lists "agent architecture" as a material change.
4. The auditor's I2 warning you invoke ("do not slip it in as instrumentation") is correctly applied.

**Minor correction to your ground, not your conclusion:** the system prompt *text* does not change —
`system_prompt()` (`org.py:47–51`) composes only `TEAM`/`DUTIES`/`SINGLE`/`AUDITOR` plus the task. So "changes
those roles' prompts" is loose. The sound grounds are (1)+(2)+(3) above. L2 stands; if anything it is better
supported than you argued it.

On "leaving a cheap measurement gap open for no reason": for the record, that premise is not quite right either —
the schema change is not the only route to the measurement. A preregistered deterministic text classifier over
role outputs is an analysis-level option (it is what the statistician already did ad hoc, labeled EXPLORATORY) and
would carry a different level. I am not recommending it — that is your call and the designer's — only noting that
"L2 or nothing" is a false choice, so the L2 refusal costs less than you think.

## 8. §F — correct call. Do not edit human policy text yourself.

Upheld, on three grounds:
1. `specs/EDGE_CASE_POLICY.md` opens "Issued by the human researcher." `specs/AUTHORITY.md` assigns policy to the
   Human and gives the PI "scientific decisions within the mandate" — not policy text.
2. §F's defective sentence is an **evidence-wording** claim about an observed result. §L's material-change list
   names "evidence wording after results" explicitly, and AUTHORITY.md's level-3 row is adjacent. A PI silently
   rewriting evidence wording after results at his own authority is close to the center of what this seat exists
   to catch — even when the rewrite is in the conservative direction, as this one is.
3. The defect as you describe it is accurate: `executor_overridden_field_present_in_any_round: false` in the
   re-aggregation output, round keys in all 80 records are exactly `action, agent_outputs, disagreement, env_result,
   round`, and §F's "0 conflicts in 80 multi-agent rounds" is therefore true by recomputation only.

**Finding 6 (small, fix).** Make the defect *reachable* by the human: §N requires deviations and new confounds to be
logged, and the `pi_decision` timeline entry truncates. Add a dedicated `bin/falsify log` entry naming the three
defects and flagging (i) for human correction of §F. Also clarify (i)'s scope: `org.py:160` **does** log
`executor_overridden` in current code, so this is a defect in §F's provenance claim about the *pilot*, not a live
instrumentation gap. As worded, (i) can be read as the latter.

## 9. Novelty language — compliant, nothing to fix

No novelty claim anywhere in D005. Grep for `novel*`, "first to": no hits. The prior-work statements run the other
way — D005 reports that the literature *corrected the PI's* premise ("near-zero uptake is NOT the expected
prior-work result"), which is the opposite of a priority claim. All three cited works exist and are classified:
Weng et al. 2025 (`sources/candidates.md:44`), Cho/Guntuku/Ungar 2025 (`:46`), Yao et al. 2025 (`:47`), all marked
ADJACENT; D005 labels them "all abstract-only," consistent with §J's separation requirement. Correct not to have
used the permitted gap sentences in a decision record until there is a claim to attach them to.

## 10. Conflicts and unresolved objections — none ignored

D005 carries every retraction and objection against its own prior position: the auditor's withdrawal of "0 h build"
(→ 0 h runner + ~1 h analysis, with the `analyze.py` METRICS 26–27 grounds), its retraction of error-independence
as measurable on the current view, the 210-vs-120 budget arithmetic, the statistician's narrowness objection, the
measurement-validity finding that half the vote vector is interpretive, and the literature's correction of the
uptake prior. It also honors the auditor's D.3 instruction verbatim — "choose it explicitly as a deferral; do not
buy it as an action" — and says so. The PI's self-correction of his own dispatch premise, against his own leading
option, is the right behavior and should be noted as such.

**Finding 7 (forward-looking, not a defect in D005).** Two conditions attached to the exp008 proposal are now
parked rather than resolved: the auditor's B.3 "retention, not replacement" condition (`wasted_actions` retained as
a floor-labeled secondary — he states he would call deletion L3) and the §E harm rule hashed before trial 1. They
are not live because D005 defers exp008 entirely, which is correct. Carry them explicitly into whichever decision
revives exp008; do not let the deferral quietly drop them.

---

## Confirmed clean

No status change, no new status label, no registry write, no primary-outcome change, no exclusion change, no
model-population change, no external spend, no novelty claim, no run authorized, data untouched. Level 1 is
correct and nothing level-2 or level-3 is concealed inside it.

## Fixes (all non-blocking; D005 may be acted on as recorded)

1. Add `code_hashes` (`org.py d683a084718f700a`, `env.py 1e894fd234aa68f2`) — D005's content is code claims.
2. Replace "Close the aggregation-rule branch" with "decline to fund now," and state D002's symmetric revival
   condition (any measured non-zero route-intention disagreement reopens it).
3. Re-word the C-005 inference as a single-trial EXPLORATORY observation per §K; it may motivate the funding call
   but may not be cited as evidence about voting, and it cannot be ranked above the measured zero as "argument."
4. "the single invalidating **multi-agent** trial" (A-005 also went ADVANCE_A ×4).
5. "14 of the 160 **free-text** role-rounds (8.75%)".
6. Log the three defects to `timeline.jsonl` addressed to the human (§N), and clarify that defect (i) concerns
   §F's provenance claim about the pilot, not current instrumentation.
