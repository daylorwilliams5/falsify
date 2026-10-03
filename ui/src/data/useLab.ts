import { useEffect, useState } from 'react';
import type { LabSnapshot, ProgramSummary, ResearchPlan } from './types';
import { activeSource } from './source';

const LOADING = Symbol('loading');
type Loadable<T> = T | typeof LOADING;

function useAsync<T>(fn: () => Promise<T>, deps: unknown[]): Loadable<T> {
  const [v, setV] = useState<Loadable<T>>(LOADING);
  useEffect(() => {
    let alive = true;
    setV(LOADING);
    fn().then((r) => alive && setV(r));
    return () => { alive = false; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);
  return v;
}

export const isLoading = (v: unknown): v is typeof LOADING => v === LOADING;
export const usePrograms = () => useAsync<ProgramSummary[]>(() => activeSource.listPrograms(), []);
export const useProgram = (id: string) => useAsync<LabSnapshot | null>(() => activeSource.loadProgram(id), [id]);
export const usePlan = (id: string) => useAsync<ResearchPlan | null>(() => activeSource.loadPlan(id), [id]);
