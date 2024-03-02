"""
id : 0
"""

from src.storage.main_db import Main_DB
from src.constant.battle.enum_role_value import EnumRoleValue
from src.constant.battle.enum_event import EnumBattleEvent

role_data = {}

role_data["name"] = "十六夜咲夜"
role_data["description"] = "我是测试英雄0"
role_data["weakness"] = [6, 4, 0, 0]
role_data["operation_dict"] = {
    EnumBattleEvent.ENUM_ON_ATTACK: [1],
    EnumBattleEvent.ENUM_ON_SPELL: [2, 5],
    EnumBattleEvent.ENUM_ON_DEFENSE: [3],
    EnumBattleEvent.ENUM_ON_FINAL: [6],
    EnumBattleEvent.ENUM_ON_QDEF: [0],
}
role_data["value_content"] = {
    EnumRoleValue.ENUM_ATTACK: 10,
    EnumRoleValue.ENUM_DEFENSE: 10,
    EnumRoleValue.ENUM_HEALTH: 100,
    EnumRoleValue.ENUM_MAGIC: 100,
    EnumRoleValue.ENUM_SPEED: 10,
    EnumRoleValue.ENUM_ATTACK_SPEED: 15,
    EnumRoleValue.ENUM_DEFENSE_SPEED: 50,
}
role_data["role_view_detail"] = {
    "ratio_of_height": 0.06,
    "image_path": "resource/sprite_8.png",
}

Main_DB.write_bulk_data("role_table", 0, role_data)
