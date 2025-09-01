import numpy as np

from datetime import datetime
from fastapi import UploadFile, HTTPException, Depends
from typing import Optional
from bson import ObjectId

from configs.index import db
from utils.minio_client import upload_to_minio, delete_from_minio
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
            "department_name": employee.department_name,
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


async def get_employees(user_id: str, page: int = 1, limit: int = 10, department_id: Optional[str] = None):
    employees = []
    skip = (page - 1) * limit

    query = {"user_id": str(user_id)}
    if department_id:
        try:
            query["department_id"] = str(department_id)
        except Exception:
            return formatResponse(
                data=[],
                success=False,
                status_code=400,
                message="Invalid department_id"
            )

    cursor = collection_employee.find(query).skip(skip).limit(limit)
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        doc["user_id"] = str(doc["user_id"])
        employees.append(EmployeeDB(**doc))

    total_docs = await collection_employee.count_documents(query)
    total_pages = (total_docs + limit - 1) // limit

    return formatResponse(
        data=employees,
        page=page,
        limit=limit,
        totalPages=total_pages,
        success=True,
        status_code=200,
        message="Employees retrieved successfully"
    )

def is_valid_object_id(oid: str) -> bool:
    return ObjectId.is_valid(oid)

async def get_employee_by_id(employee_id: str, user_id: str):
    if not is_valid_object_id(employee_id):
        return formatResponse(
            data=None,
            success=False,
            status_code=400,
            message="Invalid employee_id"
        )
    doc = await collection_employee.find_one({
        "_id": ObjectId(employee_id),
        "user_id": str(user_id)
    })
    if not doc:
        return formatResponse(
            data=None,
            success=False,
            status_code=404,
            message="Employee not found"
        )
    doc["_id"] = str(doc["_id"])
    doc["user_id"] = str(doc["user_id"])
    return formatResponse(
        data=EmployeeDB(**doc),
        success=True,
        status_code=200,
        message="Employee retrieved successfully"
    )


async def update_employee(employee_id: str, update_data: dict, file: UploadFile = None):
    try:
        employee = await collection_employee.find_one({"_id": ObjectId(employee_id)})
        if not employee:
            return formatResponse(data=[], success=False, status_code=404, message="Employee not found")
        if file:
            old_image_url = employee.get("image_url")
            if old_image_url:
                await delete_from_minio(old_image_url)
            new_image_url = await upload_to_minio(file)
            update_data["image_url"] = new_image_url
            update_data["embedding"] = generate_fake_embedding()

        update_data["updated_at"] = int(datetime.utcnow().timestamp())
        await collection_employee.update_one({"_id": ObjectId(employee_id)}, {"$set": update_data})

        updated_employee = await collection_employee.find_one({"_id": ObjectId(employee_id)})
        updated_employee["_id"] = str(updated_employee["_id"])

        return formatResponse(
            data=updated_employee,
            success=True,
            status_code=200,
            message="Employee updated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update employee: {str(e)}")


async def delete_employee(employee_id: str):
    try:
        employee = await collection_employee.find_one({"_id": ObjectId(employee_id)})
        if not employee:
            return formatResponse(
                data=[],
                success=False,
                status_code=404,
                message="Employee not found"
            )

        image_url = employee.get("image_url")
        if image_url:
            await delete_from_minio(image_url)
            
        await collection_employee.delete_one({"_id": ObjectId(employee_id)})

        return formatResponse(
            data=[],
            success=True,
            status_code=200,
            message="Employee deleted successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete employee: {str(e)}")