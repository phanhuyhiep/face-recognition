from typing import Any, Optional, Dict

def formatResponse(
    data: Any = None,
    page: Optional[int] = None,
    limit: Optional[int] = None,
    totalPages: Optional[int] = None,
    success: bool = True,
    status_code: int = 200,
    error_code: Optional[int] = None,
    message: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Format chuẩn cho response API.

    Args:
        data (Any): Dữ liệu trả về.
        page (int, optional): Trang hiện tại (nếu có pagination).
        limit (int, optional): Số bản ghi mỗi trang (nếu có pagination).
        totalPages (int, optional): Tổng số trang (nếu có pagination).
        success (bool): Trạng thái thành công hay thất bại.
        status_code (int): HTTP status code.
        error_code (int, optional): Mã lỗi nếu có.
    
    Returns:
        dict: Response chuẩn.
    """
    response = {
        "data": data,
        "page": page,
        "limit": limit,
        "totalPages": totalPages,
        "success": success,
        "status_code": status_code,
        "error_code": error_code,
        "message": message,
    }

    # Loại bỏ những key có giá trị None để response gọn hơn
    return {k: v for k, v in response.items() if v is not None}