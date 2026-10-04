# Methodology review — D017 (FOURTH PASS)

**Verdict: PASS_WITH_NOTE — 0 MATERIAL. The exp012 main run is authorized.**

Reviewer: methodology_reviewer. Fourth pass, re-tested rather than assumed: the PI's brief was
treated as unverified, as instructed. Two prior briefs contained errors; this one did not, but every
claim in it was independently recomputed before being accepted.

## Verdict history
1. 16:53:47 ESCALATE (4 MATERIAL) → 2. ESCALATE → 3. 17:06:39 ESCALATE (4 MATERIAL) →
4. **PASS_WITH_NOTE (0 MATERIAL)**

The third pass stated that with M3/M6/N1 landed and §M resolved by the human, the correct fourth-pass
verdict would be PASS_WITH_NOTE at 0 MATERIAL. That prediction was re-checked, not honoured: all three
remediations are verified on disk, §M is waived by the human in the logged record, and the one way the
prediction could have failed (regression of the M1(b) claim-boundary emission under the analyze.py
hash drift) was explicitly tested and did not occur.

## Automatic checks
`decision_recorded_before_action` true · `spec_hash_verified` true · `budget_compliant` true ·
`level_correct` true · `model_within_mandate` **false** · `code_unchanged_since_decision` **false** ·
`inside_preregistered_condition_space` **false**

The three false flags are the known, disclosed level-3 drivers, not new defects:
model population outside the mandated qwen3:8b subject (the precise thing the human card and the §M
waiver authorize), reviewer-mandated analysis-code remediation landing after the decision was
recorded (note n5), and declarative spec keys outside a hash-matched mandate entry (note n6).
None is a concealed violation; each is on the face of the record.

## The six questions

**1. Authority — level 3, correctly declared.** `bin/falsify level` reproduces required_level 3
(model anthropic/claude-haiku-4-5 vs mandated ollama/qwen3:8b). D017 declares level 3,
`escalation_required` true, `human_approval` present at 16:56:26. Nothing level-3 is hidden in a
lower-level decision: the PREREG_E amendment is level 2 on the grounds ruled at 17:05:23 — it removes
interpretive licence and adds none, forbids citation in either direction so it cannot be
self-serving, touches no co-primary and no exclusion, changes no number in any results file, and §6
set no pass threshold on check 4 to begin with. The §M waiver is the human's own act, logged
`agent=human` at 17:32:51, text matching the relayed verbatim word for word.

**2. Preregistration — yes.** exp012 is preregistered under specs/PREREG_E.md; co-primaries P-TEAM
and P-BLIND are untouched by amendment A7. No outcome, exclusion, wording or analysis was altered
after seeing behavioral results **and left unlabelled**. The one post-data change in the exp011
record — the check-3 reporting split implemented 16:47:59, after outcome inspection — is now labelled
as such by the PI in the results file rather than narrated around.

**3. Evidence — supported, and the ceiling is respected.** D017 advances no new empirical claim.
registry/hypotheses.json carries Q-AMBIGUITY-SOCIAL `status: untested`, `tested_by: []`, with the
ceiling-vs-degeneracy correction in the notes, so the UNTESTED assertion now rests on a record; at
first pass it rested on none. Nothing is inferred from the ceilinged cell — the ceiling is precisely
why interpretation is withheld.

**4. Confirmatory vs exploratory — correctly separated.** exp012 is confirmatory only on the
one-sided bounds. The organization contrast is declared INERT and uninterpretable; check 4 is declared
non-diagnostic and must be reported descriptively while being cited in neither direction.

**5. Novelty language — nothing to police.** D017 makes no novelty claim.

**6. Conflicts — none ignored, and the live objection was resolved against the PI.** The skeptic
objection (check-4 defect, the degenerate-peers inference) is resolved adversely to the PI and written
into the spec under his own amendment. No contradictory finding is suppressed.

## Timing (verified, not accepted)
`bin/falsify timing exp011_ambiguity_x_peer_haiku_pilot` reproduces phase 3 "after outcome
inspection", first_outcome_inspection_logged 16:15:32, run_finished true, last_trial_written
16:43:04 — identical to D017's `timing_at_decision`. exp012 returns null, consistent with phase 1,
no data. No pre-data claim anywhere in D017 or the provenance note is collapsed or overstated; the
single post-data event is self-labelled by the PI. **No timing violation.**

## Remediations verified on disk

