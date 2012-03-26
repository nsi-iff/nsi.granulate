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

from xml.dom import minidom
from StringIO import StringIO
from GranularUtils import Grain

import os, sys, time, random, shutil
try:
    import Image
except ImportError:
    import PIL.Image
import mimetypes

from pypdf2table import ExecuteConverter

from comparaHistogramaImage import comparaImage

class ErrorXmlto(Exception):pass
class PyPdf2TableError(Exception):pass

class GranulatePDF(object):
    """
        - Provide the grain extraction functionality for PDF documents
        - Retrieve tables and images
    """
    Document = None
    __pathFolder = None

    def __init__(self, Document=None):
        """
            Checks if the Document is a PDF file, then creates a temporary folder and saves
            the PDF file in the filesystem
        """
        self.Document = Document
        self.refresh()
        
    def refresh(self):
        if self.Document.getContentType() == "application/pdf":
            dtime = str(time.time())+str(int(random.random()*100))
            self.__pathFolder = os.path.join('/tmp', dtime)
            os.mkdir(self.__pathFolder)
            filePDF=open(os.path.join(self.__pathFolder,self.Document.getFilename()),'w')
            filePDF.write(self.Document().getvalue())
            filePDF.close()
        else:
            raise "The file is not a PDF Document"


    ### Private Methods ###

    def __getImageDocumentList (self):
        """
           Retrieves images from a PDF document
        """
        if os.system('pdfimages -j "' + os.path.join(self.__pathFolder,self.Document.getFilename())  + '" ' + self.__pathFolder +'/imagegrain') == 256:
            #raise EOFError, "File has not the mandatory ending %EOF. File must be corrupted"
            return []
        # Lists the content of the temporary folder where the files are in.
        images = os.listdir(self.__pathFolder)
        images.remove(self.Document.getFilename())
        
        # Utiliza-se um algoritmo de descarte de imagens iguais  
        resultImgListDict = comparaImage(self.__pathFolder)
        # Remove as imagens repetidas
        for imgDict in resultImgListDict:
            if imgDict.get('flag') is True:
                images.remove(imgDict.get('filename'))

        image_list = [];
        for image in images:
            f, e = os.path.splitext(image)
            #convert the images .ppm or .pbm to files .png
            if e.lower() in ['.ppm','.pbm']:
                try:
                    content = StringIO()
                    PIL.Image.open(os.path.join(self.__pathFolder,image)).save(content, "PNG")
                    image = f + ".png"
                except:
                    fileImage = open(self.__pathFolder+'/'+image, "r")
                    content = StringIO(fileImage.read())
                    fileImage.close()
            else:
                #XXX-In the variable 'images' is coming a directory, it 
                # generates the error when trying to open directory as file.
                try:
                    fileImage = open(self.__pathFolder+'/'+image, "r")
                except IOError, e:
                    print e
                    continue
                content = StringIO(fileImage.read())
                fileImage.close()

            image_list.append(Grain(id=image,content=content,graintype='image'))

        return image_list

    def __getTableDocumentList(self):
        """
            Extract tables from a pdf file using pyPdf2Table
        """
        tableList = []
        pdfFile = os.path.join(self.__pathFolder,self.Document.getFilename())
        outputXMLFolder = os.path.join(self.__pathFolder,"outputXMLFolder")
        try:
            converterObj = ExecuteConverter.ExecuteConverter()
            converterObj.extractTables(pdfFile, outputXMLFolder)
            tableListStr = converterObj.getTableList()
        except Exception, e:
            return tableList

        i = 0
        for table in tableListStr:
            # generate table name
            i+=1
            tableId = "Table" + str(i) + ".html"
            # finally, the Grain is created en added to the list
            grainObj = Grain(graintype='table')
            grainObj.setId(tableId)
            grainObj.setContent(StringIO(table))
            grainObj.setMimetype("text/html")
            tableList.append(grainObj)

        return tableList

    ### Public Methods ###

    def getThumbnailsDocument(self):
        """
            Extracts the metadata from pdf files using 'convert' tool
        """
        os.system('evince-thumbnailer -s 128 "' + os.path.join(self.__pathFolder,self.Document.getFilename())  + '" ' + self.__pathFolder +'/thumbnail.png')
	file_content = StringIO(open(self.__pathFolder +'/thumbnail.png').read())
	os.remove(self.__pathFolder + '/thumbnail.png')
        return file_content


    def getImageDocumentList(self):
        """
            Invoke the private method __getImageDocumentList in order to retrieve the document's images
        """
        if self.__pathFolder is not None:
            return self.__getImageDocumentList()
        else:
            return []

    def getTableDocumentList(self):
        """
            Invoke the private method __getTableDocumentList in order to retrieve the document's tables
        """
        if self.__pathFolder is not None:
            return self.__getTableDocumentList()
        else:
            return []

    def granulate(self):
        """
            Extract the grains from a document, returning a dictionary with a list of tables and a list of images
        """
        returnfiles = {}
        if self.__pathFolder is not None:
            returnfiles['image_list'] = self.__getImageDocumentList()
            returnfiles['file_list'] = self.__getTableDocumentList()

        return returnfiles
        
    def ungranulate(self):
        shutil.rmtree(self.__pathFolder)
        self.refresh()
