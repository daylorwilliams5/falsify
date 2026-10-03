import type { EvidenceItem as EI } from '../data/types';

const GLYPH = { MEASURED: '■', DERIVED: '◆', INFERRED: '◇', HYPOTHESIS: '○' };
const GLOSS = {
  MEASURED: 'raw experiment result',
  DERIVED: 'computed statistic',
  INFERRED: 'agent interpretation',
  HYPOTHESIS: 'untested claim',
};

export function EvidenceItem({ e }: { e: EI }) {
  return (
    <div className={`ev-item prov-${e.kind.toLowerCase()}`}>
      <div className="ev-kind mono">
        <span className="ev-glyph">{GLYPH[e.kind]}</span>
        {e.kind}
        <span className="ev-gloss">{GLOSS[e.kind]}</span>
      </div>
      <div className="ev-text">{e.text}</div>
      <div className="ev-src mono">
        {e.hypothesis && <span className="chip">{e.hypothesis}</span>}
        {e.source}
      </div>
    </div>
  );
}
