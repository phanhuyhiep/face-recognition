from fastapi import APIRouter, HTTPException, status, Query
from typing import Optional
from models.department.department_model import RequestDepartment, DepartmentCreate, DepartmentBase
from services.department_service import list_departments, add_department, edit_department, delete_department

router = APIRouter(prefix="/department", tags=["auth"])

# ------------------- List Department -------------------
@router.get("/")
async def api_list_departments(
    department_id: Optional[str] = Query(None, example="68b435933edb031a0c555edb"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    result = await list_departments(department_id, page, limit)
    if isinstance(result, dict) and result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/add_department")
async def api_add_department(department: DepartmentCreate):
    result = await add_department(department.name, department.description)
    if isinstance(result, dict) and result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.put("/edit_department/{department_id}")
async def api_edit_department(department_id: str, payload: DepartmentBase):
    result = await edit_department(department_id, name=payload.name, description=payload.description)
    if isinstance(result, dict) and result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.delete("/delete_department/{department_id}")
async def api_delete_department(department_id: str):
    result = await delete_department(department_id)
    if isinstance(result, dict) and result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result
