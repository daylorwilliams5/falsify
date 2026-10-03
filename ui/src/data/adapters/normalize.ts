import type { LabEvent, PIDecision, RejectedAlternative, Verdict } from '../types';

/**
 * Accepts a decisions/D*.json record in either the legacy shape
 * (alternatives_rejected as one " | "-separated string) or the structured one.
 */
export function normalizeDecision(raw: Record<string, unknown>): PIDecision {
  const alts = raw.alternatives_rejected;
  let structured: RejectedAlternative[] = [];
  if (Array.isArray(alts)) structured = alts as RejectedAlternative[];
  else if (typeof alts === 'string' && alts.trim()) {
    structured = alts.split(' | ').map((part) => {
      const i = part.indexOf(':');
      return i > 0 ? { label: part.slice(0, i).trim(), reason: part.slice(i + 1).trim() } : { label: part.trim(), reason: '' };
    });
  }
  const d = raw as unknown as PIDecision;
  return { ...d, reviews: d.reviews ?? [], cites: d.cites ?? [], alternatives_rejected: structured };
}

/** Parse timeline.jsonl text into events, tolerating the older actor/event/reason shape. */
export function parseTimeline(raw: string): LabEvent[] {
  return raw.split('\n').filter((l) => l.trim()).map((line, i) => {
    const e = JSON.parse(line) as Record<string, unknown>;
    return {
      i,
      ts: String(e.ts).replace(/Z$/, ''),
      actor: String(e.agent ?? e.actor ?? 'unknown'),
      stage: String(e.stage ?? e.event ?? ''),
      text: String(e.text ?? e.reason ?? ''),
      cites: (e.cites ?? e.files ?? []) as string[],
      decision_id: e.decision_id as string | undefined,
      verdict: e.verdict as Verdict | undefined,
    };
  }).sort((a, b) => a.ts.localeCompare(b.ts) || a.i - b.i);
}
