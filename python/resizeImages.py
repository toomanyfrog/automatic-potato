import os
import cv2

# TODO: automate getting the folder
path =  os.getcwd() + "/3bp2/"
filenames = os.listdir(path)

for filename in filenames:
    cv2.imwrite(path+filename, cv2.resize(cv2.imread(path+filename),None,fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC))
