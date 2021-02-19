#Author : Harshit Vishwakarma
"""
    Detect Image and output Subsignature encoded in it
"""

import os
import cv2
import numpy as np
import math

def combineUncertainity(orignalSubSign, uncertainity):
    """
    Generate 2^(len(uncertainity)) subsignatures

    Parameters : 

        originalSubSignature ([int]): Original SubSignature based on Rounding

        uncertainity ([(int, int)]): array of tuple containing index and possible value 

    Return :

        [str]: Array of possible subsignatures
    """
    result = []
    subSign = orignalSubSign.copy()
    util(subSign, uncertainity, 0, result)
    return result

def util(subSign, uncertain, index, result):
    if(index >= len(uncertain)):
        result.append(subSign)
    else:
        untouch = subSign.copy()
        util(untouch, uncertain, index+1, result)

        swapped = subSign.copy()
        swapped[uncertain[index][0]] = uncertain[index][1]
        util(swapped, uncertain, index+1, result)



def imageToSubSignature(imagePath):
    """
    Read Image from imagePath and Decode v2 SubSignature

    Parameters : 

        imagePath (str): Temporary location of Image to detect

    Return :

        (str) : SubSignature
    """
    currDir = os.getcwd()
    path = os.path.join(currDir, imagePath)
    print(path)
    img = cv2.imread(path)
    img = np.uint8(img)
    img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
    #extract green channel
    green = img[:,:,1]
    _, green = cv2.threshold(green, 140, 255, cv2.THRESH_BINARY)
    green = cv2.medianBlur(green, 3)
    green = cv2.dilate(green, (7,7))
    green = cv2.Canny(green, 200, 100)
    #Get Bounding lines
    lines = cv2.HoughLinesP(green, 1, np.pi/180, 20, minLineLength=green.shape[0])

    #get houghLines
    blank = np.zeros((green.shape[0], green.shape[1], 3), green.dtype)
    for line in lines:
        for coord in line:
            cv2.line(blank, (coord[0], coord[1]), (coord[2], coord[3]), (0,0,255))


    # get min/max x,y
    min_x = green.shape[1]
    min_y = green.shape[0]
    max_x = 0
    max_y = 0
    for line in lines:
        for coor in line:
            if min_x > min(coor[0], coor[2]):
                min_x =  min(coor[0], coor[2])
            if min_y > min(coor[1], coor[3]):
                min_y = min(coor[1], coor[3])
            if max_x < max(coor[0], coor[2]):
                max_x =  max(coor[0], coor[2])
            if max_y < max(coor[1], coor[3]):
                max_y = max(coor[1], coor[3])

    green = green[min_y+1:max_y-1, :]


    cont, heir = cv2.findContours(green, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cont.sort(key=lambda x:cv2.boundingRect(x)[0])
    centers = []
    for c in cont :
        (x,y), r = cv2.minEnclosingCircle(c)
        center = (int(x), int(y))
        r = int(r)
        if(r >= 1 and r<=3):
            #cv2.circle(blank, center, r, (9,255,0))
            centers.append(center)

    #Starting from x_m to next 20 points
    dataPoints = []
    for i in range(len(centers)):
        index = len(centers) - i - 1
        if(len(dataPoints) >= 21):
            break
        if(centers[index][0] <= max_x):
            if(len(dataPoints) == 0):
                dataPoints.append(centers[index])
                continue
            if(len(dataPoints) > 0 and abs(dataPoints[len(dataPoints)-1][0] - centers[index][0]) > 10):
                dataPoints.append(centers[index])

    for data in dataPoints:
        cv2.circle(blank, data, 1, (0,255,0))
    
    #create reference ordinate
    refY = int(green.shape[0]/2)
    ## for any point (x,y), map abs(y-refY) to [0-7] monotonically
    subSign = []
    c=0
    uncertainity = []
    for i in range(len(dataPoints)-1, -1,-1):
        point = dataPoints[i]
        res = abs(point[1] - refY)/refY
        #if first decimal is 5 uncertainity exist
        ans = res
        if round(res*8) > 7:
            res = 7
        else:
            res = round(res*8)

        if( math.trunc(ans*80)/10 - int(ans*8)) == 0.5 :
            if(int(ans*8)<7):
                u = (c, int(ans*8))
                uncertainity.append(u)

        subSign.append(res)
        c = c+1


    #Total possible subsignatures can be 2^(len(uncertainity))
    #Possible subsignatures are found by replacing org subsignature with uncertainity(index, value) in all possible combinations
    result = combineUncertainity(subSign, uncertainity)

    subSigns = []
    for ss in result:
        string = ""
        for num in ss:
            string = string + str(num)

        subSigns.append(string)
    
    return subSigns


