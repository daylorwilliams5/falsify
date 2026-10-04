import { useEffect, useRef, useState } from 'react';
import type { PIDecision } from '../../data/types';
import {
  hhmm, latestReview, LEVEL_LABEL, OUTCOME_LABEL, type Outcome, respondersTo, reviewChecks, shortCite, verdictLabel, verdictTone,
} from '../../data/view';

export function DecisionEntry({ d, all, outcome, focused }: {
  d: PIDecision; all: PIDecision[]; outcome: Outcome; focused: boolean;
}) {
  const [open, setOpen] = useState(focused);
  const ref = useRef<HTMLElement>(null);
  useEffect(() => {
    if (focused) { setOpen(true); ref.current?.scrollIntoView({ block: 'start' }); }
  }, [focused]);

  const r = latestReview(d);
  const later = respondersTo(d, all);
  const checks = r ? reviewChecks(r) : [];

  return (
    <article ref={ref} id={d.id} className={`entry out-${outcome.toLowerCase()} ${open ? 'is-open' : ''}`}>
      <div className="entry-side">
        <span className="entry-id">{d.id}</span>
        <span className="entry-time num">{hhmm(d.ts)}</span>
        <span className="entry-level">Level {d.level} · {LEVEL_LABEL[d.level].toLowerCase()}</span>
      </div>

      <div className="entry-main">
        <div className={`entry-outcome`}>{outcome === 'IN_REVIEW' && <span className="run-dot" />}{OUTCOME_LABEL[outcome]}</div>
        <h3 className="entry-summary">{d.summary ?? d.decision}</h3>
        {d.rationale && <p className="entry-why">{d.rationale}</p>}

        <div className="entry-facts">
          <span><span className="k">Confidence</span><span className="num">{d.confidence.toFixed(2)}</span></span>
          <span><span className="k">Review</span>{r ? <span className={`verdict v-${verdictTone(r.verdict)} num`}>{verdictLabel(r.verdict)}</span> : <span className="muted">pending</span>}</span>
          {d.responds_to?.length ? (
            <span><span className="k">Responds to</span>{d.responds_to.map((id) => <a key={id} href={`#/decisions/${id}`} className="xref num">{id}</a>)}</span>
          ) : null}
          {later.length ? (
            <span><span className="k">{outcome === 'CORRECTED' ? 'Corrected by' : 'Followed by'}</span>{later.map((x) => <a key={x.id} href={`#/decisions/${x.id}`} className="xref num">{x.id}</a>)}</span>
          ) : null}
        </div>

        {d.resulting_action && <p className="entry-result"><span className="k">Resulting action</span>{d.resulting_action}</p>}
        {d.human_approval && (
          <p className="entry-human"><span className="k">Human decision · Level 3 gate · <span className="num">{hhmm(d.human_approval.ts)}</span></span>Approved by the human through an Omnigent approval card.</p>
        )}
        {d.remediated && (
          <p className="entry-result"><span className="k">Review cleared · <span className="num">{hhmm(d.remediated.ts)}</span></span>{d.remediated.text}</p>
        )}
        {d.engineering_fix && (
          <p className="entry-result"><span className="k">Fixed outside the PI · {d.engineering_fix.by} · <span className="num">{hhmm(d.engineering_fix.ts)}</span></span>{d.engineering_fix.text}</p>
        )}

        <button className="entry-toggle" onClick={() => setOpen((o) => !o)}>{open ? 'Hide reasoning and audit' : 'Reasoning and audit'}</button>

        {open && (
          <div className="entry-detail">
            <section>
              <div className="label">Alternatives rejected</div>
              <ul className="alts">
                {d.alternatives_rejected.map((a) => (
                  <li key={a.label}><span className="alt-label">{a.label}</span><span className="alt-reason">{a.reason}</span></li>
                ))}
              </ul>
            </section>

            <section>
              <div className="label">Methodology review</div>
              {r ? (
                <>
                  <p className="rev-line"><span className={`verdict v-${verdictTone(r.verdict)} num`}>{verdictLabel(r.verdict)}</span><span className="muted"> · {hhmm(r.ts)}</span></p>
                  {r.highlights && <ul className="rev-findings">{r.highlights.map((h) => <li key={h}>{h}</li>)}</ul>}
                  {checks.length > 0 && (
                    <ul className="rev-checks">{checks.map((c) => <li key={c.label} className={c.ok ? '' : 'is-fail'}><span>{c.ok ? '✓' : '✕'}</span>{c.label}</li>)}</ul>
                  )}
                </>
              ) : <p className="muted">Not yet reviewed.</p>}
            </section>

            <section>
              <div className="label">Evidence used</div>
              <ul className="cites">{d.cites.map((c) => <li key={c} className="num" title={c}>{shortCite(c)}</li>)}</ul>
            </section>

            <details className="full">
              <summary>Full record</summary>
              <div className="label">Decision</div>
              <p>{d.decision}</p>
              <div className="label">Reasoning</div>
              <p>{d.reason}</p>
              {r && (<><div className="label">Review findings</div><p>{r.findings}</p></>)}
            </details>
          </div>
        )}
      </div>
    </article>
  );
}
