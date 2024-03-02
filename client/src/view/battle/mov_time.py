class MovTime:
    def __init__(self) -> None:
        """用来启动角色view element的移动 and  判断防卫的按键时间"""
        self.start_move_time: int = 0  # 开始移动的时间
        self.end_move_time: int = 0  # 单行停止时间
        self.has_set: bool = False  # 是否被设置开始
        self.start_flag: bool = False
        pass

    def set(self, start_time: int, end_time: int):
        self.start_move_time = start_time
        self.end_move_time = end_time
        self.start_flag = False
        self.has_set = True

    def reset(self):
        self.start_flag = False
        self.has_set = False

    def is_need_start_move(self, now_ticks: int) -> bool:
        """是否需要现在启动人物view ele开始移动，此方法会修改move flag
        :return bool
        - True: 已经到时间且之前并没有启动移动
        - False: 没有到时间或者已经启动移动
        """
        if self.has_set is False:
            return False
        if now_ticks < self.start_move_time:
            return False
        if self.start_flag:  # 已经开始移动
            return False
        self.start_flag = True
        return True

    def is_delayed(self, now_ticks: int):
        """是否落后于移动时间"""
        return now_ticks > self.end_move_time

    def is_in_scope(self, now_ticks: int):
        return self.start_move_time <= now_ticks <= self.end_move_time
