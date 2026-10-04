import { useState } from 'react';

// A pre-committed fork: the two outcomes the lab decided, before any data,
// how it would read.
export function StoppingRule({ intro, root, branches }: { intro: string; root: string; branches: { k: string; text: string }[] }) {
  const [hot, setHot] = useState<number | null>(null);
  const [a, b] = branches;
  return (
    <div className="fork">
      <div className="fork-intro">{intro}</div>
      <div className="fork-body">
        <div className="fork-root">{root}</div>
        <svg className="fork-lines" viewBox="0 0 80 72" preserveAspectRatio="none" aria-hidden>
          <path d="M0 36 C 30 36, 40 12, 80 12" className={`fk-path ${hot === 0 ? 'is-hot' : ''} ${hot === 1 ? 'is-dim' : ''}`} />
          <path d="M0 36 C 30 36, 40 60, 80 60" className={`fk-path ${hot === 1 ? 'is-hot' : ''} ${hot === 0 ? 'is-dim' : ''}`} />
        </svg>
        <div className="fork-branches">
          {[a, b].map((br, i) => (
            <button key={br.k} className={`fork-branch ${hot !== null && hot !== i ? 'is-dim' : ''}`}
              onMouseEnter={() => setHot(i)} onMouseLeave={() => setHot(null)} onFocus={() => setHot(i)} onBlur={() => setHot(null)}>
              <span className="fb-k">{br.k}</span>{br.text}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
