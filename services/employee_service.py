import numpy as np

from datetime import datetime
from fastapi import UploadFile, HTTPException

from configs.index import db
from utils.minio_client import upload_to_minio
from models.employee.employee_model import EmployeeCreate, EmployeeDB
from utils.format_response import formatResponse
from services.user_service import get_current_user
from utils.format_time import formatTime

collection_employee = db["employee"]
time = datetime.utcnow()

def generate_fake_embedding(dim: int = 128) -> list:
    return np.random.rand(dim).tolist()

async def add_employee(employee: EmployeeCreate, file: UploadFile, user_id: str):
    try:
        image_url = await upload_to_minio(file)
        embedding = generate_fake_embedding()
        employee_doc = {
            "name": employee.name,
            "email": employee.email,
            "address": employee.address,
            "department_id": employee.department_id,
            "image_url": image_url,
            "embedding": embedding,
            "created_at": formatTime(datetime.utcnow()),
            "user_id": str(user_id)
        }
        result = await collection_employee.insert_one(employee_doc)
        new_employee = await collection_employee.find_one({"_id": result.inserted_id})
        new_employee["_id"] = str(new_employee["_id"])
        return formatResponse(
            data=EmployeeDB(**new_employee),
            success=True,
            status_code=201,
            message="Employee added successfully"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add employee: {str(e)}")