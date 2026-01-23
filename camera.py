import io
from threading import Lock
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
import libcamera
from threading import Lock
from threading import Condition

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self,buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

class Camera():
    def __init__(self):
        self.camera_init()
   
    def camera_init(self):
        self.camera_lock = Lock()
        self.camera_rotation = 0
        self.streaming_count = 0
        self.camera = Picamera2()
        self.camera_config = self.camera.create_video_configuration(main={"size": (4608, 2596)}, lores={"size": (1920, 1080)})
        self.camera_config["transform"] = libcamera.Transform(hflip=1, vflip=0)
        self.camera.configure(self.camera_config)
        self.output = StreamingOutput()
        self.camera.set_controls({"AfMode": libcamera.controls.AfModeEnum.Continuous, "AfSpeed": libcamera.controls.AfSpeedEnum.Fast})

    def close(self):
        if self.streaming_count > 0.0: 
            self.camera.stop_recording()
    
    def start_stream(self):
        if self.streaming_count == 0:
            self.start_recording()
        self.streaming_count += 1

    def stop_stream(self):
        if self.streaming_count == 0:
            return
        
        self.streaming_count -= 1
        if self.streaming_count == 0:
            self.stop_recording()

    def start_recording(self):
        with self.camera_lock:
            self.camera.start_recording(JpegEncoder(), FileOutput(self.output), name="lores")

    def stop_recording(self):
        with self.camera_lock:
            self.camera.stop_recording()

    def capture(self, path):
        with self.camera_lock:
            self.camera.set_controls({"AfMode": libcamera.controls.AfModeEnum.Manual})
            request = self.camera.capture_request(flush=True)
            request.save("main", path)
            request.release() 
            self.camera.set_controls({"AfMode": libcamera.controls.AfModeEnum.Continuous, "AfSpeed": libcamera.controls.AfSpeedEnum.Fast})
            
    def camera_config(self, config):
        with self.camera_lock:
            self.camera.configuration(config)


    def rotate_camera(self):
        self.camera_rotation += 1
        
        if self.camera_rotation > 1:
            self.camera_rotation = 0
        
        self.camera_config["transform"] = libcamera.Transform(vflip=self.camera_rotation)
        if self.streaming_count > 0:
            self.camera.stop_recording()
            sleep(1.0)
            self.camera.configure(self.camera_config)
            self.camera.start_recording(JpegEncoder(), FileOutput(self.output))
        else:
            self.camera.configure(self.camera_config)


    def generate_http_frames(self):
        if self.streaming_count == 0:
            raise Exception("streaming not started")
        while True:
            with self.output.condition:
                self.output.condition.wait()
                frame = self.output.frame
            resp = b'--FRAME\r\n'
            resp += b'Content-Type: image/jpeg\r\n'
            resp += b'Content-Length:' + bytes(len(frame)) + b'\r\n\r\n'
            resp += frame
            resp += b'\r\n'
            yield resp

   
