from fastapi import Depends, Form, Request
from sqlalchemy.ext.asyncio import AsyncSession

from config.enums import RedisInitKeyConfig
from entity.vo.auth_vo import UserRegister, AddUserModel
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
        if user_register.password == user_register.confirm_password:
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
                )
                result = await UserService.add_user_services(query_db, add_user)
                return result
            else:
                raise ServiceException(message='注册程序已关闭，禁止注册')
        else:
            raise ServiceException(message='两次输入的密码不一致')