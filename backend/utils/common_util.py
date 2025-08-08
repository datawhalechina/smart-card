from typing import Any, Dict, List, Literal, Union
from config.database import Base
from sqlalchemy.orm.collections import InstrumentedList
import re

def worship():
    print("""
//////////////////////////////////////////////////////////////////////////////////////
//            ================  SMART CARD UP !  =================                  //
// ####  #    #   ##   #####  #####     ####    ##   #####  #####     #    # #####  //
//#      ##  ##  #  #  #    #   #      #    #  #  #  #    # #    #    #    # #    # //
// ####  # ## # #    # #    #   #      #      #    # #    # #    #    #    # #    # //
//     # #    # ###### #####    #      #      ###### #####  #    #    #    # #####  //
//#    # #    # #    # #   #    #      #    # #    # #   #  #    #    #    # #      //
// ####  #    # #    # #    #   #       ####  #    # #    # #####      ####  #      //
//            ================  SMART CARD UP !  =================                  //
//                   Secure • Reliable • Always Online                              //                                                             
//////////////////////////////////////////////////////////////////////////////////////
    """)



class SqlalchemyUtil:
    """
    sqlalchemy工具类
    """

    @classmethod
    def base_to_dict(
        cls, obj: Union[Base, Dict], transform_case: Literal['no_case', 'snake_to_camel', 'camel_to_snake'] = 'no_case'
    ):
        """
        将sqlalchemy模型对象转换为字典

        :param obj: sqlalchemy模型对象或普通字典
        :param transform_case: 转换得到的结果形式，可选的有'no_case'(不转换)、'snake_to_camel'(下划线转小驼峰)、'camel_to_snake'(小驼峰转下划线)，默认为'no_case'
        :return: 字典结果
        """
        if isinstance(obj, Base):
            base_dict = obj.__dict__.copy()
            base_dict.pop('_sa_instance_state', None)
            for name, value in base_dict.items():
                if isinstance(value, InstrumentedList):
                    base_dict[name] = cls.serialize_result(value, 'snake_to_camel')
        elif isinstance(obj, dict):
            base_dict = obj.copy()
        if transform_case == 'snake_to_camel':
            return {CamelCaseUtil.snake_to_camel(k): v for k, v in base_dict.items()}
        elif transform_case == 'camel_to_snake':
            return {SnakeCaseUtil.camel_to_snake(k): v for k, v in base_dict.items()}

        return base_dict



class SnakeCaseUtil:
    """
    小驼峰形式(camelCase)转下划线形式(snake_case)工具方法
    """

    @classmethod
    def camel_to_snake(cls, camel_str: str):
        """
        小驼峰形式字符串(camelCase)转换为下划线形式字符串(snake_case)

        :param camel_str: 小驼峰形式字符串
        :return: 下划线形式字符串
        """
        # 在大写字母前添加一个下划线，然后将整个字符串转为小写
        words = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_str)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', words).lower()

    @classmethod
    def transform_result(cls, result: Any):
        """
        针对不同类型将下划线形式(snake_case)批量转换为小驼峰形式(camelCase)方法

        :param result: 输入数据
        :return: 小驼峰形式结果
        """
        return SqlalchemyUtil.serialize_result(result=result, transform_case='camel_to_snake')


class CamelCaseUtil:
    """
    下划线形式(snake_case)转小驼峰形式(camelCase)工具方法
    """

    @classmethod
    def snake_to_camel(cls, snake_str: str):
        """
        下划线形式字符串(snake_case)转换为小驼峰形式字符串(camelCase)

        :param snake_str: 下划线形式字符串
        :return: 小驼峰形式字符串
        """
        # 分割字符串
        words = snake_str.split('_')
        # 小驼峰命名，第一个词首字母小写，其余词首字母大写
        return words[0] + ''.join(word.capitalize() for word in words[1:])

    @classmethod
    def transform_result(cls, result: Any):
        """
        针对不同类型将下划线形式(snake_case)批量转换为小驼峰形式(camelCase)方法

        :param result: 输入数据
        :return: 小驼峰形式结果
        """
        return SqlalchemyUtil.serialize_result(result=result, transform_case='snake_to_camel')
