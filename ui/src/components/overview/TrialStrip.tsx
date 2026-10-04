import { useState } from 'react';
import type { Finding, TrialOutcome } from '../../data/types';

// One bar per trial. Conditions named "Row · Column" are laid out as a grid
// (e.g. Solo/Team × evidence type). Hover a bar for that trial; hover a
// legend item to isolate an outcome.
export function TrialStrip({ trials, legend }: { trials: Finding['trials']; legend: Finding['legend'] }) {
  const [hover, setHover] = useState<number | null>(null);
  const [only, setOnly] = useState<TrialOutcome | null>(null);
  const tone = (o: TrialOutcome) => legend.find((l) => l.outcome === o)?.tone ?? 'light';

  const split = (c: string) => { const [r, ...rest] = c.split(' · '); return [r, rest.join(' · ') || r]; };
  const rows = [...new Set(trials.map((t) => split(t.condition)[0]))];
  const cols = [...new Set(trials.map((t) => split(t.condition)[1]))];
  const at = (r: string, c: string) => trials.map((t, i) => ({ t, i })).filter(({ t }) => {
    const [tr, tc] = split(t.condition); return tr === r && tc === c;
  });
  const h = hover !== null ? trials[hover] : null;

  return (
    <div className="ts2" onMouseLeave={() => setHover(null)}>
      <div className="ts2-grid" style={{ gridTemplateColumns: `auto repeat(${cols.length}, 1fr)` }}>
        <span />
        {cols.map((c) => <span key={c} className="ts2-col">{c}</span>)}
        {rows.map((r) => (
          <div key={r} className="ts2-rowwrap" style={{ display: 'contents' }}>
            <span className="ts2-row">{r}</span>
            {cols.map((c) => (
              <div key={c} className="ts2-cells">
                {at(r, c).map(({ t, i }) => {
                  const dim = (only && t.outcome !== only) || (hover !== null && hover !== i);
                  return (
                    <button
                      key={t.trial}
                      className={`ts2-cell t-${tone(t.outcome)} ${dim ? 'is-dim' : ''} ${hover === i ? 'is-hot' : ''}`}
                      style={{ animationDelay: `${i * 12}ms` }}
                      onMouseEnter={() => setHover(i)}
                      onFocus={() => setHover(i)}
                      onBlur={() => setHover(null)}
                      aria-label={`${t.trial}, ${t.condition}: ${t.detail}`}
                    />
                  );
                })}
              </div>
            ))}
          </div>
        ))}
      </div>
      <div className="ts2-readout" aria-live="polite">
        {h ? (
          <>
            <span className="ts2-trial"><span className="num">{h.trial}</span> · {h.condition}</span>
            <span className="ts2-detail">{h.detail}</span>
          </>
        ) : (
          <div className="ts2-legend">
            {legend.map(({ outcome, label, tone: tn }) => (
              <button key={outcome} className={`lg t-${tn} ${only === outcome ? 'is-on' : ''}`}
                onMouseEnter={() => setOnly(outcome)} onMouseLeave={() => setOnly(null)} onFocus={() => setOnly(outcome)} onBlur={() => setOnly(null)}>
                <i />{label} <span className="num">{trials.filter((x) => x.outcome === outcome).length}</span>
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
