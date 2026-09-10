export default function ProblemOverlay({ task, onResume }) {
  if (!task) return null;

  return (
    <div className="problem-overlay">
      <div className="problem-modal">
        <h2>⚠️ Item Flagged: {task.item.name}</h2>
        <p>This item was marked as <strong>{task.status}</strong>.</p>
        <p>Please resolve the issue, then click the button below to return to the picking queue.</p>
        <button className="btn-resume" onClick={onResume}>✅ Resume Picking</button>
      </div>
    </div>
  );
}