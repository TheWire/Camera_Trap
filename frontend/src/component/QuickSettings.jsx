function SliderSetting({ label, value, display, min, max, step = 1, onChange }) {
  return (
    <div className="slider-container">
      <div className="slider-header">
        <label className="setting-label">{label}</label>
        <span className="setting-value">{display}</span>
      </div>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
      />
    </div>
  );
}

function SelectSetting({ label, value, options, onChange }) {
  return (
    <div className="setting-item">
      <label className="setting-label">{label}</label>
      <select value={value} onChange={(e) => onChange(e.target.value)}>
        {options.map((o) => (
          <option key={o}>{o}</option>
        ))}
      </select>
    </div>
  );
}

export default function QuickSettings({ settings, onChange }) {
  return (
    <div className="panel-section">
      <h3>Quick Settings</h3>
      <SliderSetting
        label="Brightness"
        value={settings.brightness}
        display={`${settings.brightness}%`}
        min={0}
        max={100}
        onChange={(v) => onChange("brightness", v)}
      />
      <SelectSetting
        label="Resolution"
        value={settings.resolution}
        options={["1280×720", "1920×1080", "3840×2160"]}
        onChange={(v) => onChange("resolution", v)}
      />
      <SelectSetting
        label="Frame rate"
        value={settings.frameRate}
        options={["24 FPS", "30 FPS", "60 FPS"]}
        onChange={(v) => onChange("frameRate", v)}
      />
      <SliderSetting
        label="Exposure"
        value={settings.exposure}
        display={`${settings.exposure} EV`}
        min={-3}
        max={3}
        step={0.5}
        onChange={(v) => onChange("exposure", v)}
      />
    </div>
  );
}
