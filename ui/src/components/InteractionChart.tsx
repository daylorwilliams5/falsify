import type { CellResult } from '../data/types';

// Interaction plot: wasted actions by prior investment, one line per org type,
// 95% normal-approx CI whiskers. Dodged on x so overlapping series stay visible.
export function InteractionChart({ cells }: { cells: CellResult[] }) {
  const W = 460, H = 210, m = { t: 14, r: 112, b: 34, l: 34 };
  const iw = W - m.l - m.r, ih = H - m.t - m.b;
  const yMax = 3;
  const y = (v: number) => m.t + ih - (Math.min(v, yMax) / yMax) * ih;
  const xs = [m.l + iw * 0.18, m.l + iw * 0.82];
  const ks = [1, 10];
  const series = [
    { org: 'single', label: 'Single', cls: 's-single', dx: -7 },
    { org: 'multi', label: 'Multi-agent', cls: 's-multi', dx: 7 },
  ] as const;
  const get = (org: string, k: number) =>
    cells.find((c) => c.org === org && c.k === k && c.update === 'invalidating')!;
  const ci = (c: CellResult) => {
    const h = 1.96 * (c.wasted_sd / Math.sqrt(c.n));
    return [Math.max(0, c.wasted_mean - h), c.wasted_mean + h];
  };

  return (
    <svg className="chart" viewBox={`0 0 ${W} ${H}`} role="img" aria-label="Wasted actions by prior investment and organization">
      {/* floor band */}
      <rect x={m.l} y={y(0.15)} width={iw} height={y(0) - y(0.15)} className="floor-band" />
      <text x={m.l + iw / 2} y={y(0) - 5} className="ax floor-label" textAnchor="middle">FLOOR · 18/20 trials = 0</text>
      {[0, 1, 2, 3].map((t) => (
        <g key={t}>
          <line x1={m.l} x2={m.l + iw} y1={y(t)} y2={y(t)} className={t === 0 ? 'axis' : 'grid'} />
          <text x={m.l - 8} y={y(t) + 3} className="ax" textAnchor="end">{t}</text>
        </g>
      ))}
      <text x={10} y={m.t + ih / 2} className="ax ax-title" transform={`rotate(-90 10 ${m.t + ih / 2})`} textAnchor="middle">wasted actions</text>
      {ks.map((k, i) => (
        <g key={k}>
          <line x1={xs[i]} x2={xs[i]} y1={y(0)} y2={y(0) + 4} className="axis" />
          <text x={xs[i]} y={H - 14} className="ax" textAnchor="middle">{k === 1 ? 'LOW' : 'HIGH'} </text>
          <text x={xs[i]} y={H - 3} className="ax ax-dim" textAnchor="middle">k={k}</text>
        </g>
      ))}
      {series.map((s) => {
        const pts = ks.map((k, i) => ({ c: get(s.org, k), x: xs[i] + s.dx }));
        return (
          <g key={s.org} className={s.cls}>
            <polyline points={pts.map((p) => `${p.x},${y(p.c.wasted_mean)}`).join(' ')} className="line" />
            {pts.map((p) => {
              const [lo, hi] = ci(p.c);
              const capped = hi > yMax;
              return (
                <g key={p.c.cell}>
                  <line x1={p.x} x2={p.x} y1={y(lo)} y2={y(hi)} className="whisker" />
                  <line x1={p.x - 4} x2={p.x + 4} y1={y(lo)} y2={y(lo)} className="whisker" />
                  {!capped && <line x1={p.x - 4} x2={p.x + 4} y1={y(hi)} y2={y(hi)} className="whisker" />}
                  <circle cx={p.x} cy={y(p.c.wasted_mean)} r={3.6} className="pt" />
                  <text x={p.x + (s.dx > 0 ? 8 : -8)} y={y(p.c.wasted_mean) - 6} className="ax pt-label" textAnchor={s.dx > 0 ? 'start' : 'end'}>
                    {p.c.wasted_mean.toFixed(1)}
                  </text>
                </g>
              );
            })}
          </g>
        );
      })}
      {series.map((s, i) => (
        <g key={s.org} className={s.cls} transform={`translate(${m.l + iw + 18}, ${y(2.8) + i * 16})`}>
          <line x1={0} x2={14} y1={0} y2={0} className="line" />
          <circle cx={7} cy={0} r={3} className="pt" />
          <text x={20} y={3} className="ax legend">{s.label}</text>
        </g>
      ))}
      <text x={m.l + iw + 18} y={y(2.8) + 42} className="ax ax-dim">n=5 / cell</text>
      <text x={m.l + iw + 18} y={y(2.8) + 54} className="ax ax-dim">whisker 95% CI</text>
      <text x={m.l + iw + 18} y={y(2.8) + 66} className="ax ax-dim">benign ctrl = 0</text>
    </svg>
  );
}
