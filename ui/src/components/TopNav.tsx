const LINKS = [
  ['', 'Overview'],
  ['hypotheses', 'Hypotheses'],
  ['experiments', 'Experiments'],
  ['literature', 'Literature'],
  ['agents', 'Agents'],
  ['evidence', 'Evidence'],
] as const;

export function TopNav({ section, loop }: { section: string; loop: number }) {
  return (
    <header className="nav-bar">
      <a href="#/" className="brand">
        <span className="brand-name">FALSIFY</span>
        <span className="brand-tag">The lab that tries to prove itself wrong.</span>
      </a>
      <nav className="nav-links">
        {LINKS.map(([id, label]) => (
          <a key={id} href={`#/${id}`} className={section === id ? 'is-active' : ''}>{label}</a>
        ))}
      </nav>
      <div className="live-status">
        <span className="live-dot" />
        Live <span className="live-sub">· loop {loop}</span>
      </div>
    </header>
  );
}
