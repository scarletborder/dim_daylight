"""拉取另一位玩家的出招"""

from src.constant.battle.enum_event import EnumBattleEvent
import queue


class PlayerSync:
    def __init__(self, pull_func, push_func) -> None:
        """
        :pull_func(queue) - 需要非阻塞的接收并保存到queue中
        :push_func(list[tuple[int, int, EnumBattleEvent, int]])) - 直接用来发送给对方
            - caster_quid, skill_id, operation_type, target_quid
        """
        self.pull_func = pull_func
        self.push_func = push_func
        self.chan = queue.Queue(1)
        pass

    def pull(self):
        self.pull_func(self.chan)

    def push(self, data: list[tuple[int, int, EnumBattleEvent, int]]):
        self.push_func(data)

    def result(self) -> list[tuple[int, int, EnumBattleEvent, int]]:
        return self.chan.get()

    def is_ok(self):
        return self.chan.empty() ^ True
