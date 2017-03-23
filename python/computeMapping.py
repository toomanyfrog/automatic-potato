import cv2
import cv2.cv as cv
import numpy as np
import math
import sys
from detectPattern import DetectContours
from detectPattern import DetectCircles
from findHomography import FindHomography
#TODO: make dot image generator

def lerp(v, twopoints):
    (v0, value0), (v1, value1) = twopoints
    t = v - v0
    return (1 - t) * value0 + t * value1

def bilinear_interpolation(x, y, points):
    '''Interpolate (x,y) from values associated with four points.

    The four points are a list of four triplets:  (x, y, value).
    The four points can be in any order.  They should form a rectangle.

        >>> bilinear_interpolation(12, 5.5,
        ...                        [(10, 4, 100),
        ...                         (20, 4, 200),
        ...                         (10, 6, 150),
        ...                         (20, 6, 300)])
        165.0

    '''
    # See formula at:  http://en.wikipedia.org/wiki/Bilinear_interpolation

    points = sorted(points)               # order points by x, then by y
    (x1, y1, q11), (_x1, y2, q12), (x2, _y1, q21), (_x2, _y2, q22) = points

    if x1 != _x1 or x2 != _x2 or y1 != _y1 or y2 != _y2:
        raise ValueError('points do not form a rectangle')
    if not x1 <= x <= x2 or not y1 <= y <= y2:
        raise ValueError('(x, y) not within the rectangle: ' + str(x1) + ', ' + str(x) + ', ' + str(x2) + " OR "+ str(y1) + ', ' + str(y) + ', ' + str(y2))

    return (q11 * (x2 - x) * (y2 - y) +
            q21 * (x - x1) * (y2 - y) +
            q12 * (x2 - x) * (y - y1) +
            q22 * (x - x1) * (y - y1)
           ) / ((x2 - x1) * (y2 - y1) + 0.0)


#TODO: make number_points based on (r,c)
number_points = 18
dco = DetectContours()
dci = DetectCircles()
fh = FindHomography()
points = []

for i in range(0,number_points):
    #if i < 10:
    #    i = str(0) + str(i)
    img = cv2.imread("images/" + sys.argv[1] + "/" + str(i) + ".jpg")
    a = dco.getContours(img)
    #dci.get_circles(img)
    points.append(dco.getCentroids(a))
    #points.append(dci.get)


print points
forwarp = cv2.imread('images/doge.jpg')
height, width, depth = forwarp.shape


# TODO: automate getting the centroids of all the original calibration images
original = [(87, 141), (403, 141), (717, 141), (87, 347), (403, 347), (717, 347)]
original3b0 = [(33, 33), (178, 33), (326, 33), (474, 33), (622, 33), (765, 34),
                (33, 210), (178, 210), (326, 210), (474, 210), (622, 210), (766, 210),
                (33, 390), (178, 390), (326, 390), (474, 390), (622, 390), (766, 390),
                (34, 565), (178, 566), (326, 566), (474, 566), (622, 566), (765, 565)]

original3b = [(30, 30), (182, 30), (334, 30), (486, 30), (638, 30), (789, 30),
            (30, 216), (182, 216), (334, 216), (486, 216), (638, 216), (789, 216),
            (30, 403), (182, 403), (334, 403), (486, 403), (638, 403), (789, 403),
            (30, 589), (182, 589), (334, 589), (486, 589), (638, 589), (789, 589)]

original3c = [(25, 25), (135, 25), (245, 25), (355, 25), (465, 25), (575, 25), (685, 25), (794, 25),
            (25, 139), (135, 139), (245, 139), (355, 139), (465, 139), (575, 139), (685, 139), (794, 139),
            (25, 253), (135, 253), (245, 253), (355, 253), (465, 253), (575, 253), (685, 253), (794, 253),
            (25, 367), (135, 367), (245, 367), (355, 367), (465, 367), (575, 367), (685, 367), (794, 367),
            (25, 481), (135, 481), (245, 481), (355, 481), (465, 481), (575, 481), (685, 481), (794, 481),
            (25, 594), (135, 594), (245, 594), (355, 594), (465, 594), (575, 594), (685, 594), (794, 594)]


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
    if x1 != x2 and y1 != y2 and y2 < original_image.shape[0] and x2 < original_image.shape[1]:
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


def reverse_warp_helper(original_points, cam_points, target, original_image, use_bi_or_wp):
    target_h, target_w, target_d = target.shape

    #transform = fh.sourceToDest(np.array(cam_points)[:,0], np.array(original_points))
    #transform, state = cv2.findHomography(np.array(cam_points)[:,0].astype(float), np.array(original_points).astype(float))
    #transform = cv2.getPerspectiveTransform(np.array(cam_points, np.float32)[:,0], np.array(original_points, np.float32))

    #inverse_transform = np.linalg.inv(transform)
    # OR
    inverse_transform = fh.sourceToDest(np.array(original_points), np.array(cam_points)[:,0])
    #inverse_transform = cv2.getPerspectiveTransform(np.array(original_points, np.float32), np.array(cam_points, np.float32)[:,0])
    #inverse_transform, state = cv2.findHomography(np.array(original_points).astype(float), np.array(cam_points)[:,0].astype(float))



    #TODO: change this from a simple nested loop to apply a function on a single numpy array (faster)
    for y in range(target_h):
        for x in range(target_w):
            # inv transform
            # if point in original box, interpolate color, else point outside, put as black/white?
            # then mask out the black/white outside points and combine the image
            original_location = fh.getDest([x,y], inverse_transform)
            (x0, y0) = original_location[0]
            #check if the original location, according to the homography,  is  within our rectangle of interest
            if y0 >= original_points[0][1] and y0 <= original_points[-1][1] and x0 >= original_points[0][0] and x0 <= original_points[1][0]:
                target[y,x] = interpolate_colour(original_image, (x0,y0))
            else:
                target[y,x] = [0,0,0]



