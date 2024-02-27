import pygame
from storage.myLite_data_base import MyLiteDataBase
from src.view.battle.ele.battle_viewer import BattleViewer
from src.view.battle.ele.abstract_view_element import AbstractViewElement
from src.view.battle.ele.bulk_icon import BulkIcon
from model.battle.battle import Battle


class ViewBattleRole(AbstractViewElement):
    """人物(static/dynamic)"""

    is_init = False

    def __init__(
        self,
        quid: int,
        role_id: int,
        resolution: tuple[int, int],
        db: MyLiteDataBase,
        screen: pygame.Surface,
    ) -> None:
        """
        初始化一个人物

        """
        self.quid = quid
        """类变量设置"""
        if ViewBattleRole.is_init is False:
            ViewBattleRole.is_init = True
            # 网格位置
            ViewBattleRole.pixel_figure_scale = resolution[1] / 10
            ## 状态条矩形状态
            ViewBattleRole.my_bar_width = round(0.05 * resolution[0])
            ViewBattleRole.my_bar_height = round(0.008 * resolution[1])  # 一小条(1/3)
            ### 同一行
            ViewBattleRole.bar_delta_width = round(0.08 * resolution[0])
            ViewBattleRole.bar_delta_height = round(0.095 * resolution[1])
            ### 相邻列
            ViewBattleRole.bar_near_width = round(0.15 * resolution[0])
            ViewBattleRole.bar_near_height = round(0.12 * resolution[1])
            ### 一些特殊的起始点(pos的下中点)
            # bar_quid0_pos = (round(0.3155 * resolution[0]), round(0.2520 * resolution[1]))
            # bar_quid10_pos = (round(0.6164 * resolution[0]), round(0.4726 * resolution[1]))
            ViewBattleRole.bar_quid0_pos = (
                round(0.38 * resolution[0]),
                round(0.20 * resolution[1]),
            )
            ViewBattleRole.bar_quid10_pos = (
                round(0.6164 * resolution[0]),
                round(0.46 * resolution[1]),
            )

            ViewBattleRole.bar_parallel = (
                ViewBattleRole.bar_quid10_pos[0] - ViewBattleRole.bar_quid0_pos[0],
                ViewBattleRole.bar_quid10_pos[1] - ViewBattleRole.bar_quid0_pos[1],
            )

            ViewBattleRole.bar_colors = (
                (146, 180, 78),
                (122, 193, 217),
                (175, 130, 15),
            )
        """类变量设置结束"""

        # detail when load image
        # self.detail = db.read_all_values("roleview_table", role_id, {})
        self.update_flag = False
        self.screen = screen
        self.detail = db.read_data("role_table", role_id, "role_view_detail", {})
        if self.detail is None:
            self.detail = {}
        """
        ## find image path by name
        self.load_detail["image_path"] = res.get("image_path")
        ## get image extend scale
        ### indeed, it is the specified size of the image
        self.load_detail["ratio_of_height"] = res.get("ratio_of_height")
        """
        self.detail["target_height"] = self.detail["ratio_of_height"] * resolution[1]
        ## need flipping according to quid
        if quid < 10:
            self.detail["flip"] = True
        else:
            self.detail["flip"] = False

        ## 状态条左上顶点坐标
        self.top_x = (
            ViewBattleRole.bar_quid0_pos[0]
            - (ViewBattleRole.my_bar_width >> 1)
            - (quid % 5) * ViewBattleRole.bar_delta_width
        )
        self.top_y = (
            ViewBattleRole.bar_quid0_pos[1]
            - ViewBattleRole.my_bar_height
            + (quid % 5) * ViewBattleRole.bar_delta_height
        )
        match (quid / 5):
            case 1:
                self.top_x += ViewBattleRole.bar_near_width
                self.top_y += ViewBattleRole.bar_near_height
            case 2:
                self.top_x += ViewBattleRole.bar_parallel[0]
                self.top_y += ViewBattleRole.bar_parallel[1]

            case 3:
                self.top_x += (
                    ViewBattleRole.bar_near_width + ViewBattleRole.bar_parallel[0]
                )
                self.top_y += (
                    ViewBattleRole.bar_near_height + ViewBattleRole.bar_parallel[1]
                )

    def load_image(self):
        """加载人物的部件所需要的图片，包含人物图像"""
        if self.detail is None:
            return

        self.role_image = pygame.image.load(self.detail["image_path"])
        aspect_ratio = self.role_image.get_width() / self.role_image.get_height()
        new_width = int(self.detail["target_height"] * aspect_ratio)
        self.role_image = pygame.transform.scale(
            self.role_image, (new_width, self.detail["target_height"])
        )
        if self.detail["flip"] is True:
            self.role_image = pygame.transform.flip(self.role_image, True, False)

        self.detail.clear()
        self.detail["is_move"] = False

        self.role_image = (
            self.role_image.convert_alpha()
        )  # 有个参数没用到，我感觉需要穿进来main screen
        self.role_rect = self.role_image.get_rect()
        self.role_rect.x = self.top_x
        self.role_rect.bottom = self.top_y
        self.detail["old_bg_image"] = self.screen.subsurface(self.role_rect).copy()

    def start_move(self, target_view_role, oneway_time: float, fps: int):
        if self.detail is None:
            return
        # 首先计算两点之间的曼哈顿距离
        distance_x = target_view_role.top_x - self.top_x
        if distance_x > 0:
            distance_x -= 1.2 * ViewBattleRole.my_bar_width  # 多走了状态条的距离
        else:
            distance_x += 1.2 * ViewBattleRole.my_bar_width

        distance_y = target_view_role.top_y - self.top_y

        self.detail["is_move"] = True
        self.detail["vx"] = distance_x / oneway_time / fps
        self.detail["vy"] = distance_y / oneway_time / fps

        self.detail["move_times"] = oneway_time * fps + 1
        self.detail["current_times"] = 0

    def reverse_move(self):
        """当单程移动结束 该往回移动"""
        if self.detail is None:
            return
        self.detail["vx"] *= -1
        self.detail["vy"] *= -1

    def end_move(self):
        self.detail["is_move"] = False

    def update(
        self,
        # 静态bar
        health: tuple[int, int] | None = None,
        magic: tuple[int, int] | None = None,
        energy: tuple[int, int] | None = None,
    ):
        """计算更新位置并返回更新区域的矩形"""
        self.update_flag = True
        # 不再判断是否为None防止响应慢。
        if self.detail["is_move"] is True:
            # 先将人物的位置遮掩
            old_role_rect = self.role_rect.copy()
            self.screen.blit(self.detail["old_bg_image"], old_role_rect)
            # 更新位置
            self.role_rect.x += self.detail["vx"]
            self.role_rect.y += self.detail["vy"]
            # 更新遮掩区块
            self.detail["old_bg_image"] = self.screen.subsurface(self.role_rect).copy()
            # 计数
            if self.detail["current_times"] >= 0:
                self.detail["current_times"] += 1
                if self.detail["current_times"] == self.detail["move_times"]:
                    self.reverse_move()
                    self.detail["current_times"] = -1
            else:
                self.detail["current_times"] -= 1
                if self.detail["current_times"] < -1 * self.detail["move_times"]:
                    self.end_move()

            return [old_role_rect, self.role_rect]

        else:
            bar_len = 0
            # 首先加载人物的状态(hp,mp,energy)
            filled_widths = []
            if health is not None:
                filled_widths.append(
                    max(int(health[0] * ViewBattleRole.my_bar_width / health[1]), 1)
                )
                bar_len += 1
            if magic is not None:
                filled_widths.append(
                    max(int(magic[0] * ViewBattleRole.my_bar_width / magic[1]), 1)
                )
                bar_len += 1
            if energy is not None:
                filled_widths.append(
                    max(int(energy[0] * ViewBattleRole.my_bar_width / energy[1]), 1)
                )
                bar_len += 1

            self.bar_image = pygame.Surface(
                (
                    ViewBattleRole.my_bar_width,
                    bar_len * ViewBattleRole.my_bar_height,
                )
            )

            for idx in range(bar_len):
                pygame.draw.rect(
                    self.bar_image,
                    ViewBattleRole.bar_colors[idx],
                    (
                        0,
                        idx * ViewBattleRole.my_bar_height,
                        ViewBattleRole.my_bar_width,
                        ViewBattleRole.my_bar_height,
                    ),
                )

            self.bar_rect = self.bar_image.get_rect()
            self.bar_rect.x = self.top_x
            self.bar_rect.y = self.top_y
            return [self.role_rect, self.bar_rect]

    # 获得显示类
    def render(self):
        if self.update_flag is False:
            return
        self.update_flag = False
        self.screen.blit(self.role_image, self.role_rect)
        if self.detail["is_move"] is False:
            self.screen.blit(self.bar_image, self.bar_rect)

    # def register_to_viewer(self, battle_viewer: BattleViewer):
    #     battle_viewer.role_views.append(self)


# 一些人物可能特有的，比如注册小挂件比如刀盾弓
# 转向，比如近战技能要过去然后转向回来再转向


# p = pygame.Surface((rect2.width, rect2.height))    #创建一个Surface实例
#         p.blit(image, (0, 0), rect2)    #从image中拷贝rect2区域图像到p,左上角对齐
#         p=pygame.transform.flip(p,True,False)#  反向
# ————————————————

#                             版权声明：本文为博主原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接和本声明。

# 原文链接：https://blog.csdn.net/geng_zhaoying/article/details/117478136
