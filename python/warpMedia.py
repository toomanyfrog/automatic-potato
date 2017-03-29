import os
import sys
import cv2
from getUserRect import *
from detectPattern import DetectContours
from computeMapping import *

# python warpMedia.py [rows] [cols] [mediaId] [x] [y] [w] [h]

number_points = rows * cols

alldot = cv2.imread(os.getcwd() + "/user/all/" + sys.argv[3])
# make image for userpt_locations
blank = np.zeros(cv2.imread(os.getcwd() + "/user/camera/" + sys.argv[3] + "/0").shape)

points = read_dots(os.getcwd() + "/user/camera/" + sys.argv[3]) #camera points
forwarp = cv2.imread(os.getcwd() + "/user/uploads/" + sys.argv[3]) # + ".jpg") #media for warp
height, width, depth = forwarp.shape
userpt_locations = get_dots("images/user/3e18user.jpg")
warp_image(orig18, forwarp, (3,6), userpt_locations, map(lambda x:x[0], points))
