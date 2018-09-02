import os
import datetime
from gpiozero import MotionSensor
from picamera import PiCamera
from picamera import PiCameraError
from time import sleep

MOTION_PIN = 14
MIN_REC_TIME = 60
INTERVAL = 3
POLL = 0.1
APP_PATH = './'
VIDEO_PATH = 'video/'
LOG_PATH = 'logs/'

def start_camera():
	try:
		camera = PiCamera()
		camera.resolution = (1920, 1080)
	except PiCameraError:
		log("camera error on startup")
		quit()
	return camera
	
	

def log(log_text):
	now = datetime.datetime.now()
	logfile = open(os.path.expanduser(APP_PATH + LOG_PATH + now.strftime('%Y-%m-%d') + '.txt'), 'a+')
	output_text = now.strftime('%H:%M:%S') + '-' + log_text
	print(output_text)
	logfile.write(output_text + '\n')
	logfile.close()
		

def main_loop(pir, camera):
	rec_time = 0
	rec_on = False
	while True:
		if pir.motion_detected:
			log("motion detected " + str(rec_time)+ 's')
			rec_time = MIN_REC_TIME
			if rec_on == False:
				try:
					now = datetime.datetime.now()
					directory = os.path.expanduser(APP_PATH + VIDEO_PATH + now.strftime('%Y-%m-%d') + '/')
					if os.path.exists(directory) != True:
						os.mkdir(directory)
					camera.start_recording(directory + now.strftime('%H:%M:%S') + '.h264')
				except PiCameraError:
					log("camera error on start record")
					start_camera()

				rec_on = True
				log("video on")
				
		if rec_on:
			camera.wait_recording(INTERVAL)
			rec_time = rec_time - INTERVAL
		else:
			sleep(POLL)
		if rec_time <= 0 and rec_on:
			try:
				camera.stop_recording()
			except PiCameraError:
				log("camera error on stop record")
				start_camera()	
			rec_on = False
			log("video off")
			
		
		

if __name__ == "__main__":
	log("starting")
	pir = MotionSensor(MOTION_PIN)		
	log("camera startup")
	main_loop(pir, start_camera())
	
