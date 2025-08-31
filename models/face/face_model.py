from typing import List, Optional
from pydantic import BaseModel, Field
from bson import ObjectId
from typing import List, Optional

from models.objectid.objectid_model import PyObjectId



class FaceBase(BaseModel):
    user_id: str = Field(..., example="64eac12d98f0b1a8e4d9a321")
    image_url: str = Field(..., example="s3://faces/hiepph_1.jpg")
    embedding: List[float] = Field(..., example=[0.123, -0.456, 0.789])


class FaceCreate(FaceBase):
    pass


class FaceDB(FaceBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}