from platform import python_branch
from time import time
import cv2
from init import IP


class VideoCamera(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(IP) 
    
    def __del__(self):
        self.cap.release()
    
    def get_frame(self):
        success, image = self.cap.read()
        image = cv2.flip(image, -1)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

