import { isLoading, usePrograms } from './data/useLab';
import { useRoute } from './router';
import { TopNav } from './components/TopNav';
import { Home } from './pages/Home';
import { NewQuestion } from './pages/NewQuestion';
import { ProgramPage } from './pages/ProgramPage';

// Routes:  #/                       programs home
//          #/new[/<question>]       ask a new question → mocked plan
//          #/p/<program>[/<tab>[/<id>]]  program overview and detail pages
export default function App() {
  const programs = usePrograms();
  const [section = '', a, b, c] = useRoute();

  if (isLoading(programs)) return <div className="boot">Loading…</div>;

  const page = (() => {
    if (section === 'new') return <NewQuestion key={a ?? ''} initial={a ? decodeURIComponent(a) : undefined} />;
    if (section === 'p') {
      const program = programs.find((p) => p.id === a);
      if (program) return <ProgramPage key={program.id} program={program} tab={b ?? ''} sub={c} />;
    }
    return <Home programs={programs} />;
  })();

  return (
    <div className="app">
      <TopNav section={section} running={programs.length} />
      <main className="main">{page}</main>
    </div>
  );
}
