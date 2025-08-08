from datetime import datetime, time
from sqlalchemy import and_, delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from entity.do.dict_dao import SysDictData
from entity.vo.dict_vo import DictDataPageQueryModel
from utils.page_util import PageUtil


class DictTypeDao:
    @classmethod
    async def get_dict_data_list(cls, db: AsyncSession, query_object: DictDataPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取字典数据列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 字典数据列表信息对象
        """
        query = (
            select(SysDictData)
            .where(
                SysDictData.dict_type == query_object.dict_type if query_object.dict_type else True,
                SysDictData.dict_label.like(f'%{query_object.dict_label}%') if query_object.dict_label else True,
                SysDictData.status == query_object.status if query_object.status else True,
            )
            .order_by(SysDictData.dict_sort)
            .distinct()
        )
        dict_data_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return dict_data_list
