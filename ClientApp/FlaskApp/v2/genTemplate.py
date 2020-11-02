#Author : Harshit 
"""
Generate a single SVG label for platform compatibility.
Outer Borders -> width:height :: 8:1
Logo Space -> width:height :: 1:1
"""

import cairo
import os
import math

def generateBaseTemplate(baseLength, primaryColor, secondaryColor, accentColor, dst = os.getcwd()+'/LabelGen/template/v2_base.png', WHratio=8):
    """
        This function is used to generate Base Template for Optical Label.

        This function allows custom template with colors and aspect-ratios, baseLength is multiplied WHratio to 
        generate actual Template dimensions, Colors are tuples of (r,g,b,aplha).

        Parameters:

            baseLength (int):Actual dimension of Optical Label (equal to height).

            primaryColor tuple(double,double,double,double): Color of rectangular Box.

            secondaryColor tuple(double,double,double,double): Color of division line.

            accentColor tuple(double,double,double,double): Color of reference and other accent.

            WHratio (double): Width to Height ratio.

            dst (str): save destination of png file.


        Return:

            (None)
    """

    boxHeight = baseLength
    boxWidth = baseLength*WHratio

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, boxWidth, boxHeight)
    context = cairo.Context(surface)

    #borders
    degree = math.pi/180
    r = boxHeight/8
    R = boxHeight/2
    context.move_to(R,0)
    context.arc(boxWidth-r, r, r, -90*degree, 0)
    context.arc(boxWidth-r, boxHeight-r, r, 0, 90*degree)
    context.arc(R, R, R, 90*degree, -90*degree)
    context.close_path()
    context.set_source_rgba(primaryColor[0], primaryColor[1], primaryColor[2], primaryColor[3])
    context.set_line_width(4)
    context.set_source_rgba(primaryColor[0],primaryColor[1],primaryColor[2],primaryColor[3])
    context.fill()
    context.stroke()

    #dividing line
    context.move_to(boxHeight, 0)
    context.line_to(boxHeight, boxHeight)
    context.set_source_rgba(secondaryColor[0], secondaryColor[1], secondaryColor[2], secondaryColor[3])
    context.set_line_width(2)
    context.stroke()

    #reference line
    alt_width = (boxWidth-boxHeight)/22
    context.move_to(boxHeight, boxHeight/2)
    x = boxHeight - alt_width/2
    while (x < boxWidth):
        context.move_to(x + alt_width, boxHeight/2)
        context.line_to(x+alt_width*2, boxHeight/2)
        x += alt_width*2
    
    context.set_source_rgba(accentColor[0], accentColor[1], accentColor[2], accentColor[3])
    context.set_line_width(1)
    context.stroke()
    

    #save to png
    surface.write_to_png(dst)

