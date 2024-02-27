import pygame
import math

# 初始化pygame
pygame.init()

# 设置屏幕大小
screen = pygame.display.set_mode((800, 600))

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
