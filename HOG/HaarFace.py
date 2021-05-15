import numpy as np
import cv2
from imutils.video import VideoStream

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

img = cv2.imread('test.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# cv2.imshow('img',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

vs = VideoStream(src=0).start()
while(True):
    frame = vs.read()

    frame = cv2.resize(frame, (800, 400))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 1)
    for (x, y, w, h) in faces:
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        cv2.imwrite("Frame.png", frame)
        break