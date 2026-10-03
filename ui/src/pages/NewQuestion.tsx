import { useEffect, useState } from 'react';
import type { ResearchPlan } from '../data/types';
import { activeSource } from '../data/source';
import { PlanView } from '../components/PlanView';
import { EXAMPLE_QUESTION } from './Home';

// Ask → watch the agents plan → review the plan. Planning is mocked in fixture mode.
export function NewQuestion({ initial }: { initial?: string }) {
  const [q, setQ] = useState(initial ?? '');
  const [asked, setAsked] = useState<string | null>(initial ?? null);
  const [plan, setPlan] = useState<ResearchPlan | null>(null);
  const [step, setStep] = useState(0);

  useEffect(() => {
    if (!asked) return;
    setPlan(null); setStep(0);
    let alive = true;
    activeSource.draftPlan(asked).then((p) => {
      if (!alive) return;
      setPlan(p);
      p.steps.forEach((_, i) => setTimeout(() => alive && setStep(i + 1), 700 * (i + 1)));
    });
    return () => { alive = false; };
  }, [asked]);

  const done = plan && step >= plan.steps.length;
  const isExample = asked?.replace(/[’']/g, "'") === EXAMPLE_QUESTION.replace(/[’']/g, "'");

  return (
    <div className="newq">
      <div className="ov-label">New research question</div>
      {!asked ? (
        <form className="newq-form" onSubmit={(e) => { e.preventDefault(); setAsked(q.trim() || EXAMPLE_QUESTION); }}>
          <textarea value={q} onChange={(e) => setQ(e.target.value)} placeholder={EXAMPLE_QUESTION} rows={3} autoFocus />
          <button type="submit" className="cta">Plan it <span>→</span></button>
        </form>
      ) : (
        <h1 className="newq-q">“{asked}”</h1>
      )}

      {plan && (
        <ol className="planning">
          {plan.steps.map((s, i) => {
            const state = i < step ? 'done' : i === step ? 'active' : 'waiting';
            return (
              <li key={s.agent} className={`ps is-${state}`}>
                <span className="ps-dot" />
                <span className="ps-agent">{s.agent}</span>
                <span className="ps-text">{state === 'done' ? s.done : state === 'active' ? `${s.doing}…` : s.doing}</span>
              </li>
            );
          })}
        </ol>
      )}

      {done && (
        <>
          {!isExample && (
            <p className="mock-note">Preview: planning isn’t connected yet, so this is the example plan rather than one written for your question.</p>
          )}
          <PlanView plan={plan} />
        </>
      )}
    </div>
  );
}
