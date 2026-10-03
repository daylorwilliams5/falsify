import type { Status } from '../data/types';

const TONE: Record<string, string> = {
  UNTESTED: 'muted', IDLE: 'muted', QUEUED: 'muted',
  RUNNING: 'live',
  SUPPORTED: 'good', COMPLETE: 'good', READY: 'good',
  FALSIFIED: 'bad', BLOCKED: 'bad',
  INCONCLUSIVE: 'warn',
  NEEDS_REPLICATION: 'violet',
  PROPOSED: 'accent', SELECTED: 'accent',
};

export function StatusBadge({ status, size = 'sm' }: { status: Status; size?: 'sm' | 'md' }) {
  const tone = TONE[status] ?? 'muted';
  return (
    <span className={`badge badge-${tone} badge-${size}`}>
      {status === 'RUNNING' && <span className="pulse-dot" />}
      {status.replace('_', ' ')}
    </span>
  );
}

export function StatusDot({ status }: { status: Status }) {
  const tone = TONE[status] ?? 'muted';
  return <span className={`dot dot-${tone} ${status === 'RUNNING' ? 'dot-pulse' : ''}`} />;
}
