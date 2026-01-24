import { useState } from 'react';

export default function LightControl() {
  const [level, setLevel] = useState(50);           // default middle value
  const [sending, setSending] = useState(false);
  const [status, setStatus] = useState('');

  const sendLevel = async (newLevel) => {
    const clamped = Math.max(0, Math.min(100, Math.round(newLevel)));

    setSending(true);
    setStatus(`Sending level ${clamped}...`);

    try {
      const response = await fetch('/api/light', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ level: clamped }),
      });

      if (!response.ok) {
        const errorText = await response.text().catch(() => '');
        throw new Error(`HTTP ${response.status}${errorText ? `: ${errorText}` : ''}`);
      }

      setLevel(clamped);
      setStatus(`Level set to ${clamped}`);
    } catch (err) {
      console.error(err);
      setStatus(`Error: ${err.message}`);
    } finally {
      setSending(false);
    }
  };

  const handleSliderChange = (e) => {
    setLevel(Number(e.target.value));
  };

  const handleNumberChange = (e) => {
    const val = e.target.value === '' ? '' : Number(e.target.value);
    setLevel(val);
  };

  const handleNumberBlur = () => {
    if (typeof level === 'number') {
      sendLevel(level);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      e.target.blur(); // triggers handleNumberBlur
    }
  };

  return (
    <div style={{
      maxWidth: 380,
      padding: '1.5rem',
      margin: '2rem auto',
      border: '1px solid #444',
      borderRadius: '12px',
      background: '#1a1a1a',
      color: '#eee',
    }}>
      <h2>Light Control</h2>

      {status && (
        <div style={{
          margin: '1rem 0',
          padding: '0.8rem',
          borderRadius: '6px',
          background: status.includes('Error') ? '#3d1f1f' : '#1f3d2a',
          color: status.includes('Error') ? '#ffcccc' : '#ccffcc',
        }}>
          {status}
        </div>
      )}

      <div style={{ margin: '1.5rem 0' }}>
        <input
          type="range"
          min={0}
          max={100}
          step={1}
          value={level}
          onChange={handleSliderChange}
          onPointerUp={() => sendLevel(level)}   // send when user releases slider
          disabled={sending}
          style={{ width: '100%', marginBottom: '1rem' }}
        />

        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1.5rem' }}>
          <span>0</span>
          <span>100</span>
        </div>

        <label style={{ display: 'block', marginBottom: '1.5rem' }}>
          Level:
          <input
            type="number"
            min={0}
            max={100}
            value={level}
            onChange={handleNumberChange}
            onBlur={handleNumberBlur}
            onKeyDown={handleKeyDown}
            disabled={sending}
            style={{
              width: '80px',
              marginLeft: '0.8rem',
              padding: '0.5rem',
              fontSize: '1.1rem',
            }}
          />
        </label>
      </div>

      <div style={{ display: 'flex', gap: '1rem' }}>
        <button
          onClick={() => sendLevel(100)}
          disabled={sending || level === 100}
          style={{
            flex: 1,
            padding: '14px',
            fontSize: '1.1rem',
            fontWeight: 'bold',
            background: '#2e7d32',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            cursor: sending ? 'not-allowed' : 'pointer',
            opacity: sending || level === 100 ? 0.6 : 1,
          }}
        >
          ON
        </button>

        <button
          onClick={() => sendLevel(0)}
          disabled={sending || level === 0}
          style={{
            flex: 1,
            padding: '14px',
            fontSize: '1.1rem',
            fontWeight: 'bold',
            background: '#c62828',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            cursor: sending ? 'not-allowed' : 'pointer',
            opacity: sending || level === 0 ? 0.6 : 1,
          }}
        >
          OFF
        </button>
      </div>
    </div>
  );
}
