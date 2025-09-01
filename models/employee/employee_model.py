import time

from typing import List, Optional
from pydantic import BaseModel, Field
from bson import ObjectId

from models.objectid.objectid_model import PyObjectId


class EmployeeBase(BaseModel):
    name: str = Field(..., example="Nguyen Van A")
    department_id: str = Field(..., example="68b435933edb031a0c555edb")
    email: str = Field(..., example="vana@example.com")
    address: Optional[str] = Field(None, example="123 Lê Lợi, Hà Nội")


class EmployeeCreate(EmployeeBase):
    image_url: str = Field(..., example="https://minio.domain.com/faces/emp_001/profile.png")
    embedding: List[float] = Field(..., example=[0.123, -0.456, 0.789])


class EmployeeDB(EmployeeBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    image_url: str
    embedding: List[float]
    created_at: int = Field(default_factory=lambda: int(time.time()))
    updated_at: int = Field(default_factory=lambda: int(time.time()))

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
