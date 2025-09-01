from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, Query, Path
from typing import Optional

from models.employee.employee_model import EmployeeCreate, EmployeeDB
from models.user.user_model import UserDB
from services.employee_service import add_employee, get_employees, get_employee_by_id
from services.user_service import get_current_user

router = APIRouter(prefix="/employee", tags=["employee"])

@router.post("/create_employee", response_model=dict)
async def create_employee(
    name: str = Form(...),
    department_id: str = Form(...),
    email: str = Form(...),
    address: Optional[str] = Form(None),
    file: UploadFile = File(...),
    current_user: UserDB = Depends(get_current_user),
):
    try:
        employee = EmployeeCreate(
            name=name,
            department_id=department_id,
            email=email,
            address=address,
        )

        result = await add_employee(employee, file, current_user.id)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create employee: {str(e)}")


@router.get("/", response_model=dict)
async def api_get_employees(
    current_user: UserDB = Depends(get_current_user),
    department_id: Optional[str] = Query(None, example="68b435933edb031a0c555edb"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    try:
        result = await get_employees(current_user.id, page, limit, department_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get employees: {str(e)}")


@router.get("/{employee_id}", response_model=dict)
async def api_get_employee_by_id(
    employee_id: str = Path(..., example="68b59739fbbb7de239212a1c"),
    current_user: UserDB = Depends(get_current_user)
):
    try:
        result = await get_employee_by_id(employee_id, current_user.id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get employee: {str(e)}")