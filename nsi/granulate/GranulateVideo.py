# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2007 ISrg (NSI, CEFETCAMPOS, BRAZIL) and Contributors.
#                                                         All Rights Reserved.
#                            Fábio Duncan de Souza<fduncan@cefetcampos.br>
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
import re
import shutil
from GranularUtils import Grain
import Image

class Temporary(object):

    def __init__(self, videoFileName):
        self.videoFile = videoFileName

    def createDirectory(self):
        self.tempdir = tempfile.mkdtemp(prefix="VideoGranulateTemporaryDirectory")
        self.filePath = os.path.join(self.tempdir, self.videoFile)
        return self.filePath


    def createFile(self, dataFile):
        open(self.filePath, "w+").write(dataFile.getvalue())


    def removeDirectory(self):
        shutil.rmtree(self.tempdir)


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
        self.image_path = self.temporaryFileSystem.tempdir + '/segmentation_video/transitions_video'
        self.temporaryPathGrain = self.temporaryFileSystem.tempdir + '/segmentation_video/parts_videos'
        self.audio_path = self.temporaryFileSystem.tempdir + '/segmentation_video/video_audio/audio_video.oga'
        self.converted_video_path = self.temporaryFileSystem.tempdir + '/segmentation_video/video_converted/'
        self.thumbnails_path = self.temporaryFileSystem.tempdir + '/segmentation_video/thumbnails'

        if args.get('sensitivity'):
            self.sensitivityPercent = args['sensitivity']
        else:
            self.sensitivityPercent = 0.35

    def findTransition(self):
        os.system('videoShot -i ' + self.temporaryPathVideo + ' -o ' + self.temporaryFileSystem.tempdir)

    def get_transition_time(self, filename):
        return re.search('\d+.\d*', filename).group()

    def get_image_list(self):
        image_list = []
        time_list = []
        sort_list = os.listdir(self.image_path)
        sort_list.sort()
        for image in sort_list:
            image_list.append(Image.open(self.image_path + '/' + image))
            time_list.append(self.get_transition_time(image))
        return image_list, time_list

    def granulate(self):
        """
        """
        returnDict = {}
        self.findTransition()
        image_list, time_list = self.get_image_list()
        return_list_image = self.create_image_grains_list(image_list, time_list)
        return_list_video = self.create_video_grains_list()
        returnDict['image_list']=return_list_image
        returnDict['file_list']=return_list_video
        returnDict['audio'] = self.create_audio_grain()
        returnDict['converted_video'] = self.create_converted_video()
        returnDict['thumbnails'] = self.create_video_thumbnail_list()
        self.temporaryFileSystem.removeDirectory()
        return returnDict

    def create_image_grains_list(self, imageList, timeList):
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

    def create_video_thumbnail_list(self):
        returnList = []
        video_thumbnail_path = os.listdir(self.thumbnails_path)
        video_thumbnail_path.sort()
        for i, thumbnail in enumerate(video_thumbnail_path):
            filename = self.thumbnails_path + "/" + thumbnail
            content = StringIO(open(filename).read())
            content.name = filename
            content.filename = filename
            obj = Grain(id=filename, content=content, graintype='nsifile')
            returnList.append(obj)
        return returnList

    def create_audio_grain(self):
        obj = None
        filename = 'audio_video.oga'
        if os.path.exists(self.audio_path):
            content = StringIO(open(self.audio_path).read())
            content.name = filename
            content.filename = filename
            obj = Grain(id=filename, content=content, graintype='nsifile')
        return obj

    def create_converted_video(self):
        filename = os.listdir(self.converted_video_path)[0]
        self.converted_video_path += filename
        obj = None
        if os.path.exists(self.converted_video_path):
            content = StringIO(open(self.converted_video_path).read())
            content.filename = filename
            content.name = filename
            obj = Grain(id=filename, content=content, graintype='nsifile')
        return obj

    def ungranulate(self, **args):
        self.refresh(**args)
