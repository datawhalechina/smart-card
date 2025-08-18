from pydantic import BaseModel,  Field
from typing import Any, Optional, Generic, TypeVar

from utils.response_util import ResponseUtil

T = TypeVar('T')  # 定义泛型类型变量

class ResponseModel(BaseModel, Generic[T]):
    """
    操作响应模型
    """
    is_success: bool = Field(description='操作是否成功')
    message: str = Field(description='响应信息')
    result: Optional[T] = Field(default=None, description='响应结果')

# 新增 Token 结果模型
class LoginTokenResult(BaseModel):
    token: str = Field(description="用户凭证")