import pygame
import math

from src.constant.battle.enum_battle_stage import EnumBattleStage
from src.utils.view.angle_to_choice import classify_angle_with_radians

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class SelectSkill:
    """用来绘制长按选择技能的圆圈的类"""

    def __init__(self) -> None:
        # 当前状态
        self.select_skill_status: bool = False  # 是否正在选择技能

        self.caster_quid_list: list[int] = []  # my team queue
        self.select_idx = 0  # always currently
        # self.caster_quid_list[self.select_idx] => select caster quid
        self.current_target_quid = 0

        self.current_skill_operation_id = 0
        self.current_item_id = 0

        self.skill_or_item = 0  # 0=skill, 1=item
        pass

    def load_new_queue(self, caster_quid_list: list[int]):
        if len(caster_quid_list) == 0:
            return 1
        self.caster_quid_list = caster_quid_list
        self.select_idx = -1
        return 0

    def start_next_select(self) -> int:
        """开始队列中的下一个角色选择技能
        :return `int`
        - caster_quid
        - `-1` (if queue is ended)
        """
        self.select_idx += 1
        if self.select_idx >= len(self.caster_quid_list):
            return -1

        return self.caster_quid_list[self.select_idx]

    def current_selected_caster_quid(self):
        return self.caster_quid_list[self.select_idx]

    def current_selected_queue_idx(self):
        return self.select_idx

    def is_select_skill(self):
        return self.select_skill_status

    # 画圆圈
    def get_original_rect(
        self, radius, mouse_pos: tuple[int, int], screen: pygame.Surface
    ):
        self.select_skill_status = True  # 长按确认开始
        self.circle_pos = mouse_pos
        self.radius = radius
        self.circle_rect = pygame.Rect(
            mouse_pos[0] - radius, mouse_pos[1] - radius, 2 * radius, 2 * radius
        )
        self.circle_mask_surface = screen.subsurface(self.circle_rect).copy()

        # 绘制大圆
        pygame.draw.circle(
            screen,
            WHITE,
            (mouse_pos[0], mouse_pos[1]),
            radius,
            1,
        )

        # 计算并绘制小圆
        self.inner_radius = radius // 2
        pygame.draw.circle(
            screen,
            WHITE,
            (mouse_pos[0], mouse_pos[1]),
            self.inner_radius,
            1,
        )

        # 计算并绘制线条
        angles = [45, 135, 225, 315]
        for angle in angles:
            outer_x = mouse_pos[0] + radius * math.cos(math.radians(angle))
            outer_y = mouse_pos[1] + radius * math.sin(math.radians(angle))
            inner_x = mouse_pos[0] + self.inner_radius * math.cos(math.radians(angle))
            inner_y = mouse_pos[1] + self.inner_radius * math.sin(math.radians(angle))
            pygame.draw.line(
                screen,
                WHITE,
                (outer_x, outer_y),
                (inner_x, inner_y),
            )

        return self.circle_rect

    def check_skill_pos(self, mouse_pos: tuple[int, int]):
        """
        :return `int` status code
        - 0: inside inner circle or outside big circle which means don't choose any skill
        - [1,2,3,4]: confirm a specified skill to cast
        """
        # 先判断距离
        if self.inner_radius <= math.dist(mouse_pos, self.circle_pos) <= self.radius:
            res = classify_angle_with_radians(self.circle_pos, mouse_pos)
            self.current_skill_operation_id = res
            return res
        return 0

    def confirm_select_item(self, item_id):
        self.current_item_id = item_id
        self.skill_or_item = 1

    def get_item_id(self):
        return self.current_item_id

    def get_skill_operation_id(self):
        return self.current_skill_operation_id

    def confirm_select_skill(self, operation_id: int = -1):
        """如果鼠标松开并在相应的radius区间内"""
        if operation_id != -1:
            self.current_skill_operation_id = operation_id
        self.select_skill_status = False
        self.skill_or_item = 0

    def reset_area(self, screen: pygame.Surface):
        """清空选择所用到的圆圈"""
        # 清空区域并reset相关控制设置
        screen.blit(self.circle_mask_surface, self.circle_rect)
        self.select_skill_status = False
        return self.circle_rect

    def cancel_latest_select(self, stage: EnumBattleStage):
        if self.select_idx <= 0:
            return 1
        if (
            stage == EnumBattleStage.SELECT_SKILL
            and self.is_select_skill() is not True
            and self.current_selected_queue_idx() != 0
        ):
            self.select_idx -= 1
            return 2
        elif stage == EnumBattleStage.SELECT_TARGET | EnumBattleStage.SCROLL_ITEM:
            return 0
        return 1
