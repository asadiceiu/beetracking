# OpenCV Playground
## Installing multiple libraries using pip command for python

`pip install -r <filename>`

e.g.

`pip install -r requirements.txt`

## Checking OpenCV Cameras
### Import necessary modules:
```
import numpy as np
import os
import cv2
```

First, we want to show a video we already have in our filesystem.

```
fname = 'video-file-name.mp4'
cap = cv2.VideoCapture(fname)
```
here, `cap` is the object which will open the video file for us. 
```
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
```
First, we checked if the `cap` object could really open the video or not. When we can see that it has actually succedded to open the video, we create a named window to display the video.

Our next job is to continuasly check if the `cap` object is currently open or not and if open get the frame from it. 

When we read a frame from a VideoCapture object, it returns the state of the frame (true or false) and the frame itself. If the state is false, it means we were not able to succesfully read the frame, which might indicate that the video is finished already. So, we break from the loop. However, if the state is true, we show the frame to our previously opened window. 

Also, we wait for user to press `q` key for 25 millisecond to see if user want to finish the process prematurely or not. 

When we break from the loop for any of the reasons described above, we release the VideoCapture object and destroy all windows currently visible.

## Displaying video from the Webcam
Displaying video from webcam is very easy. You just have to set the source of the video as an integer index value, everything else is exactly the same as displaying video from the filesystem. In this case, since I had only one webcam, I used index 0 as python usage 0-based indexing. 
```
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
```
