import numpy as np
import cv2
import cv2.cv as cv

cap = cv2.VideoCapture('still28.mov')
frameWidth = int(cap.get(cv.CV_CAP_PROP_FRAME_WIDTH))
frameHeight = int(cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT))
frameRate = int(cap.get(cv.CV_CAP_PROP_FPS))
frameCount = int(cap.get(cv.CV_CAP_PROP_FRAME_COUNT))

fgbg = cv2.BackgroundSubtractorMOG()
prev = np.zeros((360,640), np.uint8)
while(1):
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)
    cv2.imshow('frame',fgmask)
    diff = cv2.absdiff(prev, fgmask)
#    diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    if not cv2.countNonZero(diff) == 0:
        cv2.imshow('diff', diff)

    prev = fgmask
    k = cv2.waitKey(10) & 0xff
    if k == frameCount:
        break
cap.release()
cv2.destroyAllWindows()
