export function TopNav({ section, running }: { section: string; running: number }) {
  return (
    <header className="nav-bar">
      <a href="#/" className="brand">
        <span className="brand-name">FALSIFY</span>
        <span className="brand-tag">The lab that tries to prove itself wrong.</span>
      </a>
      <nav className="nav-links">
        <a href="#/" className={section === '' || section === 'p' ? 'is-active' : ''}>Programs</a>
        <a href="#/new" className={section === 'new' ? 'is-active' : ''}>New question</a>
      </nav>
      <div className="live-status">
        <span className="live-dot" />
        Live <span className="live-sub">· {running} programs active</span>
      </div>
    </header>
  );
}
