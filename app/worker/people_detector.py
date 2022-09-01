import time
import threading
from config.constant import model_path,label_path
from tflite_runtime.interpreter import Interpreter
import numpy as np
import cv2
from repositories.mqtt import mqtt
from loguru import logger
from threading import Thread
import datetime
class VideoStream:
    """Camera object that controls video streaming from the Picamera"""
    def __init__(self,url:str,resolution=(640,480),framerate=30):
        # Initialize the PiCamera and the camera image stream
        # self.stream = cv2.VideoCapture("rtsp://admin:Poltekpelsorong1@192.168.0.8:554/Streaming/channels/2/")
        self.stream = cv2.VideoCapture(url)
        ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        ret = self.stream.set(3,resolution[0])
        ret = self.stream.set(4,resolution[1])
            
        # Read first frame from the stream
        (self.grabbed, self.frame) = self.stream.read()

	# Variable to control when the camera is stopped
        self.stopped = False

    def start(self):
	# Start the thread that reads frames from the video stream
        Thread(target=self.update,args=()).start()
        return self

    def update(self):
        # Keep looping indefinitely until the thread is stopped
        while True:
            # If the camera is stopped, stop the thread
            if self.stopped:
                # Close camera resources
                self.stream.release()
                return

            # Otherwise, grab the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
	# Return the most recent frame
        return self.frame

    def stop(self):
	# Indicate that the camera and thread should be stopped
        self.stopped = True


class PeopleDetector(threading.Thread):
    def __init__(self, url : str) -> None:

        super(PeopleDetector, self).__init__()
        self.url = url
        self.setLightOff = False
        self.isEmpty = False
        with open(label_path, 'r') as f:
            self.labels = [line.strip() for line in f.readlines()]
        if self.labels[0] == '???':
            del(self.labels[0])
        
        self.interpreter = Interpreter(model_path=model_path)
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.height = self.input_details[0]['shape'][1]
        self.width = self.input_details[0]['shape'][2]
        
        self.interpreter.allocate_tensors()
        self.floating_model = (self.input_details[0]['dtype'] == np.float32)
        
        outname = self.output_details[0]['name']
        self.input_mean = 127.5
        self.input_std = 127.5

        if ('StatefulPartitionedCall' in outname): # This is a TF2 model
            self.boxes_idx, self.classes_idx, self.scores_idx = 1, 3, 0
        else: # This is a TF1 model
            self.boxes_idx, self.classes_idx, self.scores_idx = 0, 1, 2



        return None

    def run(self,*args,**kwargs):
        resW, resH = (720,480)
        imW, imH = int(resW), int(resH)
        videostream = VideoStream(resolution=(imW,imH),framerate=30,url=self.url).start()
        while True:
            people_num = 0
            frame1 = videostream.read()
            frame = frame1.copy()
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame_rgb, (self.width, self.height))
            input_data = np.expand_dims(frame_resized, axis=0)

            if self.floating_model:
                input_data = (np.float32(input_data) - self.input_mean) / self.input_std

            # Perform the actual detection by running the model with the image as input
            self.interpreter.set_tensor(self.input_details[0]['index'],input_data)
            self.interpreter.invoke()

            boxes = self.interpreter.get_tensor(self.output_details[self.boxes_idx]['index'])[0] # Bounding box coordinates of detected objects
            classes = self.interpreter.get_tensor(self.output_details[self.classes_idx]['index'])[0] # Class index of detected objects
            scores = self.interpreter.get_tensor(self.output_details[self.scores_idx]['index'])[0] # Confidence of detected objects
            for i in range(len(scores)):
                if (scores[i] > 0.6):

                    # Get bounding box coordinates and draw box
                    # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
                    ymin = int(max(1,(boxes[i][0] * imH)))
                    xmin = int(max(1,(boxes[i][1] * imW)))
                    ymax = int(min(imH,(boxes[i][2] * imH)))
                    xmax = int(min(imW,(boxes[i][3] * imW)))
                    

                    # Draw label
                    object_name = self.labels[int(classes[i])] # Look up object name from "labels" array using class index
                    label = '%s: %d%%' % (object_name, int(scores[i]*100)) # Example: 'person: 72%'
                    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
                    if object_name == "person":
                        people_num += 1
            # logger.info(f"Number of people inside room :{people_num}")
            now = datetime.datetime.now()
            if people_num == 0:
                if self.isEmpty == False:
                    ts1 = datetime.datetime.now()
                    self.isEmpty = True
                else:
                    if (datetime.datetime.now() - ts1).total_seconds() / 60 > 0.5:
                        self.setLightOff = True
            else:
                self.isEmpty=False
                self.setLightOff = False
            # logger.info(f"ip : {self.url} person detected : {people_num}")
            mqtt.people = people_num



  
