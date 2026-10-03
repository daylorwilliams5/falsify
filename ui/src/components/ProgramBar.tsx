const TABS = [
  ['', 'Overview'],
  ['hypotheses', 'Hypotheses'],
  ['experiments', 'Experiments'],
  ['literature', 'Literature'],
  ['agents', 'Agents'],
  ['evidence', 'Evidence'],
] as const;

// Breadcrumb + section tabs shown on every page inside a program.
export function ProgramBar({ id, title, tab, tabs = true }: { id: string; title: string; tab: string; tabs?: boolean }) {
  return (
    <div className="pbar">
      <div className="pbar-crumb">
        <a href="#/">Programs</a>
        <span>/</span>
        <a href={`#/p/${id}`} className="pbar-title">{title}</a>
      </div>
      {tabs && (
        <nav className="pbar-tabs">
          {TABS.map(([t, label]) => (
            <a key={t} href={`#/p/${id}${t ? '/' + t : ''}`} className={tab === t ? 'is-active' : ''}>{label}</a>
          ))}
        </nav>
      )}
    </div>
  );
}
