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

# 数据库配置
# db_host: str = '192.168.124.23'
db_host: str = '127.0.0.1'
db_port: int = 3306
db_username: str = 'smarter'
db_password: str = 'mysql(2025Smart'
db_database: str = 'smartcard_dev'
db_echo: bool = True
db_max_overflow: int = 10
db_pool_size: int = 50
db_pool_recycle: int = 3600
db_pool_timeout: int = 30

# redis配置
# redis_host: str = '192.168.124.23'
redis_host: str = '127.0.0.1'
redis_port: int = 6379
redis_username: str = ''
redis_password: str = 'admin123'
redis_database: int = 2


secret_key: str = "a1b2c3d4e5f67890abcdef1234567890a1b2c3d4e5f67890abcdef1234567890"

# 前端密码是否加密
PWD_SEC: bool = False

# jwt配置
jwt_secret_key: str = 'b01c66dc2c58dc6a0aabfe2144256be36226de378bf87f72c0c795dda67f4d55'
jwt_algorithm: str = 'HS256'
jwt_expire_minutes: int = 1440
jwt_redis_expire_minutes: int = 30