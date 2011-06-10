# -*- coding: utf-8 -*-

##############################################################################
#
# Copyright (c) 2008 ISrg (NSI, CEFETCAMPOS, BRAZIL) and Contributors.
#                                                         All Rights Reserved.
#                              Hugo Lopes Tavares <hltbra@gmail.com>
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

from xml.dom import minidom
from StringIO import StringIO
import sys, os
from xml.parsers.expat import ExpatError # exception that carries about a not valid xml
import copy
# from nsi.granulate import PrepareSVG # not working, WHY?
from nsi.granulate.SVGUtils import PrepareSVG
from GranularUtils import Grain

GRANULATEURI = "http://www.cefetcampos.br/nsi/granulate"


class GranulateSVG:
    __svgfile = None    # svg StringIO [opened]
    __list = None       # the content list
    __writtenFiles = 0  # count the actual number os strings written
    __imgs_per_file = 0 # the number of images per svg file
    __svgTree = None    # the base svg file
    __lastAdded = None  # the last node and its parent inserted in the xml tree
    __remainder = 0     # the remainder of how many grains put in a svg file
    __usedRemainder = 0 # the flag that carry about used or not one of the remainder grains
    __nextID = 0        # the next number of granulate:id
    max = 0             # the maximum number of grains

    def __init__(self, file, **args):
        self.__svgfile = file
        self.refresh(**args)
    
    def refresh(self, **args):
        self.__list = []
        self.__writtenFiles = 0
        self.__imgs_per_file = 1
        self.__svgTree = None
        self.__lastAdded = []
        self.__nextID = 1
        self.max = args.get('max', 50)

    def granulate(self):
        """ granulate some svg file (if `max` is specified, at most in `max` files) """
        max = self.max
        try:
            xmlobj = PrepareSVG()
            xml = xmlobj.removeUse(self.__svgfile.getvalue())
        except ExpatError:
            print "\nERROR: Could not parse the svg file!\n"
            return []

        doc = xml.documentElement
        num_tags = self.__countTags(xml) # number of element tags (except block tags)
        self.__remainder = self.__setImgsPerFile(doc, max, num_tags) # stores the remainder
        self.__svgTree = self.__createTreeBased(xml)
        self.__getAllDefinitions(xml)

        for child in doc.childNodes:
            self.__visitNode(self.__svgTree.documentElement,child)

        if self.__lastAdded: # if the last things aren't written
            self.__writeSvgTree()

        xml.unlink()
        self.__svgTree.unlink()
        grain_list = []
        for grain in self.__list:
            new_grain = Grain(id='svg%s.svg' % (self.__list.index(grain)+1),
                              content=grain,
                              mimetype='image/svg+xml',
                              graintype='svg')
            grain_list.append(new_grain)
        return {'file_list' : grain_list}

    def ungranulate(self, **args):
        self.refresh(**args)

    def __visitNode(self, parent, node):
        """ visit all nodes """
        if node.nodeType == node.ELEMENT_NODE:
            if node.tagName in ['svg', 'g']:
                new = self.__createElementBased(node)
                self.__setID(new, parent)
                parent.appendChild( new )

                for child in node.childNodes:
                    self.__visitNode(new, child)

                if parent.hasChildNodes()==False and parent.parentNode:
                    parent.parentNode.removeChild(parent)

            elif node.tagName in ['rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon',\
                                  'path', 'text', 'use', 'image']:
                self.__setID(node, parent)
                self.__write(parent, node) # writes the element

    def __write(self, parentNode, child):
        """ add child to the svg tree and try to print it to any svg file """
        newchild = self.__svgTree.importNode(child, True) # deeply -> imply in text nodes
        parentNode.appendChild(newchild)

        self.__lastAdded.append( (parentNode, newchild) )
        self.__writtenFiles += 1

        if self.__writtenFiles == self.__imgs_per_file:
            # if it can put one of the remainder grains in this file, puts
            if self.__usedRemainder == False and self.__remainder > 0:
                self.__remainder -= 1
                self.__usedRemainder = True
                self.__writtenFiles -= 1 # back one
                return self.__svgTree
            self.__writeSvgTree()
        return self.__svgTree

    def __writeSvgTree(self):
        """ append the current svgTree to the list """
        newTree = copy.copy(self.__svgTree)
        self.__removeEmptyBlocks(newTree)

        string = StringIO( newTree.toxml().encode("UTF-8"))
        self.__list.append( string )
        self.__removeLastNodes()
        self.__writtenFiles = 0
        self.__usedRemainder = False
        return string

    def __removeLastNodes(self):
        """ remove the last nodes """
        for parent, child in self.__lastAdded[::-1]:
            parent.removeChild(child)
        self.__lastAdded = []

    def __removeEmptyBlocks(self, tree):
        """ remove all empty blocks """
        allG = tree.getElementsByTagName("g")
        allSVG=tree.getElementsByTagName("svg")
        for element in allG + allSVG:
            if element.hasChildNodes() == False and element.parentNode:
                element.parentNode.removeChild(element)
        return tree

    def __createElementBased(self, node):
        """ copy the node element """
        return self.__svgTree.importNode(node, False) # not deeply

    def __createTreeBased(self, xml):
        """ create a svg file based on xml """
        doctype = xml.doctype and xml.doctype.toxml() or ''
        namespaceURI = xml.documentElement.namespaceURI or 'http://www.w3.org/2000/svg'
        version = xml.version or "1.0"
        encoding = xml.encoding or "UTF-8"
        string = '<?xml version="%s" encoding="%s"?>%s\
                  <svg xmlns="%s" xmlns:granulate="%s" granulate:id="id0"/>'%\
                  (version, encoding, doctype, namespaceURI, GRANULATEURI)
        new_svg = minidom.parseString( string )
        self.__copyAttrs(new_svg.documentElement, xml.documentElement)
        return new_svg

    def __newElement(self, name):
        """ return a new element node """
        tmp = minidom.Document() # instance
        return tmp.createElement(name)

    def __setImgsPerFile(self, doc, max, num_tags):
        """ set the number of images per file and return the number of remaining grains"""
        if max > 0 and num_tags > 0 and max < num_tags:
            self.__imgs_per_file = num_tags / max
            return num_tags % max # remainder
        return 0

    def __getAllDefinitions(self, xml):
        """ get all definitions and put them in the document """
        for tag in ['style', 'defs', 'metadata']:
            for elem in xml.getElementsByTagName(tag):
                newelem = self.__svgTree.importNode(elem, True)
                self.__svgTree.documentElement.appendChild( newelem )
        return self.__svgTree.documentElement

    def __countTags(self, xml):
        """ count the number of "valid" tags in the svg file """
        num_tags = 0
        for tag in ['rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon',\
                    'path', 'text', 'use', 'image']:
            for elem in xml.getElementsByTagName(tag):
                if self.__insideDefs(elem, xml) == False:
                    num_tags += 1
        return num_tags

    def __insideDefs(self, elem, xml):
        """ verify if elem is inside a def """
        parent = elem.parentNode
        while parent.tagName != "defs" and parent != xml.documentElement:
            parent = parent.parentNode
        return parent.tagName == "defs"

    def __setID(self, node, parent):
        """ set an id and parentid to `node` """
        parentid = parent.attributes.get('granulate:id').value # always will be a parent
        newID       = self.__newAttribute(GRANULATEURI, "granulate:id","id%d"%self.__nextID)
        newParentID = self.__newAttribute(GRANULATEURI, "granulate:parentid", parentid)
        node.attributes.setNamedItem(newID)
        node.attributes.setNamedItem(newParentID)
        self.__nextID += 1
        return self.__nextID - 1

    def __newAttribute(self, namespace, localname, value):
        newAttr = self.__svgTree.createAttributeNS(namespace, localname)
        newAttr.value = value
        return newAttr

    def __copyAttrs(self, toNode, fromNode):
        """ copy all not existing attributes from `fromNode` to `toNode` """
        for attr in fromNode.attributes.values():
            if toNode.attributes.has_key(attr.name) == False:
                toNode.attributes.setNamedItem(copy.copy(attr))
        return toNode


