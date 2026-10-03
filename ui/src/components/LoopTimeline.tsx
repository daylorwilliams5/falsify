import type { Phase } from '../data/types';

// The six-step scientific loop, with the current stage highlighted.
export function LoopTimeline({ phases }: { phases: Phase[] }) {
  const current = phases.find((p) => p.state === 'RUNNING');
  return (
    <div className="loopline">
      <ol className="loopline-track">
        {phases.map((p) => (
          <li key={p.id} className={`ll-step is-${p.state.toLowerCase()}`}>
            <span className="ll-node" />
            <span className="ll-label">{p.label}</span>
          </li>
        ))}
      </ol>
      {current?.note && <p className="loopline-note">{current.note}.</p>}
    </div>
  );
}
