from fastapi import APIRouter, HTTPException, Query, Request
from bson import ObjectId
from models.authModel import Auth
from config.database import collection_auth
from models.common import message_response, paginate_response
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


# register
@router_auth.post("/auth/register")
async def register(auth: Auth = Depends(Auth.as_form)):
    check_user = collection_auth.find_one({"email": auth.email})
    if check_user:
        raise HTTPException(status_code=400, detail="User da ton tai")

    hash_password = pbkdf2_sha256.hash(auth.password)

    new_user = {
        "name": auth.name,
        "email": auth.email,
        "password": hash_password,
        "password_reset_token": auth.password_reset_token,
        "role": auth.role,
    }

    collection_auth.insert_one(new_user)
    return message_response("OK")


# login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router_auth.post("/auth/login")
async def login(auth: Auth = Depends(Auth.as_form)):
    check_user = collection_auth.find_one({"email": auth.email})
    if not check_user:
        raise HTTPException(status_code=401, detail="Tài khoản không tồn tại")
    hashed_password = check_user["password"]
    if not pbkdf2_sha256.verify(auth.password, hashed_password):
        raise HTTPException(status_code=401, detail="Sai password")
    token = create_access_token(str(check_user["_id"]))
    return paginate_response([{"token": token}], 1, 1, 1, 1)


def create_access_token(auth_id: str):
    return jwt.encode(
        claims={
            "id": auth_id,
            "exp": datetime.utcnow() + timedelta(minutes=30),
        },
        key="be-page",
        algorithm="HS256",
    )


def get_token_custom(request: Request):
    token = request.headers.get("authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
    return token


def get_current_user(token: str = Depends(get_token_custom)):
    try:
        payload = jwt.decode(token, "be-page", algorithms=["HS256"])
        user_id = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router_auth.get("/auth/profile")
async def get_profile(user_id: str = Depends(get_current_user)):
    user = collection_auth.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["_id"] = str(user["_id"])
    del user["_id"]
    del user["password"]
    del user["password_reset_token"]
    return paginate_response(user, 1, 1, 1, 1)


@router_auth.get("/auth/")
async def get_auth(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    email: str = Query(None),
):
    skip = (page - 1) * limit
    query_filter = {}
    if email:
        query_filter["email"] = {
            "$regex": email,
            "$options": "i",
        }  # Tìm kiếm không phân biệt hoa thường
    total_items = collection_auth.count_documents(query_filter)
    auths = list_auth(collection_auth.find(query_filter).skip(skip).limit(limit))
    total_pages = (total_items + limit - 1) // limit
    return paginate_response(auths, page, total_items, limit, total_pages)


@router_auth.get("/auth/{id}")
async def get_one_auth(id: str):
    auth = collection_auth.find_one({"_id": ObjectId(id)})
    if not auth:
        raise HTTPException(status_code=404, detail="User not found")
    auth["id"] = str(auth["_id"])
    del auth["_id"]
    return paginate_response(auth, 1, 1, 1, 1)


@router_auth.put("/auth/edit/{id}")
async def edit_auth(id: str, auth: Auth = Depends(Auth.as_form)):
    existing_user = collection_auth.find_one({"_id": ObjectId(id)})
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = {}
    if auth.name is not None:
        update_data["name"] = auth.name
    if auth.email != existing_user["email"]:
        check_user = collection_auth.find_one({"email": auth.email})
        if check_user:
            raise HTTPException(status_code=400, detail="Email already in use")
        update_data["email"] = auth.email
    if auth.password:
        update_data["password"] = pbkdf2_sha256.hash(auth.password)
    update_data["password_reset_token"] = auth.password_reset_token
    update_data["role"] = auth.role
    collection_auth.find_one_and_update({"_id": ObjectId(id)}, {"$set": update_data})
    return message_response("OK")


@router_auth.delete("/auth/delete/{id}")
async def delete_auth(id: str):
    collection_auth.find_one_and_delete({"_id": ObjectId(id)})
    return message_response("OK")


# reset password
@router_auth.post("/auth/forgot_password")
async def forgot_password(email: str):
    new_password = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    hash_newPassword = pbkdf2_sha256.hash(new_password)
    check_email = collection_auth.find_one({"email": email})
    if check_email:
        collection_auth.update_one(
            {"email": email}, {"$set": {"password": hash_newPassword}}
        )
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
        return message_response("OK")
    else:
        return message_response("Email không tồn tại")
