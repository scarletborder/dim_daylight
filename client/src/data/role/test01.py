from storage.main_db import Main_DB
from constant.battle.enum_role_value import EnumRoleValue
from constant.battle.enum_event import EnumBattleEvent

role_data = {}

role_data["name"] = "测试妖精1"
role_data["description"] = "我是测试妖精1，有50%概率速度+5"
role_data["weakness"] = [0, 0, 5, 5]
role_data["operation_dict"] = {
    EnumBattleEvent.ENUM_ON_ATTACK: [10],
    EnumBattleEvent.ENUM_ON_SPELL: [12],
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


Main_DB.write_bulk_data("role_table", 1, role_data)
