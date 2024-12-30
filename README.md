# Paper Encrypt

**Paper Encrypt** is a CLI tool for encrypting and decrypting files using AES encryption and QR codes. It supports exporting encrypted data as PDFs, images, or plain text.

## Features
- Encrypt files with AES encryption.
- Generate QR codes and export as PDF, image, or text file.
- Decrypt QR codes to extract encrypted data.

## Usage

```bash
python main.py --encrypt --title "Secure Document" /path/to/file.txt
```

* --encrypt: Encrypt a file and generate QR code(s).
* --decrypt: Decrypt QR code(s) to retrieve data.
* --title: Add a title to the PDF.
* file_path: Path to the file to encrypt or decrypt.