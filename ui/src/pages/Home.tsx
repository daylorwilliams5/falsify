import { useState } from 'react';
import type { ProgramSummary } from '../data/types';
import { LoopDots } from '../components/LoopTimeline';

export const EXAMPLE_QUESTION = 'Do LLM agents game their evaluation metric when they know they’re being scored?';

export function Home({ programs }: { programs: ProgramSummary[] }) {
  const [q, setQ] = useState('');
  const go = () => { window.location.hash = `#/new/${encodeURIComponent(q.trim() || EXAMPLE_QUESTION)}`; };
  const waiting = programs.filter((p) => p.needs_you).length;

  return (
    <div className="home">
      <section className="home-hero">
        <h1 className="home-title">What should the lab investigate?</h1>
        <p className="home-sub">
          Ask any question you can test with computational experiments. An agent team reads the literature,
          proposes competing hypotheses, runs experiments and tries to prove itself wrong, then stops for your approval.
        </p>
        <form className="ask" onSubmit={(e) => { e.preventDefault(); go(); }}>
          <input value={q} onChange={(e) => setQ(e.target.value)} placeholder={EXAMPLE_QUESTION} aria-label="Research question" />
          <button type="submit" className="cta">Plan it <span>→</span></button>
        </form>
      </section>

      <section className="home-programs">
        <div className="label">
          Research programs
          {waiting > 0 && <span className="home-waiting">{waiting} need you</span>}
        </div>
        <ul className="prog-list">
          {programs.map((p) => (
            <li key={p.id}>
              <a href={`#/p/${p.id}`} className="prog">
                <div className="prog-main">
                  <div className="prog-title">{p.title}</div>
                  <div className="prog-q">{p.question}</div>
                  {p.latest && <div className="prog-latest">Latest: {p.latest}</div>}
                </div>
                <LoopDots current={p.phase} />
                <div className="prog-state">
                  {p.needs_you
                    ? <span className="prog-needs"><span className="focus-dot" />{p.needs_you}</span>
                    : <span className="prog-act">{p.activity}</span>}
                </div>
              </a>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}
