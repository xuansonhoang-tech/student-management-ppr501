from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel, ConfigDict

T = TypeVar("T")

class BaseResponse(BaseModel, Generic[T]): 
    data: Optional[List[T]] = None
    page_size: int = 0
    page_number: int = 0
    total_records: int = 0
    error: Optional[List[str]] = None
    success: bool = True
    
    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)

    def to_dict(self):
        return {
            "page_size": self.page_size,
            "page_number": self.page_number,
            "page_total": self.total_records,
            "data": self.data,
            "error": self.error,
            "success": self.success
        }