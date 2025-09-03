from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import Optional
from models.department.department_model import RequestDepartment, DepartmentCreate, DepartmentBase
from services.department_service import list_departments, add_department, edit_department, delete_department
from services.user_service import get_current_user
from models.user.user_model import UserDB

router = APIRouter(prefix="/department", tags=["department"])

# ------------------- List Department -------------------
@router.get("/")
async def api_list_departments(
    current_user: UserDB = Depends(get_current_user),
    department_id: Optional[str] = Query(None, example="68b435933edb031a0c555edb"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    result = await list_departments(str(current_user.id), page, limit, department_id)
    if isinstance(result, dict) and result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/add_department")
async def api_add_department(department: DepartmentCreate, current_user: UserDB = Depends(get_current_user)):
    result = await add_department(department.name, current_user.id, department.description)
    if isinstance(result, dict) and result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.put("/edit_department/{department_id}")
async def api_edit_department(department_id: str, payload: DepartmentBase,  current_user: UserDB = Depends(get_current_user)):
    result = await edit_department(department_id, current_user.id, payload.name, payload.description)
    if isinstance(result, dict) and result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.delete("/delete_department/{department_id}")
async def api_delete_department(department_id: str, current_user: UserDB = Depends(get_current_user)):
    result = await delete_department(department_id, current_user.id)
    if isinstance(result, dict) and result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result
