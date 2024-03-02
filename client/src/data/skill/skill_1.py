from src.constant.battle.enum_skill_method import MELEE, PROJECTILE, COUNTERATTACK
from src.storage.main_db import Main_DB
from src.constant.battle.enum_role_value import EnumRoleValue
from src.constant.battle.enum_event import EnumBattleEvent
from src.constant.enum_modify_calculate import EnumModifyCalculate
from src.model.battle.battle import Battle
from src.model.battle.event_callback import RoleEventCallback

"""{技能名称}
active/passive
description{}
effect:{}

"""

"""Silver Blade
passive
description 十六夜咲夜的部分技能会为命中的敌人附加一个[刀锋]效果，[刀锋]效果可以叠加。在一整个回合中如果没有被附加新的[刀锋]效果，
刀锋效果清空并造成一定额的伤害。如果[刀锋]效果达到n层也会直接清空并造成大额伤害。
effect:{}

"""


def blade_bomb_harm(target_quid, knife_number, battle: Battle, **kwargs):
    sakuya_quid = kwargs.get("sakuya_quid")
    rate = battle.layout[sakuya_quid].query_current_value(
        EnumRoleValue.ENUM_ATTACK
    ) / battle.layout[target_quid].query_current_value(EnumRoleValue.ENUM_DEFENSE)
    if knife_number == 5:
        return (
            (
                battle.layout[target_quid].query_default_value(
                    EnumRoleValue.ENUM_HEALTH
                )
                or 20
            )
            * 0.2
            * rate
        )
    return (
        (
            battle.layout[target_quid].query_default_value(EnumRoleValue.ENUM_HEALTH)
            or 20
        )
        * 0.03
        * knife_number
        * rate
    )


def blade_bomb_speed(target_quid, knife_number, battle: Battle, **kwargs):
    if knife_number == 5:
        return (
            battle.layout[target_quid].query_default_value(EnumRoleValue.ENUM_SPEED)
            or 20
        ) * 0.4
    return (
        (
            battle.layout[target_quid].query_default_value(EnumRoleValue.ENUM_HEALTH)
            or 20
        )
        * 0.05
        * knife_number
    )


def blade_bomb_attack_speed(target_quid, knife_number, battle: Battle, **kwargs):
    if knife_number == 5:
        return (
            battle.layout[target_quid].query_default_value(EnumRoleValue.ENUM_HEALTH)
            or 20
        ) * 0.5
    return (
        (
            battle.layout[target_quid].query_default_value(EnumRoleValue.ENUM_HEALTH)
            or 20
        )
        * 0.08
        * knife_number
    )


def blade_calc(target_quid, knife_number, battle: Battle, sakuya_quid):
    #  爆炸
    dec_hp = blade_bomb_harm(target_quid, knife_number, battle, sakuya_quid=sakuya_quid)
    dec_speed = blade_bomb_speed(target_quid, knife_number, battle)
    dec_attack_speed = blade_bomb_speed(target_quid, knife_number, battle)

    battle.modify_role_value(
        target_quid,
        dec_hp,
        EnumRoleValue.ENUM_HEALTH,
        EnumModifyCalculate.ENUM_DEC,
    )
    battle.modify_role_value(
        target_quid,
        dec_speed,
        EnumRoleValue.ENUM_SPEED,
        EnumModifyCalculate.ENUM_DEC,
    )
    battle.modify_role_value(
        target_quid,
        dec_attack_speed,
        EnumRoleValue.ENUM_ATTACK_SPEED,
        EnumModifyCalculate.ENUM_DEC,
    )


def blade_callback_func(
    caster_quid, target_quid, Battle: Battle, context: dict, **kwargs
) -> bool:
    casted_times = context.get("casted_times", 1)
    current_times = Battle.turn_times
    if (current_times - casted_times >= 2) or (context.get("sakuya_blade", 0) == 5):
        # direct bomb
        blade_calc(
            caster_quid, context.get("sakuya_blade", 0), Battle, context["sakuya_quid"]
        )
        return True
    else:
        context["sakuya_blade"] = context.get("sakuya_blade", 0) + 1
    return False


def blade_desp_func(ctx: dict):
    lev = ctx.get("sakuya_blade", 0)
    return f"[刀锋]:层数{lev},满5层爆炸"


def blade_add(target_quid, battle: Battle, sakuya_quid):
    # 遍历所有global_end状态施加小刀状态
    def add_one_blade(target_quid, knife_number, battle: Battle):
        """
        :return int: new number of knife
        """
        knife_number += 1
        if knife_number == 5:
            blade_calc(target_quid, knife_number, battle, sakuya_quid)
            knife_number = 0

        return knife_number

    listener = battle.layout[target_quid].role_event_listener.get(
        EnumBattleEvent.ENUM_TURN_END, []
    )
    no_flag = True
    for idx in range(len(listener)):
        if "sakuya_blade" in listener[idx].context and no_flag:
            # 这个是刀子
            knife_number = listener[idx].context.get("sakuya_blade", 0)
            listener[idx].context["sakuya_blade"] = add_one_blade(
                target_quid, knife_number, battle
            )

            return

    # 遍历完了没找到buff
    if no_flag:
        battle.layout[target_quid].add_role_event_listener(
            EnumBattleEvent.ENUM_TURN_END,
            RoleEventCallback(
                blade_callback_func,
                blade_desp_func,
                None,
                casted_times=battle.turn_times,
                sakuya_blade=1,
                sakuya_quid=sakuya_quid,
            ),
        )


def cast_func(caster_quid, target_quid, battle: Battle, **kwargs):
    offset = round(
        battle.layout[caster_quid].value_dict.get(EnumRoleValue.ENUM_ATTACK, 0)
        * (
            0.9
            - battle.layout[target_quid].value_dict.get(EnumRoleValue.ENUM_DEFENSE, 0)
            * (1 - battle.layout[caster_quid].context.get("armor_piercing", 0))
        )
    )
    battle.modify_role_value(
        target_quid, offset, EnumRoleValue.ENUM_HEALTH, EnumModifyCalculate.ENUM_DEC
    )
    blade_add(target_quid, battle, caster_quid)


def display_func(caster_quid, target_quid, battle: Battle): ...


data = {}
data["name"] = "测试技能1-咲夜普通攻击"
data["description"] = "普通攻击，造成0.9倍攻击伤害，防御效果正常,施加一层刀锋"
data["range_method"] = MELEE
data["cast_func"] = cast_func
data["display_func"] = display_func

Main_DB.write_bulk_data("skill_table", 1, data)
