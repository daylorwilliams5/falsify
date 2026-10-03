import { useEffect, useState } from 'react';
import type { LabSnapshot, LabView } from '../data/types';
import { BudgetStrip, LabStatus } from '../components/lab/LabStrip';
import { OverrideControl } from '../components/lab/HumanControl';
import { DetailPage } from './DetailPage';
import { Panel } from '../components/Panel';
import { HypothesisRow } from '../components/HypothesisRow';
import { ExperimentCard } from '../components/ExperimentCard';
import { ResearchLoop } from '../components/ResearchLoop';
import { AgentStatusRow } from '../components/AgentStatusRow';
import { TraceRow } from '../components/TraceRow';
import { TimelineEvent } from '../components/TimelineEvent';
import { EvidenceItem } from '../components/EvidenceItem';
import { LiteratureSource } from '../components/LiteratureSource';

const ORDER = ['MEASURED', 'DERIVED', 'INFERRED', 'HYPOTHESIS'] as const;

export function HypothesesPage({ lab, base }: { lab: LabSnapshot; base: string }) {
  return (
    <DetailPage base={base} kicker="Hypotheses" title="Competing explanations" lede={lab.state.question}>
      <Panel title="Registry" meta={<span className="mono">registry/hypotheses.json</span>}>
        <div className="hyp-cols mono"><span>ID</span><span>mechanism · claim</span><span>evidence ±</span><span>tested by</span><span>status</span></div>
        {lab.hypotheses.map((h) => <HypothesisRow key={h.id} h={h} />)}
      </Panel>
    </DetailPage>
  );
}

export function ExperimentPage({ lab, base, id }: { lab: LabSnapshot; base: string; id?: string }) {
  const exp = lab.experiments.find((e) => e.id === id) ?? lab.experiments[0];
  const evidence = lab.state.evidence.filter((e) => e.hypothesis === exp.hypothesis);
  return (
    <DetailPage base={base} kicker={`Experiment · ${exp.id}`} title={exp.id} lede={exp.question}>
      <div className="detail-grid">
        <Panel title="Result" meta={<span className="mono">results/{exp.id}.json</span>}>
          <ExperimentCard x={exp} />
        </Panel>
        <Panel title="Evidence from this run" meta={<span className="mono">{evidence.length} claims</span>}>
          {ORDER.flatMap((k) => evidence.filter((e) => e.kind === k)).map((e) => <EvidenceItem key={e.id} e={e} />)}
        </Panel>
      </div>
    </DetailPage>
  );
}

export function LiteraturePage({ lab, base }: { lab: LabSnapshot; base: string }) {
  return (
    <DetailPage base={base} kicker="Literature" title="What prior work says" lede="Provisionally approved for synthesis and gap analysis. No strong novelty claims.">
      <div className="lit-grid">
        {lab.literature.map((s) => <LiteratureSource key={s.id} s={s} />)}
      </div>
    </DetailPage>
  );
}

export function AgentsPage({ lab, base, view }: { lab: LabSnapshot; base: string; view: LabView }) {
  const { activity, state, timeline } = lab;
  // Trace clock: the running span keeps growing so the waterfall feels live.
  const [tick, setTick] = useState(0);
  useEffect(() => { const i = setInterval(() => setTick((t) => t + 0.25), 250); return () => clearInterval(i); }, []);
  const traceNow = 46 + tick;
  const traceTotal = Math.max(60, traceNow + 6);

  return (
    <DetailPage base={base} kicker="Agents" title="Who is doing what" lede={`Omnigent ${state.omnigent.version} · ${state.omnigent.workers} workers · ${state.model}`}>
      <section className="lab-sec-top">
        <div className="label">Lab status</div>
        <LabStatus roles={view.state.roles} />
      </section>
      <section className="lab-sec-top">
        <div className="label">Research budget</div>
        <BudgetStrip b={view.budget} mandate={view.mandate} active={view.state.active_experiment} />
      </section>
      <OverrideControl />
      <Panel title="Scientific loop" className="loop-panel">
        <ResearchLoop stages={activity.loop} loopIndex={state.loop_index} gated={state.awaiting_human} />
      </Panel>
      <div className="row r3">
        <Panel title="Agent activity" className="span-4">
          {activity.agents.map((a) => <AgentStatusRow key={a.id} a={a} />)}
        </Panel>
        <Panel title="Run trace" className="span-5" meta={<span className="mono">{activity.trace.agent} · {activity.trace.started}</span>}>
          <div className="trace-root mono">
            <span className="muted">root</span> {activity.trace.root}
            <span className="trace-scale">0s<i />{traceTotal.toFixed(0)}s</span>
          </div>
          {activity.trace.spans.map((s) => <TraceRow key={s.id} span={s} total={traceTotal} now={traceNow} />)}
        </Panel>
        <Panel title="Timeline" className="span-3" meta={<span className="mono">timeline.jsonl</span>}>
          {[...timeline].reverse().map((e, i, arr) => <TimelineEvent key={e.ts} e={e} last={i === arr.length - 1} />)}
        </Panel>
      </div>
    </DetailPage>
  );
}
