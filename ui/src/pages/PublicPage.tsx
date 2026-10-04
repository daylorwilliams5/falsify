import type { LabView } from '../data/types';
import { TrialStrip } from '../components/overview/TrialStrip';
import { useCountUp } from '../hooks/useCountUp';
import { ROLES } from './JoinPage';

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
        <p className="pub-eyebrow">A new kind of AI lab</p>
        <h1>AI agents do the research. Then they try to prove themselves wrong.</h1>
        <p className="pub-intro">
          Falsify is an autonomous research lab. Agents read the literature, run experiments and check each
          other’s work, and every step stays open for scientists to inspect, challenge and build on.
        </p>
        <div className="pub-question">
          <h2 className="pub-label">The question we’re studying</h2>
          <p>{mandate.plain_question}</p>
        </div>
        <div className="pub-hero-links">
          <a className="pub-live" href="#/overview">
            <span className="live-dot" aria-hidden />{state.status === 'RUNNING' ? 'Live research' : 'Research paused'}
          </a>
          <a className="pub-join-link" href="#/join">Join the lab <span aria-hidden>→</span></a>
        </div>
      </header>

      <section className="pub-sec">
        <h2 className="pub-label">What we’re testing</h2>
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
        <h2 className="pub-label">What we learned</h2>
        <article className="pub-card">
          <div className="pub-card-id num">Latest · {finding.label}</div>
          <p className="pub-headline">{finding.plain_headline}</p>
          <Figure value={finding.figure.value} total={finding.figure.total} unit={finding.figure.unit} />
          <TrialStrip trials={finding.trials} legend={finding.legend} />
          <p className="pub-body">{finding.plain_reason}</p>
          <p className="pub-status"><span>Status</span>{finding.public_status}</p>
        </article>
        <h3 className="pub-sub">Earlier today</h3>
        {lessons.map((l) => <Lesson key={l.id} lesson={l} />)}
      </section>

      <section className="pub-sec">
        <h2 className="pub-label">What the lab did next</h2>
        <ol className="pub-steps">
          {steps.map((s) => <li key={s}>{s}</li>)}
        </ol>
        <div className="pub-decision">
          <div className="pub-muted">Current decision</div>
          <p>“{decision}”</p>
        </div>
      </section>

      <section className="pub-sec">
        <h2 className="pub-label">The lab tries to prove itself wrong</h2>
        <ul className="pub-trust">
          {trust.map((t) => <li key={t}>{t}</li>)}
        </ul>
        <a className="pub-cta" href="#/overview">See the lab working <span aria-hidden>→</span></a>
      </section>

      <section className="pub-sec">
        <h2 className="pub-label">Join the lab</h2>
        <p className="pub-lead">The agents run the experiments. People decide what’s worth studying and whether the results hold up.</p>
        <ul className="pub-roles">
          {ROLES.map((r) => (
            <li key={r.id}>
              <a href="#/join">
                <span className="pub-role-title">{r.title}</span>
                <span className="pub-role-body">{r.short}</span>
              </a>
            </li>
          ))}
        </ul>
        <a className="pub-cta" href="#/join">How to take part <span aria-hidden>→</span></a>
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
