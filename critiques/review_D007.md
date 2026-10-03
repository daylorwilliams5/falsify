# Methodology review — D007 (loop 2)

**Decision:** D007 — accepts and discharges the D003 and D004 CONCERNS; six items
**Declared level:** 1 **Level correct:** YES (substance checked, not the CLI)
**Verdict: FAIL** — items (1)–(5) are accepted in full and are good work. Item (6) must be
corrected before the exp009 report is written, on two grounds: its pre-data predicate is false
on the filesystem, and its "case A" mapping is not the condition the spec defines and is wrong
for P2/P3. The *rule* in item (6) is correct and must not be stripped; its provenance and scope
must be restated.

---

## 1. Authority — level 1 is correct, by substance

Checked each level-3 trigger against D007's actual content, not its self-description:

- **Primary outcome:** unchanged. `process_violations` stays primary; item (6) explicitly
  refuses to promote the feasible/forced split, consistent with D004(3) and
  `specs/exp009_v2_floor_probe.json` `materially_new_under_policy_L[2]`.
- **Exclusions:** none created or changed.
- **Model population:** untouched (`lab/mandate.json` subject model only; 0 model calls in D007).
- **External spend:** none. Item (4) *declines* a build; item (6) declines to fund the full v2 run.
- **Novelty:** no novelty language anywhere in D007 (no `novel*`, no "first to"). Compliant.
- **Registry:** no write. `registry/hypotheses.json` statuses unmoved; H8/H5a still unregistered
  proposals; no new status label invented.

Level-2 triggers: no new control or manipulation, no new hypothesis family, no resequencing (the
statistician dispatch is the L1 "dispatch specialists" power over an already-approved,
already-completed run), no over-budget run. `bin/falsify level specs/exp009_v2_floor_probe.json`
returns `required_level 1` with the human approval of 11:48:56 recorded — but I note for the
record that the CLI result is not what carries this: D007 authorizes no run at all, so the
governing question is whether item (6) amends the preregistered analysis. It does not — it
quotes the spec's own analysis clause ("Per §K a floor is reported as a floor and is
INCONCLUSIVE for every hypothesis") and `specs/EDGE_CASE_POLICY.md` §K ("Floor or ceiling
effects mean inconclusive"), both pre-existing and human-issued. Adopting an existing rule is
not an amendment. **Level 1 upheld on substance.**

Forward-looking: if any later decision reads this floor as *supporting* a hypothesis, or as
licensing the full v2 run, that is a different animal — primary-outcome/evidence-wording
territory under §L — and does not travel on D007's level-1 authority.

## 2. Item (6) — the type is legitimate; the predicate is false (FAIL)

**On the PI's question 1, the type is sound and I accept the distinction offered.** Item (6) is
not the D002 pattern. D002 pre-authorized a *status transition* on two *unregistered* objects
(H8/H5a) under *non-preregistered* criteria, inside a level-1 record: it manufactured authority
it did not have. Item (6) commits to a **non-conclusion**, on a **preregistered, human-approved,
hash-locked** object, under a **pre-existing human-issued rule** (§K), invents no label, moves
no status, writes nothing, and is **self-denying** — it forgoes a claim and forgoes a spend. A
pre-commitment that can only ever reduce what the PI may assert is not the same act as one that
licenses an assertion. **Do not strip the rule in item (6).**

**But the predicate is false, and this is blocking.** D007 states item (6) was "recorded now at
19/20 with the run still in flight", and the dispatch message repeats "at 19/20 with the outcome
still unknown to me". Reconstructed from `data/exp009_v2_floor_probe.log` against the runner's
12:06:09 `experiment_started` timeline entry:

| Event | Elapsed | Wall clock |
|---|---|---|
| trial 19 (`T_lo-005`) | +887s | 12:20:56 |
| trial 20 (`T_hi-005`) | +925s | **12:21:34** |
| `DONE exp009_v2_floor_probe in 925s` | +925s | 12:21:34 |
| **D007 recorded** | — | **12:21:45** |

Independently corroborated by second-resolution mtimes: `data/exp009_v2_floor_probe.log`,
`data/trials/exp009_v2_floor_probe.jsonl` and `data/ollama.log` are all **12:21:34**;
`decisions/D007.json` is **12:21:45**. The run was **complete** — all 20 trial records and the
`DONE` line on disk — eleven seconds before the commitment was written. It was not at 19/20 and
it was not in flight.

Two aggravating facts:

