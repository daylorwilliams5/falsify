import { useState } from 'react';
import type { NextDecision } from '../data/types';
import { StatusBadge } from './StatusBadge';

const LVL = { HIGH: 3, MEDIUM: 2, LOW: 1 } as const;

function Level({ v, invert }: { v: keyof typeof LVL; invert?: boolean }) {
  return (
    <span className={`lvl ${invert ? 'lvl-inv' : ''}`}>
      {[1, 2, 3].map((i) => <i key={i} className={i <= LVL[v] ? 'on' : ''} />)}
      <b className="mono">{v}</b>
    </span>
  );
}

export function DecisionCard({ d }: { d: NextDecision }) {
  const sel = d.options.find((o) => o.id === d.selected);
  const [local, setLocal] = useState<null | 'approve' | 'reject' | 'rationale'>(null);
  return (
    <div className="decision">
      <div className="dec-head">
        <div>
          <div className="dec-kicker mono"><span className="pulse-dot accent" /> NEXT EXPERIMENT PROPOSED</div>
          <div className="dec-by">by {d.proposed_by} · awaiting human approval</div>
        </div>
        <StatusBadge status="PROPOSED" size="md" />
      </div>

      <div className="dec-options">
        {d.options.map((o) => {
          const sel = o.id === d.selected;
          return (
            <div key={o.id} className={`dec-opt ${sel ? 'is-selected' : ''}`}>
              <div className="opt-top">
                <span className="opt-label mono">{o.label}</span>
                {sel && <span className="opt-sel mono">● SELECTED</span>}
              </div>
              <div className="opt-title">{o.title}</div>
              <div className="opt-tests"><span className="k mono">TESTS</span>{o.tests}</div>
              <div className="opt-stats">
                <div><span className="k mono">info gain</span><Level v={o.info_gain} /></div>
                <div><span className="k mono">build</span><span className={`mono ${o.build === 'READY' ? 'fg-good' : ''}`}>{o.build}</span></div>
                <div><span className="k mono">run cost</span><Level v={o.cost} invert /></div>
              </div>
              <div className="opt-foot mono">
                {o.hypotheses.map((h) => <span key={h} className="chip">{h}</span>)}
                <span className="muted">{o.spec}</span>
              </div>
            </div>
          );
        })}
      </div>

      <blockquote className="dec-reason">
        <span className="k mono">REASON</span>
        “{d.reason}”
      </blockquote>

      {sel && (
        <div className="dec-plan">
          <div><span className="k mono">IF APPROVED</span><span className="mono">{sel.spec.split('/').pop()?.replace('.json', '')}</span></div>
          <div><span className="k mono">DESIGN</span><span>{sel.design}</span></div>
          <div><span className="k mono">TRIALS</span><span className="mono">{sel.trials}</span></div>
          <div className="dec-fals"><span className="k mono">FALSIFIED IF</span><span>{sel.falsified_if}</span></div>
        </div>
      )}

      <div className="dec-actions">
        <button className="btn btn-primary" onClick={() => setLocal('approve')}>Approve experiment</button>
        <button className="btn" onClick={() => setLocal('reject')}>Reject</button>
        <button className="btn btn-ghost" onClick={() => setLocal('rationale')}>View rationale ↗</button>
        {local && (
          <span className="dec-note mono">
            {local === 'rationale' ? d.rationale_path : `${local} · not wired (fixture mode)`}
          </span>
        )}
      </div>
    </div>
  );
}
