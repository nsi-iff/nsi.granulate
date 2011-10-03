# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2007 ISrg (NSI, CEFETCAMPOS, BRAZIL) and Contributors.
#                                                         All Rights Reserved.
#                              Fábio Duncan de Souza<fduncan@cefetcampos.br>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

__author__ = """Fábio Duncan de Souza<fduncan@cefetcampos.br>"""
__docformat__ = 'plaintext'

import os
import tempfile
from StringIO import StringIO
from shotVideo import ShotVideo, InitExtract
from GranularUtils import Grain
import shutil


class Temporary(object):

    
    def __init__(self, videoFileName):
        self.videoFile = videoFileName
        
    def createDirectory(self):
        self.tempdir = tempfile.mkdtemp(prefix="temporaryVideoDirectory")
        self.filePath = os.path.join(self.tempdir, self.videoFile)
        return self.filePath
    
    def createFile(self, dataFile):
        open(self.filePath, "w+").write(dataFile.getvalue())

    def removeDirectory(self):
        os.remove(self.filePath)
        os.removedirs(self.tempdir)
       

class GranulateVideo(object):



    def __init__(self, video_file, **args):
        """
        """
        self.file = video_file
        self.refresh(**args)
        
        
    def refresh(self, **args):
        self.temporaryFileSystem = Temporary(self.file.getFilename())
        self.temporaryPathVideo = self.temporaryFileSystem.createDirectory()
        self.temporaryFileSystem.createFile(self.file.getData())
        
        if args.get('sensitivity'):
            self.sensitivityPercent = args['sensitivity']
        else:
            self.sensitivityPercent = 0.3

    def findTransition(self):
        initExtract = InitExtract()
        shotVideo = ShotVideo()
        video_loaded = initExtract.createCapture(self.temporaryPathVideo)
        list_transition, list_time = shotVideo.shotDetect(video_loaded, self.sensitivityPercent)
        return list_transition, list_time

    def cut_video(self, list_time):
        self.temporaryPathGrain = tempfile.mkdtemp(prefix="temporaryGrainDirectory")
        for i in range(len(list_time) - 1):
            init = list_time[i]
            duration = list_time[i + 1] - init - 0.2
            os.system("ffmpeg -i "+str(self.temporaryPathVideo) + " -acodec libvorbis -vcodec libtheora -ss "+ str(init) + " -t "+ str(duration)+ " " + self.temporaryPathGrain + "/video" +str(i)+".ogg")

    def granulate(self):
        """
        """
        returnDict = {}
        imageList, timeList = self.findTransition()
        self.cut_video(timeList)
        return_list_image = self.create_image_grains_list(imageList)
        return_list_video = self.create_video_grains_list()
        returnDict['image_list']=return_list_image
        returnDict['file_list']=return_list_video
        self.temporaryFileSystem.removeDirectory()
        shutil.rmtree(self.temporaryPathGrain)
        return returnDict

    def create_image_grains_list(self, imageList):
        returnList = []
        for i, img in enumerate(imageList):
            filename="shot"+str(i)+".png"
            content = StringIO()
            img.save(content,"PNG")
            obj = Grain(id=filename, content=content, graintype='image')
            obj.description = str(timeList[i])
            returnList.append(obj)
        return returnList

    def create_video_grains_list(self):
        returnList = []
        video_grains_path = os.listdir(self.temporaryPathGrain)
        video_grains_path.sort()
        for i, video in enumerate(video_grains_path):
            filename="video_grain"+str(i)+".ogv"
            content = StringIO(open(self.temporaryPathGrain + "/" + video).read())
            content.name = filename
            content.filename = filename
            obj = Grain(id=filename, content=content, graintype='nsifile')
            returnList.append(obj)
        return returnList        

    def ungranulate(self, **args):
        self.refresh(**args)

