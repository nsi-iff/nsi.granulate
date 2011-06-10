##############################################################################
#
# Copyright (c) 2007 ISrg (NSI, CEFETCAMPOS, BRAZIL) and Contributors.
#                                                         All Rights Reserved.
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

class Grain(object):
    """
        This Class is used as reference to manipulate Grains
    """
    def __init__(self, id=None, caption=None, content=None, mimetype=None, graintype=None):
        """
            The default attributes represent the metadata from Grain.
        """
        self.id = id
        self.caption = caption
        self.content = content
        self.mimetype= mimetype
        self.graintype= graintype

    def __call__(self):
        """
            Should be used getContent instead of __call___
            For this object, call is useless.
        """
        return self.getContent()

    def getId(self):
        return self.id

    def setId(self,id=None):
        self.id = id

    def getCaption(self):
        return self.caption

    def setCaption(self,caption=None):
        self.caption = caption

    def getContent(self):
        """
            Content is usually a StringIO.
        """
        return self.content

    def setContent(self,content=None):
        """
            Content should receive only a StringIO
        """
        self.content = content

    def getMimetype(self):
        return self.mimetype

    def setMimetype(self, mimetype=None):
        self.mimetype=mimetype

    def setGraintype(self, graintype=None):
        self.graintype = graintype

    def getGraintype(self):
        return self.graintype

