import type { LabDataSource } from '../source';
import type {
  AgentActivity, Budget, Escalation, Finding, LabState, Mandate, Experiment, ExperimentRun, Hypothesis, LabSnapshot,
  LiteratureSource, ProgramSummary, ResearchPlan, ResearchState, TimelineEvent,
} from '../types';

import mandate from '../fixtures/lab/mandate.json';
import budget from '../fixtures/lab/results/budget.json';
import exp001 from '../fixtures/lab/results/exp001_pilot.json';
import labState from '../fixtures/lab/lab_state.json';
import escalationExample from '../fixtures/lab/escalation_example.json';
import { normalizeDecision } from './normalize';
import programs from '../fixtures/programs.json';
import plans from '../fixtures/plans.json';
import researchState from '../fixtures/corrigibility/research_state.json';
import hypotheses from '../fixtures/corrigibility/hypotheses.json';
import experiments from '../fixtures/corrigibility/experiments.json';
import agentStatus from '../fixtures/corrigibility/agent_status.json';
import timeline from '../fixtures/corrigibility/timeline.json';
import literature from '../fixtures/corrigibility/literature.json';

// decisions/D*.json, loaded the way a directory listing would be.
const decisionFiles = import.meta.glob('../fixtures/lab/decisions/D*.json', { eager: true, import: 'default' });
const decisions = Object.values(decisionFiles)
  .map((d) => normalizeDecision(d as Record<string, unknown>))
  .sort((a, b) => a.ts.localeCompare(b.ts));

const snapshots: Record<string, LabSnapshot> = {
  corrigibility: {
    state: researchState as ResearchState,
    hypotheses: hypotheses as Hypothesis[],
    experiments: experiments.experiments as Experiment[],
    runs: experiments.runs as ExperimentRun[],
    activity: agentStatus as AgentActivity,
    timeline: timeline as TimelineEvent[],
    literature: literature as LiteratureSource[],
  },
};

const planFixtures = plans as Record<string, ResearchPlan>;

export const fixtureSource: LabDataSource = {
  name: 'fixtures',
  async loadLab() {
    // Demo switch: ?escalation=1 shows a Level 3 card.
    const q = new URLSearchParams(window.location.search);
    const state = { ...(labState as LabState) };
    if (q.get('escalation')) state.escalations = [escalationExample as Escalation];
    return {
      mandate: mandate as Mandate,
      finding: exp001 as Finding,
      decisions,
      budget: budget as Budget,
      state,
    };
  },
  async listPrograms() { return programs as ProgramSummary[]; },
  async loadProgram(id) { return snapshots[id] ?? null; },
  async loadPlan(id) { return planFixtures[id] ?? null; },
  // Mocked: always returns the example plan, keeping the user's wording.
  async draftPlan(question) { return { ...planFixtures['eval-gaming'], question }; },
};
