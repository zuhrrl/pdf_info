
import pypdfium2 as pdfium
from fastapi import FastAPI, File, UploadFile
import shutil
import os
import uuid


PAGEINDEX = 0  # the first page
FILEPATH = ""


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

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    fileName = getRandomString(20)
    path = f"files/{fileName}.pdf"
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    filePath = 'files/' + fileName + '.pdf'
    print(filePath)
    pdf = pdfium.PdfDocument(filePath)
    width, height = pdf.get_page_size(PAGEINDEX)
    os.remove(filePath) 
    
    return {"status": True, "message" : "success get pdf info", "original_file_name": file.filename, 'width': round(width), 'height': round(height), 'orientation': getOrientation(width, height)}

