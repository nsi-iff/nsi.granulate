from nsi.svgtool.SvgTool import *
import StringIO
from GranularUtils import Grain

class SvgExtractRegion(object):
    """ """

    def __init__(self, document, **args):
        self.tool = SvgTool()
        self.x = args.get("x")
        self.y = args.get("y")
        self.w = args.get("w")
        self.h = args.get("h")
        self.document = document

    def extractRegion(self):
        content_file = self.tool.makeNewSvgStringIO(self.document.getFilename(), self.document.getData())
        image = self.tool.makeNewSvgImage(content_file)

        new_content_file = self.tool.makeNewSvgStringIO("new_"+self.document.getFilename(), StringIO.StringIO(''))
        new_svg = self.tool.makeNewSvgImage(new_content_file)

        region = Box(Point(self.x,self.y),self.w,self.h)

        new_image = self.tool.selectGrainsInRegion(region, image, new_svg)
        objGran = Grain(content=new_image.getContentFile(),mimetype="image/svg+xml",graintype='svg')
        return objGran

