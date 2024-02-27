from enum import IntEnum


class EnumBattleStage(IntEnum):
    # 自己的选择技能并释放阶段
    SELECT_SKILL = 0x0001
    SELECT_TARGET = 0x0002
    SCROLL_ITEM = 0x0003
    SELECT_FINAL_CASTER = 0x0004
    # 演示技能:别人的回合中
    READY_DEFENSE = 0x0011
    # 演示技能:自己的回合，别人回合回到原来的位置
    GENERAL_CAST = 0x0021
