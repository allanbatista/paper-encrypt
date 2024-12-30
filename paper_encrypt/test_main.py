import os
import unittest

from fpdf import FPDF

from paper_encrypt.decryptor import decrypt_qr
from paper_encrypt.encryptor import encrypt_file


class TestPaperEncrypt(unittest.TestCase):

    def setUp(self):
        """Setup temporary directory and files for testing."""
        self.temp_dir = "/tmp"
        self.test_file = os.path.join(self.temp_dir, "test_file.txt")
        self.password = "securepassword"
        with open(self.test_file, "w") as f:
            f.write("This is a test file.")

        self.test_file_not_supported = os.path.join(self.temp_dir, "test_file.o")
        with open(self.test_file_not_supported, "w") as f:
            f.write("This is a test file.")

    # def tearDown(self):
    #     """Clean up temporary files."""
    #     for ext in ["_encrypted.pdf", "_encrypted.txt", "_encrypted.png", "_decrypted.txt"]:
    #         temp_file = self.test_file.replace(".txt", ext)
    #         if os.path.exists(temp_file):
    #             os.remove(temp_file)
    #
    #     if os.path.exists(self.test_file):
    #         os.remove(self.test_file)
    #
    #     if os.path.exists(self.test_file_not_supported):
    #         os.remove(self.test_file_not_supported)

    def test_encrypt_file_creates_pdf_img_and_txt(self):
        """Test if encrypt_file files are created"""
        encrypt_file(self.test_file, self.password, title="Test Title", export_formats=['pdf', 'txt', 'img'])
        for ext in ['pdf', 'txt', 'img']:
            ext = 'png' if ext == 'img' else ext
            encrypted_file = self.test_file + f"_encrypted.{ext}"
            self.assertTrue(os.path.exists(encrypted_file), f"Encrypted {ext} was not created.")

    def test_encrypt_decrypt_txt(self):
        """Test encryption and decryption using txt format."""
        encrypt_file(self.test_file, self.password, title="Test Title", export_formats=['txt'])
        encrypted_file = self.test_file + "_encrypted.txt"
        self.assertTrue(os.path.exists(encrypted_file), "Encrypted txt file was not created.")

        decrypt_qr(encrypted_file, self.password)
        decrypted_file = self.test_file +"_encrypted.txt_decrypted.txt"
        self.assertTrue(os.path.exists(decrypted_file), "Decrypted txt file was not created.")

        with open(decrypted_file, "r") as f:
            content = f.read()
        self.assertEqual(content, "This is a test file.", "Decrypted content does not match original.")

    def test_encrypt_decrypt_img(self):
        """Test encryption and decryption using img format."""
        encrypt_file(self.test_file, self.password, title="Test Title", export_formats=['img'])
        encrypted_file = self.test_file + "_encrypted.png"
        self.assertTrue(os.path.exists(encrypted_file), "Encrypted image file was not created.")

        decrypt_qr(encrypted_file, self.password)
        decrypted_file = self.test_file + "_encrypted.png_decrypted.txt"
        self.assertTrue(os.path.exists(decrypted_file), "Decrypted txt file was not created.")

        with open(decrypted_file, "r") as f:
            content = f.read()
        self.assertEqual(content, "This is a test file.", "Decrypted content does not match original.")

    def test_encrypt_decrypt_img_empty_image(self):
        """Test encryption and decryption using img format."""
        encrypt_file(self.test_file, self.password, title="Test Title", export_formats=['img'])
        encrypted_file = self.test_file + "_encrypted.png"
        self.assertTrue(os.path.exists(encrypted_file), "Encrypted image file was not created.")

        import PIL.Image as Image

        # create empty image
        img = Image.new('RGB', (1, 1), color = 'white')
        img.save(encrypted_file)

        try:
            decrypt_qr(encrypted_file, self.password)
        except Exception as e:
            self.assertEqual(str(e), "No QR code detected or QR code is empty.")

    def test_encrypt_decrypt_pdf(self):
        """Test encryption and decryption using pdf format."""
        encrypt_file(self.test_file, self.password, title="Test Title", export_formats=['pdf'])
        encrypted_file = self.test_file + "_encrypted.pdf"
        self.assertTrue(os.path.exists(encrypted_file), "Encrypted pdf file was not created.")

        decrypt_qr(encrypted_file, self.password)
        decrypted_file = self.test_file + "_encrypted.pdf_decrypted.txt"
        self.assertTrue(os.path.exists(decrypted_file), "Decrypted txt file was not created.")

        with open(decrypted_file, "r") as f:
            content = f.read()
        self.assertEqual(content, "This is a test file.", "Decrypted content does not match original.")

    def test_encrypt_decrypt_extension_not_supported(self):
        """Test encryption and decryption using pdf format."""
        try:
            decrypt_qr(self.test_file_not_supported, self.password)
        except Exception as e:
            self.assertEqual(str(e), "Export is only allowed pdf, img or txt")

    def test_encrypt_decrypt_pdf_with_empty_file(self):
        """Test encryption and decryption using pdf format with empty file."""
        encrypt_file(self.test_file, self.password, title="Test Title", export_formats=['pdf'])
        encrypted_file = self.test_file + "_encrypted.pdf"
        self.assertTrue(os.path.exists(encrypted_file), "Encrypted pdf file was not created.")

        # create empty pdf
        pdf = FPDF()
        pdf.add_page()
        pdf.output(encrypted_file)

        try:
            decrypt_qr(encrypted_file, self.password)
        except Exception as e:
            self.assertEqual(str(e), "No QR code detected or QR code is empty.")

    def test_decrypt_file_not_exists(self):
        """Test decryption with file that does not exist."""
        try:
            decrypt_qr("file_not_exists.txt", self.password)
        except Exception as e:
            self.assertEqual(str(e), "Error: File 'file_not_exists.txt' does not exist.")

    def test_encrypt_file_not_exists(self):
        """Test encryption with file that does not exist."""
        try:
            encrypt_file("file_not_exists.txt", self.password, title="Test Title", export_formats=['pdf'])
        except Exception as e:
            self.assertEqual(str(e), "File 'file_not_exists.txt' does not exist.")

if __name__ == "__main__":
    unittest.main()
