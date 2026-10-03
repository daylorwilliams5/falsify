// Breadcrumb shown on program pages.
export function ProgramBar({ id, title }: { id: string; title: string }) {
  return (
    <div className="pbar">
      <div className="pbar-crumb">
        <a href="#/programs">Programs</a>
        <span>/</span>
        <a href={`#/p/${id}`} className="pbar-title">{title}</a>
      </div>
    </div>
  );
}
