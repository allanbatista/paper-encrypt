import os
import glob
import getpass
import argparse

from paper_encrypt.decryptor import decrypt_qr
from paper_encrypt.encryptor import encrypt_file


def main():
    parser = argparse.ArgumentParser(description="Encrypt or decrypt files using AES and QR codes.")
    parser.add_argument("--encrypt", action="store_true", help="Encrypt a file and generate a QR code in a PDF.")
    parser.add_argument("--decrypt", action="store_true", help="Decrypt a QR code from an image.")
    parser.add_argument("--export", type=str, help="Export format. pdf|img|txt. default=pdf. multiple formats is "
                                                   "separed by comman. --export=pdf,img,txt", default='pdf')
    parser.add_argument("--title", type=str, help="Title to add to the generated PDF.", default=None)
    parser.add_argument("--output_path", type=str, help="Title to add to the generated PDF.", default=None)
    parser.add_argument("file_path", type=str, help="Path to the file to encrypt or decrypt.")

    args = parser.parse_args()

    if args.encrypt and args.decrypt:
        print("Error: You cannot use --encrypt and --decrypt at the same time.")
        return

    if not args.encrypt and not args.decrypt:
        print("Error: You must specify either --encrypt or --decrypt.")
        return

    export_formats = [x.strip() for x in args.export.lower().split(',')]

    for ef in export_formats:
        if ef not in ['pdf', 'img', 'txt']:
            print("Error: Export is only allowed pdf, img or txt")
            return

    file_path = args.file_path

    if not file_path.startswith('/') and (os.environ.get('BASE_PATH') or os.environ.get('BASE_PATH') != ''):
        file_path = os.path.join(os.environ.get('BASE_PATH'), file_path)

    file_paths = glob.glob(file_path)

    output_path = args.output_path

    if not output_path.startswith('/') and (os.environ.get('BASE_PATH') or os.environ.get('BASE_PATH') != ''):
        output_path = os.path.join(os.environ.get('BASE_PATH'), output_path)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    password = getpass.getpass("Enter password: ")

    for file_path in file_paths:
        if args.encrypt:
            encrypt_file(file_path, password, title=args.title, export_formats=export_formats, output_path=output_path)
        elif args.decrypt:
            decrypt_qr(file_path, password, output_path=output_path)


if __name__ == "__main__":
    main()
