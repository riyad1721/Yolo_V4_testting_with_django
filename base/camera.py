import cv2
import cv2 as cv
import numpy as np
import time
import imutils
from imutils.video import VideoStream
from django.conf import settings
from pathlib import Path


# CONFIGATION_DIR=Path(settings.CONFIGATION_DIR)
# #print('SC: ',settings.CONFIGATION_DIR)
# detectClgPath = CONFIGATION_DIR / 'custom-yolov4-detector.cfg'
# #print(detectClgPath)
# detectWeightPath = CONFIGATION_DIR / 'custom-yolov4-detector_final.weights'
# #print('W: ', detectWeightPath)
# detectNamePath = CONFIGATION_DIR / 'obj.names'

net = cv2.dnn.readNet('./configuration/custom-yolov4-detector_final.weights','./configuration/custom-yolov4-detector.cfg')
classes = []
with open('./configuration/obj.names', "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i-1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

#######detected frame



class VideoPTZ(object):
	def __init__(self):
            self.rtsp_url=""
            self.video_stream = VideoStream(self.rtsp_url).start()
            

	def __del__(self):
            cv2.destroyAllWindows()
            self.video_stream.stop()

	def get_frame(self):
            frame = self.video_stream.read()
            #frame = imutils.resize(frame,width=1200)
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()


class ObjectDetect(object):
	def __init__(self):
            self.rtsp_url = ""
            self.cap = VideoStream(self.rtsp_url).start()
            self.font = cv2.FONT_HERSHEY_SIMPLEX
            self.starting_time = time.time()
            self.frame_id = 0

	def __del__(self):
            cv2.destroyAllWindows()
            self.cap.stop()

	def detect_and_predict(self,frame,net,output_layers):
            self.frame_id += 1
            height, width, channels = frame.shape
            # Detecting objects
            blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
            net.setInput(blob)
            outs = net.forward(output_layers)
            class_ids = []
            confidences = []
            boxes = []
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.8:
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)

                        # Rectangle coordinates
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)

                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.8, 0.3)

            label=[]
            confidence=[]
            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    label = str(classes[class_ids[i]])
                    confidence = confidences[i]
                    color = colors[class_ids[i]]
                    #######
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 30), self.font, 3, color, 3)
                    #######
            
            realTime= time.ctime(time.time())
            elapsed_time = time.time() - self.starting_time
            fps = self.frame_id / elapsed_time
            #print(confidence)
            return (label,confidence,fps,realTime)

	def get_frame(self):
            frame = self.cap.read()
            (label,confidence,fps,realTime) = self.detect_and_predict(frame,net,output_layers)
            ######
            cv2.putText(frame, "FPS: " + str(round(fps, 2)), (40, 670), self.font, .7, (0, 255, 255), 1)
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()
            ######
    
