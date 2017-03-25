import cv2
import numpy as np

# remember to generate the dot image based on their desired projected image


class CalibrationPatternGenerator:
    dot_radius = 20

    def createRegular(self, imgsize, dotshape, pathtowrite):
        height, width = imgsize
        rows, cols = dotshape
        if rows <= 1 or cols <= 1:
            raise ValueError("Not enough dots to generate a meaningful calibration pattern.")
        # imgsize : (h, w) e.g. (400, 600)
        # dotshape: (h, w) e.g. (2, 3), (4, 6) - determines the detail of dot
        # temp = np.zeros((height, width, 3), dtype=np.uint8)

        dot_index = 0
        for r in range(rows):
            for c in range(cols):
                temp = np.zeros((height+20, width+20, 3), dtype=np.uint8)
                y = r * (height - 2*self.dot_radius) / (rows -1) + self.dot_radius
                x = c * (width  - 2*self.dot_radius) / (cols -1) + self.dot_radius
                cv2.circle(temp, (x+10,y+10), self.dot_radius, [255,255,255], -1)
                cv2.imwrite(pathtowrite + str(dot_index) + ".jpg", temp)
                dot_index += 1
        # cv2.imwrite(pathtowrite + "a.jpg", temp)




    # def createSpecific(): for adaptive calibration


cpg = CalibrationPatternGenerator()
cpg.createRegular((600,800),(5,7), "images/35pts/")
