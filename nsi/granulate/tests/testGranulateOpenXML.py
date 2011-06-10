# coding: utf-8
##############################################################################
#
# Copyright (c) 2007 ISrg (NSI, CEFETCAMPOS, BRAZIL) and Contributors.
#                                                         All Rights Reserved.
#                       Hugo Lopes Tavares <hltbra@gmail.com>
#                       Rafael dos Santos Gonçalves <rafaelsantosg@gmail.com>
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

from nsi.granulate import GranulateOpenXML
from nsi.granulate import File
from openxml_utils import *
from lxml import etree
from zipfile import ZipFile
import unittest


class TestGranulateOpenXML(unittest.TestCase):
    def test_getting_images_from_docx(self):
        granulator = GranulateOpenXML(File(data=DOCX_DATA,
                                                 filename='test_27images.docx'))
        images = granulator.getImageDocumentList()
        self.assertEquals(len(images), 27)
        self.assertEquals(FIRST_DOCX_IMAGE, images[0].getvalue())

    def test_getting_images_from_pptx(self):
        granulator = GranulateOpenXML(File(data=PPTX_DATA,
                                                 filename='test_1image.pptx'))
        images = granulator.getImageDocumentList()
        self.assertEquals(len(images), 1)
        self.assertEquals(FIRST_PPTX_IMAGE, images[0].getvalue())

    def test_getting_tables_from_docx(self):
        granulator = GranulateOpenXML(File(data=THREE_TABLES_DOCX_DATA,
                                           filename='three_tables.docx'))
        files_with_single_tables = granulator.getTableDocumentList()
        first_file = files_with_single_tables[0]
        document_xml = first_file.read('word/document.xml')
        xml_root = etree.fromstring(document_xml)
        tbl_tags = xml_root.xpath('//w:tbl', namespaces=xml_root.nsmap)
        self.assertEquals(len(tbl_tags), 1)
        self.assertEquals(len(files_with_single_tables), 3)

    def test_getting_tables_from_pptx(self):
        granulator = GranulateOpenXML(File(data=TWO_TABLES_PPTX_DATA,
                                           filename='two_tables.pptx'))
        files_with_single_tables = granulator.getTableDocumentList()
        first_file = files_with_single_tables[0]
        document_xml = first_file.read('word/document.xml')
        xml_root = etree.fromstring(document_xml)
        tbl_tags = xml_root.xpath('//w:tbl', namespaces=xml_root.nsmap)
        self.assertEquals(len(tbl_tags), 1)
        self.assertEquals(len(files_with_single_tables), 2)

    def test_get_thumbnails_from_docx(self):
        granulator = GranulateOpenXML(File(data=THREE_TABLES_DOCX_DATA,
                                           filename='three_tables.docx'))
        thumbnails_docx = granulator.getThumbnailsDocument()
        self.assertEquals(thumbnails_docx.getvalue(), THUMBNAILS_DOCX_DATA)

    def test_get_thumbnails_from_pptx(self):
        granulator = GranulateOpenXML(File(data=TWO_TABLES_PPTX_DATA,
                                           filename='two_tables.pptx'))
        thumbnails_pptx = granulator.getThumbnailsDocument()
        self.assertEquals(thumbnails_pptx.getvalue(), THUMBNAILS_PPTX_DATA)


def test_suite():
    suite = unittest.TestSuite()
    tests=(TestGranulateOpenXML,)
    for t in tests:
        suite.addTest(unittest.makeSuite(t))
    return suite

if __name__ == '__main__':
    test_suite()

