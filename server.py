from fastapi import  FastAPI
from fastapi.middleware.cors import CORSMiddleware
import datetime
from pymongo import MongoClient
from pydantic import BaseModel
import random, string

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
    project={
        '_id':0
    }
    try :
        return dict(client.nz.user.find_one(filter=filter,projection=project))
    except Exception as e:
        return {'status': 400, 'message': str(e)}

@app.post('/user')
async def create_user(user: User):
    try :
        client.nz.user.insert_one(dict(user))
        return {'status': 200, 'message':'user added successfully'}
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
        return {'status': 200, 'message':'user updated successfully'}
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

# api to generate random id

@app.get('/apikey')
async def generate_key(email:str):
    apikey = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
    try : 
        filter = {
            'email' : email
        }
        update = {
            '$set': {
                'apikey' : apikey,
                'datetime' : datetime.datetime.now()
            }
        }
        client.nz.user.update_one(filter=filter, update=update)
        return {'status': 200, 'message':'apikey generated successfully', 'apikey' : apikey}
    except Exception  as e:
        return {'status': 400 , 'message': str(e)}

@app.get('/check_apikey')
async def check_apikey(email:str):
    filter = {
        'email' : email
    }
    project ={
        '_id':0,
        'apikey' : 1,
        'expiry_date':1
    }
    user = dict(client.nz.user.find_one(filter=filter,projection=project))
    

#api for payment details

class Payment(BaseModel):
    email :str
    apikey :str
    amount :float
    mode : str
    status : str 
    datetime : str = datetime.datetime.now()

@app.get('/payment')
async def get_payment(email:str):
    try :
        filter = { 
        'email' :email,
        }
        project ={
            "_id":0
        }
        return list(client.nz.payment.find(filter=filter,projection=project))
    except Exception as e:
        return { 'status' : 400 , 'message' : str(e)}


@app.post('/payment')
async def payment(payment: Payment):
    try :
        client.nz.payment.insert_one(dict(payment))
        filter = {
            'email' : payment.email,
        }
        update = {
            '$set':
            {
                'status' : "active",
                'expiry_date' : datetime.datetime.now()+datetime.timedelta(days=31)
            }
        }
        client.nz.payment.update_one(filter=filter,update=update)
        return {'status': 200, 'message':'payment added successfully'}
    except Exception as e:
        return {'status': 400 , 'message': str(e)}
    