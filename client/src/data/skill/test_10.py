from src.constant.battle.enum_skill_method import MELEE, PROJECTILE
from src.storage.main_db import Main_DB
from src.constant.battle.enum_role_value import EnumRoleValue
from src.constant.battle.enum_event import EnumBattleEvent
from src.constant.enum_modify_calculate import EnumModifyCalculate
from src.model.battle.battle import Battle


def cast_func(caster_quid, target_quid, battle: Battle, **kwargs):
    offset = round(
        battle.layout[caster_quid].value_dict.get(EnumRoleValue.ENUM_ATTACK, 0)
        * (
            1
            - battle.layout[target_quid].value_dict.get(EnumRoleValue.ENUM_DEFENSE, 0)
            * (1 - battle.layout[caster_quid].context.get("armor_piercing", 0))
        )
    )
    battle.modify_role_value(
        target_quid, offset, EnumRoleValue.ENUM_HEALTH, EnumModifyCalculate.ENUM_DEC
    )


def display_func(caster_quid, target_quid, battle: Battle): ...


data = {}
data["name"] = "测试技能10-普通攻击"
data["description"] = "mob普通攻击，造成1.0倍攻击伤害，防御效果正常"
data["range_method"] = MELEE
data["cast_func"] = cast_func
data["display_func"] = display_func

Main_DB.write_bulk_data("skill_table", 10, data)
