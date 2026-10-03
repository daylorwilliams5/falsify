import type { LiteratureSource as LS } from '../data/types';

export function LiteratureSource({ s }: { s: LS }) {
  return (
    <article className="lit">
      <div className="lit-tags mono">
        <span className={`tag tag-${s.directness.toLowerCase()}`}>{s.directness}</span>
        <span className={`tag tag-ver ver-${s.verification}`}>{s.verification}</span>
        <span className="lit-year">{s.year}</span>
      </div>
      <a className="lit-title" href={s.url} target="_blank" rel="noreferrer">{s.title}</a>
      <div className="lit-authors">{s.authors}</div>
      <dl className="lit-dl">
        <dt>Finding</dt><dd>{s.finding}</dd>
        <dt>Relevance</dt><dd>{s.relevance}</dd>
      </dl>
      <div className="lit-hyps mono">
        {s.hypotheses.map((h) => <a key={h} href="#hypotheses" className="chip">{h}</a>)}
      </div>
    </article>
  );
}
