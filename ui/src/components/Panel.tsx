import type { ReactNode } from 'react';

export function Panel({ id, index, title, meta, children, className = '' }: {
  id?: string; index?: string; title: string; meta?: ReactNode; children: ReactNode; className?: string;
}) {
  return (
    <section id={id} className={`panel ${className}`}>
      <header className="panel-head">
        <div className="panel-title">
          {index && <span className="panel-index mono">{index}</span>}
          <h2>{title}</h2>
        </div>
        {meta && <div className="panel-meta">{meta}</div>}
      </header>
      <div className="panel-body">{children}</div>
    </section>
  );
}
