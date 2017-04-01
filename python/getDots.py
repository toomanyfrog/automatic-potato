import cv2
import numpy as np
import imutils
import sys
from detectPattern import DetectContours


# remember to generate the dot image based on their desired projected image
# two images - one white rectangle and one dots based on user-drawn/getPerspectiveTransform

def read_cam_dots(path, number_points):
    dco = DetectContours()
    points = []
    bg = cv2.imread(path + "/0.jpg")
    for i in range(0, number_points):
        img = cv2.imread(path + "/" + str(i+1) + ".jpg")
        diff = cv2.absdiff(bg, img)

def read_dots(path, number_points):
    dco = DetectContours()
    points = []
    for i in range(0,number_points):
        #if i < 10:
        #    i = str(0) + str(i)
        print path + "/" + str(i+1) + ".jpg"
        img = cv2.imread(path + "/" + str(i+1) + ".jpg")
        a = dco.getContours(img)
        #dci.get_circles(img)
        points.append(dco.getCentroids(a))
        #points.append(dci.get)
    return points



def read_user_dots(path, number_points, x, y, w, h, shape):
    dco = DetectContours()
    points = []
    for i in range(0,number_points):
        #if i < 10:
        #    i = str(0) + str(i)
        print path + "/" + str(i+1) + ".jpg"
        img = cv2.imread(path + "/" + str(i+1) + ".jpg")
        # make image for userpt_locations
        blank = np.zeros(shape)
        f_x = 1.0 * w / img.shape[1]
        f_y = 1.0* h / img.shape[0]

        print img.shape
        print f_y, f_x
        print w/img.shape[1], h/img.shape[0]
        sys.stdout.flush()

        dots = cv2.resize(img, (None), fx=f_x, fy=f_y, interpolation = cv2.INTER_LINEAR)
        blank[y:int(y+h), x:int(x+w)] = dots
        print blank.dtype
        sys.stdout.flush()
        a = dco.getContours(np.asarray(blank, np.uint8))
        #dci.get_circles(img)
        points.append(dco.getCentroids(a))
        #points.append(dci.get)
    return points

#DOTS IS A IMG MADE BLACK N WHITE SO CAN USE THRESH 240
def get_dots(dots):
#    dots = cv2.imread(path)

    print dots.shape
    print dots.dtype
    gots = cv2.cvtColor(dots, cv2.COLOR_BGR2GRAY)
    (thresh, bwots) = cv2.threshold(gots, 240, 255, cv2.THRESH_BINARY) # | cv2.THRESH_OTSU)

    print bwots.shape
    print bwots.dtype
    sys.stdout.flush()

    dot_cnts = cv2.findContours(bwots, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    dot_cnts = dot_cnts[0] if imutils.is_cv2() else dot_cnts[1]
    cnts = dot_cnts[::-1]
    #x,y,w,h = cv2.boundingRect(rect_contours[0])
    centroids = []
    for contour in cnts:
        cv2.drawContours(dots, contour, -1, (0, 255, 0), 2)
        cv2.imshow("a", dots)
        cv2.waitKey(0)
        M = cv2.moments(contour)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        centroids.append((cX,cY))

    return centroids
