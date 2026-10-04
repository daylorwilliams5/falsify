import type { LabEvent, PIDecision, Review, Verdict } from './types';

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
  IN_REVIEW: 'Not yet reviewed',
  OPEN: 'Awaiting correction',
};

export const respondersTo = (d: PIDecision, all: PIDecision[]) =>
  all.filter((x) => x.responds_to?.includes(d.id));

export function outcomeOf(d: PIDecision, all: PIDecision[]): Outcome {
  const r = latestReview(d);
  if (d.human_approval || r?.verdict === 'ESCALATE') return 'ESCALATED';
  if (respondersTo(d, all).length || d.remediated) return 'CORRECTED';
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

/** Plain-language status for readers outside the lab. */
export const PLAIN_STATUS: Record<string, string> = {
  UNTESTED: 'Not tested yet',
  RUNNING: 'Being tested',
  SUPPORTED: 'Supported',
  FALSIFIED: 'Ruled out',
  INCONCLUSIVE: 'Not enough evidence yet',
  NEEDS_REPLICATION: 'Needs to be repeated',
};

// ---------- timeline ----------
/** Decisions the reviewer stopped outright (fail, block or escalate) at least once. */
export const stoppedByReviewer = (all: PIDecision[]) =>
  all.filter((d) => d.reviews.some((r) => ['FAIL', 'BLOCK', 'ESCALATE'].includes(r.verdict)));

export const LANES = [
  { id: 'human', label: 'Human', actors: ['human'] },
  { id: 'lead', label: 'Lab lead', actors: ['PI', 'director', 'falsify'] },
  { id: 'reviewer', label: 'Independent reviewer', actors: ['methodology_reviewer'] },
  { id: 'specialists', label: 'Specialist agents', actors: ['literature', 'scientist', 'designer', 'skeptic', 'statistician', 'auditor'] },
  { id: 'experiments', label: 'Experiments', actors: ['runner', 'statistician-tool'] },
  { id: 'engineering', label: 'Engineering', actors: ['engineer'] },
] as const;
export type LaneId = (typeof LANES)[number]['id'];

export const laneOf = (actor: string): LaneId =>
  (LANES.find((l) => (l.actors as readonly string[]).includes(actor))?.id ?? 'specialists');

export type EventKind = 'decision' | 'review-fail' | 'review' | 'directive' | 'run' | 'fix' | 'note';

export function eventKind(e: LabEvent): EventKind {
  if (e.stage === 'pi_decision') return 'decision';
  if (e.stage === 'methodology_review') return e.verdict === 'FAIL' || e.verdict === 'BLOCK' ? 'review-fail' : 'review';
  if (e.actor === 'human') return 'directive';
  if (e.stage.startsWith('experiment') || e.actor === 'runner' || e.actor === 'statistician-tool') return 'run';
  if (e.stage.includes('fix') || e.stage === 'correction') return 'fix';
  return 'note';
}

const firstSentence = (t: string) => t.split(/(?<=[.!?])\s/)[0];

/** A readable line for an event: decision/review summaries when they exist, else the first sentence. */
export function eventHeadline(e: LabEvent, decisions: PIDecision[]): string {
  const d = e.decision_id ? decisions.find((x) => x.id === e.decision_id) : undefined;
  if (e.stage === 'pi_decision' && d?.summary) return d.summary;
  if (e.stage === 'methodology_review' && e.decision_id) {
    const r = d?.reviews.find((x) => x.ts.slice(0, 19) === e.ts.slice(0, 19));
    const hl = r?.highlights?.[0];
    return `${e.decision_id} reviewed: ${e.verdict ? verdictLabel(e.verdict) : ''}${hl ? `. ${hl}` : ''}`;
  }
  return firstSentence(e.text);
}

/** Events tied to `id`: the decision, its reviews, what it responds to and what responds to it. */
export function chainOf(id: string, decisions: PIDecision[]): Set<string> {
  const ids = new Set([id]);
  const d = decisions.find((x) => x.id === id);
  d?.responds_to?.forEach((x) => ids.add(x));
  decisions.filter((x) => x.responds_to?.includes(id)).forEach((x) => ids.add(x.id));
  return ids;
}

export const hhmmss = (iso: string) => iso.slice(11, 19);

const ACTOR_LABEL: Record<string, string> = {
  PI: 'Principal investigator', methodology_reviewer: 'Independent reviewer', human: 'Human', engineer: 'Engineer',
  falsify: 'Lab system', director: 'Director', 'statistician-tool': 'Statistics tool', runner: 'Experiment runner',
};
export const actorLabel = (a: string) => {
  if (ACTOR_LABEL[a]) return ACTOR_LABEL[a];
  const words = a.replace(/[_-]+/g, ' ');
  return words.charAt(0).toUpperCase() + words.slice(1);
};

/** Events worth showing by default: human acts, decisions, experiment runs and results, fixes. Reviews fold into their decision. */
export function isKeyMoment(e: LabEvent): boolean {
  if (e.stage === 'methodology_review') return false;
  if (e.actor === 'human' || e.stage === 'pi_decision') return true;
  if (e.stage === 'experiment_started' || e.stage === 'analysis_written') return true;
  return e.stage === 'enforcement_fix' || e.stage.startsWith('loop');
}
