# generate the dot-dot mappings
import math
from util import *
import cv2
import sys
import os
from getUserRect import *
from scipy.spatial.distance import cdist
from findHomography import FindHomography

def closest_dot(pt, pts):
    return pts[cdist(pts, np.asarray([pt])).argmin()]
img = cv2.imread(os.getcwd() + "/user/camera/" + sys.argv[3] + "/0.jpg")


# 1 | 2
# --+--
# 3 | 4
def find_quad(pt, pts): #indices
    img0 = img.copy()
    quad1_pts = np.asarray([p for p in pts if (p[0]<=pt[0] and p[1]>pt[1])]) # x' < x, y' > y
    quad2_pts = np.asarray([p for p in pts if (p[0]>pt[0] and p[1]>pt[1])]) # x' > x, y' > y
    quad3_pts = np.asarray([p for p in pts if (p[0]<=pt[0] and p[1]<=pt[1])]) # x' < x, y' < y
    quad4_pts = np.asarray([p for p in pts if (p[0]>pt[0] and p[1]<=pt[1])])# x' > x, y' < y
    cv2.circle(img0, (pt[0], pt[1]), 3, [255,255,255], -1)
    for pt1 in quad1_pts:
        cv2.circle(img0, (pt1[0], pt1[1]), 3, [0,255,0], -1)
    for pt2 in quad2_pts:
        cv2.circle(img0, (pt2[0], pt2[1]), 3, [255,0,0], -1)
    for pt3 in quad3_pts:
        cv2.circle(img0, (pt3[0], pt3[1]), 3, [0,255,255], -1)
    for pt4 in quad4_pts:
        cv2.circle(img0, (pt4[0], pt4[1]), 3, [255,255,0], -1)
    cv2.imshow('img0', img0)
    cv2.waitKey(0)
    lpts = pts.tolist()
    ans = [closest_dot(pt, quad1_pts), closest_dot(pt, quad2_pts), closest_dot(pt, quad3_pts), closest_dot(pt, quad4_pts)]
    return [lpts.index(ans[0].tolist()), lpts.index(ans[1].tolist()), lpts.index(ans[2].tolist()), lpts.index(ans[3].tolist())]


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


def reverse_warp_helper(original_points, warp_pts, target, forwarp):

    target_h, target_w, target_d = target.shape
    inverse_transform = fh.sourceToDest(np.array(warp_pts), np.array(original_points))

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
                target[y,x] = interpolate_colour(forwarp, (x0,y0))
            else:
                target[y,x] = [0,0,0]

def warp_image(original_points, forwarp, points_shape, warp_pts, path):
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
            warp_corners = [warp_pts[index], warp_pts[index+1], warp_pts[index+cols], warp_pts[index+cols+1]]

            reverse_warp_helper(original_corners, warp_corners, temp, forwarp)
            # for corner in warp_corners:
            #     cv2.circle(temp, (int(corner[0]), int(corner[1])), 3, [0,0,255], -1)
            # cv2.imshow("temp", temp)
            # cv2.waitKey(0)
        blank = cv2.add(blank, temp)

    cv2.imwrite(path, blank)


fh = FindHomography()
rows = int(sys.argv[1])
cols = int(sys.argv[2])
x = int(float(sys.argv[4]))
y = int(float(sys.argv[5]))
w = float(sys.argv[6])
h = float(sys.argv[7])

number_points = rows * cols
forwarp = cv2.imread(os.getcwd() + "/user/uploads/" + sys.argv[3]) # + ".jpg") #media for warp

#   projection dots in the camera image
cam_img_pts  = map(lambda x: x[0], read_dots(os.getcwd() + "/user/camera/" + sys.argv[3], number_points)) #camera points
#   dot location in the calibration images
orig_pts     = map(lambda x: x[0], read_dots(os.getcwd() + "/user/generated/" + sys.argv[3], number_points))
#   the dot locations in the user-defined rectangle
user_def_pts = map(lambda x: x[0], read_user_dots(os.getcwd() + "/user/generated/" + sys.argv[3], number_points, x,y,w,h,
                    cv2.imread(os.getcwd() + "/user/camera/" + sys.argv[3] + "/0.jpg").shape))
cam_img_pts  = np.asarray(cam_img_pts)
orig_pts     = np.asarray(orig_pts)
user_def_pts = np.asarray(user_def_pts)

warp_coords = []
# warp_coords contains all the coordinates of the dots in the pre-warp image

for pt in user_def_pts:
    img2 = img.copy()
    lpt = pt.tolist()
    lcam = cam_img_pts.tolist()
    if lpt in lcam:
        warp_coords.append(orig_pts[lcam.index(lpt)])
    else:
        (a,b,c,d) = find_quad(pt, cam_img_pts)
        print a,b,c,d
        cam_corners = [cam_img_pts[a], cam_img_pts[b], cam_img_pts[c], cam_img_pts[d]]
        for (cx, cy) in cam_corners:
           cv2.circle(img2, (int(cx), int(cy)), 3, [0,255,0], -1)
        cv2.imshow("img", img2)
        cv2.waitKey(0)
        orig_corners = [orig_pts[a], orig_pts[b], orig_pts[c], orig_pts[d]]
        transform = fh.sourceToDest(np.array(cam_corners), np.array(orig_corners))
        print fh.getDest(pt, transform)[0]
        warp_coords.append(fh.getDest(pt, transform)[0])

print warp_coords
for (x,y) in warp_coords:
    cv2.circle(img, (int(x), int(y)), 3, [0,0,255], -1)
    cv2.imshow("img", img)
    cv2.waitKey(0)

warp_image(orig_pts, forwarp, (rows, cols), warp_coords, os.getcwd() + "/user/final/" + sys.argv[3]+".jpg")
