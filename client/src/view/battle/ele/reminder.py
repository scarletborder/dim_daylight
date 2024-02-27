import pygame
from storage.myLite_data_base import MyLiteDataBase
from src.view.battle.ele.battle_viewer import BattleViewer
from src.view.battle.ele.abstract_view_element import AbstractViewElement
from src.view.battle.ele.bulk_icon import BulkIcon
from model.battle.battle import Battle
from src.utils.view.text_span import render_text_within_rect


class ViewBattleReminder(AbstractViewElement):

    def __init__(self, resolution: tuple[int, int]) -> None:
        self.resolution = resolution
        self.update_flag = False

        self.frame_rect = pygame.Rect(
            0, 0.75 * resolution[1], 0.2 * resolution[0], 0.25 * resolution[1]
        )

        self.info_rect = pygame.Rect(
            0, 0.75 * resolution[1], 0.2 * resolution[0], 0.205 * resolution[1]
        )
        self.keytip_rect = pygame.Rect(
            0, 0.955 * resolution[1], 0.2 * resolution[0], 0.045 * resolution[1]
        )
        self.info_surfs = self.info_rects = self.tip_surfs = self.tip_rects = []

    def load_image(self, screen: pygame.Surface):
        self.old_bg_image = screen.subsurface(self.frame_rect).copy()
        pygame.draw.rect(screen, (255, 255, 255), self.frame_rect, 1)

    def update(
        self,
        screen: pygame.Surface,
        text_info: str = "",
        text_keytip: str = "",
    ):
        self.update_flag = True
        screen.blit(self.old_bg_image, self.frame_rect)
        ret = []

        if text_info != "":
            self.info_rects = self.info_surfs = []
            # text info
            self.info_surfs, self.info_rects, _ = render_text_within_rect(
                screen,
                text_info,
                self.info_rect,
                initial_font_size=int(0.028 * self.resolution[1]),
                color=(255, 255, 25),
            )
            ret += self.info_rects

        if text_keytip != "":
            self.tip_surfs = self.tip_rects = []
            # key tip
            self.tip_surfs, self.tip_rects, _ = render_text_within_rect(
                screen,
                text_keytip,
                self.keytip_rect,
                initial_font_size=int(0.045 * self.resolution[1]),
                color=(244, 244, 244),
            )
            ret += self.tip_rects
        return ret

    def render(self, screen: pygame.Surface):
        if self.update_flag is False:
            return
        self.update_flag = False
        screen.blits(
            [
                (surface, rect)
                for surface, rect in zip(
                    self.info_surfs + self.tip_surfs, self.info_rects + self.tip_rects
                )
            ]
        )
