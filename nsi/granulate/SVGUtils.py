##############################################################################
#
# Copyright (c) 2008 ISrg (NSI, CEFETCAMPOS, BRAZIL) and Contributors.
#                                                         All Rights Reserved.
#                        Marguerite des Trois Maisons <des4maisons@gmail.com>
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

# this part was written originally by Marguerite des Trois Maisons <des4maisons@gmail.com>
# and modified by Hugo Lopes Tavares <hltbra@gmail.com>
from xml.dom import minidom

class PrepareSVG:
    def __init__(self):
        __doc = None

    def __replaceUse(self):
        """ replaces all <use .../> tags that reference elements defined in the 
            document with the original definition mutates node """
        for use in self.__doc.getElementsByTagName("use"):
                self.__replaceUseInNode(use)
    
    def __replaceUseInNode(self, old):
        """ removes old node, replaces with linked node (with modifications 
            according to www.w3.org/TR/SVG/struct.html#UseElement ) """
        if old.attributes and old.attributes.get('xlink:href'):
            link = old.attributes.get('xlink:href').value
            new = self.__followLink(link)
            if new:
                new = self.__wrapInGTag(new)
                self.__transferAttributes(old, new)
                old.parentNode.replaceChild(new, old)
                self.__removeDefs(new)
    
    def __wrapInGTag(self, node):
        doc = minidom.Document()
        newnode = self.__doc.parentNode.importNode(node, True)
        G = doc.createElement("g")
        G.appendChild(newnode)
        return G
    
    def __followLink(self, link):
        """  returns node referred to by link """
        if link[0] == '#':
            return self.__getNodeById(self.__doc, link[1:])
    
    def __getNodeById(self, node, id):
        """ my own version of getElementById that I can actually use
            this doesn't work if the id attribute is defined as something else
            at the beginning of the document, like with
            <!ATTLIST bla myid ID #IMPLIED> """
        # sorry it's messy; attributes are not very nice objects
        ID = node.attributes and node.attributes.get('id')
        if ID and ID.value == id:
            return node.cloneNode(True)
        for child in node.childNodes:
            n = self.__getNodeById(child, id)
            if n:
                return n
    
    def __transferAttributes(self, old, new):
        """ new is assumed to be wrapped in a fresh G tag and is modified according to
            www.w3.org/TR/SVG/struct.html#UseElement
            post: mutates new """
        c = new.firstChild
        for attribute in old.attributes.values():
            if attribute.name not in ("x", "y", "width", "height", "xlink:href"):
                new.attributes.setNamedItem(attribute)
            elif attribute.name in ("x", "y"):
                # executed twice if both x and y are present. oh well
                x = old.attributes.get("x", 0)
                y = old.attributes.get("y", 0)
                if x:
                    x = float(x.value) 
                if y:
                    y =  float(y.value)
                if new.attributes.get("transform"):
                    if "translate(%s,%s)"%(x,y) not in new.attributes["transform"].value:
                        newValue = new.attributes["transform"].value + " translate(%s,%s)" % (x,y)
                        new.attributes["transform"].value = newValue
                else:
                    new.setAttributeNS(None, "transform", "translate(%s,%s)" %(x,y))
            elif c.nodeName == 'symbol' and attribute.name in ("width", "height"):
                w = old.attributes.get("width", "100%")
                h = old.attributes.get("height", "100%")
                c.tagName = 'svg'
                if not isinstance(w, basestring):
                    w = w.value
                if not isinstance(h, basestring):
                    h = h.value
                if c.attributes.get("width"):
                    del c.attributes["width"]
                if c.attributes.get("height"):
                    del c.attributes["height"]
                c.setAttributeNS(None, "width", w)
                c.setAttributeNS(None, "height", h)
        c.attributes.removeNamedItem('id')
    
    def __removeDefs(self, node):
        """ remove all the defs sections (they are no longer needed for display) """
        if node.nodeName == 'defs':
            node.parentNode.removeChild(node)
        elif node.childNodes:
            for child in node.childNodes:
                self.__removeDefs(child)
    
    def removeUse(self, xmlString):
        """ replace all uses """
        parsedFile = minidom.parseString(xmlString)
        self.__doc = parsedFile.documentElement
        self.__replaceUse()
        return parsedFile
