import uvicorn
from fastapi import FastAPI, File, UploadFile, Form
from pyresparser import ResumeParser
import shutil
import os
from datetime import datetime

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.post('/resume_parse')
def parse(file: UploadFile = File(...)):
    time_str = datetime.now().strftime("%Y%m%d-%H%M%S")
    file_name = time_str + str(file.filename)
    path = os.path.abspath(os.sep) + "tmp"
    if not os.path.isdir(path):
        os.mkdir(path)
    os.chdir(path)
    with open(file_name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    data = ResumeParser(file_name).get_extracted_data()
    os.remove(file_name)
    return data

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)