export default function Header({ online = true }) {
  return (
    <header className="header">
      <h1>
        <span className="camera-icon" aria-hidden="true">📷</span>
        Camera Trap
      </h1>
      <div className="status-indicator">
        <span className="status-dot" style={{ background: online ? "#10b981" : "#ef4444" }} />
        <span>{online ? "Online" : "Offline"}</span>
      </div>
    </header>
  );
}
