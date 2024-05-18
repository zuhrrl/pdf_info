
import pypdfium2 as pdfium
from fastapi import FastAPI, File, UploadFile
import shutil

PAGEINDEX = 0  # the first page
FILEPATH = ""

def getOrientation(width, height):
    if width > height:
        return 'LANDSCAPE'
    return 'POTRAIT'

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    path = f"files/document.pdf"
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    pdf = pdfium.PdfDocument('files/document.pdf')
    width, height = pdf.get_page_size(PAGEINDEX)
    
    return {"status": True, "message" : "success get pdf info", "original_file_name": file.filename, 'width': round(width), 'height': round(height), 'orientation': getOrientation(width, height)}

