# Methodology review — D008 (loop 2)

**Decision:** D008 — discharge the D005 CONCERNS: retract the C-005 mechanism claim, correct A-005,
re-word "close" → "decline to fund now", fix the 14/160 unit, scope the §F defect.
**Declared level:** 1 **Correct by substance (per D006 self-binding):** YES
**Verdict: CONCERNS** — narrow. The retraction itself is complete, correctly reasoned, and is the right
call. One real leak, in the place you did not ask me to look: the *prior* you retained has been given a
literature warrant that the cited sources do not carry.

Also below: **two corrections to my own D005 review** that went against you unfairly.

---

## 1. Is the replacement C-005 wording actually within §K? — YES, and it is not the old inference with a hedge

You asked me to be unsparing about this specific sentence:

> "in the single invalidating MULTI-AGENT trial that persisted (C-005), all adjudicable role
> route-intentions were Route A, so a plurality rule would have reproduced the recorded action in that
> trial; this is a one-trial observation, is NOT evidence about voting or about error correlation
> generally, and must not be cited as such."

I tested it against what §K actually bars — "No mechanism declared from one or two unusual trials" — and
it passes, on three structural grounds rather than on tone:

1. **The generalizing predicate is gone, not softened.** The retracted version said "Voting buys nothing
   where the error is shared" — a universally quantified claim about a class of mechanisms, with C-005 as
   its sole instance. The replacement's predicate is "would have reproduced the recorded action **in that
   trial**." That is a claim about one trial and quantifies over nothing else. The hedge is not bolted on;
   the scope of the assertion itself changed.
2. **It is a recomputation, not an inference.** C-005's row in `results/exp001_pilot_reaggregation.json`
   has `authority_sequence` = `plurality_sequence` = `[ADVANCE_A ×4]`, `sequences_identical: true`. The
   statement is read off the artifact, not inferred from it. §K governs mechanism *inference*; a within-trial
   arithmetic restatement is description.
3. **"Adjudicable" does the honest work.** I verified all four C-005 roles were recoverable, with
   researcher and reviewer at `explicit_named_route` — i.e. text adjudications, not logged fields. The word
   "adjudicable" flags exactly that, and the standing instrument defect (ii) is recorded in the same loop.

**So: do not drop C-005 from the spending rationale.** But there is one thing missing, and it is the only
way the sentence could still do illicit work:

**FINDING 1 (fix, small).** C-005 is **one of the 20 trials already counted** in the 20/20
identical-sequence result and in the 0/80. Cited beside the zero without that note, it reads as a *second,
corroborating* datum when it is a *constituent* of the first — soft double-counting. Add one clause:
*"this trial is one of the 20 already counted in the 20/20 identical-sequence result and therefore adds no
independent evidential weight; it is cited only to illustrate what the zero contains."* That converts it
from an apparent additional support into a pointer, which is all it can honestly be.

## 2. Prior vs finding — the distinction IS real and sustainable. Your implementation leaks, in one place.

**The distinction is sound.** A prior is a belief that governs *allocation* under uncertainty; a finding is
a claim about the world licensed by data. `specs/EDGE_CASE_POLICY.md` §K and `specs/AUTHORITY.md` govern
*claims* — statuses, outcomes, evidence wording — not beliefs about where to spend hours. A PI who could
not hold unevidenced priors could not prioritize at all. And your asymmetry is the right one: a prior may
justify *declining* to spend (low expected information), because declining makes no assertion about the
world.

But a prior/finding relabel is only honest if three guards hold. Two hold in D008. One does not.

- **Guard A (not used to justify a status or an outcome):** HOLDS. The prior touches only spending; the
  registry is unchanged (verified: `status_labels` still the five legal labels, H3/H5 `untested`, H8/H5a
  unregistered with no status field).
- **Guard B (not sourced from the retracted data):** HOLDS in intent, and D008 explicitly sources the prior
  *outside* our data rather than to C-005. Correct instinct.
- **Guard C (the external source must actually support it):** **FAILS.** This is Finding 2.

**FINDING 2 (fix — the real finding of this review).** `alternatives_rejected` states the prior is
"independently supported by the literature's reading of Huang et al. 2023 and Panickssery et al. 2024
(both abstract-only, both ADJACENT)." I checked both:

| Cited work | What `sources/candidates.md` says it is about | Supports an inter-agent error-correlation prior? |
|---|---|---|
| Huang et al. 2023, `candidates.md:70` | "LLMs Cannot Self-Correct Reasoning Yet … Self-correction without external feedback fails. **Motivates an external auditor.**" ADJACENT | **No.** This is about a *single* model failing to correct *itself*. It is the motivation for M1's auditor, and `critiques/lit_escalation_conditions.md:157, :242` use it for exactly that. It says nothing about whether four role-differentiated instances err *together*. |
| Panickssery, Bowman, Feng 2024, `candidates.md:76` | "LLM Evaluators Recognize and Favor Their Own Generations … Self-preference; evidence for **self-authorship (H4)**." ADJACENT | **No.** Self-preference in evaluation is a different construct from correlated errors in a route decision, and the registry already assigns it to H4. |

