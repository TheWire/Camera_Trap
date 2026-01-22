import os
from flask import Flask, Response, request, render_template, jsonify, send_from_directory
#from picamera2 import Picamera2
from gpiozero import MotionSensor, LightSensor, PWMLED, OutputDevice, InputDevice
import time
import threading
from threading import Thread
#import cv2
#from ultralytics import YOLO
from camera import Camera

app = Flask(__name__)

#picam2 = Picamera2()
#camera_config = picam2.create_video_configuration(main={"size": (640, 480), "format": "RGB888"})  # Adjust resolution as needed

#picam2.configure(camera_config)
#picam2.start()

#model = YOLO("yolo11n.pt")
#names = model.names
#threshold = .40
camera = Camera()
led = PWMLED(18)
ldr = LightSensor(27)

timelapse_thread = None

#def generate_frames():
#    """Generator function to capture and yield JPEG frames for MJPEG streaming."""
#    while True:
#        # Capture a frame as JPEG
#        frame = picam2.capture_array()
#        results = model(frame)
#        annotated = results[0].plot()
#        boxes = results[0].boxes.xyxy.cpu().tolist()
#        clss = results[0].boxes.cls.cpu().tolist()
#        confs = results[0].boxes.conf.cpu().tolist()
#        if boxes is not None:
#            # if set(clss) == previous_classes:
#            #     print("Scene is unchanged, not saving images.")
#            #     return set(clss)
#
#            for box, cls, conf in zip(boxes, clss, confs):
#                if conf < threshold: # Is confidence under threshold?
#                    continue
#                cv2.rectangle(frame,
#                              (int(box[0]), int(box[1])),
#                              (int(box[2]), int(box[3])),
#                              (0, 255, 0), 1)
#                font = cv2.FONT_HERSHEY_SIMPLEX
#                text = f"{names[int(cls)]} {conf*100:10.2f}%"
#                cv2.putText(frame,text,(int(box[0])+5,int(box[1])+18), font, 0.6,(0, 255, 0),1,cv2.LINE_AA)
#
#        # Convert to JPEG format
#        _, buffer = cv2.imencode('.jpg', frame)
#        frame = buffer.tobytes()
#        # Yield the frame in MJPEG format
#        yield (b'--frame\r\n'
#               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#        time.sleep(0.1)  # Control frame rate (adjust as needed)

def light_on():
    if ldr.value == 0:
        led.on()

def light_off():
    led.off()

class Timelapse_Thread(Thread):
    def __init__(self, interval, duration):
        super().__init__()
        self._stop_event = threading.Event()

        self.interval = interval
        self.duration = duration

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        if self.duration < 0:
            end_time = float('inf')
        else:
            end_time = time.time() + self.duration

        while not self._stop_event.is_set() and time.time() < end_time:
            light_on()
            camera.capture(f"./images/{time.time()}.jpg")
            light_off()
            time.sleep(self.interval)

        print("timelapse end")

@app.route('/api/video')
def video():
    """Stream the video feed as MJPEG."""
    camera.start_stream()
    response = Response(camera.generate_http_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=FRAME')

    @response.call_on_close
    def on_close():
        camera.stop_stream()

    return response

@app.route('/api/timelapse-on', methods=["POST"])
def timelapse():
    global timelapse_thread
    content = request.get_json()
    print(content)
    interval = content["interval"] #request.args.get('interval', default=30, type=int)
    duration = content["duration"] #request.args.get('duration', default=15*60, type=int)
    if timelapse_thread is not None:
        return jsonify(success=False, message="timelapse already running", status=400, mimetype='application/json')
    timelapse_thread = Timelapse_Thread(interval, duration)
    timelapse_thread.start()
    response = jsonify(success=True)
    return response

@app.route('/api/timelapse-off', methods=["POST"])
def timelapse_off():
    global timelapse_thread
    if timelapse_thread is None:
        return jsonify(success=False, message="timelapse not running", status=400, mimetype='application/json')
    if timelapse_thread.stopped():       
        return jsonify(success=False, message="timelapse not running", status=400, mimetype='application/json')
    timelapse_thread.stop()
    timelapse_thread = None
    response = jsonify(success=True)
    return response

@app.route('/api/images/<path:filename>')
def serve_images(filename):
    return send_from_directory('images', filename)

@app.route('/api/images')
def serve_available_images():
    files = [f for f in os.listdir("./images") if os.path.isfile(os.path.join("./images", f))]
    images = [i for i in files if os.path.splitext(i)[1][1:] == "jpg"]
    return jsonify(images=images)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_static(path): 
    # Otherwise → SPA fallback: serve index.html so React Router can handle it
    return send_from_directory("./templates", 'index.html')

#@app.route('/')
#def serve_react():
    #return render_template('index.html')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
