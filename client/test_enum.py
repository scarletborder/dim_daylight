from enum import StrEnum


class EnumRoleValue(StrEnum):
    ENUM_HEALTH = "HEALTH"
    ENUM_ENERGY = "ENERGY"
    ENUM_MAGIC = "MAGIC"
    ENUM_ATTACK = "ATTACK"
    ENUM_DEFENSE = "DEFENSE"
    ENUM_SPEED = "SPEED"
    ENUM_ATTACK_SPEED = "ATTACK_SPEED"
    ENUM_DEFENSE_SPEED = "DEFENSE_SPEED"


for v_name in EnumRoleValue:
    print(v_name)
