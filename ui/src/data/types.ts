// View-model types for the Falsify UI.
//
// These are the shapes the components consume. They intentionally mirror the
// artifacts the lab already writes (registry/hypotheses.json, results/*.json,
// timeline.jsonl, critiques/*.md, sources/candidates.md) so that a live adapter
// only has to *map* those files into these types — components never change.

export type HypothesisStatus =
  | 'UNTESTED'
  | 'RUNNING'
  | 'SUPPORTED'
  | 'FALSIFIED'
  | 'INCONCLUSIVE'
  | 'NEEDS_REPLICATION';

export type AgentState = 'COMPLETE' | 'RUNNING' | 'IDLE' | 'QUEUED' | 'BLOCKED';

export type Status = HypothesisStatus | AgentState | 'PROPOSED' | 'READY' | 'SELECTED';

export type Provenance = 'MEASURED' | 'DERIVED' | 'INFERRED' | 'HYPOTHESIS';

export type EventSource = 'HUMAN' | 'AGENT' | 'EXPERIMENT';

// research_state.json  ←  registry/hypotheses.json (question) + director state
export interface LatestResult {
  experiment: string;
  label: string;
  headline: string;
  finding: string;
  verdict: string;
  reason: string;
}

export interface ResearchState {
  program: string;
  question: string;
  question_short: string;
  latest_result: LatestResult;
  current_phase: string;
  refined_from?: string;
  current_experiment: string;
  loop_index: number;
  started_at: string;
  elapsed_seconds_at_snapshot: number;
  model: string;
  omnigent: { status: 'ONLINE' | 'DEGRADED' | 'OFFLINE'; version: string; workers: number };
  awaiting_human: boolean;
  evidence: EvidenceItem[];
  next_decision: NextDecision;
}

export interface EvidenceItem {
  id: string;
  kind: Provenance;
  text: string;
  source: string; // artifact path or agent that produced it
  hypothesis?: string;
}

export interface DecisionOption {
  id: string;
  label: string;
  title: string;
  spec: string; // specs/candidates/*.json
  tests: string;
  info_gain: 'HIGH' | 'MEDIUM' | 'LOW';
  build: string; // e.g. "~30 min" or "READY"
  cost: 'HIGH' | 'MEDIUM' | 'LOW';
  hypotheses: string[];
  short: string;
  one_line: string;
  design: string;
  trials: number;
  falsified_if: string;
}

export interface NextDecision {
  status: 'PROPOSED' | 'APPROVED' | 'REJECTED';
  proposed_by: string;
  selected: string;
  reason: string;
  rationale_path: string;
  options: DecisionOption[];
}

// hypotheses.json  ←  registry/hypotheses.json
export interface Hypothesis {
  id: string;
  mechanism: string;
  claim: string;
  falsified_if: string;
  status: HypothesisStatus;
  supporting: number;
  contradicting: number;
  tested_by: string[];
}

// experiments.json  ←  specs/*.json + results/<id>.json + results/<id>_stats.json
export interface CellResult {
  cell: string;
  org: 'single' | 'multi';
  k: number;
  update: 'invalidating' | 'benign';
  n: number;
  wasted_mean: number;
  wasted_sd: number;
  switched_mean: number;
}

export interface Experiment {
  id: string;
  status: 'COMPLETE' | 'RUNNING' | 'PROPOSED' | 'QUEUED';
  question: string;
  design: { label: string; factors: { name: string; levels: string[] }[] };
  trials: { done: number; total: number; invalid: number };
  primary?: { metric: string; delta: number; ci95: [number, number]; n_boot: number };
  flags: { level: 'warn' | 'info'; title: string; detail: string }[];
  hypothesis: string;
  hypothesis_status: HypothesisStatus;
  cells: CellResult[];
  metrics: { label: string; value: string; hint?: string }[];
  spec_hash: string;
  env: string;
}

// agent_status.json  ←  Omnigent worker state + latest artifact per role
export interface AgentStatus {
  id: string;
  name: string;
  role: string;
  state: AgentState;
  task: string;
  artifact?: string;
  updated: string;
  tokens?: number;
}

export interface LoopStage {
  id: string;
  label: string;
  agent: string;
  state: AgentState;
  task: string;
  artifact: string;
}

export interface TraceSpan {
  id: string;
  depth: number;
  kind: 'agent' | 'tool' | 'llm' | 'read' | 'write';
  name: string;
  detail?: string;
  start: number; // seconds from trace start
  duration: number | null; // null = still running
  state: AgentState;
}

// Coarse six-step view of the loop used on the Overview.
export interface Phase {
  id: string;
  label: string;
  state: AgentState;
  note?: string;
}

export interface AgentActivity {
  phases: Phase[];
  focus: { agent: string; verb: string; state: AgentState }[];
  agents: AgentStatus[];
  loop: LoopStage[];
  trace: { root: string; agent: string; started: string; spans: TraceSpan[] };
}

// timeline.json  ←  timeline.jsonl (one event per line)
export interface TimelineEvent {
  ts: string;
  source: EventSource;
  actor: string;
  stage: string;
  text: string;
  cites: string[];
}

// literature.json  ←  sources/candidates.md (table rows)
export interface LiteratureSource {
  id: string;
  title: string;
  authors: string;
  year: string;
  directness: 'DIRECT' | 'ADJACENT';
  verification: 'peer-reviewed' | 'preprint' | 'abstract-only';
  finding: string;
  relevance: string;
  hypotheses: string[];
  url: string;
}

export interface ExperimentRun {
  id: string;
  status: Experiment['status'];
  label: string;
}

export interface LabSnapshot {
  state: ResearchState;
  hypotheses: Hypothesis[];
  experiments: Experiment[];
  runs: ExperimentRun[];
  activity: AgentActivity;
  timeline: TimelineEvent[];
  literature: LiteratureSource[];
}
