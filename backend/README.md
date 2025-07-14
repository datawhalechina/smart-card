# Smart Card API 项目文档

## 项目目录结构说明

```
backend/
├── app/                # 主应用模块
│   ├── admin/          # 管理后台相关路由
│   ├── public/         # 公共API路由
│   └── __init__.py     # Python包标识文件
├── dal/                # 数据访问层
├── integration/        # 调用远程api
├── services/           # 业务服务层
├── utils/              # 工具函数库
├── config_dev.py       # 开发环境配置
├── config_prod.py      # 生产环境配置
├── main.py             # 应用入口和主配置
└── requirements.txt    # 项目依赖
```

## 目录详细说明

### app/
主应用模块，包含API路由定义
- `admin/`: 管理后台相关API路由
- `public/`: 公共API路由
- `__init__.py`: 标识为Python包

### dao/
数据访问层(Data Access Object)
- 数据库操作封装
- 模型定义

### services/
业务服务层
- 核心业务逻辑实现
- 服务组合

### utils/
工具函数库
- 公共工具函数
- 辅助类

### 配置文件
- `config_dev.py`: 开发环境配置
- `config_prod.py`: 生产环境配置

### 核心文件
- `main.py`: FastAPI应用入口
- `requirements.txt`: 项目依赖列表

## 快速开始

1. 安装依赖:
```bash
pip install -r requirements.txt
```

2. 运行服务器(默认使用8080端口):
```bash
python main.py
```
或直接使用uvicorn:
```bash
uvicorn main:app --port 8080 --reload
uvicorn main:app --reload
```

3. 访问API文档:
http://127.0.0.1:8080/docs

## 配置说明
- 端口号在config_dev.py和config_prod.py中配置
- 开发环境默认端口: 8080
- 生产环境默认端口: 8080