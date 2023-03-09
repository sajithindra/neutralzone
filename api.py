from fastapi import FastAPI 
import os
import uvicorn
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



@app.post('/upload')
async def upload_file(email : str = Form() ,apikey :str = Form(),filename: str = Form(), file : UploadFile = File(...)):
    path = os.path.join(email,filename+".pdf")
    filter ={
        'apikey':apikey,
        'email':email
    }
    if client.nz.user.count_documents(filter=filter) == 0:
        return {'status':800, 'message': 'apikey not found'}
    else:
        try:
            filter={
                'apikey' : apikey
            }
            project = {
                '_id':0,
                'email':1
            }
            email= dict(client.nz.user.find_one(filter=filter,projection=project))['email']
            contents = file.file.read()
            with open(path, 'wb') as f:
                f.write(contents)
        except Exception as e:
            return {'status':400 , 'message': str(e)}
        finally:
            file.file.close()
            return {'status':200 , 'message': 'Success','path':path}

class Download(BaseModel):
    email :str
    apikey :str
    filename :str

@app.get('/download')
async def download(download : Download):
    
