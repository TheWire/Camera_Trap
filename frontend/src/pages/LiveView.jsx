import { useEffect, useState } from "react";
import CameraView from "../components/CameraView";
import CameraControls from "../components/CameraControls";
import QuickSettings from "../components/QuickSettings";
import ActivityStats from "../components/ActivityStats";

export default function LiveView({ onStartTimelapse }) {
  const [recording, setRecording] = useState(false);
  const [lightOn, setLightOn] = useState(false);
  const [settings, setSettings] = useState({
    brightness: 75,
    exposure: 0,
    resolution: "1920×1080",
    frameRate: "30 FPS",
  });

  const [capturing, setCapturing] = useState(false);
  const [notice, setNotice] = useState(null); // { type: "success" | "error", text }

  // Clear the status message after a few seconds
  useEffect(() => {
    if (!notice) return;
    const id = setTimeout(() => setNotice(null), 3000);
    return () => clearTimeout(id);
  }, [notice]);

  const handleQuickCapture = async () => {
    if (capturing) return;
    setCapturing(true);
    try {
      const res = await fetch("/api/quick-capture", { method: "POST" });
      if (!res.ok) throw new Error(`Request failed (${res.status})`);
      setNotice({ type: "success", text: "Photo captured" });
    } catch (err) {
      setNotice({ type: "error", text: "Capture failed. Check the camera connection and try again." });
    } finally {
      setCapturing(false);
    }
  };

  const updateSetting = (key, value) =>
    setSettings((prev) => ({ ...prev, [key]: value }));

  return (
    <main className="main-content">
      <section className="camera-view">
        <CameraView
          recording={recording}
          info={`${settings.resolution} • ${settings.frameRate}`}
        />
        {notice && (
          <div className={`toast ${notice.type}`} role="status">
            {notice.text}
          </div>
        )}
        <CameraControls
          recording={recording}
          lightOn={lightOn}
          onToggleRecording={() => setRecording((r) => !r)}
          onToggleLight={() => setLightOn((l) => !l)}
          capturing={capturing}
          onTakePhoto={handleQuickCapture}
          onDownload={() => console.log("download")}
        />
      </section>

      <aside className="side-panel">
        <QuickSettings settings={settings} onChange={updateSetting} />
        <ActivityStats photos={247} videos={18} storage="3.2 GB" battery={82} />
        <div className="panel-section">
          <h3>Quick Actions</h3>
          <button className="action-btn primary" onClick={onStartTimelapse}>
            🎬 Start Timelapse
          </button>
        </div>
      </aside>
    </main>
  );
}
