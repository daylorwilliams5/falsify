# Methodology review — D006 (enforcement bypass in the authority layer)

Reviewer: methodology_reviewer. Date: 2026-10-03, loop 2. **Verdict: CONCERNS.**
Level 1 upheld. Defect reproduced independently. No violation blocks any action.

Read: `decisions/D006.json`, `critiques/exp008_skeptic.md` (§2.6 T10a/T10b, §6),
`specs/AUTHORITY.md`, `specs/PREREG_V2.md`, `lab/mandate.json`, `decisions/D001.json`,
`decisions/D004.json`, `timeline.jsonl` (12:14–12:21), `falsify/cli.py`, `falsify/org.py`,
`falsify/env.py`, `specs/exp009_v2_floor_probe.json`, `specs/candidates/*.json`,
`data/exp009_v2_floor_probe.log`, `data/trials/exp009_v2_floor_probe.jsonl`.
Executed: `bin/falsify level` on all 12 specs under both the live and the pre-fix checker; git
archaeology on `falsify/cli.py`.

---

## 1. The defect is real. I reproduced it myself.

I did not take the skeptic's word or the PI's. Reproduction required archaeology, because **the live
checker already fails closed** — my first attempt returned level 2 for the renamed spec, which if
accepted at face value would have made D006 a false alarm. It is not. The reason is in §2.

Pre-fix code = commit `2625a6a`, checked out into a detached worktree (`/tmp/prelab`, since removed).

| Spec (pre-fix checker) | required_level | reason |
|---|---|---|
| `specs/candidates/exp008_auditor_m1.json` (as written) | **2** | `cell M_hier_aud: auditor=True outside preregistered [False]` |
| same spec, `auditor` → `auditor_mode` + `auditor_view` | **1** | `inside preregistered condition space, mandated model, within level-1 budget` |

**The 2 → 1 drop reproduces exactly as D006 describes it.** Same experiment, same 4 cells, same 15
seeds, same 60 trials, same subject model; two brand-new manipulations; classified PI-autonomous.

Mechanism, read in pre-fix `falsify/cli.py:103-116`:

```python
for key, allowed in space.items():      # iterates PREREG_SPACE keys ONLY
    ...
    for c in spec.get("cells", []):
        v = c.get(key, False if key == "auditor" else None)
        if v is not None and v not in allowed: ...
```

The loop is driven by the *known* keys, so a cell key absent from `PREREG_SPACE` is never visited and
never validated. Second gap confirmed: pre-fix `falsify/org.py:53-55` hashes
`[TEAM, DUTIES, SINGLE, AUDITOR, SCHEMAS]`; `Scenario.auditor_view` is defined at
`falsify/env.py:47` and is absent from that list.

**No false alarm.** Protocol honored: `specs/candidates/exp008_auditor_m1.json` was not modified in
place — md5 `7eba7e9be431b996b638dbd2d1438348` before and after, `git status specs/` clean, all
scratch artifacts removed.

## 2. The defect is already fixed — and D006 cannot say so. Close the record.

An **engineer** agent — not the PI — committed `be90931` *"Close D006 enforcement bypass: allowlist
fields for authority level; hash environment text"* at **12:20:34**, i.e. **100 seconds after** D006
was recorded at 12:18:54 (`timeline.jsonl`, stage `enforcement_fix`).

I verified the fix closes the hole. On live code the renamed spec returns level 2 with
`cell M_hier_aud: 'auditor_mode' is not a recognized preregistered field`. New allowlists
`CELL_META_KEYS` / `ENV_DEFAULTS` / `MODEL_DEFAULTS` at `cli.py:68-74`; unrecognized-field checks at
`cli.py:138, 146, 155`. `code_hashes()` now also hashes `env.Scenario.task_text`,
`auditor_view`, `contradiction_text`, `env2.Scenario2.task_text` and `env2.INCENTIVES` — closing the
prompt-hash gap at the code-hash layer. `org.py:53-55` itself is unchanged.

**Fix required:** append to D006 that the defect was closed at `be90931` / timeline 12:20:34 and
verified by this review. As written, D006 stands in `decisions/` and `timeline.jsonl` as an **open,
unremediated** integrity defect. That is now false and will mislead the next loop.

## 3. The refusal to self-patch — I argued the other side. Conclusion sound, reasoning overstated.

