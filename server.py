from fastapi import  FastAPI
from fastapi.cors.middleware import CORSMiddleware
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

#user crud operations

class User(BaseModel):
    name : str
    email : str
    password : str

@app.get('/user')
async def get_user(email: str):
    filter = {
        'email' : email
    }
    try :
        return dict(client.nz.user.find_one(filter=filter))
    except Exception as e:
        return {'status': 400, 'message': str(e)}

@app.post('/user')
async def create_user(user: User):
    try :
        client.nz.user.insert_one(dict(user))
        return {'status': 200, 'message':{'user added successfully'}}
    except Exception  as e:
        return {'status': 400 , 'message': str(e)}

class Cuser(BaseModel):
    email : str
    key : str
    value : str

@app.put('/user')
async def update_user(user: Cuser):
    try :
        filter = {
            'email' : user.email
        }
        update = {
            '$set' : {
                user.key : user.value
            }
        }
        client.nz.user.update_one(filter=filter, update=update)
        return {'status': 200, 'message':{'user updated successfully'}}
    except Exception as e:
        return {'status': 400 , 'message': str(e)}

@app.delete('/user')
async def delete_user(email: str):
    try :
        filter ={
            'email':email
        }
        client.nz.user.delete_one(filter)
        return {'status':200 , 'message' :"user deleted successfully"}
    except Exception as  e:
        return {'status': 400 , 'message': str(e)}

# api to check if the username is unique or not

@app.get('/check_username')
async def check_username(email: str):
    filter = {
        'email' : email
    }
    try :
        if(client.nz.user.count_documents(filter)) ==0 : 
            return True
        else:
            return False
    except Exception as e: 
        return {'status': 400 , 'message': str(e)}
