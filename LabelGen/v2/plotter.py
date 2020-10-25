#author : Harshit
"""
Plot data points over LabelStage2.png
"""

import cv2 as cv
import numpy as np
import cairo

def plotDatapoints(stage2label_path, label_dst, sub_signature):
    """
    Plot Datapoints on Label Stage 2 given from sub_signature.

    PLot Datapoints over logo binded Label using sub_signature for current label version.

    Parameters:

        stage2label_path (str): The Logo Binded Label template path.

        label_dst (str): AudioLabel save destination.

        sub_signature (str): Sub-Signature string for current version of audio label.

    Return:

        (None)
    """
    #len = 21 and radix = 8
    #7=boxHeight/2 - boxHeight/16
    #0,0 is intersection of reference line and dividing line.
    label = cv.imread(stage2label_path, cv.IMREAD_UNCHANGED)

    boxHeight = label.shape[0]
    boxWidth = label.shape[1]
    alt_width = int((boxWidth-boxHeight)/22)

    data = np.zeros((len(sub_signature), 2), dtype="float")

    surface = cairo.ImageSurface.create_for_data(label, cairo.FORMAT_ARGB32, boxWidth, boxHeight)
    context = cairo.Context(surface)

    flag = True
    x = 0
    i = 0
    for c in sub_signature:
        num = ord(c) - ord('0')
        y = num*boxHeight/16
        if flag:
            flag = False
        else:
            y = -y
            flag = True

        x += alt_width
        data[i][0] = x
        data[i][1] = y
        i = i + 1

    origin = [boxHeight, boxHeight/2]
    #Bezier Curve
    context.move_to(origin[0] + data[0][0], origin[1] - data[0][1])
    for i in range(data.shape[0]-1):
        coord0 = (origin[0] + data[i][0], origin[1] - data[i][1])
        coord1 = (origin[0] + data[i+1][0], origin[1] - data[i+1][1])
        context.curve_to(coord0[0] + alt_width/2, coord0[1], coord1[0] - alt_width/2, coord1[1], coord1[0], coord1[1])

    context.set_source_rgba(0, 1, 0, 0.5)
    context.set_line_width(1)
    context.stroke()

    #Pattern
    for datapoint in data:
        coord = (int(origin[0] + datapoint[0]), int(origin[1] - datapoint[1]))

        #draw dot at coord
        label = cv.ellipse(label, coord, (2, 2), 0, 0, 360, (0, 255, 0, 255), -1)
        #outer circle
        label = cv.ellipse(label, coord, (5, 5), 0, 0, 360, (0, 255, 0, 255)) 

    

    cv.imwrite(label_dst, label)