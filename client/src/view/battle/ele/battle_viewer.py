import pygame
from src.model.battle.battle import Battle
from src.constant.battle.enum_battle_stage import EnumBattleStage


class BattleViewer:
    """切换至战斗界面"""

    def __init__(self, battle: Battle) -> None:
        self.role_views = []

        # 加载元素

        self.current_battle_stage = EnumBattleStage.SELECT_SKILL

    def load_elements(self): ...

    def get_main_screen(self, main_screen: pygame.surface.Surface): ...

    # def enter_new_stage(self, new_stage: BattleStage) -> list[tuple]:
    #     self.current_battle_stage = new_stage
    #     pygame.event.set_blocked(None)
    #     pygame.event.set_allowed(pygame.QUIT)
    #     pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)  # 允许鼠标点击事件
    #     pygame.event.set_allowed(pygame.MOUSEMOTION)  # 允许鼠标移动事件
    #     pygame.event.set_allowed(pygame.MOUSEBUTTONUP)  # 允许鼠标点击事件
    #     pygame.event.set_allowed(pygame.KEYDOWN)
    #     pygame.event.set_allowed(pygame.KEYUP)

    #     match new_stage:
    #         case BattleStage.SELECT_SKILL:
    #             return []
    #         case BattleStage.SELECT_TARGET:
    #             return []


"""
                    # 敌方
                    ("0",  False),
                    ("1",  False),
                    ("2",  False),
                    ("3",  False),
                    ("4",  False),
                    ("5",  False),
                    ("6",  False),
                    ("7",  False),
                    ("8",  False),
                    ("9",  False),
                    # 己方
                    (")",  False),
                    ("!",  False),
                    ("@",  False),
                    ("#",  False),
                    ("$",  False),
                    ("%",  False),
                    ("^",  False),
                    ("&",  False),
                    ("*",  False),
                    ("(",  False),
                    # 技能
                    ("q", False),
                    ("w", False),
                    ("e", False),
                    # log
                    (",", False),
                    (".", False),
"""
