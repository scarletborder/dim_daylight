from src.constant.battle.enum_skill_method import MELEE, PROJECTILE
from src.storage.main_db import Main_DB
from src.constant.battle.enum_role_value import EnumRoleValue
from src.constant.battle.enum_event import EnumBattleEvent
from src.constant.enum_modify_calculate import EnumModifyCalculate
from src.model.battle.battle import Battle

from src.utils.battle.calculate_pos import position_calc

data = {}


def cast_func(caster_quid, target_quid, battle: Battle):
    # main target
    offset = round(
        battle.layout[caster_quid].value_dict.get(EnumRoleValue.ENUM_ATTACK, 0)
        * (
            1.3
            - battle.layout[target_quid].value_dict.get(EnumRoleValue.ENUM_DEFENSE, 0)
            * (0.88 - battle.layout[caster_quid].context.get("armor_piercing", 0))
        )
    )
    battle.modify_role_value(
        target_quid, offset, EnumRoleValue.ENUM_HEALTH, EnumModifyCalculate.ENUM_DEC
    )
    # T字形目标
    ## 如果有左边的对象
    if (secondary_quid := position_calc.left(target_quid)) is not None and (
        (secondary_quid) in battle.layout is True
        and battle.is_dead_by_quid(secondary_quid) is False
    ):
        offset = round(
            battle.layout[caster_quid].value_dict.get(EnumRoleValue.ENUM_ATTACK, 0)
            * (
                0.8
                - battle.layout[secondary_quid].value_dict.get(
                    EnumRoleValue.ENUM_DEFENSE, 0
                )
                * (0.95 - battle.layout[caster_quid].context.get("armor_piercing", 0))
            )
        )
        battle.modify_role_value(
            secondary_quid,
            offset,
            EnumRoleValue.ENUM_HEALTH,
            EnumModifyCalculate.ENUM_DEC,
        )
    ## 如果有右边的对象
    if (secondary_quid := position_calc.right(target_quid)) is not None and (
        (secondary_quid) in battle.layout is True
        and battle.is_dead_by_quid(secondary_quid) is False
    ):
        secondary_quid = target_quid + 1
        offset = round(
            battle.layout[caster_quid].value_dict.get(EnumRoleValue.ENUM_ATTACK, 0)
            * (
                0.8
                - battle.layout[secondary_quid].value_dict.get(
                    EnumRoleValue.ENUM_DEFENSE, 0
                )
                * (0.95 - battle.layout[caster_quid].context.get("armor_piercing", 0))
            )
        )
        battle.modify_role_value(
            secondary_quid,
            offset,
            EnumRoleValue.ENUM_HEALTH,
            EnumModifyCalculate.ENUM_DEC,
        )

    ## 如果有前方的对象
    if (secondary_quid := position_calc.front(target_quid)) is not None and (
        (secondary_quid) in battle.layout is True
        and battle.is_dead_by_quid(secondary_quid) is False
    ):
        secondary_quid = target_quid + 5
        offset = round(
            battle.layout[caster_quid].value_dict.get(EnumRoleValue.ENUM_ATTACK, 0)
            * (
                0.8
                - battle.layout[secondary_quid].value_dict.get(
                    EnumRoleValue.ENUM_DEFENSE, 0
                )
                * (0.95 - battle.layout[caster_quid].context.get("armor_piercing", 0))
            )
        )
        battle.modify_role_value(
            secondary_quid,
            offset,
            EnumRoleValue.ENUM_HEALTH,
            EnumModifyCalculate.ENUM_DEC,
        )

    elif (15 <= target_quid <= 19) and ((target_quid - 5) in battle.layout):
        secondary_quid = target_quid - 5
        offset = round(
            battle.layout[caster_quid].value_dict.get(EnumRoleValue.ENUM_ATTACK, 0)
            * (
                0.8
                - battle.layout[secondary_quid].value_dict.get(
                    EnumRoleValue.ENUM_DEFENSE, 0
                )
                * (0.95 - battle.layout[caster_quid].context.get("armor_piercing", 0))
            )
        )
        battle.modify_role_value(
            secondary_quid,
            offset,
            EnumRoleValue.ENUM_HEALTH,
            EnumModifyCalculate.ENUM_DEC,
        )


def display_func(caster_quid, target_quid, battle: Battle): ...


data["name"] = "测试技能12-寒冰咒"
data["description"] = (
    "mob寒冰咒，主要目标造成1.3倍攻击力自带12%穿透，T字形目标造成0.8倍攻击力自带5%穿透"
)
data["range_method"] = PROJECTILE
data["cast_func"] = cast_func
data["display_func"] = display_func

Main_DB.write_bulk_data("skill_table", 12, data)
