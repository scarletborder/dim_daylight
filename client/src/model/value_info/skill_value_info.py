from model.value_info.abstract_value_info import AbstractValueInfo

# from model.battle.skill.skill_effect import SkillEffect

from constant.battle import enum_skill_receiver


class SkillValueInfo(AbstractValueInfo):
    """只包含有名字，技能效果(一个effect格式字符串的list)"""

    def __init__(self, id: int) -> None:
        super().__init__()
        self.id = id
        self.name = ""
        self.description = ""
        self.target = 0
        self.skill_effects: list[SkillEffect] = []

    @staticmethod
    def new_from_content(content: dict):
        ret = SkillValueInfo(content.get("id", 0))

        return ret
