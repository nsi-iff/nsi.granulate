import unittest
import testGranulate, testGranulateOffice, testGranulateDOC, testGranulatePDF, testGranulateSVG, testGranulateVideo, testComparaHistograma, testGranulateOpenXML

def test_main():
    suite = unittest.TestSuite()
    for testcase in (testGranulate.TestGranulate,
                              testGranulateOffice.TestGranulateOffice,
                              testGranulateDOC.TestGranulateDoc,
                              testGranulatePDF.TestGranulatePDF,
                              testGranulateSVG.TestGranulateSVG,
                              testGranulateVideo.TestGranulateVideo,
                              testComparaHistograma.TestComparaImage,
                              testGranulateOpenXML.TestGranulateOpenXML,
                             ):
        suite.addTest(unittest.makeSuite(testcase))
    unittest.TextTestRunner().run(suite)

if __name__ == '__main__':
    test_main()
