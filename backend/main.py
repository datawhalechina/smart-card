import os
from fastapi import FastAPI
import uvicorn
from app.router import get_main_router
from config.config import settings


# 创建FastAPI应用
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    debug=settings.DEBUG
)

# 挂载主路由
app.include_router(get_main_router())

# 启动应用
def run_server():
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=settings.DEBUG
    )

if __name__ == "__main__":
    run_server()