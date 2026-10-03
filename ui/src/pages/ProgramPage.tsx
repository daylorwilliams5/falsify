import type { ProgramSummary } from '../data/types';
import { isLoading, usePlan, useProgram } from '../data/useLab';
import { ProgramBar } from '../components/ProgramBar';
import { LoopTimeline, phasesAt } from '../components/LoopTimeline';
import { PlanView } from '../components/PlanView';
import { Overview } from '../Overview';
import { AgentsPage, DecisionPage, EvidencePage, ExperimentPage, HypothesesPage, LiteraturePage } from './Pages';

export function ProgramPage({ program, tab, sub }: { program: ProgramSummary; tab: string; sub?: string }) {
  const lab = useProgram(program.id);
  const plan = usePlan(program.id);
  if (isLoading(lab) || isLoading(plan)) return null;

  // Programs that haven't run an experiment yet: show their question, stage and plan.
  if (!lab) {
    return (
      <>
        <ProgramBar id={program.id} title={program.title} tab="" tabs={false} />
        <div className="ov">
          <div className="ov-label">Research question</div>
          <h1 className="ov-question">“{program.question}”</h1>
          <section className="ov-loop" style={{ marginTop: 64 }}>
            <div className="ov-label">Where the lab is</div>
            <LoopTimeline phases={phasesAt(program.phase, program.activity)} />
          </section>
          {plan && (
            <section style={{ marginTop: 88 }}>
              <div className="plan-head">
                <span className="focus-dot" /> {program.needs_you}
              </div>
              <PlanView plan={plan} />
            </section>
          )}
        </div>
      </>
    );
  }

  const base = `#/p/${program.id}`;
  const page = (() => {
    switch (tab) {
      case 'hypotheses': return <HypothesesPage lab={lab} base={base} />;
      case 'experiments': return <ExperimentPage lab={lab} base={base} id={sub} />;
      case 'decision': return <DecisionPage lab={lab} base={base} />;
      case 'literature': return <LiteraturePage lab={lab} base={base} />;
      case 'agents': return <AgentsPage lab={lab} base={base} />;
      case 'evidence': return <EvidencePage lab={lab} base={base} />;
      default: return <Overview lab={lab} base={base} />;
    }
  })();

  return (
    <>
      <ProgramBar id={program.id} title={program.title} tab={tab === 'decision' ? '' : tab} />
      {page}
    </>
  );
}
