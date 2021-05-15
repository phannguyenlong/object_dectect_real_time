import cv2
import numpy as np
import HOG.HOG1
import os
import glob
from sklearn import svm
import joblib
import time
from HOG.Facenet import detectFace
#
# class_img= ["Correct","Wrong"]
# y=[]
# features_arr = np.empty(shape=[0,3780],dtype=float)
# for i in range(len(class_img)):
#         img_dir = "persons/" + class_img[i]  # Enter Directory of all images
#         data_path = os.path.join(img_dir, '*g')
#         files = glob.glob(data_path)
#         for j in files:
#             face = detectFace(cv2.imread(j));
#             print(type(face))
#             print(j)
#             if(type(face)==int):
#                 print("Cannot find face in ",j)
#                 continue
#             else:
#                 feature = HOG.HOG1.Hog1(face)
#                 features_arr = np.append(features_arr,[feature],axis=0)
#                 if (class_img[i] == "Correct"):
#                     y.append(1)
#                 else:
#                     y.append(-1)
#
# print(y)
# print(features_arr.shape)
#
# clf = svm.SVC(kernel='linear')
# print(np.where(features_arr >= np.finfo(np.float64).max))
# clf.fit(features_arr,y)
# joblib.dump(clf,'model.pkl')


# load model :


#feature = HOG.HOG1.Hog1(cv2.imread("nomaask.jpg"))
def Result(frame):
    path = os.path.dirname(os.path.abspath(__file__))
    clf = joblib.load(os.path.sep.join([path, "model.pkl"]))

    face = detectFace(frame)
    result = 1
    if (type(face) == int):
        print("Not finding face")
    else:
        feature = HOG.HOG1.Hog1(detectFace(frame))
        result = clf.predict([feature])
        print("Result: ", result)

        if result == -1:
            return frame
        else:
            return 0


#vs = VideoStream(src=0,resolution=(360,480)).start()

# while(True):
#     frame = vs.read()
#     face = detectFace(frame)
#     result =1
#     if(type(face)==int):
#         continue
#     else:
#         feature = HOG.HOG1.Hog1(detectFace(frame))
#         result = clf.predict([feature])
#         print("Result: ",result)
#
#         cv2.imshow("Frame", frame)
#
#         key = cv2.waitKey(1) & 0xFF
#
#     if result == -1:
#         cv2.imwrite("Frame.png", frame)
#         break