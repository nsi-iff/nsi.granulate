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

import mimetypes
from StringIO import StringIO

class File(object):
    """
        This class is used for file handling
    """
    def __init__(self, filename=None, data=None):
        """
            Sets the filename and the file content
        """
        self.setFilename(filename)
        self.setData(data)
        
    def __call__(self):
        """
            Should be used getData instead of __call___
            For this object, call is useless.
        """
        return self.getData()
       
    def getFilename(self):
        return self.filename
    
    def setFilename(self, filename=None):
        """
            Set Filename and extract MimeType document
        """
        self.filename = filename
        self.mimetype = mimetypes.guess_type(filename)[0]

        
    def getData(self):
        return self.data
    
    def setData(self,data=None):
        """
            Set Data as a StringIO 
        """
        if isinstance(data,StringIO):
            self.data = data
        else:
            self.data = StringIO(str(data))
    
    def getContentType(self):
        return self.mimetype
    
    def setContentType(self, mimetype=None):
        self.mimetype = mimetype    


