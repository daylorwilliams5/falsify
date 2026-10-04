import { useEffect, useMemo, useState } from 'react';
import type { LabView } from '../data/types';
import { hhmm, LANES, type LaneId, laneOf, stoppedByReviewer } from '../data/view';
import { DayBar } from '../components/timeline/DayBar';
import { Chapter } from '../components/timeline/Chapter';

export function TimelinePage({ lab, focus }: { lab: LabView; focus?: string }) {
  const { events, decisions, state } = lab;
  const [showAll, setShowAll] = useState(false);
  const [who, setWho] = useState<LaneId | null>(null);
  const [selected, setSelected] = useState<number | null>(null);
  const [activeLoop, setActiveLoop] = useState<number | null>(null);

  const loopOf = (ts: string) => [...state.loops].reverse().find((l) => ts >= l.start) ?? state.loops[0];

  // #/timeline/D011 opens that decision.
  useEffect(() => {
    if (!focus) return;
    const e = events.find((x) => x.decision_id === focus && x.stage === 'pi_decision');
    if (!e) return;
    setSelected(e.i);
    requestAnimationFrame(() => document.getElementById(`loop-${loopOf(e.ts).n}`)?.scrollIntoView({ block: 'start' }));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [focus, events]);

  // Highlight the loop whose chapter is on screen.
  useEffect(() => {
    const io = new IntersectionObserver((entries) => {
      const v = entries.filter((x) => x.isIntersecting).sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top)[0];
      if (v) setActiveLoop(Number(v.target.id.replace('loop-', '')));
    }, { rootMargin: '-30% 0px -60% 0px' });
    document.querySelectorAll('.ch').forEach((el) => io.observe(el));
    return () => io.disconnect();
  }, []);

  const stats = useMemo(() => [
    [state.loops.length, 'research loops'],
    [decisions.length, 'decisions'],
    [stoppedByReviewer(decisions).length, 'stopped by the reviewer'],
    [decisions.filter((d) => d.human_approval).length, 'human approvals'],
    [state.runs.length, 'experiments run'],
  ] as const, [state, decisions]);

  const filtered = who ? events.filter((e) => laneOf(e.actor) === who) : events;
  const jump = (n: number) => document.getElementById(`loop-${n}`)?.scrollIntoView({ behavior: 'smooth', block: 'start' });

  return (
    <div className="tl3">
      <div className="label">Timeline</div>
      <h1 className="dec-title">What happened, in order</h1>
      <p className="tl2-asof">
        One day of autonomous research, October 3, <span className="num">{hhmm(events[0].ts)}–{hhmm(events[events.length - 1].ts)}</span>.
        Every entry comes from the lab’s own record.
      </p>

      <div className="tl2-stats">
        {stats.map(([n, label]) => <div key={label}><span className="num">{n}</span>{label}</div>)}
      </div>

      <section className="tl3-day">
        <div className="h2-label">The day at a glance</div>
        <DayBar loops={state.loops} runs={state.runs} events={events} decisions={decisions} active={activeLoop} onJump={jump} />
      </section>

      <div className="tl3-controls">
        <div className="seg" role="group" aria-label="Detail level">
          <button className={!showAll ? 'is-on' : ''} onClick={() => setShowAll(false)}>Key moments</button>
          <button className={showAll ? 'is-on' : ''} onClick={() => setShowAll(true)}>Everything</button>
        </div>
        <div className="who" role="group" aria-label="Filter by who acted">
          <button className={!who ? 'is-on' : ''} onClick={() => setWho(null)}>Everyone</button>
          {LANES.map((l) => (
            <button key={l.id} className={who === l.id ? 'is-on' : ''} onClick={() => setWho(who === l.id ? null : l.id)}>{l.label}</button>
          ))}
        </div>
      </div>

      {state.loops.map((l) => {
        const evs = filtered.filter((e) => loopOf(e.ts).n === l.n);
        return evs.length ? (
          <Chapter key={l.n} loop={l} events={evs} decisions={decisions} showAll={showAll || !!who} selected={selected} onSelect={setSelected} />
        ) : null;
      })}
    </div>
  );
}
