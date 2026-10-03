import { isLoading, useLabView, useProgram } from './data/useLab';
import { useRoute } from './router';
import { TopNav } from './components/TopNav';
import { LabOverview } from './LabOverview';
import { DecisionsPage } from './pages/DecisionsPage';
import { TimelinePage } from './pages/TimelinePage';
import { PublicPage } from './pages/PublicPage';
import { AgentsPage, ExperimentPage, HypothesesPage, LiteraturePage } from './pages/Pages';

// Routes:  #/              public one-page demo (no nav)
//          #/overview      lab overview
//          #/research | experiments[/<id>] | decisions[/<D###>] | literature | lab | timeline[/<D###>]
// Multi-program views (pages/Home, NewQuestion, ProgramPage) are kept but unrouted for now.
export default function App() {
  const lab = useLabView();
  const snapshot = useProgram('corrigibility');
  const [section = '', a] = useRoute();

  if (isLoading(lab) || isLoading(snapshot) || !snapshot) {
    return <div className="boot">Loading…</div>;
  }

  if (section === '') return <PublicPage lab={lab} />;

  const base = '#/';
  const page = (() => {
    switch (section) {
      case 'research': return <HypothesesPage lab={snapshot} base={base} />;
      case 'experiments': return <ExperimentPage lab={snapshot} base={base} id={a} />;
      case 'literature': return <LiteraturePage lab={snapshot} base={base} />;
      case 'lab': return <AgentsPage lab={snapshot} base={base} view={lab} />;
      case 'decisions': return <DecisionsPage key={a ?? ''} decisions={lab.decisions} focus={a} />;
      case 'timeline': return <TimelinePage key={a ?? ''} lab={lab} focus={a} />;
      default: return <LabOverview lab={lab} />; // #/overview
    }
  })();

  return (
    <div className="app">
      <TopNav section={section} status={lab.state.status} />
      <main className="main">{page}</main>
    </div>
  );
}
