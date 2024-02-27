from constant.battle.enum_role_value import EnumRoleValue


class RoleValueInfo:
    """所有角色怪物value info的通用基础数值"""

    def __init__(self, id: int) -> None:
        self.value_dict: dict[str, int | None] = dict()
        self.id = id
        self.weakness: list[int] = []

    def set_basic_value_from_basic_content(self, basic_content: dict[str, int]):
        """从content dict中的basic dict中读取基础数值"""
        self.value_dict.update(basic_content)
        for v_name in EnumRoleValue:
            if basic_content.get(v_name, None) is None:
                self.value_dict[v_name] = None  # 表示有这个key但是没有这个数值

    def get_health_point(self):
        return self.value_dict.get(EnumRoleValue.ENUM_HEALTH)

    def get_magic_point(self):
        return self.value_dict.get(EnumRoleValue.ENUM_MAGIC)

    def get_energy_point(self):
        return self.value_dict.get(EnumRoleValue.ENUM_ENERGY)

    def get_attack(self):
        return self.value_dict.get(EnumRoleValue.ENUM_ATTACK)

    def get_defense(self):
        return self.value_dict.get(EnumRoleValue.ENUM_DEFENSE)

    def get_speed(self):
        return self.value_dict.get(EnumRoleValue.ENUM_SPEED)

    def get_attack_speed(self):
        return self.value_dict.get(EnumRoleValue.ENUM_ATTACK_SPEED)

    def get_defense_speed(self):
        return self.value_dict.get(EnumRoleValue.ENUM_DEFENSE_SPEED)
