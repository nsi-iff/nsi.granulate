from nsi.granulate import GranulateOffice as GranulateOfficeOriginal
from StringIO import StringIO
from os.path import join, abspath, dirname

data_abspath = join(abspath(dirname(__file__)), 'data')

def __convertDocumentToOdf(self):
    odf = open(data_abspath + '/test.odt')
    data = odf.read()
    odf.close()
    return StringIO(data)

def insertFakeOoodCallIntoGranulateOffice():
    GranulateOfficeOriginal._GranulateOffice__convertDocumentToOdf = __convertDocumentToOdf


    
    
    