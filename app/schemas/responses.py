from typing import Optional
from pydantic import BaseModel, Field


class ResponseModel(BaseModel):
    OK: bool = Field(..., title="OK")
    detail: Optional[str] = Field(None, title="Detail")
    id: Optional[int] = Field(..., title="ID")
