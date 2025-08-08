from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from entity.do.user_dao import SysUser
from entity.vo.user_vo import UserModel


class UserDal:
    """
    用户管理模块数据库操作层
    """

    @classmethod
    async def add_user_dao(cls, db: AsyncSession, user: UserModel):
        """
        新增用户数据库操作

        :param db: orm对象
        :param user: 用户对象
        :return: 新增校验结果
        """
        db_user = SysUser(**user.model_dump(exclude={'admin'}))
        db.add(db_user)
        await db.flush()

        return db_user

    @classmethod
    async def get_user_by_info(cls, db: AsyncSession, user: UserModel):
        """
                根据用户参数获取用户信息

                :param db: orm对象
                :param user: 用户参数
                :return: 当前用户参数的用户信息对象
                """
        query_user_info = (
            (
                await db.execute(
                    select(SysUser)
                    .where(
                        SysUser.del_flag == '0',
                        SysUser.user_name == user.user_name if user.user_name else True,
                        SysUser.phonenumber == user.phonenumber if user.phonenumber else True,
                        SysUser.email == user.email if user.email else True,
                    )
                    .order_by(desc(SysUser.create_time))
                    .distinct()
                )
            )
            .scalars()
            .first()
        )

        return query_user_info


