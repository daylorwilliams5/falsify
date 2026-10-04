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
export interface ResearchState {
  program: string;
  question: string;
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

// programs.json  ←  one entry per research program (one directory per program later)
export interface ProgramSummary {
  id: string;
  title: string;
  question: string;
  status: 'RUNNING' | 'AWAITING' | 'PLANNING' | 'PAUSED';
  phase: string; // loop phase id the program is currently in
  needs_you: string | null;
  activity: string;
  latest: string | null;
  experiments_run: number;
  hypotheses: number;
  opened: string;
}

// A research plan the lab drafts from a new question, before any experiment runs.
export interface ResearchPlan {
  question: string;
  refined_question: string;
  steps: { agent: string; doing: string; done: string }[];
  sources: { title: string; year: string; why: string }[];
  hypotheses: { id: string; claim: string; falsified_if: string }[];
  first_experiment: { title: string; design: string; environment: string; trials: number; est_time: string; est_cost: string };
  risks: string[];
}

// ---------- PI architecture (lab/, decisions/, reviews, results/) ----------

export type AuthorityLevel = 1 | 2 | 3;

// lab/mandate.json — set by the human
export interface Mandate {
  set_by: string;
  set_at: string;
  summary: string;
  plain_question: string; // one-sentence, jargon-free version for the Overview
  research_objective: string;
  subject_model: { provider: string; name: string };
  budget: { max_trials_per_experiment_level1: number; max_estimated_model_calls_per_experiment_level1: number; external_spend_usd_without_human: number };
}

// decisions/D*.json — written by the PI. Fields marked NEW are what the PI and
// reviewer should emit natively; legacy records are normalized in adapters/normalize.ts.
export type Verdict = 'PASS' | 'PASS_WITH_NOTE' | 'BLOCK' | 'ESCALATE' | 'CONCERNS' | 'FAIL';

export interface Review {
  ts: string;
  by: string;
  verdict: Verdict;
  findings: string;
  highlights?: string[]; // NEW: 1–3 one-line findings
  auto_checks?: Record<string, boolean>;
  attested?: Record<string, boolean | null>;
}

export interface RejectedAlternative { label: string; reason: string }

export interface PIDecision {
  id: string;
  ts: string;
  by: string;
  level: AuthorityLevel;
  action: string;
  confidence: number;
  decision: string; // full decision text
  reason: string; // full reasoning
  summary?: string; // NEW: one sentence, what was decided
  rationale?: string; // NEW: one sentence, why
  alternatives_rejected: RejectedAlternative[]; // NEW structure (legacy: " | "-separated text)
  responds_to?: string[]; // NEW: decisions this one corrects or discharges
  resulting_action?: string; // NEW: what actually happened
  human_approval?: { ts: string; via: string; question?: string }; // Level 3 gate answered by the human
  engineering_fix?: { by: string; ts: string; text: string }; // change made outside the PI's authority
  remediated?: { ts: string; text: string }; // review findings cleared without a new decision
  cites: string[];
  reviews: Review[];
  spec?: string;
  spec_hash?: string;
  code_hashes?: Record<string, string>;
}

export type TrialOutcome = string;

// results/<exp>.json, reduced to what the Overview shows
export interface Finding {
  experiment_id: string;
  label: string;
  headline: string;
  plain_headline: string;
  status: HypothesisStatus;
  status_reason: string;
  plain_reason: string;
  public_status: string;
  figure: { value: number; total: number; unit: string };
  trials: { trial: string; cell: string; condition: string; outcome: TrialOutcome; detail: string }[];
  legend: { outcome: TrialOutcome; label: string; tone: 'solid' | 'light' | 'hatched' | 'accent' }[];
  decision?: string;
}

// results/budget.json — written by `falsify budget`
export interface Budget {
  as_of: string;
  elapsed_research_minutes: number;
  external_spend_usd: number;
  external_spend_cap_usd: number;
  model_calls_used: number;
  trials_run: number;
  experiments: Record<string, { trials: number; finished: boolean }>;
  experiments_completed: number;
  subject_models: string[];
  hypotheses_eliminated: string[];
  unresolved: string[];
}

export interface RoleStatus { role: string; state: 'RUNNING' | 'WAITING' | 'IDLE'; detail: string }

export interface Escalation { id: string; decision: string; title: string; why: string; detail: string }

export interface LabState {
  as_of: string;
  status: 'RUNNING' | 'PAUSED';
  loop: number;
  loop_stage: string;
  latest_finding: string;
  next: { plain_goal: string; stage_label: string; rule_intro: string; branches: { k: string; text: string }[] };
  reviewer: { auditing: string | null; active: boolean };
  roles: RoleStatus[];
  process: { id: string; caption: string }[];
  loops: { n: number; label: string; sub: string; start: string; end: string | null; ended?: string; title?: string; summary?: string }[];
  runs: { id: string; start: string; end: string; trials: number }[];
  escalations: Escalation[];
  public: PublicState;
}

// The one-page public demo (#/). Edit lab_state.json to drop in the final result.
export interface PublicState {
  testing: {
    id: string;
    question: string;
    manipulation: string;
    behavior: string;
    trials_done: number;
    trials_total: number;
    status: string;
  };
  lessons: {
    id: string;
    headline: string;
    body: string;
    figure: { value: number; total: number; unit: string };
    status: 'Replicated' | 'Preliminary' | 'Not enough evidence';
  }[];
  steps: string[];
  decision: string;
  trust: string[];
}

// timeline.jsonl — one event per line. Most lines use agent/stage/text;
// a few older ones use actor/event/reason.
export interface LabEvent {
  i: number;
  ts: string;
  actor: string;
  stage: string;
  text: string;
  cites: string[];
  decision_id?: string;
  verdict?: Verdict;
}

/** Everything the Overview needs: the latest of each object, nothing more. */
export interface LabView {
  mandate: Mandate;
  finding: Finding;
  decisions: PIDecision[]; // oldest first
  events: LabEvent[]; // oldest first
  budget: Budget;
  state: LabState;
}
