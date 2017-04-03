import cv2
import cv2.cv as cv
import numpy as np
import math
import sys
import os
import imutils
from util import *
from getDotsOld import *
from detectPattern import DetectContours
from detectPattern import DetectCircles
from findHomography import FindHomography
#from computeMapping import interpolate_colour, reverse_warp_helper, warp_image


# 1) check that i warp rectangle to camera image

number_points = 28
dco = DetectContours()
fh = FindHomography()
cam_points = []
cam_shape = []
x = 100
y = 50
w = 300
h = 200
#userpt_locations = read_user_dots(os.getcwd() + "/user/generated/" + sys.argv[3], number_points, x,y,w,h,
        #            cv2.imread(os.getcwd() + "/user/camera/" + sys.argv[3] + "/0.jpg").shape)
#origpoints = read_dots(os.getcwd() + "/user/generated/" + sys.argv[3], number_points) #camera points

for i in range(0,number_points):
    #if i < 10:
    #    i = str(0) + str(i)
    img = cv2.imread("images/" + sys.argv[1] + "/" + str(i) + ".jpg")
    a = dco.getContours(img)
    #dci.get_circles(img)
    cam_points.append(dco.getCentroids(a))
    #points.append(dci.get)

#userpt_locations = get_dots(cv2.imread("images/user/3e18user.jpg"))
userpts = read_user_dots("images/4e28", number_points, x,y,w,h,cv2.imread("images/4c28/0.jpg").shape)
userpts = map(lambda x: x[0], userpts)
#userpt_orig_locations = original_locations(userpt_locations, (3,6), orig18, points)

def rvs_warp_pts(points_shape, user_points, cam_points):
    #blank = np.zeros(cv2.imread("images/" + sys.argv[1] + "/0.jpg").shape, dtype=np.uint8)
    blank = cv2.imread("images/4c28/0.jpg")
    rows = points_shape[0]
    cols = points_shape[1]
    for index in range(len(user_points)-cols-1):
        print index, index+1, index+cols, index+cols+1
        if (index+1) % cols != 0:
            cam_corners = [cam_points[index], cam_points[index+1], cam_points[index+cols], cam_points[index+cols+1]]
            user_corners = [user_points[index], user_points[index+1], user_points[index+cols], user_points[index+cols+1]]

            #transform = fh.sourceToDest(np.array(cam_points)[:,0], np.array(original_points))
            inverse_transform = fh.sourceToDest(np.array(user_corners), np.array(cam_corners)[:,0])
            for corner in user_corners:
                (x, y) = fh.getDest(corner, inverse_transform)[0]
                cv2.circle(blank, (int(x), int(y)), 3, [0,0,255], -1)
    #    blank = cv2.add(blank, temp)

    cv2.imwrite(sys.argv[2], blank)


# 2)


def warp_pts(points_shape, user_points, cam_points):
    #blank = np.zeros(cv2.imread("images/" + sys.argv[1] + "/0.jpg").shape, dtype=np.uint8)
    blank = cv2.imread("images/4c28/0.jpg")
    rows = points_shape[0]
    cols = points_shape[1]
    for index in range(len(user_points)-cols-1):
        print index, index+1, index+cols, index+cols+1
        if (index+1) % cols != 0:
            cam_corners = [cam_points[index], cam_points[index+1], cam_points[index+cols], cam_points[index+cols+1]]
            user_corners = [user_points[index], user_points[index+1], user_points[index+cols], user_points[index+cols+1]]

            #transform = fh.sourceToDest(np.array(cam_points)[:,0], np.array(original_points))
            transform = fh.sourceToDest(np.array(cam_corners)[:,0], np.array(user_corners))
            for corner in map(lambda x: x[0], cam_corners):
                (x, y) = fh.getDest(corner, transform)[0]
                print x,y
                cv2.circle(blank, (int(x), int(y)), 3, [0,0,255], -1)
    #    blank = cv2.add(blank, temp)

    cv2.imwrite(sys.argv[2], blank)


warp_pts((4,7), userpts, cam_points)
