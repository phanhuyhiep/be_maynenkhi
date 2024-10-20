from fastapi import APIRouter, HTTPException, Query
from bson import ObjectId
from models.authModel import Auth
from config.database import collection_auth
from schema.authSchema import list_auth, auth_seriral
from passlib.hash import pbkdf2_sha256
from jose import jwt
from fastapi import Depends
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib, ssl
import smtplib
import random
import string
router_auth = APIRouter()

#register
@router_auth.post("/auth/register")
async def register(auth:Auth = Depends(Auth.as_form)):
    check_user = collection_auth.find_one({"email": auth.email})
    if check_user:
        raise HTTPException(status_code=400, detail="User da ton tai")

    hash_password = pbkdf2_sha256.hash(auth.password)
    
    new_user = {
        "name": auth.name,
        "email": auth.email,
        "password": hash_password,
        "password_reset_token": auth.password_reset_token,
        "role": auth.role
    }
    
    collection_auth.insert_one(new_user)   
    return{"message": "Tạo tài khoản thành công"}

#login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
@router_auth.post("/auth/login")
async def login(auth:Auth = Depends(Auth.as_form)):
    check_user = collection_auth.find_one({"email": auth.email})
    if not check_user:
        raise HTTPException(status_code=401, detail="Tài khoản không tồn tại")
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
async def get_auth(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    email: str = Query(None)  # email là tùy chọn, có thể không nhập
    ):
    skip = (page - 1) * limit
    # Điều kiện tìm kiếm theo email nếu có
    query_filter = {}
    if email:
        query_filter["email"] = {"$regex": email, "$options": "i"}  # Tìm kiếm không phân biệt hoa thường
    total_items = collection_auth.count_documents(query_filter)
    auths = list_auth(
        collection_auth.find(query_filter).skip(skip).limit(limit)
    )
    total_pages = (total_items + limit - 1) // limit
    return {
        "auths": auths,
        "current_page": page,
        "total_items": total_items,
        "total_pages": total_pages,
        "limit_pages": limit,
    }
@router_auth.get("/auth/{id}")
async def get_one_auth(id: str):
    auth = collection_auth.find_one({"_id": ObjectId(id)})
    
    if not auth:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "email": auth.get("email"),
        "name": auth.get("name")
    }
@router_auth.put("/auth/edit/{id}")
async def edit_auth(id: str, auth: Auth = Depends(Auth.as_form)):
    # Find the existing user
    existing_user = collection_auth.find_one({"_id": ObjectId(id)})
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    # Prepare the update data
    update_data = {}
    if auth.name is not None:
        update_data["name"] = auth.name
    if auth.email != existing_user["email"]:
        # Check if the new email already exists in the database
        check_user = collection_auth.find_one({"email": auth.email})
        if check_user:
            raise HTTPException(status_code=400, detail="Email already in use")
        update_data["email"] = auth.email
    if auth.password:
        # Hash the new password if it's provided
        update_data["password"] = pbkdf2_sha256.hash(auth.password)
    # Update the password_reset_token and role if needed
    update_data["password_reset_token"] = auth.password_reset_token
    update_data["role"] = auth.role
    # Perform the update
    collection_auth.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": update_data}
    )
    return {"message": "OK"}
@router_auth.delete("/auth/delete/{id}")
async def delete_auth(id:str):
    collection_auth.find_one_and_delete({"_id": ObjectId(id)})
    return {"message": "OK"} 

# reset password
@router_auth.post("/auth/forgot_password")
async def forgot_password(email:str):
    new_password = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    hash_newPassword = pbkdf2_sha256.hash(new_password)
    check_email = collection_auth.find_one({"email": email})
    if check_email:
        collection_auth.update_one({"email": email}, {"$set": {"password": hash_newPassword}})
        subject = "Hiepph - Reset Password"  
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = "hiepphdemo@gmail.com"
        receiver_email = email  
        password = "bjcluvuycapnugei"
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        body = f"Chào bạn,\n\nMật khẩu của bạn đã được đặt lại. Dưới đây là mật khẩu mới của bạn:\n\n{new_password}\n\nVui lòng sử dụng mật khẩu này để đăng nhập và sau đó thay đổi thành mật khẩu mới một lần nữa.\n\nTrân trọng,\nHiepph"
        message.attach(MIMEText(body, "plain"))
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        return {"message": "OK"}
    else:
        return {"message": "Email không tồn tại trọng hệ thống" }