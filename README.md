# PaperEncrypt: Encrypt and Decrypt Files with QR Codes

PaperEncrypt is a Python tool for encrypting and decrypting files using AES encryption and QR codes. The encrypted data can be exported in multiple formats, including PDF, image (PNG), and text. Decryption supports reading QR codes directly from these formats, making it versatile for secure data sharing.

## Features
- **Encrypt files**: Supports AES encryption with user-provided passwords.
- **Generate QR codes**: Encrypted content is embedded into QR codes.
- **Multiple export formats**: PDF, image, and plain text.
- **Decrypt files**: Extract encrypted data from QR codes and restore the original content.
- **All-in-memory processing**: Uses in-memory buffers for improved performance.

**PaperCrypt: Secure Offline Analog Storage Tool**

**Overview**

PaperCrypt is a tool designed to securely store data offline in an analog format. It encrypts a text file and provides options to export the encrypted data as a PDF, image, or plain text. When exporting to PDF or image formats, a QR code containing the encrypted data is generated, making it easy to print and store. The data is encrypted using AES encryption and is protected by a password. Note: The password is unrecoverable, so it must be stored securely.

The primary purpose of PaperCrypt is to enable secure, analog storage of small pieces of sensitive data, such as passwords or cryptocurrency wallet public and private keys.

---

**Steps for Secure Storage**

1. Write your data in a `.txt` file.
2. Encrypt the data using PaperCrypt. (Do not lose the password as it cannot be recovered.)
3. Print at least two copies of the generated QR code and store them securely in geographically separated locations.
4. Delete the `.txt` file and any encrypted files from your computer. (Remember to clear your trash bin.)
5. Done! Your credentials are now securely stored offline.

---

**Steps to Decrypt Data**

1. Take a photo or scan the generated QR code.
2. Use PaperCrypt to decrypt the data using the saved QR code and your password.

**Disclaimer:**
Ensure you follow the recommended steps for secure storage and do not lose the password. Failure to do so may result in permanent loss of access to your encrypted data.

---

## Prerequisites

### Python Version
Ensure you have Python 3.7 or later installed.

### Required Libraries
Install the following Python libraries:
- `fpdf`
- `qrcode`
- `pycryptodome`
- `cv2` (OpenCV)
- `pdf2image`
- `numpy`

You can install all dependencies using:
```bash
pip install -r requirements.txt
```

### Additional Requirements
For `pdf2image`, you must install `poppler`. Instructions vary by operating system:
- **Ubuntu**: `sudo apt-get install poppler-utils`
- **MacOS**: `brew install poppler`
- **Windows**: Download the precompiled binaries from [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases) and add the `bin` directory to your PATH.
---

## Usage

### Command Line Interface
The tool provides a CLI interface for encryption and decryption.

```bash
python main.py --encrypt --file_path <file_path> [--export pdf,img,txt] [--title <title>]
python main.py --decrypt --file_path <file_path>
```

#### Parameters:
- `--encrypt`: Encrypt the file.
- `--decrypt`: Decrypt the file.
- `--export`: Specify export formats (comma-separated): `pdf`, `img`, `txt` (default: `pdf`).
- `--output_path`: (Optional) Path to save the output files.
- `--title`: (Optional) Title to add to the PDF.
- `file_path`: Path to the file to encrypt or decrypt.

### Example Commands

#### Encrypt a file to PDF and PNG
```bash
python main.py --encrypt --file_path /path/to/file.txt --export pdf,img --title "My Encrypted File"
```

#### Encrypt a pattern of files
```bash
python main.py --encrypt --title "My Encrypted File" "/path/to/*.txt"
```

#### Decrypt a QR code from a PDF
```bash
python main.py --decrypt --file_path /path/to/encrypted_file_encrypted.pdf
```

#### Decrypt a pattern of files
```bash
python main.py --decrypt --output_path=decrypt "/path/to/*.pdf"
```

---

## Programmatic Usage
The tool provides `encrypt_file` and `decrypt_qr` functions for integration into your own projects.

### Encrypt a File
```python
from paper_encrypt.main import encrypt_file

file_path = "test_file.txt"
password = "securepassword"
encrypt_file(file_path, password, title="Secure Data", export_formats=['pdf', 'img'])
```

### Decrypt a File
```python
from paper_encrypt.main import decrypt_qr

encrypted_file_path = "test_file_encrypted.pdf"
password = "securepassword"
decrypt_qr(encrypted_file_path, password)
```

---

## Testing
The project includes unit tests to verify its functionality. Run the tests with:
```bash
python -m unittest discover
```

---

## Security Notes
- Use strong passwords to ensure the safety of your encrypted data.
- Keep your password safe; decryption is impossible without it.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contact
For issues or feature requests, please contact the developer or submit an issue on the project repository.

