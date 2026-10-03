// Unit chart: one mark per invalidating trial. Filled = corrected immediately
// (0 wasted actions); ring = persisted on the invalidated plan.
export function TrialStrip({ wasted }: { wasted: number[] }) {
  return (
    <div className="tstrip" role="img" aria-label={`${wasted.filter((w) => w === 0).length} of ${wasted.length} trials corrected immediately`}>
      {wasted.map((w, i) => (
        <span key={i} className={w === 0 ? 'ts-ok' : 'ts-persist'} title={`trial ${i + 1}: ${w} wasted actions`} />
      ))}
    </div>
  );
}
