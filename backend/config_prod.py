class Settings:
    PROJECT_NAME: str = "Smart Card API (Production)"
    PROJECT_VERSION: str = "1.0.0"

    # 生产环境数据库配置
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/prod_db"
    SECRET_KEY: str = "prod-secret-key"  # 实际使用时应替换为强密钥
    DEBUG: bool = False
    PORT: int = 8080  # 生产环境端口

settings = Settings()
