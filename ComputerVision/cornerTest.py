import numpy as np
import cv2
from operator import itemgetter
from colordetection import ColorDetector

def find_corner(image):
        img = image
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

def main():
    src = 0
    cap = cv2.VideoCapture(src)
    _, frame = cap.read()
    #find_corner(frame)
    cd = ColorDetector(frame)
    ul,lr = cd.getCorners()
    frame[ul[1]][ul[0]] = [0,0,255]
    frame [lr[1]][lr[0]] = [0,0,255]
    print(ul,lr)
    cv2.imshow('frame',frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows
    cap.release()

if __name__=="__main__":
    main()