#!/usr/bin/env python
#-*- coding: utf-8 -*-

from opencv.cv import cvCanny, cvCreateImage, cvCvtColor, cvGetSize
from opencv.cv import IPL_DEPTH_8U, CV_BGR2GRAY
from opencv.adaptors import Ipl2PIL


class ImageManipulation(object):

    def createHistogramBoxes(self, vetImg, frame, totalHorizontalDivisions = 4,
                             totalVerticalDivisions = 4):
        cropHistogram = []
        sizeBox = self.calculateSizeBox(vetImg[frame])
        for horizontalDivision in range(totalHorizontalDivisions):
            for verticalDivision in range(totalVerticalDivisions):
                x1Point = horizontalDivision * sizeBox[0]
                y1Point = verticalDivision * sizeBox[1]
                x2Point = x1Point + sizeBox[0] -1
                y2Point = y1Point + sizeBox[1] -1
                box = (x1Point, y1Point, x2Point, y2Point)
                cropHistogram.append(vetImg[frame].crop(box).convert("L").
                histogram())
        return cropHistogram

    def calculateSizeBox(self, frame, totalHorizontalDivisions = 4,
                          totalVerticalDivisions = 4):
        sizeBox = [0, 0]
        sizeBox[0] = frame.size[0] / totalHorizontalDivisions
        sizeBox[1] = frame.size[1] / totalVerticalDivisions
        return sizeBox

    def calculateHistogramDiference(self, histogram1, histogram2):
        diferenceHistogram = []
        for box in range(len(histogram1)):
            diferenceHistogram.append(0)
            for bin in range(0, 256):
                diferenceHistogram[box] = diferenceHistogram[box] + \
                (abs(histogram1[box][bin] - histogram2[box][bin]))
        diferenceHistogram.sort()
        diferenceHistogram = diferenceHistogram[0:8]
        return sum(diferenceHistogram)