def warp_helper(original_points, cam_points, blank, original_image, use_bi_or_wp):
    #print "ogp: ", original_points

    transform = fh.sourceToDest(np.array(cam_points)[:,0], np.array(original_points))
    transform2,state = cv2.findHomography(np.array(cam_points)[:,0].astype(float), np.array(original_points).astype(float))
    transform3 = cv2.getPerspectiveTransform(np.array(cam_points, np.float32)[:,0], np.array(original_points, np.float32))
    new_points = map(lambda x: x[0], map(lambda x: fh.getDest(x, transform), original_points))
    if use_bi_or_wp == "bi":
        bi_points = []
        for ctr in range(len(new_points)):
            (x,y)= new_points[ctr]
            (x0,y0) = original_points[ctr]
            bi_points.append((x0,y0,np.array([x,y])))

        for y in range(0, height):
        #img[87:403, 141:347]:
            for x in range(0, width):
                if y >= original_points[0][1] and y <= original_points[-1][1] and x >= original_points[0][0] and x <= original_points[1][0]: # 0134
                    #bilinear_interpolation
                    (_x, _y) = map(int, bilinear_interpolation(x, y, bi_points))
                    blank[_y,_x] = original_image[y,x]

    elif use_bi_or_wp == "wp":
        #warpPerspective
        #dst = fh.fix_translation(original_image, transform)
        #out_2 = cv.fromarray(np.zeros((3000,3000,3),np.uint8))
        #out = cv2.warpPerspective(dst[original_points[0][1]:original_points[-1][1],
        #        original_points[0][0]:original_points[1][0]], transform, (600,600))
        #cv2.imshow("out", out)
        #cv2.waitKey(0)
        #warpPerspective
        #out_2 = cv.fromarray(np.zeros((3000,3000,3),np.uint8))
        og = original_image[original_points[0][1]:original_points[-1][1],
                original_points[0][0]:original_points[1][0]]
        cv2.imshow("out", og)
        cv2.waitKey(0)
        out2 = cv2.warpPerspective(original_image[original_points[0][1]:original_points[-1][1],
                original_points[0][0]:original_points[1][0]], transform, (600,600))
        cv2.imshow("out", out2)
        cv2.waitKey(0)
        out2 = cv2.warpPerspective(original_image[original_points[0][1]:original_points[-1][1],
                original_points[0][0]:original_points[1][0]], transform2, (600,600))
        cv2.imshow("out", out2)
        cv2.waitKey(0)
        out2 = cv2.warpPerspective(original_image[original_points[0][1]:original_points[-1][1],
                original_points[0][0]:original_points[1][0]], transform3, (600,600))
        cv2.imshow("out", out2)
        cv2.waitKey(0)

def warp_image(original_points, original_image, cam_points, points_shape, use_bi_or_wp):
    # points_shape: (rows, cols) tuple, describing the layout of dots e.g. 9 dots (3,3) or 12 dots (3,4)
    blank = np.zeros((1200,1200, 3), dtype=np.uint8)
    #this function passes indices to a helper, which will transform that sub-rectangle
    rows = points_shape[0]
    cols = points_shape[1]
    for index in range(len(original_points)-cols-1):
        temp = np.zeros(blank.shape, dtype=np.uint8)
        if index==0 or index+1 % cols != 0:
            print index+cols+1

            original_corners = [original_points[index], original_points[index+1],
                                original_points[index+cols], original_points[index+cols+1]]
            cam_corners = [cam_points[index], cam_points[index+1], cam_points[index+cols], cam_points[index+cols+1]]
            #warp_helper(original_corners, cam_corners, blank, original_image, use_bi_or_wp)
            reverse_warp_helper(original_corners, cam_corners, temp, original_image, "none")
        blank = cv2.add(blank, temp)

    cv2.imwrite(sys.argv[2], blank)
#    cv2.imshow('blank', blank)
#    cv2.waitKey(0)

warp_image(orig18, forwarp, points, (3,6), "bi")

#I_POINTS1:  [(184, 149, array([27, 40, 54], dtype=uint8)), (185, 149, array([32, 41, 54], dtype=uint8)), (184, 149, array([27, 40, 54], dtype=uint8)), (185, 149, array([32, 41, 54], dtype=uint8))]

#BI_POINTS2:  [(87, 141, array([  -4.05636305,  139.37910581])), (403, 141, array([ 339.37195198,  104.17919413])), (87, 347, array([   4.64631623,  403.31791846])), (403, 347, array([ 350.99598779,  434.90636472]))]


#(2)
#
#splice image first?

# def compute_orig_loc():


# print points[:4]
# transform = fh.sourceToDest(np.array([points[0], points[1], points[3], points[4]])[:,0], np.array([original[0], original[1], original[3], original[4]]))
# dst = fh.fix_translation(original_image, transform)
# #out_2 = cv.fromarray(np.zeros((3000,3000,3),np.uint8))
# out = cv2.warpPerspective(dst, transform, (500,500))
# cv2.imshow("out", out)
# cv2.waitKey(0)

#cv.WarpPerspective(cv.fromarray(dst), out_2, cv.fromarray(transform))
#cv.SaveImage("../processed/testing.jpg", out_2) #fh.crop(out_2))
