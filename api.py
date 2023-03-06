from fastapi import  FastAPI
from fastapi.middleware.cors import CORSMiddleware
import datetime
from fastapi import FastAPI,File , UploadFile,Form
from pymongo import MongoClient
from pydantic import BaseModel

client = MongoClient('mongodb://localhost:27017/')

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
    )
@app.get('/')
async def get():
    return {'status': 200 , 'message': 'Success'}

@app.post("/upload")
def upload(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}

@app.post('/uploadugpdf')
async def uploadug(apikey :str = Form(),filename: str = Form(), file : UploadFile = File(...)):
    path = os.path.join(email,filename+".pdf")
    try:
        contents = file.file.read()
        with open(path, 'wb') as f:
            f.write(contents)
    except Exception as e:
        return {'status':400 , 'message': str(e)}
    finally:
        file.file.close()
        return True
