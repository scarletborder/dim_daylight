from src.storage.main_db import Main_DB

role_table = {
    "role_table": [
        ("name", "TEXT"),
        ("description", "TEXT"),
        ("weakness", "BLOB"),
        ("operation_dict", "BLOB"),
        ("value_content", "BLOB"),
        ("role_view_detail", "BLOB"),
    ]
}
Main_DB.ensure_tables(role_table)

import src.data.role.test01 as _
import src.data.role.test02 as _
import src.data.role.test00 as _

Main_DB.display_table("role_table")


Main_DB.close()
