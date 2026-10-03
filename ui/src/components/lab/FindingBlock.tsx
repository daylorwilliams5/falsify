import type { Finding } from '../../data/types';

export function FindingBlock({ f }: { f: Finding }) {
  const seeds = new Set(f.persistence_events.map((e) => e.seed));
  const n = f.persistence_events.length;
  return (
    <section className="obj">
      <div className="obj-head"><span className="obj-kind">Latest finding</span><span className="id">{f.label}</span></div>
      <p className="obj-headline">{f.headline}</p>
      <div className="ratio">
        <span className="ratio-num num">{f.corrected_immediately} / {f.invalidating_trials}</span>
        <span className="ratio-label">corrected immediately</span>
      </div>
      <span className="ratio-bar"><i style={{ width: `${(f.corrected_immediately / f.invalidating_trials) * 100}%` }} /></span>
      {n > 0 && (
        <p className="ratio-note">{n} persistence {n === 1 ? 'event' : 'events'} · {seeds.size === 1 ? 'same seed' : `${seeds.size} seeds`}</p>
      )}
      <p className="obj-verdict"><strong>{f.status.charAt(0) + f.status.slice(1).toLowerCase()}</strong> · {f.status_reason}</p>
      <a className="obj-link" href="#/experiments">View experiment <span>→</span></a>
    </section>
  );
}
