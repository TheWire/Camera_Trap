import { useEffect, useState } from "react";

const pad = (n) => String(n).padStart(2, "0");
const formatTime = (s) => `${pad(Math.floor(s / 3600))}:${pad(Math.floor(s / 60) % 60)}:${pad(s % 60)}`;

export default function CameraView({ recording, info, streamUrl }) {
  const [seconds, setSeconds] = useState(0);

  useEffect(() => {
    if (!recording) return setSeconds(0);
    const id = setInterval(() => setSeconds((s) => s + 1), 1000);
    return () => clearInterval(id);
  }, [recording]);

  return (
    <div className="video-container">
      {streamUrl ? (
        <img className="video-feed" src={streamUrl} alt="Live camera feed" />
      ) : (
        <div className="video-placeholder" aria-label="Camera feed placeholder">📹</div>
      )}
      <div className="video-overlay">
        {recording ? (
          <div className="recording-indicator">
            <span className="rec-dot" />
            REC {formatTime(seconds)}
          </div>
        ) : (
          <span />
        )}
        <div className="camera-info">{info}</div>
      </div>
    </div>
  );
}
