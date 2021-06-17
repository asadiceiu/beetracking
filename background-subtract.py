import numpy as np
import os
import cv2
import matplotlib.pyplot as plt

base_folder = 'raw-data'
filelist = os.listdir(base_folder)

insectMinThresh = 500.0 
insectMaxThresh = 4000.0
startPosition = 0


cap = cv2.VideoCapture(("{}/{}".format(base_folder,filelist[10])))
cap.set(cv2.CAP_PROP_POS_FRAMES,startPosition)
wrt = cv2.VideoWriter('predicted-bees/video.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 30, (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
nFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

bg = cv2.createBackgroundSubtractorKNN()
cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
cv2.namedWindow("Mask", cv2.WINDOW_NORMAL)


def findInsects(binary_image):
    '''
    Finds all contours larger then a specific area size
    '''
    contours, hier = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    insects = np.zeros(shape=(0,3))
    for c in contours:
        (x,y), (w,h), _ = cv2.minAreaRect(c)
        if w*h > insectMinThresh and w*h < insectMaxThresh:
            insects = np.vstack([insects, (x,y,w*h)])
    return insects, contours

def draw_label(img, text, pos, bg_color):
    font_face = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.4
    color = (0, 0, 0)
    thickness = cv2.FILLED
    margin = 2

    txt_size = cv2.getTextSize(text, font_face, scale, thickness)

    end_x = pos[0] + txt_size[0][0] + margin
    end_y = pos[1] - txt_size[0][1] - margin

    cv2.rectangle(img, pos, (end_x, end_y), bg_color, thickness)
    cv2.putText(img, text, pos, font_face, scale, color, 1, cv2.LINE_AA)
    return img

def processImage(frame, counter=0):
    median = cv2.medianBlur(frame, 9)
    kernel = np.ones((5,5), np.uint8)
    erode = cv2.erode(median, kernel=kernel, iterations=1)
    insects, contours = findInsects(erode)
    if len(insects)>0:
        with open('insect-pos.txt','a+') as fp:
            fp.write('\n')
            txt = "\n".join([", ".join([str(insect[0]),str(insect[1]),str(insect[2])]) for insect in insects])
            fp.write(txt)
        return erode, contours
    return erode, False

def showImages(frame, mask, counter):
    
    mask, contours = processImage(mask, counter)
    frame = draw_label(frame, "Frame No:{}/{}, FPS:{}".format(cap.get(cv2.CAP_PROP_POS_FRAMES),nFrames, cap.get(cv2.CAP_PROP_FPS)),(20,20), (0,255,0)) #B,G,R
    if contours and np.sum(np.uint8(mask>0),axis=None)>200:
        frame = cv2.drawContours(frame,contours,-1,(0,0,255))
        
        frame[:,:,2] = mask
        #cv2.imwrite("predicted-bees/frame-{:06d}.jpg".format(counter+startPosition),frame)
        #cv2.imwrite("predicted-bees/mask-{:06d}.jpg".format(counter,startPosition),mask)        
        wrt.write(frame)
    cv2.imshow("Mask", mask)
    cv2.imshow("Frame",frame)

counter = 0
while cap.isOpened():
    state, frame = cap.read()
    counter += 1
    if state:
        mask = bg.apply(frame)
        showImages(frame, mask, counter)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break
cap.release()
wrt.release()
cv2.destroyAllWindows()
