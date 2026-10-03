import type { PIDecision, RejectedAlternative } from '../types';

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
