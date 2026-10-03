import { useEffect, useMemo, useRef, useState } from 'react';
import type { LabEvent, LabState, PIDecision } from '../../data/types';
import { chainOf, eventHeadline, eventKind, hhmm, hhmmss, LANES, type LaneId, laneOf } from '../../data/view';

const LANE_H = 58;
const TOP = 44; // room for loop labels + time axis
const ms = (iso: string) => new Date(iso).getTime();

export const ACTOR_LABEL: Record<string, string> = {
  PI: 'Principal investigator', methodology_reviewer: 'Independent reviewer', human: 'Human', engineer: 'Engineer',
  falsify: 'Lab system', director: 'Director', 'statistician-tool': 'Statistics tool',
};
export const actorLabel = (a: string) => ACTOR_LABEL[a] ?? a.charAt(0).toUpperCase() + a.slice(1);

export function SwimLanes({ events, decisions, loops, runs, selected, onSelect, laneFocus, onLaneFocus }: {
  events: LabEvent[];
  decisions: PIDecision[];
  loops: LabState['loops'];
  runs: LabState['runs'];
  selected: LabEvent | null;
  onSelect: (e: LabEvent) => void;
  laneFocus: LaneId | null;
  onLaneFocus: (l: LaneId | null) => void;
}) {
  const t0 = ms(events[0].ts) - 6 * 60000;
  const tEnd = ms(events[events.length - 1].ts);
  const t1 = tEnd + 6 * 60000;
  const x = (iso: string | number) => ((typeof iso === 'number' ? iso : ms(iso)) - t0) / (t1 - t0) * 100;
  const laneIndex = (id: LaneId) => LANES.findIndex((l) => l.id === id);
  const height = TOP + LANES.length * LANE_H;

  // Nudge marks that would overlap within a lane.
  const placed = useMemo(() => {
    const lastX: Record<string, number[]> = {};
    return events.map((e) => {
      const lane = laneOf(e.actor);
      const px = x(e.ts);
      const prev = lastX[lane] ?? [];
      const crowd = prev.filter((p) => px - p < 0.9).length;
      lastX[lane] = [...prev.filter((p) => px - p < 0.9), px];
      const offset = crowd === 0 ? 0 : (crowd % 2 ? -1 : 1) * Math.ceil(crowd / 2) * 9;
      return { e, lane, px, py: TOP + laneIndex(lane) * LANE_H + LANE_H / 2 + offset, kind: eventKind(e) };
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [events]);

  const [hover, setHover] = useState<number | null>(null);
  const active = hover !== null ? placed[hover].e : selected;
  const chain = active?.decision_id ? chainOf(active.decision_id, decisions) : null;
  const inChain = (e: LabEvent) => !!chain && !!e.decision_id && chain.has(e.decision_id);
  const chainPts = chain ? placed.filter((p) => inChain(p.e)) : [];

  // Replay: sweep a playhead across the session.
  const [play, setPlay] = useState<number | null>(null);
  const raf = useRef(0);
  const startReplay = () => {
    cancelAnimationFrame(raf.current);
    const dur = 14000, start = performance.now(), from = ms(events[0].ts);
    const step = (now: number) => {
      const p = Math.min(1, (now - start) / dur);
      setPlay(from + (tEnd - from) * p);
      if (p < 1) raf.current = requestAnimationFrame(step);
      else setTimeout(() => setPlay(null), 900);
    };
    raf.current = requestAnimationFrame(step);
  };
  const stopReplay = () => { cancelAnimationFrame(raf.current); setPlay(null); };
  useEffect(() => () => cancelAnimationFrame(raf.current), []);

  const ticks: number[] = [];
  for (let t = Math.ceil(t0 / 900000) * 900000; t < t1; t += 900000) ticks.push(t);
  const fmt = (t: number) => new Date(t).toTimeString().slice(0, 5);
  const hv = hover !== null ? placed[hover] : null;

  return (
    <div className="swim">
      <div className="swim-bar">
        <button className="replay" onClick={play === null ? startReplay : stopReplay}>
          {play === null ? <><span className="replay-icon">▶</span>Replay the session</> : <><span className="replay-icon">■</span>Stop</>}
        </button>
        {play !== null && <span className="replay-clock num">{fmt(play)}</span>}
        <span className="swim-hint">Hover a decision to trace its review and correction. Click to read it.</span>
      </div>

      <div className="swim-grid">
        <div className="swim-lanes" style={{ paddingTop: TOP }}>
          {LANES.map((l) => (
            <button key={l.id} className={`lane-label ${laneFocus === l.id ? 'is-on' : ''} ${laneFocus && laneFocus !== l.id ? 'is-dim' : ''}`}
              style={{ height: LANE_H }} onClick={() => onLaneFocus(laneFocus === l.id ? null : l.id)}>
              {l.label}
              <span className="lane-n num">{placed.filter((p) => p.lane === l.id).length}</span>
            </button>
          ))}
        </div>

        <div className="swim-plot" style={{ height }} onMouseLeave={() => setHover(null)}>
          {loops.map((lp, i) => (
            <div key={lp.n} className={`loop-band ${i % 2 ? 'is-alt' : ''}`}
              style={{ left: `${x(lp.start)}%`, width: `${(lp.end ? x(lp.end) : 100) - x(lp.start)}%` }}>
              <span className="lb-label">{lp.label} <span>· {lp.sub}</span></span>
              {lp.ended && <span className="lb-end">{lp.ended}</span>}
            </div>
          ))}
          {ticks.map((t) => (
            <div key={t} className="tick" style={{ left: `${x(t)}%` }}><span className="num">{fmt(t)}</span></div>
          ))}
          {LANES.map((l, i) => <div key={l.id} className={`lane-row ${laneFocus && laneFocus !== l.id ? 'is-dim' : ''}`} style={{ top: TOP + i * LANE_H, height: LANE_H }} />)}

          {runs.map((r) => (
            <div key={r.id} className={`run-span ${play !== null && play < ms(r.start) ? 'is-future' : ''}`}
              style={{ left: `${x(r.start)}%`, width: `${x(r.end) - x(r.start)}%`, top: TOP + laneIndex('experiments') * LANE_H + LANE_H / 2 - 9 }}>
              <span className="num">{r.id} · 20 trials</span>
            </div>
          ))}

          <svg className="chain" viewBox={`0 0 100 ${height}`} preserveAspectRatio="none" aria-hidden>
            {chainPts.slice(1).map((p, i) => {
              const a = chainPts[i];
              const mx = (a.px + p.px) / 2;
              return <path key={p.e.i} d={`M${a.px} ${a.py} C ${mx} ${a.py}, ${mx} ${p.py}, ${p.px} ${p.py}`} vectorEffect="non-scaling-stroke" />;
            })}
          </svg>

          {play !== null && <div className="playhead" style={{ left: `${x(play)}%` }} />}

          {placed.map((p, i) => {
            const future = play !== null && ms(p.e.ts) > play;
            const dim = (laneFocus && p.lane !== laneFocus) || (chain && !inChain(p.e));
            return (
              <button
                key={p.e.i}
                className={`mark k-${p.kind} ${dim ? 'is-dim' : ''} ${future ? 'is-future' : ''} ${selected?.i === p.e.i ? 'is-sel' : ''} ${chain && inChain(p.e) ? 'is-chain' : ''}`}
                style={{ left: `${p.px}%`, top: p.py }}
                onMouseEnter={() => setHover(i)}
                onFocus={() => setHover(i)}
                onBlur={() => setHover(null)}
                onClick={() => onSelect(p.e)}
                aria-label={`${hhmm(p.e.ts)} ${actorLabel(p.e.actor)}: ${eventHeadline(p.e, decisions)}`}
              />
            );
          })}

          {hv && (
            <div className={`tip ${hv.px > 70 ? 'is-left' : ''}`} style={{ left: `${hv.px}%`, top: hv.py }}>
              <div className="tip-head"><span className="num">{hhmmss(hv.e.ts)}</span> · {actorLabel(hv.e.actor)}{hv.e.decision_id && <span className="num"> · {hv.e.decision_id}</span>}</div>
              <div className="tip-text">{eventHeadline(hv.e, decisions)}</div>
            </div>
          )}
        </div>
      </div>

      <div className="swim-key">
        <span><i className="mark k-directive" />Human directive</span>
        <span><i className="mark k-decision" />Decision</span>
        <span><i className="mark k-review" />Review</span>
        <span><i className="mark k-review-fail" />Review failed a decision</span>
        <span><i className="mark k-fix" />Fix or correction</span>
        <span><i className="mark k-note" />Other</span>
      </div>
    </div>
  );
}
