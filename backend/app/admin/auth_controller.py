from fastapi import APIRouter
import logging

from config.get_db import get_db
from entity.standard_response import standard_response
from entity.vo.auth_vo import UserRegister
from entity.vo.common_vo import CrudResponseModel
from fastapi import APIRouter, Depends, Request
from pydantic import ValidationError

from services.auth_service import LoginService
from utils.request_util import RequestUtil
from utils.response_util import ResponseUtil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()

# 更具需求生成卡片接口

@router.post('/register', response_model = standard_response[CrudResponseModel])
async def register_user(request: Request, user_data: RequestUtil, query_db: AsyncSession = Depends(get_db)):

    user_register = UserRegister.model_validate(user_data.data.dict())
    user_register_result = await LoginService.register_user_services(request, query_db, user_register)
    logger.info(user_register_result.message)

    return ResponseUtil.success(data=user_register_result, msg=user_register_result.message)
