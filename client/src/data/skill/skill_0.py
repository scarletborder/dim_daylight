from src.constant.battle.enum_skill_method import MELEE, PROJECTILE, COUNTERATTACK
from src.storage.main_db import Main_DB
from src.constant.battle.enum_role_value import EnumRoleValue
from src.constant.battle.enum_event import EnumBattleEvent
from src.constant.enum_modify_calculate import EnumModifyCalculate
from src.model.battle.battle import Battle
from src.model.battle.event_callback import RoleEventCallback

"""
什么都不做
"""


def cast_func(caster_quid, target_quid, battle: Battle, **kwargs):
    return


def display_func(caster_quid, target_quid, battle: Battle): ...


data = {}
data["name"] = "测试技能0-什么都不做"
data["description"] = "通用防御"
data["range_method"] = COUNTERATTACK
data["cast_func"] = cast_func
data["display_func"] = display_func

Main_DB.write_bulk_data("skill_table", 0, data)
