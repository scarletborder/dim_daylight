from src.constant.battle.enum_skill_method import MELEE, PROJECTILE, COUNTERATTACK
from src.storage.main_db import Main_DB
from src.constant.battle.enum_role_value import EnumRoleValue
from src.constant.battle.enum_event import EnumBattleEvent
from src.constant.enum_modify_calculate import EnumModifyCalculate
from src.model.battle.battle import Battle
from src.model.battle.event_callback import RoleEventCallback

from src.data.skill.skill_1 import blade_add
from src.utils.battle.calculate_pos import position_calc

"""穿透飞刀
active
attack
description 
effect:{}

"""


def cast_func(caster_quid, target_quid, battle: Battle, **kwargs):
    offset = round(
        battle.layout[caster_quid].value_dict.get(EnumRoleValue.ENUM_ATTACK, 0)
        * (
            1.3
            - battle.layout[target_quid].value_dict.get(EnumRoleValue.ENUM_DEFENSE, 0)
            * (1 - battle.layout[caster_quid].context.get("armor_piercing", 0))
        )
    )
    battle.modify_role_value(
        target_quid, offset, EnumRoleValue.ENUM_HEALTH, EnumModifyCalculate.ENUM_DEC
    )
    blade_add(target_quid, battle, caster_quid)
    if (secondary_quid := position_calc.back(target_quid)) is not None and (
        (secondary_quid) in battle.layout is True
        and battle.is_dead_by_quid(secondary_quid) is False
    ):
        offset = round(
            battle.layout[caster_quid].value_dict.get(EnumRoleValue.ENUM_ATTACK, 0)
            * (
                1.3
                - battle.layout[secondary_quid].value_dict.get(
                    EnumRoleValue.ENUM_DEFENSE, 0
                )
                * (1 - battle.layout[caster_quid].context.get("armor_piercing", 0))
            )
        )
        battle.modify_role_value(
            secondary_quid,
            offset,
            EnumRoleValue.ENUM_HEALTH,
            EnumModifyCalculate.ENUM_DEC,
        )


def display_func(caster_quid, target_quid, battle: Battle): ...


data = {}
data["name"] = "测试技能2-咲夜穿刺飞刀"
data["description"] = (
    "spell攻击，对两个敌人造成1.3倍攻击伤害，防御效果正常,施加一层刀锋"
)
data["range_method"] = PROJECTILE
data["cast_func"] = cast_func
data["display_func"] = display_func

Main_DB.write_bulk_data("skill_table", 2, data)
