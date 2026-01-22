import { useState } from 'react';

export default function TimelapseTrigger() {
  const [intervalSeconds, setIntervalSeconds] = useState(10);
  const [durationMinutes, setDurationMinutes] = useState(60);
  const [isRequesting, setIsRequesting] = useState(false);
  const [message, setMessage] = useState('');

  const startTimelapse = async () => {
    if (intervalSeconds < 1 || durationMinutes < 1) {
      setMessage('Interval and duration must be at least 1');
      return;
    }

    setIsRequesting(true);
    setMessage('Starting timelapse...');

    try {
      const response = await fetch('/api/timelapse-on', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          interval: intervalSeconds,           // seconds
          duration: durationMinutes * 60,      // seconds
        }),
      });

      if (!response.ok) {
        const errorText = await response.text().catch(() => 'Unknown error');
        throw new Error(`Failed (${response.status}): ${errorText}`);
      }

      setMessage(`Request sent — interval ${intervalSeconds}s, duration ${durationMinutes} min`);
    } catch (err) {
      console.error(err);
      setMessage(`Error: ${err.message}`);
    } finally {
      setIsRequesting(false);
    }
  };

  const stopTimelapse = async () => {
    setIsRequesting(true);
    setMessage('Stopping timelapse...');

    try {
      const response = await fetch('/api/timelapse-off', {
        method: 'POST',           // or 'DELETE' — change if your API uses DELETE
        headers: {
          'Content-Type': 'application/json',
        },
        // body: JSON.stringify({})   // ← add if your endpoint expects something
      });

      if (!response.ok) {
        const errorText = await response.text().catch(() => '');
        throw new Error(`Failed (${response.status}): ${errorText}`);
      }

      setMessage('Stop request sent');
    } catch (err) {
      console.error(err);
      setMessage(`Error: ${err.message}`);
    } finally {
      setIsRequesting(false);
    }
  };

  return (
    <div style={{ maxWidth: 400, padding: '1.5rem', margin: '2rem auto' }}>
      <h2>Timelapse Control</h2>

      {message && (
        <div style={{
          marginBottom: '1.2rem',
          padding: '0.8rem',
          background: message.includes('Error') ? '#3d1f1f' : '#1f3d2a',
          borderRadius: '6px',
          color: message.includes('Error') ? '#ffcccc' : '#ccffcc'
        }}>
          {message}
        </div>
      )}

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1.2rem' }}>
        <label>
          Interval (seconds):
          <input
            type="number"
            min={1}
            max={600}
            value={intervalSeconds}
            onChange={e => setIntervalSeconds(Number(e.target.value))}
            disabled={isRequesting}
            style={{ marginLeft: '1rem', width: '90px' }}
          />
        </label>

        <label>
          Duration (minutes):
          <input
            type="number"
            min={1}
            max={1440}
            value={durationMinutes}
            onChange={e => setDurationMinutes(Number(e.target.value))}
            disabled={isRequesting}
            style={{ marginLeft: '1rem', width: '90px' }}
          />
        </label>

        <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
          <button
            onClick={startTimelapse}
            disabled={isRequesting}
            style={{
              padding: '10px 20px',
              background: '#2e7d32',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              cursor: isRequesting ? 'not-allowed' : 'pointer',
              opacity: isRequesting ? 0.6 : 1
            }}
          >
            Start Timelapse
          </button>

          <button
            onClick={stopTimelapse}
            disabled={isRequesting}
            style={{
              padding: '10px 20px',
              background: '#c62828',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              cursor: isRequesting ? 'not-allowed' : 'pointer',
              opacity: isRequesting ? 0.6 : 1
            }}
          >
            Stop Timelapse
          </button>
        </div>
      </div>
    </div>
  );
}
