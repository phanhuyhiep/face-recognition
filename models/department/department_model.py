from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId

from models.objectid.objectid_model import PyObjectId

class RequestDepartment(BaseModel):
    department_id: Optional[str] = Field(None, example="64eac12d98f0b1a8e4d9a321")
    limit: Optional[int] = Field(10, example=10)
    page: Optional[int] = Field(1, example=1)

class DepartmentBase(BaseModel):
    name: str = Field(..., example="IT Department")
    description: Optional[str] = Field(None, example="Information Technology")


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentDB(DepartmentBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str = Field(..., example="68b3f70708171bd88234e9da")
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}