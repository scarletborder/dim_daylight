from src.storage.main_db import Main_DB

skill_table_dict = {
    "skill_table": [
        ("name", "TEXT"),
        ("description", "TEXT"),
        ("cast_func", "BLOB"),
        ("display_func", "BLOB"),
        ("range_method", "INTEGER"),
    ]
}
Main_DB.ensure_tables(skill_table_dict)

import src.data.skill.skill_0 as _
import src.data.skill.skill_1 as _
import src.data.skill.skill_2 as _
import src.data.skill.skill_3 as _
import src.data.skill.skill_4 as _
import src.data.skill.skill_5 as _
import src.data.skill.skill_6 as _
import src.data.skill.test_10 as _
import src.data.skill.test_11 as _
import src.data.skill.test_12 as _

Main_DB.display_table("skill_table")


# myf = Main_DB.read_data("skill_table", 10, "range_method", None)
# print(myf)
Main_DB.close()
