#from imutils import paths
import numpy as np
#import imutils
import cv2
from operator import itemgetter
from colordetection import ColorDetector

class FindWorldPoseFromPixels:
    def __init__(self, image):
        self.image = image
        self.upperleft = [-0.406520238446,0.314348683295] #this is (x,y) from cam and (y,x) from sawyer
        self.lowerRight = [0.289579707007,0.741919848134]
        # self.upperleft1D = [-0.239140019919,0.650653669801] #this is (x,y) from cam and (y,x) from sawyer
        # self.lowerRight1D = [0.178982502624,.739727213783]
        self.CD = ColorDetector(image)
        self.calibrate_camera()
        
        

    def calibrate_camera(self):
        self.pixelUl,self.pixelLR = self.CD.getCorners()
        self.fx = (self.lowerRight[0]-self.upperleft[0])/(self.pixelLR[0]-self.pixelUl[0])
        self.fy = (self.lowerRight[1]-self.upperleft[1])/(self.pixelLR[1]-self.pixelUl[1])
        # self.fx1D = (self.lowerRight1D[0]-self.upperleft1D[0])/(pixelLR[0]-pixelUl[0])
        

    def calc_pose(self, target):
        return [((target[0]-self.pixelUl[0])*self.fx)+self.upperleft[0]+.075, ((target[1]-self.pixelUl[1])*self.fy)+self.upperleft[1]+.03]

