import getpass
from datetime import datetime, timezone
import argparse
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
import qrcode
from fpdf import FPDF
import cv2
import os


def encrypt_file(file_path, password, title=None):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return

    # Read the file content
    with open(file_path, 'r') as f:
        data = f.read()

    # Encrypt the data using AES
    key = password.encode('utf-8').ljust(32, b' ')[:32]
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    encrypted_data = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    encrypted_content = b64encode(iv + encrypted_data).decode('utf-8')

    # Generate QR code
    qr = qrcode.QRCode()
    qr.add_data(encrypted_content)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")

    pdf = FPDF()
    pdf.add_page()

    if title:
        pdf.set_font("Arial", size=16)
        pdf.cell(200, 5, txt=title, ln=True, align='C')

    pdf.set_font("Arial", size=8)
    pdf.cell(200, 5, txt=datetime.now(timezone.utc).isoformat(), ln=True, align='C')

    qr_image.save("temp_qr.png")
    pdf.image("temp_qr.png", x=(210 - 100) / 2, y=20, w=100)  # Move QR code slightly below the title and center it
    os.remove("temp_qr.png")

    pdf.set_font("Arial", size=10)
    pdf.ln(100)  # Ensure proper spacing below the QR code
    pdf.cell(200, 10, txt="Encrypted Text:", ln=True, align='C')
    pdf.multi_cell(0, 5, txt=encrypted_content, border=True)

    output_pdf = os.path.splitext(file_path)[0] + "_encrypted.pdf"
    pdf.output(output_pdf)

    print(f"Encrypted content saved as QR code in: {output_pdf}")

def decrypt_qr(image_path, password):
    if not os.path.exists(image_path):
        print(f"Error: File '{image_path}' does not exist.")
        return

    # Read QR code from image
    qr_image = cv2.imread(image_path)
    detector = cv2.QRCodeDetector()
    encrypted_content, _, _ = detector.detectAndDecode(qr_image)

    if not encrypted_content:
        print("No QR code detected or QR code is empty.")
        return

    # Decrypt the content
    key = password.encode('utf-8').ljust(32, b' ')[:32]
    try:
        encrypted_data = b64decode(encrypted_content)
        iv = encrypted_data[:AES.block_size]
        encrypted_message = encrypted_data[AES.block_size:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(encrypted_message), AES.block_size).decode('utf-8')

        # Write decrypted content to a new file
        output_file = os.path.splitext(image_path)[0] + "_decrypted.txt"
        with open(output_file, 'w') as f:
            f.write(decrypted_data)

        print(f"Decrypted content saved to: {output_file}")
    except Exception as e:
        print("Decryption failed. Ensure the password is correct and the QR code is valid.")
        print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Encrypt or decrypt files using AES and QR codes.")
    parser.add_argument("--encrypt", action="store_true", help="Encrypt a file and generate a QR code in a PDF.")
    parser.add_argument("--decrypt", action="store_true", help="Decrypt a QR code from an image.")
    parser.add_argument("--title", type=str, help="Title to add to the generated PDF.", default=None)
    parser.add_argument("file_path", type=str, help="Path to the file to encrypt or decrypt.")

    args = parser.parse_args()

    if args.encrypt and args.decrypt:
        print("Error: You cannot use --encrypt and --decrypt at the same time.")
        return

    if not args.encrypt and not args.decrypt:
        print("Error: You must specify either --encrypt or --decrypt.")
        return

    password = getpass.getpass("Enter password: ")

    if args.encrypt:
        encrypt_file(args.file_path, password, args.title)
    elif args.decrypt:
        decrypt_qr(args.file_path, password)


if __name__ == "__main__":
    main()
