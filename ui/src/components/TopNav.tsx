const LINKS = [
  ['overview', 'Overview'],
  ['research', 'Research'],
  ['experiments', 'Experiments'],
  ['decisions', 'Decisions'],
  ['literature', 'Literature'],
  ['lab', 'Lab'],
  ['timeline', 'Timeline'],
] as const;

export function TopNav({ section, status }: { section: string; status: string }) {
  return (
    <header className="nav-bar">
      <a href="#/" className="brand">
        <span className="brand-name">FALSIFY</span>
        <span className="brand-tag">The lab that tries to prove itself wrong.</span>
      </a>
      <nav className="nav-links" aria-label="Main">
        {LINKS.map(([id, label]) => (
          <a key={id} href={`#/${id}`} className={section === id ? 'is-active' : ''} aria-current={section === id ? 'page' : undefined}>{label}</a>
        ))}
      </nav>
      <div className="nav-right">
        <span className="live-status"><span className="live-dot" aria-hidden />{status === 'RUNNING' ? 'Lab running' : 'Lab paused'}</span>
        <a href="#/join" className={`nav-join ${section === 'join' ? 'is-active' : ''}`}>Join the lab</a>
      </div>
    </header>
  );
}
