from src.constant.battle import enum_skill_method


class Skill:
    def __init__(
        self,
        name: str,
        description: str,
        cast_func,
        display_func=None,
        range_method=enum_skill_method.MELEE,
    ) -> None:
        """
        ## 参数来源
        外部读取db，再穿进来
        ```
        res = db.read_all_values("skill_table", id, {})
        self.name = res.get("name")
        self.description = res.get("description")
        self.cast_func = res.get("cast_func")
        self.display_func = res.get("display_func")
        self.range_method = res.get("range_method")
        ```

        ## 参数要求
        - cast_func : 函数，接受(caster_quid, target_quid, battle)，返回None
                    需要在其中完成对role的value修改,extra,监听器修改

        - display_func : 函数，接受(caster_quid, target_quid, battle)，返回None
                    对view唯一单例发送显示函数的信息

        """
        self.name = name
        self.description = description
        self.cast_func = cast_func
        self.display_func = display_func
        self.range_method = range_method

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def cast(self, caster_quid, target_quid, battle):
        """
        如果是active，caster_quid就是发起者，target_quid就是选中的目标
        如果是passive，caster_quid就是battle中传入的自己，target_quid就是那个释放者
        """
        if self.cast_func is not None:
            self.cast_func(caster_quid, target_quid, battle)
        if self.display_func is not None:
            self.display_func(caster_quid, target_quid, battle)
