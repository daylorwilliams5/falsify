import type { AgentStatus } from '../data/types';
import { StatusBadge, StatusDot } from './StatusBadge';

export function AgentStatusRow({ a }: { a: AgentStatus }) {
  return (
    <div className={`agent-row state-${a.state.toLowerCase()}`}>
      <StatusDot status={a.state} />
      <div className="agent-main">
        <div className="agent-name">{a.name}</div>
        <div className="agent-sub">
          {a.state === 'RUNNING' ? (
            <><span className="k">task</span> {a.task}</>
          ) : a.artifact ? (
            <><span className="k">artifact</span> <span className="mono artifact">{a.artifact}</span></>
          ) : (
            <span className="muted">{a.role}</span>
          )}
        </div>
      </div>
      <div className="agent-side">
        <StatusBadge status={a.state} />
        <span className="mono muted tiny">{a.tokens ? `${(a.tokens / 1000).toFixed(1)}k tok · ` : ''}{a.updated}</span>
      </div>
    </div>
  );
}