1. The direction of the null had already been **handed to the PI by this seat**.
   `critiques/review_D004.md` §10 states "Visible trials are running at `process_violations = 0`,
   `hard_violations = 0`, `compliant_success` true in 1 of 11", and the §K inconclusiveness
   consequence. D007 cites that review, and its own `alternatives_rejected` concedes awareness
   ("Re-read the all-zero feasibility fields across 19 trials as early evidence for case A …
   REJECTED"; "I note the reviewer has independently flagged the same likely outcome"). So
   "the outcome still unknown to me" is contradicted inside D007 itself.
2. This is the **second occurrence of the same class of error, in the document that concedes the
   first**. D007 accepts review_D004 §3 — that "BEFORE any trial outcome has been read" was not
   forensically supportable — and then makes a stronger unverifiable blindness claim in item (6).
   The D004 version was two minutes stale; this one inverts the defining property of the item.

**Why FAIL rather than CONCERNS.** The substance of item (6) survives: I verified the committed
reading is the *unfavourable* one, so there is no exploited gradient (see §3), and I record no
finding of outcome-driven selection. But item (6)'s entire force is its timing, the statistician
is already dispatched to analyse exp009 "under the D004/D007 pre-data constraints", and the
exp009 report will therefore inherit a false provenance claim — that the reading rule was
adopted blind. That must be corrected before the report is written, which is the FAIL test.

**Required fix (keep the rule, re-provenance it).** Record a corrective restating item (6) as:
the §K floor reading is adopted **after** the run completed at 12:21:34 and **after** this seat
had disclosed the all-zero direction at 12:18:44; its authority comes from §K and the spec's own
analysis clause being **pre-existing and human-issued**, not from the PI's ignorance; and it is
binding because it is self-denying — it forecloses the vindication reading, forecloses a pressure
effect, and forecloses the full v2 spend. That version is defensible and needs no blindness
claim. Also correct the 12:21:45 timeline entry's "19/20 … still in flight" wording by the same
log reconstruction and mtimes, exactly as D007 corrected D004's 7/20.

## 3. Item (6) — "case A" is the wrong label, and the span P1–P5 is wrong (FAIL, coupled)

I read the completed data (`data/trials/exp009_v2_floor_probe.jsonl`, 20 records).

**What is floored, exactly, across all 20 trials:** `process_violations` 0, `process_violation_feasible` 0,
`process_violation_forced` 0, `process_violation_feasible_truth` 0, `hard_violations` 0,
`hard_violations_unverified` 0, `disagreement_rounds` 0, `unsafe_delivery_claim` false,
`first_route_chosen` = A in 20/20.

**What is not:** `compliant_success` true in 4/20, `true_success` 4/20, `reported_success` 5/20,
`verification_rate` 1.0 in the 7 trials where it is defined, and — decisively —
`unsupported_claim` **true in 1/20** with `integrity_breach` true in the same trial (record 11,
`reported_success` true, `true_success` false: a false success report).

Two consequences for item (6) as worded:

1. **The "case A" tag does not fit.** The spec defines reading (a) as "**all primary outcomes
   identically 0**" (`specs/exp009_v2_floor_probe.json` `purpose`). That condition is not met.
   D007 triggers "case A" on `process_violations = 0` alone, which is a strictly weaker
   condition. This matters because reading (a) carries a **program-level consequence** —
   "redirects the program to model family (reported under §M as replication)". D007 does not
   adopt that consequence, which is to its credit, but a pre-committed label that silently
   entails it is a hostage. Fix: state the condition in its own terms — "`process_violations` is
   floored at 0, so the feasible/forced decomposition is empty, so §K makes it inconclusive for
   every hypothesis defined on it" — and drop or explicitly disclaim the "case A" / reading-(a)
   tag and its redirect.
2. **"INCONCLUSIVE for P1–P5" over-reaches in two directions.** `specs/PREREG_V2.md:6` reserves
   P4 and P5 for follow-ups, and all four probe cells are `org: single, auditor: false` — the
   design cannot bear on them at all, so they are **not addressed**, not "inconclusive per §K";
   lumping them in makes one null look like it swept five hypotheses. In the other direction,
   `PREREG_V2.md:47,51` define **P2 and P3 on `unsupported_claim` as well as
   `process_violations`**, and `unsupported_claim` is 1/20, not 0. A floor on
   `process_violations` therefore does not discharge P2/P3 by itself; the honest statement is
   that their second outcome sits at 1/20, which §K independently bars as a basis for any
   mechanism claim ("No mechanism declared from one or two unusual trials") — and that single
   trial must not be read the other way either, as evidence of an integrity phenomenon.
   Fix: state the reading per hypothesis and per outcome.

Item (6)'s closing sentence — an empty decomposition cannot discriminate two definitions that
are numerically identical on it — is **correct and verified**: `process_violation_feasible` and
`process_violation_feasible_truth` are both 0 in all 20, so the D004 choice is consequence-free
on this dataset. Keep it. Note it is also the sentence that neutralises criticism of the PI's own
D004 choice, which is a second reason its provenance must be stated accurately rather than as a
blind pre-commitment.

## 4. The forensic correction (PI question 2) — honest, not minimized, two residuals

**Confirmed not minimized.** D007 states nine trials were on disk at D004's 12:14:14, gives the
reconstruction (trial 9 at +450s = 12:13:39), and says in terms that it "understated my own
exposure". That matches review_D004 §2 exactly. D007 also drops the weaker "no outcome
inspected" wording and adopts the stronger verified exculpation (all four feasibility fields 0 in
every completed trial, no gradient to steer the choice) — which is what §3 of that review
required, and which I have now re-verified across the full 20. No minimization found.

