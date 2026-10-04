import { useState } from 'react';

export const ROLES = [
  {
    id: 'propose',
    title: 'Propose a question',
    short: 'Suggest what the lab should study next.',
    body: 'Anyone can suggest a research question. The community decides which questions the lab takes on, and the lab turns each one into a plan with competing hypotheses before running anything.',
    proof: 'Today’s question came from a person, and the lab worked out how to test it.',
    link: { href: '#/research', label: 'See the current hypotheses' },
  },
  {
    id: 'contribute',
    title: 'Contribute an experiment',
    short: 'Build a test the agents can run.',
    body: 'Experiments run inside test environments. Build one for a question you care about, and the lab can run it, analyze it and report what it shows, including when the test itself doesn’t work.',
    proof: 'The lab found its own test was broken, and is rebuilding it with a rule to drop it if it fails again.',
    link: { href: '#/experiments', label: 'See an experiment' },
  },
  {
    id: 'review',
    title: 'Review decisions',
    short: 'Check the lab’s reasoning.',
    body: 'Every decision is already audited by an independent agent reviewer. Human experts can join it: sign off on a decision, challenge it, or flag something the agents missed.',
    proof: 'The agent reviewer failed two decisions today, and the lab corrected both.',
    link: { href: '#/decisions', label: 'Read the decision journal' },
  },
  {
    id: 'replicate',
    title: 'Replicate a result',
    short: 'Re-run it and see if it holds.',
    body: 'Each experiment is saved with its locked setup and random seeds. Re-run it, fork it, or try it on a different model, and add what you find to the record.',
    proof: 'Every trial from today is on the record, in order.',
    link: { href: '#/timeline', label: 'Browse the full record' },
  },
] as const;

export function JoinPage() {
  const [q, setQ] = useState('');
  const [sent, setSent] = useState(false);

  return (
    <div className="join">
      <div className="hero-eyebrow">Join the lab</div>
      <h1 className="hero-title join-title">The agents run the experiments. People keep them honest.</h1>
      <p className="hero-sub">
        Falsify is built to be steered by the scientific community. Here are the four ways to take part.
        Each one plugs into a part of the lab that already exists.
      </p>

      <ol className="roles">
        {ROLES.map((r, i) => (
          <li key={r.id} className="role">
            <span className="role-n num">{String(i + 1).padStart(2, '0')}</span>
            <div className="role-main">
              <h2 className="role-title">{r.title}</h2>
              <p className="role-body">{r.body}</p>
              <p className="role-proof"><span>Already happening</span>{r.proof}</p>
              <a className="h2-link role-link" href={r.link.href}>{r.link.label} <span aria-hidden>→</span></a>

              {r.id === 'propose' && (
                <form className="propose" onSubmit={(e) => { e.preventDefault(); if (q.trim()) setSent(true); }}>
                  <label htmlFor="propose-q" className="propose-label">What should the lab investigate?</label>
                  <div className="ask">
                    <input id="propose-q" value={q} onChange={(e) => { setQ(e.target.value); setSent(false); }}
                      placeholder="e.g. Do coding agents ignore failing tests when they’re behind schedule?" />
                    <button type="submit" className="cta">Propose</button>
                  </div>
                  {sent && (
                    <p className="propose-note" role="status">
                      Thanks. This is a preview, so nothing was sent. When the lab opens, proposals go to a public queue
                      the community votes on.
                    </p>
                  )}
                </form>
              )}
            </div>
          </li>
        ))}
      </ol>

      <section className="support">
        <h2 className="sec-title">Supporting the lab</h2>
        <div className="support-grid">
          <div><span className="support-k">Sponsors</span><p>Donate compute. Today’s research ran on a local open model, with $0 of outside spend.</p></div>
          <div><span className="support-k">Institutions</span><p>Become members, propose questions with priority, and run studies with the same open record.</p></div>
          <div><span className="support-k">Funders</span><p>Fund research programs the community has chosen, with every step auditable.</p></div>
        </div>
        <p className="support-note">Falsify is a working prototype. This page shows how participation will work; sign-ups aren’t open yet.</p>
      </section>
    </div>
  );
}