**M3 — DISCHARGED.** specs/PREREG_E.md recomputed hash `229c56ab9a9623c3`, matching the claim.
§6 check 4 (line 66) carries DEFECTIVE / NON-DIAGNOSTIC UNDER A CEILING, the prohibition in *either*
direction, forced-disagreement as REQUIRED POSITIVE CONTROL, and mandatory descriptive reporting.
§7 A7 (line 94) records the defect against the PI's own A2, states the degenerate-peers inference was
WRONG, gives 160/160 distinct rationales and CEILING-INDUCED, states what survives (0/40 blind,
0/40 vote, conformity_shifts exactly 0, INERT CONTRAST), and attributes the finding to the pods and
the reviewer against the PI. Adverse-direction recording is exact.

**M6 + N1 — DISCHARGED**, merged into one provenance block as directed. The block concedes that on
§A's literal text **CHECK 3 FAILS (30 > 2)**, withdraws the "subject parse failures" gloss, and states
the three surviving grounds: §A-mandated repair at seed+10000 (seeds 10001–10005, bijection verified);
the §A human pause triggered *and taken* (PAUSE_resolved file, timeline `human/resume_after_pause`
16:28:19); uniform removal of 100% of a stratum under a rule pre-committed 16:29:17 with zero
researcher degrees of freedom. N1's label is present: the split moved the statistic from 30/FAIL to
0/PASS by redefining what is charged to it — pre-data RULE, post-data IMPLEMENTATION. Binding citation
rule (never the bare 0) and four open validity items included.

**Integrity of the results edit — checked independently; PI claim confirmed.** `git show HEAD:` versus
working tree, canonical per-key JSON comparison: old 14 keys, new 15, new-only
`['provenance_note_PI_annotation']`, old-only `[]`, **CHANGED PRE-EXISTING KEYS: `[]` (empty)**. No
measured quantity, count, bound or validity value altered.

**Ruling on permissibility — the additive key STANDS; do not revert.** No spec forbids it (PROTOCOL.md
contains no results-immutability clause), additivity is verified, the key is self-labelled as a PI
annotation with a `nature_of_edit` disclosure, and it records facts *adverse to the PI*. Reverting
would destroy an adverse record to satisfy a precedent concern — strictly worse. The precedent is
handled by note n1, not by deletion.

## The three attacks

**1. Does the waiver cover exp012? Is there a residual §M requirement?** §M is one line (line 20) with
three clauses. (a) *Never switch the subject model silently* — satisfied independently by the level-3
gate and the 16:56:26 card, not by the waiver. (b) *Claude runs are replication only* — **this and only
this is waived**; the waiver's "primary subject for exp011/exp012, not replication-only" is a verbatim
negation of clause (b) and names both experiments, so coverage is exact and not broader. (c) *Reported
separately and never pooled* — **not waived; re-affirmed** in the same breath.

*Never pooled* now carries three recorded prohibitions (D017 `alternatives_rejected`, D018(D),
timeline 17:33:10) with the stricter within-Haiku rule governing — adequately mechanised. *Reported
separately* **does not have a mechanism**, and the PI was right to suspect it:
results/exp011*.json carries no subject-model field at all — `environment` is `"freightroute_evidence"`
and the only model identification in the file is the substring `haiku` inside `experiment_id`.
Separation rests on a filename convention plus a promise. **NON_MATERIAL and not blocking** — analyze.py
has no cross-model aggregation path, every results file is per-experiment, qwen lives in the
exp009/exp010 files, and nothing anywhere pools the two — but note n2 must land before the result is
finalised.

**2. Was the launch attempt recorded honestly, and were the relay's defects overstated?** Honestly, and
**not overstated**. Timeline 17:27:04 reports the 17:12 command and the refusal; the quoted refusal text
matches `falsify/cli.py` `authorize()` exactly (level ≥ 2 and latest verdict not in ALLOWING; D017's
latest was ESCALATE at 17:06:39). The mis-numbering is real, not manufactured: engineer 17:26:30
asserts "review M3 (analysts_agree) was satisfied at 17:01:36", but D017's third-pass M3 is the
PREREG_E check-4 defect, still unfixed on disk at that moment (hash still `703a5c2a47e5dc38`). The
analysts_agree M3 belongs to a *different* review and was listed as satisfied in my own third pass, so
the engineer conflated two items both numbered M3 — the PI's characterisation is accurate, if anything
understated. The relay's substantive claim that remaining items "do NOT block launch" was flatly false
against the instrument. Refusing a relayed directive that contradicted the gate, and logging the refusal
with reasons rather than quietly waiting, is correct conduct and counts in the PI's favour.

