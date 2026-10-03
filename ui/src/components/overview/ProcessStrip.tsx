import { useState } from 'react';
import { PLAIN_PHASES } from '../LoopTimeline';

// How Falsify works: five steps, the current one lit. Hover any step to see
// what the lab most recently did there.
export function ProcessStrip({ current, captions }: { current: string; captions: { id: string; caption: string }[] }) {
  const ci = Math.max(0, PLAIN_PHASES.findIndex(([id]) => id === current));
  const [hover, setHover] = useState<number | null>(null);
  const shown = hover ?? ci;
  const caption = captions.find((c) => c.id === PLAIN_PHASES[shown][0])?.caption;
  const pct = (ci / (PLAIN_PHASES.length - 1)) * 100;

  return (
    <div className="proc" onMouseLeave={() => setHover(null)}>
      <div className="proc-track">
        <span className="proc-rail" />
        <span className="proc-fill" style={{ width: `${pct}%` }} />
        <span className="proc-comet" style={{ left: `${pct}%` }} />
        {PLAIN_PHASES.map(([id, label], i) => (
          <button
            key={id}
            className={`proc-step ${i < ci ? 'is-done' : i === ci ? 'is-now' : ''} ${shown === i ? 'is-shown' : ''}`}
            style={{ left: `${(i / (PLAIN_PHASES.length - 1)) * 100}%` }}
            onMouseEnter={() => setHover(i)}
            onFocus={() => setHover(i)}
          >
            <span className="proc-node" />
            <span className="proc-label">{label}</span>
          </button>
        ))}
      </div>
      <p className="proc-caption" key={shown}>
        {shown === ci && <span className="proc-now">Now · </span>}
        {caption}
      </p>
    </div>
  );
}
