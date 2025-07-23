PROJECT_NAME: str = "Smart Card BackEnd (Development)"
PROJECT_VERSION: str = "1.0.0"

# 开发环境配置
DATABASE_URL: str = "postgresql://user:password@localhost:5432/prod_db"
SECRET_KEY: str = "dev-secret-key"
DEBUG: bool = True
PORT: int = 8000  # 开发环境端口

# LLM Configuration (New - Ark Platform via OpenAI client)
ARK_API_KEY: str = ""
ARK_BASE_URL: str = "https://chat.intern-ai.org.cn/api/v1/"
ARK_BASE_MODEL: str = "internlm3-latest"

JINA_API_URL: str = "https://r.jina.ai/"
JINA_API_KEY = ""

OUTPUT_DIR: str = "output"
STATIC_DIR: str = "static"
TEMPLATES_DIR: str = "templates"