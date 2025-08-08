from sqlalchemy.ext.asyncio import AsyncSession

from dal.user_dal import UserDal
from entity.vo.auth_vo import AddUserModel
from entity.vo.common_vo import CrudResponseModel
from entity.vo.user_vo import UserModel, UserRoleModel
from utils.constant import CommonConstant
from utils.exceptions.exception import ServiceException


class UserService:
    @classmethod
    async def add_user_services(cls, query_db: AsyncSession, page_object: AddUserModel):
        """
        新增用户信息service

        :param query_db: orm对象
        :param page_object: 新增用户对象
        :return: 新增用户校验结果
        """
        add_user = UserModel(**page_object.model_dump(by_alias=True))
        if not await cls.check_user_name_unique_services(query_db, page_object):
            raise ServiceException(message=f'新增用户{page_object.user_name}失败，登录账号已存在')
        elif page_object.phonenumber and not await cls.check_phonenumber_unique_services(query_db, page_object):
            raise ServiceException(message=f'新增用户{page_object.user_name}失败，手机号码已存在')
        elif page_object.email and not await cls.check_email_unique_services(query_db, page_object):
            raise ServiceException(message=f'新增用户{page_object.user_name}失败，邮箱账号已存在')
        else:
            try:
                add_result = await UserDal.add_user_dao(query_db, add_user)
                user_id = add_result.user_id
                if page_object.role_ids:
                    for role in page_object.role_ids:
                        await UserDal.add_user_role_dao(query_db, UserRoleModel(userId=user_id, roleId=role))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='新增成功')
            except Exception as e:
                await query_db.rollback()
                raise e

    @classmethod
    async def check_user_name_unique_services(cls, query_db: AsyncSession, page_object: UserModel):
        """
        校验用户名是否唯一service

        :param query_db: orm对象
        :param page_object: 用户对象
        :return: 校验结果
        """
        user_id = -1 if page_object.user_id is None else page_object.user_id
        user = await UserDal.get_user_by_info(query_db, UserModel(userName=page_object.user_name))
        if user and user.user_id != user_id:
            return CommonConstant.NOT_UNIQUE
        return CommonConstant.UNIQUE


    @classmethod
    async def check_phonenumber_unique_services(cls, query_db: AsyncSession, page_object: UserModel):
        """
        校验用户手机号是否唯一service

        :param query_db: orm对象
        :param page_object: 用户对象
        :return: 校验结果
        """
        user_id = -1 if page_object.user_id is None else page_object.user_id
        user = await UserDal.get_user_by_info(query_db, UserModel(phonenumber=page_object.phonenumber))
        if user and user.user_id != user_id:
            return CommonConstant.NOT_UNIQUE
        return CommonConstant.UNIQUE


    @classmethod
    async def check_email_unique_services(cls, query_db: AsyncSession, page_object: UserModel):
        """
        校验用户邮箱是否唯一service

        :param query_db: orm对象
        :param page_object: 用户对象
        :return: 校验结果
        """
        user_id = -1 if page_object.user_id is None else page_object.user_id
        user = await UserDal.get_user_by_info(query_db, UserModel(email=page_object.email))
        if user and user.user_id != user_id:
            return CommonConstant.NOT_UNIQUE
        return CommonConstant.UNIQUE