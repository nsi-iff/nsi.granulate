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
        self.temporaryPath = self.temporaryFileSystem.createDirectory()
        self.temporaryFileSystem.createFile(self.file.getData())
        
        if args.get('sensitivity'):
            self.sensitivityPercent = args['sensitivity']
        else:
            self.sensitivityPercent = 0.3

    def findTransition(self):
        initExtract = InitExtract()
        shotVideo = ShotVideo()
        video_loaded = initExtract.createCapture(self.temporaryPath)
        sensitivity = 0.295
        list_transition = shotVideo.shotDetect(video_loaded, sensitivity)
        return list_transition

    def granulate(self):
        """
        """
        returnDict = {}
        returnList = []
        imageList = self.findTransition()
        i = 0
        for img in imageList:
            i+=1
            filename="shot"+str(i)+".jpg"
            content = StringIO()
            img.save("im" + str(i) + "jpeg" ,"JPEG")
            obj = Grain(id=filename, content=content, graintype='image')
            returnList.append(obj)
        returnDict['image_list']=returnList
        return returnDict
        
    def ungranulate(self, **args):
        self.refresh(**args)

