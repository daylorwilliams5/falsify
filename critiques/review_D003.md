# Methodology review — D003 (loop 2)

**Decision:** D003 — corrective to D002; withdraws the pre-committed H8/H5a status-transition clause
**Declared level:** 1 **Level correct:** YES (a withdrawal strictly reduces the authority exercised)
**Verdict: CONCERNS** — the corrective is accepted in full and the resource-allocation call is upheld; findings 3–6 are documentation fixes required before the re-aggregation is cited downstream.

---

## 0. My D002 finding 2 was wrong — withdrawn

The PI's correction is accepted and recorded. `results/exp001_pilot_reaggregation.json` (mtime 12:10:59), `_reaggregation.py` and `_memo.md` (12:12:04) were written **after** my filesystem check. My "the artifact does not exist" blocker was a race condition and I withdraw it. The D002 FAIL stands on the three authority findings alone, which is also the PI's own position.

Having now audited the artifact, it exceeds what D002 promised: source sha256 recorded, `source_mutated: false`, 0 model calls, EXPLORATORY in `_meta` and in the memo header, machine-readable `no_hypothesis_status_change_proposed: true`, the HOLD tie-break implemented (`tie_frequency` 0/80), Wilson intervals at round/trial/invalidating-trial level, an explicit clustering caveat, and an adversarial sensitivity analysis over every unrecoverable role-intention showing 0 rounds could flip.

## 1. The withdrawal

Complete and correctly reasoned. D003 voids the clause, concedes all three authority findings in terms that match the documents, creates no status label, applies no status, leaves H3/H5 `untested`, and adopts both of my omissions (HOLD tie-break with `tie_broken` logged; `org.py:161`). I have nothing to add against it.

## 2. "Declining to fund the build" — I attacked it and I uphold it

**The case against (argued at full strength).** The 3–4h build is the only vehicle for testing H8/H5a. Declining it forecloses the test. Recording "the rate is zero, we will not build" carries the epistemic payload of *inert* while shedding the label that would attract review. D003's own phrase — "decision-relevance is preserved WITHOUT any status claim" — is precisely the shape of a laundered verdict.

**Why it fails.**

1. H8's prediction is explicitly **conditional**: "*Conditional on a non-zero within-round route-intention disagreement rate*, mean a_actions is higher under plurality aggregation…". A measured 0/80 leaves the antecedent unmet *in this dataset*. A verdict must generalize; this cannot.
2. The registry is untouched. H8/H5a remain unregistered proposals with no status. The decision leaves no registry trace and retires nothing.
3. `specs/AUTHORITY.md` L1 includes "choose among approved families" and sequencing diagnostics within budget. Allocation among candidate builds *is* the core L1 competence. If declining to spend 3–4h required a reviewer PASS, the PI could sequence nothing.
4. The verdict-shaped move is the one D003 **rejected**: "declare H8/H5a inert on the designer's and auditor's arithmetic alone."

A funding call and a verdict can come apart, and here they demonstrably do. **Do not strip it.**

## 3. CONCERN — reversibility is not stated in D003

The declination is only distinguishable from a verdict if it is scoped and reversible. D002 carried that scoping ("a measured NON-zero would revive H8 as the cheapest live hypothesis"); D003, which supersedes the relevant part of D002, does not restate it.

**Fix:** add an explicit line — the declination is scoped to exp001_pilot's 80 rounds, is reversed by any future non-zero route-intention disagreement rate, and no downstream document may paraphrase it as H8 being inert, dead, falsified or vacuous. Without that line, the distinction I just upheld is unrecorded and will not survive summarization.

## 4. CONCERN — the measured zero is partly structural, and D003 does not say so

The re-aggregation's own §3 reports a measurement-validity finding that qualifies the number the funding call rests on:

- 2 of 4 roles (researcher, reviewer) have **no route field** in their output schema (`falsify/org.py` SCHEMAS:20–23), so their route intention is never structurally recorded.
- 14/160 free-text role-rounds were unrecoverable.
- The two roles that *do* carry structured route fields are planner and executor, already coupled by EDGE_CASE_POLICY §F planner authority.

A disagreement rate measured on an instrument that cannot express the construct for half the roles is not a clean zero — it is adjacent to the §K floor logic the lab itself applied to H1. The statistician handled this honestly (adversarial imputation: 0 rounds flip; dropping both free-text roles leaves planner vs executor agreeing 80/80), which is why this is a CONCERN and not a FAIL.

**Fix:** state in D003 that the zero is conditional on an instrument that structurally cannot record route intention for 2 of 4 roles, and that the adversarial sensitivity analysis is what licenses relying on it.

## 5. CONCERN — provenance points at a FAILED decision

`_meta.authorized_by` reads `decisions/D002.json (PI, Level 1)`. D002's verdict is FAIL. The analysis portion of D002 was and remains legitimately L1 (I ruled the route-intention redefinition not level 2), so the artifact is **not** tainted — but its only authorization pointer is to a failed record.

**Fix:** re-authorize the artifact under D003 and update `_meta.authorized_by`, so no future reader has to reconstruct which half of D002 survived.

## 6. CONCERN — residual `org.py:160` in the artifact

D003 adopts `:161`, but the artifact still carries the old reference in two places: the JSON key `legacy_disagreement_field_org_py_160` and the memo §2 table row "Legacy `disagreement` (`falsify/org.py:160`)". Verified: the expression is at `falsify/org.py:161`; line 160 is `executor_overridden`. Fix both in the artifact, not only in the decision.

## 7. Evidence — recomputed independently

| Quantity | Memo | My recomputation |
|---|---|---|
| Legacy disagreement rounds | 6/80 = 0.075 | 6/80 (D: 5, C: 1, C0: 0, D0: 0) ✓ |
| Route-intention disagreement | 0/80 | 0/80 ✓ |
| Sequences identical | 20/20 | 20/20 ✓ |
| Ties | 0/80 | 0/80 ✓ |

**Unit ambiguity worth fixing.** "`disagreement_rounds` = 1.0 in cell D" is **correct** but is a per-trial *count* (cell D per-trial values `[1,2,1,1,0]`, mean 1.0 rounds/trial), not a proportion; as a rate it is 0.25 of rounds, which is what the memo reports. Stated bare as "1.0" it reads as 100%, and it has been repeated that way since timeline 11:10:03. Always give the unit.

## 8. Confirmatory vs exploratory, novelty, conflicts

EXPLORATORY is carried in `_meta`, the memo header and D003, plus a machine-readable flag. The memo's "I checked rather than assumed, and I did not find the interesting counter-result" is the correct register. No novelty claim. No conflict ignored — D003 engages every finding of `review_D002.md`, including the one it corrects.

Alternatives-rejected: no misrepresentation. The refusal to escalate the clause to L2 as "a rescue vehicle for a clause I should not have written" is the right instinct and I endorse it explicitly.

---

## Required fixes (non-blocking)

1. State the scoping and reversibility of the build declination (§3).
2. Carry the measurement-validity qualification into D003 (§4).
3. Re-authorize the artifact under D003; update `_meta.authorized_by` (§5).
4. Correct `org.py:160` → `:161` inside the artifact and memo (§6).
5. Give the unit whenever `disagreement_rounds = 1.0` is quoted (§7).
