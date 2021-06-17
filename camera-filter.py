import numpy as np
import cv2

## Step 1: Get Video from the camera
## Step 2: Get input: Left, Right, Top, Down, Diagonal Top-left, Diagonal Top-right, Diagonal Bottom-left, Diagonal Bottom-right
## Step 3: Display the line based on user input

print("L: left to right\nR: right to left\nT: top to bottom\nB: bottom to top\n\nBoth uppercase and lowercase is accepted. ESC to quit.")

cap = cv2.VideoCapture(0)
counter = 0
direction = -1 #L=1, R=2, T=3, B=4
state, frame = cap.read()
h,w,d = frame.shape
newframe = np.zeros_like(frame)
while state:
    cv2.imshow("Frame",frame)
    key = cv2.waitKeyEx(25)
    if key == ord('L') or key == ord('l'):
        direction = 1
        counter = 0
    elif key == ord('R') or key == ord('r'):
        direction = 2
        counter = w
    elif key == ord('T') or key == ord('t'):
        direction = 3
        counter = 0
    elif key == ord('B') or key == ord('b'):
        direction = 4
        counter = h
    if direction==1 and counter<w-1:
        newframe[:,counter:counter+1,:] = frame[:,counter:counter+1,:] 
        counter += 1
    elif direction==2 and counter>0:
        newframe[:,counter-1:counter,:] = frame[:,counter-1:counter,:] 
        counter -= 1
    elif direction==3 and counter<h-1:
        newframe[counter:counter+1,:,:] = frame[counter:counter+1,:,:]
        counter += 1
    elif direction==4 and counter>0:
        newframe[counter-1:counter,:,:] = frame[counter-1:counter,:,:] 
        counter -= 1
    if direction > 0:
        cv2.imshow("Scanned",newframe)
    if key == 27: #27 is the value for ESC key. #cv2.waitKey(10) & 0xFF == ord('q'):
        break
    state, frame = cap.read()
cv2.imwrite('filterdimage.jpg',newframe)
cap.release()
cv2.destroyAllWindows()


def showScanLine(img,dir=1):
    h,w,d = img.shape
    #Top to bottom
    newImage = np.zeros_like(img)
    for i in range(0,h):
        newImage[i:i+1,:,:] = img[i:(i+1),:,:]
        cv2.imshow('Scanned',newImage)
        if cv2.waitKey(1000) & 0xFF==ord('q'):
            break