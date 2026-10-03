import type { TraceSpan } from '../data/types';

const KIND: Record<TraceSpan['kind'], string> = { agent: 'AGT', tool: 'TOOL', llm: 'LLM', read: 'READ', write: 'WRITE' };

export function TraceRow({ span, total, now }: { span: TraceSpan; total: number; now: number }) {
  const dur = span.duration ?? Math.max(now - span.start, 0.5);
  const left = (span.start / total) * 100;
  const width = Math.max((dur / total) * 100, 0.6);
  return (
    <div className={`trace-row state-${span.state.toLowerCase()}`}>
      <div className="trace-name" style={{ paddingLeft: span.depth * 16 }}>
        {span.depth > 0 && <span className="trace-elbow" />}
        <span className={`trace-kind kind-${span.kind}`}>{KIND[span.kind]}</span>
        <span className="mono trace-fn">{span.name}</span>
        {span.detail && <span className="trace-detail">{span.detail}</span>}
      </div>
      <div className="trace-wf">
        {span.state !== 'QUEUED' && (
          <span className={`trace-bar ${span.duration === null ? 'is-live' : ''}`} style={{ left: `${left}%`, width: `${width}%` }} />
        )}
      </div>
      <div className="trace-dur mono">
        {span.state === 'QUEUED' ? 'queued' : span.duration === null ? `${dur.toFixed(1)}s…` : `${span.duration.toFixed(1)}s`}
      </div>
    </div>
  );
}
