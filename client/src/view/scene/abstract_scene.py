import pygame


# 场景基类
class AbstractScene:
    def __init__(self):
        self.update_rects = []
        pass

    def process_input(
        self, events: list[pygame.event.Event], pressed_keys: pygame.key.ScancodeWrapper
    ):
        pass

    def update(self):
        pass

    def get_update_rects(self):
        return self.update_rects

    def render(self):
        pass
