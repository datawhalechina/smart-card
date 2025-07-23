import os
from fastapi import FastAPI
import uvicorn
from starlette.staticfiles import StaticFiles

from app.router import get_main_router
from config.config import settings

# 创建FastAPI应用
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    debug=settings.DEBUG
)

os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
app_static_dir = os.path.join(os.path.dirname(__file__), settings.STATIC_DIR)
os.makedirs(app_static_dir, exist_ok=True)
app.mount(f"/{settings.STATIC_DIR}", StaticFiles(directory=app_static_dir), name=settings.STATIC_DIR)

# 挂载主路由
app.include_router(get_main_router())

# 添加中间件 用来验证jwt token
# app.middleware("http")(check_token)

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