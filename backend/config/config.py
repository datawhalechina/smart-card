import os
import importlib

# 根据环境变量选择配置模块
env = os.getenv("ENV", "dev")

# 动态导入对应的配置模块
if env == "prod":
    config_module = importlib.import_module("config.config_prod")
else:
    config_module = importlib.import_module("config.config_dev")

# 将配置项导出，供全项目使用
# 这样可以直接使用 from app.config import settings 来访问所有配置
settings = config_module