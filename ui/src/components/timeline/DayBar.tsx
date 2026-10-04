import type { LabEvent, LabState, PIDecision } from '../../data/types';
import { hhmm, stoppedByReviewer } from '../../data/view';

const ms = (iso: string) => new Date(iso).getTime();

// The whole day on one line: loops as blocks, experiment runs underneath,
// and only the moments that matter most (human approvals, reviewer stops) above.
export function DayBar({ loops, runs, events, decisions, active, onJump }: {
  loops: LabState['loops']; runs: LabState['runs']; events: LabEvent[]; decisions: PIDecision[];
  active: number | null; onJump: (n: number) => void;
}) {
  const hour = 3600000;
  const t0 = Math.floor(ms(events[0].ts) / hour) * hour;
  const tEnd = ms(events[events.length - 1].ts);
  const t1 = Math.ceil(tEnd / hour) * hour;
  const x = (t: string | number) => (((typeof t === 'number' ? t : ms(t)) - t0) / (t1 - t0)) * 100;
  const hours: number[] = [];
  for (let t = t0; t <= t1; t += hour) hours.push(t);

  const stopped = new Set(stoppedByReviewer(decisions).map((d) => d.id));
  const marks = [
    ...decisions.filter((d) => d.human_approval).map((d) => ({ ts: d.human_approval!.ts, kind: 'human', label: `${hhmm(d.human_approval!.ts)} · Human approved ${d.id}` })),
    ...events.filter((e) => e.stage === 'methodology_review' && e.decision_id && stopped.has(e.decision_id) && ['FAIL', 'BLOCK', 'ESCALATE'].includes(e.verdict ?? ''))
      .map((e) => ({ ts: e.ts, kind: 'stop', label: `${hhmm(e.ts)} · Reviewer: ${e.verdict} on ${e.decision_id}` })),
  ];

  return (
    <div className="day">
      <div className="day-marks" aria-hidden>
        {marks.map((m, i) => <span key={i} className={`day-mark m-${m.kind}`} style={{ left: `${x(m.ts)}%` }} title={m.label} />)}
      </div>
      <div className="day-track">
        {loops.map((l) => {
          const w = (l.end ? x(l.end) : x(tEnd)) - x(l.start);
          return (
            <button key={l.n} className={`day-loop ${active === l.n ? 'is-on' : ''}`} style={{ left: `${x(l.start)}%`, width: `${w}%` }}
              onClick={() => onJump(l.n)} title={`${l.label}: ${l.title ?? l.sub}`}>
              <span>{w > 9 ? l.label : l.n}</span>
            </button>
          );
        })}
      </div>
      <div className="day-runs">
        {runs.map((r) => (
          <span key={r.id} className="day-run" style={{ left: `${x(r.start)}%`, width: `max(${x(r.end) - x(r.start)}%, 6px)` }}
            title={`${r.id} · ${r.trials} trials · ${hhmm(r.start)}–${hhmm(r.end)}`}>
            <i className="num">{r.id}</i>
          </span>
        ))}
      </div>
      <div className="day-hours">
        {hours.map((t) => <span key={t} className="num" style={{ left: `${x(t)}%` }}>{new Date(t).toTimeString().slice(0, 5)}</span>)}
      </div>
      <div className="day-key">
        <span><i className="day-mark m-human" />Human approval</span>
        <span><i className="day-mark m-stop" />Reviewer stopped a decision</span>
        <span><i className="day-run-key" />Experiment running</span>
      </div>
    </div>
  );
}
