# Methodology review — D001 (loop 2)

**Decision:** D001 — run `specs/exp009_v2_floor_probe.json` (20 trials, 4 frozen v2 cells, seeds 1–5, qwen3:8b)
**Declared level:** 1 **Computed level:** 1 **Level correct:** YES
**Verdict: CONCERNS** — no violation requiring the in-flight run to be stopped; three fixes required before the results are interpreted.

---

## 1. Authority

Level 1 is correct, and correct independently of the CLI.

- `bin/falsify level specs/exp009_v2_floor_probe.json` → `required_level 1`, reasons "inside preregistered condition space, mandated model, within level-1 budget" and "human-approved spec".
- Independent check: all four cells are the frozen `specs/PREREG_V2.md` cells (budget 24/10 × ordinary/target, `auditor: false`, `org: single`); model is the mandated `ollama/qwen3:8b` (`lab/mandate.json.subject_model`); 20 trials and ~230–340 calls sit far under the level-1 budgets of 120 trials / 4000 calls; environment family `freightroute_v2` is in `approved_environment_families`.
- `spec_hash` `e4d5f3d91f2df2f1` recorded in `D001.json` matches the on-disk spec (recomputed).
- Human approval exists at `timeline.jsonl` 2026-10-03T11:48:56 and in `lab/mandate.json.approved_specs`.

**No hidden level-3 content.** No primary-outcome change, no exclusion change, no non-subject model, no external spend, no novelty claim, no status transition.

### Does the 11:48:56 approval cover what was launched?

Yes, element by element. The approval reads "single-agent, 4 frozen v2 cells, budget 24 vs 10, ordinary vs target, seeds 1-5, qwen3:8b, no API cost" — this is exactly the launched spec. `data/exp009_v2_floor_probe.log` confirms the running job declares `spec e4d5f3d91f2df2f1`, and pid 11816 was verified live running `python -m falsify.run specs/exp009_v2_floor_probe.json`.

### Is the env2.py hash change a level-2 protocol amendment?

**No — but the decision record hides it.** I pushed on this and it survives:

- `specs/PREREG_V2.md:3` does not forbid environment change; it requires that any change "be logged in `timeline.jsonl` with a reason, and results from before and after the change are reported separately." Logged at 11:48:56 under `stage: protocol_deviation` with a reason, per EDGE_CASE_POLICY §N.
- The change is named *inside the approved, hash-locked spec* (`requires_build` F15-C) and justified in `env_freeze_note`. The human approved "exp009 instrumentation build + 20-trial v2 floor probe" — the build was explicitly in scope.
- No model-generated v2 trial existed, so the "before/after reported separately" clause has an empty "before". This is the one configuration in which instrumenting a frozen environment is not a data-splitting amendment.
- It changes measurement, not manipulation, prompts, scoring or exclusions, so it is not a level-2 "protocol amendment" in the AUTHORITY sense and not a level-3 "primary-outcome change after results".

**CONCERN (fix required).** `D001.json` records `spec_hash` but no `env_hash`, and nowhere mentions `3acdf7bbbc1e2d94 → 0d36c8bbb3e4c339` or the protocol_deviation entry. The AUTHORITY integrity control ("a decision records the spec's hash") is satisfied for the spec while the frozen artifact that actually changed is invisible in the record. Current on-disk env2.py hash verified as `0d36c8bbb3e4c339`.
**Fix 1:** append the env hash and a pointer to the 11:48:56 protocol_deviation entry to D001 and to `results/exp009_v2_floor_probe.json`.

### New finding — scope creep inside the approved build

The spec's `requires_build` names `compliance_was_feasible` (agent-knowledge feasibility), `bad_index`, and first-route choice. The shipped instrumentation (timeline 11:48:56) *also* adds `process_violation_feasible_truth` (ground-truth feasibility) and per-reserve `compliance_feasible_known/truth` — a **second feasibility operationalization that is not in the approved, hash-locked spec**.

It is measurement-only, pre-data and descriptive, so it is not a level-2 amendment. But two rival feasibility definitions now exist and nothing commits the lab to one before the 20 trials are read. That is a live analytic degree of freedom.
**Fix 2:** declare now, before any result is read, that `process_violation_feasible` (agent-knowledge) is *the* reported decomposition and `_truth` is a robustness check. Log it.

## 2. Preregistration

