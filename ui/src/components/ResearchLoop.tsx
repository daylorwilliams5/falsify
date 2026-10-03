import { Fragment } from 'react';
import type { LoopStage } from '../data/types';
import { StatusBadge } from './StatusBadge';

export function ResearchLoop({ stages, loopIndex, gated }: { stages: LoopStage[]; loopIndex: number; gated: boolean }) {
  return (
    <div className="loop">
      <div className="loop-row">
        {stages.map((s, i) => {
          const next = stages[i + 1];
          const flowing = next && (next.state === 'RUNNING' || s.state === 'RUNNING');
          return (
            <Fragment key={s.id}>
              <div className={`loop-node state-${s.state.toLowerCase()} ${s.id === 'next' && gated ? 'is-gated' : ''}`}>
                {s.state === 'RUNNING' && <span className="scan" />}
                <div className="ln-top">
                  <span className="ln-idx mono">{String(i + 1).padStart(2, '0')}</span>
                  <StatusBadge status={s.state} />
                </div>
                <div className="ln-label">{s.label}</div>
                <div className="ln-task">{s.task}</div>
                <div className="ln-art">
                  <span className="ln-art-k mono">last artifact</span>
                  <span className="ln-art-v">{s.artifact}</span>
                </div>
                {s.id === 'next' && gated && <div className="gate mono">⏸ HUMAN GATE</div>}
              </div>
              {next && (
                <div className={`loop-edge ${flowing ? 'is-flowing' : ''} ${s.state === 'COMPLETE' ? 'is-done' : ''}`}>
                  <span className="edge-line" />
                  <span className="edge-head">›</span>
                </div>
              )}
            </Fragment>
          );
        })}
      </div>
      <svg className="loop-return" viewBox="0 0 1000 40" preserveAspectRatio="none">
        <path d="M 975 0 L 975 22 Q 975 32 965 32 L 35 32 Q 25 32 25 22 L 25 0" className="ret-path" vectorEffect="non-scaling-stroke" />
        <path d="M 975 0 L 975 22 Q 975 32 965 32 L 35 32 Q 25 32 25 22 L 25 0" className="ret-flow" vectorEffect="non-scaling-stroke" />
      </svg>
      <div className="loop-return-label mono">
        <span>LOOP {loopIndex}</span>
        <span className="muted">→ next experiment feeds back into literature &amp; hypotheses →</span>
        <span>LOOP {loopIndex + 1}</span>
      </div>
    </div>
  );
}
