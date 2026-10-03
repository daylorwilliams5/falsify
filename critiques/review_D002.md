# Methodology review — D002 (loop 2)

**Decision:** D002 — zero-model-call F9-C1 offline re-aggregation of the existing exp001_pilot multi-agent transcripts
**Declared level:** 1 **Level correct for the analysis:** YES **Level correct for the decision as written:** NO
**Verdict: FAIL** — narrow and correctable. The analysis itself is level 1 and defensible; a level-2 status transition has been pre-authorized inside it, and the claimed output artifact does not exist.

---

## 1. Authority — BLOCKING

The analysis is level 1: zero model calls, zero trials, zero external spend, no new condition, no new environment, read-only on `data/trials/`. Nothing about *running* it is objectionable.

The problem is this clause in `D002.decision`:

> "if the re-derived action sequence is identical in 20/20 trials and the route-intention disagreement rate is 0, I will record H8/H5a as VACUOUS-not-falsified"

Three independent defects, each sufficient on its own.

**(a) H8 and H5a are not registered hypotheses.** `registry/hypotheses.json` places them under `proposed_loop1`, whose own `status` field reads:

> "PROPOSALS ONLY — not registered hypotheses. Registration and any status transition are gated on the human per EDGE_CASE_POLICY §L. No experiment is assigned to any of these."

The registered set is `hypotheses[]` = H1–H6, M1, P1–P5. None of them is H8 or H5a. A status cannot be transitioned on an object that has no status — so executing the clause necessarily means *registering* them first. And H5a is defined in the registry as a "proposed split of H5", i.e. a re-specification of a registered hypothesis. Registering a split of a registered hypothesis is a registry amendment: level 2 under `specs/AUTHORITY.md` ("new hypothesis family" / protocol amendment), requiring a reviewer PASS. AUTHORITY supersedes §L's *human* gate for routine actions, but it does not downgrade an amendment to level 1.

**(b) "VACUOUS-not-falsified" is not a legal status.** `registry/hypotheses.json.status_labels` = `["untested", "supported", "falsified", "inconclusive", "needs replication"]`. Adding a label is an amendment to the registry schema, not a routine status update.

**(c) The criteria are not preregistered.** Level 1 authorizes a "Status update when **preregistered criteria** are met" (`specs/AUTHORITY.md`, levels table). These criteria were written for the first time in D002 itself, in the same record that commissions the analysis, after the exp001 results already existed and after two specialists had publicly predicted the answer is exactly zero. Pre-commitment inside the decision that will consume it is not preregistration; it is self-certification. The honesty of writing the rule down in advance is real and worth credit — it is just not the same instrument.

**Fix:** either strike the status-transition clause and re-record D002 as evidence-gathering only, or file a separate level-2 decision to register H8/H5a and to extend `status_labels`, obtain a reviewer PASS, and only then apply a status. Do not apply any status to H8/H5a on the strength of D002 as written.

## 2. Evidence — BLOCKING

D002 is reported as already acted on, but the output does not exist.

- `results/` contains only `exp001_pilot.json`, `exp001_pilot_stats.json`, `exp001_pilot_wasted.png`. **`results/exp001_pilot_reaggregation.json` is absent.**
- `timeline.jsonl` has no `analysis_written` entry — or any entry at all — after the D002 `pi_decision` at 2026-10-03T12:06:38. EDGE_CASE_POLICY §N requires results and deviations to be logged.

There is therefore no artifact to audit. I cannot verify the route-intention disagreement rate, the count of the 80 rounds that the plurality rule would resolve differently, the tie frequency, or the vote vectors. **No claim derived from this analysis may be cited until the file and a timeline entry exist.**

Positive finding: `data/trials/exp001_pilot.jsonl` is unmodified and `data/trials/` shows no write. The read-only commitment appears honored.

## 3. The analysis-definition challenge — I side with the PI, with conditions

The PI asked me to argue the other side of "is redefining *disagreement* over route intentions a new analysis definition requiring preregistration, i.e. level 2?" I argued it and it does not hold up as a level escalation.

Against level 2 / level 3:

- `disagreement_rounds` is **not a primary outcome**. `specs/PREREG_V2.md:32` lists it under "Secondary and descriptive"; `specs/exp005_evidence_x_org.json:25` likewise lists it as secondary. So this is not a level-3 "primary-outcome change after results exist."
- The recorded field is verifiably an artifact. `falsify/org.py:161`: `"disagreement": (len(set(recs)) > 1 or mismatch) if org != "single" else None` — a disjunction over the CONTINUE/REPLAN recommendation token OR `plan != action`. That is exactly what `critiques/exp001_pilot_skeptic.md` §1.4 describes, and it produced `disagreement_rounds = 1.0` in cell D while all four roles argued for the same route.
- The redefinition was specified by a specialist *before* this decision: `critiques/loop1_auditor.md:289-290` (C7) — "Rotation cannot be evaluated until `disagreement` is redefined over **route intentions**… That redefinition is a cheap prerequisite worth doing." It is not PI-invented post-hoc convenience.
- Keeping the old field would, as D002 argues, *overstate* disagreement and manufacture a live-looking H8. The redefinition is the conservative direction.

