import numpy as np
import numpy.linalg as la
import cv2
import cv2.cv as cv
from colourmatch import ColourMatch
from findHomography import FindHomography
import sys
import os

# look at the photo
# identify coloured circles
# find pattern (red blue green magenta)
# use contours to find a centroid
# use the centroids to compute a homography

# ==========================================

# find cyan circles - these are the ends of the projection

fh = FindHomography()

def calibrate(cm, original_image, original_centers, filepath, filename):
    img = cv2.imread(filepath)
    print "cwd: ", os.getcwd() + "/" + filepath
    print img
    sys.stdout.flush()

    contours = []
    centroids = []
    for colour_index in range(0,4):
        mask = cm.threshold_colour(img, colour_index)
        blurred = cv2.GaussianBlur(mask,(49,49),0)
        #cv2.imshow('b', blurred)
        #cv2.waitKey(0)
        #cm.getCircles(a)
        contours.append(cm.get_contours(blurred))

    print "ctrs: ", contours
    sys.stdout.flush()


    for c in contours:
        # compute the center of the contour
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        centroids.append([cX, cY])

        print "centroids: ", centroids
        sys.stdout.flush()


        # draw the contour and center of the shape on the image
        cv2.drawContours(img, [c], -1, (0, 255, 0), 2)
        cv2.circle(img, (cX, cY), 7, (255, 255, 255), -1)
        cv2.putText(img, "center", (cX - 20, cY - 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # show the image
        cv2.imshow("Image", img)
        cv2.waitKey(0)

    transform = fh.sourceToDest(centroids, original_centers)
    dst = fh.fix_translation(original_image, transform)
    out_2 = cv.fromarray(np.zeros((1000,1000,3),np.uint8))
    cv.WarpPerspective(cv.fromarray(dst), out_2, cv.fromarray(transform))
    #cv.ShowImage("test", out_2)
    cv.SaveImage("processed/" + filename + ".jpg", fh.crop(out_2))
    #cv2.imwrite(filename+".jpg", crop(out_2))
    print "completed"
    sys.stdout.flush()
    # cv2.warpPerspective(original_image, transform, dsize[, dst[, flags[, borderMode[, borderValue]]]])
    # for x in range(4):
    #     new_p getDest(original_centers[x], transform)


def main():

    data = "this began life in python"
    print(data)
    sys.stdout.flush()
    filepath = sys.argv[1] #read_in()
    filename = sys.argv[2]
    print filepath, filename
    cm = ColourMatch()
    original_image = cv2.imread("python/test2.jpg")
    cv2.imshow("-", original_image)
    cv2.waitKey(0)
    original_centers = [[436, 101], [110, 251], [429, 247], [266, 98]]
    calibrate(cm, original_image, original_centers, filepath, filename)


if __name__ == '__main__':
    main()
