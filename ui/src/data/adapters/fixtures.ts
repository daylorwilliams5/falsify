import type { LabDataSource } from '../source';
import type {
  AgentActivity, Experiment, ExperimentRun, Hypothesis, LabSnapshot,
  LiteratureSource, ProgramSummary, ResearchPlan, ResearchState, TimelineEvent,
} from '../types';

import programs from '../fixtures/programs.json';
import plans from '../fixtures/plans.json';
import researchState from '../fixtures/corrigibility/research_state.json';
import hypotheses from '../fixtures/corrigibility/hypotheses.json';
import experiments from '../fixtures/corrigibility/experiments.json';
import agentStatus from '../fixtures/corrigibility/agent_status.json';
import timeline from '../fixtures/corrigibility/timeline.json';
import literature from '../fixtures/corrigibility/literature.json';

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
  async listPrograms() { return programs as ProgramSummary[]; },
  async loadProgram(id) { return snapshots[id] ?? null; },
  async loadPlan(id) { return planFixtures[id] ?? null; },
  // Mocked: always returns the example plan, keeping the user's wording.
  async draftPlan(question) { return { ...planFixtures['eval-gaming'], question }; },
};
