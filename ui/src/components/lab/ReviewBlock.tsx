import type { PIDecision } from '../../data/types';
import { CHECK_LABEL, latestReview, reviewChecks, STANDARD_CHECKS, verdictLabel, verdictTone } from '../../data/view';

export function ReviewBlock({ d, auditing }: { d: PIDecision; auditing: boolean }) {
  const r = latestReview(d);
  const checks = r ? reviewChecks(r) : STANDARD_CHECKS.map((k) => ({ label: CHECK_LABEL[k], ok: true }));
  const pending = !r;
  return (
    <section className={`obj review ${pending ? 'is-auditing' : `is-${verdictTone(r.verdict)}`}`}>
      <div className="obj-head"><span className="obj-kind">Methodology review</span><span className="id">{d.id}</span></div>
      <p className="obj-headline review-verdict">
        {pending ? <>{auditing && <span className="audit-dot" />}{auditing ? 'Auditing…' : 'Review pending'}</> : verdictLabel(r.verdict)}
      </p>
      {r?.highlights && <p className="review-gist">{r.highlights[0]}</p>}
      <ul className="checks">
        {checks.map((c, i) => (
          <li key={c.label} className={pending ? 'is-pending' : c.ok ? 'is-ok' : 'is-fail'} style={{ animationDelay: `${i * 0.35}s` }}>
            <span className="check-mark">{pending ? '' : c.ok ? '✓' : '✕'}</span>
            {c.label}
          </li>
        ))}
      </ul>
      <p className="review-note">
        {pending ? 'Independent of the PI. Level 1 decisions proceed while the audit runs.' : 'Independent of the PI.'}
      </p>
      <a className="obj-link" href={`#/decisions/${d.id}`}>Audit record <span>→</span></a>
    </section>
  );
}
