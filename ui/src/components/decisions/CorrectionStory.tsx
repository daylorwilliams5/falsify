import type { PIDecision } from '../../data/types';
import { hhmm, latestReview, minutesBetween, verdictLabel } from '../../data/view';

// D → review FAIL → correction → (no) human. The architecture in one sequence.
export function CorrectionStory({ original, correction }: { original: PIDecision; correction: PIDecision }) {
  const review = latestReview(original)!;
  const mins = minutesBetween(original.ts, correction.ts);
  const human = correction.human_intervention ?? original.human_intervention;
  return (
    <section className="story">
      <div className="label">A decision that failed review</div>
      <ol className="story-steps">
        <li>
          <div className="st-kind"><span className="id">{original.id}</span>PI decision<span className="st-time num">{hhmm(original.ts)}</span></div>
          <p className="st-text">{original.summary}</p>
        </li>
        <li className="is-fail">
          <div className="st-kind">Methodology review<span className="st-time num">{hhmm(review.ts)}</span></div>
          <p className="st-verdict num">{verdictLabel(review.verdict)}</p>
          {review.highlights && <ul className="st-findings">{review.highlights.map((h) => <li key={h}>{h}</li>)}</ul>}
        </li>
        <li>
          <div className="st-kind"><span className="id">{correction.id}</span>PI correction<span className="st-time num">{hhmm(correction.ts)}</span></div>
          <p className="st-text">{correction.summary}</p>
          {correction.resulting_action && <p className="st-result">{correction.resulting_action}</p>}
        </li>
        <li className="is-end">
          <div className="st-kind">Human</div>
          <p className="st-text st-quiet">{human ? human.text : 'No intervention.'}</p>
        </li>
      </ol>
      <p className="story-foot">
        Caught and corrected inside the lab in <span className="num">{mins}</span> minutes.
        {!human && ' Nobody had to step in.'}
      </p>
      <a className="obj-link" href={`#/decisions/${correction.id}`}>Read both records <span>→</span></a>
    </section>
  );
}
