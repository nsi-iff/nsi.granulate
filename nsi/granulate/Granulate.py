# -*- coding: utf-8 -*-
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

from GranularUtils import Grain
from FileUtils import File
import os
import commands
from GranulateOffice import GranulateOffice
from GranulatePDF import GranulatePDF
from GranulateSVG import GranulateSVG
from GranulateVideo import GranulateVideo
from SvgExtractRegion import SvgExtractRegion
from GranulateOpenXML import GranulateOpenXML
from plone.memoize import ram

def cachekey(method, self, filename, data, **args):
    return (filename, data)

class Granulate(object):
    """
        - Provides the content granularization delegating the responsability to the appropriate class.
        - Keeps the oood server related information (host and port).

        About the usage of the methods: getSummaryDocument, getThumbnailsDocument, getTableDocumentList,
        getImageDocumentList and granulateDocument:
            - The first parameter is the filename (without the path), like "test.odt"
            - The second one is a string representing the file content.
                    Ex. >>> file = open(filepath,'r')
                        >>> file.read()
    """
    ooodServer = None
    supportedOfficeDocument=('application/vnd.oasis.opendocument.text',
                             'application/vnd.sun.xml.writer',
                             'application/msword',
                             'application/rtf',
                             'application/vnd.stardivision.writer',
                             'application/x-starwriter',
                             'application/vnd.oasis.opendocument.spreadsheet',
                             'application/vnd.sun.xml.calc',
                             'application/vnd.ms-excel',
                             'application/vnd.stardivision.calc',
                             'application/x-starcalc',
                             'application/vnd.oasis.opendocument.presentation',
                             'application/vnd.sun.xml.impress',
                             'application/vnd.ms-powerpoint',
                             'application/vnd.stardivision.draw',
                             'application/vnd.stardivision.impress',
                             'application/x-starimpress',)
    supportedVideoMimetypes=('video/mpeg', #mpeg
                             'video/mp4', #mp4
                             'video/ogg', #ogv
                             'video/x-theora+ogg', #ogg
                             'video/x-msvideo', #avi
                             'video/x-flv', ) #flv


    def __init__(self, host=None, port=None):
        """Set the host and port of the oood daemon during the instance
        creation"""
        if (host is not None) and (port is not None):
            self.setServer(host, port)

    def __createGranulateOffice(self, document):
        granulate_office = GranulateOffice(document, self.ooodServer)
        return granulate_office

    def __get_mimetype(self, _file):
        path = os.path.join(os.getcwd(), _file.filename)
        return commands.getoutput('mimetype ' + path).split(':')[-1][1:]

    def __process(self, filename=None, data=None, **args):
        """
            Checks the file type and creates the proper object.
        """
        if filename and data:
            # create instance FileUtils
            Document = File(filename=filename, data=data)
            mimetype = self.__get_mimetype(Document)

            if mimetype in self.supportedOfficeDocument:
                return self.__createGranulateOffice(Document)


            elif mimetype == 'application/pdf':
                return GranulatePDF(Document)

            elif mimetype == 'image/svg+xml':
                # Verifica se foi passado os parametros para Extração de Regiao
                if args.has_key("x") and args.has_key("y") and args.has_key("w") and args.has_key("h"):
                    return SvgExtractRegion(Document, **args)
                return GranulateSVG(Document(), **args)

            elif mimetype in self.supportedVideoMimetypes:
                return GranulateVideo(Document, **args)

            elif Document.getFilename()[-5:] in ('.docx', '.pptx'):
                return GranulateOpenXML(Document, **args)

        return None

    def setServer(self, host=None, port=None):
        """Set OpenOffice Daemon - oood host and port for conversion
        document"""
        self.ooodServer = 'http://%s:%s' % (host, port)

    def getServer(self):
        """
            Get OpenOffice Daemon - oood informations for conversion document
        """
        return self.ooodServer

    def getSummaryDocument(self, filename=None, data=None):
        """
            Get Office Document's summary (odf, doc, ppt for instance)
        """
        GranulateObj = self.__process(filename=filename, data=data)
        if hasattr(GranulateObj, 'getSummaryDocument'):
            return GranulateObj.getSummaryDocument()
        else:
            return None

    def getThumbnailsDocument(self, filename=None, data=None):
        """
            Get Office Document's Thumbnails (odf, doc, ppt for instance)
        """
        GranulateObj = self.__process(filename=filename, data=data)
        if hasattr(GranulateObj, 'getThumbnailsDocument'):
            return GranulateObj.getThumbnailsDocument()
        else:
            return None

    def getTableDocumentList(self, filename=None, data=None):
        """
            Get a Table List from Office and PDF Documents
        """
        GranulateObj = self.__process(filename=filename, data=data)
        if hasattr(GranulateObj, 'getTableDocumentList'):
            return GranulateObj.getTableDocumentList()
        else:
            return None

    def getImageDocumentList(self, filename=None, data=None):
        """
            Get a Image List from Office and PDF Documents
        """
        GranulateObj = self.__process(filename=filename, data=data)
        if hasattr(GranulateObj, 'getImageDocumentList'):
            return GranulateObj.getImageDocumentList()
        else:
            return None

    def granulate(self, filename=None, data=None, **args):
        """
            Retrieve the grains of Documents (tables and images, for example) and Media contents.(Video)
        """
        GranulateObj = self.__process(filename=filename, data=data, **args)
        if hasattr(GranulateObj, 'granulate'):
            return GranulateObj.granulate()
        else:
            return None

    def ungranulate(self, filename=None, data=None, **args):
        GranulateObj = self.__process(filename=filename, data=data, **args)
        if hasattr(GranulateObj, 'ungranulate'):
            return GranulateObj.ungranulate(**args)

    def extractorRegion(self, filename=None, data=None, **args):
        """
            Extractor Rich Rock Methods Sun Shine
        """
        GranulateObj = self.__process(filename=filename, data=data, **args)
        if hasattr(GranulateObj, 'extractRegion'):
            return GranulateObj.extractRegion()
        else:
            return None

