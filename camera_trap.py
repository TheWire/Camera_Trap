import os
import numbers
from flask import Flask, Response, request, render_template, jsonify, send_from_directory
from gpiozero import MotionSensor, LightSensor, PWMLED, OutputDevice, InputDevice
import time
import threading
from threading import Thread
from camera import Camera

app = Flask(__name__)


camera = Camera()
led = PWMLED(18)
motion_sensor = MotionSensor(23)
timelapse_thread = None

def LDR_value(pin, charge_time_limit=0.005):
    
    # Take the pin LOW to discharge the capacitor
    ldr = OutputDevice(pin=pin, active_high=True, 
                       initial_value=False)
    time.sleep(0.1)

    # Configure the pin as an input
    ldr.close()
    ldr = InputDevice(pin=pin, pull_up=None,
                      active_state=True)

    # Wait for the capacitor to recharge, but only up to
    # the charge time limit
    lit = 0
    start = time.time()
    while True:
        if time.time() - start >  charge_time_limit:
            break
        if ldr.is_active:
            lit += 1

    ldr.close()
    return lit

def light_on():
    ldr_value = LDR_value(22, 0.01)
    print(ldr_value)
    if ldr_value < 5:
        print("light on")
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
            is_motion = motion_sensor.motion_detected
            if is_motion:
                print("motion")
            print("capturing")
            camera.capture(f"./images/{time.time()}{'_M' if is_motion else ''}.jpg")
            print("captured")
            light_off()
            time.sleep(self.interval)


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

@app.route('/api/light', methods=["post"])
def light():
    content = request.get_json()
    level = content["level"]
    if level is None \
        or not isinstance(level, numbers.Number) \
        or level < 0 \
        or level > 100:
            return jsonify(success=False, message="invalid light value", status=400, mimtype="application/json")
    led.value = level / 100
    return jsonify(success=True)

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
    return jsonify(success=True)

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
