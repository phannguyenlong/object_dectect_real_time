import numpy as np
import cv2
from numpy import linalg as LA


#img = cv2.imread("data_test.jpg")
def Hog1(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    y_kernel = np.array([[-1],[0],[1]]) # 1d array, different from sobel kernel (3x3)
    x_kernel = np.array([[-1,0,1]]) # carefully to have double [[

    dx = cv2.filter2D(gray,cv2.CV_32F,x_kernel)
    dy = cv2.filter2D(gray,cv2.CV_32F,y_kernel)

    magnitude_arr = np.sqrt(np.square(dx)+np.square(dy))
    orientation_arr = np.degrees(np.arctan(np.divide(dy,dx+0.001)))
    orientation_arr+=90
    # vote 8x8 cell into histogram

    number_cell_x = 8
    number_cell_y = 16

    histogram = np.zeros(shape=[number_cell_y,number_cell_x,9])
    for cx in range(number_cell_x):
        for cy in range(number_cell_y):
            histogram_cell = np.zeros([9])
            magnitude_cell = magnitude_arr[cy * 8:cy * 8 + 8, cx * 8:cx * 8 + 8]
            orientation_cell = orientation_arr[cy * 8:cy * 8 + 8, cx * 8:cx * 8 + 8]
            for i in range(orientation_cell.shape[0]):
                for j in range(orientation_cell.shape[1]):
                    index =np.int(np.abs(np.divide(orientation_cell[i,j]-1,20))) # avoid 20/20 = 1 (20 is in bin 0), abs to avoid 0-1 = negative => negative index
                    histogram_cell[index] +=magnitude_cell[i,j]
            histogram[cy,cx,:] = histogram_cell


    features = np.zeros(shape=[15,7,36],dtype=float)
    for i in range(15):
        for j in range(7):
            v = histogram[i:i+2,j:j+2].flatten()
            features[i,j,:] = v/LA.norm(v,2)
            if np.isnan(features[i, j, :]).any():  # avoid NaN (zero division)
                         features[i, j, :] = v

    features = features.flatten()
    # print(np.dtype(features[0]))
    return features
    # print(features)
    # cv2.imshow("img",gray)
    #cv2.waitKey(0)


