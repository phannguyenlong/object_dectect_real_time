from time import time
import cv2

class Camera(object):
    def __init__(self):
        # self.frames = [open(f + '.jpg', 'rb').read() for f in ['1', '2', '3']]
        self.frames = cv2.VideoCapture(0);

    def get_rawFrame(self):
        ret, frame= self.frames.read()
        return frame

    def convert_frame(self,frame):
        (flag, encodedImage) = cv2.imencode(".jpg", frame)
        return encodedImage
        # return self.frames[int(time()) % 3]