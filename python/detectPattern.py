import numpy as np
import cv2
import cv2.cv as cv
import imutils

#threshold image via brightness - this will work assuming the projections are used in a dark place
#in a bright place, projections contrast is affected as well, so what method can be used for these scenarios?

#then, 2 methods - 1 is finding contours and 2nd is Hough circles. So far, contours seems to be more robust, but
#sometimes, false positives.

# MOMENTS IS NOT WORKING ??!?!?!?!?



class DetectContours:
    def getCentroids(self, contours):
        centroids = []
        for c in contours:
            #compute the center of the contour
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            centroids.append((cX,cY))

        return centroids

    def getContours(self, img): #returns centroid of contour (should only have one)
        # find contours in the thresholded image

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # TODO: fix the threshold to be based on overall image - relative brightness instead of absolute
        (thresh, im_bw) = cv2.threshold(gray, 145, 255, cv2.THRESH_BINARY) # | cv2.THRESH_OTSU)
        # cv2.imshow("b", im_bw)
        # cv2.waitKey(0)
        #im_bw = 255 - im_bw
        blurred = cv2.GaussianBlur(im_bw,(19,19),0)


        #cnts = cv2.findContours(im_bw.copy(), cv2.RETR_EXTERNAL,
        #    cv2.CHAIN_APPROX_SIMPLE)
    #    cnts, hierarchy = cv2.findContours(blurred, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        cnts = cv2.findContours(blurred, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

        # show the image
        cv2.drawContours(img, [cnts[0]], -1, (0, 255, 0), 2)
#
        cv2.imshow("Image", img)
        cv2.waitKey(0)
        return [cnts[0]]


class DetectCircles:
    def getAvgCenter(self, circles):
        x_sum = 0
        y_sum = 0
        for (x,y,r) in circles:
            x_sum += x
            y_sum += y
        x_sum = x_sum / len(circles)
        y_sum = y_sum / len(circles)
        return (x_sum, y_sum)

    def getCircles(self, image):
        output = image.copy()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray,(9,9),0)

        # detect circles in the image
        circles = cv2.HoughCircles(blurred, cv2.cv.CV_HOUGH_GRADIENT, 2, 3)
        #circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 2,5,100,100,1,400)# 1, 1, 200, 100)
    #    circles = cv2.HoughCircles(gray,cv2.cv.CV_HOUGH_GRADIENT,1,20,
            #                    param1=50,param2=30,minRadius=0,maxRadius=0)
        # ensure at least some circles were found
        if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")

            # loop over the (x, y) coordinates and radius of the circles
            for (x, y, r) in circles:
                # draw the circle in the output image, then draw a rectangle
                # corresponding to the center of the circle
                cv2.circle(output, (x, y), r, (0, 255, 0), 4)
                cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

            # show the output image
            # cv2.imshow("b", output) # np.hstack([image, output]))
            # cv2.waitKey(0)
        return circles

#
# for i in range(1,7):
#     img = cv2.imread("1/a" + str(i) + ".jpg")
#     dco = DetectContours()
#     #dci = DetectCircles()
#     cnts = dco.get_contours(img)
#     #dci.get_circles(img)
#     print dco.get_centroids(cnts)
