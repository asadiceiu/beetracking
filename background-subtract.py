import numpy as np
import os
import cv2
import matplotlib.pyplot as plt

base_folder = 'raw-data'
filelist = os.listdir(base_folder)

cap = cv2.VideoCapture(0)#("{}/{}".format(base_folder,filelist[10]))

bg = cv2.createBackgroundSubtractorKNN()
cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
cv2.namedWindow("Mask", cv2.WINDOW_NORMAL)

def processImage(frame):
    median = cv2.medianBlur(frame, 9)
    kernel = np.ones((5,5), np.uint8)
    erode = cv2.erode(median, kernel=kernel, iterations=1)
    return erode

def showImages(frame, mask):
    cv2.imshow("Frame",frame)
    cv2.imshow("Mask",processImage(mask))

counter = 0
while cap.isOpened():
    state, frame = cap.read()
    counter += 1
    # if counter % 10 > 0:
    #     pass
    if state:
        mask = bg.apply(frame)
        showImages(frame, mask)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break
cap.release()
cv2.destroyAllWindows()
