import type { ReactNode } from 'react';

export function Metric({ label, value, hint, tone, size = 'sm' }: {
  label: string; value: ReactNode; hint?: string; tone?: 'warn' | 'good' | 'live' | 'accent'; size?: 'sm' | 'lg';
}) {
  return (
    <div className={`metric metric-${size}`}>
      <div className="metric-label">{label}</div>
      <div className={`metric-value mono ${tone ? `fg-${tone}` : ''}`}>{value}</div>
      {hint && <div className="metric-hint">{hint}</div>}
    </div>
  );
}
