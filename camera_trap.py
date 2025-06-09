from flask import Flask, Response, render_template
from picamera2 import Picamera2
import time
import cv2

app = Flask(__name__)

picam2 = Picamera2()
camera_config = picam2.create_video_configuration(main={"size": (640, 480)})  # Adjust resolution as needed
picam2.configure(camera_config)
picam2.start()

def generate_frames():
    """Generator function to capture and yield JPEG frames for MJPEG streaming."""
    while True:
        # Capture a frame as JPEG
        frame = picam2.capture_array()
        # Convert to JPEG format
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        # Yield the frame in MJPEG format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.1)  # Control frame rate (adjust as needed)

@app.route('/video')
def video():
    """Stream the video feed as MJPEG."""
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def serve_react():
    return render_template('index.html')

@app.route('/api/<endpoint>')
def api(endpoint):
    # Handle API requests
    return {"message": f"API endpoint: {endpoint}"}

if __name__ == '__main__':
    app.run(debug=True)