import random


class position_calc:
    # 有关战斗中位置的计算
    @staticmethod
    def front(quid) -> int | None:
        """根据quid返回站在前排的quid，不额外判定alive
        :return `int`
            - None: 没有
            - other: quid
        """
        if 5 <= quid < 10 or 10 <= quid < 15:
            return None

        if quid < 5:
            return quid + 5
        return quid - 5

    @staticmethod
    def back(quid) -> int | None:
        """根据quid返回站在后排的quid，不额外判定alive
        :return `int`
            - None: 没有
            - other: quid
        """
        if (5 <= quid < 15) is False:
            return None

        if quid < 10:
            return quid - 5
        return quid + 5

    @staticmethod
    def left(quid) -> int | None:
        """根据quid返回站在左下的quid，不额外判定alive
        :return `int`
            - None: 没有
            - other: quid
        """
        if quid + 1 % 5 == 0:
            return None

        return quid + 1

    @staticmethod
    def right(quid) -> int | None:
        """根据quid返回站在右上的quid，不额外判定alive
        :return `int`
            - None: 没有
            - other: quid
        """
        if quid % 5 == 0:
            return None

        return quid - 1

    @staticmethod
    def random_me(quid: int) -> int:
        """己方随机"""
        if 0 <= quid < 10:
            return random.randint(0, 9)
        else:
            return random.randint(10, 19)

    @staticmethod
    def reverse_party(quid: int) -> int:
        return 20 - quid
