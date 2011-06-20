#!/usr/bin/env python
#-*- coding: utf-8 -*-

try:
    import Image
except ImportError:
    import PIL.Image
from imageManipulation import ImageManipulation


class HistogramPolitic(object):

    imageManipulation = ImageManipulation()

    def potentialShot(self, diference, sensitivity):
        return sensitivity < diference

    def verifyTransition(self, frameAHistogram, frameBHistogram,
                         frameCHistogram, sensitivity):
        backwardDiference = self.imageManipulation.\
             calculateHistogramDiference(frameAHistogram, frameBHistogram)
        forwardDiference = self.imageManipulation.\
             calculateHistogramDiference(frameBHistogram, frameCHistogram)
        if not(self.potentialShot(forwardDiference, sensitivity)) and\
               (self.potentialShot(backwardDiference, sensitivity)):
                return True
        return False

    def calculateSensitivity(self, sensitivityPercentage, frame):
        total_pixels = frame.size[0] * frame.size[1]
        sensitivity = int(total_pixels * sensitivityPercentage)
        return sensitivity