The run is preregistered: the condition space is PREREG_V2's frozen cells, the spec is locked (`git tag exp009-locked`), and the reading rules (case A floor / case B forced-dominated / case C feasible) are written in the spec before the first trial. Nothing was altered after seeing behavioral results, because there are no v2 behavioral results.

**Descriptive-only constraint: HONORED.** The human's 11:48:56 condition — "Primary outcomes unchanged; feasible/forced split DESCRIPTIVE only; `process_violations_feasible` NOT promoted to primary" — is carried correctly in `D001.decision` ("PREREG_V2 primary outcomes unchanged, feasible/forced decomposition reported as DESCRIPTIVE") and matches the spec's `primary_outcome` field and `materially_new_under_policy_L` item 3, which itself pre-flags that promoting `process_violations_feasible` to primary later would be a material change needing approval *before* that run, "never after seeing these 20 trials."

Accuracy note: this constraint lives in `timeline.jsonl` 11:48:56 and in the spec. It is **not** in `lab/mandate.json`, which contains no such clause. Anyone relying on the mandate alone would not find it.

**CONCERN.** D001 omits the rest of the same authorization: "After exp009: Statistician → Skeptic → Designer → Director; pause for approval before any full v2 or materially changed experiment."
**Fix 3:** record that sequencing condition so the next decision cannot silently skip it.

## 3. Evidence

Every quoted number checks out, exactly:

| Claim in D001 | Source | Verdict |
|---|---|---|
| `wasted_actions=0` in 18/20 invalidating trials | timeline 11:10:03 (statistician) | exact |
| two non-zero trials A-005, C-005, one seed (5) | `critiques/exp001_pilot_skeptic.md` §1.1, lines 22–32 | exact |
| route-attribution failures, not persistence | same, plus timeline 11:14:57 | exact |
| instrumentation "built and tested (19/19)" | timeline 11:48:56 engineer | exact |
| env2.py:64, :90-92, :87; tests/test_env2.py:42-48, 56-65 | spec `code_verification_by_designer`; independently re-verified timeline 11:40:05 | exact |
| `exp008_auditor_m1.json` → required_level 2 | re-run by me: returns 2, reason "auditor=True outside preregistered [False]" | exact |

No mechanism is inferred from the two seed-5 trials — D001 explicitly treats them as the skeptic's attribution failures, which is the EDGE_CASE_POLICY §K-compliant reading. No claim rests on a floored cell; the *point* of the decision is that the cells are floored.

## 4. Confirmatory vs exploratory

Clean. The spec states "this spec makes NO hypothesis verdict" and "Descriptive only, no bootstrap verdicts". D001 repeats both. The read-out rules are pre-committed, so the case A/B/C classification cannot be chosen after the fact. §K's floor→INCONCLUSIVE rule is explicitly invoked in the spec's `analysis` field.

## 5. Novelty language

No novelty claim of any kind appears in D001. Compliant.

## 6. Conflicts and unresolved objections

None ignored. D001 engages the skeptic's F15/F16, the auditor's two code defects, the designer's self-withdrawal of exp005, and the designer's downgrade of exp003 — all accurately.

## 7. Alternatives-rejected: specialist record

No misrepresentation found.

- "I1 … critiques/loop1_auditor.md rank 1" — correct (§3 ranking table, rank 1).
- "bin/falsify level … returns required_level 2" — reproduced exactly.
- org.py:222-229 and env.py:53-55 defects are the auditor's own (timeline 11:45:56), independently confirmed by the director the same minute.
- exp005 withdrawal is the designer's own (timeline 11:40:05; `critiques/loop1_design.md:21-23`).
- exp003 arithmetic rejection matches `critiques/loop1_design.md:26-27`.
- "rejected as a substitute, not on merit" is a fair and unusually honest characterization of I1.

**One wording caution.** D001 says exp009 is "the only approved action that can produce a non-floored phenomenon." True only on the word *approved* — the auditor's §3 table marks I1 "No — survives the floor", i.e. I1 is also non-floor-limited; it is merely unapproved and level 2. Recommend rewording so the record does not imply I1 is floor-limited.

---

## Required fixes (non-blocking for the run, blocking for interpretation)

1. Record the env hash `0d36c8bbb3e4c339` and the 11:48:56 protocol_deviation reference in D001 and in the exp009 results file.
2. Commit, before reading results, to `process_violation_feasible` (agent-knowledge) as the single reported decomposition, `_truth` as robustness only.
3. Record the human's post-exp009 sequencing and pause condition.
4. Reword the "only approved action" claim per §7.
