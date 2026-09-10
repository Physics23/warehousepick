// Helper: Format seconds into "MM:SS" or "H:MM:SS"
const formatTime = (totalSeconds) => {
  if (totalSeconds < 60) return `${totalSeconds.toFixed(0)}s`;
  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = Math.floor(totalSeconds % 60);
  if (hours > 0) return `${hours}h ${minutes}m`;
  return `${minutes}m ${seconds}s`;
};

// Helper: Format cycle time as "X.Xs" or "Xm Ys"
const formatCycleTime = (seconds) => {
  if (seconds < 60) return `${seconds.toFixed(2)}s`;
  const minutes = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${minutes}m ${secs}s`;
};

export default function Header({ stationId, operatorName, stats }) {
  return (
    <header className="kiosk-header">
      <div className="station-info">
        <h1>{stationId}</h1>
        <p>Abdoulaye: {operatorName || 'Unknown'}</p>
      </div>
      <div className="stats-grid">
        <div className="stat-box">
          <span className="stat-label">Rate/UPH</span>
          <span className="stat-value">{Math.round(stats?.rate_uph ?? 0)}</span>
        </div>
        <div className="stat-box">
          <span className="stat-label">Cycle Time</span>
          <span className="stat-value">{formatCycleTime(stats?.cycle_time_secs ?? 0)}</span>
        </div>
        <div className="stat-box">
          <span className="stat-label">Session</span>
          <span className="stat-value">{formatTime(stats?.session_time_secs ?? 0)}</span>
        </div>
        <div className="stat-box">
          <span className="stat-label">Total Units</span>
          <span className="stat-value">{stats?.total_units_picked ?? 0}</span>
        </div>
      </div>
    </header>
  );
}