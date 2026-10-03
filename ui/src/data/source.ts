import type { LabSnapshot } from './types';
import { fixtureSource } from './adapters/fixtures';

/**
 * A LabDataSource is the only thing the UI knows about where data comes from.
 *
 *   fixtureSource  — static JSON in ./fixtures (today)
 *   artifactSource — maps registry/, results/, timeline.jsonl, critiques/,
 *                    sources/ into the same LabSnapshot (later; see
 *                    ./adapters/artifacts.ts for the planned mapping)
 *
 * `subscribe` lets a live source push updates (file watcher, SSE, websocket)
 * without components caring.
 */
export interface LabDataSource {
  name: string;
  load(): Promise<LabSnapshot>;
  subscribe?(onChange: (snap: LabSnapshot) => void): () => void;
}

export const activeSource: LabDataSource = fixtureSource;