Still true, and binding:

It remains a new, non-preregistered analysis definition created after behavioral results exist. Conditions: label EXPLORATORY **in the output file itself**, not only in the decision record; report the original `disagreement_rounds` alongside the new measure in `results/exp001_pilot_reaggregation.json` so the two are comparable; attach no confirmatory language to either.

D002's EXPLORATORY label is correct and sufficient *for the analysis*. It is the decision rule stacked on top (§1) that converts an acceptable exploratory diagnostic into an authority violation.

## 4. Confirmatory vs exploratory

The analysis is correctly marked EXPLORATORY, and D002 correctly holds that "H3 and H5 stay 'untested' either way, since this analysis manipulates nothing." That matches the scientist's 11:43:21 finding that H3/H5's IV never varied (0 conflicts in 80 multi rounds).

But the same logic condemns the H8/H5a clause. H8's registered-as-proposed prediction is itself explicitly conditional: "**Conditional on a non-zero within-round route-intention disagreement rate**, mean a_actions is higher under plurality aggregation…". A conditional whose antecedent is unmet yields no verdict at all — it leaves the hypothesis untested. `untested` is already a legal label and is the honest one. Inventing `VACUOUS-not-falsified` adds a connotation ("we checked and it held up in a degenerate way") that a zero-variance IV cannot support.

## 5. Quotation accuracy

Everything checkable checks out:

| Claim | Source | Verdict |
|---|---|---|
| "0 conflicts in 80 multi-agent rounds" | timeline 11:35:32, 11:43:21; `critiques/loop1_design.md:23-26` | exact |
| 20 multi-agent transcripts | exp001_pilot n=40 across single+multi | consistent |
| `disagreement_rounds=1.0` in cell D vs `wasted_actions=0.0` | timeline 11:10:03; `critiques/loop1_auditor.md:287-288` | exact |
| org.py disagreement = recommendation-set difference OR plan!=action | verified in source | exact |

**Minor:** D002 cites `org.py:160` for the disagreement field; the expression is at `falsify/org.py:161` (line 160 is `executor_overridden`). Correct the citation.

## 6. Novelty language

No novelty claim in D002. Compliant.

## 7. Conflicts and unresolved objections

None ignored. D002 engages the skeptic's F9-C1 inertness claim and the auditor's C7 head-on. Its rationale for measuring rather than assuming the zero —

> "an assumed-zero kills a branch on an unverified arithmetic claim, whereas a measured zero kills it on evidence, and a measured NON-zero would revive H8 as the cheapest live hypothesis"

— is methodologically sound and the strongest part of the record. The decision to spend zero resources confirming a prediction two specialists agree on, rather than retiring a branch on inference, is exactly right.

## 8. Alternatives-rejected: specialist record

No misrepresentation found.

- `critiques/loop1_design.md:23-26` does say the manipulation is inert and is "checkable for free by re-aggregating existing logs (F9-C1, 0.5 h, 0 model calls; do this instead of the 6 h build)".
- `critiques/loop1_auditor.md:278-282` does name the offline re-aggregation as the free precursor, does specify read-only on `data/trials/exp001_pilot.jsonl`, and does say "If it is, the build is not worth 3–4 h." D002's quotation is accurate and in context.
- The rejection of `disagreement_rounds` as the measure accurately reproduces `critiques/exp001_pilot_skeptic.md` §1.4.

**One omission.** The auditor at :281-282 also requires: "If the tie-break is ever reached, it must break to **HOLD** with `tie_broken` logged." D002 reports tie *frequency* but does not adopt the HOLD tie-break rule. Adopt it in the re-aggregation, or state why not — otherwise the re-derived action sequence under ties is undefined and the "identical in 20/20" criterion is not well-formed.

---

## Confirmed clean

No primary-outcome change, no exclusion change, no model-population change, no external spend, no novelty claim, and no *executed* status transition in D002.

## Required before acting further

1. Strike or re-authorize (level 2, reviewer PASS) the pre-committed H8/H5a status transition and the `VACUOUS-not-falsified` label.
2. Produce `results/exp001_pilot_reaggregation.json` and log it to `timeline.jsonl`; until then cite nothing from it.
3. Report `disagreement_rounds` alongside the route-intention measure; mark EXPLORATORY inside the file.
4. Adopt the auditor's HOLD tie-break rule with `tie_broken` logged, or justify its omission.
5. Fix the `org.py:160` → `org.py:161` citation.
