import re
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import Network, NotBlank, Size, Xss
from typing import List, Literal, Optional


from utils.exceptions.exception import ModelValidatorException


class UserModel(BaseModel):
    """
    用户表对应pydantic模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    user_id: Optional[int] = Field(default=None, description='用户ID')
    dept_id: Optional[int] = Field(default=None, description='部门ID')
    user_name: Optional[str] = Field(default=None, description='用户账号')
    nick_name: Optional[str] = Field(default=None, description='用户昵称')
    user_type: Optional[str] = Field(default=None, description='用户类型（00系统用户）')
    email: Optional[str] = Field(default=None, description='用户邮箱')
    phonenumber: Optional[str] = Field(default=None, description='手机号码')
    sex: Optional[Literal['0', '1', '2']] = Field(default=None, description='用户性别（0男 1女 2未知）')
    avatar: Optional[str] = Field(default=None, description='头像地址')
    password: Optional[str] = Field(default=None, description='密码')
    status: Optional[Literal['0', '1']] = Field(default=None, description='帐号状态（0正常 1停用）')
    del_flag: Optional[Literal['0', '2']] = Field(default=None, description='删除标志（0代表存在 2代表删除）')
    login_ip: Optional[str] = Field(default=None, description='最后登录IP')
    login_date: Optional[datetime] = Field(default=None, description='最后登录时间')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')
    admin: Optional[bool] = Field(default=False, description='是否为admin')

    @model_validator(mode='after')
    def check_password(self) -> 'UserModel':
        pattern = r"""^[^<>"'|\\]+$"""
        if self.password is None or re.match(pattern, self.password):
            return self
        else:
            raise ModelValidatorException(message='密码不能包含非法字符：< > " \' \\ |')

    @model_validator(mode='after')
    def check_admin(self) -> 'UserModel':
        if self.user_id == 1:
            self.admin = True
        else:
            self.admin = False
        return self

    @Xss(field_name='user_name', message='用户账号不能包含脚本字符')
    @NotBlank(field_name='user_name', message='用户账号不能为空')
    @Size(field_name='user_name', min_length=0, max_length=30, message='用户账号长度不能超过30个字符')
    def get_user_name(self):
        return self.user_name

    @Xss(field_name='nick_name', message='用户昵称不能包含脚本字符')
    @Size(field_name='nick_name', min_length=0, max_length=30, message='用户昵称长度不能超过30个字符')
    def get_nick_name(self):
        return self.nick_name

    @Network(field_name='email', field_type='EmailStr', message='邮箱格式不正确')
    @Size(field_name='email', min_length=0, max_length=50, message='邮箱长度不能超过50个字符')
    def get_email(self):
        return self.email

    @Size(field_name='phonenumber', min_length=0, max_length=11, message='手机号码长度不能超过11个字符')
    def get_phonenumber(self):
        return self.phonenumber

    def validate_fields(self):
        self.get_user_name()
        self.get_nick_name()
        self.get_email()
        self.get_phonenumber()


class UserRoleModel(BaseModel):
    """
    用户和角色关联表对应pydantic模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    user_id: Optional[int] = Field(default=None, description='用户ID')
    role_id: Optional[int] = Field(default=None, description='角色ID')