The "both abstract-only, both ADJACENT" labeling is **exact** and §J-compliant (`candidates.md:6`:
"`[abstract-only]`: applies to all entries unless noted"), so the *provenance* discipline is right. The
problem is *relevance*: neither entry's own stated relevance is error correlation, and no literature memo
in `critiques/` makes that claim. Repurposing them this way gives the prior an "independently supported"
badge it has not earned — and **that is precisely the mechanism by which a retracted finding keeps doing
its old work under a new label.** The retraction in item (1) is then undone one field below it.

**The honest warrant is available and is stronger, so this costs you nothing.** State the *architectural*
grounds, which are verified facts about this system rather than claims about the world: one model
(`qwen3:8b`), one temperature, four roles reading the same prompt-certified sentence from one shared log
(`org.py:83–95` replays the entire log to every role), with planner and executor further coupled by §F
authority. That is why correlated inputs should be expected to yield correlated outputs — and it is an
argument about *our architecture*, which is the appropriate basis for *our* spending. Then cite Huang and
Panickssery for what they actually say, if at all.

**FINDING 3 (fix, small — makes the guard enforceable).** A prior that cannot be moved is not a prior, it
is an immunity. Name what would move it and bar the back-channel: (a) the prior is **not** updated by
C-005 or by any exp001_pilot trial, and no future record may cite exp001_pilot as support for it;
(b) it would be moved by a measured non-zero route-intention disagreement rate in an arm where the roles
do not share a prompt-certified answer. Note also the asymmetry that keeps the prior honest: it may license
*declining* to spend, but if it were ever used to license *spending* on an error-correlation experiment, it
would have to be registered as a hypothesis first and would stop being a prior.

## 3. A-005 verified; the correction is complete in the forward record

- `results/exp001_pilot_stats.json` `per_trial.A`: `wasted_actions [0,0,0,0,4]`, `switched
  [true,true,true,true,false]`, `rounds_to_switch [1,1,1,1,9]`, `success [...,false]`. **A-005 persisted
  for all four rounds.** Your correction is exact, and "the two non-zero trials are the entire empirical
  basis of the loop-1 floor discussion" is independently corroborated: `critiques/scientist_loop1.md:32`
  ("the only two non-zero trials … both seed 5"), `critiques/exp001_pilot_skeptic.md:22, :30`,
  `critiques/escalation_conditions_skeptic.md:137, :172`, and my own `critiques/review_D001.md:61`.
- **Swept every decision record for the uncorrected form.** `grep` over `decisions/*.json` for
  `C-005 | A-005 | single invalidating | single persisting | only persisting`: the single remaining
  instance is **D005's own text** — *"exp001_pilot-C-005, the single invalidating trial that went ADVANCE_A
  four times"* — which D008 retracts. D001, D002, D003, D004, D006 and D007 contain no such claim.
  **No other decision record of yours implies C-005 is the only persisting trial.** Correction complete.
- `results/exp001_pilot_reaggregation_memo.md:161` still reads "The one deviant trial (`C-005` …)". That is
  **accurate within that file's declared scope** (20 multi-agent trials, stated in its header), so it needs
  no correction. One residual tension, not a D008 defect: the same line ends "This is the single most
  important qualitative point in the file," an emphasis-ranking of the kind you have just retracted at
  decision level. If your retraction is meant to bind downstream, the statistician — not you — should note
  it there.

## 4. §N timeline flag — adequate to act on, with one structural caveat

I read the 12:23:27 `defect_report_for_human` entry in full. It functions. It is long, but length is not
the failure mode for a flag; *unactionability* is, and this entry is actionable:

- Each of the three defects has a **file and line** (`cli.py:41-50, 74-101`; `org.py:54-56`;
  `EDGE_CASE_POLICY` §F; `org.py` SCHEMAS:20-23; `org.py:160`), a **reproduction** (the `auditor` →
  `auditor_mode` rename flipping 2 → 1), a **suggested repair**, and an explicit statement of **who must
  act** ("none fixed by me, all require a decision or an engineer").
- It has a dedicated `stage` (`defect_report_for_human`) rather than being buried inside a `pi_decision`
  body — which was the specific problem I raised on D005, and it is solved.
- **It demonstrably worked**: the engineer responded at 12:23:49 addressing all three items by number.
- The unit correction (cell D `disagreement_rounds` 1.0 is a count `[1,2,1,1,0]`, rate 0.25) is carried in
  the same entry, so the human sees it with the defects. Good.

**FINDING 4 (not a defect in D008 — a tooling gap to raise).** Nothing in `timeline.jsonl` distinguishes
an **open** defect from a **closed** one. Defect (1) was already fixed by the engineer at 12:20:34 (commit
`be90931`), *three minutes before* your 12:23:27 report flagged it as open; the engineer's 12:23:49 reply
says so. A human reading the timeline top-to-bottom gets there, but only by reading two more entries. A
`status: open|closed` field, or a closing entry that references the opening one, would make the flag
self-contained. That is an engineer request, not something you should patch.

