from typing import Optional
from pydantic import BaseModel

class Meta(BaseModel):
    timestamp: str
    nonce: str
    signature: str
    traceId: str

class Paging(BaseModel):
    page: Optional[int] = 1
    pageSize: Optional[int] = 10

class Data(BaseModel):
    username: str
    password: str
    confirmPassword: str
    email: str
    code: str
    uuid: str

class RequestUtil(BaseModel):
    meta: Meta
    paging: Optional[Paging] = None
    data: Data