**Against the PI.** `specs/AUTHORITY.md` nowhere reserves `falsify/cli.py` to the human. The PI's
"Cannot" list is: edit raw data, change preregistered results, silently change exclusions, invent
evidence, unqualified novelty claims. Patching a checker to be *stricter* is none of them. The PI
also does direct changes to frozen artifacts when the science wants it — the `env2.py` instrumentation
it authorized and defended in D001/D004 — so "I must not touch code bearing on my own conduct" is not
applied uniformly. And the independence claim is simply too strong: **a PI-authored patch is a git
diff I can adversarially test exactly as I just tested the engineer's.** I am not dependent on the
checker's authorship, only on my ability to re-derive levels from substance — which I keep either way.
So the sentence *"a reviewer auditing my levels against a checker I wrote has been given a weaker
instrument"* is false as stated.

**For the PI — the conclusion survives, on narrower grounds.**
1. **Separation of duty**, not of audit capability: the PI is not the lab's engineer; delegating cost
   nothing and lost nothing.
2. **Incentive hygiene:** the PI is the sole beneficiary of a loose ceiling. A self-authored ceiling
   invites a motive dispute on every future level call — expensive to litigate, cheap to avoid.
3. **The outcome refutes the "excuse for leaving the hole open" reading.** Exposure was ~100 seconds,
   no run passed through the defective path (§6), and the hole was closed by a second party and
   verified by a third. Constrained party reports → unconstrained party repairs → independent party
   verifies. That is the correct structure and it worked.

**I do not conclude the PI should have patched it.** Fix: restate the rationale as separation of duty
plus zero-cost delegation, and drop the "weaker instrument" claim.

## 4. Level call on D006 itself: **Level 1 is correct.**

Against every level-3 trigger in `specs/AUTHORITY.md`: no primary-outcome change after results, no
exclusion change, no model-population change, no external spend, no sensitive/external data, no
publication-level novelty claim. The only arguable trigger is *safety-policy override* — and D006 is
its exact inverse: it **tightens** the PI's discretion and requests no permission. `escalate`
authorizes what the PI may not do alone; D006 asks for nothing.

Level 2 does not bite either: a strictly tighter self-imposed constraint is not a new control, not a
new manipulation, not an amendment to any experiment, not resequencing, and spends no trials. A known
governance bypass is a serious *engineering* defect; that does not make its *report* a level-3 act.
Escalating would have paused the human's card on a decision needing no authorization while leaving
the actual repair unassigned.

Strongest counterargument, recorded: D006 does change the rule by which the PI declares levels for
all future decisions, which has a protocol-amendment flavor. It fails to reach level 2 because the
change is unilaterally tightening, prejudices no measurement, and can only be undone by loosening —
which would itself require review. **Level 1 upheld.**

## 5. D001 and D004 re-derived from substance, not the CLI.

This was the part that mattered most, so I enumerated by hand rather than trusting any checker.

**D001** — `specs/exp009_v2_floor_probe.json`: env `{freightroute_v2, segments: 4}`; cells
N_hi/N_lo/T_hi/T_lo = `org single` × `budget {24,10}` × `incentive {ordinary,target}` ×
`auditor False`; seeds 1–5; 20 trials. **Every cell field name is a preregistered PREREG_V2 factor**
(`specs/PREREG_V2.md:11-14`) and every value sits inside it. There is **no renamed, novel or
unrecognized key anywhere in the spec**, so the defective code path was never load-bearing for
D001's level. Model `ollama/qwen3:8b` = mandate `subject_model` exactly; 20 ≤ 120 trials; no external
spend; human-approved at timeline 11:48:56; spec hash still `e4d5f3d91f2df2f1`, matching D001.
→ **Substance: LEVEL 1.** (Also level 1 under the new strict checker.)

**D004** — no spec, no trials, no manipulation. It narrows reporting to the one feasibility field
named in the approved spec's `requires_build` and declines three fields shipped beyond it. By
substance that is a *withdrawal of discretion*: no primary outcome changed, no observation excluded
(fields retained in logs, merely unreported), no condition/model/spend change. The asymmetry holds —
adopting the ground-truth variant instead **would** have been level 2. Only the tightening direction
was available at level 1, and the PI took it. → **Substance: LEVEL 1.**

**Neither D001 nor D004 should have been level 2. Nothing to record against either.** D001's reliance
on `bin/falsify level` was lucky in form but correct in substance. exp009 has since completed 20/20
(`DONE ... in 925s`; 20 records on disk); the "14/20" in the request was stale, with no level
consequence.

## 6. The bypass was never used — plus one latent instance everyone missed.

Strict checker run over all 12 specs, diffed against the pre-fix checker. The two specs that have
actually **run** are clean under **both**: `specs/exp001_pilot.json` and
`specs/exp009_v2_floor_probe.json`, both level 1, zero unrecognized fields. No renamed or
unrecognized cell key appears in any spec the PI has run, cited as authority, or acted on.

