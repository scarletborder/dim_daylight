import sqlite3
import pickle


class MyLiteDataBase:
    """
    # 简易游戏数据库
    ## method
    写入，查询，批量写入，查询整块数据

    缺失的数据将会返回None

    ## example
    ```
    from mysqlite import MyLiteDataBase

    db_path = "game_data.db"
    db = MyLiteDataBase(db_path)

    # 定义表结构
    tables_dict = {
        "role_table": [
            ("name", "TEXT"),
            ("address", "TEXT"),
            ("skill_list", "BLOB"),  # 用于存储序列化的Python列表
        ],
        "skill_table": [("skill_func", "BLOB")],  # 用于存储序列化的函数对象
    }

    # 创建表
    db.ensure_tables(tables_dict)

    # 接下来可以使用write_data和read_data等方法操作数据库


    # 定义一个示例函数作为技能
    def example_skill():
        print("Epicmo已经超神了.")


    # 写入角色数据
    db.write_data("role_table", 1, "name", "scarletborder")
    db.write_data("role_table", 1, "skill_list", ["sleep", "打游戏"])
    db.write_bulk_data("role_table", 2, {"name": "epicmo", "skill_list": ["code", "约会"]})
    db.write_data("role_table", 3, "name", "wisdom go")
    # 写入技能数据


    # 读取角色数据
    role_data = db.read_data("role_table", 2, "name")
    print(f"Role Data: {role_data}")
    role_data = db.read_all_values("role_table", 1)
    print(f"Role Data: {role_data}")
    role_data = db.read_data("role_table", 3, "skill_list")
    print(f"Role Data: {role_data}")

    db.write_data("skill_table", 1, "skill_func", example_skill)

    # 读取并执行技能函数
    skill_func = db.read_data("skill_table", 1, "skill_func")
    if skill_func:
        skill_func()  # 这应该会执行example_skill函数

    db.close()
    ```
    return
    ```
    Role Data: epicmo
    Role Data: {'id': 1, 'name': 'scarletborder', 'address': None, 'skill_list': ['sleep', '打游戏']}
    Role Data: None
    Epicmo已经超神了.
    ```

    ## Author
    [scarletborder](https://github.com/scarletborder)
    """

    def __init__(self, db_path):
        self.__conn = sqlite3.connect(db_path)
        self.__conn.row_factory = sqlite3.Row
        self.__cursor = self.__conn.cursor()

    def ensure_tables(self, tables_dict: "dict[str, list[tuple[str,str]]]"):
        """定义表结构
        ```
        tables_dict = {
            "role_table": [
                ("name", "TEXT"),
                ("address", "TEXT"),
                ("skill_list", "BLOB"),  # 用于存储序列化的Python列表
            ],
            "skill_table": [("skill_func", "BLOB")],  # 用于存储序列化的函数对象
        }
        ```"""
        for table_name, columns in tables_dict.items():
            # 构建创建表的SQL语句
            columns_sql = ", ".join(
                [f"{col_name} {col_type}" for col_name, col_type in columns]
            )
            sql = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, {columns_sql})"
            self.__cursor.execute(sql)
        self.__conn.commit()

    def write_data(self, table_name: "str", id: "int", key: "str", value):
        # 序列化非基本数据类型
        if not isinstance(value, (int, float, str)):
            value = pickle.dumps(value)
        else:
            value = str(value)  # 确保value是可以直接写入SQL的格式

        # 动态SQL，注意SQL注入风险，确保参数安全
        sql = f"INSERT INTO {table_name} (id, {key}) VALUES (?, ?) ON CONFLICT(id) DO UPDATE SET {key} = ?"
        self.__cursor.execute(sql, (id, value, value))
        self.__conn.commit()

    def read_data(self, table_name: "str", id: "int", key: "str", default=None):
        # 动态SQL，注意SQL注入风险，确保参数安全
        sql = f"SELECT {key} FROM {table_name} WHERE id = ?"
        self.__cursor.execute(sql, (id,))
        row = self.__cursor.fetchone()
        if row:
            data = row[key]
            try:
                # 尝试反序列化，如果失败则直接返回原始数据
                return pickle.loads(data)
            except BaseException:
                return data
        return default

    def write_bulk_data(self, table_name: str, id: int, data_dict: dict):
        for key, value in data_dict.items():
            if not isinstance(value, (int, float, str)):
                value = pickle.dumps(value)
            else:
                value = str(value)
            sql = f"INSERT INTO {table_name} (id, {key}) VALUES (?, ?) ON CONFLICT(id) DO UPDATE SET {key} = ?"
            self.__cursor.execute(sql, (id, value, value))
        self.__conn.commit()

    def read_all_values(self, table_name: str, id: int, default: "dict|None" = None):
        sql = f"SELECT * FROM {table_name} WHERE id = ?"
        self.__cursor.execute(sql, (id,))
        row = self.__cursor.fetchone()
        if row:
            result = {}
            for key in row.keys():
                try:
                    result[key] = pickle.loads(row[key]) if key != "id" else row[key]
                except BaseException:
                    result[key] = row[key]
            return result
        return default

    def delete_record_by_id(self, table_name, id):
        # 动态构建删除特定ID记录的SQL语句，注意SQL注入风险，确保table_name参数安全
        sql = f"DELETE FROM {table_name} WHERE id = ?"
        self.__cursor.execute(sql, (id,))
        self.__conn.commit()

    def drop_table(self, table_name):
        # 动态构建删除表的SQL语句，注意SQL注入风险，确保table_name参数安全
        sql = f"DROP TABLE IF EXISTS {table_name}"
        self.__cursor.execute(sql)
        self.__conn.commit()

    def display_table(self, table_name):
        sql = f"SELECT * FROM {table_name}"
        self.__cursor.execute(sql)
        rows = self.__cursor.fetchall()

        if rows:
            # 打印列名
            columns = [description[0] for description in self.__cursor.description]
            print("\t".join(columns))
            # 打印每一行的数据
            for row in rows:
                print("\t".join(str(value) for value in row))
        else:
            print(f"No data found in {table_name}.")

    def close(self):
        self.__conn.close()
