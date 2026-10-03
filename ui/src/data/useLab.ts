import { useEffect, useState } from 'react';
import type { LabSnapshot } from './types';
import { activeSource } from './source';

export function useLab(): LabSnapshot | null {
  const [snap, setSnap] = useState<LabSnapshot | null>(null);
  useEffect(() => {
    let alive = true;
    activeSource.load().then((s) => alive && setSnap(s));
    const unsub = activeSource.subscribe?.((s) => alive && setSnap(s));
    return () => { alive = false; unsub?.(); };
  }, []);
  return snap;
}
