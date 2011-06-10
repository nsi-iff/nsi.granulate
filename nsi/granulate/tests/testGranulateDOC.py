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
from nsi.granulate import File, GranulateOffice
from doubles_for_tests import insertFakeOoodCallIntoGranulateOffice

# FileInfo{Filename:(Image Number, Table Number)}
FileInfo = {'test.doc':(4,1)}

ServerOood = 'http://localhost:8008'

absPath = os.path.abspath(__file__)

insertFakeOoodCallIntoGranulateOffice()

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

class TestGranulateDoc(unittest.TestCase):

    def createInstanceGraDoc(self, filename, filedata):
        fileDoc = File(data=filedata,filename=filename)
        granObj = GranulateOffice(Document = fileDoc, ooodServer = ServerOood)
        return granObj

    def testCheckCreateInstanceGranDoc(self):
        """
            This test passes arguments the old way.
        """
        t1 = time.time()
        dictFile = getFileDirList()
        for k, v in dictFile.iteritems():
            granObj = self.createInstanceGraDoc(filename = k, filedata = v)
            self.failUnless(granObj is not None)
            self.failUnless(granObj.Document is not None)
            print " \n File: "+ k + '\n Time run method: ' + str((time.time() -t1)/(24*3600))

    def testGranulate(self):
        """
            This test passes arguments the old way.
        """
        t1 = time.time()
        dictFile = getFileDirList()
        for k, v in dictFile.iteritems():
            granObj = self.createInstanceGraDoc(filename = k, filedata = v)
            self.failUnless(granObj is not None)
            resultDict = granObj.granulate()
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
            granObj = self.createInstanceGraDoc(filename = k, filedata = v)
            self.failUnless(granObj is not None)
            resultList = granObj.getTableDocumentList()
            self.assertEquals(len(resultList), FileInfo[k][1])
            print " \n File: "+ k + '\n Time run method: ' + str((time.time() -t1)/(24*3600))

    def testGetImageDocumentList(self):
        """
            This test passes arguments the old way.
        """
        t1 = time.time()
        dictFile = getFileDirList()
        for k, v in dictFile.iteritems():
            granObj = self.createInstanceGraDoc(filename = k, filedata = v)
            self.failUnless(granObj is not None)
            resultList = granObj.getImageDocumentList()
            self.assertEquals(len(resultList), FileInfo[k][0])
            print " \n File: "+ k + '\n Time run method: ' + str((time.time() -t1)/(24*3600))

    def testGetThumbnailsDocument(self):
        """
            This test passes arguments the old way.
        """
        t1 = time.time()
        dictFile = getFileDirList()
        for k, v in dictFile.iteritems():
            granObj = self.createInstanceGraDoc(filename = k, filedata = v)
            self.failUnless(granObj is not None)
            result = granObj.getThumbnailsDocument()
            self.failUnless(result is not None)
            print " \n File: "+ k + '\n Time run method: ' + str((time.time() -t1)/(24*3600))

    def testGetSummaryDocument(self):
        """
            This test passes arguments the old way.
        """
        t1 = time.time()
        dictFile = getFileDirList()
        for k, v in dictFile.iteritems():
            granObj = self.createInstanceGraDoc(filename = k, filedata = v)
            self.failUnless(granObj is not None)
            resultList = granObj.getSummaryDocument()
            headings = [heading['value'] for heading in resultList]
            self.assertTrue('Algoritmo de Dijkstra' in headings)
            print " \n File: "+ k + '\n Time run method: ' + str((time.time() -t1)/(24*3600))

    def testAllMethodsGranulateObj(self):
        """
            This test all methods.
        """
        t1 = time.time()
        dictFile = getFileDirList()
        for k, v in dictFile.iteritems():
            granObj = self.createInstanceGraDoc(filename = k, filedata = v)
            self.failUnless(granObj is not None)
            resultDict = granObj.granulate()
            self.assertEquals(len(resultDict['image_list']), FileInfo[k][0])
            self.assertEquals(len(resultDict['file_list']), FileInfo[k][1])

            resultListTable = granObj.getTableDocumentList()
            self.assertEquals(len(resultListTable), FileInfo[k][1])

            resultListImage = granObj.getImageDocumentList()
            self.assertEquals(len(resultListImage), FileInfo[k][0])

            resultThumbnails = granObj.getThumbnailsDocument()
            self.failUnless(resultThumbnails is not None)

            resultListSummary = granObj.getSummaryDocument()
            headings = [heading['value'] for heading in resultListSummary]
            self.assertTrue('Algoritmo de Dijkstra' in headings)

            print " \n File: "+ k + '\n Time run method: ' + str((time.time() -t1)/(24*3600))


def test_suite():
    suite = unittest.TestSuite()
    tests=(TestGranulateDoc,)
    for t in tests:
        suite.addTest(unittest.makeSuite(t))
    return suite

if __name__ == '__main__':
    test_suite()

