import type { ReactNode } from 'react';

export function DetailPage({ base, kicker, title, lede, children }: {
  base: string; kicker: string; title: string; lede?: string; children: ReactNode;
}) {
  return (
    <div className="detail">
      <a href={base} className="back">← Overview</a>
      <div className="label">{kicker}</div>
      <h1 className="detail-title">{title}</h1>
      {lede && <p className="detail-lede">{lede}</p>}
      <div className="detail-body">{children}</div>
    </div>
  );
}
