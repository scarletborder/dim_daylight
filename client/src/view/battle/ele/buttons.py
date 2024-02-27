import pygame

# from storage.myLite_data_base import MyLiteDataBase
# from view.battle.battle_viewer import BattleViewer
from src.view.battle.abstract_view_element import AbstractViewElement

# from src.view.battle.bulk_icon import BulkIcon
# from model.battle.battle import Battle
# from src.utils.view.text_span import render_text_within_rect


class ViewButtons(AbstractViewElement):
    """画面中间下方"""

    def __init__(self, resolution: tuple[int, int]) -> None:
        self.resolution = resolution

        self.final_spell_rect = pygame.Rect(
            0.69 * resolution[0],
            0.94 * resolution[1],
            0.05 * resolution[0],
            0.05 * resolution[1],
        )
        self.item_rect = pygame.Rect(
            0.63 * resolution[0],
            0.94 * resolution[1],
            0.05 * resolution[0],
            0.05 * resolution[1],
        )

    def load_image(self, screen: pygame.Surface):
        pygame.draw.rect(screen, (100, 100, 100), self.final_spell_rect)
        pygame.draw.rect(screen, (100, 100, 100), self.item_rect)

    def update(self):
        return [self.final_spell_rect, self.item_rect]

    def render(self):
        return
