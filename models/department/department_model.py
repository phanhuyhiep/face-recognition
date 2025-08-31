from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId

from models.objectid.objectid_model import PyObjectId

class DepartmentBase(BaseModel):
    name: str = Field(..., example="IT Department")
    description: Optional[str] = Field(None, example="Information Technology")


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentDB(DepartmentBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}