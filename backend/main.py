import os
from fastapi import FastAPI
import uvicorn

# 根据环境变量加载配置
env = os.getenv("ENV", "dev")
if env == "prod":
    from config_prod import settings
else:
    from config_dev import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    debug=settings.DEBUG
)

@app.get("/")
async def root():
    return {
        "message": "Hello World",
        "environment": env,
        "debug_mode": settings.DEBUG,
        "port": settings.PORT
    }

def run_server():
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=settings.DEBUG
    )

if __name__ == "__main__":
    run_server()