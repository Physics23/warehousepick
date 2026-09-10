export default function ActionButtons({ onAction }) {
  return (
    <footer className="kiosk-actions">
      <button className="btn success" onClick={() => onAction('picked')}>Picked</button>
      <button className="btn warning" onClick={() => onAction('unscannable')}>Unscannable</button>
      <button className="btn warning" onClick={() => onAction('missing')}>Missing</button>
      <button className="btn danger" onClick={() => onAction('problem_tote')}>Problem Tote</button>
    </footer>
  );
}