from model.value_info.abstract_value_info import AbstractValueInfo
from model.value_info.role_value_info import RoleValueInfo


class RoleHeroValueInfo(AbstractValueInfo, RoleValueInfo):
    def __init__(self, id: int) -> None:
        super().__init__(id)

    @staticmethod
    def new_from_content(content: dict):
        # 基础数值
        ret = RoleHeroValueInfo(content.get("id", 0))
        ret.set_basic_value_from_basic_content(content.get("value", {}))
        return ret
