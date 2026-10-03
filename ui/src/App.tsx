import type { ReactNode } from 'react';
import { isLoading, useLabView, useProgram } from './data/useLab';
import { useRoute } from './router';
import { TopNav } from './components/TopNav';
import { LabOverview } from './LabOverview';
import { DetailPage } from './pages/DetailPage';
import { DecisionsPage } from './pages/DecisionsPage';
import { AgentsPage, ExperimentPage, HypothesesPage, LiteraturePage } from './pages/Pages';

// Routes:  #/              lab overview
//          #/research | experiments[/<id>] | decisions[/<D###>] | literature | lab | timeline
// Multi-program views (pages/Home, NewQuestion, ProgramPage) are kept but unrouted for now.
export default function App() {
  const lab = useLabView();
  const snapshot = useProgram('corrigibility');
  const [section = '', a] = useRoute();

  if (isLoading(lab) || isLoading(snapshot) || !snapshot) {
    return <div className="boot">Loading…</div>;
  }

  const base = '#/';
  const soon = (kicker: string, title: string, lede: string): ReactNode => (
    <DetailPage base={base} kicker={kicker} title={title} lede={lede}><span /></DetailPage>
  );

  const page = (() => {
    switch (section) {
      case 'research': return <HypothesesPage lab={snapshot} base={base} />;
      case 'experiments': return <ExperimentPage lab={snapshot} base={base} id={a} />;
      case 'literature': return <LiteraturePage lab={snapshot} base={base} />;
      case 'lab': return <AgentsPage lab={snapshot} base={base} view={lab} />;
      case 'decisions': return <DecisionsPage key={a ?? ''} decisions={lab.decisions} focus={a} />;
      case 'timeline': return soon('Timeline', 'Lab timeline', 'The full timeline.jsonl record of human, PI, specialist and runner events. Not built yet.');
      default: return <LabOverview lab={lab} />;
    }
  })();

  return (
    <div className="app">
      <TopNav section={section} status={lab.state.status} />
      <main className="main">{page}</main>
    </div>
  );
}
