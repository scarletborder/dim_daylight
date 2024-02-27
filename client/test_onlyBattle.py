"""
battle test alpha
战斗测试 alpha
模拟以下步骤：
1. 模拟从本地读取战斗所需要的数据，有人物，技能
2. 战斗的gui
"""

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
# base_resolution = (1024, 768)  # 假设的游戏设计基准分辨率
user_resolution = (1024, 768)  # 用户选择的分辨率

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
skill_id_list = []

"""测试关卡模拟加载遇怪"""
"""
player2 -> hero 右下方
player1 -> mob gang 左上方
"""

gang_id = 1
test_mob_gang1_dict = Main_DB.read_all_values("mob_gang_table", gang_id, {})
if test_mob_gang1_dict is None:
    sys.exit()

test_mob_gang1_id_list = test_mob_gang1_dict.get("mob_id_list", [])
test_mob_gang1_quid_list = test_mob_gang1_dict.get("quid_list", [])

mob_info_list = []
handle_basic_content_func = test_mob_gang1_dict.get("handle_basic_content_func")
for idx in range(len(test_mob_gang1_id_list)):
    role_id = test_mob_gang1_id_list[idx]
    role_info = Main_DB.read_all_values("role_table", role_id, {})
    handle_basic_content_func(role_id, role_info)

    for t_skill_id_list in role_info.get("operation_dict").values():
        skill_id_list += t_skill_id_list

    mob_info_list.append(
        BattleRole(
            role_id,
            role_info.get("name"),
            role_info.get("description"),
            role_info.get("weakness"),
            EnumParty.ENUM_PLAYER2,
            role_info.get("operation_dict"),
            role_info.get("value_content"),
        )
    )

"""模拟加载英雄
这里现在只测试一个英雄
"""

hero_role_id = 0
hero_role_info = Main_DB.read_all_values("role_table", hero_role_id, {})
hero_info_list = [
    BattleRole(
        hero_role_id,
        hero_role_info.get("name"),
        hero_role_info.get("description"),
        [0, 0, 0, 0],
        EnumParty.ENUM_PLAYER1,
        hero_role_info.get("operation_dict"),
        hero_role_info.get("value_content"),
    )
]

for t_skill_id_list in hero_role_info.get("operation_dict").values():
    skill_id_list += t_skill_id_list

"""加载技能"""
skill_id_dict = {}
for skill_id in skill_id_list:
    res = Main_DB.read_all_values("skill_table", skill_id, {})
    skill_id_dict[skill_id] = Skill(
        res.get("name"),
        res.get("description"),
        res.get("cast_func"),
        res.get("display_func"),
        res.get("range_method"),
    )

"""加载战斗模块"""
my_battle = Battle(
    player1_info_list=mob_info_list,
    player1_position=test_mob_gang1_quid_list,
    player2_info_list=hero_info_list,
    player2_position=[7],  # 右下的前排正中
    skill_dict=skill_id_dict,
)


"""加载结束"""
scene_manager.switch_to_scene(
    BattleScene(window, my_battle, user_resolution, Main_DB, fps)
)
# 删除无用加载项
del skill_id_list
del test_mob_gang1_dict
del test_mob_gang1_id_list
del hero_role_info
# del test_mob_gang1_quid_list
# del hero_info_list
# del mob_info_list


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
