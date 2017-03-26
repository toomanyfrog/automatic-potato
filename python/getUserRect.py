import cv2
import numpy as np
import imutils
import sys

# remember to generate the dot image based on their desired projected image
# two images - one white rectangle and one dots based on user-drawn/getPerspectiveTransform

def get_dots(path):
    dots = cv2.imread(path)

    gots = cv2.cvtColor(dots, cv2.COLOR_BGR2GRAY)
    (thresh, bwots) = cv2.threshold(gots, 240, 255, cv2.THRESH_BINARY) # | cv2.THRESH_OTSU)
    dot_cnts = cv2.findContours(bwots, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    dot_cnts = dot_cnts[0] if imutils.is_cv2() else dot_cnts[1]
    cnts = dot_cnts[::-1]
    #x,y,w,h = cv2.boundingRect(rect_contours[0])
    centroids = []
    for contour in cnts:
        cv2.drawContours(dots, contour, -1, (0, 255, 0), 2)
        # cv2.imshow("a", dots)
        # cv2.waitKey(0)
        M = cv2.moments(contour)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        centroids.append((cX,cY))

    return centroids
