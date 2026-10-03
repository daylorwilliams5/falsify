# Loop-quality rubric (registered 2026-10-03, before Loop 3 runs)

Purpose: compare the scientific reasoning of the pod-based Loop 3 with Loop 1 (director + specialists) and Loop 2 (PI + reviewer, no pods). **Whatever the outcome, report it.** If the pods do not improve these metrics, that is the finding.

All metrics are computed from `timeline.jsonl`, `decisions/`, `critiques/`, `pods/` and git history. None are model-judged. A loop spans from its first timeline event to the PI's (or director's) final next-experiment decision.

| # | Metric | Operationalization | Better is |
|---|---|---|---|
| Q1 | Errors caught before reaching the PI | Count of distinct factual or code errors in a specialist or pod artifact that another lab agent corrected *before* a PI decision cited it (pods: disagreements marked `material` and resolved inside the pod; loops 1–2: specialist cross-corrections recorded in critiques) | higher |
| Q2 | Errors that reached a decision | Reviewer findings of factual, citation or authority errors in PI decisions (BLOCK/FAIL counts, plus CONCERNS that name an error) | lower |
| Q3 | Disagreements surfaced | Disagreements recorded with each side's position (pod `disagreements[]`; loops 1–2: explicit specialist conflicts in the timeline) | higher, if material |
| Q4 | Disagreements left silently unresolved | Surfaced disagreements that no later decision addresses | lower |
| Q5 | Citation density | Share of PI decision claims with a file, line, trial or result reference (count of `cites` per decision ÷ count of numbered claims) | higher |
| Q6 | Decision reversals | PI decisions later withdrawn or corrected (e.g. D002 → D003) | lower |
| Q7 | Cost | Claude sessions started, wall-clock minutes per loop, and subject-model calls (`falsify budget`) | lower, for equal Q1–Q6 |
| Q8 | Independent replication of analysis | Primary outcomes computed by two analysts who didn't see each other's work, and whether they agree | present, and agreeing |

**Caveats, stated in advance:**
- Each loop faces a different scientific situation (loop 1: a floored pilot; loop 2: a probe; loop 3: probe results). So this compares *process quality*, not difficulty-matched performance. n = 1 loop per architecture: the comparison is descriptive, never inferential.
- Loop 2's architecture changed mid-loop (D006 enforcement fix, reviewer verdict vocabulary). Report Loop 2 events before and after 12:20:34 separately where relevant.
