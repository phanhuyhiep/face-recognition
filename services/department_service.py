from datetime import datetime
from jose import JWTError, jwt
from pymongo import ReturnDocument
from bson import ObjectId
from typing import Optional, List
from fastapi import Query

from utils.format_time import formatTime
from configs.mongodb_config import MongodbSettings
from models.department.department_model import DepartmentCreate, DepartmentDB
from configs.core_config import CoreSettings
from configs.index import db
from utils.format_response import formatResponse

time = datetime.utcnow()
collection_department = db["department"]

async def list_departments(user_id: str, page: int = 1, limit: int = 10, department_id: Optional[str] = None):
    departments = []
    print("department_id:", department_id)
    if department_id:
        try:
            doc = await collection_department.find_one({"user_id": user_id, "_id": ObjectId(department_id)})
            if doc:
                doc["_id"] = str(doc["_id"])
                departments.append(DepartmentDB(**doc))
            total_docs = len(departments)
        except Exception:
            return formatResponse(
                data=[],
                success=False,
                status_code=400,
                message="Invalid department_id"
            )
    else:
        skip = (page - 1) * limit
        cursor = collection_department.find().skip(skip).limit(limit)
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            departments.append(DepartmentDB(**doc))
        total_docs = await collection_department.count_documents({"user_id": user_id})

    total_pages = (total_docs + limit - 1) // limit if not department_id else 1

    return formatResponse(
        data=departments,
        page=page if not department_id else 1,
        limit=limit if not department_id else 1,
        totalPages=total_pages,
        success=True,
        status_code=200,
        message="Departments retrieved successfully"
    )

async def add_department(name: str, user_id: str, description: Optional[str] = None):
    department_doc = {
        "name": name,
        "user_id": user_id,
        "created_at": formatTime(datetime.utcnow()),
    }
    if description:
        department_doc["description"] = description

    result = await collection_department.insert_one(department_doc)
    new_department = await collection_department.find_one({"_id": result.inserted_id})
    return formatResponse(
        data=DepartmentDB(**new_department),
        success = True,
        status_code = 201,
        message = "Department created successfully",
    )

async def edit_department(department_id: str, name: Optional[str] = None, description: Optional[str] = None):
    update_doc = {}
    if name:
        update_doc["name"] = name
    if description:
        update_doc["description"] = description

    if not update_doc:
        return {"error": "Nothing to update"}

    result = await collection_department.update_one(
        {"_id": ObjectId(department_id)},
        {"$set": update_doc}
    )
    if result.matched_count == 0:
        return {"error": "Department not found"}

    updated_doc = await collection_department.find_one({"_id": ObjectId(department_id)})
    updated_doc["_id"] = str(updated_doc["_id"])
    return formatResponse(
        data=DepartmentDB(**updated_doc),
        success=True,
        status_code=200,
        message="Department updated successfully"
    )

async def delete_department(department_id: str):
    result = await collection_department.delete_one({"_id": ObjectId(department_id)})
    if result.deleted_count == 0:
        return {"error": "Department not found"}

    return formatResponse(
        data={"_id": department_id},
        success=True,
        status_code=200,
        message="Department deleted successfully"
    )