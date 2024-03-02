from src.storage.main_db import Main_DB
import random
from src.constant.battle.enum_role_value import EnumRoleValue


def handle_func(role_id: int, role_info: dict):
    if role_id == 1:
        if random.random() > 0.5:
            role_info["name"] += " FAST"
            role_info["value_content"][EnumRoleValue.ENUM_SPEED] += 5

    elif role_id == 2:
        if random.random() > 0.5:
            role_info["name"] += " FLAME"
            role_info["weakness"] = [0, 0, 2, 8]


Main_DB.write_bulk_data(
    "mob_gang_table",
    1,
    {
        "mob_id_list": [1, 2],
        "quid_list": [0, 1],
        "handle_basic_content_func": handle_func,
    },
)
