import cv2
import imutils

bg = cv2.imread('cd/cd28/0.jpg')
a = cv2.imread('cd/cd28/1.jpg')
b = cv2.imread('cd/cd28/10.jpg')
a1 = cv2.absdiff(bg, a)
b1 = cv2.absdiff(bg, b)

gray = cv2.cvtColor(a1, cv2.COLOR_BGR2GRAY)
# TODO: fix the threshold to be based on overall image - relative brightness instead of absolute
(thresh, im_bw) = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY) # | cv2.THRESH_OTSU)
# cv2.imshow("b", im_bw)
# cv2.waitKey(0)
#im_bw = 255 - im_bw
#blurred = cv2.GaussianBlur(im_bw,(3,3),0)
blurred = cv2.medianBlur(im_bw,11)

cv2.imshow('blur', blurred)
cv2.waitKey(0)
#cnts = cv2.findContours(im_bw.copy(), cv2.RETR_EXTERNAL,
#    cv2.CHAIN_APPROX_SIMPLE)
#    cnts, hierarchy = cv2.findContours(blurred, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

cnts = cv2.findContours(blurred, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

# show the image
for cnt in cnts:
    cv2.drawContours(a1, cnt, -1, (0, 255, 0), 2)
    #
    cv2.imshow("Image", a1)
    cv2.waitKey(0)
