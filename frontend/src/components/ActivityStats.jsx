function Stat({ value, label }) {
  return (
    <div className="stat-card">
      <div className="stat-value">{value}</div>
      <div className="stat-label">{label}</div>
    </div>
  );
}

export default function ActivityStats({ photos, videos, storage, battery }) {
  return (
    <div className="panel-section">
      <h3>Today's Activity</h3>
      <div className="stats-grid">
        <Stat value={photos} label="Photos" />
        <Stat value={videos} label="Videos" />
        <Stat value={storage} label="Storage" />
        <Stat value={`${battery}%`} label="Battery" />
      </div>
    </div>
  );
}
