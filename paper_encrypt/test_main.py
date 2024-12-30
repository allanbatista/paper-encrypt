import os
import unittest
from paper_encrypt.main import encrypt_file, decrypt_pdf, decrypt_img, decrypt_txt

class TestPaperEncrypt(unittest.TestCase):

    def setUp(self):
        """Setup temporary directory and files for testing."""
        self.temp_dir = "/tmp"
        self.test_file = os.path.join(self.temp_dir, "test_file.txt")
        self.password = "securepassword"
        with open(self.test_file, "w") as f:
            f.write("This is a test file.")

    def tearDown(self):
        """Clean up temporary files."""
        for ext in ["_encrypted.pdf", "_encrypted.txt", "_encrypted.png", "_decrypted.txt"]:
            temp_file = self.test_file.replace(".txt", ext)
            if os.path.exists(temp_file):
                os.remove(temp_file)
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_encrypt_file_creates_pdf_img_and_txt(self):
        """Test if encrypt_file files are created"""
        encrypt_file(self.test_file, self.password, title="Test Title", export_formats=['pdf', 'txt', 'img'])
        for ext in ['pdf', 'txt', 'img']:
            ext = 'png' if ext == 'img' else ext
            encrypted_file = self.test_file.replace(".txt", f"_encrypted.{ext}")
            self.assertTrue(os.path.exists(encrypted_file), f"Encrypted {ext} was not created.")

    def test_encrypt_decrypt_txt(self):
        """Test encryption and decryption using txt format."""
        encrypt_file(self.test_file, self.password, title="Test Title", export_formats=['txt'])
        encrypted_file = self.test_file.replace(".txt", "_encrypted.txt")
        self.assertTrue(os.path.exists(encrypted_file), "Encrypted txt file was not created.")

        decrypt_txt(encrypted_file, self.password)
        decrypted_file = self.test_file.replace(".txt", "_encrypted_decrypted.txt")
        self.assertTrue(os.path.exists(decrypted_file), "Decrypted txt file was not created.")

        with open(decrypted_file, "r") as f:
            content = f.read()
        self.assertEqual(content, "This is a test file.", "Decrypted content does not match original.")

    def test_encrypt_decrypt_img(self):
        """Test encryption and decryption using img format."""
        encrypt_file(self.test_file, self.password, title="Test Title", export_formats=['img'])
        encrypted_file = self.test_file.replace(".txt", "_encrypted.png")
        self.assertTrue(os.path.exists(encrypted_file), "Encrypted image file was not created.")

        decrypt_img(encrypted_file, self.password)
        decrypted_file = self.test_file.replace(".txt", "_encrypted_decrypted.txt")
        self.assertTrue(os.path.exists(decrypted_file), "Decrypted txt file was not created.")

        with open(decrypted_file, "r") as f:
            content = f.read()
        self.assertEqual(content, "This is a test file.", "Decrypted content does not match original.")

    def test_encrypt_decrypt_pdf(self):
        """Test encryption and decryption using pdf format."""
        encrypt_file(self.test_file, self.password, title="Test Title", export_formats=['pdf'])
        encrypted_file = self.test_file.replace(".txt", "_encrypted.pdf")
        self.assertTrue(os.path.exists(encrypted_file), "Encrypted pdf file was not created.")

        decrypt_pdf(encrypted_file, self.password)
        decrypted_file = self.test_file.replace(".txt", "_encrypted_decrypted.txt")
        self.assertTrue(os.path.exists(decrypted_file), "Decrypted txt file was not created.")

        with open(decrypted_file, "r") as f:
            content = f.read()
        self.assertEqual(content, "This is a test file.", "Decrypted content does not match original.")

if __name__ == "__main__":
    unittest.main()