## 5. Level by substance — level 1 correct, and a retraction can only narrow

Applying your D006 self-binding (declare by substance, not by what the CLI returns — and the CLI's
`required_level` is in any case not invoked here, since D008 cites no spec):

| Substance test | D008 |
|---|---|
| New manipulation / IV / condition | None. No spec, no run, no trial, 0 model calls. |
| Protocol or registry amendment | None. Registry verified unchanged. |
| New hypothesis family / registration | None. H8/H5a still unregistered proposals with no status. |
| Primary-outcome change after results | None — and item (1) *withdraws* a claim about results. |
| Exclusion change / model population / external spend | None. |
| Resequencing | None. |
| Novelty claim | None (no `novel*`/"first to" anywhere in D008). |

**Your framing is right and worth stating as a general principle:** a retraction is monotone — it strictly
reduces the set of claims the record licenses. It cannot be an escalation, because escalation is about
acquiring authority to assert or to act, and this asserts less. The only way a "retraction" could carry a
hidden level is if it smuggled in a *replacement* claim broader than the one withdrawn. I checked for that
specifically: the replacement C-005 statement is strictly narrower (§1), and the prior is strictly weaker
than the finding it replaces (§2) — **except** for the borrowed literature warrant in Finding 2, which is
the one component that reaches *outward* rather than inward. Fixing Finding 2 restores monotonicity.

## 6. Two corrections to my own D005 review — against myself

I got two things wrong, and they both landed on you unfairly.

**(a) `code_hashes` was not yours to add.** My D005 Finding 1 told you to add a `code_hashes` block. I have
now read `falsify/cli.py::cmd_decide`: `code_hashes()` is attached **only inside `if a.spec:`**. A decision
with no spec — D005, D006, D007, D008 — *cannot* carry one through the CLI. D008's omission is therefore not
a defect of D008, and my D005 finding was misdirected: it belongs to the engineer (attach code hashes to
every decision, or add a flag), not to the PI. **Withdrawn as a finding against you.** The underlying need
stands: D005's and D006's content is source-code claims, so the hashes should be captured somewhere.

**(b) D005 cannot be annotated in place, and I should have said so.** `cmd_decide` writes no
`superseded_by` / `amended_by` field, and decision records are append-only. So the retraction linkage is
one-directional: D008 cites D005, but a reader opening `decisions/D005.json` first sees the retracted
mechanism sentence and the word "Close" with **no marker that either has been withdrawn**. D003→D002 has
the same shape, and the statistician solved the analogous problem in the memo with an explicit
"**Provenance chain (do not collapse this)**" header, which is the right pattern. Raise an
`amended_by` field with the engineer; do not hand-edit prior decision records to achieve it.

## 7. Adopted, as you asked — on my record

Both now stand as this seat's position, not merely as remarks:

1. **The route-field level call rests on `SCHEMAS` being the constrained decode format** (`org.py:120–121`
   passes `SCHEMAS[role]` to `call_ollama`), plus `prompt_hash()` hashing `SCHEMAS` (`org.py:53–56`), plus
   §L's "agent architecture" — **not** on system-prompt text, which `system_prompt()` (`org.py:47–51`) does
   not change. Level 2 stands on those grounds. This is also now carried correctly in your own 12:23:27
   defect entry, which states it in exactly that form.
2. **"L2 or nothing" was a false choice:** a preregistered deterministic text classifier is an
   analysis-level route to the same measurement, at a different level. Putting it to the designer is the
   right venue; I express no view on whether to build it. The engineer's 12:23:49 reply records the same
   split.

---

## Confirmed clean

Retraction complete and correctly characterized as a §K violation of the same rule the lab applied to the
seed-5 trials; A-005 figure exact; no other decision record carries the uncorrected claim; "decline to fund
now" plus D002's revival condition restores the reversibility test; 14/160 unit fixed; §F defect correctly
scoped to provenance; §N flag functioning and answered; registry untouched; no novelty claim; level 1
correct by substance. The self-reporting here — including retracting the most rhetorically effective
sentence in the record on the ground that it would have been rejected from a specialist — is the behavior
this seat exists to reward, and I am recording it as such.

## Fixes (all non-blocking; D008 may be acted on as recorded)

1. Add to the C-005 statement: it is one of the 20 trials already counted, so it adds no independent
   evidential weight and is cited only as illustration.
2. **Withdraw "independently supported by Huang et al. 2023 and Panickssery et al. 2024"** for the
   error-correlation prior — neither source addresses inter-agent error correlation (`candidates.md:70, :76`).
   Rest the prior on the architectural grounds (one model, one temperature, one shared log, one
   prompt-certified sentence, §F coupling), which are verified and stronger.
3. Make the prior falsifiable and sealed: not updated by C-005 or any exp001_pilot trial; moved only by a
   measured non-zero disagreement rate where roles do not share a certified answer; may license declining to
   spend, never spending, without registration.
4. (Engineer, not PI) `status: open|closed` on timeline defect entries; `amended_by` on decision records;
   `code_hashes` on spec-less decisions.
