# common/response.py
from typing import Generic, TypeVar, Optional, Any, List, Dict
from pydantic import BaseModel

# 定义泛型类型，支持任意数据结构
T = TypeVar("T")

class standard_response(BaseModel, Generic[T]):
    """通用API响应模型，支持对象、列表等任意数据类型"""
    code: int = 200
    msg: str = "操作成功"
    data: Optional[T] = None  # T 可表示对象、列表、字典等

# 响应工具函数（自动适配数据类型）
def success(
    data: Optional[Any] = None,
    msg: str = "操作成功"
) -> standard_response:
    """成功响应：自动处理对象/列表/空值"""
    return standard_response(code=200, msg=msg, data=data)

def error(
    code: int = 500,
    msg: str = "操作失败",
    data: Optional[Any] = None
) -> standard_response:
    """错误响应：统一包含data字段（可为空）"""
    return standard_response(code=code, msg=msg, data=data)

# 常用错误快捷函数
def not_found(msg: str = "资源不存在") -> standard_response:
    return error(code=404, msg=msg)

def bad_request(msg: str = "参数错误") -> standard_response:
    return error(code=400, msg=msg)


# 全局异常处理器（统一捕获异常并转换为ApiResponse）
def setup_exception_handlers(app):
    from fastapi import Request, HTTPException
    from fastapi.responses import JSONResponse

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            content=error(code=exc.status_code, msg=exc.detail).dict()
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            content=error(msg=str(exc)).dict()
        )

