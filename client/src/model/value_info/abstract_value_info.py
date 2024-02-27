from abc import ABC, abstractmethod


class AbstractValueInfo(ABC):

    @staticmethod
    @abstractmethod
    def new_from_content(content: dict):
        """从json反序列化后的`content` dict中读取相应内容，构建一个子类类型的value_info"""
        ...

    # dump
    """保存到本地内存和硬盘
    """
