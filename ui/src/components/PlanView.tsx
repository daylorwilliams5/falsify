import { useState } from 'react';
import type { ResearchPlan } from '../data/types';

// A drafted research plan, shown for human approval before anything runs.
export function PlanView({ plan }: { plan: ResearchPlan }) {
  const [note, setNote] = useState<string | null>(null);
  const x = plan.first_experiment;
  return (
    <div className="plan">
      <section className="plan-sec">
        <div className="ov-label">Refined question</div>
        <p className="plan-refined">{plan.refined_question}</p>
      </section>

      <section className="plan-sec">
        <div className="ov-label">Competing hypotheses</div>
        <ol className="plan-hyps">
          {plan.hypotheses.map((h) => (
            <li key={h.id}>
              <span className="plan-hid">{h.id}</span>
              <div>
                <p className="plan-claim">{h.claim}</p>
                <p className="plan-fals">Falsified if: {h.falsified_if}</p>
              </div>
            </li>
          ))}
        </ol>
      </section>

      <div className="plan-pair">
        <section className="plan-sec">
          <div className="ov-label">First experiment</div>
          <p className="plan-xtitle">{x.title}</p>
          <dl className="plan-dl">
            <dt>Design</dt><dd>{x.design}</dd>
            <dt>Environment</dt><dd>{x.environment}</dd>
            <dt>Trials</dt><dd>{x.trials}</dd>
            <dt>Time</dt><dd>{x.est_time}</dd>
            <dt>Cost</dt><dd>{x.est_cost}</dd>
          </dl>
        </section>
        <section className="plan-sec">
          <div className="ov-label">Skeptic’s concerns</div>
          <ul className="plan-risks">
            {plan.risks.map((r) => <li key={r}>{r}</li>)}
          </ul>
          <div className="ov-label" style={{ marginTop: 32 }}>Starting literature</div>
          <ul className="plan-sources">
            {plan.sources.map((s) => (
              <li key={s.title}><span className="plan-src-t">{s.title}</span> <span className="plan-src-y">{s.year}</span><p>{s.why}</p></li>
            ))}
          </ul>
        </section>
      </div>

      <div className="plan-actions">
        <button className="cta" onClick={() => setNote('Not wired yet: approval will be written to the program timeline.')}>Approve plan</button>
        <a className="ov-link-inline" href="#/new">Revise the question</a>
        {note && <span className="plan-note">{note}</span>}
      </div>
    </div>
  );
}
