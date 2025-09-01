from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from services.user_service import register_user, login_user, get_current_user
from models.user.user_model import UserCreate, UserDB, response_model
from utils.format_response import formatResponse

router = APIRouter(prefix="/auth", tags=["auth"])

# ------------------- REGISTER -------------------
@router.post("/register", response_model=UserDB, status_code=status.HTTP_201_CREATED)
async def api_register(user: UserCreate):
    result = await register_user(user)
    if isinstance(result, dict) and result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# ------------------- LOGIN -------------------
class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login", response_model=response_model)
async def api_login(credentials: LoginRequest):
    result = await login_user(credentials.email, credentials.password)
    if isinstance(result, dict) and result.get("error"):
        raise HTTPException(status_code=401, detail=result["error"])
    return result

@router.get("/profile")
async def get_profile(current_user: UserDB = Depends(get_current_user)):
    return formatResponse(
        data=current_user,
        success=True,
        status_code=200,
        message="Current user profile"
    )