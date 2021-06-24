import numpy as np
import os
import cv2
bg = cv2.createBackgroundSubtractorKNN()
cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
cv2.namedWindow("Mask", cv2.WINDOW_NORMAL)

cap = cv2.VideoCapture(0)
if cap.isOpened() == False:
    print("Camera couldn't be opened")
else:
    cv2.namedWindow("Video Player", cv2.WINDOW_KEEPRATIO)
    print("Press 'Q' to stop")
    while cap.isOpened():
        state, frame = cap.read()
        if state==True:
            mask = bg.apply(frame)
            median = cv2.medianBlur(mask, 9)
            kernel = np.ones((3,3), np.uint8)
            erode = cv2.erode(median, kernel=kernel, iterations=1)

            cv2.imshow("Frame", frame)
            cv2.imshow("Mask",erode)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break
cap.release()
cv2.destroyAllWindows()