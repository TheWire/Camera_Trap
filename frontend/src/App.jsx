import { useState } from "react";
import "./styles.css";
import Header from "./components/Header";
import NavTabs from "./components/NavTabs";
import LiveView from "./pages/LiveView";
import ImageGallery from "./pages/ImageGallery";

export default function Home() {
  const [activeTab, setActiveTab] = useState("Live View");

  const pages = {
    "Live View": <LiveView onStartTimelapse={() => setActiveTab("Timelapse")} />,
    "Gallery": <ImageGallery />,
  };

  return (
    <div className="container">
      <Header online />
      <NavTabs tabs={Object.keys(pages)} active={activeTab} onChange={setActiveTab} />
      {}
      {pages[activeTab] ?? (
        <main className="main-content placeholder">{activeTab} page goes here</main>
      )}
    </div>
  );
}