# end of GranulateSVG #


if __name__ == '__main__':
    if not sys.argv[1]:
        print 'ERROR! The svg file name wasn\'t specified'
        sys.exit()

    file = sys.argv[1]
    svgfile = open(sys.argv[1], 'r')

    string_io = StringIO()
    string_io.write( svgfile.read())

    N = 50 # default

    if len(sys.argv) > 2 and int(sys.argv[2]) > 0:
        N = int(sys.argv[2])

    svg = GranulateSVG(string_io, max = N)

    svglist = svg.granulateDocument().get('file_list', [])

    string_io.close() # close the stringIO

    if file.rfind('/') != -1:
        file = file[ file.rfind('/') + 1 : ]

    if file.endswith('.svg'):
        file = file[:-4]

    list = os.listdir('.')
    file += '_granulated'

    # try to create a folder based on the svg file name
    if file in list:
        answer = raw_input('The folder already exists.\nDo you want to replace it? ([y]/n)')
        if answer.lower() == 'y' or answer == '':
            for i in os.listdir('./' + file):
                os.remove('./' + file + '/' + i ) # remove all files
        else:
            print 'Going out...'
            sys.exit()
    else:
        os.mkdir('./' + file)

    i = 0
    for l in svglist:
        i += 1
        f=open('./' + file + '/' + str(i) + '.svg', 'w')
        f.write(l.getvalue().encode("utf-8"))
        f.close()

    print 'Granulated.'

# -- end -- #
