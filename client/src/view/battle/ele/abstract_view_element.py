from abc import ABC, abstractmethod


class AbstractViewElement(ABC):

    @abstractmethod
    def load_image(self):
        """由viewer主控传入image并使得element保存"""
        ...

    # @abstractmethod
    # def register_to_viewer(self, battle_viewer: BattleViewer):
    #     """将这个显示部件的信息加载到battle viewer中
    #     每个元素的显示图片在从路径到内存中的显示部件对象经历以下加载步骤
    #     1. load
    #     2. resize: 使用 pygame.transform.scale,根据具体元素类型具体决定对这个类型的新显示部件的各个组成部分
    #                 进行resize到适合该分辨率
    #     3. init data: 初始化这个显示部件在显示时所需要的数据
    #     """
    #     ...

    @abstractmethod
    def update(self):
        """返回list[Rect]"""
        ...

    @abstractmethod
    def render(self, screen):
        """进行展示
        如果是移动的物体在这一步中需要画原先的位置和最新的位置
        坐标需要在加载和update步骤中已经存在
        """
        ...
