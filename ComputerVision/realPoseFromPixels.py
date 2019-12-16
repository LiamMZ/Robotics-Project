#from imutils import paths
import numpy as np
#import imutils
import cv2
from operator import itemgetter
from colordetection import ColorDetector

class FindWorldPoseFromPixels:
    def __init__(self, image):
        self.image = image
        # self.upperleft = [-0.437781832879,0.348674242753] #this is (x,y) from cam and (y,x) from sawyer
        # self.lowerRight = [.258586520435,.739727213783]
        self.upperleft1D = [-0.239140019919,0.650653669801] #this is (x,y) from cam and (y,x) from sawyer
        self.lowerRight1D = [0.178982502624,.739727213783]
        self.CD = ColorDetector(image)
        self.calibrate_camera()
        
        

    def calibrate_camera(self):
        pixelUl,pixelLR = self.CD.getCorners()
        # self.fx = (self.lowerRight[0]-self.upperleft[0])/(pixelLR[0]-pixelUl[0])
        # self.fy = (self.lowerRight[1]-self.upperleft[1])/(pixelLR[1]-pixelUl[1])
        self.fx1D = (self.lowerRight1D[0]-self.upperleft1D[0])/(pixelLR[0]-pixelUl[0])
        

    def calc_pose(self, target):
        return [(target[0]*self.fx1D)+self.upperleft1D[0], 0.6936975683]

