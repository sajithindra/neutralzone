from fastapi import FastAPI 
from os import listdir
from os.path import isfile, join
from fastapi.responses import FileResponse
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

## api to test connection
@app.get('/')
async def get():
    return {'status': 200 , 'message': 'Success'}

#api to upload file
@app.post('/upload')
async def upload_file(email : str = Form() ,apikey :str = Form(), project_name: str = Form(),file : UploadFile = File(...)):
    path = join(email,project_name,file.filename)
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

# api to get file list 
@app.get('/files')
async def get_files(email :str):
    files = [f for f in listdir(email) if isfile(join(email, f))]
    return files

#api to download file
class Download(BaseModel):
    email :str
    apikey :str
    filename :str

@app.post('/download')
async def download(download : Download):
    filter = {
        "email" : download.email,
        "apikey" : download.apikey
    }
    if (client.nz.user.count_documents(filter)) == 1 :
        path = join(download.email,download.filename)
        return FileResponse(path)
    else : return { 'status ' : 400, "message" : "user or api not found"}

#api to share file with another user
class FileShare(BaseModel):
    data_source_email :str
    data_source_apikey :str
    data_source_filename :str
    destination_email: str
    destination_apikey :str

@app.post('/file_share')
async def file_share(fileshare : FileShare):
    filter = {
        'email' : fileshare.data_source_email,
        'apikey' : fileshare.data_source_apikey
    }
    if (client.nz.user.count_documents(filter)) == 1 :
        filter = {
            'email' : fileshare.destination_email,
            'apikey' : fileshare.destination_apikey
        }
        if (client.nz.user.count_documents(filter)) == 1 :
            try:
                client.nz.fileshare.insert_one(dict(fileshare))
                return {'status': 200 , 'message': 'filesharing initiated'}
            except Exception as e:
                return {'status': 400 , 'message': 'filesharing failed'}
        else:
            return {'status':400 , 'message': "destination account is invalid"}
    else :
        return {'status':400 , 'message':'data source account is invalid'}

# api to share folder with another user

class FolderShare(BaseModel):
    data_source_email :str
    data_source_apikey :str
    data_source_foldername :str
    destination_email: str
    destination_apikey :str

@app.post('/folder_share')
async def folder_share(foldershare:FolderShare):
    filter = {
        'email' : foldershare.data_source_email,
        'apikey' : foldershare.data_source_apikey
    }
    if (client.nz.user.count_documents(filter)) == 1 :
        filter = {
            'email' : foldershare.destination_email,
            'apikey' : foldershare.destination_apikey
            }
        if (client.nz.user.count_documents(filter)) == 1 :
            try:
                client.nz.foldershare.insert_one(dict(foldershare))
                return {'status': 200 , 'message': 'foldersharing request initiated'}
            except Exception as e:
                return {'status':400 , 'message': 'foldersharing request failed'}
        else:
            return {'status':400 , 'message': "destination account is invalid"}
    else :
        return {'status':400 , 'message':'data source account is invalid'}

    