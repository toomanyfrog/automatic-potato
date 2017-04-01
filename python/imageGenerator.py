import cv2
import numpy as np

# remember to generate the dot image based on their desired projected image


class CalibrationPatternGenerator:
    # TODO: make smaller dots
    dot_radius = 10

    def __init__(self, rows, cols, imgpath, folderpath, allpath):
        self.dotshape = (rows, cols)
        self.imgsize = cv2.imread(imgpath).shape
        self.pathtowrite = folderpath

    def createRegular(self):
        height, width, depth = map(int, self.imgsize)
        rows, cols = map(int, self.dotshape)
        if rows <= 1 or cols <= 1:
            raise ValueError("Not enough dots to generate a meaningful calibration pattern.")
        # imgsize : (h, w) e.g. (400, 600)
        # dotshape: (h, w) e.g. (2, 3), (4, 6) - determines the detail of dot
        #blank = np.zeros((self.dot_radius*2 + height, self.dot_radius*2 + width, 3), dtype=np.uint8)

        temp = np.zeros((self.dot_radius*2 + height, self.dot_radius*2 + width, 3), dtype=np.uint8)
        cv2.imwrite(self.pathtowrite + "/0.jpg", temp)
        dot_index = 1
        for r in range(rows):
            for c in range(cols):
                temp = np.zeros((self.dot_radius*2 + height, self.dot_radius*2 + width, 3), dtype=np.uint8)
                y = r * (height - 2*self.dot_radius) / (rows -1) + self.dot_radius
                x = c * (width  - 2*self.dot_radius) / (cols -1) + self.dot_radius
                cv2.circle(temp, (x + self.dot_radius, y + self.dot_radius), self.dot_radius, [255,255,255], -1)
                cv2.imwrite(self.pathtowrite + "/" + str(dot_index) + ".jpg", temp)
                dot_index += 1
                #blank = cv2.add(blank, temp)

    ##    cv2.imwrite(self.pathforall + ".jpg", blank)




    # def createSpecific(): for adaptive calibration
