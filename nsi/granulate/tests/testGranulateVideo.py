#!/usr/bin/python
##############################################################################
#
# Copyright (c) 2007 ISrg (NSI, CEFETCAMPOS, BRAZIL) and Contributors.
#                                                         All Rights Reserved.
#                              Ronaldo Amaral Santos <ronaldinho.as@gmail.com>
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

__author__ = """Ronaldo Amaral Santos <ronaldinho.as@gmail.com>"""
__docformat__ = 'plaintext'

"""
Test methods GranulateVideo
"""

import sys, unittest
import time,os
from nsi.granulate import File
from nsi.granulate import GranulateVideo

absPath = os.path.abspath(__file__)

# FileInfo{Filename:Image Number}
FileInfo = {'cachorros-mpeg1.mpeg':19,
            'Rio_de_Janeiro_Travel_Guide.mpg':27,
            'cachorros-mpeg4.mp4':23,
            'working_google.flv':115,
            'linuxBoy.avi':5,
            'foo.ogg':14}

def getFileDirList():
    returnDictFile = {}
    path = os.path.join(os.path.dirname(absPath), 'data')
    fileList = os.listdir(path)
    for fileTest in fileList:
        if fileTest in FileInfo.keys():
            filePath = os.path.join(path, fileTest)
            try:
                filedata = open(filePath, 'rb').read()
                returnDictFile[fileTest] = filedata
            except IOError:
                print "File not found"
                sys.exit(1)
    return returnDictFile

class TestGranulateVideo(unittest.TestCase):

    def createInstanceGraVideo(self, filename, filedata):
        fileDoc = File(data=filedata,filename=filename)
        granObj = GranulateVideo(video_file=fileDoc, sensitivity=0.3)
        return granObj

    def testCheckCreateInstanceGranVideo(self):
        """
            This test passes arguments the old way.
        """
        t1 = time.time()
        dictFile = getFileDirList()
        for k, v in dictFile.iteritems():
            granObj = self.createInstanceGraVideo(filename = k, filedata = v)
            self.failUnless(granObj is not None)
            self.failUnless(granObj.file is not None)
            print " \n File: "+ k + '\n Time run method: ' + str((time.time() -t1)/(24*3600))
            

    def testGranulate(self):
        """
            This test passes arguments the old way.
        """
        t1 = time.time()
        dictFile = getFileDirList()
        for k, v in dictFile.iteritems():
            granObj = self.createInstanceGraVideo(filename = k, filedata = v)
            self.failUnless(granObj is not None)
            #import ipdb;ipdb.set_trace()
            resultDict = granObj.granulate()
            self.assertEquals(len(resultDict['image_list']), FileInfo[k])

            print " \n File: "+ k + '\n Time run method: ' + str((time.time() -t1)/(24*3600))


def test_suite():
    suite = unittest.TestSuite()
    tests=(TestGranulateVideo,)
    for t in tests:
        suite.addTest(unittest.makeSuite(t))
    return suite

if __name__ == '__main__':
    test_suite()

