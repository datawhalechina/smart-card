
# 📦 API 接口请求与响应规范

本项目采用统一的 API 数据结构，适用于前后端分离架构，涵盖请求参数规范、安全校验机制、响应格式等内容。

---

## 🔐 请求结构（Request）

```json
{
  "meta": {
    "timestamp": 1723037946,
    "nonce": "abcdef123456",
    "signature": "a1b2c3d4e5f6g7h8i9j0",
    "traceId": "req-7890"
  },
  "paging": {
    "page": 1,
    "pageSize": 10
  },
  "data": {
    "username": "testuser1",
    "password": "user123",
    "confirmPassword": "user123",
    "email": "testuser1@sohu.com",
    "code": "1234",
    "uuid": "123456789"
  }
}
```

### ✅ 字段说明

#### `meta` 公共元信息（所有接口通用）
| 字段名       | 类型     | 说明 |
|--------------|----------|------|
| `timestamp`  | int      | 发起请求的时间戳（秒） |
| `nonce`      | string   | 请求唯一随机串，防止重放攻击 |
| `signature`  | string   | 请求签名（详见下方校验逻辑） |
| `traceId`    | string   | 链路追踪 ID，用于日志排查 |
| `clientType` | string   | 客户端类型，如 `web`、`app`、`miniapp` |
| `locale`     | string   | 语言地区，如 `zh-CN`、`en-US` |
| `version`    | string   | 客户端版本号 |

#### `paging` 分页信息（可选）
| 字段名      | 类型   | 说明 |
|-------------|--------|------|
| `page`      | int    | 当前页数 |
| `pageSize`  | int    | 每页数量 |

#### `data` 业务数据
具体字段依据接口功能而定，如注册、登录、搜索等。

---

## 📤 响应结构（Response）

```json
{
  "code": 0,
  "message": "操作成功",
  "traceId": "req-7890",
  "data": {
    "userId": 1001,
    "username": "testuser1",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  },
  "paging": {
    "total": 100,
    "page": 1,
    "pageSize": 10
  },
  "serverTime": 1723037947
}
```

### ✅ 字段说明

| 字段名       | 类型     | 说明 |
|--------------|----------|------|
| `code`       | int      | 状态码，0 表示成功，非 0 表示业务异常 |
| `message`    | string   | 状态描述信息 |
| `traceId`    | string   | 与请求对应的追踪 ID |
| `data`       | object   | 返回的业务数据内容 |
| `paging`     | object   | 分页信息（可选） |
| `serverTime` | int      | 接口响应时间戳（秒） |

---

## 🔑 签名机制（Signature）

### 加签方式（客户端）

使用 `HMAC-SHA256` 算法对以下字符串进行签名：

```text
signature = HMAC_SHA256(secretKey, timestamp + nonce + JSON.stringify(data))
```

> 建议：对 `data` 使用 `JSON.stringify(data, null, 0)` 并排序字段，确保一致性。

### 后端验签伪代码

```python
import hmac
import hashlib
import json

def verify_signature(header: dict, data: dict, secret_key: str) -> bool:
    raw_string = f"{header['timestamp']}{header['nonce']}{json.dumps(data, separators=(',', ':'), sort_keys=True)}"
    expected = hmac.new(secret_key.encode(), raw_string.encode(), hashlib.sha256).hexdigest()
    return expected == header.get("signature")
```

### 防重放攻击建议

- 后端存储最近请求的 `nonce` + `timestamp`（可用 Redis）
- 拒绝重复 `nonce` 或超时请求（如 5 分钟内有效）

---

## 📎 状态码规范（示例）

| code | 含义说明        |
|------|-----------------|
| 0    | 成功            |
| 10001| 验证码错误       |
| 10002| 用户名重复       |
| 10003| 参数不合法       |
| 20001| 登录已过期       |
| 50000| 系统内部错误     |

---

## 🚀 使用建议

- 所有接口均建议统一此规范，便于中间件处理、日志追踪和前端统一封装
- 非分页接口可省略 `paging`
- 建议所有请求均添加 `traceId`，方便问题定位
- 所有敏感数据（如 token）请使用 HTTPS 传输

---

如需接口 SDK 示例或调试工具，请参考项目中的 `docs/sdk/` 或联系架构组。


## 接口请求示例
### 注册接口
请求路径：
请求入参：
```
curl -X 'POST' \
  'http://localhost:8000/admin/v1/auth/register' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "meta": {
    "timestamp": 1723037946,
    "nonce": "abcdef123456",
    "signature": "a1b2c3d4e5f6g7h8i9j0",
    "traceId": "req-7890"
  },
  "paging": {
    "page": 1,
    "pageSize": 10
  },
  "data": {
    "username": "testuser1",
    "password": "user123",
    "confirmPassword": "user123",
    "email": "testuser1@sohu.com",
    "code": "1234",
    "uuid": "123456789"
  }
}' ```

请求成功出参：
```{
  "code": 200,
  "msg": "新增成功",
  "data": {
    "is_success": true,
    "message": "新增成功",
    "result": null
  },
  "success": true,
  "time": "2025-08-09T13:37:24.951186"
}``` 

请求失败：
```
{
  "code": 409,
  "msg": "新增用户testuser1失败，登录账号已存在",
  "success": false,
  "time": "2025-08-09T13:40:22.302610"
}
```