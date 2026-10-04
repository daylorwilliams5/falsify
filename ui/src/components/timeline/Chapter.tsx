import { useState } from 'react';
import type { LabEvent, LabState, PIDecision } from '../../data/types';
import {
  actorLabel, eventHeadline, eventKind, hhmm, hhmmss, isKeyMoment, latestReview, respondersTo, shortCite, verdictLabel, verdictTone,
} from '../../data/view';

type Loop = LabState['loops'][number];

// One research loop: what it was about, then what happened, in order.
export function Chapter({ loop, events, decisions, showAll, selected, onSelect }: {
  loop: Loop; events: LabEvent[]; decisions: PIDecision[]; showAll: boolean;
  selected: number | null; onSelect: (i: number | null) => void;
}) {
  const [expanded, setExpanded] = useState(false);
  const key = events.filter(isKeyMoment);
  const shown = showAll || expanded ? events.filter((e) => e.stage !== 'methodology_review' || showAll) : key;
  const hidden = events.length - key.length;
  const nDecisions = events.filter((e) => e.stage === 'pi_decision').length;
  const nRuns = events.filter((e) => e.stage === 'experiment_started').length;

  return (
    <section id={`loop-${loop.n}`} className="ch">
      <header className="ch-head">
        <div className="ch-when num">{hhmm(loop.start)}{loop.end ? `–${hhmm(loop.end)}` : ' onward'}</div>
        <div className="ch-label">{loop.label}</div>
        <h2 className="ch-title">{loop.title ?? loop.sub}</h2>
        {loop.summary && <p className="ch-summary">{loop.summary}</p>}
        <p className="ch-meta">
          {nDecisions} decision{nDecisions === 1 ? '' : 's'} · {nRuns} experiment{nRuns === 1 ? '' : 's'} run · {events.length} events
          {loop.ended && <span className="ch-ended"> · {loop.ended}</span>}
        </p>
      </header>

      <ol className="ch-list">
        {shown.map((e) => (
          <Moment key={e.i} e={e} decisions={decisions} open={selected === e.i} onToggle={() => onSelect(selected === e.i ? null : e.i)} />
        ))}
      </ol>

      {!showAll && hidden > 0 && (
        <button className="ch-more" onClick={() => setExpanded((v) => !v)}>
          {expanded ? 'Show key moments only' : `Show ${hidden} more events (reviews, agent notes, engineering)`}
        </button>
      )}
    </section>
  );
}

function Moment({ e, decisions, open, onToggle }: { e: LabEvent; decisions: PIDecision[]; open: boolean; onToggle: () => void }) {
  const kind = eventKind(e);
  const d = e.stage === 'pi_decision' && e.decision_id ? decisions.find((x) => x.id === e.decision_id) : undefined;
  return (
    <li className={`mo k-${kind} ${open ? 'is-open' : ''}`}>
      <span className="mo-time num">{hhmm(e.ts)}</span>
      <span className="mo-dot" aria-hidden />
      <div className="mo-body">
        <button className="mo-main" onClick={onToggle} aria-expanded={open}>
          <span className="mo-who">{actorLabel(e.actor)}{d && <span className="num"> · {d.id}</span>}</span>
          <span className="mo-text">{eventHeadline(e, decisions)}</span>
        </button>
        {d && <Thread d={d} all={decisions} />}
        {open && (
          <div className="mo-detail">
            <div className="mo-full">{e.text}</div>
            {e.cites.length > 0 && <div className="mo-cites">{e.cites.map((c) => <span key={c} className="num" title={c}>{shortCite(c)}</span>)}</div>}
            <div className="mo-foot"><span className="num">{hhmmss(e.ts)}</span>{d && <a href={`#/decisions/${d.id}`}>Open {d.id} in Decisions →</a>}</div>
          </div>
        )}
      </div>
    </li>
  );
}

// What happened to a decision afterwards, inline: review → correction → human.
function Thread({ d, all }: { d: PIDecision; all: PIDecision[] }) {
  const r = latestReview(d);
  const first = d.reviews[0];
  const later = respondersTo(d, all);
  if (!r && !later.length && !d.human_approval) return <div className="th"><span className="th-chip th-wait">Not yet reviewed</span></div>;
  return (
    <div className="th">
      {first && first !== r && (
        <span className={`th-chip v-${verdictTone(first.verdict)}`}>Review <b className="num">{verdictLabel(first.verdict)}</b> {hhmm(first.ts)}</span>
      )}
      {r && <span className={`th-chip v-${verdictTone(r.verdict)}`}>{first !== r ? 'Then' : 'Review'} <b className="num">{verdictLabel(r.verdict)}</b> {hhmm(r.ts)}</span>}
      {d.human_approval && <span className="th-chip th-human">Human approved {hhmm(d.human_approval.ts)}</span>}
      {later.map((x) => (
        <a key={x.id} className="th-chip th-link" href={`#/decisions/${x.id}`}>→ {x.id} responded {hhmm(x.ts)}</a>
      ))}
    </div>
  );
}
