import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from starlette.staticfiles import StaticFiles

from config.config import settings
from config.get_db import init_create_table
from config.get_redis import RedisUtil
from middlewares.handle import handle_middleware
from utils.common_util import worship
from utils.exceptions.handle import handle_exception
from utils.log_util import logger

from app.router import get_main_router

# 生命周期事件
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f'{settings.PROJECT_NAME}开始启动')
    worship()
    await init_create_table()
    app.state.redis = await RedisUtil.create_redis_pool()
    # await RedisUtil.init_sys_dict(app.state.redis)
    # await RedisUtil.init_sys_config(app.state.redis)
    logger.info(f'{settings.PROJECT_NAME}启动成功')
    yield
    await RedisUtil.close_redis_pool(app)
# 创建FastAPI应用
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
app_static_dir = os.path.join(os.path.dirname(__file__), settings.STATIC_DIR)
os.makedirs(app_static_dir, exist_ok=True)
app.mount(f"/{settings.STATIC_DIR}", StaticFiles(directory=app_static_dir), name=settings.STATIC_DIR)


# 挂载主路由
main_router, admin_router = get_main_router()
# 分别挂载主路由和管理路由
app.include_router(main_router)
app.include_router(admin_router)

# 加载中间件处理方法
handle_middleware(app)
# 加载全局异常处理方法
handle_exception(app)

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