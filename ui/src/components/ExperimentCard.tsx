import type { Experiment } from '../data/types';
import { StatusBadge } from './StatusBadge';
import { Metric } from './Metric';
import { InteractionChart } from './InteractionChart';

export function ExperimentCard({ x }: { x: Experiment }) {
  const pct = (x.trials.done / x.trials.total) * 100;
  const [f1, f2] = x.design.factors;
  return (
    <div className="exp">
      <div className="exp-top">
        <div>
          <div className="exp-id mono">{x.id}</div>
          <div className="exp-q">{x.question}</div>
        </div>
        <StatusBadge status={x.status} size="md" />
      </div>

      <div className="exp-grid">
        <div className="exp-design">
          <div className="lbl">Design · <span className="mono">{x.design.label}</span></div>
          <div className="matrix">
            <span />
            {f2.levels.map((l) => <span key={l} className="mx-h mono">{l}</span>)}
            {f1.levels.map((r, ri) => (
              <FragmentRow key={r} label={r} cells={x.cells.filter((c) => c.org === (ri === 0 ? 'single' : 'multi') && c.update === 'invalidating')} />
            ))}
          </div>
          <div className="mx-foot mono">cell mean · wasted actions</div>

          <div className="lbl" style={{ marginTop: 14 }}>Trials</div>
          <div className="trials">
            <span className="mono trials-n">{x.trials.done}<span className="muted"> / {x.trials.total}</span></span>
            <span className="mono muted tiny">{x.trials.invalid} invalid</span>
          </div>
          <div className="progress"><i style={{ width: `${pct}%` }} /></div>
        </div>

        <div className="exp-result">
          <div className="lbl">Primary result · {x.primary?.metric}</div>
          <div className="primary mono">
            Δ = {x.primary?.delta.toFixed(1)}
          </div>
          <div className="ci mono">
            95% CI [{x.primary?.ci95[0].toFixed(1)}, {x.primary?.ci95[1].toFixed(1)}]
            <CiStrip lo={x.primary!.ci95[0]} hi={x.primary!.ci95[1]} est={x.primary!.delta} />
          </div>
          <div className="mono muted tiny">bootstrap n={x.primary?.n_boot.toLocaleString()} · threshold 0.5</div>
          <div className="exp-hstatus">
            <span className="mono">{x.hypothesis}</span>
            <StatusBadge status={x.hypothesis_status} size="md" />
          </div>
        </div>
      </div>

      {x.flags.map((f) => (
        <div key={f.title} className={`flag flag-${f.level}`}>
          <span className="flag-mark mono">{f.level === 'warn' ? '▲' : 'i'}</span>
          <span className="flag-title mono">{f.title}</span>
          <span className="flag-detail">{f.detail}</span>
        </div>
      ))}

      <div className="exp-chart">
        <InteractionChart cells={x.cells} />
      </div>

      <div className="exp-metrics">
        {x.metrics.map((m) => <Metric key={m.label} {...m} />)}
      </div>
      <div className="exp-foot mono">
        <span>{x.env}</span><span>{x.spec_hash}</span><span>seed-locked</span>
      </div>
    </div>
  );
}

function FragmentRow({ label, cells }: { label: string; cells: Experiment['cells'] }) {
  return (
    <>
      <span className="mx-r mono">{label}</span>
      {cells.sort((a, b) => a.k - b.k).map((c) => (
        <span key={c.cell} className={`mx-c ${c.wasted_mean === 0 ? 'is-zero' : ''}`}>
          <span className="mono mx-id">{c.cell}</span>
          <span className="mono mx-v">{c.wasted_mean.toFixed(1)}</span>
        </span>
      ))}
    </>
  );
}

function CiStrip({ lo, hi, est }: { lo: number; hi: number; est: number }) {
  const R = 2.5;
  const p = (v: number) => ((v + R) / (2 * R)) * 100;
  return (
    <span className="ci-strip">
      <i className="ci-zero" style={{ left: `${p(0)}%` }} />
      <i className="ci-thresh" style={{ left: `${p(0.5)}%` }} />
      <i className="ci-range" style={{ left: `${p(lo)}%`, width: `${p(hi) - p(lo)}%` }} />
      <i className="ci-est" style={{ left: `${p(est)}%` }} />
    </span>
  );
}
