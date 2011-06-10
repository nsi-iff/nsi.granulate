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
    Test methods comparaImage
"""

import sys, unittest
import re, time,os
from nsi.granulate.comparaHistogramaImage import comparaImage

absPath = os.path.abspath(__file__)

def getPathDir():
    path = os.path.join(os.path.dirname(absPath), 'data', 'compared_images')
    return path

class TestComparaImage(unittest.TestCase):

    def testComparaImage(self):
        """
            This test passes arguments the old way.
        """
        contTrue = 0
        contFalse = 0
        t1 = time.time()
        resultImgListDict = comparaImage(getPathDir())
        for imgDict in resultImgListDict:
            if imgDict.get('flag') is True:
                print "\n File: " + imgDict.get('filename') + " is True"
                contTrue +=1
            else:
                print "\n File: " + imgDict.get('filename') + " is False"
                contFalse +=1 
        self.assertEquals(contTrue, 1)
        self.assertEquals(contFalse, 2)
        print '\n Time run method: ' + str((time.time() -t1)/(24*3600))


def test_suite():
    suite = unittest.TestSuite()
    tests=(TestComparaImage,)
    for t in tests:
        suite.addTest(unittest.makeSuite(t))
    return suite

if __name__ == '__main__':
    test_suite()

