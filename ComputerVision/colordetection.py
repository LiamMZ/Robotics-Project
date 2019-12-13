import pdb
import pickle
import random
import copy
import cv2 # You may have to "pip install opencv-contrib-python" to install this
import numpy as np # You may have to "pip install numpy" to install thi
from operator import itemgetter

class ColorDetector():
    def __init__(self, img):
        self.image = img
        self.color_ranges = [[[170,39,39], [255,140,120]]]

    def check_if_color_in_range(self, bgr_tuple):
        for entry in self.color_ranges:
            lower, upper = entry[0], entry[1]
            in_range = True
            for i in range(len(bgr_tuple)):
                if bgr_tuple[i] < lower[i] or bgr_tuple[i] > upper[i]:
                    in_range = False
                    break
            if in_range: return True
        return False
    
    def do_color_filtering(self):
        # Color Filtering
        img_height = self.image.shape[0]
        img_width = self.image.shape[1]

        # Create a matrix of dimensions [height, width] using numpy
        mask = np.zeros([img_height, img_width]) # Index mask as [height, width] (e.g.,: mask[y,x])

        # TODO: Iterate through each pixel (x,y) coordinate of the image, 
        #       checking if its color is in a range we've specified using check_if_color_in_range
        # TIP: You'll need to index into 'mask' using [y,x] instead of [x,y] as you may be
        #      more familiar with, due to how the matrices are stored
        for y in range(img_height):
            for x in range(img_width):
                if self.check_if_color_in_range(self.image[y][x]):
                    mask[y,x] = 1

        return mask

    def expand_nr(self, img_mask, cur_coord):
        coordinates_in_blob = []
        coordinate_list = [cur_coord] # List of all coordinates to try expanding to
        while len(coordinate_list) > 0:
            cur_coordinate = coordinate_list.pop() # Take the first coordinate in the list and perform 'expand' on it
            # TODO: Check to make sure cur_coordinate is in bounds, otherwise 'continue'
            # TODO: Check to see if the value is 0, if so, 'continue'
            if  (cur_coordinate[0]<0 or cur_coordinate[0]>img_mask.shape[0]-1) or (cur_coordinate[1]<0 or cur_coordinate[1]>img_mask.shape[1]-1) or img_mask[cur_coordinate[0], cur_coordinate[1]]==0:
                continue

            # TODO: Set image mask at this coordinate to 0
            # TODO: Add this coordinate to 'coordinates_in_blob'
            img_mask[cur_coordinate[0], cur_coordinate[1]]=0
            coordinates_in_blob.append(cur_coordinate)
            # TODO: Add all neighboring coordinates (above, below, left, right) to coordinate_list to expand to them
            coordinate_list.append([cur_coordinate[0]-1, cur_coordinate[1]])
            coordinate_list.append([cur_coordinate[0]+1, cur_coordinate[1]])
            coordinate_list.append([cur_coordinate[0], cur_coordinate[1]-1])
            coordinate_list.append([cur_coordinate[0], cur_coordinate[1]+1])
        return coordinates_in_blob

    def get_blobs(self, img_mask):
        img_mask_height = img_mask.shape[0]
        img_mask_width = img_mask.shape[1]
        local_mask = copy.copy(img_mask)
        blobs_list = []
        for y in range(img_mask_height):
            for x in range(img_mask_width):
                if local_mask[y,x]==1:
                    blobs_list.append(self.expand_nr(local_mask,[y,x]))

        return blobs_list
    
    def get_blob_centroids(self, blobs_list):
        
        object_positions_list = []

        # TODO: Implement blob centroid calculation
        for blob in blobs_list:
            ys = [x[0] for x in blob]
            xs = [x[1] for x in blob]
            xave = sum(xs)/len(xs)
            yave = sum(ys)/len(ys)
            object_positions_list.append([yave,xave])
        return object_positions_list

    def getCorners(self):
        img_mask = self.do_color_filtering()
        blobs = self.get_blobs(img_mask)
        object_positions_list = self.get_blob_centroids(blobs)

        posList = []
        for obj_pos in object_positions_list:
            posList.append([obj_pos[1], obj_pos[0]])
        sumCrn = [x[0]+x[1] for x in posList]
        minIndex = sumCrn.index(min(sumCrn))
        maxIndex = sumCrn.index(max(sumCrn))
        return posList[minIndex], posList[maxIndex]