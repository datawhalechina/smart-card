from sqlalchemy.ext.asyncio import AsyncSession

from entity.do.dict_dao import DictDataDao
from entity.vo.dict_vo import DictDataPageQueryModel


class DictDataService:
    """
    字典数据管理模块服务层
    """

    @classmethod
    async def get_dict_data_list_services(
        cls, query_db: AsyncSession, query_object: DictDataPageQueryModel, is_page: bool = False
    ):
        """
        获取字典数据列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 字典数据列表信息对象
        """
        dict_data_list_result = await DictDataDao.get_dict_data_list(query_db, query_object, is_page)

        return dict_data_list_result