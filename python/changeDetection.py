import numpy as np
import cv2
import cv2.cv as cv
import imutils

def get_frames(vid,skip):
    cap = cv2.VideoCapture(vid)
    frame_count = cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
    i_fCount = int(frame_count)
    images = []
    _,img = cap.read()
    for fr in range(0,i_fCount):
        _,img = cap.read()
        if(fr % skip == 0):
            cv2.imwrite(vid[:-4] + "_frame%d.jpg" % fr,img)
            images.append((vid[:-4] + "_frame%d.jpg" % fr))

    return images

get_frames("cd/media/final.mov", 2)

# cap = cv2.VideoCapture('media/fast.mp4')
# frameWidth = int(cap.get(cv.CV_CAP_PROP_FRAME_WIDTH))
# frameHeight = int(cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT))
# frameRate = int(cap.get(cv.CV_CAP_PROP_FPS))
# frameCount = int(cap.get(cv.CV_CAP_PROP_FRAME_COUNT))
#
# fgbg = cv2.BackgroundSubtractorMOG()
# prev = np.zeros((frameHeight,frameWidth), np.uint8)
# while(1):
#     ret, frame = cap.read()
#     fgmask = fgbg.apply(frame)
#     cv2.imshow('frame',fgmask)
#     diff = cv2.absdiff(prev, fgmask)
# #    diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
#
#     prev = fgmask
#     k = cv2.waitKey(10) & 0xff
#     if k == frameCount:
#         break
# cap.release()
# cv2.destroyAllWindows()

# bg = cv2.imread('cd/media/bg.jpg')
# cap = cv2.VideoCapture('cd/media/fast.mp4')
# frameWidth = int(cap.get(cv.CV_CAP_PROP_FRAME_WIDTH))
# frameHeight = int(cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT))
# frameRate = int(cap.get(cv.CV_CAP_PROP_FPS))
# frameCount = int(cap.get(cv.CV_CAP_PROP_FRAME_COUNT))
#
# prev = np.zeros((frameHeight,frameWidth), np.uint8)
# fr = 0
# skip = 1
# prev = []
# while(1):
#     ret, frame = cap.read()
#     diff = cv2.cvtColor(cv2.absdiff(frame, bg), cv2.COLOR_BGR2GRAY)
#     (thresh, im_bw) = cv2.threshold(diff, 20, 255, cv2.THRESH_BINARY) # | cv2.THRESH_OTSU)
#
#     blurred = cv2.medianBlur(im_bw,21)
#     #cv2.imshow("b", blurred)
#     cnts = cv2.findContours(blurred.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
#     cnts = cnts[0] if imutils.is_cv2() else cnts[1]
#     cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
#     if len(cnts) == 1:
#         M = cv2.moments(cnts[0])
#         if  M["m00"] != 0:
#             cX = int(M["m10"] / M["m00"])
#             cY = int(M["m01"] / M["m00"])
#     if(fr % skip == 0) and len(cnts) == 1 and (cX, cY) != prev:
#         prev = (cX,cY)
#         cv2.imwrite('cd/media/fast.mp4'[:-4] + "_%d.jpg" % fr,blurred)
# #    diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
#     fr += 1
#     k = cv2.waitKey(10) & 0xff
#     if k == frameCount:
#         break
# cap.release()
# cv2.destroyAllWindows()
