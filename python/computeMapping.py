import cv2
import cv2.cv as cv
import numpy as np
import math
import sys
import os
import imutils
from util import *
from getUserRect import *
from detectPattern import DetectContours
from detectPattern import DetectCircles
from findHomography import FindHomography

dco = DetectContours()
dci = DetectCircles()
fh = FindHomography()

# TODO: automate getting the centroids of all the original calibration images

orig12 = [(30, 30), (283, 30), (536, 30), (789, 30), (30, 310), (283, 310),
(536, 310), (789, 310), (30, 589), (283, 589), (536, 589), (789, 589)]

orig18 = [(30, 30), (182, 30), (334, 30), (486, 30), (638, 30),
(789, 30), (30, 310), (182, 310), (334, 310), (486, 310),
(638, 310), (789, 310), (30, 589), (182, 589), (334, 589),
(486, 589), (638, 589), (789, 589)]


#(1) translation from original to points -> get in between pixels from bilinear interpolation
#(2) homography from 4 points (1245) (2356)

#(1)

#form corners for bilinear interpolation: find a homography to make 4 corners rectilinear and apply
# homo from camera to original. new = apply homo to original
# bilinearly interpolate the orignal pixels to the new image

# def scale_translate_correction(image, transform) <-- TODO: needs to be cumulative for geometric prewarp


def interpolate_colour(original_image, (x0,y0)):
    # x0, y0 are non-integers
    x1 = int(math.floor(x0))
    x2 = int(math.ceil(x0))
    y1 = int(math.floor(y0))
    y2 = int(math.ceil(y0))
    if y2 >= original_image.shape[0] or x2 >= original_image.shape[1]:
        return [0,0,0]
    if x1 != x2 and y1 != y2:
        bi_points = []
        #TODO: check if its original_image[x,y] or original_image[y,x]
        bi_points.append((x1, y1, np.array(map(int, original_image[y1, x1]))))
        bi_points.append((x2, y1, np.array(map(int, original_image[y1, x2]))))
        bi_points.append((x1, y2, np.array(map(int, original_image[y2, x1]))))
        bi_points.append((x2, y2, np.array(map(int, original_image[y2, x2]))))
        colour = bilinear_interpolation(x0, y0, bi_points)
    else:
        colour = [0, 0, 0]
        if x1 == x2:
            #linearly interpolate y: color = ...
            colour = lerp(y0, [(y1, original_image[y1, x1]), (y2,original_image[y2, x1])])
        if y1 == y2:
            #linearly interpolate x: color = ...
            colour = lerp(x0, [(x1, original_image[y1, x1]), (x2,original_image[y1, x2])])
    return colour


# TRANSFORM :  H (inverse)
# reverse_warp_helper and warp_image are functions that loop through the rectangles and apply reverse bilinear interpolation
# to each point in the target image rectangle to obtain the colour

def reverse_warp_helper(original_points, user_points, target, forwarp, cam_points, fx, fy, tx, ty):

    target_h, target_w, target_d = target.shape

    inverse_transform = fh.sourceToDest(np.array(user_points), np.array(cam_points))

    #TODO: change this from a simple nested loop to apply a function on a single numpy array (faster)
    for y in range(target_h):
        for x in range(target_w):
            # inv transform
            # if point in original box, interpolate color, else point outside, put as black/white?
            # then mask out the black/white outside points and combine the image
            original_location = fh.getDest([x,y], inverse_transform)
            (x0, y0) = original_location[0]

            scale = np.asarray([[fx, 0, 0], [0, fy, 0], [0, 0, 1]])
            (x1, y1) = fh.getDest([x0, y0], scale)[0]

            x2 = x1 - tx
            y2 = y1 - ty


            #check if the original location, according to the homography,  is  within our rectangle of interest
            if y2 >= original_points[0][1] and y2 <= original_points[-1][1] and x2 >= original_points[0][0] and x2 <= original_points[1][0]:
                target[y,x] = interpolate_colour(forwarp, (x2,y2))
            else:
                target[y,x] = [0,0,0]


def warp_image(original_points, forwarp, points_shape, user_points, cam_points, path, fx, fy, x, y):
    # points_shape: (rows, cols) tuple, describing the layout of dots e.g. 9 dots (3,3) or 12 dots (3,4)
    blank = np.zeros(forwarp.shape, dtype=np.uint8)
    #this function passes indices to a helper, which will transform that sub-rectangle
    rows = points_shape[0]
    cols = points_shape[1]
    for index in range(len(original_points)-cols-1):
        temp = np.zeros(blank.shape, dtype=np.uint8)
        if (index+1) % cols != 0:
            print index+cols+1
            sys.stdout.flush()

            original_corners = [original_points[index], original_points[index+1],
                                original_points[index+cols], original_points[index+cols+1]]
            cam_corners = [cam_points[index], cam_points[index+1], cam_points[index+cols], cam_points[index+cols+1]]
            user_corners = [user_points[index], user_points[index+1], user_points[index+cols], user_points[index+cols+1]]
            reverse_warp_helper(original_corners, user_corners, temp, forwarp, cam_corners, fx, fy, x, y)
        blank = cv2.add(blank, temp)

    cv2.imwrite(path, blank)
#    cv2.imshow('blank', blank)
#    cv2.waitKey(0)

def read_dots(path, number_points):
    dco = DetectContours()
    points = []
    for i in range(0,number_points):
        #if i < 10:
        #    i = str(0) + str(i)
        print path + "/" + str(i) + ".jpg"
        img = cv2.imread(path + "/" + str(i) + ".jpg")
        a = dco.getContours(img)
        #dci.get_circles(img)
        points.append(dco.getCentroids(a))
        #points.append(dci.get)
    return points



#TODO: make number_points based on (r,c)
# number_points = 28
# dco = DetectContours()
# fh = FindHomography()
# points = []
# cam_shape = []
#
# points = read_dots("images/" + sys.argv[1], number_points)
#
# x = 250
# y = 150
# w = 300
# h = 200
#
# print points
# forwarp = cv2.imread("images/" + sys.argv[1] + "/0.jpg")
# height, width, depth = forwarp.shape
# userpt_locations = map(lambda x: x[0], read_user_dots("images/4e28/", number_points, x,y,w,h, cv2.imread("images/" + sys.argv[1] + "/0.jpg").shape))
# orig = map(lambda x: x[0], read_dots("images/4e28/", number_points))
#
# #warp_image(orig, forwarp, (4,7), userpt_locations, map(lambda x:x[0], points), sys.argv[2])
# warp_image(map(lambda x:x[0], points), forwarp, (4,7), userpt_locations, map(lambda x:x[0], points), sys.argv[2])
