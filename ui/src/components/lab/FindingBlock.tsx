import type { Finding } from '../../data/types';
import { TrialStrip } from './TrialStrip';

export function FindingBlock({ f }: { f: Finding }) {
  const n = f.invalidating_trials_wasted_actions.length;
  const ok = f.invalidating_trials_wasted_actions.filter((w) => w === 0).length;
  return (
    <section className="obj">
      <div className="obj-head"><span className="obj-kind">Latest finding</span><span className="id">{f.label}</span></div>
      <p className="obj-headline">{f.headline}</p>
      <TrialStrip wasted={f.invalidating_trials_wasted_actions} />
      <p className="obj-line"><span className="num">{ok}/{n}</span> invalidating trials corrected immediately.</p>
      <p className="obj-verdict"><strong>{f.status.charAt(0) + f.status.slice(1).toLowerCase()}</strong> · {f.status_reason}</p>
      <a className="obj-link" href="#/experiments">View experiment <span>→</span></a>
    </section>
  );
}
