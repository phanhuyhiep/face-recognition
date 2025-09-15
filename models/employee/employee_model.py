import time

from typing import List, Optional
from pydantic import BaseModel, Field
from bson import ObjectId

from models.objectid.objectid_model import PyObjectId


class EmployeeBase(BaseModel):
    name: str = Field(..., example="Nguyen Van A")
    department_id: str = Field(..., example="68b435933edb031a0c555edb")
    department_name: str = Field(..., example="IT")
    email: str = Field(..., example="vana@example.com")
    address: Optional[str] = Field(None, example="123 Lê Lợi, Hà Nội")


class EmployeeCreate(EmployeeBase):
    pass

class EmployeeDB(EmployeeBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str = Field(..., example="68b3f70708171bd88234e9da")
    image_url: str
    # embedding: List[float]

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
