import type { LabView } from './data/types';
import { PLAIN_STAGE } from './components/LoopTimeline';
import { EscalationCard } from './components/lab/HumanControl';
import { TrialStrip } from './components/overview/TrialStrip';
import { StoppingRule } from './components/overview/StoppingRule';
import { ProcessStrip } from './components/overview/ProcessStrip';
import { ROLES } from './pages/JoinPage';
import { useCountUp } from './hooks/useCountUp';
import { hhmm, outcomeOf, PLAIN_STATUS } from './data/view';

// The front page, written for someone seeing Falsify for the first time.
export function LabOverview({ lab }: { lab: LabView }) {
  const { mandate, finding, state, decisions, events, budget } = lab;
  const n = useCountUp(finding.figure.value);
  const next = state.next;

  const reviews = events.filter((e) => e.stage === 'methodology_review').length;
  const failedFixed = decisions.filter((d) =>
    d.reviews.some((r) => r.verdict === 'FAIL' || r.verdict === 'BLOCK') && outcomeOf(d, decisions) === 'CORRECTED').length;
  const day = new Date(events[0].ts).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });

  return (
    <div className="home2">
      <section className="hero">
        <div className="hero-eyebrow">A new kind of AI lab</div>
        <h1 className="hero-title">AI agents do the research. Then they try to prove themselves wrong.</h1>
        <p className="hero-sub">
          Falsify is an autonomous research lab. Agents read the literature, run experiments and check each other’s
          work, and every step stays open for scientists to inspect, challenge and build on.
        </p>
        <div className="hero-ctas">
          <a className="cta" href="#now">See what the lab is studying</a>
          <a className="btn-quiet" href="#/join">Join the lab</a>
        </div>
      </section>

      {state.escalations.map((e) => <EscalationCard key={e.id} e={e} />)}

      <section id="now" className="h2-question">
        <div className="h2-label">What the lab is studying right now</div>
        <p className="h2-q">{mandate.plain_question}</p>
      </section>

      <div className="h2-pair">
        <section className="h2-block">
          <h2 className="h2-label">What we learned <span className="h2-id num">{finding.label}</span></h2>
          <p className="h2-headline">{finding.plain_headline}</p>
          <div className="h2-figure">
            <span className="h2-num num">{n} / {finding.figure.total}</span>
            <span className="h2-unit">{finding.figure.unit}</span>
          </div>
          <TrialStrip trials={finding.trials} />
          <p className="h2-status"><span className="h2-status-k">Result</span>{PLAIN_STATUS[finding.status]}</p>
          <p className="h2-why">{finding.plain_reason}</p>
          <a className="h2-link" href={`#/timeline/${finding.decision ?? ''}`}>See how the lab caught it <span aria-hidden>→</span></a>
        </section>

        <section className="h2-block">
          <h2 className="h2-label">What the lab is doing next</h2>
          <p className="h2-headline">{next.plain_goal}</p>
          <p className="h2-stage"><span className="run-dot" aria-hidden />{next.stage_label}</p>
          <StoppingRule intro={next.rule_intro} ifWorks={next.if_works} ifFails={next.if_fails} />
          <a className="h2-link" href="#/decisions">How decisions are made <span aria-hidden>→</span></a>
        </section>
      </div>

      <section className="h2-how">
        <h2 className="h2-label">How it works</h2>
        <ProcessStrip current={PLAIN_STAGE[state.loop_stage] ?? 'experiment'} captions={state.process} />
      </section>

      <section className="trust">
        <h2 className="sec-title">Why you can check the results</h2>
        <div className="trust-grid">
          <a className="trust-item" href="#/decisions">
            <span className="trust-num num">{reviews}</span>
            <span className="trust-head">Every decision gets a second opinion</span>
            <span className="trust-body">An independent reviewer audits each decision the lab makes. It has failed {failedFixed}, and the lab corrected both.</span>
          </a>
          <a className="trust-item" href="#/timeline">
            <span className="trust-num num">{events.length}</span>
            <span className="trust-head">Nothing happens off the record</span>
            <span className="trust-body">Every decision, review and result is time-stamped, so anyone can see what was decided before the data came in, and what wasn’t.</span>
          </a>
          <a className="trust-item" href="#/experiments">
            <span className="trust-num num">{budget.trials_run}</span>
            <span className="trust-head">Results you can re-run</span>
            <span className="trust-body">Each trial is saved with its locked setup and random seed, so a result can be repeated, not just believed.</span>
          </a>
        </div>
      </section>

      <section className="join-teaser">
        <h2 className="sec-title">Science is a community. So is this lab.</h2>
        <p className="sec-sub">The agents run the experiments. People decide what’s worth studying and whether the results hold up.</p>
        <div className="role-row">
          {ROLES.map((r) => (
            <a key={r.id} className="role-mini" href={`#/join`}>
              <span className="role-mini-title">{r.title}</span>
              <span className="role-mini-body">{r.short}</span>
            </a>
          ))}
        </div>
        <a className="cta" href="#/join">Join the lab <span aria-hidden>→</span></a>
      </section>

      <footer className="site-foot">
        Working prototype. Everything shown comes from the lab’s own records of {day}, {hhmm(events[0].ts)}–{hhmm(events[events.length - 1].ts)}.
      </footer>
    </div>
  );
}
