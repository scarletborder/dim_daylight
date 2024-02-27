from model.value_info.abstract_value_info import AbstractValueInfo
from model.value_info.role_value_info import RoleValueInfo


class RoleMobValueInfo(AbstractValueInfo, RoleValueInfo):
    def __init__(
        self, id: int, active_skill_ids: list[int], passive_skill_ids: list[int]
    ) -> None:
        super().__init__(id)

        # 怪物专用
        self.active_skill_ids = active_skill_ids
        self.passive_skill_ids = passive_skill_ids

        self.name = ""
        self.description = ""
        self.weakness: list[int] = []

    @staticmethod
    def new_from_content(content: dict):
        # 基础数值
        ret = RoleMobValueInfo(
            content.get("id", 0),
            content.get("active_skill_ids", [0]),
            content.get("passive_skill_ids", [0]),
        )
        ret.set_basic_value_from_basic_content(content.get("value", {}))
        ret.name = content["mob"]["name"]
        ret.description = content["mob"]["description"]
        ret.weakness = content["mob"]["weakness"]
