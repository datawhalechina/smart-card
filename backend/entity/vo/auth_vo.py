import re
from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic.alias_generators import to_camel
from typing import List, Optional, Union

from entity.vo.common_vo import ResponseModel
from entity.vo.user_vo import UserModel
from utils.exceptions.exception import ModelValidatorException


class UserRegister(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    username: str = Field(description='用户名称')
    password: str = Field(description='用户密码')
    email: str = Field(description='用户邮箱')
    confirmPassword: str = Field(description='用户二次确认密码')
    code: Optional[str] = Field(default=None, description='验证码')
    uuid: Optional[str] = Field(default=None, description='会话编号')

    @model_validator(mode='after')
    def check_password(self) -> 'UserRegister':
        pattern = r"""^[^<>"'|\\]+$"""
        if self.password is None or re.match(pattern, self.password):
            return self
        else:
            raise ModelValidatorException(message='密码不能包含非法字符：< > " \' \\ |')


class AddUserModel(UserModel):
    """
    新增用户模型
    """
    role_ids: Optional[List] = Field(default=[], description='角色ID信息')
    post_ids: Optional[List] = Field(default=[], description='岗位ID信息')
    type: Optional[str] = Field(default=None, description='操作类型')


class RegisterResponseModel(BaseModel):
    data: ResponseModel


class UserLogin(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    username: str = Field(description='用户名称')
    password: str = Field(description='用户密码')
    email: str = Field(description='用户邮箱')

    @model_validator(mode='after')
    def check_password(self) -> 'UserLogin':
        pattern = r"""^[^<>"'|\\]+$"""
        if self.password is None or re.match(pattern, self.password):
            return self
        else:
            raise ModelValidatorException(message='密码不能包含非法字符：< > " \' \\ |')



class LoginResponseModel(BaseModel):
    data: ResponseModel