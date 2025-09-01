from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from typing import Optional

from models.employee.employee_model import EmployeeCreate, EmployeeDB
from models.user.user_model import UserDB
from services.employee_service import add_employee
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