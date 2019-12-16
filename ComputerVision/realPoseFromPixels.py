#from imutils import paths
import numpy as np
#import imutils
import cv2
from operator import itemgetter
from colordetection import ColorDetector

class FindWorldPoseFromPixels:
    def __init__(self, image):
        self.image = image
        self.upperleft = [-0.454196989865,0.328892665195] #this is (x,y) from cam and (y,x) from sawyer
        self.lowerRight = [0.227441122039,.752779534673]
        self.CD = ColorDetector(image)
        self.calibrate_camera()
        
        

    def calibrate_camera(self):
        pixelUl,pixelLR = self.CD.getCorners()
        self.fx = (self.lowerRight[0]-self.upperleft[0])/(pixelLR[0]-pixelUl[0])
        self.fy = (self.lowerRight[1]-self.upperleft[1])/(pixelLR[1]-pixelUl[1])

    def calc_pose(self, target):
        return [(target[0]*self.fx)-self.upperleft[0], (target[1]*self.fy)-self.upperleft[1]]

