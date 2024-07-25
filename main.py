from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
import uuid
import pypdfium2 as pdfium
from convert_to_pdf import convert_to_pdf, pdf_to_base64
from fastapi.responses import FileResponse
from merge import merge_pdfs
from typing import List

PAGEINDEX = 0  # Default page index

def getRandomString(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    random = random.upper() # Make all characters uppercase.
    random = random.replace("-","") # Remove the UUID '-'.
    return random[0:string_length]

def getOrientation(width, height):
    if width > height:
        return 'LANDSCAPE'
    return 'POTRAIT'

app = FastAPI()

# Tambahkan middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ganti dengan daftar asal yang diizinkan
    allow_credentials=True,
    allow_methods=["*"],  # Ganti dengan daftar metode yang diizinkan
    allow_headers=["*"],  # Ganti dengan daftar header yang diizinkan
)

@app.get("/")
def root():
    return {"message": "Hello World"}

class Item(BaseModel):
    page: int

@app.post("/uploadfile/")
async def create_upload_file(
    file: UploadFile = File(...),
    page: int = Form(...)
):
    fileName = getRandomString(20)
    path = f"files/{fileName}.pdf"
    
    # Save uploaded file
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Open PDF and get page size
    pdf = pdfium.PdfDocument(path)
    width, height = pdf.get_page_size(page)  # Use page from form data
    os.remove(path)  # Clean up

    return {
        "status": True,
        "message": "success get pdf info",
        "original_file_name": file.filename,
        'width': round(width),
        'height': round(height),
        'orientation': getOrientation(width, height)
    }

@app.post("/convert-to-pdf/")
async def convert_to_pdf_endpoint(file: UploadFile = File(...)):
    # Ensure 'files' directory exists
    if not os.path.exists('files'):
        os.makedirs('files')

    # Generate random file name
    file_extension = os.path.splitext(file.filename)[1]
    fileName = getRandomString(20)
    input_path = f"files/{fileName}{file_extension}"
    output_dir = "pdf"
    
    # Save uploaded file
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Convert file to PDF
    output_file = convert_to_pdf(input_path, output_dir)
    os.remove(input_path)
    if output_file is None:
        return {"status": False, "message": "Error during conversion"}
    output_file = f"{output_dir}/{fileName}.pdf"

    return FileResponse(output_file, media_type='application/pdf', filename=os.path.basename(output_file))

@app.post("/merge-pdfs/")
async def merge_pdfs_endpoint(files: List[UploadFile] = File(...)):
    # Ensure 'files' directory exists
    if not os.path.exists('files'):
        os.makedirs('files')

    # Generate random file name for output
    output_file_name = getRandomString(20) + ".pdf"
    output_path = f"files/{output_file_name}"
    
    # Save uploaded files
    pdf_paths = []
    for file in files:
        file_name = getRandomString(20) + os.path.splitext(file.filename)[1]
        file_path = f"files/{file_name}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        pdf_paths.append(file_path)
    
    # Merge PDFs
    merge_pdfs(pdf_paths, output_path)

    # Clean up individual PDF files
    for pdf_path in pdf_paths:
        os.remove(pdf_path)

    return FileResponse(output_path, media_type='application/pdf', filename=output_file_name)
