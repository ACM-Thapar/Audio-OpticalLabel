#Author: Harshit
"""
Bind the logo and base_template together.
"""
import cv2 as cv
import os
import math
import numpy as np

def bindCompanyLogo(logoDir, boxheight, saveDst, WHratio=8):
    """
    Bind the Company logo over the base Template.

    Parameters:

        logoDir (str): Company Logo location/path.

        boxHeight (float): Template Height.

        saveDst (str): File save location.

        WHratio (float): Width to Height Ratio of Template.

    Return:

        (None)
    """
    currdir = os.getcwd()
    tempDir = currdir + "/v2/template/v2_base.png"
    temp = cv.imread(tempDir, cv.IMREAD_UNCHANGED)
    logo = cv.imread(logoDir, cv.IMREAD_UNCHANGED)


    #resize logo
    finalDim = np.ones((int(boxheight-boxheight/8), int(boxheight - boxheight/8)), dtype=logo.dtype)
    finalDim = cv.resize(logo, (int(finalDim.shape[0]), int(finalDim.shape[1])) )

    #circle and threshold over trans layer
    mask = np.zeros((finalDim.shape[0], finalDim.shape[1]), dtype=logo.dtype)
    mask = cv.ellipse(mask, (int(finalDim.shape[0]/2), int(finalDim.shape[1]/2)), (int(finalDim.shape[0]/2), int(finalDim.shape[1]/2)), 0, 0, 360, (255), -1)    

    if len(finalDim.shape) == 3 and (finalDim.shape[2] == 4):
        (b, g, r, a) = cv.split(finalDim)
        b = cv.bitwise_and(b, mask)
        g = cv.bitwise_and(g, mask)
        r = cv.bitwise_and(r, mask)
        a = cv.bitwise_and(a, mask)
        finalDim = cv.merge((b, g, r, a))
    
    else:
        (b, g, r) = cv.split(finalDim)
        b = cv.bitwise_and(b, mask)
        g = cv.bitwise_and(g, mask)
        r = cv.bitwise_and(r, mask)        
        finalDim = cv.merge((b, g, r))

    

    #overlap logo and template
    xstart = int(boxheight/16)
    xstop = int(boxheight - boxheight/16)
    ystart = int(boxheight/16)
    ystop = int(boxheight - boxheight/16)

    if len(finalDim.shape) == 3 and (finalDim.shape[2] == 4):
        temp[ystart:ystop, xstart:xstop, 0] = b
        temp[ystart:ystop, xstart:xstop, 1] = g
        temp[ystart:ystop, xstart:xstop, 2] = r
        
    else:
        temp[ystart:ystop, xstart:xstop, 0] = b
        temp[ystart:ystop, xstart:xstop, 1] = g
        temp[ystart:ystop, xstart:xstop, 2] = r
    
    

    #save
    success = cv.imwrite(saveDst, temp)
    print("LabelStage2 Success : " + str(success))
