#from imutils import paths
import numpy as np
#import imutils
import cv2
from operator import itemgetter
from colordetection import ColorDetector

class FindWorldPoseFromPixels:
    def __init__(self, image):
        self.image = image
        self.upperleft = [-0.402280485368,0.427773202467] #this is (x,y) from cam and (y,x) from sawyer
        self.lowerRight = [.236229533989,.848546261491]
        self.CD = ColorDetector(image)
        self.calibrate_camera()
        
        

    def calibrate_camera(self):
        pixelUl,pixelLR = self.CD.getCorners()
        self.fx = (self.upperleft[0]+self.lowerRight[0])/(pixelUl[0]+pixelLR[0])
        self.fy = (self.upperleft[1]+self.lowerRight[1])/(pixelUl[1]+pixelLR[1])

    def calc_pose(self, target):
        return [target[0]*self.fx, target[1]*self.fy]

