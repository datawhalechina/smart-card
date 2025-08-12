import json
import hashlib
import re
import time
from fnmatch import fnmatch
from typing import List, Union, Pattern

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from utils.verify_signature_util import verify_signature
from utils.response_util import ResponseUtil



class SignatureMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        *,
        secret_key: str,
        excluded_paths: List[Union[str, Pattern]] = None,
        allowed_methods: List[str] = None,
        allowed_skew_seconds: int = 300
    ):
        super().__init__(app)
        self.secret_key = secret_key
        self.excluded_paths = excluded_paths or []
        self.allowed_methods = set(m.upper() for m in (allowed_methods or ["POST", "PUT", "PATCH", "DELETE"]))
        self.allowed_skew_seconds = allowed_skew_seconds

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        method = request.method.upper()

        # 路径排除
        if self._is_excluded(path):
            return await call_next(request)

        # 方法排除
        if method not in self.allowed_methods:
            return await call_next(request)

        try:
            body = await request.body()
            body_json = json.loads(body)
        except Exception:
            return ResponseUtil.error(code=400, msg="请求体不是合法 JSON")
        meta = body_json.get("meta", {})
        data = body_json.get("data", {})
        paging = body_json.get("paging", {})

        timestamp = meta.get("timestamp")
        nonce = meta.get("nonce")
        signature = meta.get("signature")

        if not all([timestamp, nonce, signature]):
            return ResponseUtil.error(code = 400, msg="缺少签名字段")

        # 生成签名
        verifysignature = verify_signature(timestamp, nonce, self.secret_key, data, signature)

        if not verifysignature:
            return ResponseUtil.unauthorized(msg="签名验证失败")

        # 重新构造 request.body（因为已读取过）
        request._stream_consumed = False

        async def receive():
            return {"type": "http.request", "body": body}

        request._receive = receive

        return await call_next(request)

    def _is_excluded(self, path: str) -> bool:
        for pattern in self.excluded_paths:
            if isinstance(pattern, str) and fnmatch(path, pattern):
                return True
            if isinstance(pattern, Pattern) and pattern.match(path):
                return True
        return False


