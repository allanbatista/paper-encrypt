import os
from base64 import b64encode
from datetime import datetime, timezone

import qrcode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from fpdf import FPDF


def encrypt_file(file_path, password, title=None, export_formats=['pdf']):
    if not os.path.exists(file_path):
        raise Exception(f"File '{file_path}' does not exist.")

    # Read the file content
    with open(file_path, 'r') as f:
        data = f.read()

    # Encrypt the data using AES
    key = password.encode('utf-8').ljust(32, b' ')[:32]
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    encrypted_data = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    encrypted_content = b64encode(iv + encrypted_data).decode('utf-8')

    if 'txt' in export_formats:
        output_txt = os.path.splitext(file_path)[0] + "_encrypted.txt"
        with open(output_txt, 'w+') as f:
            f.write(encrypted_content)
        print(f"Encrypted content saved as QR code in: {output_txt}")

    # Generate QR code
    qr = qrcode.QRCode()
    qr.add_data(encrypted_content)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")

    if 'img' in export_formats:
        output_img = os.path.splitext(file_path)[0] + "_encrypted.png"
        qr_image.save(output_img)
        print(f"Encrypted content saved as QR code in: {output_img}")

    if 'pdf' not in export_formats:
        return

    pdf = FPDF()
    pdf.add_page()

    if title:
        pdf.set_font("Arial", size=16)
        pdf.cell(200, 5, txt=title, ln=True, align='C')

    pdf.set_font("Arial", size=8)
    pdf.cell(200, 5, txt=datetime.now(timezone.utc).isoformat(), ln=True, align='C')

    qr_image.save("temp_qr.png")
    pdf.image("temp_qr.png", x=(210 - 100) / 2, y=20, w=100)
    os.remove("temp_qr.png")

    pdf.set_font("Arial", size=10)
    pdf.ln(100)  # Ensure proper spacing below the QR code
    pdf.cell(200, 10, txt="Encrypted Text:", ln=True, align='C')
    pdf.multi_cell(0, 5, txt=encrypted_content, border=True)

    output_pdf = os.path.splitext(file_path)[0] + "_encrypted.pdf"
    pdf.output(output_pdf)

    print(f"Encrypted content saved as QR code in: {output_pdf}")
