"""存储拥有英雄的状态"""

from model.value_info.role_hero_value_info import RoleHeroValueInfo


class hero_state(RoleHeroValueInfo):
    current_value_name = {"current_health", "current_magic"}

    def __init__(self, id: int) -> None:
        super().__init__(id)
        # 一些不会在战斗结束后复原的属性
        self.current_value_dict: dict[str, int | None] = {
            "current_health": self.get_health_point(),
            "current_magic": self.get_magic_point(),
        }
        # 等级
        self.level = 1
        self.exp = 0

    def fix_exp(self):
        """针对目前exp和等级进行纠正"""
        if self.exp > 10:
            self.exp = 0
            self.level += 1


class user_heroes:
    def __init__(self) -> None:
        self.owned_heroes: dict[int, hero_state] = {}

    def add_hero(self, hero_id: int):
        self.owned_heroes[hero_id] = hero_state(hero_id)

    def modify_hero_state(self, hero_id: int, value_name: str, value: int):
        """对英雄的某个特定值的修改"""
        if value_name in hero_state.current_value_name:
            self.owned_heroes[hero_id].current_value_dict[value_name] = value
        elif (
            value_name in RoleHeroValueInfo.basic_value_name
            or value_name in RoleHeroValueInfo.advanced_value_name
        ):
            self.owned_heroes[hero_id].value_dict[value_name] = value

        elif value_name == "exp":
            self.owned_heroes[hero_id].exp = value
            self.owned_heroes[hero_id].fix_exp()
