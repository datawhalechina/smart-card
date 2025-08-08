# Smart Card API 项目文档

## 1 项目目录结构说明

```
backend/
├── app/                # 主应用模块
│   ├── admin/          # 管理后台相关路由
│   ├── public/         # 公共API路由
│   └── __init__.py         # Python包标识文件
├── config/             # 配置文件
│   └── __config_dev.py     # 开发环境配置
│   └── __config_prod.py    # 生产环境配置
├── dal/                # 数据访问层
├── doc/                # 设计文档 表定义
├── integration/        # 调用远程api
├── middlewares/        # 中间件 http拦截并处理
├── services/           # 业务服务层
├── utils/              # 工具函数库
├── main.py             # 应用入口和主配置
└── requirements.txt    # 项目依赖
```

### 1.1 目录详细说明

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



## 2 快速开始

1. 安装依赖:
```bash
 conda activate smartcard
 
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



### 2.1 配置说明

- 端口号在config_dev.py和config_prod.py中配置
- 开发环境默认端口: 8080
- 生产环境默认端口: 8080

4. 请求体和返回体



## 3 管理端API接口

### 3.1 注册登录时序图

``` mermaid
sequenceDiagram
    participant User as 用户
    participant React as React前端
    participant FastAPI as FastAPI后端
    participant Redis as Redis缓存
    participant DB as 数据库

    # 注册流程
    User->>React: 1. 填写注册信息(用户名/密码/邮箱等)
    React->>React: 2. 前端表单验证
    React->>FastAPI: 3. POST /api/register (JSON数据)
    
    FastAPI->>FastAPI: 4. 验证数据合法性
    FastAPI->>DB: 5. 检查用户名/邮箱是否已存在
    DB-->>FastAPI: 6. 返回查询结果
    
    alt 信息可用
        FastAPI->>FastAPI: 7. 密码哈希处理(bcrypt)
        FastAPI->>DB: 8. 创建用户记录
        DB-->>FastAPI: 9. 返回创建的用户ID
        
        FastAPI->>Redis: 10. 写入邮箱验证码(key:email_verify:xxx)
        Redis-->>FastAPI: 11. 存储成功确认
        
        FastAPI-->>React: 12. 返回201 + 验证提示
        React-->>User: 13. 显示验证提示
    else 信息已存在
        FastAPI-->>React: 7. 返回400错误
        React-->>User: 8. 显示错误信息
    end

    # 登录流程(与之前整合)
    User->>React: 14. 输入已注册的账号密码
    React->>FastAPI: 15. POST /api/login 
    FastAPI->>DB: 16. 验证用户凭证
    alt 验证成功
        FastAPI->>Redis: 17. 存储JWT令牌
        FastAPI-->>React: 18. 返回令牌
        React-->>User: 19. 登录成功
    else 验证失败
        FastAPI-->>React: 17. 返回401
        React-->>User: 18. 显示错误
    end

    note left of FastAPI: 注册关键逻辑：\n1. 密码必须哈希存储\n2. 敏感操作需验证邮箱\n3. Redis存储验证码限流
```





## 4 表设计

基于项目单一登录入口以及多角色的特点，用户表设计方案采用统一用户表。



### **方案对比：统一用户表 vs 分离用户表**

| **设计方式** | **统一用户表（推荐）**             | **分离用户表（传统）**                         |
| :----------- | :--------------------------------- | :--------------------------------------------- |
| **表结构**   | 基础用户表 + 角色表 + 扩展属性表   | 完全独立的表（如 `admins` 和 `consumers`）     |
| **典型场景** | 多角色系统（用户可能兼有多个角色） | 角色互斥且属性差异极大                         |
| **登录流程** | 单一点登录入口                     | 不同入口（如 `/admin/login` 和 `/user/login`） |
| **扩展性**   | 轻松新增角色类型                   | 每新增角色需建新表                             |
| **关联查询** | 需要 JOIN 操作                     | 直接查询对应表                                 |
| **权限控制** | 基于 RBAC 统一管理                 | 硬编码角色判断                                 |
| **代表案例** | AWS IAM、Shopify 后台              | 早期电商系统、简单CMS                          |







## 5 生成端的API接口设计

