import re

from fastapi import FastAPI

from config.config import settings
from middlewares.add_signature_middleware import  SignatureMiddleware
from middlewares.cors_middleware import add_cors_middleware
from middlewares.trace_middleware import add_trace_middleware


def handle_middleware(app: FastAPI):
    """
    全局中间件处理
    """
    # 标准中间件（跨域、trace）
    # 加载跨域中间件
    add_cors_middleware(app)
    # 加载trace中间件
    add_trace_middleware(app)

    # 验签中间件
    app.add_middleware(
        SignatureMiddleware,
        secret_key = settings.secret_key,
        excluded_paths=[
            "/health",
            "/docs",
            "/openapi.json",
            "/login",
            # "/register",
            "/static/*",
            re.compile(r"^/public/.*")
        ],
        allowed_methods=["POST", "PUT", "PATCH", "DELETE"],
        allowed_skew_seconds=300
    )



