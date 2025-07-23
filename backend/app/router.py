from fastapi import APIRouter

from app.public import summarize, download
from app.public.requirement import router as generate_files_router


# 主路由配置
def get_main_router():
    # 创建主路由
    main_router = APIRouter(prefix="/api")

    # 挂载各个模块的路由
    main_router.include_router(generate_files_router, prefix="/v1/requirement", tags=["需求生成"])
    main_router.include_router(summarize.router, prefix="/v1/summarize", tags=["智能总结"])
    main_router.include_router(download.router, prefix="/v1/download-html", tags=["下载"])
    # main_router.include_router(paste.router, prefix="/v1/paste", tags=["粘贴HTML"])

    return main_router