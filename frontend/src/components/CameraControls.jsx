function ControlButton({ label, icon, variant = "secondary", active, disabled, onClick }) {
  return (
    <button
      className={`control-btn ${variant}${active ? " active" : ""}`}
      title={label}
      aria-label={label}
      aria-pressed={active}
      disabled={disabled}
      onClick={onClick}
    >
      {icon}
    </button>
  );
}

export default function CameraControls({
  recording,
  lightOn,
  capturing,
  onToggleRecording,
  onToggleLight,
  onTakePhoto,
  onDownload,
}) {
  return (
    <div className="camera-controls">
      <ControlButton label="Toggle light" icon="💡" active={lightOn} onClick={onToggleLight} />
      <ControlButton
        label={capturing ? "Capturing…" : "Take photo"}
        icon={capturing ? "⏳" : "📸"}
        disabled={capturing}
        onClick={onTakePhoto}
      />
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
