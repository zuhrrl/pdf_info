import subprocess
import os
import base64

def convert_to_pdf(doc_path, output_dir):
    """
    Mengonversi file dokumen ke PDF menggunakan LibreOffice.
    """
    subprocess.call(['soffice',
                 # '--headless',
                 '--convert-to',
                 'pdf',
                 '--outdir',
                 output_dir,
                 doc_path])
    print('bbbbbb',doc_path)
    return doc_path

def pdf_to_base64(pdf_path):
    """
    Membaca file PDF dan mengonversinya ke format base64.
    """
    with open(pdf_path, "rb") as pdf_file:
        pdf_data = pdf_file.read()
        base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
    return base64_pdf

convert_to_pdf('files/2C6D8E92CA8D415A992E.jpeg','ada')
