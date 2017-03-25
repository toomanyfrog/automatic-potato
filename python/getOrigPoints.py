import cv2
import numpy as np
import sys
from detectPattern import DetectContours

number_points = 35
dco = DetectContours()
points = []

for i in range(0,number_points):
    #if i < 10:
    #    i = str(0) + str(i)
    img = cv2.imread("images/" + sys.argv[1] + "/" + str(i) + ".jpg")
    a = dco.getContours(img)
    #dci.get_circles(img)
    points.append(dco.getCentroids(a))

print map(lambda x: x[0], points)
