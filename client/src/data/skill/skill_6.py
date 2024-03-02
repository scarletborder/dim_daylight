from src.constant.battle.enum_skill_method import MELEE, PROJECTILE, COUNTERATTACK
from src.storage.main_db import Main_DB
from src.constant.battle.enum_role_value import EnumRoleValue
from src.constant.battle.enum_event import EnumBattleEvent
from src.constant.enum_modify_calculate import EnumModifyCalculate
from src.model.battle.battle import Battle
from src.model.battle.event_callback import RoleEventCallback

from src.data.skill.skill_1 import blade_add

"""穿透飞刀
active
attack
description 
effect:{}

"""


def callback_func(caster_quid, target_quid, Battle: Battle, context, **kwargs) -> bool:
    if Battle.turn_times > context.get("casted_times", 0) + 1:
        Battle.modify_role_value(
            caster_quid, 5, EnumRoleValue.ENUM_DEFENSE, EnumModifyCalculate.ENUM_ADD
        )
        return True
    return False


def c_des_func(ctx: dict):
    return ""


def cast_func(caster_quid, target_quid, battle: Battle, **kwargs):
    offset = round(
        battle.layout[caster_quid].value_dict.get(EnumRoleValue.ENUM_ATTACK, 0)
        * (
            3
            - battle.layout[target_quid].value_dict.get(EnumRoleValue.ENUM_DEFENSE, 0)
            * (1 - battle.layout[caster_quid].context.get("armor_piercing", 0))
        )
    )
    battle.modify_role_value(
        target_quid, offset, EnumRoleValue.ENUM_HEALTH, EnumModifyCalculate.ENUM_DEC
    )
    blade_add(target_quid, battle, caster_quid)
    battle.layout[caster_quid].add_role_event_listener(
        EnumBattleEvent.ENUM_GLOBAL_TURN_END,
        RoleEventCallback(
            callback_func, c_des_func, None, casted_times=battle.turn_times
        ),
    )
    battle.modify_role_value(
        caster_quid, 5, EnumRoleValue.ENUM_DEFENSE, EnumModifyCalculate.ENUM_DEC
    )


def display_func(caster_quid, target_quid, battle: Battle): ...


data = {}
data["name"] = "测试技能5-咲夜大毁伤"
data["description"] = (
    "final spell攻击，对单个敌人造成3倍攻击伤害，防御效果正常,施加一层刀锋并减少自己防御值一回合"
)
data["range_method"] = MELEE
data["cast_func"] = cast_func
data["display_func"] = display_func

Main_DB.write_bulk_data("skill_table", 6, data)
