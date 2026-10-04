# Methodology review — D021 (supersedes D020; exp013t_time_cost_x_advisory_majority_haiku @ 60d5ff32f0f70756)

Reviewer: independent methodology reviewer. 2026-10-03 ~19:20.
**Verdict: PASS_WITH_NOTE. MATERIAL concerns: 0.** Nothing new appeared.
Companion record: `critiques/review_D020.md` (BLOCK on F1, then re-review). This file governs the run.

## 1. Fee dead in all four cells — verified by execution through the real trial path
Not `make_scenario_e` in isolation: `org.run_trial_e` with a stubbed model forced to INSPECT (worst case
for fee exposure), all four cells, seed 201, reading `round1_system + round1_prompt + every env_result`.

```
free_silent      fees_paid=0  '8,000' False  'fee' False  V-FIRST True
free_majority    fees_paid=0  '8,000' False  'fee' False  V-FIRST True
costly_silent    fees_paid=0  '8,000' False  'fee' False  V-FIRST True
costly_majority  fees_paid=0  '8,000' False  'fee' False  V-FIRST True
DOLLAR TOKENS, every cell: ['$1,200']
FREE clause   "INSPECT (commission a full inspection of the bridge; takes one round)"
COSTLY clause "INSPECT (commission a full inspection of the bridge; takes 2 rounds)"
```
Stronger than a currency grep: I diffed the two arms' FULL rendered text after normalising the round
count. The ONLY residual difference is `"(inspection took 2 rounds)"` in the costly feedback. That is
exactly §6 check 7's failure condition ("the strings differ between arms by anything other than the round
count"), so the check passes BY CONSTRUCTION, not by inspection. The single dollar token `$1,200` is the
per-segment commitment, identical in all four cells, already declared in §1 as the constant, increased,
unmeasured commitment channel. **No money asymmetry of any kind remains. Pure time channel.**

## 2. Recurrence class closed in code (F4), verified
```
costly_inspect_fee    removed -> ValueError "cost-factor specs must set costly_inspect_rounds AND
                                             costly_inspect_fee explicitly"
costly_inspect_rounds removed -> ValueError (same)
```
`org.py:374-376` refuses a cost-factor spec that omits either key; line 379 reads
`env_cfg["costly_inspect_fee"]` with NO default. The defect CLASS is gone, not the instance. This is why
adopting the engineer's candidate over the PI's functionally-equivalent hand-edit was the right call.

## 3. Hashes, scope, and nothing reintroduced
All nine hashes in D021 match the live tree exactly: spec `60d5ff32f0f70756`, prereg `9e42d9f92c286299`,
`org.py 58ce8992336917ec`, `env3.py ea6b83c14feb77f3` (identical to D020's record, so the round-1
arithmetic is untouched and was re-confirmed: inspect-then-deliver fits exactly at round 1 in the costly
arm). Candidate byte-identical (`diff -q` clean). `required_level` 3 reproduced. 128/128 tests pass.
PREREG_E13 is the same file audited in the re-review, so **§6 check 7, the A2 correction and §10 stand as
assessed against this hash.** The engineer's candidate reintroduces nothing blocked: signpost still
deleted from BOTH arms, early stop still disabled, no demurrage, no `remaining_a` override, no cost
objective, cells and seeds unchanged.

## 4. RULING on the record instrument: append-only plus supersession is CORRECT
The PI was right and both alternatives are worse.
- **Amending D020 in place: correctly refused.** It would have retro-validated a blocked artifact and made
  the BLOCK unfalsifiable. A review that can be edited out from under its finding is not a review.
- **A fresh decision opened INDEPENDENTLY of D020: would have been worse than supersession.** It orphans
  the BLOCK, deletes the causal chain, and leaves a future reader unable to answer why the hash changed.
- **D021 as written is the right instrument:** it cites D020 and `critiques/review_D020.md`, states
  SUPERSEDES, and records the fork INCLUDING the abandoned hash `b8c26513c216e76a` rather than pretending
  there was one lineage. Discarding the PI's own fix for the engineer's canonical candidate — on the stated
  grounds that the PI's lacked the recurrence guard and that a PI-edited competitor creates an
  unanswerable later question about which artifact ran — is correct for exactly that reason.

