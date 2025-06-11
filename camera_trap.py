from flask import Flask, Response, render_template
from picamera2 import Picamera2
import time
import cv2
from ultralytics import YOLO

app = Flask(__name__)

picam2 = Picamera2()
camera_config = picam2.create_video_configuration(main={"size": (640, 480), "format": "RGB888"})  # Adjust resolution as needed
picam2.configure(camera_config)
picam2.start()

model = YOLO("yolo11n.pt")
names = model.names
threshold = .40

def generate_frames():
    """Generator function to capture and yield JPEG frames for MJPEG streaming."""
    while True:
        # Capture a frame as JPEG
        frame = picam2.capture_array()
        results = model(frame)
        annotated = results[0].plot()
        boxes = results[0].boxes.xyxy.cpu().tolist()
        clss = results[0].boxes.cls.cpu().tolist()
        confs = results[0].boxes.conf.cpu().tolist()
        if boxes is not None:
            # if set(clss) == previous_classes:
            #     print("Scene is unchanged, not saving images.")
            #     return set(clss)

            for box, cls, conf in zip(boxes, clss, confs):
                if conf < threshold: # Is confidence under threshold?
                    continue
                cv2.rectangle(frame,
                              (int(box[0]), int(box[1])),
                              (int(box[2]), int(box[3])),
                              (0, 255, 0), 1)
                font = cv2.FONT_HERSHEY_SIMPLEX
                text = f"{names[int(cls)]} {conf*100:10.2f}%"
                cv2.putText(frame,text,(int(box[0])+5,int(box[1])+18), font, 0.6,(0, 255, 0),1,cv2.LINE_AA)

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
    app.run(host='0.0.0.0', port=5000, threaded=True)