/**
 * PLANNED — not wired. Maps live Falsify artifacts into a LabSnapshot.
 *
 *   registry/hypotheses.json       → state.question, hypotheses[]
 *       status: lowercase → HypothesisStatus (e.g. "inconclusive" → "INCONCLUSIVE")
 *       supporting/contradicting: counted from evidence items citing the id
 *   specs/<exp>.json               → experiments[].design, trials.total, spec_hash
 *   results/<exp>.json             → experiments[].cells, trials.done/invalid,
 *                                    primary (H1_interaction_wasted.delta/ci95)
 *   results/<exp>_stats.json       → experiments[].flags, metrics (power, floor)
 *   timeline.jsonl                 → timeline[] (agent === "human" → HUMAN,
 *                                    *-tool / runner → EXPERIMENT, else AGENT)
 *                                    and the latest event per agent → activity.agents
 *   critiques/*.md                 → INFERRED evidence + loop stage artifacts
 *   specs/candidates/*.json        → state.next_decision.options
 *   sources/candidates.md          → literature[] (parse markdown tables;
 *                                    [abstract-only]/[2026 preprint] → verification)
 *
 * Expected transport: a tiny read-only dev endpoint (or Vite plugin) that
 * serves these files as JSON, plus SSE on timeline.jsonl append for `subscribe`.
 */
export {};
