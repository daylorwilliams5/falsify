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
import { TrialStrip } from '../components/overview/TrialStrip';
import allExperiments from '../data/fixtures/lab/experiments_all.json';
import exp012Finding from '../data/fixtures/lab/results/exp012.json';
import exp013tFinding from '../data/fixtures/lab/results/exp013t.json';
import type { Finding } from '../data/types';

type ExpSummary = (typeof allExperiments)[number];
const FINDINGS: Record<string, Finding> = { exp012: exp012Finding as Finding, exp013t: exp013tFinding as Finding };
const REPO = 'https://github.com/daylorwilliams5/falsify/blob/main/';

function ExperimentIndex({ current }: { current: string }) {
  return (
    <div className="xi">
      {allExperiments.map((e) => (
        <a key={e.id} href={`#/experiments/${e.id}`} className={`xi-card tone-${e.tone} ${e.id === current ? 'is-on' : ''}`}>
          <div className="xi-top mono"><span>{e.short}</span><span className="muted">{e.loop}</span></div>
          <div className="xi-head">{e.headline}</div>
          <div className="xi-meta mono muted">{e.model} · {e.trials.split(' ')[0]} trials</div>
          <div className={`xi-verdict mono tone-${e.tone}`}>{e.verdict}</div>
        </a>
      ))}
    </div>
  );
}

function ExperimentSummaryCard({ e }: { e: ExpSummary }) {
  const f = 'finding' in e && e.finding ? FINDINGS[e.finding as string] : undefined;
  return (
    <div className="xs">
      <div className="xs-meta">
        <div><div className="lbl">Subject model</div><div className="mono">{e.model}</div></div>
        <div><div className="lbl">Trials</div><div className="mono">{e.trials}</div></div>
        <div className="xs-wide"><div className="lbl">Design</div><div>{e.design}</div></div>
      </div>
      <div className="xs-headline">{e.headline}</div>
      <ul className="xs-bullets">{e.bullets.map((b) => <li key={b}>{b}</li>)}</ul>
      {f && <TrialStrip trials={f.trials} legend={f.legend} />}
      <div className={`xs-verdict mono tone-${e.tone}`}>{e.verdict}</div>
      <div className="xs-foot mono">
        <a href={REPO + e.result} target="_blank" rel="noreferrer">{e.result}</a>
        {e.decision.startsWith('D') && <a href={`#/decisions/${e.decision}`}>decision {e.decision}</a>}
      </div>
    </div>
  );
}


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
  const summary = allExperiments.find((e) => e.id === id) ?? (id ? undefined : allExperiments[allExperiments.length - 1]);
  const exp = lab.experiments.find((e) => e.id === (summary?.id ?? id));
  if (summary && summary.id !== 'exp001_pilot') {
    return (
      <DetailPage base={base} kicker={`Experiment · ${summary.short} · ${summary.loop}`} title={summary.short} lede={summary.question}>
        <Panel title="All experiments" meta={<span className="mono">{allExperiments.length} run · in order</span>}>
          <ExperimentIndex current={summary.id} />
        </Panel>
        <Panel title="Result" meta={<span className="mono">{summary.result}</span>}>
          <ExperimentSummaryCard e={summary} />
        </Panel>
      </DetailPage>
    );
  }
  const x = exp ?? lab.experiments[0];
  const evidence = lab.state.evidence.filter((e) => e.hypothesis === x.hypothesis);
  return (
    <DetailPage base={base} kicker={`Experiment · ${x.id}`} title={x.id} lede={x.question}>
      <Panel title="All experiments" meta={<span className="mono">{allExperiments.length} run · in order</span>}>
        <ExperimentIndex current={x.id} />
      </Panel>
      <div className="detail-grid">
        <Panel title="Result" meta={<span className="mono">results/{x.id}.json</span>}>
          <ExperimentCard x={x} />
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
        <BudgetStrip b={view.budget} />
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
