import { useState } from "react";
import "./styles.css";
import Header from "./Header";
import NavTabs from "./NavTabs";
import LiveView from "./pages/LiveView";

const TABS = ["Live View", "Gallery", "Timelapse", "Settings"];

export default function Home() {
  const [activeTab, setActiveTab] = useState("Live View");

  return (
    <div className="container">
      <Header online />
      <NavTabs tabs={TABS} active={activeTab} onChange={setActiveTab} />
      {activeTab === "Live View" ? (
        <LiveView onStartTimelapse={() => setActiveTab("Timelapse")} />
      ) : (
        // Replace with <Gallery />, <Timelapse />, <Settings /> as you build them
        <main className="main-content placeholder">{activeTab} page goes here</main>
      )}
    </div>
  );
}
