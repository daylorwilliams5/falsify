import { useEffect, useState } from 'react';
import type { LabState } from '../../data/types';
import { elapsedSince } from '../../data/view';

export function LabStatus({ roles }: { roles: LabState['roles'] }) {
  return (
    <div className="strip">
      {roles.map((r) => (
        <div key={r.role} className={`strip-cell role-${r.state.toLowerCase()}`}>
          <span className="strip-k">{r.role}</span>
          <span className="strip-v">{r.state === 'RUNNING' && <span className="run-dot" />}{r.detail}</span>
        </div>
      ))}
    </div>
  );
}

export function BudgetStrip({ b }: { b: LabState['budget'] }) {
  const [now, setNow] = useState(Date.now());
  useEffect(() => { const i = setInterval(() => setNow(Date.now()), 30_000); return () => clearInterval(i); }, []);
  const k = (n: number) => (n >= 1000 ? `${(n / 1000).toFixed(1)}k` : String(n));
  const cells = [
    ['Experiments completed', String(b.experiments_completed), `${b.experiments_running} running`],
    ['Model calls used', `${b.model_calls_estimated ? '≈' : ''}${k(b.model_calls_used)}`, 'local model, $0 external'],
    ['Compute remaining', `${k(b.calls_remaining_current)} calls`, `of ${k(b.calls_budget_current)} on current run`],
    ['Research time', elapsedSince(b.research_started, now), 'since loop 1 opened'],
    ['Hypotheses', `${b.hypotheses_eliminated} / ${b.hypotheses_unresolved}`, 'eliminated / unresolved'],
  ];
  return (
    <div className="strip">
      {cells.map(([label, v, sub]) => (
        <div key={label} className="strip-cell">
          <span className="strip-k">{label}</span>
          <span className="strip-num">{v}</span>
          <span className="strip-sub">{sub}</span>
        </div>
      ))}
    </div>
  );
}
