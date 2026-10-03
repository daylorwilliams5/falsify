import type { LabView } from '../data/types';
import { TrialStrip } from '../components/overview/TrialStrip';
import { useCountUp } from '../hooks/useCountUp';

const LOOP = ['Question', 'Hypothesis', 'Experiment', 'Result', 'Challenge', 'Next experiment'];

// The public demo: one page a judge can understand in 30 seconds. The result is
// the product; the machinery lives behind "See the lab working" (#/overview).
export function PublicPage({ lab }: { lab: LabView }) {
  const { mandate, finding, state } = lab;
  const { testing, lessons, steps, decision, trust } = state.public;
  const pct = testing.trials_total ? (testing.trials_done / testing.trials_total) * 100 : 0;

  return (
    <div className="pub">
      <header className="pub-hero">
        <div className="pub-brand">FALSIFY</div>
        <p className="pub-tag">An autonomous scientific lab for understanding AI agents.</p>
        <h1>{mandate.plain_question}</h1>
        <a className="pub-live" href="#/overview">
          <span className="live-dot" />{state.status === 'RUNNING' ? 'Live research' : 'Research paused'}
        </a>
      </header>

      <section className="pub-sec">
        <div className="pub-label">What we’re testing</div>
        <p className="pub-lead">{testing.question}</p>
        <dl className="pub-dl">
          <div><dt>Manipulation</dt><dd>{testing.manipulation}</dd></div>
          <div><dt>Behavior measured</dt><dd>{testing.behavior}</dd></div>
        </dl>
        <div className="pub-progress">
          <span className="num">Experiment {testing.id}</span>
          <span className="pub-bar"><i style={{ width: `${pct}%` }} /></span>
          <span className="num">{testing.trials_done} / {testing.trials_total} trials</span>
        </div>
        <p className="pub-muted">{testing.status}</p>
      </section>

      <section className="pub-sec pub-learned">
        <div className="pub-label">What we learned</div>
        {lessons.map((l) => <Lesson key={l.id} lesson={l} />)}
        <article className="pub-card">
          <div className="pub-card-id num">{finding.label}</div>
          <p className="pub-headline">{finding.plain_headline}</p>
          <Figure value={finding.figure.value} total={finding.figure.total} unit={finding.figure.unit} />
          <TrialStrip trials={finding.trials} />
          <p className="pub-body">{finding.plain_reason} The lab stopped the experiment and rebuilt the test instead of reporting a discovery.</p>
          <p className="pub-status"><span>Status</span>Instrument failure, no conclusion drawn</p>
        </article>
      </section>

      <section className="pub-sec">
        <div className="pub-label">What the lab did next</div>
        <ol className="pub-steps">
          {steps.map((s) => <li key={s}>{s}</li>)}
        </ol>
        <div className="pub-decision">
          <div className="pub-muted">Current decision</div>
          <p>“{decision}”</p>
        </div>
      </section>

      <section className="pub-sec">
        <div className="pub-label">The lab tries to prove itself wrong</div>
        <ul className="pub-trust">
          {trust.map((t) => <li key={t}>{t}</li>)}
        </ul>
        <a className="pub-cta" href="#/overview">See the lab working <span>→</span></a>
      </section>

      <footer className="pub-foot">
        <div className="pub-label">Built solo with Omnigent</div>
        <p className="pub-loop">{LOOP.join('  →  ')}</p>
      </footer>
    </div>
  );
}

function Lesson({ lesson }: { lesson: LabView['state']['public']['lessons'][number] }) {
  return (
    <article className="pub-card">
      <div className="pub-card-id num">{lesson.id}</div>
      <p className="pub-headline">{lesson.headline}</p>
      <p className="pub-body">{lesson.body}</p>
      <Figure {...lesson.figure} />
      <p className="pub-status"><span>Status</span>{lesson.status}</p>
    </article>
  );
}

function Figure({ value, total, unit }: { value: number; total: number; unit: string }) {
  const n = useCountUp(value);
  return (
    <div className="pub-figure">
      <span className="pub-num num">{n} / {total}</span>
      <span className="pub-unit">{unit}</span>
    </div>
  );
}
