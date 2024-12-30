import os
from base64 import b64decode
from io import BytesIO

import cv2
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from pdf2image import convert_from_path

from paper_encrypt.utils import get_file_ext


def decrypt(encrypted_content, password, file_path, output_path):
    # Decrypt the content
    key = password.encode('utf-8').ljust(32, b' ')[:32]

    encrypted_data = b64decode(encrypted_content)
    iv = encrypted_data[:AES.block_size]
    encrypted_message = encrypted_data[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_message), AES.block_size).decode('utf-8')

    filename = os.path.basename(file_path)

    if output_path is None:
        output_path = os.path.dirname(file_path)

    output_filename = os.path.join(output_path, filename) + "_decrypted.txt"

    with open(output_filename, 'w') as f:
        f.write(decrypted_data)

    print(f"Decrypted content saved to: {output_filename}")


def decrypt_txt(file_path, password, output_path=None):
    with open(file_path, 'r') as f:
        decrypt(f.read(), password, file_path, output_path)


def decrypt_img(file_path, password, output_path=None):
    # Read QR code from image
    qr_image = cv2.imread(file_path)
    detector = cv2.QRCodeDetector()
    encrypted_content, _, _ = detector.detectAndDecode(qr_image)

    if not encrypted_content:
        raise Exception("No QR code detected or QR code is empty.")

    decrypt(encrypted_content, password, file_path, output_path)


def decrypt_pdf(file_path, password, output_path=None):
    # Convert the first page of the PDF to an image
    pages = convert_from_path(file_path)

    # Save the page image into an in-memory buffer
    buffer = BytesIO()
    pages[0].save(buffer, format="JPEG")
    buffer.seek(0)

    # Read the image from the buffer using OpenCV
    np_image = np.frombuffer(buffer.read(), np.uint8)
    qr_image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)

    # Detect and decode the QR code
    detector = cv2.QRCodeDetector()
    encrypted_content, _, _ = detector.detectAndDecode(qr_image)

    if not encrypted_content:
        raise Exception("No QR code detected or QR code is empty.")

    decrypt(encrypted_content, password, file_path, output_path)


def decrypt_qr(file_path, password, output_path=None):
    if not os.path.exists(file_path):
        raise Exception(f"Error: File '{file_path}' does not exist.")

    ext = get_file_ext(file_path)

    if ext is None:
        raise Exception('Export is only allowed pdf, img or txt')

    if ext == 'txt':
        return decrypt_txt(file_path, password, output_path)

    if ext == 'pdf':
        return decrypt_pdf(file_path, password, output_path)

    if ext == 'img':
        return decrypt_img(file_path, password, output_path)
