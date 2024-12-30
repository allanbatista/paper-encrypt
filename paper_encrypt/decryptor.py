import os
from base64 import b64decode
from io import BytesIO

import cv2
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from pdf2image import convert_from_path


def decrypt(encrypted_content, password, file_path):
    # Decrypt the content
    key = password.encode('utf-8').ljust(32, b' ')[:32]
    try:
        encrypted_data = b64decode(encrypted_content)
        iv = encrypted_data[:AES.block_size]
        encrypted_message = encrypted_data[AES.block_size:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(encrypted_message), AES.block_size).decode('utf-8')

        # Write decrypted content to a new file
        output_file = os.path.splitext(file_path)[0] + "_decrypted.txt"
        with open(output_file, 'w') as f:
            f.write(decrypted_data)

        print(f"Decrypted content saved to: {output_file}")
    except Exception as e:
        print("Decryption failed. Ensure the password is correct and the QR code is valid.")
        print(f"Error: {e}")


def get_file_ext(file_path):
    if file_path.endswith('.pdf'):
        return 'pdf'

    if file_path.endswith('png') or file_path.endswith('jpg') or file_path.endswith('jpeg'):
        return 'img'

    return 'txt'


def decrypt_txt(file_path, password):
    with open(file_path, 'r') as f:
        decrypt(f.read(), password, file_path)


def decrypt_img(file_path, password):
    # Read QR code from image
    qr_image = cv2.imread(file_path)
    detector = cv2.QRCodeDetector()
    encrypted_content, _, _ = detector.detectAndDecode(qr_image)

    if not encrypted_content:
        print("No QR code detected or QR code is empty.")
        return

    decrypt(encrypted_content, password, file_path)


def decrypt_pdf(file_path, password):
    # Convert the first page of the PDF to an image
    pages = convert_from_path(file_path)

    if len(pages) != 1:
        print("Only permitted PDFs with 1 page.")
        return

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
        print("No QR code detected or QR code is empty.")
        return

    decrypt(encrypted_content, password, file_path)


def decrypt_qr(file_path, password):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return

    ext = get_file_ext(file_path)

    if ext == 'txt':
        return decrypt_txt(file_path, password)

    if ext == 'pdf':
        return decrypt_pdf(file_path, password)

    if ext == 'img':
        return decrypt_img(file_path, password)

    print('Extension is not supported')