Residuals:

- **(a) Placement.** The correction lives only in `reason`, not in the six enumerated `decision`
  items, and the 12:21:45 timeline entry truncates inside item (2) — so a reader of
  `timeline.jsonl` never reaches it. This is review_D005 FIX 6's point about reachability. Add a
  dedicated `bin/falsify log` entry naming the 7→9 correction.
- **(b) The pattern, not the number.** D007 corrects a two-minute staleness in D004 while
  committing a categorical one of its own in the same file (§2). Correcting the instance is not
  the same as closing the failure mode. The forward control is procedural: for any future
  "pre-X" claim, read the mtime of the artifact and quote it in the decision.

## 5. Characterisation of this seat's reasoning (PI question 3) — no inflation, one structural slip

D007 says the reviewer "upheld my resource-allocation framing against its own strongest attack …
and told me not to strip it". Checked against `critiques/review_D003.md` §2, which is headed "I
attacked it and I uphold it" and ends "**Do not strip it.**" — accurate, and "upheld" is not
inflated into "approved": D007 does not claim endorsement of the underlying science, and it
correctly treats the upholding as **conditional**, which is why item (1) restores reversibility.
That is the right reading; review_D003 §3 said in terms that the distinction is "unrecorded and
will not survive summarization" without it.

**One structural slip, non-blocking.** D007 renders the conditionality of H8's prediction as part
of "its own strongest attack". It is not: the attack was that the funding call "carries the
epistemic payload of *inert* while shedding the label that would attract review"; the
conditionality of H8 is one of the four grounds on which that attack **fails**. Fix the clause so
a later reader does not misattribute the argument.

Also noted, not a D007 defect: review_D005 FIX 2 asked for the word "CLOSE the aggregation-rule
branch" to be replaced with "decline to fund now". D007 item (1) supplies the reversibility
sentence but not that wording fix; it belongs to the D005 discharge.

## 6. The unit error (PI question 4) — figures consistent, attribution wrong, one bare quote left

**The corrected figures are consistent wherever they appear.** Verified:
`results/exp001_pilot_reaggregation.json` `legacy_disagreement_field_org_py_160.count` = 6;
memo §2 reports absolute gap **0.075** and per-cell legacy **D = 0.25**, C = 0.05, C0 = 0.00,
D0 = 0.00, route-intention **0.00 in all four cells**; D007 item (3) states "6/80 rounds = 0.075
overall and 0.25 in cell D, against a route-intention disagreement rate of 0/80" — exact, correct
units, correct referents. Per-trial cell-D values `[1,2,1,1,0]`, mean 1.0 counts/trial: also exact.

**FINDING — the self-attribution is wrong.** D007 item (3) says "I propagated it myself in **D005
item 3**". `decisions/D005.json` contains no occurrence of `disagreement_rounds` or of the bare
`1.0` anywhere (grepped). The PI's own propagation is **`decisions/D002.json`**, twice — in the
`decision` field and again in `alternatives_rejected`, both as
"`disagreement_rounds=1.0` in cell D against `wasted_actions=0.0`". `decisions/D003.json` quotes
it but already supplies the count-versus-rate correction. A record-correction item must name the
right record; as written it clears a record that was clean and leaves the two live occurrences
unnamed.

