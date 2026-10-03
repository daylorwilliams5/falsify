import type { PIDecision } from '../../data/types';
import { decisionHeadline, LEVEL_LABEL } from '../../data/view';

export function DecisionBlock({ d }: { d: PIDecision }) {
  const h = decisionHeadline(d);
  const rejected = d.alternatives_rejected[0];
  return (
    <section className="obj">
      <div className="obj-head"><span className="obj-kind">PI decision</span><span className="id">{d.id}</span></div>
      <p className="obj-headline">{h.text ?? <>{h.verb} <span className="id-lg">{h.target}</span></>}</p>
      <p className="obj-level">Level {d.level} — {LEVEL_LABEL[d.level].toLowerCase()}</p>
      {d.rationale && <blockquote className="obj-quote">“{d.rationale}”</blockquote>}
      <div className="obj-conf">
        <span>Confidence</span>
        <span className="conf-bar"><i style={{ width: `${d.confidence * 100}%` }} /></span>
        <span className="num">{d.confidence.toFixed(2)}</span>
      </div>
      {rejected && <p className="obj-rejected"><span>Rejected alternative</span>{rejected.label}</p>}
      <a className="obj-link" href={`#/decisions/${d.id}`}>View decision <span>→</span></a>
    </section>
  );
}
