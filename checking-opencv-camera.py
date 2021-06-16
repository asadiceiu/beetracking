import numpy as np
import os
import cv2
import matplotlib.pyplot as plt

base_folder = 'raw-data'
filelist = os.listdir(base_folder)

cap = cv2.VideoCapture("{}/{}".format(base_folder,filelist[1]))

if cap.isOpened()==False:
    print("Error opening the video")

else:
    cv2.namedWindow("Video Player", cv2.WINDOW_NORMAL)
    while cap.isOpened():
        state, img = cap.read()
        if state == True:
            cv2.imshow('Video Player',img)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break
cap.release()
cv2.destroyAllWindows()

## Opening and displaying images from the laptop camera (find the appropriate name for laptop camera)
cap = cv2.VideoCapture(0)
if cap.isOpened() == False:
    print("Camera couldn't be opened")
else:
    cv2.namedWindow("Video Player", cv2.WINDOW_KEEPRATIO)
    print("Press 'Q' to stop")
    while cap.isOpened():
        state, img = cap.read()
        img = cv2.Canny(img, 100,200)
        if state==True:
            cv2.imshow("Video Player", img)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break
cap.release()
cv2.destroyAllWindows()