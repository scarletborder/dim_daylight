# """用于根据相对速度，分辨率，帧率，当前点，目标点来计算一帧后新的点位置"""

# """用于根据逻辑坐标来计算场上的物品的绝对坐标位置"""

# """两个quid的逻辑距离"""

import pygame
import math

# 初始化pygame
pygame.init()

resolution = (1366, 768)

# 网格位置
## 状态条矩形状态
my_bar_width = round(0.0437 * resolution[0])
my_bar_height = round(0.0183 * resolution[1])
### 同一行
bar_delta_width = round(0.0667 * resolution[0])
bar_delta_height = round(0.0945 * resolution[1])
### 相邻列
bar_near_width = round(0.1121 * resolution[0])
bar_near_height = round(0.0976 * resolution[1])
### 一些特殊的起始点
bar_quid0_pos = (round(0.3155 * resolution[0]), round(0.2520 * resolution[1]))
bar_quid10_pos = (round(0.6164 * resolution[0]), round(0.8506 * resolution[1]))

# 设置屏幕大小
screen = pygame.display.set_mode(resolution)

# 设置标题
pygame.display.set_caption("移动物体示例")

# 设置颜色
black = (0, 0, 0)
white = (255, 255, 255)

# 设置帧率
clock = pygame.time.Clock()
fps = 60

# 初始化物体位置和速度
start_pos = (100, 300)
end_pos = (700, 300)
velocity = 100  # 每秒100像素

# 计算移动方向
dx = end_pos[0] - start_pos[0]
dy = end_pos[1] - start_pos[1]
distance = math.sqrt(dx**2 + dy**2)
direction = (dx / distance, dy / distance)

# 计算每帧移动距离
per_frame_distance = velocity / fps

# 当前物体位置
current_pos = list(start_pos)

# 游戏主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 移动物体
    current_pos[0] += direction[0] * per_frame_distance
    current_pos[1] += direction[1] * per_frame_distance

    # 检查是否到达终点
    if (
        math.sqrt(
            (current_pos[0] - start_pos[0]) ** 2 + (current_pos[1] - start_pos[1]) ** 2
        )
        >= distance
    ):
        current_pos = end_pos  # 到达终点，停止移动

    # 绘制背景和物体
    screen.fill(black)
    pygame.draw.circle(screen, white, (int(current_pos[0]), int(current_pos[1])), 10)

    # 更新屏幕
    pygame.display.flip()

    # 控制游戏帧率
    clock.tick(fps)

# 退出pygame
pygame.quit()
