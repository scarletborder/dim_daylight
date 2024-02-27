from src.view.scene.abstract_scene import AbstractScene
from src.model.battle.battle import Battle
from src.model.battle.cache_cast import CacheCast

from src.view.battle.ele.battle_role import ViewBattleRole
from src.view.battle.ele.reminder import ViewBattleReminder
from src.view.battle.ele.info_bar import ViewBattleInfoBar
from src.view.battle.ele.log_bar import ViewBattleLogBar
from src.view.battle.ele.buttons import ViewButtons

from src.view.battle.mov_time import MovTime
from src.view.battle.select_skill import SelectSkill

from src.constant.battle.enum_battle_stage import EnumBattleStage
from src.constant.battle.enum_role_value import EnumRoleValue
from src.constant.battle.enum_event import EnumBattleEvent
from src.constant.battle.enum_skill_method import MELEE, PROJECTILE

import sys
import pygame

LONG_PRESS_TIME = 200
WHITE = (255, 255, 255)


class BattleScene(AbstractScene):
    def __init__(
        self,
        screen: pygame.Surface,
        battle: Battle,
        resolution: tuple[int, int],
        db,
        fps: int,
    ):
        super().__init__()
        self.battle = battle
        self.screen = screen
        self.fps = fps
        self.battle_status_code = 0

        # 初始化角色视图
        self.ele_battle_roles: list[ViewBattleRole] = []
        for quid, t_battle_role in battle.layout.items():
            self.ele_battle_roles.append(
                ViewBattleRole(quid, t_battle_role.role_id, resolution, db, screen)
            )

        for ele_view_role in self.ele_battle_roles:
            ele_view_role.load_image()

        # 初始化reminder
        self.ele_reminder = ViewBattleReminder(resolution)

        # 初始化info
        self.ele_info_bar = ViewBattleInfoBar(resolution)

        # 初始化log
        self.ele_log_bar = ViewBattleLogBar(resolution)

        # 初始化按钮组 - 大招和item
        self.ele_buttons = ViewButtons(resolution)

        # 注册按键
        self.mouse_right_start_time = None
        self.mouse_left_start_time = None

        # 显示细节
        self.view_context = dict()
        self.update_rects: list[pygame.Rect] = []

        # 控制细节
        self.c_cast = CacheCast()
        self.mov_time = MovTime()
        self.select_skill_tool = SelectSkill()
        ## context
        self.mouse_target = None
        self.ctrl_context = dict()

        # io密集load image
        for ele in self.ele_battle_roles:
            ele.load_image()

        # 结束
        ## 触发一次Battle_Start效果
        self.battle.battle_start()
        self.on_new_select_turn()

    """
    state
    """

    def on_new_select_turn(self):
        """在一次回合的结束后进入新回合的选择技能阶段"""
        self.stage = EnumBattleStage.SELECT_SKILL
        # 进行状态显示
        # 判断游戏结束的函数移动到每次health数值发生变化时
        caster_queue = self.battle.get_speed_queue()
        new_queue = []
        # 找到自己队伍的排序
        for quid in caster_queue:
            if quid >= 10 and self.battle.layout[quid].is_alive():
                new_queue.append(quid)
        # 加载自己的队伍
        self.select_skill_tool.load_new_queue(new_queue)
        self.battle.on_ready_turn_start()  # 技能

    def switch_to_select_skill(self, caster_quid: int):
        """切换到选择技能的回合"""
        self.stage = EnumBattleStage.SELECT_SKILL
        # self.view_detail[""]

    def switch_to_select_target(self):
        self.stage = EnumBattleStage.SELECT_TARGET

    def next_select_skill(self):
        # 这个select skill + select target结束，切换到下一个人物
        if (caster_quid := self.select_skill_tool.start_next_select()) != -1:
            self.switch_to_select_skill(caster_quid)
        else:
            # 否则进入默认施法阶段
            self.switch_to_general_cast()

    def switch_to_scroll_item(self):
        """选择物品"""
        self.stage = EnumBattleStage.SCROLL_ITEM
        # 告知info bar展示物品列表

    def switch_to_ready_defense(self, mov_time):
        # 组装长度
        # 提示reminder进行防御
        self.update_rects += self.ele_reminder.update(
            self.screen,
            f"在敌人运动时点击{self.c_cast.target_quid}角色进行防卫",
            "Left Click",
        )
        self.stage = EnumBattleStage.READY_DEFENSE
        self.ready_to_move(mov_time)

    def ready_to_move(self, mov_time: float):
        """mov_time : float seconds"""
        start_ticks = pygame.time.get_ticks() + 500
        mov_time = round(mov_time * 1000)
        self.mov_time.set(start_ticks, start_ticks + mov_time)  # 理应的防卫终止时间

    def reset_defense(self): ...

    def judge_defense_successful(self, mouse_target):
        if mouse_target == self.c_cast.target_quid:
            return self.mov_time.is_in_scope(pygame.time.get_ticks())

    def switch_to_general_cast(self):
        # 默认施法阶段
        self.battle.global_turn_start()

    def end_global_cast(self):
        """所有角色施法结束"""
        self.on_new_select_turn()
        ...

    """
    cast associated
    """

    def new_cast_display(self):

        ret_tuple = self.battle.get_role_cast()
        if ret_tuple is None:
            self.end_global_cast()
            return

        caster_quid, target_quid, castable_id, operation_type, mov_time = ret_tuple
        self.battle.turn_start(caster_quid)  # 此角色回合开始
        ## 判断游戏是否结束

        if (t := self.battle.judge_battle_end()) != 0:
            print(f"玩家{t}获得胜利")
            self.end_scene(t)
            return
        self.end_scene(t)
        # 对视觉图进行更新
        self.update()
        self.c_cast.reset(caster_quid, target_quid, operation_type, castable_id)

        self.stage = EnumBattleStage.GENERAL_CAST
        # 近战/远程
        if operation_type == EnumBattleEvent.ENUM_ON_ITEM:
            method = self.battle.item_dict[castable_id].range_method
        else:
            method = self.battle.skill_dict[castable_id].range_method

        # 如果目标是我方的角色并且是近战技能
        if caster_quid > 10 and method == MELEE:
            self.switch_to_ready_defense(mov_time)
        elif method == MELEE:
            # 如果目标是敌方的角色并且是近战技能
            self.ready_to_move(mov_time)

        else:
            # 如果是远程技能
            self.update_rects += self.ele_reminder.update(
                self.screen, f"{target_quid}受到远程攻击"
            )
            self.battle.cast(*self.c_cast.get())

        ## 判断游戏是否结束
        if (t := self.battle.judge_battle_end()) != 0:
            print(f"玩家{t}获得胜利")
            self.end_scene(t)
            return
        self.end_scene(t)
        self.battle.turn_end(caster_quid)  # 此角色回合结束
        ## 判断游戏是否结束
        if (t := self.battle.judge_battle_end()) != 0:
            print(f"玩家{t}获得胜利")
            self.end_scene(t)
            return
        self.end_scene(t)

        self.battle.global_turn_end()

    """
    input
    """

    def process_input(
        self, events: list[pygame.event.Event], pressed_keys: pygame.key.ScancodeWrapper
    ):
        mouse_pos = pygame.mouse.get_pos()
        mouse_target = None
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                # 鼠标悬浮选人
                # 处理鼠标移动
                for idx in range(len(self.ele_battle_roles)):
                    if (
                        self.ele_battle_roles[idx].role_rect.collidepoint(mouse_pos)
                        is False
                    ):
                        continue

                    ### 在当前人物框中，告诉info_bar
                    mouse_target = self.ele_battle_roles[idx].quid
                    break

                ## 通用的信息，用来调用涉及到关于鼠标指向的quid
                ### 只有在移动时，此值会变为None或者一个quid。
                ### 例如
                ### 信息栏查询人物，如果鼠标不在人物方框上,告诉info_bar不显示或是select_skill阶段显示caster
                ### select_target左键时的选择
                self.mouse_target = mouse_target
                if mouse_target is not None:
                    self.ele_info_bar.reload_info(
                        self.battle.layout[mouse_target].value_dict,
                        self.battle.get_role_skills(mouse_target),
                    )

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 处理鼠标按下事件
                if event.button == 1:  # 左键
                    self.mouse_left_start_time = pygame.time.get_ticks()  # 记录按下时刻
                    if self.stage == EnumBattleStage.READY_DEFENSE:
                        # 按下瞬间判断防御
                        self.battle.cast(
                            *self.c_cast.get(),
                            is_qdef=self.judge_defense_successful(mouse_target),
                        )
                        self.reset_defense()
                elif event.button == 3:  # 右键
                    self.mouse_right_start_time = pygame.time.get_ticks()

            elif event.type == pygame.MOUSEBUTTONUP:
                # 处理鼠标释放事件
                if event.button == 1:  # 左键
                    press_duration = pygame.time.get_ticks() - (
                        self.mouse_left_start_time or 0
                    )
                    self.mouse_left_start_time = None

                    # 判断长按或短按
                    if press_duration >= LONG_PRESS_TIME:
                        # print("Long press detected.")
                        ...
                    else:
                        if self.stage == EnumBattleStage.SELECT_SKILL:
                            # 判断是否移动到item/final按钮上
                            if self.ele_buttons.item_rect.collidepoint(mouse_pos):
                                self.switch_to_scroll_item()
                                break

                            if self.ele_buttons.final_spell_rect.collidepoint(
                                mouse_pos
                            ):
                                # 选择释放大招
                                self.select_skill_tool.confirm_select_skill(5)
                                self.switch_to_select_target()
                                break
                        elif (
                            self.stage == EnumBattleStage.SELECT_TARGET
                            and self.mouse_target is not None
                            # and self.view_detail["mouse_target"]
                            # != self.ctrl_detail["select_caster_quid"]
                        ):
                            if self.select_skill_tool.skill_or_item == 0:
                                self.battle.ready_skill_by_operation(
                                    self.select_skill_tool.current_selected_caster_quid(),
                                    self.mouse_target,
                                    self.select_skill_tool.get_skill_operation_id(),
                                )
                            else:
                                self.battle.ready_item_by_itemId(
                                    self.select_skill_tool.current_selected_caster_quid(),
                                    self.mouse_target,
                                    self.select_skill_tool.get_item_id(),
                                )
                            self.next_select_skill()
                            break
                        elif (
                            self.stage == EnumBattleStage.SCROLL_ITEM
                            and self.ele_info_bar.frame_rect.collidepoint(mouse_pos)
                        ):
                            t_item_pack_id = self.ele_info_bar.choose(mouse_pos)
                            if t_item_pack_id is not None:
                                self.select_skill_tool.confirm_select_item(
                                    t_item_pack_id
                                )
                                self.switch_to_select_target()
                            break
                elif event.button == 3:  # 右键
                    press_duration = pygame.time.get_ticks() - (
                        self.mouse_right_start_time or 0
                    )
                    self.mouse_right_start_time = None

                    # 判断长按或短按
                    if press_duration >= LONG_PRESS_TIME:
                        ...
                        # print("Long press detected.")
                    else:
                        # 撤销到上一步
                        if (
                            status_code := self.select_skill_tool.cancel_latest_select(
                                self.stage
                            )
                        ) == 0:
                            self.switch_to_select_skill(
                                self.select_skill_tool.current_selected_caster_quid()
                            )
                        elif status_code == 2:
                            self.battle.cancel_by_caster_quid(
                                self.select_skill_tool.caster_quid_list[
                                    self.select_skill_tool.select_idx + 1
                                ]
                            )
                            self.switch_to_select_skill(
                                self.select_skill_tool.current_selected_caster_quid()
                            )
                        else:
                            self.update_rects += self.ele_reminder.update(
                                self.screen,
                                "cancel失败，不能位于队列首位或按住时",
                                "",
                            )

                        ...
            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:  # Scroll up
                    t_aspect = True
                elif event.y < 0:
                    t_aspect = False
                if self.ele_info_bar.frame_rect.collidepoint(mouse_pos) is True:
                    self.ele_info_bar.update(t_aspect)
                elif self.ele_log_bar.frame_rect.collidepoint(mouse_pos) is True:
                    self.ele_log_bar.update(t_aspect)

            # 其他判断，如对长按状态的判断
            match self.stage:
                case EnumBattleStage.SELECT_SKILL:
                    ## select skill中，在角色的rect中长按时，监测是否滑倒区间来store一个选项枚举数。如果滑出则取消
                    if (
                        # 不在长按选择中，防止滑倒其他角色上
                        self.select_skill_tool.is_select_skill() is False
                        and self.mouse_left_start_time is not None  # 按住鼠标左键情况下
                        # 选择的是现在即将施法的角色
                        and self.mouse_target
                        == self.select_skill_tool.current_selected_caster_quid()
                    ):
                        ### 左键已经按下并且在方框内，初次达到圈圈
                        if pygame.time.get_ticks() - self.mouse_left_start_time > 350:
                            # 初次达到时间上限，绘制圈圈
                            self.select_skill_tool.get_original_rect(
                                radius=ViewBattleRole.my_bar_width * 0.6,
                                mouse_pos=mouse_pos,
                                screen=self.screen,
                            )
                            break
                    ## 已经绘制了圈圈
                    elif self.select_skill_tool.is_select_skill() is True:
                        ### 判断是否松开
                        if self.mouse_left_start_time is None:
                            # 根据偏移角度位置选择
                            operation_id = self.select_skill_tool.check_skill_pos(
                                mouse_pos
                            )
                            if operation_id == 0:
                                # 没有选择
                                self.select_skill_tool.reset_area(self.screen)
                            else:
                                # 清空区域并reset相关控制设置,进入select_target阶段
                                self.select_skill_tool.confirm_select_skill()
                                self.select_skill_tool.reset_area(self.screen)
                                self.switch_to_select_target()
                            break
                        ...
                case EnumBattleStage.GENERAL_CAST | EnumBattleStage.READY_DEFENSE:
                    if self.mov_time.is_need_start_move(pygame.time.get_ticks()):
                        # 是否需要开始移动
                        self.ele_battle_roles[self.c_cast.caster_quid].start_move(
                            self.c_cast.target_quid,
                            self.mov_time.end_move_time - self.mov_time.start_move_time,
                            self.fps,
                        )
                    elif self.mov_time.is_delayed(pygame.time.get_ticks()):
                        # 防御失败
                        if self.c_cast.has_casted() is False:
                            self.battle.cast(*self.c_cast.get(), is_qdef=False)
                            self.reset_defense()
        return self.battle_status_code

    def update(self):
        """一些无法被直接link而update的放在这"""
        # 角色
        for ele in self.ele_battle_roles:
            if ele.detail["is_move"] is True:
                ele.update(None, None, None)
            else:
                default_health = self.battle.layout[ele.quid].query_default_value(
                    EnumRoleValue.ENUM_HEALTH
                )
                ### health
                health_pair = (
                    (
                        self.battle.layout[ele.quid].query_current_value(
                            EnumRoleValue.ENUM_HEALTH,
                        ),
                        default_health,
                    )
                    if default_health is not None
                    else None
                )
                ### magic
                default_magic = self.battle.layout[ele.quid].query_default_value(
                    EnumRoleValue.ENUM_MAGIC
                )

                magic_pair = (
                    (
                        self.battle.layout[ele.quid].query_current_value(
                            EnumRoleValue.ENUM_MAGIC,
                        ),
                        default_magic,
                    )
                    if default_magic is not None
                    else None
                )

                ### energy
                default_energy = self.battle.layout[ele.quid].query_default_value(
                    EnumRoleValue.ENUM_ENERGY
                )

                energy_pair = (
                    (
                        self.battle.layout[ele.quid].query_current_value(
                            EnumRoleValue.ENUM_MAGIC,
                        ),
                        default_energy,
                    )
                    if default_energy is not None
                    else None
                )
                ## update
                self.update_rects += ele.update(health_pair, magic_pair, energy_pair)

        return super().update()

    def render(self):
        pygame.display.update(self.update_rects)
        self.update_rects.clear()
        return super().render(self.screen, self.fps)

    def get_update_rects(self):
        return self.update_rects

    def end_scene(self, code):
        self.battle_status_code = code
