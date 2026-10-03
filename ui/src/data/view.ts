import type { PIDecision, Review, Verdict } from './types';

// Derivations from raw artifacts. No text truncation: if a record lacks the
// structured field, the UI shows less rather than an invented summary.

/** "run" + "specs/exp009_v2_floor_probe.json" → ["Run", "exp009_v2_floor_probe"] */
export function decisionHeadline(d: PIDecision): { verb?: string; target?: string; text?: string } {
  const target = d.spec?.split('/').pop()?.replace(/\.json$/, '');
  if (d.action === 'run' && target) return { verb: 'Run', target };
  return { text: d.summary ?? `${d.id} · ${d.action}` };
}

export const LEVEL_LABEL = { 1: 'Autonomous', 2: 'Needs reviewer pass', 3: 'Needs human' } as const;

export const latestReview = (d: PIDecision): Review | null => d.reviews.at(-1) ?? null;

const VERDICT_LABEL: Record<Verdict, string> = {
  PASS: 'PASS', PASS_WITH_NOTE: 'PASS WITH NOTE', BLOCK: 'BLOCK', ESCALATE: 'ESCALATE', CONCERNS: 'CONCERNS', FAIL: 'FAIL',
};
export const verdictLabel = (v: Verdict) => VERDICT_LABEL[v];
export const verdictTone = (v: Verdict) =>
  v === 'PASS' || v === 'PASS_WITH_NOTE' ? 'pass' : v === 'CONCERNS' ? 'concerns' : 'fail';

export const CHECK_LABEL: Record<string, string> = {
  decision_recorded_before_action: 'Recorded before action',
  level_correct: 'Authority level correct',
  inside_preregistered_condition_space: 'Inside preregistered space',
  spec_hash_verified: 'Spec hash verified',
  code_unchanged_since_decision: 'Code unchanged since decision',
  model_within_mandate: 'Model within mandate',
  budget_compliant: 'Budget within mandate',
  preregistered: 'Preregistered',
  primary_outcomes_unchanged: 'Primary outcomes unchanged',
  exploratory_labeled: 'Exploratory work labeled',
  novelty_language_ok: 'Novelty language',
};

/** Checks a review runs on every decision; shown as pending while it audits. */
export const STANDARD_CHECKS = [
  'decision_recorded_before_action', 'level_correct', 'preregistered', 'primary_outcomes_unchanged', 'budget_compliant',
];

/** Recorded checks: automatic ones always; attested ones only when actually attested. */
export function reviewChecks(r: Review): { label: string; ok: boolean }[] {
  const auto = Object.entries(r.auto_checks ?? {}).map(([k, ok]) => ({ label: CHECK_LABEL[k] ?? k, ok }));
  const att = Object.entries(r.attested ?? {})
    .filter(([, v]) => v !== null)
    .map(([k, ok]) => ({ label: CHECK_LABEL[k] ?? k, ok: !!ok }));
  return [...auto, ...att];
}

export type Outcome = 'ACCEPTED' | 'CORRECTED' | 'ESCALATED' | 'IN_REVIEW' | 'OPEN';

export const OUTCOME_LABEL: Record<Outcome, string> = {
  ACCEPTED: 'Autonomously accepted',
  CORRECTED: 'Corrected after review',
  ESCALATED: 'Escalated to human',
  IN_REVIEW: 'In review',
  OPEN: 'Awaiting correction',
};

export const respondersTo = (d: PIDecision, all: PIDecision[]) =>
  all.filter((x) => x.responds_to?.includes(d.id));

export function outcomeOf(d: PIDecision, all: PIDecision[]): Outcome {
  const r = latestReview(d);
  if (d.human_intervention || d.level === 3 || r?.verdict === 'ESCALATE') return 'ESCALATED';
  if (respondersTo(d, all).length) return 'CORRECTED';
  if (!r) return 'IN_REVIEW';
  if (r.verdict === 'PASS' || r.verdict === 'PASS_WITH_NOTE') return 'ACCEPTED';
  return 'OPEN';
}

export const hhmm = (iso: string) => iso.slice(11, 16);

export function minutesBetween(a: string, b: string): number {
  return Math.round((new Date(b).getTime() - new Date(a).getTime()) / 60000);
}

export function elapsedSince(iso: string, now = Date.now()): string {
  const s = Math.max(0, Math.floor((now - new Date(iso).getTime()) / 1000));
  const h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60);
  return h ? `${h}h ${String(m).padStart(2, '0')}m` : `${m}m`;
}

/** "results/exp001_pilot.json" → "exp001_pilot.json"; plain IDs pass through. */
export const shortCite = (c: string) => c.split('/').pop() ?? c;
