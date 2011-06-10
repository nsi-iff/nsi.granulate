import os

def myopen(fname):
    return open(os.path.join(os.path.dirname(os.path.abspath(__file__)), fname))

DOCX_DATA = myopen('data/test_27images.docx').read() # improve
FIRST_DOCX_IMAGE = myopen('data/test_first_docx_image.png').read()
PPTX_DATA = myopen('data/test_1image.pptx').read()
FIRST_PPTX_IMAGE = myopen('data/test_first_pptx_image.jpg').read()
THREE_TABLES_DOCX_DATA = myopen('data/three_tables.docx').read()
ONE_TABLE_PPTX_DATA = myopen('data/one_table_pptx_data.pptx').read()
TWO_TABLES_PPTX_DATA = myopen('data/two_tables.pptx').read()
THUMBNAILS_DOCX_DATA = myopen('data/docx_icon.png').read()
THUMBNAILS_PPTX_DATA = myopen('data/pptx_icon.png').read()
