import os
import cv2

# TODO: automate getting the folder
path =  os.getcwd() + "/3bp2a/"
filenames = os.listdir(path)

for filename in filenames:
    print filename
    print path+filename
    image = cv2.imread(path+filename)
    h,w,d = image.shape
    cropped = image[:, 250:w-1]

    cv2.imwrite(os.getcwd()+ "/3bp2b/"+filename, cropped)
