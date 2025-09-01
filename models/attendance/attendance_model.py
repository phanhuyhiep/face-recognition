from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId
from models.objectid.objectid_model import PyObjectId

class AttendanceBase(BaseModel):
    user_id: str
    employee_id: Optional[str] = None
    check_in: Optional[int] = None
    check_out: Optional[int] = None
    check_in_face_url: Optional[str] = None
    check_out_face_url: Optional[str] = None

class AttendanceCreate(AttendanceBase):
    face_file_url: Optional[str] = None
    embedding: Optional[List[float]] = None

class AttendanceDB(AttendanceBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: int = Field(default_factory=lambda: int(datetime.utcnow().timestamp()))
    updated_at: int = Field(default_factory=lambda: int(datetime.utcnow().timestamp()))

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