**New finding — the bypass was not merely hypothetical.**
`specs/candidates/exp005_stage1_comprehension_pilot.json` computed **level 1** under the defective
checker and is **level 2** under the strict one: unrecognized cell field `evidence` (6 cells) and
unrecognized environment parameter `comprehension_probe` — two genuinely new manipulations silently
classified PI-autonomous, with no rename and no bad intent by anyone. Never run; cited in no
decision (proposed only in `critiques/loop1_design.md`). `exp006_peer_deterministic.json` and both
`exp005_evidence_x_org.json` copies also carry unrecognized fields but were level 2 anyway on
independent grounds (`org='peer'`, 180 trials).

**Fix:** record this in D006. The truer and more damning statement is not that an agent *could*
rename a field, but that **a real, innocently-written candidate spec in this repo was already being
under-leveled.**

## 7. Citation errors — must be corrected.

Exact and verified: both verbatim reason strings, and the AUTHORITY.md quote *"enforcement assumes
agents use the CLI. An agent with shell access could edit files directly"* (`AUTHORITY.md:31`).

Wrong, all inherited from `critiques/exp008_skeptic.md` §2.6 without re-verification:

| D006 says | Pre-fix reality |
|---|---|
| `PREREG_SPACE` at `cli.py:41-50` | `cli.py:46-52` |
| iterated at `cli.py:74-101` | `required_level` at `:88`; defective loop at `:103-116` |
| `prompt_hash` at `org.py:54-56` | `org.py:53-55` |
| level-1 reason `'inside preregistered condition space'` | `'inside preregistered condition space, mandated model, within level-1 budget'` (truncated) |

These matter more than usual: the D004 review certified "LINE CITATIONS — ALL EXACT", the fix has now
moved every line number again, and an integrity record that cannot be navigated to the code it
indicts loses most of its value. **Fix:** correct all four and pin them to commit `2625a6a`.

## 8–10. Inference, novelty, conflicts

**Confirmatory vs exploratory: clean.** No empirical claim about the subject, no hypothesis status, no
behavioral number; nothing floored or ceilinged because nothing is measured. The one claim I checked
hardest — that exp009's level-1 status "does not depend on the defective path" — is **true** (§5).
Attribution is accurately hedged: the PI claims code-reading confirmation of the *mechanism*, not
re-execution, which is what it appears to have done. Credit to the skeptic is properly given, not
appropriated.

**Novelty:** no novelty claim of any kind. Compliant.

**Conflicts:** none ignored. D006 adopts T10a/T10b rather than disputing them, and the repair it
recommends is the skeptic's own prescribed control, which the skeptic had already assigned to the lab
as a prerequisite build — consistent with routing it to an engineer. No contradictory finding in
`critiques/` or `results/` is omitted; no skeptic objection is left unanswered.

## 11. Standing audit item: accepted, with two additions

I will check declared levels against **substance**, never against `bin/falsify` output, and treat any
CLI/substance disagreement as a defect to report. Added to the standing list:

1. Re-audit any level on a spec carrying a cell field, environment parameter or model parameter
   outside `PREREG_SPACE`. The strict checker is new and untested in anger, and **the allowlists at
   `cli.py:68-74` are now themselves authority-bearing configuration that no test or review has yet
   validated against `PREREG_V2`.**
2. Verify on each decision that the `code_hashes` block is present and that env/prompt text changes
   move it — that is now the only detector for `auditor_view` drift, since `org.py:53-55` is still
   unfixed in itself.

## 12. Consistency check the PI asked for — upheld

Rejecting the statistician's route-field change under a level-1 decision, because a prompt change is
substance and not instrumentation, is the same principle as D006 applied in the direction that
**costs** the PI something. The two are consistent, and I will hold the PI to it symmetrically:
substance outranks the label when the label is convenient *and* when it is inconvenient.

The live risk in the other direction is the D004-style *"it is only measurement"* move. That was
correct there **only** because the added fields provably could not reach the subject's prompt or
action space (verified in code). It does not generalize and must be re-earned each time.

---

## Verdict

**CONCERNS.** The defect is real and exactly as reported; level 1 is correct; the refusal to
self-patch was the right call and has been vindicated by events; D001 and D004 both re-derive to
level 1 on substance with no under-declaration anywhere. Nothing blocks any action.

Required before D006 is relied on as a record:
- **§2** — record that the fix landed (`be90931`, 12:20:34) and was independently verified.
- **§6** — record the real `exp005_stage1_comprehension_pilot.json` instance.
- **§7** — correct the four line citations and the truncated quote; pin to `2625a6a`.
- **§3** — narrow the self-patch rationale to separation of duty; drop the "weaker instrument" claim.
