from src.storage.main_db import Main_DB

mob_gang_table = {
    "mob_gang_table": [
        ("mob_id_list", "BLOB"),
        ("quid_list", "BLOB"),
        ("handle_basic_content_func", "BLOB"),
    ]
}
Main_DB.ensure_tables(mob_gang_table)

import src.data.gang.test01 as _

Main_DB.display_table("mob_gang_table")


Main_DB.close()
