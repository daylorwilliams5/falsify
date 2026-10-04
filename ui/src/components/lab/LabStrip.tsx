import type { Budget, LabState } from '../../data/types';

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

export function BudgetStrip({ b }: { b: Budget }) {
  const h = Math.floor(b.elapsed_research_minutes / 60), m = Math.round(b.elapsed_research_minutes % 60);
  const cells = [
    ['Experiments completed', String(b.experiments_completed), `${b.trials_run} trials · ${b.subject_models.length} AI models`],
    ['Model calls used', b.model_calls_used.toLocaleString(), b.subject_models.join(' + ')],
    ['Outside spend', `$${b.external_spend_usd.toFixed(2)}`, `of a $${b.external_spend_cap_usd} cap the human set`],
    ['Research time', `${h}h ${String(m).padStart(2, '0')}m`, `as of ${b.as_of.slice(11, 16)}`],
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
