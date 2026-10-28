function ControlButton({ label, icon, variant = "secondary", active, onClick }) {
  return (
    <button
      className={`control-btn ${variant}${active ? " active" : ""}`}
      title={label}
      aria-label={label}
      aria-pressed={active}
      onClick={onClick}
    >
      {icon}
    </button>
  );
}

export default function CameraControls({
  recording,
  lightOn,
  onToggleRecording,
  onToggleLight,
  onTakePhoto,
  onDownload,
}) {
  return (
    <div className="camera-controls">
      <ControlButton label="Toggle light" icon="💡" active={lightOn} onClick={onToggleLight} />
      <ControlButton label="Take photo" icon="📸" onClick={onTakePhoto} />
      <ControlButton
        label={recording ? "Stop recording" : "Record video"}
        icon={recording ? "⏹" : "⏺"}
        variant="primary"
        onClick={onToggleRecording}
      />
      <ControlButton label="Download latest" icon="💾" onClick={onDownload} />
    </div>
  );
}
