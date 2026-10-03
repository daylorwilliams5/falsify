import type { TimelineEvent as TE } from '../data/types';

export function TimelineEvent({ e, last }: { e: TE; last?: boolean }) {
  const time = e.ts.slice(11, 16);
  return (
    <div className={`tl-row src-${e.source.toLowerCase()} ${last ? 'is-last' : ''}`}>
      <span className="tl-time mono">{time}</span>
      <span className="tl-rail"><i /></span>
      <div className="tl-body">
        <div className="tl-head">
          <span className="tl-src mono">{e.source}</span>
          <span className="tl-actor mono">{e.actor}</span>
        </div>
        <div className="tl-text">{e.text}</div>
        {e.cites[0] && <div className="tl-cite mono">↳ {e.cites[0]}</div>}
      </div>
    </div>
  );
}
