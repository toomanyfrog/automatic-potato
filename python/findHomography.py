import cv2
import numpy as np

class FindHomography:
    #corrects for translation in homography
    def fix_translation(self, image, transform):
        height, width = image.shape[:2]
        corners = [[0,0], [width, 0], [height,width], [0, height]]
        new_points = []
        for point in corners:
            new_points.append(self.getDest(point, transform))
        #print new_points
        top_left = new_points[0][0]
        print top_left
        translation = np.float32([[1, 0, -1*top_left[0] ],
                                  [0, 1, -1*top_left[1] ]])

        return cv2.warpAffine(image, translation, (3000,3000))

    def scaleByCoeff(self, point1, point2, point3, point4):
        a = np.array([[point1[0], point2[0], point3[0]], [point1[1], point2[1], point3[1]], [1,1,1]])
        b = np.array([point4[0],point4[1], 1])
        x = np.linalg.solve(a,b) #coefficients
        A = np.array([[x[0]*point1[0], x[1]*point2[0], x[2]*point3[0]],
                     [x[0]*point1[1], x[1]*point2[1], x[2]*point3[1]],
                     x.transpose()])
        return A

    def adjoint(self,A):
        return np.array([[A[1,1]*A[2,2]-A[1,2]*A[2,1], A[0,2]*A[2,1]-A[0,1]*A[2,2], A[0,1]*A[1,2]-A[0,2]*A[1,1]],
                         [A[1,2]*A[2,0]-A[1,0]*A[2,2], A[0,0]*A[2,2]-A[0,2]*A[2,0], A[0,2]*A[1,0]-A[0,0]*A[1,2]],
                         [A[1,0]*A[2,1]-A[1,1]*A[2,0], A[0,1]*A[2,0]-A[0,0]*A[2,1], A[0,0]*A[1,1]-A[0,1]*A[1,0]]])

    #get transform
    def sourceToDest(self,source,dest):
        basisToSource = self.scaleByCoeff(source[0], source[1], source[2], source[3])
        sourceToBasis = self.adjoint(basisToSource)
        basisToDest = self.scaleByCoeff(dest[0],dest[1],dest[2],dest[3])
        a = np.dot(basisToDest, sourceToBasis)
        print "a", a
        return a

    # applies transform
    def getDest(self, source, transform):
        s = np.array([source[0], source[1], 1]) #homogeneous
        t = np.dot(transform, s)
        return np.array([[t[0]/t[2], t[1]/t[2]], t[2]])

    def crop(self,img):
        gray = cv2.cvtColor(np.array(img),cv2.COLOR_BGR2GRAY)
        _,thresh = cv2.threshold(gray,1,255,cv2.THRESH_BINARY)
        #Now find contours in it. There will be only one object, so find bounding rectangle for it.

        contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnt = contours[0]
        x,y,w,h = cv2.boundingRect(cnt)
        #Now crop the image, and save it into another file.

        crop = img[y:y+h+10,x:x+w+10]
        return crop
