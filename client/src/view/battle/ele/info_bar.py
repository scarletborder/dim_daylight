import pygame
from src.storage.myLite_data_base import MyLiteDataBase
from src.view.battle.ele.battle_viewer import BattleViewer
from src.constant.battle.enum_role_value import EnumRoleValue
from src.model.battle.skill import Skill
from src.model.battle.battle_role import BattleRole
from src.model.battle.item import Item
from src.view.battle.ele.abstract_view_element import AbstractViewElement
from src.view.battle.ele.bulk_icon import BulkIcon
from src.model.battle.battle import Battle
from src.utils.view.text_span import render_text_within_rect


class ViewBattleInfoBar(AbstractViewElement):
    """画面右侧上方"""

    def __init__(self, resolution: tuple[int, int]) -> None:
        self.resolution = resolution
        self.update_flag = False  # False-None, True-info/item
        self.width = 0.25 * resolution[0]
        self.height = 0.8 * resolution[1]  # Full height of the screen
        self.x = resolution[0] - self.width  # Positioned at the right side
        self.y = 0

        self.items = []
        self.font = pygame.font.SysFont("SimSun", 30)  # Default font and size
        self.start_index = 0  # Index of the topmost item in the view
        self.end_index = 0  # 最下方的那个index
        self.item_heights = []  # Store the height of each item
        self.item_tops = []  # Store the top Y coordinate of each item
        self.wrapped_texts = []

        self.frame_rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def load_image(self, screen: pygame.Surface):
        self.old_bg_image = screen.subsurface(self.frame_rect).copy()
        pygame.draw.rect(screen, (255, 255, 255), self.frame_rect, 1)

    def reload_role_info(self, role: BattleRole, skills: list[Skill]):
        self.items = [role.name, role.description]
        if (v := role.value_dict.get(EnumRoleValue.ENUM_HEALTH)) is not None:
            self.items.append("HEALTH:" + str(v))
        if (v := role.value_dict.get(EnumRoleValue.ENUM_MAGIC)) is not None:
            self.items.append("MAGIC:" + str(v))
        if (v := role.value_dict.get(EnumRoleValue.ENUM_ENERGY)) is not None:
            self.items.append("ENERGY:" + str(v))
        if (v := role.value_dict.get(EnumRoleValue.ENUM_ATTACK)) is not None:
            self.items.append("ATTACK:" + str(v))
        if (v := role.value_dict.get(EnumRoleValue.ENUM_DEFENSE)) is not None:
            self.items.append("DEFENSE:" + str(v))
        if (v := role.value_dict.get(EnumRoleValue.ENUM_SPEED)) is not None:
            self.items.append("SPEED:" + str(v) + "\n")
        if (v := role.value_dict.get(EnumRoleValue.ENUM_ATTACK_SPEED)) is not None:
            self.items.append("ATTACK_SPEED:" + str(v))
        if (v := role.value_dict.get(EnumRoleValue.ENUM_DEFENSE_SPEED)) is not None:
            self.items.append("DEFENSE_SPEED:" + str(v))

        self.items += [t_item.name + ":" + t_item.description for t_item in skills]
        self.bind()

    def reload_items(self, items: list[tuple[Item, int]]):
        self.items = [
            t_item.name + "X" + str(number) + "\n" + t_item.description
            for t_item, number in items
        ]
        self.bind()

    """一些解析"""

    def update(self, is_up: bool):
        self.update_flag = True  # 0-None,1-info,2-items
        if is_up and self.start_index > 0:
            self.start_index -= 1
        elif is_up is False and self.end_index + 1 < len(self.items):
            self.start_index += 1
            self.end_index += 1
            next_total_height = sum(
                self.item_heights[self.start_index : self.end_index + 1]
            )
            while next_total_height > self.height:
                next_total_height -= self.item_heights[self.start_index]
                self.start_index += 1

        return [self.frame_rect]

    def render(self, screen: pygame.Surface):
        if self.update_flag is False:  # False-None,True for both items and skills:
            # 具体根据reload的项目决定
            return
        else:
            self.update_flag = False
            # 先清空原来rect
            screen.blit(self.old_bg_image, self.frame_rect)
            pygame.draw.rect(
                screen, (200, 200, 200), (self.x, self.y, self.width, self.height)
            )
            self.item_tops = []
            y_offset = 0
            for i in range(self.start_index, len(self.items)):
                if y_offset + self.item_heights[i] > self.height:
                    break  # Stop drawing if we run out of vertical space
                self.item_tops.append(self.y + y_offset)
                for line in self.wrapped_texts[i]:
                    text_surface = self.font.render(line, True, (0, 0, 0))
                    screen.blit(text_surface, (self.x, self.y + y_offset))
                    y_offset += self.font.get_height()
                pygame.draw.line(
                    screen,
                    (140, 14, 14),
                    (self.x, self.y + y_offset),
                    (self.resolution[0], self.y + y_offset),
                )

    def choose(self, mouse_pos: tuple[int, int]):
        """点击时，返回选项的绝对序号[0,len)
        需要在外部`        if self.frame_rect.collidepoint(mouse_pos):`
        """
        relative_y = mouse_pos[1]
        for i, top in enumerate(self.item_tops):
            if top <= relative_y < top + self.item_heights[i]:
                return self.start_index + i
        return None

    # low interface
    def wrap_text(self, text, max_width):
        lines = []
        for paragraph in text.split("\n"):  # Handle explicit line breaks
            words = paragraph.split(" ")
            line = words[0]
            for word in words[1:]:
                if self.font.size(line + " " + word)[0] <= max_width:
                    line += " " + word
                else:
                    lines.append(line)
                    line = word
            lines.append(line)
        return lines

    def bind(self, list: list[str] | None = None):
        self.update_flag = True
        if list is not None:
            self.items = list
        self.start_index = 0  # Reset the start index when a new list is bound
        self.end_index = 0  # 最下方的那个index
        self.item_heights = []
        self.item_tops = []
        self.wrapped_texts = []

        for i in range(len(self.items)):
            wrapped_text = self.wrap_text(self.items[i], self.width)
            # 一个多行文本的高度
            item_height = sum([self.font.get_height() for _ in wrapped_text])
            # print(item_height)

            self.item_heights.append(item_height)
            self.wrapped_texts.append(wrapped_text)

        total_height = 0
        while (
            self.end_index < len(self.item_heights)
            and total_height + self.item_heights[self.end_index] < self.height
        ):
            total_height += self.item_heights[self.end_index]
            self.end_index += 1
