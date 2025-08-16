import logging

from config.get_db import get_db
from entity.vo.auth_vo import UserRegister, RegisterResponseModel, UserLogin, LoginResponseModel
from fastapi import APIRouter, Depends, Request

from services.auth_service import LoginService
from utils.request_util import RequestUtil
from utils.response_util import ResponseUtil
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


# 登录接口
@router.post('/login', response_model = LoginResponseModel)
async def login_user(request: Request, user_login_data: RequestUtil[UserLogin], query_db: AsyncSession = Depends(get_db)):

    user_login = UserLogin.model_validate(user_login_data.data.dict())
    user_login_data_result = await LoginService.login_user_services(query_db, user_login)

    return ResponseUtil.success(data=user_login_data_result, msg=user_login_data_result.message)

# 更具需求生成卡片接口
# 注册接口
@router.post('/register', response_model = RegisterResponseModel)
async def register_user(request: Request, user_data: RequestUtil[UserRegister], query_db: AsyncSession = Depends(get_db)):

    user_register = UserRegister.model_validate(user_data.data.dict())
    user_register_result = await LoginService.register_user_services(request, query_db, user_register)
    logger.info(user_register_result.message)

    return ResponseUtil.success(data=user_register_result, msg=user_register_result.message)


