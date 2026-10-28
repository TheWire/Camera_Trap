import { useState } from "react";
import CameraView from "../component/CameraView";
import CameraControls from "../component/CameraControls";
import QuickSettings from "../component/QuickSettings";
import ActivityStats from "../component/ActivityStats";

export default function LiveView({ onStartTimelapse }) {
  const [recording, setRecording] = useState(false);
  const [lightOn, setLightOn] = useState(false);
  const [settings, setSettings] = useState({
    brightness: 75,
    exposure: 0,
    resolution: "1920×1080",
    frameRate: "30 FPS",
  });

  const updateSetting = (key, value) =>
    setSettings((prev) => ({ ...prev, [key]: value }));

  return (
    <main className="main-content">
      <section className="camera-view">
        <CameraView
          recording={recording}
          info={`${settings.resolution} • ${settings.frameRate}`}
          streamUrl={'/api/video'}
        />
        <CameraControls
          recording={recording}
          lightOn={lightOn}
          onToggleRecording={() => setRecording((r) => !r)}
          onToggleLight={() => setLightOn((l) => !l)}
          onTakePhoto={() => console.log("photo")}
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
