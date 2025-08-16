from typing import Optional, Generic, TypeVar, Any
from pydantic import BaseModel
from pydantic.generics import GenericModel

class Meta(BaseModel):
    timestamp: str
    nonce: str
    signature: str
    traceId: str

class Paging(BaseModel):
    page: Optional[int] = 1
    pageSize: Optional[int] = 10


# 定义泛型类型变量
T = TypeVar('T')

class RequestUtil(GenericModel, Generic[T]):
    meta: Meta
    paging: Optional[Paging] = None
    data: T
