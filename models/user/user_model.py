from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId

from models.objectid.objectid_model import PyObjectId


class UserBase(BaseModel):
    username: str = Field(..., example="hiepph")
    email: str = Field(..., example="hiepph@example.com")
    department_id: Optional[str] = Field(None, example="64eac12d98f0b1a8e4d9a321")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str

class response_model(BaseModel):
    data: Optional[TokenResponse]
    success: bool
    status_code: int
    message: str

class UserCreate(UserBase):
    password: str = Field(..., example="strongpassword123")


class UserDB(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    password_hash: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}