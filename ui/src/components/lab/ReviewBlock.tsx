import type { ReviewRecord } from '../../data/types';

export function ReviewBlock({ r, decisionId }: { r: ReviewRecord | null; decisionId: string }) {
  const auditing = !r || r.status === 'AUDITING';
  const verdict = r?.verdict;
  return (
    <section className={`obj review ${auditing ? 'is-auditing' : `is-${verdict?.toLowerCase()}`}`}>
      <div className="obj-head"><span className="obj-kind">Methodology review</span><span className="id">{decisionId}</span></div>
      <p className="obj-headline review-verdict">
        {auditing ? <><span className="audit-dot" />Auditing…</> : verdict}
      </p>
      <ul className="checks">
        {r?.checks.map((c, i) => (
          <li key={c.id} className={auditing ? 'is-pending' : c.ok ? 'is-ok' : 'is-fail'} style={{ animationDelay: `${i * 0.35}s` }}>
            <span className="check-mark">{auditing ? '' : c.ok ? '✓' : '✕'}</span>
            {c.label}
          </li>
        ))}
      </ul>
      <p className="review-note">
        {auditing ? 'Independent of the PI. The decision proceeds at Level 1 while the audit runs.' : 'Independent of the PI.'}
      </p>
      <a className="obj-link" href="#/decisions">Audit record <span>→</span></a>
    </section>
  );
}
