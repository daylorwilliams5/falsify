import { useState } from 'react';
import type { PIDecision } from '../data/types';
import { latestReview, OUTCOME_LABEL, type Outcome, outcomeOf } from '../data/view';
import { Powers } from '../components/decisions/Powers';
import { CorrectionStory } from '../components/decisions/CorrectionStory';
import { DecisionEntry } from '../components/decisions/DecisionEntry';

const MAIN: Outcome[] = ['ACCEPTED', 'CORRECTED', 'ESCALATED'];

export function DecisionsPage({ decisions, focus }: { decisions: PIDecision[]; focus?: string }) {
  const [filter, setFilter] = useState<Outcome | null>(null);
  const outcomes = new Map(decisions.map((d) => [d.id, outcomeOf(d, decisions)]));
  const count = (o: Outcome) => decisions.filter((d) => outcomes.get(d.id) === o).length;
  const inReview = count('IN_REVIEW') + count('OPEN');

  // Feature the first decision that a reviewer blocked and the PI then corrected.
  const failed = decisions.find((d) => ['FAIL', 'BLOCK'].includes(latestReview(d)?.verdict ?? '') && outcomes.get(d.id) === 'CORRECTED');
  const correction = failed && decisions.find((x) => x.responds_to?.includes(failed.id));

  const shown = [...decisions].reverse().filter((d) => {
    if (!filter) return true;
    const o = outcomes.get(d.id)!;
    return filter === 'IN_REVIEW' ? o === 'IN_REVIEW' || o === 'OPEN' : o === filter;
  });

  return (
    <div className="dec">
      <div className="label">Decisions</div>
      <h1 className="dec-title">How the lab decides</h1>
      <Powers />

      <div className="tally">
        {MAIN.map((o) => (
          <button key={o} className={`tally-cell ${filter === o ? 'is-on' : ''}`} onClick={() => setFilter(filter === o ? null : o)}>
            <span className="tally-num num">{count(o)}</span>
            <span className="tally-label">{OUTCOME_LABEL[o]}</span>
          </button>
        ))}
        <button className={`tally-cell tally-minor ${filter === 'IN_REVIEW' ? 'is-on' : ''}`} onClick={() => setFilter(filter === 'IN_REVIEW' ? null : 'IN_REVIEW')}>
          <span className="tally-num num">{inReview}</span>
          <span className="tally-label">In review</span>
        </button>
      </div>

      {failed && correction && !filter && <CorrectionStory original={failed} correction={correction} />}

      <section className="journal">
        <div className="label">
          Decision journal
          {filter && <button className="clear" onClick={() => setFilter(null)}>Show all</button>}
        </div>
        {shown.map((d) => (
          <DecisionEntry key={d.id} d={d} all={decisions} outcome={outcomes.get(d.id)!} focused={d.id === focus} />
        ))}
      </section>
    </div>
  );
}
