"""
battle test alpha
战斗测试 alpha
模拟以下步骤：
1. 模拟从本地读取战斗所需要的数据，有人物，技能
2. 战斗的gui
"""

from src.utils.battle.load_battle import LoadBattle

from src.view.scene_manager import SceneManager
from src.view.scene.battle_scene import BattleScene
from src.model.battle.battle_role import BattleRole
from src.model.battle.battle import Battle
from src.model.battle.skill import Skill


from src.constant.battle.enum_party import EnumParty

from src.storage.main_db import Main_DB
import pygame
import sys


# 一次简单的战斗测试
# 不从服务端读取对应info_row而是用本地的数据模拟

"""
一些外部设置
"""
user_resolution = (1366, 768)  # 用户选择的分辨率

# scale_x = user_resolution[0] / base_resolution[0]
# scale_y = user_resolution[1] / base_resolution[1]

fps = 60


"""正片"""
pygame.init()

window = pygame.display.set_mode(user_resolution)  # screen
pygame.display.set_caption("东方永昼日 battle test alpha")  # 设置窗口标题
fclock = pygame.time.Clock()

scene_manager = SceneManager()

"""加载测试关卡"""
gang_id = 1
my_battle = LoadBattle.load_battle_ai(gang_id, 0)
"""加载结束"""
scene_manager.switch_to_scene(
    BattleScene(window, my_battle, user_resolution, Main_DB, fps)
)


running = True
while running:
    ret = scene_manager.process_input(pygame.event.get(), pygame.key.get_pressed())
    if ret != 0:
        break
    scene_manager.update()
    scene_manager.render(screen=window, fps=fps)
    pygame.display.update(scene_manager.get_update_rects())

    fclock.tick(fps)

print("战斗正常结束")
