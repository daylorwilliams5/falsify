import { useEffect, useState } from 'react';
import type { LabSnapshot } from '../data/types';
import { DetailPage } from './DetailPage';
import { Panel } from '../components/Panel';
import { HypothesisRow } from '../components/HypothesisRow';
import { ExperimentCard } from '../components/ExperimentCard';
import { ResearchLoop } from '../components/ResearchLoop';
import { AgentStatusRow } from '../components/AgentStatusRow';
import { TraceRow } from '../components/TraceRow';
import { DecisionCard } from '../components/DecisionCard';
import { TimelineEvent } from '../components/TimelineEvent';
import { EvidenceItem } from '../components/EvidenceItem';
import { LiteratureSource } from '../components/LiteratureSource';

const ORDER = ['MEASURED', 'DERIVED', 'INFERRED', 'HYPOTHESIS'] as const;

export function HypothesesPage({ lab }: { lab: LabSnapshot }) {
  return (
    <DetailPage kicker="Hypotheses" title="Competing explanations" lede={lab.state.question}>
      <Panel title="Registry" meta={<span className="mono">registry/hypotheses.json</span>}>
        <div className="hyp-cols mono"><span>ID</span><span>mechanism · claim</span><span>evidence ±</span><span>tested by</span><span>status</span></div>
        {lab.hypotheses.map((h) => <HypothesisRow key={h.id} h={h} />)}
      </Panel>
    </DetailPage>
  );
}

export function ExperimentPage({ lab, id }: { lab: LabSnapshot; id?: string }) {
  const exp = lab.experiments.find((e) => e.id === id) ?? lab.experiments[0];
  const evidence = lab.state.evidence.filter((e) => e.hypothesis === exp.hypothesis);
  return (
    <DetailPage kicker={`Experiment · ${exp.id}`} title={lab.state.latest_result.headline} lede={exp.question}>
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

export function DecisionPage({ lab }: { lab: LabSnapshot }) {
  return (
    <DetailPage kicker="Next move" title="Proposed next experiment" lede="The lab pauses here for human approval before building or running anything.">
      <Panel title="Decision" meta={<span className="mono">{lab.state.next_decision.rationale_path}</span>} className="decision-panel">
        <DecisionCard d={lab.state.next_decision} />
      </Panel>
    </DetailPage>
  );
}

export function LiteraturePage({ lab }: { lab: LabSnapshot }) {
  return (
    <DetailPage kicker="Literature" title="What prior work says" lede="Provisionally approved for synthesis and gap analysis. No strong novelty claims.">
      <div className="lit-grid">
        {lab.literature.map((s) => <LiteratureSource key={s.id} s={s} />)}
      </div>
    </DetailPage>
  );
}

export function EvidencePage({ lab }: { lab: LabSnapshot }) {
  return (
    <DetailPage kicker="Evidence" title="What we measured vs. what we believe" lede="Every claim carries its provenance: measured, derived, inferred, or still a hypothesis.">
      <div className="prov-legend mono">
        {ORDER.map((k) => <span key={k} className={`prov-${k.toLowerCase()}`}>{k}</span>)}
      </div>
      {ORDER.flatMap((k) => lab.state.evidence.filter((e) => e.kind === k)).map((e) => <EvidenceItem key={e.id} e={e} />)}
    </DetailPage>
  );
}

export function AgentsPage({ lab }: { lab: LabSnapshot }) {
  const { activity, state, timeline } = lab;
  // Trace clock: the running span keeps growing so the waterfall feels live.
  const [tick, setTick] = useState(0);
  useEffect(() => { const i = setInterval(() => setTick((t) => t + 0.25), 250); return () => clearInterval(i); }, []);
  const traceNow = 46 + tick;
  const traceTotal = Math.max(60, traceNow + 6);

  return (
    <DetailPage kicker="Agents" title="Who is doing what" lede={`Omnigent ${state.omnigent.version} · ${state.omnigent.workers} workers · ${state.model}`}>
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
