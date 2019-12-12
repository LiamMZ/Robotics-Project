#from imutils import paths
import numpy as np
#import imutils
import cv2
from operator import itemgetter

class FindWorldPoseFromPixels:
    def __init__(self, image):
        self.image = image
        self.upperleft = [0,0]
        self.lowerRight = [.75,.75]
        self.calibrate_camera()

    
    def find_corner(self):
        img = self.image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = np.float32(gray)
        dst = cv2.cornerHarris(gray,5,3,0.04)
        ret, dst = cv2.threshold(dst,0.1*dst.max(),255,0) #sets corners to white sets everything else to black
        dst = np.uint8(dst)
        img[dst>0.1*dst.max()]=[0,0,255]
        cv2.imshow('image', img)
        ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
        corners = cv2.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)
        corners = sorted(corners, key=itemgetter(0))
        sumCrn = [x[0]+x[1] for x in corners]
        indexMin = sumCrn.index(min(sumCrn))
        indexMax = sumCrn.index(max(sumCrn))
        cv2.waitKey(0)
        cv2.destroyAllWindows
        return corners[indexMin], corners[indexMax]
        

    def calibrate_camera(self):
        pixelUl,pixelLR = self.find_corner()
        self.fx = (self.upperleft[0]+self.lowerRight[0])/(pixelUl[0]+pixelLR[0])
        self.fy = (self.upperleft[1]+self.lowerRight[1])/(pixelUl[1]+pixelLR[1])

    def calc_pose(self, target):
        return [target[0]*self.fx, target[1]*self.fy]



# img = cv2.imread('table.jpeg')
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# gray = np.float32(gray)
# dst = cv2.cornerHarris(gray,5,3,0.03)
# ret, dst = cv2.threshold(dst,0.1*dst.max(),255,0) #sets corners to white sets everything else to black
# dst = np.uint8(dst) 
# ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
# criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
# corners = cv2.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)
# corners = sorted(corners, key=itemgetter(1))
# for i in range(1, len(corners)):
#     print(corners[i])
# img[dst>0.1*dst.max()]=[0,0,255]
# cv2.imshow('image', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows