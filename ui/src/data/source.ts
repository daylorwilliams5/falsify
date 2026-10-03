import type { LabSnapshot, LabView, ProgramSummary, ResearchPlan } from './types';
import { fixtureSource } from './adapters/fixtures';

/**
 * A LabDataSource is the only thing the UI knows about where data comes from.
 *
 *   fixtureSource  — static JSON in ./fixtures (today)
 *   artifactSource — maps each program's registry/, results/, timeline.jsonl,
 *                    critiques/, sources/ into the same shapes (later; see
 *                    ./adapters/artifacts.ts for the planned mapping)
 */
export interface LabDataSource {
  name: string;
  /** Latest finding, PI decision, review verdict and lab state for the Overview. */
  loadLab(): Promise<LabView>;
  listPrograms(): Promise<ProgramSummary[]>;
  /** Full snapshot for a program that has run experiments; null if it is still planning. */
  loadProgram(id: string): Promise<LabSnapshot | null>;
  /** The plan awaiting approval for a program, if any. */
  loadPlan(id: string): Promise<ResearchPlan | null>;
  /** Ask the lab to plan a new question. Mocked in fixture mode. */
  draftPlan(question: string): Promise<ResearchPlan>;
  subscribe?(onChange: () => void): () => void;
}

export const activeSource: LabDataSource = fixtureSource;
