# exp013t skeptic pass — PARTIAL (checkpoint 1, ~19:30)

Single independent pass. Scope fixed: (Q1) is the advisory-majority effect real or artifact; (Q2) is the cost null interpretable.
Checkpoints written incrementally; this file is overwritten with accumulated content.

## C1. The 60 harness exceptions — CHECKED, NOT material
`results/...haiku.json`: `n_trials 120, n_invalid 60, V3_invalid.harness_exceptions 60`.
`..._PAUSE_resolved_2026-10-03T190201.json`: invalid rate **1.0 in all four cells**.
`falsify/analyze.py:343` + `falsify/org.py:285`: attempt 1 was a **400 from the Anthropic structured-output endpoint
before any model call** (schema rejected `minimum`/`maximum` on the F3 probability field).

Ruling: attrition was (a) complete (15/15 per cell), (b) uniform across all four cells, (c) pre-subject — no token was
ever generated. Therefore it cannot be outcome-dependent and cannot bias the dissent contrast. NOT MATERIAL.
Residual, for the write-up: the analysed 60 are attempt 2 after a **schema edit between attempts**, so the F3 field now
has no enforced bounds. Verify no out-of-range p values (see C2) and state in the card that the run is attempt 2 of 2.

## C2. `fees_paid_total = 0` in the costly cells — vestigial channel, reporting hazard
Cost channel is TIME (`cost_channel: "TIME (INSPECT takes 2 rounds of a 6-round stated deadline)"`,
spec `costly_inspect_fee: 0`). But the result file still carries `fee_regex`, `fees_paid_total`, and
`fee_reference_rate_round1 = 0.0` in all four cells. These are inert leftovers of the money design, not evidence.
Hazard: `fee_reference_rate_round1 = 0.0` everywhere must NOT be read as "the agent ignored the cost" and
`MC_C1_cost_delivered: pass` must not be read as a fee being delivered. Limitation, not material.
(continued)
