import os
import cv2
import imutils

# TODO: automate getting the folder
path =  os.getcwd() + "/images/3d18s/"
filenames = os.listdir(path)

for filename in filenames:
    print filename
    print path+filename
    image = cv2.imread(path+filename)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     (thresh, im_bw) = cv2.threshold(gray, 55, 255, cv2.THRESH_BINARY) # | cv2.THRESH_OTSU)
#
#     cnts = cv2.findContours(im_bw, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
#     cnts = cnts[0] if imutils.is_cv2() else cnts[1]
#     cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
#
#     # show the image
#     cv2.drawContours(image, [cnts[0]], -1, (0, 255, 0), 2)
# #
#     cv2.imshow("Image", image)
#     cv2.waitKey(0)
# TODO : find a way to automate the cropping?

    h,w,d = image.shape
    cropped = image[:, 50:]

    cv2.imwrite(os.getcwd()+ "/images/3d18s1/"+filename, cropped)
