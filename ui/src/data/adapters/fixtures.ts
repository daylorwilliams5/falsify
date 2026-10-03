import type { LabDataSource } from '../source';
import type {
  AgentActivity, Experiment, ExperimentRun, Hypothesis, LabSnapshot,
  LiteratureSource, ResearchState, TimelineEvent,
} from '../types';

import researchState from '../fixtures/research_state.json';
import hypotheses from '../fixtures/hypotheses.json';
import experiments from '../fixtures/experiments.json';
import agentStatus from '../fixtures/agent_status.json';
import timeline from '../fixtures/timeline.json';
import literature from '../fixtures/literature.json';

export const fixtureSource: LabDataSource = {
  name: 'fixtures',
  async load(): Promise<LabSnapshot> {
    return {
      state: researchState as ResearchState,
      hypotheses: hypotheses as Hypothesis[],
      experiments: experiments.experiments as Experiment[],
      runs: experiments.runs as ExperimentRun[],
      activity: agentStatus as AgentActivity,
      timeline: timeline as TimelineEvent[],
      literature: literature as LiteratureSource[],
    };
  },
};
