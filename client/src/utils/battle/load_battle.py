"""加载战场"""

from model.battle import battle


def load_battle_ai():
    """between player and ai"""
    return battle.Battle()


def load_battle_player():
    """between two players"""
