import type { PIDecision } from '../../data/types';
import { decisionReason, decisionTitle, LEVEL_LABEL, rejectedAlternative } from '../../data/view';

export function DecisionBlock({ d }: { d: PIDecision }) {
  const [verb, ...rest] = decisionTitle(d).split(' ');
  const rejected = rejectedAlternative(d);
  return (
    <section className="obj">
      <div className="obj-head"><span className="obj-kind">PI decision</span><span className="id">{d.id}</span></div>
      <p className="obj-headline">{verb} <span className="id-lg">{rest.join(' ')}</span></p>
      <p className="obj-level">Level {d.level} — {LEVEL_LABEL[d.level].toLowerCase()}</p>
      <blockquote className="obj-quote">“{decisionReason(d)}”</blockquote>
      <div className="obj-conf">
        <span>Confidence</span>
        <span className="conf-bar"><i style={{ width: `${d.confidence * 100}%` }} /></span>
        <span className="num">{d.confidence.toFixed(2)}</span>
      </div>
      {rejected && <p className="obj-rejected"><span>Rejected alternative</span>{rejected}</p>}
      <a className="obj-link" href="#/decisions">View decision <span>→</span></a>
    </section>
  );
}
