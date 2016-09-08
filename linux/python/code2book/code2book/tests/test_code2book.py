import sys
import unittest

sys.path.append('..')
import code2book


class Test(unittest.TestCase):
    def setUp(self):
        ###  XXX code to do setup
        pass

    def tearDown(self):
        ###  XXX code to do tear down
        pass

    def test_splitPath(self):
        self.assertListEqual(code2book.splitPath('/test/test.txt'), ['/', 'test', 'test.txt'])
        self.assertListEqual(code2book.splitPath('test/test.txt'), ['test', 'test.txt'])
        self.assertListEqual(code2book.splitPath('test.txt'), ['test.txt'])
        self.assertListEqual(code2book.splitPath(''), [])

    def test_searchFileDirectory(self):
        fileList = code2book.searchFileDirectory('../')
        print(code2book.convertFileList('../', fileList, 1))

    def test_code2MarkdownText(self):
        print(code2book.code2MarkdownText('./test_code2book.py', chapterLevel=2))

if __name__ == '__main__':
    print(unittest.main())
