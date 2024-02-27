from src.view.scene.abstract_scene import AbstractScene


class SceneManager:
    def __init__(self):
        self.active_scene = None

    def switch_to_scene(self, scene: AbstractScene):
        self.active_scene = scene

    def process_input(self, events, pressed_keys):
        if self.active_scene is not None:
            return self.active_scene.process_input(events, pressed_keys)

    def update(self):
        if self.active_scene is not None:
            return self.active_scene.update()
        else:
            return []

    def render(self, screen, fps: int):
        if self.active_scene is not None:
            self.active_scene.render(screen, fps)

    def get_update_rects(self):
        if self.active_scene is not None:
            return self.active_scene.get_update_rects()
