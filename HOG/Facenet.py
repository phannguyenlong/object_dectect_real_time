import numpy as np
import cv2
import os
# prototxtPath = os.path.sep.join([args["face"], "deploy.prototxt"])
# weightsPath = os.path.sep.join([args["face"], "res10_300x300_ssd_iter_140000.caffemodel"])


def detectFace(frame):
	path = os.path.dirname(os.path.abspath(__file__))
	faceNet = cv2.dnn.readNet(os.path.sep.join([path, "face_detector/deploy.prototxt"]),
							  os.path.sep.join([path, "face_detector/res10_300x300_ssd_iter_140000.caffemodel"]))

	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))
	faceNet.setInput(blob)
	detections = faceNet.forward()

	# Extract ROIs

	for i in range(0, detections.shape[2]):
		confidence = detections[0, 0, i, 2]
		if confidence > 0.5:
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			(startX, startY) = (max(0, startX), max(0, startY))
			(endX, endY) = (min(w - 1, endX), min(h - 1, endY))

			face = frame[startY:endY, startX:endX].copy()
			face = cv2.resize(face, (64, 128))

			# cv2.imshow("Face",face)

			return face
	return 0
