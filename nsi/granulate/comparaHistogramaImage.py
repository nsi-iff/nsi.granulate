# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2007 ISrg (NSI, CEFETCAMPOS, BRAZIL) and Contributors.
#                                                         All Rights Reserved.
#                              Ronaldo Amaral Santos <ronaldinho.as@gmail.com>
#                              Fabio Duncan de Souza<fduncan@cefetcampos.br>
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

__author__ = """Ronaldo Amaral Santos<ronaldinho.as@gmail.com> 
                Fabio Duncan de Souza<fduncan@cefetcampos.br>"""
__docformat__ = 'plaintext'

try:
    import Image
except ImportError:
    import PIL.Image
import os

class imageOperations(object):
    
    def __init__(self,image1):
        self.image1 = image1
    
    def histogramCompare(self, image2):
        return self.image1.histogram() == image2.histogram()


def comparaImage(path):
    imageList=[]
    images = os.listdir(path)
    for image in images:
        try:
            try:
                img = Image.open(os.path.join(path,image))
            except ImportError:
                img = PIL.Image.open(os.path.join(path,image))
            imageList.append({'filename':image,'objImage':img,'flag':False})
        except IOError:
            pass        
    i=0
    for imgDict in imageList:
        i+=1 
        if imgDict.get('flag') is False:
            operacao = imageOperations(imgDict.get('objImage'))
            for imgDict2 in imageList[i:]:
                if imgDict2.get('flag') is False:
                    compResult = operacao.histogramCompare(imgDict2.get('objImage'))
                    if compResult is True:
                        imgDict2['flag']=True
    return imageList  
