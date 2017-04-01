import os
import sys
import cv2
from getUserRect import *
from detectPattern import DetectContours
from computeMapping import *

# python warpMedia.py [rows] [cols] [mediaId] [x] [y] [w] [h]


class DetectContours:
    def getCentroids(self, contours):
        centroids = []
        for c in contours:
            #compute the center of the contour
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            centroids.append((cX,cY))

        return centroids

    def getContours(self, img): #returns centroid of contour (should only have one)
        # find contours in the thresholded image

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # TODO: fix the threshold to be based on overall image - relative brightness instead of absolute
        (thresh, im_bw) = cv2.threshold(gray, 145, 255, cv2.THRESH_BINARY) # | cv2.THRESH_OTSU)
        # cv2.imshow("b", im_bw)
        # cv2.waitKey(0)
        #im_bw = 255 - im_bw
        blurred = cv2.GaussianBlur(im_bw,(19,19),0)


        #cnts = cv2.findContours(im_bw.copy(), cv2.RETR_EXTERNAL,
        #    cv2.CHAIN_APPROX_SIMPLE)
    #    cnts, hierarchy = cv2.findContours(blurred, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        cnts = cv2.findContours(blurred, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

        # show the image
        cv2.drawContours(img, [cnts[0]], -1, (0, 255, 0), 2)
#
        cv2.imshow("Image", img)
        cv2.waitKey(0)
        return [cnts[0]]

rows = int(sys.argv[1])
cols = int(sys.argv[2])
x = int(float(sys.argv[4]))
y = int(float(sys.argv[5]))
w = float(sys.argv[6])
h = float(sys.argv[7])

number_points = rows * cols
print rows, cols
sys.stdout.flush()


userpt_locations = read_user_dots(os.getcwd() + "/user/generated/" + sys.argv[3], number_points, x,y,w,h,
                    cv2.imread(os.getcwd() + "/user/camera/" + sys.argv[3] + "/0.jpg").shape)
origpoints = read_dots(os.getcwd() + "/user/generated/" + sys.argv[3], number_points) #camera points

points = read_dots(os.getcwd() + "/user/camera/" + sys.argv[3], number_points) #camera points
forwarp = cv2.imread(os.getcwd() + "/user/uploads/" + sys.argv[3]) # + ".jpg") #media for warp
height, width, depth = forwarp.shape
warp_image(map(lambda x:x[0],origpoints), forwarp, (rows, cols), map(lambda x:x[0], userpt_locations), map(lambda x:x[0], points), os.getcwd() + "/user/final/" + sys.argv[3]+".jpg")
