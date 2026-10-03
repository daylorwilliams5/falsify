import type { LabView } from './data/types';
import { LoopTimeline, PLAIN_PHASES, PLAIN_STAGE, phasesAt } from './components/LoopTimeline';
import { EscalationCard } from './components/lab/HumanControl';
import { PLAIN_STATUS } from './data/view';

// The front page: three plain-language answers. Lab internals live on detail pages.
export function LabOverview({ lab }: { lab: LabView }) {
  const { mandate, finding, state } = lab;
  const x = state.active_experiment;
  const finished = x.done === x.total;
  const reviewing = !!state.reviewer.auditing;

  return (
    <div className="home2">
      <section className="h2-question">
        <div className="h2-label">What we’re trying to understand</div>
        <h1>{mandate.plain_question}</h1>
      </section>

      {state.escalations.map((e) => <EscalationCard key={e.id} e={e} />)}

      <div className="h2-pair">
        <section className="h2-block">
          <div className="h2-label">What we learned</div>
          <p className="h2-headline">{finding.plain_headline}</p>
          <div className="h2-figure">
            <span className="h2-num num">{finding.corrected_immediately} / {finding.invalidating_trials}</span>
            <span className="h2-unit">corrected course immediately</span>
          </div>
          <p className="h2-status">
            <span className="h2-status-k">Result</span>{PLAIN_STATUS[finding.status]}
          </p>
          <p className="h2-why">{finding.plain_reason}</p>
          <a className="h2-link" href="#/experiments">See the experiment <span>→</span></a>
        </section>

        <section className="h2-block">
          <div className="h2-label">What the lab is doing next</div>
          <p className="h2-headline">{x.plain_goal}</p>
          <div className="h2-figure">
            <span className="h2-num num">{x.done} / {x.total}</span>
            <span className="h2-unit">trials · <span className="num">{x.label}</span> · {finished ? 'analyzing results' : 'running'}</span>
          </div>
          <span className="h2-bar"><i className={finished ? '' : 'is-live'} style={{ width: `${(x.done / x.total) * 100}%` }} /></span>
          {reviewing && (
            <p className="h2-trust"><span className="h2-check">✓</span>Independent review active</p>
          )}
          <a className="h2-link" href="#/decisions">How decisions are made <span>→</span></a>
        </section>
      </div>

      <section className="h2-how">
        <div className="h2-label">How Falsify works</div>
        <LoopTimeline phases={phasesAt(PLAIN_STAGE[state.loop_stage] ?? 'experiment', undefined, PLAIN_PHASES)} />
      </section>
    </div>
  );
}
