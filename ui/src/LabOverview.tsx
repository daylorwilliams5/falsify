import type { LabView } from './data/types';
import { LoopTimeline, LAB_PHASES, phasesAt } from './components/LoopTimeline';
import { FindingBlock } from './components/lab/FindingBlock';
import { DecisionBlock } from './components/lab/DecisionBlock';
import { ReviewBlock } from './components/lab/ReviewBlock';
import { BudgetStrip, LabStatus } from './components/lab/LabStrip';
import { EscalationCard, OverrideControl } from './components/lab/HumanControl';

export function LabOverview({ lab }: { lab: LabView }) {
  const { mandate, finding, decisions, budget, state } = lab;
  const decision = decisions[decisions.length - 1];
  const x = state.active_experiment;
  return (
    <div className="lab">
      <section className="mandate">
        <div className="label">Research mandate <span className="label-sub">set by human</span></div>
        <h1 className="mandate-text">“{mandate.summary}”</h1>
      </section>

      {state.escalations.map((e) => <EscalationCard key={e.id} e={e} />)}

      <div className="objects">
        <FindingBlock f={finding} />
        <DecisionBlock d={decision} />
        <ReviewBlock d={decision} auditing={state.reviewer.auditing === decision.id} />
      </div>

      <section className="lab-sec">
        <div className="label">Autonomous scientific loop</div>
        <LoopTimeline phases={phasesAt(state.loop_stage, x.done === x.total ? `${x.id} complete · ${x.total} of ${x.total} trials · readout pending` : `${x.id} running · ${x.done} of ${x.total} trials`, LAB_PHASES)} />
      </section>

      <section className="lab-sec lab-sec-tight">
        <div className="label">Lab status</div>
        <LabStatus roles={state.roles} />
      </section>

      <section className="lab-sec lab-sec-tight">
        <div className="label">Research budget</div>
        <BudgetStrip b={budget} mandate={mandate} active={x} />
      </section>

      <OverrideControl />
    </div>
  );
}
