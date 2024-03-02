"""通用即时防御
active/passive
description{}
effect:{}

"""

from src.constant.battle.enum_skill_method import MELEE, PROJECTILE, COUNTERATTACK
from src.storage.main_db import Main_DB
from src.constant.battle.enum_role_value import EnumRoleValue
from src.constant.battle.enum_event import EnumBattleEvent
from src.constant.enum_modify_calculate import EnumModifyCalculate
from src.model.battle.battle import Battle
from src.model.battle.event_callback import RoleEventCallback


def cast_func(caster_quid, target_quid, battle: Battle, **kwargs):

    # 提升防御力，通用是10
    battle.modify_role_value(
        caster_quid, 10, EnumRoleValue.ENUM_DEFENSE, EnumModifyCalculate.ENUM_ADD
    )
    battle.modify_role_value(
        caster_quid, 10, EnumRoleValue.ENUM_DEFENSE_SPEED, EnumModifyCalculate.ENUM_ADD
    )

    # 调用执行防御函数
    battle.layout[caster_quid].cast_active_defense()

    # 添加事件监听器，在回合结束时减少防御并调用取消防御函数
    def end_active_defense(caster_quid, target_quid, battle: Battle, context, **kwargs):
        """
        callback_func : 函数接受caster_quid,target_quid,Battle,context(dict),**kwargs(cast的参数)作为参数，返回bool表示是否删除这个listener
        """
        battle.modify_role_value(
            caster_quid, 10, EnumRoleValue.ENUM_DEFENSE, EnumModifyCalculate.ENUM_DEC
        )
        battle.modify_role_value(
            caster_quid,
            10,
            EnumRoleValue.ENUM_DEFENSE_SPEED,
            EnumModifyCalculate.ENUM_DEC,
        )
        battle.layout[caster_quid].cancel_active_defense()
        return True

    def des_func(context):
        return "本回合结束后取消防御状态"

    battle.layout[caster_quid].add_role_event_listener(
        EnumBattleEvent.ENUM_GLOBAL_TURN_END,
        RoleEventCallback(end_active_defense, des_func),
    )


def display_func(caster_quid, target_quid, battle: Battle): ...


data = {}
data["name"] = "测试技能4-通用主动防御"
data["description"] = "通用主动防御增加10点防御能力"
data["range_method"] = COUNTERATTACK
data["cast_func"] = cast_func
data["display_func"] = display_func

Main_DB.write_bulk_data("skill_table", 4, data)
