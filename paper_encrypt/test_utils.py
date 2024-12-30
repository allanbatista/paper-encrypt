import unittest
from paper_encrypt.utils import get_file_ext

class TestGetFileExt(unittest.TestCase):
    def test_pdf_extension(self):
        self.assertEqual(get_file_ext('document.pdf'), 'pdf')

    def test_png_extension(self):
        self.assertEqual(get_file_ext('image.png'), 'img')

    def test_jpg_extension(self):
        self.assertEqual(get_file_ext('photo.jpg'), 'img')

    def test_jpeg_extension(self):
        self.assertEqual(get_file_ext('picture.jpeg'), 'img')

    def test_default_extension(self):
        self.assertEqual(get_file_ext('notes.o'), None)

if __name__ == '__main__':
    unittest.main()