import { useState } from "react";
import "./styles.css";
import Header from "./component/Header";
import NavTabs from "./component/NavTabs";
import LiveView from "./pages/LiveView";
import ImageGallery from "./pages/ImageGallery";

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
        <ImageGallery />,
        <main className="main-content placeholder">{activeTab} page goes here</main>
      )}
    </div>
  );
}
