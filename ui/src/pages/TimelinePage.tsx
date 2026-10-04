import { useEffect, useMemo, useRef, useState } from 'react';
import type { LabView, LabEvent } from '../data/types';
import { eventHeadline, eventKind, hhmm, hhmmss, LANES, type LaneId, laneOf, shortCite, stoppedByReviewer } from '../data/view';
import { SwimLanes, actorLabel } from '../components/timeline/SwimLanes';

const KIND_LABEL = {
  decision: 'Decision', 'review-fail': 'Review: failed', review: 'Review', directive: 'Human directive',
  run: 'Experiment', fix: 'Fix', note: 'Note',
} as const;

export function TimelinePage({ lab, focus }: { lab: LabView; focus?: string }) {
  const { events, decisions, state } = lab;
  const [selected, setSelected] = useState<LabEvent | null>(null);
  const [laneFocus, setLaneFocus] = useState<LaneId | null>(null);
  const detailRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!focus) return;
    const e = events.find((x) => x.decision_id === focus && x.stage === 'pi_decision');
    if (e) setSelected(e);
  }, [focus, events]);

  const select = (e: LabEvent, scroll = false) => {
    setSelected(e);
    if (scroll) detailRef.current?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  };

  const stats = useMemo(() => {
    return [
      [events.length, 'events'],
      [decisions.length, 'decisions'],
      [events.filter((e) => e.stage === 'methodology_review').length, 'independent reviews'],
      [stoppedByReviewer(decisions).length, 'decisions stopped by the reviewer'],
      [decisions.filter((d) => d.human_approval).length, 'human approvals'],
    ] as const;
  }, [events, decisions]);

  const shown = laneFocus ? events.filter((e) => laneOf(e.actor) === laneFocus) : events;
  // Each event belongs to the last loop that had started by then.
  const loopOf = (e: LabEvent) => [...state.loops].reverse().find((lp) => e.ts >= lp.start) ?? null;
  const groups = [null, ...state.loops].map((lp) => ({ lp, items: shown.filter((e) => loopOf(e) === lp) }));

  return (
    <div className="tl2">
      <div className="label">Timeline</div>
      <h1 className="dec-title">Everything the lab did, in order</h1>
      <p className="tl2-asof">Snapshot of the lab’s record through <span className="num">{hhmm(events[events.length - 1].ts)}</span>, October 3.</p>

      <div className="tl2-stats">
        {stats.map(([n, label]) => (
          <div key={label}><span className="num">{n}</span>{label}</div>
        ))}
      </div>

      <SwimLanes events={events} decisions={decisions} loops={state.loops} runs={state.runs}
        selected={selected} onSelect={(e) => select(e, true)} laneFocus={laneFocus} onLaneFocus={setLaneFocus} />

      <div ref={detailRef} className={`tl2-detail ${selected ? 'is-on' : ''}`}>
        {selected ? <EventDetail e={selected} lab={lab} onClose={() => setSelected(null)} /> : (
          <p className="tl2-empty">Click any mark to read the full entry.</p>
        )}
      </div>

      <section className="tl2-list">
        <div className="label">
          {laneFocus ? `${LANES.find((l) => l.id === laneFocus)?.label} only` : 'Full log'}
          {laneFocus && <button className="clear" onClick={() => setLaneFocus(null)}>Show all</button>}
        </div>
        {groups.map(({ lp, items }) => items.length > 0 && (
          <div key={lp?.n ?? 0} className="tl2-loop">
            <div className="tl2-loop-head">
              <span>{lp ? lp.label : 'Before Loop 1'}</span>
              {lp && <span className="muted">{lp.sub} · <span className="num">{hhmm(lp.start)}{lp.end ? `–${hhmm(lp.end)}` : ' onward'}</span></span>}
              {lp?.ended && <span className="tl2-ended">{lp.ended}</span>}
            </div>
            {items.map((e) => <Row key={e.i} e={e} lab={lab} sel={selected?.i === e.i} onClick={() => select(e, true)} />)}
          </div>
        ))}
      </section>
    </div>
  );
}

function Row({ e, lab, sel, onClick }: { e: LabEvent; lab: LabView; sel: boolean; onClick: () => void }) {
  const kind = eventKind(e);
  return (
    <button className={`tl2-row k-${kind} ${sel ? 'is-sel' : ''}`} onClick={onClick}>
      <span className="tl2-time num">{hhmm(e.ts)}</span>
      <span className={`mark k-${kind}`} />
      <span className="tl2-actor">{actorLabel(e.actor)}</span>
      <span className="tl2-text">{eventHeadline(e, lab.decisions)}</span>
    </button>
  );
}

function EventDetail({ e, lab, onClose }: { e: LabEvent; lab: LabView; onClose: () => void }) {
  const kind = eventKind(e);
  const d = e.decision_id ? lab.decisions.find((x) => x.id === e.decision_id) : undefined;
  return (
    <div className="ed">
      <div className="ed-head">
        <span className={`mark k-${kind}`} />
        <span className="num">{hhmmss(e.ts)}</span>
        <span>{actorLabel(e.actor)}</span>
        <span className="muted">{KIND_LABEL[kind]}</span>
        {e.decision_id && <span className="num">{e.decision_id}</span>}
        <button className="ed-close" onClick={onClose} aria-label="Close">×</button>
      </div>
      <p className="ed-headline">{eventHeadline(e, lab.decisions)}</p>
      <div className="ed-text">{e.text}</div>
      {e.cites.length > 0 && <div className="ed-cites">{e.cites.map((c) => <span key={c} className="num" title={c}>{shortCite(c)}</span>)}</div>}
      {d && <a className="h2-link ed-link" href={`#/decisions/${d.id}`}>Open {d.id} in Decisions <span>→</span></a>}
    </div>
  );
}
