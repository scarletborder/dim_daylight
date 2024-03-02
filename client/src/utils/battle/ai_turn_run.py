"""ai进行操作"""

# 测试期间随机所有技能,释放其中一个
from src.utils.battle.player_sync import PlayerSync
from src.utils.battle.calculate_pos import position_calc
from src.constant.battle.enum_event import EnumBattleEvent
import queue


def pull_func(q: queue.Queue):
    # 随意选择，这里默认选择技能10
    q.put_nowait(
        [
            (0, 10, EnumBattleEvent.ENUM_ON_ATTACK, position_calc.random_me(10)),
            (1, 10, EnumBattleEvent.ENUM_ON_ATTACK, position_calc.random_me(10)),
        ]
    )


def push_func(a):
    return


Ai_ = PlayerSync(pull_func, push_func)
