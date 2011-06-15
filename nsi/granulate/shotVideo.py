#!/usr/bin/env python
# -*- coding: utf-8 -*-

from opencv.highgui import (cvCreateFileCapture, cvQueryFrame, cvSaveImage,
cvGetCaptureProperty, CV_CAP_PROP_FPS)
from opencv.cv import cvCloneImage
from opencv.adaptors import Ipl2PIL
from imageManipulation import ImageManipulation
from politics import  HistogramPolitic
import os


class InitExtract(object):

    def createCapture(self, file_name):
        capture = cvCreateFileCapture(file_name)
        return capture

    def initFrameCapture(self, video_loaded):
        for i in range(25):
            frame = cvQueryFrame(video_loaded)
        return frame


class ShotVideo(object):

    number_transition = 0
    lastSaved = 0
    number_frame = 33
    total_frames = 0

    def initLoadFrames(self, frameA, frameB):
        vet_frames = [Ipl2PIL(frameA), Ipl2PIL(frameB), 0]
        return vet_frames

    def atualizeVetImg(self, vet_img, frame):
        vet_img.pop(0)
        vet_img.append(frame)
        return vet_img

    def passFrame(self, video_loaded):
        frameA = cvQueryFrame(video_loaded)
        frameB = cvQueryFrame(video_loaded)
        frameC = cvQueryFrame(video_loaded)
        return frameA, frameB, frameC

    def shotDetect(self, video_loaded, sensitivity):
        list_trasitions = []
        histogramPolitic = HistogramPolitic()
        imageManipulation = ImageManipulation()
        frameA, frameB, frameC = self.passFrame(video_loaded)
        vet_img = self.initLoadFrames(frameA, frameB)
        frameA_histogram = imageManipulation.createHistogramBoxes(vet_img, 0)
        frameB_histogram = imageManipulation.createHistogramBoxes(vet_img, 1)
        limiar = histogramPolitic.calculateSensitivity(sensitivity, vet_img[0])
        while not(frameC is None):
            vet_img = self.atualizeVetImg(vet_img, Ipl2PIL(frameC))
            frameC_histogram = imageManipulation.createHistogramBoxes(vet_img, 2)
            if histogramPolitic.verifyTransition(frameA_histogram,
            frameB_histogram, frameC_histogram, limiar) and\
            (self.number_frame - self.lastSaved) > 20:
                list_trasitions.append(vet_img[1])
            frameA, frameB, frameC = self.atualizeVar(frameA, frameB, frameC, \
             video_loaded)
            frameA_histogram = frameB_histogram
            frameB_histogram = frameC_histogram
            self.number_frame += 1
        return list_trasitions

    def atualizeVar(self, frameA, frameB, frameC, video_loaded):
        frameA = cvCloneImage(frameB)
        frameB = cvCloneImage(frameC)
        frameC = cvQueryFrame(video_loaded)
        return frameA, frameB, frameC
