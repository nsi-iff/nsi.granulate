from StringIO import StringIO
from nsi.granulate.openxml_granulator import TableGranulator
from zipfile import ZipFile
import os

class GranulateOpenXML(object):
    def __init__(self, document):
        self._document = document

    def _getThumbnailsDocx(self):
        return StringIO(open(os.path.join(os.path.dirname(__file__),
                                         'icons',
                                         'docx_icon.png')).read())
    def _getThumbnailsPptx(self):
        return StringIO(open(os.path.join(os.path.dirname(__file__),
                                         'icons',
                                         'pptx_icon.png')).read())

    def getImageDocumentList(self):
        docx = ZipFile(self._document.getData())
        initial_path = 'word/media'
        if self._document.getFilename().endswith('.pptx'):
            initial_path = 'ppt/media'
        image_filenames = (image for image in docx.namelist() if image.startswith(initial_path))
        images = []
        for image_path in image_filenames:
            image_wrapped = StringIO(docx.read(image_path))
            images.append(image_wrapped)
        return images

    def getTableDocumentList(self):
        extension = self._document.getFilename()[self._document.getFilename().rfind('.')+1:]
        return TableGranulator.granulate(self._document.getData(), extension)

    def getThumbnailsDocument(self):
        if self._document.getFilename().endswith('.docx'):
            return self._getThumbnailsDocx()

        elif self._document.getFilename().endswith('.pptx'):
            return self._getThumbnailsPptx()
