import { useEffect } from 'react';
import type { ProgramSummary } from '../data/types';
import { isLoading, usePlan, useProgram } from '../data/useLab';
import { ProgramBar } from '../components/ProgramBar';
import { LoopTimeline, phasesAt } from '../components/LoopTimeline';
import { PlanView } from '../components/PlanView';

// Early-stage programs: question, loop stage and the plan awaiting approval.
// The active lab program lives at the Overview.
export function ProgramPage({ program }: { program: ProgramSummary }) {
  const lab = useProgram(program.id);
  const plan = usePlan(program.id);
  useEffect(() => { if (lab && !isLoading(lab)) window.location.replace('#/'); }, [lab]);
  if (isLoading(lab) || isLoading(plan) || lab) return null;

  return (
    <>
      <ProgramBar id={program.id} title={program.title} />
      <div className="ov">
        <div className="label">Research question</div>
        <h1 className="ov-question">“{program.question}”</h1>
        <section className="ov-loop" style={{ marginTop: 64 }}>
          <div className="label">Where the lab is</div>
          <LoopTimeline phases={phasesAt(program.phase, program.activity)} />
        </section>
        {plan && (
          <section style={{ marginTop: 88 }}>
            <div className="plan-head"><span className="focus-dot" /> {program.needs_you}</div>
            <PlanView plan={plan} />
          </section>
        )}
      </div>
    </>
  );
}
