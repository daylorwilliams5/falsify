import type { Phase } from '../data/types';

// How Falsify works, in plain words. Internal loop stages map onto these five.
export const PLAIN_PHASES = [
  ['read', 'Read the research'],
  ['hypothesis', 'Form a hypothesis'],
  ['experiment', 'Run an experiment'],
  ['challenge', 'Challenge the result'],
  ['next', 'Decide what to test next'],
] as const;

export const PLAIN_STAGE: Record<string, string> = {
  literature: 'read', hypothesis: 'hypothesis', experiment: 'experiment', result: 'experiment',
  critique: 'challenge', review: 'challenge', decision: 'next', next: 'next', design: 'experiment',
};

export const LAB_PHASES = [
  ['literature', 'Literature'],
  ['hypothesis', 'Hypothesis'],
  ['experiment', 'Experiment'],
  ['result', 'Result'],
  ['critique', 'Critique'],
  ['decision', 'PI decision'],
  ['review', 'Methodology review'],
  ['next', 'Next experiment'],
] as const;

export const PHASES = [
  ['literature', 'Literature'],
  ['hypothesis', 'Hypothesis'],
  ['experiment', 'Experiment'],
  ['result', 'Result'],
  ['critique', 'Critique'],
  ['next', 'Next experiment'],
] as const;

/** Build the six-step loop with everything before `current` complete. */
export function phasesAt(current: string, note?: string, list: readonly (readonly [string, string])[] = PHASES): Phase[] {
  const i = list.findIndex(([id]) => id === current);
  return list.map(([id, label], j) => ({
    id, label,
    state: j < i ? 'COMPLETE' : j === i ? 'RUNNING' : 'QUEUED',
    note: j === i ? note : undefined,
  }));
}

// The six-step scientific loop, with the current stage highlighted.
export function LoopTimeline({ phases }: { phases: Phase[] }) {
  const current = phases.find((p) => p.state === 'RUNNING');
  return (
    <div className="loopline">
      <ol className="loopline-track" style={{ gridTemplateColumns: `repeat(${phases.length}, 1fr)` }}>
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

/** Compact loop for list rows: six dots, current one lit, label underneath. */
export function LoopDots({ current }: { current: string }) {
  const phases = phasesAt(current);
  const label = phases.find((p) => p.state === 'RUNNING')?.label;
  return (
    <div className="loopdots" title={`Current stage: ${label}`}>
      <span className="ld-track">
        {phases.map((p) => <i key={p.id} className={`is-${p.state.toLowerCase()}`} />)}
      </span>
      <span className="ld-label">{label}</span>
    </div>
  );
}
