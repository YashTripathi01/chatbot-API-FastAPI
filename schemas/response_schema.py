from typing import Optional, Union
from pydantic import BaseModel, Field


class ApiResponse(BaseModel):
    message: str
    data: list | dict
    status_code: int
    success: bool
