'''
    >>> from openxml_granulator import TableGranulator
    >>> files = TableGranulator.granulate(open('uma_tabela.docx'), extension='docx')
    >>> len(files)
    1
    >>> document_xml = files[0].read('word/document.xml')
    >>> xml_root = etree.fromstring(document_xml)
    >>> tbl_tags = xml_root.xpath('//w:tbl', namespaces=xml_root.nsmap)
    >>> len(tbl_tags)
    1

    >>> files = TableGranulator.granulate(open('duas_tabelas.docx'), extension='docx')
    >>> len(files)
    2
    >>> document_xml = files[0].read('word/document.xml')
    >>> xml_root = etree.fromstring(document_xml)
    >>> tbl_tags = xml_root.xpath('//w:tbl', namespaces=xml_root.nsmap)
    >>> len(tbl_tags)
    1
    >>> document_xml = files[1].read('word/document.xml')
    >>> xml_root = etree.fromstring(document_xml)
    >>> tbl_tags = xml_root.xpath('//w:tbl', namespaces=xml_root.nsmap)
    >>> len(tbl_tags)
    1

    >>> files = TableGranulator.granulate(open('duas_tabelas.pptx'), extension='pptx')
    >>> len(files)
    2
    >>> document_xml = files[0].read('word/document.xml')
    >>> xml_root = etree.fromstring(document_xml)
    >>> tbl_tags = xml_root.xpath('//w:tbl', namespaces=xml_root.nsmap)
    >>> len(tbl_tags)
    1
    >>> document_xml = files[1].read('word/document.xml')
    >>> xml_root = etree.fromstring(document_xml)
    >>> tbl_tags = xml_root.xpath('//w:tbl', namespaces=xml_root.nsmap)
    >>> len(tbl_tags)
    1
'''

from lxml import etree
from zipfile import ZipFile
import doctest

if __name__ == '__main__':
    doctest.testmod()
