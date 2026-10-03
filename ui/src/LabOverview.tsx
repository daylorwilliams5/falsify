import type { LabView } from './data/types';
import { PLAIN_STAGE } from './components/LoopTimeline';
import { EscalationCard } from './components/lab/HumanControl';
import { TrialStrip } from './components/overview/TrialStrip';
import { StoppingRule } from './components/overview/StoppingRule';
import { ProcessStrip } from './components/overview/ProcessStrip';
import { useCountUp } from './hooks/useCountUp';
import { PLAIN_STATUS } from './data/view';

// The front page: three plain-language answers. Lab internals live on detail pages.
export function LabOverview({ lab }: { lab: LabView }) {
  const { mandate, finding, state } = lab;
  const n = useCountUp(finding.figure.value);
  const next = state.next;

  return (
    <div className="home2">
      <section className="h2-question">
        <div className="h2-label">What we’re trying to understand</div>
        <h1>{mandate.plain_question}</h1>
      </section>

      {state.escalations.map((e) => <EscalationCard key={e.id} e={e} />)}

      <div className="h2-pair">
        <section className="h2-block">
          <div className="h2-label">What we learned <span className="h2-id num">{finding.label}</span></div>
          <p className="h2-headline">{finding.plain_headline}</p>
          <div className="h2-figure">
            <span className="h2-num num">{n} / {finding.figure.total}</span>
            <span className="h2-unit">{finding.figure.unit}</span>
          </div>
          <TrialStrip trials={finding.trials} />
          <p className="h2-status"><span className="h2-status-k">Result</span>{PLAIN_STATUS[finding.status]}</p>
          <p className="h2-why">{finding.plain_reason}</p>
          <a className="h2-link" href={`#/timeline/${finding.decision ?? ''}`}>See how the lab caught it <span>→</span></a>
        </section>

        <section className="h2-block">
          <div className="h2-label">What the lab is doing next</div>
          <p className="h2-headline">{next.plain_goal}</p>
          <p className="h2-stage"><span className="run-dot" />{next.stage_label}</p>
          <StoppingRule intro={next.rule_intro} ifWorks={next.if_works} ifFails={next.if_fails} />
          {state.reviewer.active && (
            <p className="h2-trust"><span className="h2-check">✓</span>Independent review active</p>
          )}
          <a className="h2-link" href="#/decisions">How decisions are made <span>→</span></a>
        </section>
      </div>

      <section className="h2-how">
        <div className="h2-label">How Falsify works</div>
        <ProcessStrip current={PLAIN_STAGE[state.loop_stage] ?? 'experiment'} captions={state.process} />
      </section>
    </div>
  );
}
