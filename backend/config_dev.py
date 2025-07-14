class Settings:
    PROJECT_NAME: str = "Smart Card BackEnd (Development)"
    PROJECT_VERSION: str = "1.0.0"

    # 开发环境配置
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/prod_db"
    SECRET_KEY: str = "dev-secret-key"
    DEBUG: bool = True
    PORT: int = 8000  # 开发环境端口

settings = Settings()