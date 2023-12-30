import os
import PyPDF2
import sys

def decrypt_pdfs(folder_path, master_password):
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)

            source = open(pdf_path, 'rb')
            reader = PyPDF2.PdfReader(source)

            if reader.is_encrypted:
                try:
                    reader.decrypt(master_password)
                    writer = PyPDF2.PdfWriter()

                    writer.append_pages_from_reader(reader)

                    dest = open(os.path.join(folder_path, filename.replace('.pdf', '_decrypted.pdf')), 'wb')
                    writer.write(dest)

                except Exception as e:
                    print(f'Failed to decrypt {filename}: {e}')
            else:
                print(f'{filename} is not encrypted')

if __name__ == "__main__":
    folder_path = sys.argv[1]
    master_password = sys.argv[2]
    decrypt_pdfs(folder_path, master_password)

