import numpy as np
import logging
import asyncio

from typing import List
from fastapi import UploadFile, HTTPException
from datetime import datetime, timezone

from typing import Optional
from models.attendance.attendance_model import AttendanceDB
from configs.index import db
from utils.minio_client import upload_to_minio
from utils.format_response import formatResponse
from models.user.user_model import UserDB
from configs.core_config import CoreSettings
from utils.datetime import current_time_vn_by_timestamp
from test import get_face_similarity, load_face_model

collection_employee = db["employee"]
collection_attendance = db["attendance"]

TIME_ZONE = CoreSettings.TIME_ZONE

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

async def add_attendance(file: UploadFile, current_user: UserDB):
    try:
        face_image_url = await upload_to_minio(file)
        employees_cursor = collection_employee.find({"user_id": str(current_user.id)})
        matched_employee = None
        max_sim = 0.0
        model = load_face_model()
        async for emp in employees_cursor:
            similarity = await asyncio.to_thread(get_face_similarity, emp["image_url"], face_image_url, model)
            if similarity > max_sim:
                max_sim = similarity
                matched_employee = emp
        if not matched_employee or max_sim < 0.7:
            logger.info("No matching employee found")
            return formatResponse(
                data=None,
                success=False,
                status_code=404,
                message="No matching employee found"
            )
        now_ts = current_time_vn_by_timestamp()
        today = datetime.fromtimestamp(now_ts, TIME_ZONE).date()
        last_attendance = await collection_attendance.find_one(
            {"employee_id": str(matched_employee["_id"]),
             "user_id": str(current_user.id)},
            sort=[("check_in", -1)]
        )

        if last_attendance:
            last_checkin_date = datetime.fromtimestamp(last_attendance["check_in"], tz = TIME_ZONE).date()
            if last_checkin_date == today:
                await collection_attendance.update_one(
                    {"_id": last_attendance["_id"]},
                    {"$set": {"check_out": now_ts, "check_out_face": face_image_url}}
                )
                logger.info(f"Check-out updated for employee {matched_employee['name']} (checkout timestamp: {now_ts})")
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
            "department_name": matched_employee["department_name"],
            "check_in": now_ts,
            "check_in_face": face_image_url,
            "check_out": None,
            "check_out_face": None
        }
        result = await collection_attendance.insert_one(attendance_doc)
        attendance_doc["_id"] = str(result.inserted_id)
        logger.info(f"Attendance recorded for employee: {matched_employee['name']} (checkin timestamp: {now_ts})")
        return formatResponse(
            data=attendance_doc,
            success=True,
            status_code=201,
            message="Check-in recorded"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add attendance: {str(e)}")


async def get_attendance(
    user_id: str,
    page: int = 1,
    limit: int = 10,
    date_start: Optional[int] = None,
    date_end: Optional[int] = None
):
    try:
        skip = (page - 1) * limit
        attendances = []
        query = {"user_id": str(user_id)}
        if date_start is not None or date_end is not None:
            date_filter = {}
            if date_start is not None:
                date_filter["$gte"] = date_start
            if date_end is not None:
                date_filter["$lte"] = date_end
            query["check_in"] = date_filter
        total_docs = await collection_attendance.count_documents(query)
        total_pages = (total_docs + limit - 1) // limit

        cursor = collection_attendance.find(query).sort("check_in", -1).skip(skip).limit(limit)
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            attendances.append(AttendanceDB(**doc))
        return formatResponse(
            data=attendances,
            page=page,
            limit=limit,
            totalPages=total_pages,
            success=True,
            status_code=200,
            message="Attendance retrieved successfully"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get attendance: {str(e)}")
