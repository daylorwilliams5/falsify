import { useLab } from './data/useLab';
import { useRoute } from './router';
import { TopNav } from './components/TopNav';
import { Overview } from './Overview';
import { AgentsPage, DecisionPage, EvidencePage, ExperimentPage, HypothesesPage, LiteraturePage } from './pages/Pages';

export default function App() {
  const lab = useLab();
  const [section = '', id] = useRoute();

  if (!lab) return <div className="boot">Loading lab state…</div>;

  const page = (() => {
    switch (section) {
      case 'hypotheses': return <HypothesesPage lab={lab} />;
      case 'experiments': return <ExperimentPage lab={lab} id={id} />;
      case 'decision': return <DecisionPage lab={lab} />;
      case 'literature': return <LiteraturePage lab={lab} />;
      case 'agents': return <AgentsPage lab={lab} />;
      case 'evidence': return <EvidencePage lab={lab} />;
      default: return <Overview lab={lab} />;
    }
  })();

  return (
    <div className="app">
      <TopNav section={section === 'decision' ? '' : section} loop={lab.state.loop_index} />
      <main className="main">{page}</main>
    </div>
  );
}
