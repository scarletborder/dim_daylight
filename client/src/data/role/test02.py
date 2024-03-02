"""
id:2
"""

from src.storage.main_db import Main_DB
from src.constant.battle.enum_role_value import EnumRoleValue
from src.constant.battle.enum_event import EnumBattleEvent

role_data = {}

role_data["name"] = "测试妖精2"
role_data["description"] = "我是测试妖精2，有50%概率刷为2水8火"
role_data["weakness"] = [0, 0, 10, 0]
role_data["operation_dict"] = {
    EnumBattleEvent.ENUM_ON_ATTACK: [10],
    EnumBattleEvent.ENUM_ON_SPELL: [11],
}
role_data["value_content"] = {
    EnumRoleValue.ENUM_ATTACK: 10,
    EnumRoleValue.ENUM_DEFENSE: 10,
    EnumRoleValue.ENUM_HEALTH: 100,
    EnumRoleValue.ENUM_MAGIC: 100,
    EnumRoleValue.ENUM_SPEED: 10,
    EnumRoleValue.ENUM_ATTACK_SPEED: 15,
    EnumRoleValue.ENUM_DEFENSE_SPEED: 15,
}

role_data["role_view_detail"] = {
    "ratio_of_height": 0.06,
    "image_path": "resource/sprite_5.png",
}
Main_DB.write_bulk_data("role_table", 2, role_data)
