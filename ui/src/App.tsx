import type { ReactNode } from 'react';
import { isLoading, useLabView, usePrograms, useProgram } from './data/useLab';
import { useRoute } from './router';
import { TopNav } from './components/TopNav';
import { LabOverview } from './LabOverview';
import { DetailPage } from './pages/DetailPage';
import { Home } from './pages/Home';
import { NewQuestion } from './pages/NewQuestion';
import { ProgramPage } from './pages/ProgramPage';
import { AgentsPage, ExperimentPage, HypothesesPage, LiteraturePage } from './pages/Pages';

// Routes:  #/              lab overview
//          #/research | experiments[/<id>] | decisions | literature | lab | timeline
//          #/programs, #/new[/<q>], #/p/<id>   multi-program views
export default function App() {
  const lab = useLabView();
  const programs = usePrograms();
  const snapshot = useProgram('corrigibility');
  const [section = '', a] = useRoute();

  if (isLoading(lab) || isLoading(programs) || isLoading(snapshot) || !snapshot) {
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
      case 'lab': return <AgentsPage lab={snapshot} base={base} />;
      case 'decisions': return soon('Decisions', 'Decision history', 'Every PI decision with its level, reasoning, rejected alternatives and methodology review. Not built yet.');
      case 'timeline': return soon('Timeline', 'Lab timeline', 'The full timeline.jsonl record of human, PI, specialist and runner events. Not built yet.');
      case 'programs': return <Home programs={programs} />;
      case 'new': return <NewQuestion key={a ?? ''} initial={a ? decodeURIComponent(a) : undefined} />;
      case 'p': {
        const program = programs.find((p) => p.id === a);
        if (program) return <ProgramPage key={program.id} program={program} />;
        return <LabOverview lab={lab} />;
      }
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
