import { useEffect, useState } from 'react';
import type { Budget, LabState, Mandate } from '../../data/types';
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

export function BudgetStrip({ b, mandate }: { b: Budget; mandate: Mandate }) {
  const [now, setNow] = useState(Date.now());
  useEffect(() => { const i = setInterval(() => setNow(Date.now()), 30_000); return () => clearInterval(i); }, []);
  // Research clock starts where the budget report says it did.
  const started = new Date(new Date(b.as_of).getTime() - b.elapsed_research_minutes * 60000).toISOString();
  const cells = [
    ['Experiments completed', String(b.experiments_completed), `${b.trials_run} trials`],
    ['Model calls used', b.model_calls_used.toLocaleString(), `local model · $${b.external_spend_usd.toFixed(0)} external`],
    ['Per-experiment limit', `${mandate.budget.max_trials_per_experiment_level1} trials`, 'before review is required'],
    ['Research time', elapsedSince(started, now), 'since loop 1 opened'],
    ['Hypotheses', `${b.hypotheses_eliminated.length} / ${b.unresolved.length}`, 'eliminated / unresolved'],
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
