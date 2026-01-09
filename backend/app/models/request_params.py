from pydantic import BaseModel
from typing import Optional

class sort_params(BaseModel):
    field: str
    ascending: bool = True

class filter_params(BaseModel):
    field: str
    value: str

class request_params(BaseModel):
    page: int
    page_size: int
    sort_by: Optional[sort_params] = None
    filter_by: Optional[filter_params] = None
    