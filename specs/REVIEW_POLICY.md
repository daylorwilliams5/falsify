# Review materiality and timing claims (human policy, 2026-10-03)

## A. Review materiality (Level 1 decisions)
| Verdict | Effect |
|---|---|
| PASS | Proceed normally |
| PASS_WITH_NOTE | Proceed; batch the note into the end-of-loop disposition. Cannot carry MATERIAL concerns |
| CONCERNS | Proceed **unless** at least one concern is MATERIAL |
| BLOCK / FAIL | Stop until corrected |

A concern is **MATERIAL** only if it could affect: protocol validity; data integrity; authority classification; timing or preregistration claims; primary outcomes or exclusions; interpretation of the scientific result; validity of the next experiment.

**NON_MATERIAL** concerns include: wording precision that doesn't change meaning; formatting; minor documentation inconsistencies; optional clarifications; stylistic issues; already-fixed defects whose current state is verified.

**Rules:**
- The reviewer labels every concern MATERIAL or NON_MATERIAL with a one-sentence reason, and records the count (`--material N`, required by the CLI for CONCERNS and PASS_WITH_NOTE).
- The PI must not create a new decision only to clear NON_MATERIAL concerns. Those go into one end-of-loop record: `bin/falsify disposition <loop> --decisions ... --note ...`.
- MATERIAL concerns must be resolved before the affected scientific action proceeds. The CLI refuses `run` or `conclude` under a decision whose latest review is CONCERNS with N > 0.
- Review findings are never deleted or suppressed. The record is append-only.

## B. Timing claims
Any claim such as "preregistered before data", "decided while the run was in progress" or "chosen before outcomes were known" must be verified against machine timestamps where available. Always distinguish:
1. **before run completion**
2. **after run completion, before outcome inspection**
3. **after outcome inspection**

Never collapse these into "pre-data".

**Machine support:**
- `bin/falsify timing <exp>` derives the phase from the run log (DONE line), the trial file's write time, and the first logged `analysis_written` or `pod_synthesis` event.
- Every decision records `timing_at_decision` for each experiment it cites.

**Limitation:** phase 3 detection relies on logged analyses. An agent that reads raw trial data without running the logged analysis isn't detected, so reviewer judgment still applies.
