import numpy as np

from typing import List
from fastapi import UploadFile, HTTPException
from datetime import datetime, timezone

from configs.index import db
from utils.minio_client import upload_to_minio
from utils.format_response import formatResponse
from models.user.user_model import UserDB

collection_employee = db["employee"]
collection_attendance = db["attendance"]

def generate_fake_embedding(dim: int = 128) -> List[float]:
    return np.random.rand(dim).tolist()

def cosine_similarity(a: List[float], b: List[float]) -> float:
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

async def add_attendance(file: UploadFile, current_user: UserDB):
    try:
        face_image_url = await upload_to_minio(file)
        query_embedding = generate_fake_embedding()
        employees_cursor = collection_employee.find({"user_id": str(current_user.id)})
        matched_employee = None
        max_sim = 0.0

        async for emp in employees_cursor:
            sim = cosine_similarity(emp["embedding"], query_embedding)
            if sim > max_sim:
                max_sim = sim
                matched_employee = emp

        if not matched_employee or max_sim < 0.7:
            return formatResponse(
                data=None,
                success=False,
                status_code=404,
                message="No matching employee found"
            )

        now_ts = int(datetime.utcnow().timestamp())
        today = datetime.utcnow().date()
        last_attendance = await collection_attendance.find_one(
            {"employee_id": str(matched_employee["_id"]),
             "user_id": str(current_user.id)},
            sort=[("check_in", -1)]
        )

        if last_attendance:
            last_checkin_date = datetime.fromtimestamp(last_attendance["check_in"], tz=timezone.utc).date()
            if last_checkin_date == today:
                await collection_attendance.update_one(
                    {"_id": last_attendance["_id"]},
                    {"$set": {"check_out": now_ts, "check_out_face": face_image_url}}
                )
                return formatResponse(
                    data={"employee_id": str(matched_employee["_id"]), "action": "check_out_updated"},
                    success=True,
                    status_code=200,
                    message="Check-out updated"
                )

        attendance_doc = {
            "employee_id": str(matched_employee["_id"]),
            "user_id": str(current_user.id),
            "name": matched_employee["name"],
            "department_id": matched_employee["department_id"],
            "check_in": now_ts,
            "check_in_face": face_image_url,
            "check_out": None,
            "check_out_face": None
        }
        result = await collection_attendance.insert_one(attendance_doc)
        attendance_doc["_id"] = str(result.inserted_id)

        return formatResponse(
            data=attendance_doc,
            success=True,
            status_code=201,
            message="Check-in recorded"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add attendance: {str(e)}")
