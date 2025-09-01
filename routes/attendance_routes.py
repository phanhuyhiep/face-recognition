from fastapi import APIRouter, UploadFile, Depends
from services.user_service import get_current_user
from models.user.user_model import UserDB
from services.attendance_service import add_attendance

router = APIRouter(prefix="/attendance", tags=["attendance"])

@router.post("/check_face", response_model=dict)
async def api_check_face(file: UploadFile, current_user: UserDB = Depends(get_current_user)):
    return await add_attendance(file, current_user)
