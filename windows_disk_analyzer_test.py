import unittest
from windows_disk_analyzer import WindowsDiskAnalyzer,ConvertPathToCygwinPath

class TestWindowsDiskAnalyzer(unittest.TestCase):
    def test_outputCorrectlyParsed(self):
        with open("logicaldisk.out","r",encoding="utf-16") as file:
            content=file.readlines()
        wda=WindowsDiskAnalyzer()
        goodict=dict()
        goodict["LUBUNTU 18_"]="E:"
        outputdict=wda.getDictionnaryOfKeyAndDrive(content)
        self.assertEqual(goodict,outputdict," extracting dictionnary of drive out of output")


    def test_outputCorrectlyParsed_ActuallyLaunchingCommand(self):
        wda=WindowsDiskAnalyzer()
        goodict=dict()
        goodict["LUBUNTU 18_"]="E:"
        outputdict=wda.getDictionnaryOfKeyAndDrive()
        self.assertEqual(goodict,outputdict," extracting dictionnary of drive out of output")

class TestConvertPathToCygwin(unittest.TestCase):
    def test_ConvertPathToCygwin(self):
        convertedpath='/cygdrive/c/Users/foo/bar'
        self.assertEqual(convertedpath,ConvertPathToCygwinPath("C:\\Users\\foo\\bar"))
    def test_ConvertPathToCygwinWithTrailingSlash(self):
        convertedpath='/cygdrive/c/Users/foo/bar/'
        self.assertEqual(convertedpath,ConvertPathToCygwinPath("C:\\Users\\foo\\bar\\"))

if __name__ == '__main__':
    unittest.main()