from datetime import timedelta, datetime, timezone
from typing import Union

from authlib.jose import jwt
from passlib.context import CryptContext

from config.config import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class PwdUtil:
    """
    密码工具类
    """

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        """
        工具方法：校验当前输入的密码与数据库存储的密码是否一致

        :param plain_password: 当前输入的密码
        :param hashed_password: 数据库存储的密码
        :return: 校验结果
        """
        return pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def get_password_hash(cls, input_password):
        """
        工具方法：对当前输入的密码进行加密

        :param input_password: 输入的密码
        :return: 加密成功的密码
        """
        return pwd_context.hash(input_password)

    @classmethod
    async def get_token_payload(cls, data: dict, expires_delta: Union[timedelta, None] = None):
        """
         获取生成token前的 payload 数据

         :param data: 登录信息
         :param expires_delta: token有效期
         :return: 生成token前的字典数据
         """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=30)
        to_encode.update({'exp': expire})
        return to_encode


    @classmethod
    async def create_access_token(cls, data: dict, expires_delta: Union[timedelta, None] = None):
        """
         根据登录信息创建当前用户token

         :param data: 登录信息
         :param expires_delta: token有效期
         :return: token
         """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=30)
        to_encode.update({'exp': expire})
        print(f'settings.jwt_secret_key: {settings.jwt_secret_key}, settings.jwt_algorithm: {settings.jwt_algorithm}')
        # authlib.jose算法实现
        # encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, settings.jwt_algorithm)
        # 修改 JWT 编码方式（authlib 的用法）
        encoded_jwt = jwt.encode(
            {'alg': settings.jwt_algorithm, 'typ': 'JWT'},  # 添加 header
            to_encode,
            settings.jwt_secret_key
        ).decode('utf-8')
        return encoded_jwt