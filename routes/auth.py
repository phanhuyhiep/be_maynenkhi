from fastapi import APIRouter, HTTPException
from bson import ObjectId
from models.model import Auth
from config.database import collection_auth
from schema.auth import list_auth, auth_seriral
from passlib.hash import pbkdf2_sha256
from jose import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
router_auth = APIRouter()

#register
@router_auth.post("/auth/register")
async def register(auth:Auth):
    check_user = collection_auth.find_one({"email": auth.email})
    if check_user:
        raise HTTPException(status_code=400, detail="User da ton tai")

    hash_password = pbkdf2_sha256.hash(auth.password)
    
    new_user = {
        "name": auth.name,
        "email": auth.email,
        "password": hash_password,
        "role": auth.role
    }
    
    collection_auth.insert_one(new_user)   
    return{"message": "Tạo tài khoản thành công"}

#login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
@router_auth.post("/auth/login")
async def login(auth:Auth):
    check_user = collection_auth.find_one({"email": auth.email})
    if not check_user:
        raise HTTPException(status_code=401, detail="Tài khoản không tồn tại")
    #verify password
    hashed_password = check_user["password"]
    if not pbkdf2_sha256.verify(auth.password, hashed_password):
        raise HTTPException(status_code=401, detail="Sai password")

    token = create_access_token(str(check_user["_id"]))
    
    return {"access_token": token}

def create_access_token(auth_id: str):
    access_token = jwt.encode(
        claims = {
            "id": auth_id,
            "exp": datetime.utcnow() + timedelta(minutes=30),
        },
        key = "be-page",
        algorithm="HS256",
    )
    return access_token

@router_auth.get("/auth/")
async def get_auth():
    auth = list_auth(collection_auth.find())
    return auth
  
@router_auth.get("/auth/{id}")
async def get_one_auth( id: str):
    auth = collection_auth.find_one({"_id": ObjectId(id)})
    return auth_seriral(auth)

@router_auth.put("/auth/edit/{id}")
async def edit_auth(id: str, auth:Auth):
    collection_auth.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(auth)})
    return {"message": "OK"}

@router_auth.delete("/auth/delete/{id}")
async def delete_auth(id:str):
    collection_auth.find_one_and_delete({"_id": ObjectId(id)})
    return {"message": "OK"} 
