from src.constant.battle.enum_skill_method import MELEE, PROJECTILE, COUNTERATTACK
from src.storage.main_db import Main_DB
from src.constant.battle.enum_role_value import EnumRoleValue
from src.constant.battle.enum_event import EnumBattleEvent
from src.constant.enum_modify_calculate import EnumModifyCalculate
from src.model.battle.battle import Battle
from src.model.battle.event_callback import RoleEventCallback

from src.data.skill.skill_4 import cast_func as general_cast_func  # 经典防御
from src.data.skill.skill_1 import blade_add

"""咲夜的主动防御
active
description 主动防御后的敌方阶段，如果敌方的带有近战属性的攻击被咲夜的即时防御成功，则附加一次无属性追击并加一把刀
effect:{}

"""


def del_all_del_callback(
    caster_quid, target_quid, battle: Battle, context, **kwargs
) -> bool:
    listener = battle.layout[caster_quid].role_event_listener.get(
        EnumBattleEvent.ENUM_ON_QDEF, []
    )
    if len(listener) == 0:
        return False
    new_lis = []
    for lis in listener:
        if lis.context.get("del_in_global_turn_end", False) is False:
            new_lis.append(lis)

    battle.layout[caster_quid].role_event_listener[
        EnumBattleEvent.ENUM_ON_QDEF
    ] = new_lis
    return False


def cast_func(caster_quid, target_quid, battle: Battle, **kwargs):
    general_cast_func(caster_quid, target_quid, battle, **kwargs)

    def des_func(context):
        return "对近战攻击释放快速防御时施加小刀"

    def qdef_back_attack(
        caster_quid, target_quid, battle: Battle, context, **kwargs
    ) -> bool:
        if kwargs.get("method") == MELEE:
            # 防御的是近战攻击
            blade_add(target_quid, battle, caster_quid)
        return False

    battle.layout[caster_quid].add_role_event_listener(
        EnumBattleEvent.ENUM_ON_QDEF,
        RoleEventCallback(
            qdef_back_attack, des_func, None, del_in_global_turn_end=True
        ),
    )
    listener = battle.layout[caster_quid].role_event_listener.get(
        EnumBattleEvent.ENUM_GLOBAL_TURN_END, []
    )
    for lis in listener:
        if lis.context.get("del_in_global_turn_end", False) is True:
            return

    battle.layout[caster_quid].add_role_event_listener(
        EnumBattleEvent.ENUM_GLOBAL_TURN_END,
        RoleEventCallback(
            del_all_del_callback,
            lambda ctx: "删除所有无关项",
            None,
            del_in_global_turn_end=True,
        ),
    )


def display_func(caster_quid, target_quid, battle: Battle): ...


data = {}
data["name"] = "测试技能3-主动防御"
data["description"] = (
    "咲夜的主动防御,主动防御后的敌方阶段，如果敌方的带有近战属性的攻击被咲夜的即时防御成功，则附加一次刀锋"
)
data["range_method"] = COUNTERATTACK
data["cast_func"] = cast_func
data["display_func"] = display_func

Main_DB.write_bulk_data("skill_table", 3, data)
