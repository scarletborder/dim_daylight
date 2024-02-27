import pygame


"""
battle test alpha
战斗测试 alpha
模拟以下步骤：
1. 模拟从本地读取战斗所需要的数据，有人物，技能
2. 战斗的gui
"""

import pygame

# 一次简单的战斗测试
# 不从服务端读取对应info_row而是用本地的数据模拟

"""
一些外部设置
"""
base_resolution = (1024, 768)  # 假设的游戏设计基准分辨率
user_resolution = (1024, 768)  # 用户选择的分辨率

scale_x = user_resolution[0] / base_resolution[0]
scale_y = user_resolution[1] / base_resolution[1]

fps = 60


"""正片"""
pygame.init()

window = pygame.display.set_mode(user_resolution)
pygame.display.set_caption("东方永昼日 battle test alpha")  # 设置窗口标题
fclock = pygame.time.Clock()

running = True
pygame.event.set_blocked(None)
pygame.event.set_allowed(pygame.QUIT)
pygame.event.set_allowed(pygame.KEYDOWN)
pygame.event.set_allowed(pygame.KEYUP)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            print("=", event.dict.get("unicode", ""))

        # 清屏
    window.fill((0, 0, 0))

    # 根据缩放比例绘制游戏元素
    # 例如：绘制一个矩形
    base_rect = pygame.Rect(100, 100, 200, 100)  # 基准分辨率下的矩形
    scaled_rect = base_rect.inflate(
        base_rect.width * (scale_x - 1), base_rect.height * (scale_y - 1)
    )
    pygame.draw.rect(window, (255, 0, 0), scaled_rect)

    # 更新屏幕
    pygame.display.flip()
    fclock.tick(fps)

pygame.quit()
