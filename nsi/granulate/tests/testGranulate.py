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
    Test methods Granulate
"""

import sys, unittest
import re, time,os
from nsi.granulate import Granulate
from openxml_utils import *
from doubles_for_tests import insertFakeOoodCallIntoGranulateOffice
# FileInfo{Filename:(Image Number, Table Number)}
FileInfo = {'26images-1table.odt':(26,1),'2images-1table.odt':(2,1)}

ServerOoodhost = 'localhost'
ServerOoodport = 8080

absPath = os.path.abspath(__file__)

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

class TestGranulate(unittest.TestCase):

    def setUp(self):
        self.granController = Granulate(host=ServerOoodhost, port=ServerOoodport)


    def testGranulate(self):
        """
            This test passes arguments the old way.
        """
        t1 = time.time()
        dictFile = getFileDirList()
        for k, v in dictFile.iteritems():
            resultDict = self.granController.granulate(filename=k, data=v)
            self.assertEquals(len(resultDict['image_list']), FileInfo[k][0])
            self.assertEquals(len(resultDict['file_list']), FileInfo[k][1])
            print " \n File: "+ k + '\n Time run method: ' + str((time.time() -t1)/(24*3600))

    def testGetTableDocumentList(self):
        """
            This test passes arguments the old way.
        """
        t1 = time.time()
        dictFile = getFileDirList()
        for k, v in dictFile.iteritems():
            resultList = self.granController.getTableDocumentList(filename=k, data=v)
            self.assertEquals(len(resultList), FileInfo[k][1])
            print " \n File: "+ k + '\n Time run method: ' + str((time.time() -t1)/(24*3600))

    def testGetImageDocumentList(self):
        """
            This test passes arguments the old way.
        """
        t1 = time.time()
        dictFile = getFileDirList()
        for k, v in dictFile.iteritems():
            resultList = self.granController.getImageDocumentList(filename=k, data=v)
            self.assertEquals(len(resultList), FileInfo[k][0])
            print " \n File: "+ k + '\n Time run method: ' + str((time.time() -t1)/(24*3600))

    def testGetThumbnailsDocument(self):
        """
            This test passes arguments the old way.
        """
        t1 = time.time()
        dictFile = getFileDirList()
        for k, v in dictFile.iteritems():
            result = self.granController.getThumbnailsDocument(filename=k, data=v)
            self.failUnless(result is not None)
            #self.assertEquals(resultDict['thumbnails'], is instance)
            print " \n File: "+ k + '\n Time run method: ' + str((time.time() -t1)/(24*3600))

    def testGetSummaryDocument(self):
        """
            This test passes arguments the old way.
        """
        t1 = time.time()
        dictFile = getFileDirList()
        for k, v in dictFile.iteritems():
            resultList = self.granController.getSummaryDocument(filename=k, data=v)
            self.assertFalse(bool(resultList))
            print " \n File: "+ k + '\n Time run method: ' + str((time.time() -t1)/(24*3600))

    def testGettingImagesFromDocx(self):
        images = self.granController.getImageDocumentList(data=DOCX_DATA, filename='file.docx')
        self.assertEquals(len(images), 27)
        self.assertEquals(FIRST_DOCX_IMAGE, images[0].getvalue())

    def testGettingImagesFromPptx(self):
        images = self.granController.getImageDocumentList(data=PPTX_DATA, filename='file.pptx')
        self.assertEquals(len(images), 1)
        self.assertEquals(FIRST_PPTX_IMAGE, images[0].getvalue())

    def testGettingThumbnailsFromDocx(self):
        thumbnails_docx = self.granController.getThumbnailsDocument(data=THREE_TABLES_DOCX_DATA,
                                                                filename='three_tables.docx')
        self.assertEquals(thumbnails_docx.getvalue(), THUMBNAILS_DOCX_DATA)

    def testGettingThumbnailsFromPptx(self):
        thumbnails_pptx = self.granController.getThumbnailsDocument(data=TWO_TABLES_PPTX_DATA,
                                                                filename='two_tables.pptx')
        self.assertEquals(thumbnails_pptx.getvalue(), THUMBNAILS_PPTX_DATA)


def test_suite():
    suite = unittest.TestSuite()
    tests=(TestGranulate,)
    for t in tests:
        suite.addTest(unittest.makeSuite(t))
    return suite

if __name__ == '__main__':
    test_suite()

