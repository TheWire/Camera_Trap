export default function NavTabs({ tabs, active, onChange }) {
  return (
    <nav className="nav" aria-label="Main">
      {tabs.map((tab) => (
        <button
          key={tab}
          className={`nav-item${tab === active ? " active" : ""}`}
          aria-current={tab === active ? "page" : undefined}
          onClick={() => onChange(tab)}
        >
          {tab}
        </button>
      ))}
    </nav>
  );
}
