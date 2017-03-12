import numpy as np
import numpy.linalg as la
import cv2
import cv2.cv as cv
import imutils

class ColourMatch:
    low_lower_red = np.array([0,100,100])
    low_upper_red = np.array([10,255,255])
    hi_lower_red = np.array([170,100,100])
    hi_upper_red = np.array([180,255,255])

    lower_blue = np.array([100,100,100])
    upper_blue = np.array([130,255,255])

    lower_pink = np.array([133, 100, 100])
    upper_pink = np.array([163, 255, 255])

    lower_green = np.array([45, 100, 100])
    upper_green = np.array([75, 255, 255])

    lowclrs = [[low_lower_red, low_upper_red],[lower_blue,upper_blue],[lower_pink,upper_pink],[lower_green,upper_green]]
    hiclrs = [[hi_lower_red, hi_upper_red]]


    def threshold_colour(self, img, clr):
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # lower mask (0-10)

        mask0 = cv2.inRange(img_hsv, self.lowclrs[clr][0], self.lowclrs[clr][1])
        mask = mask0
        # upper mask (170-180)
        if clr == 0:
            mask1 = cv2.inRange(img_hsv, self.hiclrs[clr][0], self.hiclrs[clr][1])
            # join my masks
            mask = mask0+mask1

        # # set my output img to zero everywhere except my mask
        # output_img = img.copy()
        # output_img[np.where(mask==0)] = 1
        # output_img[np.where(mask==1)] = 0


        #mask = 255 - mask
        #return cv2.cvtColor(output_img, cv.CV_BGR2GRAY)
        cv2.imshow('mask.jpg', mask)
        cv2.waitKey(0)
        return mask

    def get_contours(self, image): #returns centroid of contour (should only have one)
        # find contours in the thresholded image
        cnts = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL,
        	cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        # loop over the contours and show the centroids
        # for c in cnts:
        # 	# compute the center of the contour
        # 	M = cv2.moments(c)
        # 	cX = int(M["m10"] / M["m00"])
        # 	cY = int(M["m01"] / M["m00"])
        #
        # 	# draw the contour and center of the shape on the image
        # 	cv2.drawContours(self.img, [c], -1, (0, 255, 0), 2)
        # 	cv2.circle(self.img, (cX, cY), 7, (255, 255, 255), -1)
        # 	cv2.putText(self.img, "center", (cX - 20, cY - 20),
        # 		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        #
        # 	# show the image
        # 	#cv2.imshow("Image", self.img)
        # 	#cv2.waitKey(0)
        # only returning the centroid of the first contour
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        return cnts[0]

    def get_circles(self, image):
        output = image.copy()
        #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # detect circles in the image
    #    circles = cv2.HoughCircles(image, cv2.cv.CV_HOUGH_GRADIENT, 2, 5)
        circles = cv2.HoughCircles(image, cv2.cv.CV_HOUGH_GRADIENT, 2,5,100,100,1,1000)# 1, 1, 200, 100)

        print 'hi'
        # ensure at least some circles were found
        if circles is not None:
            print 'hi2'
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")

            # # loop over the (x, y) coordinates and radius of the circles
            # for (x, y, r) in circles:
            # 	# draw the circle in the output image, then draw a rectangle
            # 	# corresponding to the center of the circle
            # 	cv2.circle(output, (x, y), r, (0, 255, 0), 4)
            # 	cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            #
            # # show the output image
            # # cv2.imshow("output", np.hstack([image, output]))
            # # cv2.waitKey(0)
        return circles[0]
