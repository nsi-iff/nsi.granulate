from zipfile import ZipFile 
from lxml import etree
from StringIO import StringIO
import string
import os


class _DocxHandler(object):
    def __init__(self):
        self._document_root = None
        self._original_docx = None

    def _create_header(self):
        header = "<w:document "
        for namespace,value in self._document_root.nsmap.items():
            header += "xmlns:%s='%s' " %(namespace, value)
        header += "><w:body>"
        return header

    def _create_footer(self):
        return "</w:body></w:document>"

    def _create_new_docx(self, new_xml):
        new_docx_content = StringIO(new_xml)
        new_docx = ZipFile(new_docx_content, 'w')
        for file_from_docx in self._original_docx.infolist():
            if file_from_docx.filename == 'word/document.xml':
                new_docx.writestr(file_from_docx.filename, new_xml)
            else:
                new_docx.writestr(file_from_docx.filename,
                                  self._original_docx.read(file_from_docx.filename))
        new_docx.close()
        return ZipFile(new_docx_content)

    def create_docx_with_table(self, table, original_docx):
        self._document_root = etree.fromstring(original_docx.read("word/document.xml"))
        self._original_docx = original_docx
        sectPr = self._document_root.xpath("//w:sectPr",
                                           namespaces=self._document_root.nsmap)[0]
        rsidR = sectPr.attrib['{%s}rsidR' %self._document_root.nsmap['w']]
        parser = etree.XMLParser(remove_blank_text=True)
        parser.feed(self._create_header()+\
                    etree.tostring(table)+\
                    "<w:p w:rsidR=\"%s\" w:rsidRDefault=\"%s\"/>" %(rsidR,rsidR)+\
                    etree.tostring(sectPr)+\
                    self._create_footer())
        root = parser.close()
        new_xml = etree.tostring(root,
                                 xml_declaration=True,
                                 encoding="UTF-8").replace("<a:", "<w:").\
                                                   replace("</a:", "</w:")
        return self._create_new_docx(new_xml)
    
class _PptxHandler(object):
    def get_slides_data(self, pptx):
        return [pptx.read(filename.filename) for filename in pptx.infolist()
                    if filename.filename.startswith('ppt/slides/slide')]

    
class TableGranulator(object):
    
    @classmethod
    def _granulate_docx(cls, docx_file):
        docx_creator = _DocxHandler()
        original_docx = ZipFile(docx_file)
        document_xml = original_docx.read("word/document.xml")
        document_root = etree.fromstring(document_xml)
        tables = document_root.xpath("//w:tbl", namespaces=document_root.nsmap)
        docx_files = []
        for table in tables:
            new_docx = docx_creator.create_docx_with_table(table, original_docx)
            docx_files.append(new_docx)
        return docx_files

    @classmethod
    def _granulate_pptx(cls, pptx_file):
        pptx_files = []
        pptx_creator = _PptxHandler()
        docx_creator = _DocxHandler()
        pptx_zipped = ZipFile(pptx_file)
        template_docx = ZipFile(open(os.path.join(os.path.dirname(__file__), "template_docx.docx")))
        slides_data = pptx_creator.get_slides_data(pptx_zipped)
        for slide in slides_data:
            root = etree.fromstring(slide)
            tables = root.xpath('//a:tbl', namespaces=root.nsmap)
            pptx_files.extend([docx_creator.create_docx_with_table(table, template_docx) for table in tables])
        return pptx_files

    @classmethod
    def granulate(cls, file_object, extension):
        if extension == 'docx':
            return cls._granulate_docx(file_object)
        elif extension == 'pptx':
            return cls._granulate_pptx(file_object)
