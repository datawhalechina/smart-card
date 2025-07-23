# from fastapi import Request
# from fastapi.responses import JSONResponse
# import redis
# import jwt
# from datetime import datetime, timezone
#
# # 连接 Redis
# redis_client = redis.Redis(host='localhost', port=6379, db=0)
#
# # 假设这是 JWT 的密钥，实际使用时可从配置文件获取
# JWT_SECRET = "your_jwt_secret"
# # 定义不需要检查 token 的路径列表
# WHITELIST_PATHS = ["/login"]
#
# async def check_token(request: Request, call_next):
#     # 获取请求路径
#     path = request.url.path
#     # 检查请求路径是否在白名单中
#     if path in WHITELIST_PATHS:
#         # 若在白名单中，直接调用后续处理逻辑
#         response = await call_next(request)
#         return response
#
#     token = request.headers.get("token")
#     if not token:
#         return JSONResponse(
#             status_code=401,
#             content={"message": "Unauthorized: Missing token"}
#         )
#
#     try:
#         # 验证 JWT 格式
#         payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
#         user_id = payload.get("user_id")
#         if not user_id:
#             return JSONResponse(
#                 status_code=401,
#                 content={"message": "Unauthorized: Invalid token payload"}
#             )
#
#         # 从 Redis 中获取 Token
#         redis_token = redis_client.get(f"user:{user_id}:token")
#         if not redis_token or redis_token.decode() != token:
#             return JSONResponse(
#                 status_code=401,
#                 content={"message": "Unauthorized: Token not found or invalid"}
#             )
#
#         # 检查 Token 是否过期
#         exp = payload.get("exp")
#         if exp and datetime.fromtimestamp(exp, timezone.utc) < datetime.now(timezone.utc):
#             # Token 过期，从 Redis 中删除
#             redis_client.delete(f"user:{user_id}:token")
#             return JSONResponse(
#                 status_code=401,
#                 content={"message": "Unauthorized: Token expired"}
#             )
#
#     except jwt.ExpiredSignatureError:
#         return JSONResponse(
#             status_code=401,
#             content={"message": "Unauthorized: Token expired"}
#         )
#     except jwt.InvalidTokenError:
#         return JSONResponse(
#             status_code=401,
#             content={"message": "Unauthorized: Invalid token"}
#         )
#
#     response = await call_next(request)
#     return response