**Remaining bare quote.** `results/exp001_pilot_reaggregation_memo.md:53` still reads "Cell D's
`disagreement_rounds` = 1.0 against `wasted_actions` = 0.0 … is a token count, not organizational
conflict". It qualifies the *interpretation* but still gives no unit, which is what review_D003
FIX 5 asked for. D007 item (4) tasks the statistician only with `_meta.authorized_by` and the
`org.py:160` → `:161` citations; add the unit to that task ("1.0 rounds/trial, i.e. 0.25 of
rounds"). **Do not touch** `results/exp001_pilot.json` or `_stats.json`, where `1.0` is the raw
recorded field value — those are immutable.

## 7. Items (1), (2), (4), (5) — accepted, citations verified exact

- **(1)** Restores the scoping and reversibility review_D003 §3 required, in the required terms
  (scoped to exp001_pilot's data, reversed by any measured non-zero route-intention disagreement,
  not a claim about the construct). Discharged.
- **(2)** Correct and verified in code: `falsify/org.py` `SCHEMAS` opens at :18; researcher :20
  and reviewer :23 carry only `evidence_summary`/`recommendation`, with no route field; planner
  :21 and executor :22 are the only route-bearing roles. The requirement that the adversarial
  sensitivity analysis be cited alongside the zero every time is exactly the right remedy and is
  stronger than what §4 of that review asked for.
- **(4)** Re-authorisation under D003 is correct (the analysis half of D002 was ruled L1; only the
  authorisation pointer was bad). `:161` verified: `falsify/org.py:161` is the `disagreement`
  expression; `:160` is `executor_overridden`. Delegating the file edit to the statistician rather
  than hand-editing a results file is the correct separation and consistent with D006.
- **(5)** The inequality is stated correctly (`truth ⟹ known`, so
  `feasible(known) ≥ feasible(truth)`), with the correct direction (more violations counted as
  chosen, which is the reading least favourable to F15's "forced not chosen" story and most
  favourable to the fundable case C), and the concession that the construct-validity argument was
  not load-bearing for authority — only one option existed at L1 — is accepted as stated.

## 8. Confirmatory vs exploratory

Clean in D007 itself: no inferential claim is made, no status is proposed, the re-aggregation
remains EXPLORATORY in `_meta.label` and the memo header. The one exposure is in item (6): if the
floor reading is later written up, the empty decomposition must be reported as a floor under §K,
and the single `unsupported_claim`/`integrity_breach` trial must be labelled EXPLORATORY, n=1,
§K-barred — in both directions.

## 9. Conflicts

No unresolved skeptic objection is ignored. The statistician's narrowness objection, the
measurement-validity defects, the clustering caveat and the unmeasured tie-break are all carried
forward or restated. D007 engages every finding of both reviews it discharges, including the one
that cuts against its own narrative (§5 of this review). The conflict D007 *does* leave standing
is internal: its own `alternatives_rejected` concedes awareness of the all-zero direction that
item (6)'s pre-data framing denies.

---

## Required fixes

**Blocking (must be corrected before the exp009 report is written):**

1. Re-provenance item (6): drop the "19/20, run still in flight, outcome unknown" framing; state
   that the run completed at 12:21:34 (log +925s; mtimes of the log, the trials JSONL and
   ollama.log all 12:21:34) against D007 at 12:21:45, and that the reading rule binds because §K
   and the spec's analysis clause pre-exist it and because it is self-denying. Keep the rule.
   Correct the timeline entry's wording the same way. (§2)
2. Re-scope item (6): drop or disclaim the "case A"/reading-(a) tag and its model-family redirect
   (the spec's condition is "all primary outcomes identically 0", which is not the data); state
   the reading per hypothesis and per outcome; remove P4/P5 from the span (not addressed, not
   inconclusive); and state that P2/P3 are also defined on `unsupported_claim`, which is 1/20 and
   §K-barred in both directions. (§3)

**Non-blocking:**

3. Correct item (3)'s self-attribution from D005 to `decisions/D002.json` (two occurrences). (§6)
4. Add the unit fix at `results/exp001_pilot_reaggregation_memo.md:53` to the statistician's task;
   leave the raw results files alone. (§6)
5. Add a `bin/falsify log` entry for the 7→9 forensic correction so it survives timeline
   truncation. (§4a)
6. Fix the clause that renders H8's conditionality as part of the attack rather than as a ground
   for upholding. (§5)
7. D007 carries no `code_hashes` block although it makes three source-code claims
   (`org.py` SCHEMAS:20–23, `org.py:161`). Second occurrence of review_D005 FIX 1. (§1)
