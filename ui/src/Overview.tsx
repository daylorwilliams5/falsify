import type { LabSnapshot } from './data/types';
import { LoopTimeline } from './components/LoopTimeline';

export function Overview({ lab, base }: { lab: LabSnapshot; base: string }) {
  const { state, activity } = lab;
  const r = state.latest_result;
  const d = state.next_decision;

  return (
    <div className="ov">
      <section className="ov-hero">
        <div className="ov-label">Research question</div>
        <h1 className="ov-question">“{state.question_short}”</h1>
      </section>

      <div className="ov-pair">
        <section className="ov-block">
          <div className="ov-label">Latest result <span className="ov-label-id">{r.label}</span></div>
          <p className="ov-headline">{r.headline}</p>
          <p className="ov-body">{r.finding}</p>
          <p className="ov-verdict"><span>{r.verdict}</span> — {r.reason}</p>
          <a className="ov-link" href={`${base}/experiments/${r.experiment}`}>View experiment <span>→</span></a>
        </section>

        <section className="ov-block">
          <div className="ov-label">Next move</div>
          <p className="ov-headline">The lab is deciding between</p>
          <ol className="ov-options">
            {d.options.map((o) => (
              <li key={o.id} className={o.id === d.selected ? 'is-leading' : ''}>
                <span className="opt-letter">{o.id}</span>
                <span className="opt-text">
                  {o.short}
                  {o.id === d.selected && <em>leading</em>}
                </span>
              </li>
            ))}
          </ol>
          <ul className="ov-focus">
            {activity.focus.map((f) => (
              <li key={f.agent}><span className="focus-dot" />{f.agent} <span>is {f.verb}</span></li>
            ))}
          </ul>
          <a className="ov-link" href={`${base}/decision`}>Review proposal <span>→</span></a>
        </section>
      </div>

      <section className="ov-loop">
        <div className="ov-label">Where the lab is</div>
        <LoopTimeline phases={activity.phases} />
      </section>
    </div>
  );
}