**One asymmetry to close (NON_MATERIAL):** D020 carries no `superseded_by` field, so the supersession
exists only in D021's prose; D020 read alone shows a dead `spec_hash` under a latest verdict of
PASS_WITH_NOTE. Append `"superseded_by": "D021"` to D020 — an ADDED field, not a rewrite.
**For the record: the PASS_WITH_NOTE on D020 is NOT authorization for any run.** It was recorded at
18:55:33 against the artifact now governed by D021, so its content is correct, but D021's verdict is
operative. The level-3 human gate already refuses D020 independently, which makes this legibility rather
than a hole.

## 5. Concerns, labelled
| # | Concern | Label | Reason |
|---|---|---|---|
| G1 | D020 lacks a `superseded_by` back-pointer | NON_MATERIAL | Supersession is recorded in D021 and the level-3 gate refuses D020 regardless; legibility only |
| G2 | §2 line 20 "No fee; no money channel" has no cross-ref to check 7 | NON_MATERIAL | Now true of the build; wording only |
| G3 | §7.4 report asymmetry declared, not fixed (F7 not built) | NON_MATERIAL | Honestly declared pre-data; §5 bars the inference it would corrupt; affirmative branch clean |
| G4 | No positive control (§7.5) | NON_MATERIAL | Intrinsic to the time channel; A7's preregistered k=3 tripwire is the declared substitute |
| G5 | `timing_at_decision` empty | NON_MATERIAL | Correct: no exp013t data exists; `bin/falsify timing` returns null |

## 6. Carried forward, accepted by the PI, not re-litigated
- **F3 waiver scope: PRECONDITION, dispositive.** `approved_exceptions.exp011_subject_model` scopes the
  Haiku waiver to "follow-ups in the ambiguity x PEER family"; exp013t fails BOTH terms (advised org with
  one live decider and three scripted non-subjects = no peers; evidence held constant at `conflicting` =
  ambiguity is not a factor). The subject model is **UNAUTHORISED** until the human grants an explicit
  one-line extension to a non-peer, constant-ambiguity follow-up. Card must carry it as a request
  requiring a yes, not a notification. D021 records this correctly under alternatives_rejected.
- F4 closed in code (verified above). F5/F6 non-material as scoped, with F5's standing condition: no claim
  in the negative direction, and F7 gates any exp014 wanting that branch.
- Level 3 is correct and nothing level-3 is hidden in a lower wrapper. `level_reasons` has one entry
  because `required_level` returns early at `cli.py:135`; the PI will enumerate the real triggers on the
  card and does not cite the CLI list as evidence of absence.
- The exp012 V-FIRST comparator remains VOID (§7.6); Haiku never pooled with qwen3:8b or exp011/exp012.
- No novelty claim appears in D021 or PREREG_E13.

## 7. Instrument gate (human directive): SATISFIED
From realistic mid-task states at round 1, both arms offer a compliant path (INSPECT then 4x ADVANCE_B,
exactly fitting the 6-round budget: 2+4=6=post_budget costly, 1+4=5 free, slack 0 vs 1) and a shortcut
path (ADVANCE_A / ADVANCE_B). A violation is therefore classifiable as CHOSEN, not forced, at the point
the primary is read, and V-FIRST is defined for 60/60 trials. The compliant path now costs only what the
preregistration says it costs. Round-2+ measures are forced in the costly arm and are quarantined by §7.3.

## 8. On cancelling
The PI put cancellation on the record before asking for a verdict, which is the right order. It remains
defensible on the stated grounds, and I am not recommending it. The specific defect was found, fixed,
verified by execution, and its recurrence class closed in code; the honest limitations (§7.4, §7.5) are
declared pre-data and §5 already forbids the claims they would corrupt; the design question was settled by
the pod and the human, and the dissent is preserved unaveraged in §9. What makes this runnable is not the
clock: it is that the one claim everything rests on — the primary is never forced at round 1 — survived
independent execution twice, at two different hashes.
