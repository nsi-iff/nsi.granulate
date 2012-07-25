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

from xmlrpclib import *
from httplib import socket
from xml.dom.minidom import parseString
import copy
from StringIO import StringIO

from GranularUtils import Grain

import zipfile, base64, re
import os, sys, time, random
import shutil

try:
    import Image
except ImportError:
    import PIL.Image
import commands
#import config
import mimetypes

class ConectionServerError(Exception): pass


class GranulateOffice(object):
    """
        - Provide the grain extraction functionality for ms-office and odf documents
        - Retrieve tables, images, thumbnails and summary
    """
    Document = None
    __parseContent = None
    __zipFile = None
    __ooodServer = None
    supportedMimeType=('application/vnd.oasis.opendocument.text',
                     'application/vnd.sun.xml.writer',
                     'application/msword',
                     'application/rtf',
                     'application/vnd.stardivision.writer',
                     'application/x-starwriter',
                     'text/plain',
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

    supportedGranulateMimeTypes=('application/vnd.oasis.opendocument.text',
                                 'application/vnd.oasis.opendocument.presentation',)

    supportedConvertionMimeTypes=('application/msword',
                                  'application/rtf',
                                  'application/vnd.ms-powerpoint',)




    # Construct
    def __init__(self, Document=None, ooodServer=None):
        """
            - The parameter "Document" is a instance of the class "File" what it is in the FileUtils module
            - The ooodServer MUST be specified if the file is a ms-office file, or else the convertion server
              will be not found, and the grains will not be extracted
        """
        self.Document = Document
        self.__ooodServer = ooodServer
        self.refresh()

    def refresh(self, **args):
        if self.Document.getContentType() in self.supportedConvertionMimeTypes:
            # converts the file and stores in the Document object
            self.Document.setData(self.__convertDocumentToOdf())
            self.__parseXmlZipFile()

        elif self.Document.getContentType() in self.supportedGranulateMimeTypes:
            self.__parseXmlZipFile()



    def __call__(self):
        return self.granulateDocument()


    ### Private Methods ###


    def __mkServer(self):
        """
            Create a connection to the OpenOffice(oood-ERP5) Server
        """
        try:
            if self.__ooodServer is None:
                raise ConectionServerError, "It was not possible to connect. oood Server not found "
            return ServerProxy(self.__ooodServer)
        except:
            raise ConectionServerError, "It was not possible to connect to the Convertion Server."

    def __createNewOOoDocument(self):
        """
            Creates a new odt document based in a blank template
        """
        templatePath = os.path.join(os.path.dirname(__file__), 'template', 'template.odt')
        template_str=open(templatePath).read()
        return template_str

    def __getNodeText(self,node):
        """
            Get text value in a xml node
        """
        text = ''
        for child in node.childNodes:
            if child.nodeType is child.TEXT_NODE:
                text += child.data
            return text

    def __getTextChildNodesImage(self,node,text=[]):
        """
            Get the subtitle text of image in odf document
        """
        if node.nextSibling:
            node = node.nextSibling
            if node.nodeType is node.TEXT_NODE:
                text.append(node.data)
            else:
                text.append(self.__getNodeText(node))
            return self.__getTextChildNodesImage(node,text)
        else:
            return text

    def __getTextChildNodesTable(self,node,text=[]):
        """
            Get the subtitle text of a table in odf document
        """
        for n in node.childNodes:
            if n.nodeType is n.TEXT_NODE:
                text.append(n.data)
            if n.hasChildNodes():
                self.__getTextChildNodesTable(n,text)
        return text

    def __getAttrStyles(self, Node):
        """
            Get the associated Styles of given node
        """
        if Node.attributes is not None:
            for i in Node.attributes.keys():
                if re.search("^.+\:style-name$",i):
                    if Node.getAttribute(i):
                        return Node.getAttribute(i)

    def __getAttributesR(self, Node, styles=[]):
        style=self.__getAttrStyles(Node)
        if style:
            styles.append(style)
        for i in Node.childNodes:
            self.__getAttributesR(i,styles)
        if styles:
            return styles

    def __convertDocumentToOdf(self):
        """
            Convert a ms-office document to Open Document Format (odf)
        """
        oood_server = self.__mkServer()
        try:
            response = oood_server.run_convert(self.Document.getFilename(), base64.encodestring(self.Document.getData().getvalue()))
            if response[0]==200:
                file=StringIO(base64.decodestring(response[1]['data']))
                return file
            else:
                return None
        except (Error, socket.error), e:
            raise ConectionServerError(e)


    def __getSummaryDocument(self):
        """
            Get the Summary of an odf document
        """
        title_elements = self.__parseContent.getElementsByTagName('text:h')
        titles = []
        for t in title_elements:
            level = int(t.attributes['text:outline-level'].value)
            title = self.__getNodeText(t)
            titles.append({'level':level, 'value':title})
        if titles:
            return titles
        else:
            return []


    def __getThumbnailsDocument(self):
        """
            Get the Thumbnails of an odf document
        """
        for f in self.__zipFile.infolist():
            if f.filename == 'Thumbnails/thumbnail.png':
                contents = self.__zipFile.read('Thumbnails/thumbnail.png')
                return StringIO(contents)

        return None

    def __parseXmlZipFile(self):
        """
            Uncompress an odf file and parse the "content.xml" file.
        """
        try:
            self.__zipFile = zipfile.PyZipFile(self.Document.getData(),'r')
        except zipfile.BadZipfile, e:
            #Log.error("File is not a zip file")
            return None, None

        contents = self.__zipFile.read('content.xml')
        self.__parseContent = parseString(contents)


    def __getTableDocumentList(self):
        """
            Extract the tables from a document and return a list of Grain instances
        """
        table_list=[]
        # create an empty template
        template_str=self.__createNewOOoDocument()
        tables= self.__parseContent.getElementsByTagName('table:table')
        stylesDoc= self.__parseContent.getElementsByTagName('style:style')
        for t in tables:
            styles = self.__getAttributesR(t)
            table_name = t.getAttribute('table:name')
            imgHrefs=[]
            for img in t.getElementsByTagName("draw:image"):
                if img.hasAttribute("xlink:href"):
                    path=img.getAttribute('xlink:href')
                    #checks if the path is empty
                    if "ObjectReplacements" in path:
                        # remove th "./" of the path that could be "./ObjectReplacements/Object 2"
                        imgHrefs.append(path.replace("./",""))
                    # happens when it has an image from a website
                    elif re.match("^http://.+[\.jpg|\.png|\.gif]$",path):
                        continue
                    else:
                        imgHrefs.append(path)

            # extract legend
            objGran = Grain(graintype='table')
            leg=[]
            p = t.previousSibling
            n = t.nextSibling
            if p is not None:
              if p.hasChildNodes():
                  legenda = ''
                  for i in self.__getTextChildNodesTable(p,text=[]):
                      legenda+=i
                  leg.append(legenda)
              else:
                  leg.append(self.__getNodeText(p))
            if n is not None:
                if n.hasChildNodes():
                    legenda = ''
                    for j in self.__getTextChildNodesTable(n,text=[]):
                        legenda+=j
                    leg.append(legenda)
                else:
                    leg.append(self.__getNodeText(n))

            # join the strings to make a single legend
            caption = ' '.join([ i for i in leg if i is not None])

            objGran.setCaption(caption)
            # Creating an empty File
            table_name = t.getAttribute('table:name')
            new_table = StringIO()
            new_table.write(template_str)
            template_odt = zipfile.PyZipFile(new_table,'a')
            doc = parseString(template_odt.read('content.xml'))
            template_odt.close()
            office_text=doc.getElementsByTagName('office:text')
            office_text=office_text[0]

            # copy the table node from a document to a new table grain
            newTableNo=doc.importNode(t,True)
            office_text.appendChild(newTableNo)

            for sty in stylesDoc:
                if (sty.getAttribute('style:name') in styles):
                    office_automatic_styles=doc.getElementsByTagName('office:automatic-styles')
                    office_automatic_styles=office_automatic_styles[0]
                    office_automatic_styles.appendChild(doc.importNode(sty,True))
            if imgHrefs:
                for image in imgHrefs:
                    template_odt = zipfile.PyZipFile(new_table,'a')
                    template_odt.writestr(str(image),self.__zipFile.read(image))
                    template_odt.close()
            template_odt = zipfile.PyZipFile(new_table,'a')
            template_odt.writestr('content.xml',doc.toxml().encode('utf-8'))
            template_odt.close()
            if table_name:
                #objGran.setId(plone_utils.normalizeString(table_name))
                objGran.setId(table_name)
                objGran.setContent(new_table)
                objGran.setMimetype("application/vnd.oasis.opendocument.text")
                table_list.append(objGran)
        if table_list:
            return table_list
        else:
            return []



    def __getImageDocumentList(self):
        """
            Extract the images from a document and return a list of Grain instances
        """
        image_list=[]
        #get the elements in the tags draw:image, where the image references are kept
        tag_images = self.__parseContent.getElementsByTagName('draw:image')
        #checks if an image element exists
        if len(tag_images):
            for item in tag_images:
                name=None
                if item.hasAttribute("xlink:href"):
                    path=item.getAttribute('xlink:href')
                    #checks if the path is empty
                    if "Pictures" in path:
                        #remove the file extension
                        name=path.replace("Pictures/","")
                    elif "ObjectReplacements" in path:
                        name=path.replace("./ObjectReplacements/","")
                        # removes the "./" of the path that could be "./ObjectReplacements/Object 2"
                        path = path.replace("./","")

                    #  happens when it has an image from a website
                    elif re.match("^http://.+[\.jpg|\.png|\.gif]$",path):
                        continue

                    if name is not None:
                        #checks the image extension
                        f, e = os.path.splitext(name)
                        if e.lower() in ['.png','.gif','.jpg']:
                            # verifies if the image is already in the list
                            if not name in [image.getId() for image in image_list]:
                                parent = item.parentNode
                                nChild = parent.nextSibling
                                objGran = Grain(graintype='image')
                                if nChild:
                                    text=[]
                                    caption = ''
                                    if nChild.nodeType is nChild.TEXT_NODE:
                                        text.append(nChild.data)
                                    for t in self.__getTextChildNodesImage(nChild,text):
                                        if t is not None: caption+=t
                                    objGran.setCaption(caption)
                                imagefile = StringIO(self.__zipFile.read(path))
                                objGran.setId(name)
                                objGran.setContent(imagefile)
                                image_list.append(objGran)
        if image_list:
            return image_list
        else:
            return []


    ### Public Methods ###

    def getThumbnailsDocument(self):
        """
            Get document's thumbnails
        """
        if self.__zipFile is not None:
            return self.__getThumbnailsDocument()
        else:
            return None

    def getSummaryDocument(self):
        """
            Get document's summary
        """
        if self.__zipFile is not None:
            return self.__getSummaryDocument()
        else:
            return None

    def getImageDocumentList(self):
        """
            Invoke the private method __getImageDocumentList in order to retrieve the document's images
        """
        if self.__zipFile is not None:
            return self.__getImageDocumentList()
        else:
            return []

    def getTableDocumentList(self):
        """
            Invoke the private method __getTableDocumentList in order to retrieve the document's tables
        """
        if self.__zipFile is not None:
            return self.__getTableDocumentList()
        else:
            return []

    def granulate(self):
        """
            Extract the grains from a document, returning a dictionary with a list of tables, a list of images
            and the file's thumbnail
        """
        returnfiles = {}
        if self.__zipFile is not None:
            returnfiles['image_list'] = self.__getImageDocumentList()
            returnfiles['file_list'] = self.__getTableDocumentList()
            returnfiles['thumbnail'] = self.__getThumbnailsDocument()

        return returnfiles

    def ungranulate(self, **args):
        self.refresh(**args)

