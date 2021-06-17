import numpy as np
import os
import cv2
import matplotlib.pyplot as plt

base_folder = 'raw-data'
filelist = os.listdir(base_folder)

insectMinThresh = 500.0 
insectMaxThresh = 4000.0
startPosition = 0

#create a KNN background subtractor
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

def findInsectsCC(binary_image):
    '''
    Finds insects using connected component analysis of the binary image which is 
    expected to be filtered with median blur and erosion technique to eliminate
    all high frequency noises
    '''
    (nlabels, labels, stats, centroids) = cv2.connectedComponentsWithStats(binary_image, connectivity=8)
    positions = np.zeros(shape=(0,8)) #left, top, w, h, area, centroid, label
    mask = np.zeros_like(binary_image)
    if nlabels>1: #the first label is always the background
        for i in range(1,nlabels):
            if stats[i,4] > insectMinThresh and stats[i,4] <= insectMaxThresh:
                positions = np.vstack([positions, (stats[i,0], stats[i,1], stats[i,2], stats[i,3], stats[i,4], centroids[i,0], centroids[i,1], i)])
                cmask = (labels == i).astype("uint8") * 255
                mask = np.bitwise_or(mask, cmask)
    return mask, positions


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

def processImage(frame):
    median = cv2.medianBlur(frame, 9)
    kernel = np.ones((5,5), np.uint8)
    erode = cv2.erode(median, kernel=kernel, iterations=1)
    return findInsectsCC(erode)
    

def showImages(frame, mask, fname, counter):
    insects, positions = processImage(mask)
    frame = draw_label(frame, "Video: {}, Frame No:{}/{}, FPS:{}".format(fname, cap.get(cv2.CAP_PROP_POS_FRAMES),nFrames, cap.get(cv2.CAP_PROP_FPS)),(20,20), (0,255,0)) #B,G,R
    if len(positions)>0:
        frame[:,:,2] = insects
        #cv2.imwrite("predicted-bees/frame-{:06d}.jpg".format(counter+startPosition),frame)
        #cv2.imwrite("predicted-bees/mask-{:06d}.jpg".format(counter,startPosition),mask)        
        wrt.write(frame)
    cv2.imshow("Mask", insects)
    cv2.imshow("Frame",frame)

for fname in filelist[10:]:
    #Creating a video capture and video writter object 
    cap = cv2.VideoCapture(("{}/{}".format(base_folder,fname)))
    cap_w, cap_h = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    nFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    dirname = os.path.splitext(fname)[0]
    if not os.path.isdir("background-subtract/{}".format(dirname)):
        os.mkdir("background-subtract/{}".format(dirname))
    wrt = cv2.VideoWriter("background-subtract/{0}/{0}.avi".format(dirname), cv2.VideoWriter_fourcc('M','J','P','G'), 24, (cap_w, cap_h))
    counter = 0
    while cap.isOpened():
        state, frame = cap.read()
        counter += 1
        if state:
            mask = bg.apply(frame)
            showImages(frame, mask, fname, counter)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    wrt.release()
        
cv2.destroyAllWindows()
