from passlib.context import CryptContext
from datetime import datetime
from jose import JWTError, jwt
from pymongo import ReturnDocument
from bson import ObjectId
from typing import Optional
from fastapi import HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer

from utils.format_time import formatTime
from configs.mongodb_config import MongodbSettings
from models.user.user_model import UserCreate, UserDB
from configs.core_config import CoreSettings
from configs.index import db
from utils.format_response import formatResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = CoreSettings.SECRET_KEY
ALGORITHM = CoreSettings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = CoreSettings.ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
time = datetime.utcnow()
collection_user = db["user"]

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    now_ts = formatTime()
    expire_ts = now_ts + expires_minutes * 60
    to_encode.update({"exp": expire_ts})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(request: Request):
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(status_code=401, detail="Authorization header missing")

        token = auth_header.strip()  # lấy nguyên token, không cần "Bearer "

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user = await collection_user.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        user["_id"] = str(user["_id"])
        return UserDB(**user)

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def register_user(user: UserCreate):
    existing = await collection_user.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = get_password_hash(user.password)
    user_doc = {
        "username": user.username,
        "email": user.email,
        "password_hash": hashed_password,
        "created_at": formatTime(time),
    }

    result = await collection_user.insert_one(user_doc)
    new_user = await collection_user.find_one({"_id": result.inserted_id})
    new_user["_id"] = str(new_user["_id"])
    return UserDB(**new_user)


async def login_user(email: str, password: str):
    user = await collection_user.find_one({"email": email})
    if not user:
        return {"error": "Invalid credentials"}

    if not verify_password(password, user["password_hash"]):
        return {"error": "Invalid credentials"}

    access_token = create_access_token(data={"sub": str(user["_id"])})
    return formatResponse(
        data={
            "user_id": str(user["_id"]),
            "access_token": access_token,
            "token_type": "bearer"
        },
        success=True,
        status_code=200,
        message="Login successful"
    )