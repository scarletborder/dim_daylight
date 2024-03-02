import pygame
from src.storage.myLite_data_base import MyLiteDataBase

"""用于返回所有诸如状态条，buff磁贴的修改后图片"""


class BulkIcon:

    def __init__(self, db: MyLiteDataBase) -> None:
        # 在这里读取图片
        ## buff
        self.sheet = pygame.image.load("resource/buff_icons.png")
        self.buff_icon_id_dict = {}
        for buff_id in range(12):  # 目前游戏中拥有的buff数量
            icon_id = db.read_data("buff_table", buff_id, "icon_id")
            if icon_id is None:
                break
            self.buff_icon_id_dict[buff_id] = icon_id

        ...

    # 暗红：#A32527
    # 浅绿：#92B44E
    # 浅黄：#AF820F
    # 浅蓝：#7AC1D9

    def get_buff_icon(
        self,
        buff_id: int,
        duration: int,
        db: MyLiteDataBase,
    ):
        icon_per_line = 10
        radius = 10
        buff_icon_id = self.buff_icon_id_dict[buff_id]
        x = buff_icon_id / icon_per_line
        y = buff_icon_id % icon_per_line
        # 计算图标在大图中的位置
        rect = pygame.Rect(x * radius, y * radius, radius, radius)
        # 使用subsurface方法提取图标
        return self.sheet.subsurface(rect)
