import os
import cv2
import numpy as np

# TODO: automate getting the folder
path =  os.getcwd() + "/cd/cd28/"
filenames = os.listdir(path)

for filename in filenames:
   cv2.imwrite(path+filename, cv2.resize(cv2.imread(path+filename),None,fx=0.25, fy=0.25, interpolation = cv2.INTER_CUBIC))

# shape = (560, 996, 3)
# for i in range(18):
#     img = cv2.imread(os.getcwd() + "/images/18pts/"+str(i)+".jpg")
#     cv2.imshow("i", img)
#     cv2.waitKey(0)
#     im = cv2.resize(img, None,fx=0.45, fy=0.45, interpolation = cv2.INTER_CUBIC)
#     blank = np.zeros(shape)
#     blank[120:399, 280:649] = im
#     cv2.imwrite(os.getcwd() + "/images/3e18/"+str(i)+".jpg", blank)
