const LINKS = [
  ['', 'Overview'],
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
      <nav className="nav-links">
        {LINKS.map(([id, label]) => (
          <a key={id} href={`#/${id}`} className={section === id ? 'is-active' : ''}>{label}</a>
        ))}
      </nav>
      <div className="live-status">
        <span className="live-dot" />
        {status === 'RUNNING' ? 'Lab running' : 'Lab paused'}
      </div>
    </header>
  );
}