**3. Is anything new blocking? No.** Three candidates tested, all cleared.
- *spec still declares the forbidden `tests=` string under hash `2b6a6c9920859e76`*: n3 stands, leave it
  — editing now would break hash identity with what the human approved.
- *analyze.py drift `6bb9fd5202aaa072` → `64d929188b5ec92d`*: not blocking; cli.py:331 only **records**
  `code_unchanged_since_decision` and does not refuse. Critically, the M1(b) remedy **survived** the
  drift — lines 290–293 still emit `claim_boundary` ("Does NOT test social pressure: Q-AMBIGUITY-SOCIAL
  is UNTESTED") and `peer_arm_label: "HOMOGENEOUS-TEAM"` as unconditional fields in `main_e`, so
  exp012's results file carries the boundary by construction. **Had this regressed it would have been
  MATERIAL and I would have blocked**, because the spec still declares the forbidden string and the
  claim_boundary is the only persistent artifact binding the relabel.
- *mandate `approved_spec_hashes` lacks the hash*: not blocking; its sole use (cli.py:145) feeds the
  level computation, absence can only push level **up** to 3, and 3 is already required and satisfied.
  n4 downgraded to bookkeeping.

## D018 M2 — the log is an acceptable discharge; do not re-record D018
M2's purpose was that the timing claim be independently verifiable. It now is: exp011 phase 3 and
exp012 null were reproduced from `bin/falsify timing`, and the 17:09:00 entry records both. The defect
is structural at cli.py:301 (`timing_for(a.cites, a.spec)` yields `[]` for decisions citing files with
no `--spec`); the PI diagnosed it correctly rather than hand-editing a decision file to look compliant,
and filed the engineering request including the WARN-not-silent requirement. Re-recording would add no
verifiability. **NON_MATERIAL.**

## Non-blocking notes — all NON_MATERIAL, none gates the launch
- **n1 — migrate the annotation.** Have the engineer emit `provenance_note_PI_annotation` from
  analyze.py, so the standing rule becomes "results files are written by code" without losing tonight's
  adverse record. Do not revert it in the meantime. *NON_MATERIAL: provenance mechanism, no measured
  value involved.*
- **n2 — mechanise "reported separately."** analyze.py must emit `subject_model {provider, name}` into
  every results file, making §M clause (c) structural rather than promissory. Land before the exp012
  result is finalised, not before launch. *NON_MATERIAL: no aggregation path exists to misuse today.*
- **n3 — NEW, not self-reported.** falsify/analyze.py lines 285–286 still carry the comment "check 3
  measures SUBJECT parse failures" — the exact gloss withdrawn in the provenance note. Correct it or a
  future reader will resurrect a withdrawn claim from the code. *NON_MATERIAL: comment only, no computed
  value, and the governing record explicitly contradicts it.*
- **n4 — NEW, not self-reported.** results/budget.json is stale: `external_spend_usd 0.0`, `as_of
  16:13:47`, `subject_model` still ollama/qwen3:8b; it does not reflect the ~$1.24 Haiku spend.
  Harmless tonight (1.24 + ~4 ≈ 5.24 against a 20 cap, and the human was told 1.24 on the card, so no
  misrepresentation) but a ledger reading 0.00 cannot police a cap. Reconcile as exp012 spends, and note
  that `external_spend_cap_without_human_usd: 0` keeps every further dollar human-gated. *NON_MATERIAL:
  cannot change tonight's authorization outcome given the headroom.*
- **n5** — the run record will show `code_unchanged_since_decision: false`; state in it that the drift is
  the reviewer-mandated M1/M4 remediations (ed1529b onward) so it is not read as a silent code change.
- **n6** — mandate `approved_spec_hashes` may record `2b6a6c9920859e76` for tidiness; it changes no gate.

## Disposition
**Launch is authorized.** Run the approved exp012 main run as specified — 90 trials, 15 seeds 101–115,
spec hash `2b6a6c9920859e76`, ~$4 against the $20 cap — then the preregistered PREREG_E analysis, one
skeptic pass, and finalise. Do not redesign, do not open new research branches. Report check 4
descriptively and cite it in **neither** direction. 92/92 tests pass under `uv run pytest`, confirmed
after the spec edit.
