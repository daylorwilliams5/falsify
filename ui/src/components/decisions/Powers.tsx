// The separation of powers, stated once at the top of the journal.
export function Powers() {
  return (
    <ol className="powers">
      <li><span className="pw-who">Human</span><span className="pw-what">Sets the mandate, budget and policy. Decides only Level 3 escalations.</span></li>
      <li><span className="pw-who">Principal Investigator</span><span className="pw-what">Makes every scientific decision within the mandate.</span></li>
      <li><span className="pw-who">Methodology reviewer</span><span className="pw-what">Audits every PI decision. Cannot choose the science; can block it.</span></li>
    </ol>
  );
}
