import type { Hypothesis } from '../data/types';
import { StatusBadge } from './StatusBadge';

export function HypothesisRow({ h }: { h: Hypothesis }) {
  const max = 3;
  return (
    <div className={`hyp-row ${h.status === 'UNTESTED' ? 'is-dim' : ''}`}>
      <span className="hyp-id mono">{h.id}</span>
      <div className="hyp-main">
        <div className="hyp-mech">{h.mechanism}</div>
        <div className="hyp-claim">{h.claim}</div>
      </div>
      <div className="hyp-ev mono" title="supporting / contradicting evidence">
        <span className="ev-bar">
          {Array.from({ length: max }).map((_, i) => (
            <i key={'s' + i} className={i < h.supporting ? 'on-good' : ''} />
          ))}
        </span>
        <span className="fg-good">+{h.supporting}</span>
        <span className="fg-bad">−{h.contradicting}</span>
        <span className="ev-bar">
          {Array.from({ length: max }).map((_, i) => (
            <i key={'c' + i} className={i < h.contradicting ? 'on-bad' : ''} />
          ))}
        </span>
      </div>
      <a className="hyp-link mono" href="#experiment">
        {h.tested_by[0] ?? '—'}
      </a>
      <StatusBadge status={h.status} />
    </div>
  );
}
