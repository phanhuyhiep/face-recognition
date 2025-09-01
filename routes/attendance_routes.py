from fastapi import APIRouter, UploadFile, Depends, Query
from typing import Optional

from services.user_service import get_current_user
from models.user.user_model import UserDB
from services.attendance_service import add_attendance, get_attendance


router = APIRouter(prefix="/attendance", tags=["attendance"])

@router.post("/check_face", response_model=dict)
async def api_check_face(file: UploadFile, current_user: UserDB = Depends(get_current_user)):
    return await add_attendance(file, current_user)


@router.get("/", response_model=dict)
async def api_get_attendance(
    current_user: UserDB = Depends(get_current_user),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    date_start: Optional[int] = Query(None, example=1756659600),
    date_end: Optional[int] = Query(None, example=1756745999)
):
    return await get_attendance(
        user_id=current_user.id,
        page=page,
        limit=limit,
        date_start=date_start,
        date_end=date_end
    )