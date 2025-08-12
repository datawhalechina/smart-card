import hmac
import hashlib
import json


def verify_signature(timestamp: str, nonce: str, secret_key: str, data: dict, signature: str) -> bool:
    return signature == get_signature(timestamp, nonce, secret_key, data)


def get_signature(timestamp: str, nonce: str, secret_key: str, data: dict) -> str:
    sorted_data_str = _sorted_data_str(data)
    sign_input = f"{sorted_data_str}{timestamp}{nonce}{secret_key}"
    signature = hmac.new(secret_key.encode(), sign_input.encode(), hashlib.sha256).hexdigest()
    print(f'signature: {signature}')
    return signature


def _sorted_data_str(data: dict) -> str:
        if not isinstance(data, dict):
            return ""
        sorted_items = sorted(data.items())
        return "&".join(f"{k}={json.dumps(v, separators=(',', ':'), ensure_ascii=False) if isinstance(v, (dict, list)) else v}" for k, v in sorted_items)



import secrets

# 生成 32 字节（64 字符）的随机密钥
secret_key = secrets.token_hex(32)
print(secret_key)


