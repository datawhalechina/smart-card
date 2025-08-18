import uuid
from datetime import timedelta

from fastapi import Depends, Form, Request
from sqlalchemy.ext.asyncio import AsyncSession

from config.config import settings
from config.enums import RedisInitKeyConfig
from entity.vo.auth_vo import UserRegister, AddUserModel
from entity.vo.common_vo import  ResponseModel, LoginTokenResult
from services.user_service import UserService
from utils.exceptions.exception import ServiceException
from utils.pwd_util import PwdUtil


class LoginService:
    """
    登录模块服务层
    """
    @classmethod
    async def register_user_services(cls, request: Request, query_db: AsyncSession, user_register: UserRegister):
        """
        用户注册services

        :param request: Request对象
        :param query_db: orm对象
        :param user_register: 注册用户对象
        :return: 注册结果
        """
        register_enabled = (
            True
            if await request.app.state.redis.get(f'{RedisInitKeyConfig.SYS_CONFIG.key}:sys.account.registerUser')
            == 'true'
            else False
        )
        captcha_enabled = (
            True
            if await request.app.state.redis.get(f'{RedisInitKeyConfig.SYS_CONFIG.key}:sys.account.captchaEnabled')
            == 'true'
            else False
        )
        if user_register.password == user_register.confirmPassword:
            if register_enabled:
                if captcha_enabled:
                    captcha_value = await request.app.state.redis.get(
                        f'{RedisInitKeyConfig.CAPTCHA_CODES.key}:{user_register.uuid}'
                    )
                    if not captcha_value:
                        raise ServiceException(message='验证码已失效')
                    elif user_register.code != str(captcha_value):
                        raise ServiceException(message='验证码错误')
                add_user = AddUserModel(
                    userName=user_register.username,
                    nickName=user_register.username,
                    password=PwdUtil.get_password_hash(user_register.password),
                    email=user_register.email,
                )
                result = await UserService.add_user_services(query_db, add_user)
                return result
            else:
                raise ServiceException(message='注册程序已关闭，禁止注册')
        else:
            raise ServiceException(message='两次输入的密码不一致')

    @classmethod
    async def login_user_services(cls, request: Request, query_db, user_login):

        # 登录check
        # 登录用户名密码比对
        check_login_user_services = await UserService.check_login_user_services(query_db, user_login)
        # 登录成功，发放Token，返回登录成功信息，登录表中写入登录时间
        if not check_login_user_services:
            raise ServiceException(message='登录失败')
        else:
            access_token_expires = timedelta(minutes=settings.jwt_expire_minutes)
            session_id = str(uuid.uuid4())
            # 生成Token
            access_token = await PwdUtil.create_access_token(
                data={
                    'user_name': user_login.username,
                    'session_id': session_id,
                },
                expires_delta=access_token_expires,
            )
            token_data = LoginTokenResult(
                token=access_token  # 实际应替换为动态生成的token
            )

            # 保存到redis
            await request.app.state.redis.set(
                f'{user_login.username}:{access_token}', access_token, ex=timedelta(settings.jwt_expire_minutes)
            )
            return ResponseModel[LoginTokenResult](is_success=True, message='登录成功,token已发放', result=token_data)
