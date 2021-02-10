#Author : Harshit Vishwakarma
"""
    Detect Image and output Subsignature encoded in it
"""

import os
import cv2
import numpy as np

def imageToSubSignature(imagePath):
    """
    Read Image from imagePath and Decode v2 SubSignature

    Parameters : 

        imagePath (str): Temporary location of Image to detect

    Return :

        (str) : SubSignature
    """
    currDir = os.getcwd()
    path = currDir+"/Decoding/"+imagePath
    print(path)
    img = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
    #img = cv2.Sobel(img, cv2.CV_8UC1, 1, 0, ksize=3)
    img = cv2.GaussianBlur(img, (5,5), 1)
    can = cv2.Canny(img, 200, 100)
    can = cv2.medianBlur(can, 3)
    res = np.zeros((can.shape), dtype=can.dtype)
    #circles = cv2.HoughCircles(can, cv2.HOUGH_GRADIENT, 1, 1, param1=10, param2=13)
    contours, heirarchy = cv2.findContours(can, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(res, contours, -1, 255, thickness=1)
    cv2.imshow('Image', img)
    cv2.imshow('Filtered', can)
    cv2.imshow('Contour', res)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

imageToSubSignature('Decoding/446300322707631427235.jpg')