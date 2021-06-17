import numpy as np
import os
import cv2
import matplotlib.pyplot as plt

base_folder = 'raw-data'
filelist = os.listdir(base_folder)

#create a KNN background subtractor
bg = cv2.createBackgroundSubtractorKNN()

cap = cv2.VideoCapture(("{}/{}".format(base_folder,filelist[10])))
cap.set(cv2.CAP_PROP_POS_FRAMES,3600)
cap_w, cap_h = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
state, frame = cap.read()
while state:
    cv2.imshow("Frame",frame)
    mask = bg.apply(frame)
    cv2.imshow("Mask",mask)
    key = cv2.waitKeyEx(0)
    if key ==  ord('q'):
        break
    if key == ord('s'):
        median = cv2.medianBlur(mask, 9)
        cv2.imshow("Median", median)
        kernel = np.ones((5,5), np.uint8)
        erode = cv2.erode(median, kernel=kernel, iterations=1)
        cv2.imshow("Erode",erode)
        (numLabels, labels, stats, centroids) = cv2.connectedComponentsWithStats(erode,connectivity=8)
        for i in range(1,numLabels):
            print(stats[i])
            print(centroids[i])
    state, frame = cap.read()
cap.release()
cv2.destroyAllWindows()