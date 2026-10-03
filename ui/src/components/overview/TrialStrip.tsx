import { useState } from 'react';
import type { Finding, TrialOutcome } from '../../data/types';

const LEGEND: { o: TrialOutcome; label: string }[] = [
  { o: 'measured', label: 'Measured' },
  { o: 'stuck', label: 'Stuck in a loop' },
  { o: 'breach', label: 'Claimed a delivery it couldn’t make' },
];

// One bar per trial, grouped by condition. Hover a bar for that trial; hover a
// legend item to isolate an outcome.
export function TrialStrip({ trials }: { trials: Finding['trials'] }) {
  const [hover, setHover] = useState<number | null>(null);
  const [only, setOnly] = useState<TrialOutcome | null>(null);
  const groups: { condition: string; idx: number[] }[] = [];
  trials.forEach((t, i) => {
    const g = groups.find((x) => x.condition === t.condition);
    if (g) g.idx.push(i); else groups.push({ condition: t.condition, idx: [i] });
  });
  const t = hover !== null ? trials[hover] : null;

  return (
    <div className="ts2" onMouseLeave={() => setHover(null)}>
      <div className="ts2-groups">
        {groups.map((g) => (
          <div key={g.condition} className="ts2-group">
            <div className="ts2-cells">
              {g.idx.map((i) => {
                const tr = trials[i];
                const dim = (only && tr.outcome !== only) || (hover !== null && hover !== i);
                return (
                  <button
                    key={tr.trial}
                    className={`ts2-cell o-${tr.outcome} ${dim ? 'is-dim' : ''} ${hover === i ? 'is-hot' : ''}`}
                    style={{ animationDelay: `${i * 45}ms` }}
                    onMouseEnter={() => setHover(i)}
                    onFocus={() => setHover(i)}
                    onBlur={() => setHover(null)}
                    aria-label={`${tr.trial}: ${tr.detail}`}
                  />
                );
              })}
            </div>
            <div className="ts2-cond">{g.condition}</div>
          </div>
        ))}
      </div>
      <div className="ts2-readout" aria-live="polite">
        {t ? (
          <>
            <span className="ts2-trial"><span className="num">{t.trial}</span> · {t.condition}</span>
            <span className="ts2-detail">{t.detail}</span>
          </>
        ) : (
          <div className="ts2-legend">
            {LEGEND.map(({ o, label }) => (
              <button key={o} className={`lg o-${o} ${only === o ? 'is-on' : ''}`}
                onMouseEnter={() => setOnly(o)} onMouseLeave={() => setOnly(null)} onFocus={() => setOnly(o)} onBlur={() => setOnly(null)}>
                <i />{label} <span className="num">{trials.filter((x) => x.outcome === o).length}</span>
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
