from platform import python_branch
from time import time
import cv2
from init import *


class VideoCamera(object):
    def __init__(self,IP_USE):
        self.cap = cv2.VideoCapture(IP_USE) 
    
    def __del__(self):
        self.cap.release()
    
    def get_frame(self):
        success, image = self.cap.read()
        image = cv2.flip(image, -1)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

