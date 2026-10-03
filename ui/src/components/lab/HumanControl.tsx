import { useState } from 'react';
import type { Escalation } from '../../data/types';

/** Shown only for a real Level 3 escalation. */
export function EscalationCard({ e }: { e: Escalation }) {
  const [note, setNote] = useState<string | null>(null);
  return (
    <section className="escalation">
      <div className="esc-kind"><span className="audit-dot" />Human decision required <span className="id">{e.decision} · Level 3</span></div>
      <p className="esc-title">{e.title}</p>
      <p className="esc-why"><span>Why</span>{e.why}. {e.detail}</p>
      <div className="esc-actions">
        <button className="cta" onClick={() => setNote('Not wired yet.')}>Approve</button>
        <button className="btn-quiet" onClick={() => setNote('Not wired yet.')}>Reject</button>
        {note && <span className="esc-note">{note}</span>}
      </div>
    </section>
  );
}

/** Small persistent override control. Deliberately quiet. */
export function OverrideControl() {
  const [open, setOpen] = useState(false);
  return (
    <div className={`override ${open ? 'is-open' : ''}`}>
      {open && (
        <div className="override-menu">
          <p>Overrides are recorded in the timeline and audited.</p>
          <button disabled>Pause the lab</button>
          <button disabled>Revert latest PI decision</button>
          <button disabled>Edit mandate</button>
          <span>Not wired yet</span>
        </div>
      )}
      <button className="override-btn" onClick={() => setOpen((o) => !o)}>Human override</button>
    </div>
  );
}
