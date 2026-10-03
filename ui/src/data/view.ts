import type { PIDecision } from './types';

// Small derivations so the UI reads raw artifacts without extra fields.

/** "run" + "specs/exp009_v2_floor_probe.json" → "Run exp009_v2_floor_probe" */
export function decisionTitle(d: PIDecision): string {
  const verb = d.action.charAt(0).toUpperCase() + d.action.slice(1);
  const target = d.spec?.split('/').pop()?.replace(/\.json$/, '');
  return target ? `${verb} ${target}` : verb;
}

/** Prefer the PI's one-line summary; otherwise the first sentence of the reason. */
export function decisionReason(d: PIDecision): string {
  if (d.summary) return d.summary;
  const first = (d.reason ?? '').split(/(?<=\.)\s/)[0];
  return first.length > 160 ? first.slice(0, 157) + '…' : first;
}

/** Prefer a short label; otherwise the text before the first ':' of the first alternative. */
export function rejectedAlternative(d: PIDecision): string | null {
  if (d.rejected_summary) return d.rejected_summary;
  const first = d.alternatives_rejected?.split('|')[0]?.split(':')[0]?.trim();
  return first || null;
}

export const LEVEL_LABEL = { 1: 'Autonomous', 2: 'Needs reviewer pass', 3: 'Needs human' } as const;

export function elapsedSince(iso: string, now = Date.now()): string {
  const s = Math.max(0, Math.floor((now - new Date(iso).getTime()) / 1000));
  const h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60);
  return h ? `${h}h ${String(m).padStart(2, '0')}m` : `${m}m`;
}
