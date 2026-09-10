export default function ComparisonPanel({ task }) {
  if (!task) return null;

  return (
    <div className="comparison-panel">
      <div className="comparison-box">
        <span className="label">Source Tote</span>
        <div className="tote-placeholder">{task.source_tote.tote_id}</div>
      </div>
      <div className="arrow">→</div>
      <div className="comparison-box">
        <span className="label">Destination Tote</span>
        <div className="tote-placeholder">{task.destination_tote.tote_id}</div>
      </div>
    </div>
  );
}