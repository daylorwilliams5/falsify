import { useState } from 'react';

// A pre-committed fork: what happens if the rebuilt test works, and if it fails.
export function StoppingRule({ intro, ifWorks, ifFails }: { intro: string; ifWorks: string; ifFails: string }) {
  const [hot, setHot] = useState<'works' | 'fails' | null>(null);
  return (
    <div className="fork">
      <div className="fork-intro">{intro}</div>
      <div className="fork-body">
        <div className="fork-root">Rebuilt test</div>
        <svg className="fork-lines" viewBox="0 0 80 72" preserveAspectRatio="none" aria-hidden>
          <path d="M0 36 C 30 36, 40 12, 80 12" className={`fk-path ${hot === 'works' ? 'is-hot' : ''} ${hot === 'fails' ? 'is-dim' : ''}`} />
          <path d="M0 36 C 30 36, 40 60, 80 60" className={`fk-path ${hot === 'fails' ? 'is-hot' : ''} ${hot === 'works' ? 'is-dim' : ''}`} />
        </svg>
        <div className="fork-branches">
          <button className={`fork-branch ${hot === 'fails' ? 'is-dim' : ''}`} onMouseEnter={() => setHot('works')} onMouseLeave={() => setHot(null)} onFocus={() => setHot('works')} onBlur={() => setHot(null)}>
            <span className="fb-k">works</span>{ifWorks}
          </button>
          <button className={`fork-branch ${hot === 'works' ? 'is-dim' : ''}`} onMouseEnter={() => setHot('fails')} onMouseLeave={() => setHot(null)} onFocus={() => setHot('fails')} onBlur={() => setHot(null)}>
            <span className="fb-k">fails</span>{ifFails}
          </button>
        </div>
      </div>
    </div>
  );
}
