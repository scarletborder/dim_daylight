import pygame
import sys
from pygame.locals import QUIT
import time

# 初始化Pygame
pygame.init()

# 设置窗口
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("起点到终点移动")

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 起点和终点线
start_line = 50
end_line = WIDTH - 50

# 物体位置
object_pos = start_line

# 移动时间和速度计算
total_time = 0.1  # 给定的时间，秒
distance = end_line - start_line
speed = distance / total_time  # 每秒移动的像素数

# 设置字体和大小
font = pygame.font.SysFont("SimSun", 36)

# 游戏主循环
start_time = time.time()
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # 计算物体当前位置和已走时间
    current_time = time.time() - start_time
    if current_time < total_time:
        object_pos = start_line + (speed * current_time)
        elapsed_time = round(current_time, 2)  # 显示两位小数的时间
    else:
        object_pos = end_line  # 确保物体停在终点线
        elapsed_time = total_time  # 最终显示给定的总时间

    # 清屏
    screen.fill(BLACK)

    # 画起点线和终点线
    pygame.draw.line(screen, WHITE, (start_line, 0), (start_line, HEIGHT), 2)
    pygame.draw.line(screen, WHITE, (end_line, 0), (end_line, HEIGHT), 2)

    # 画物体
    pygame.draw.circle(screen, RED, (int(object_pos), HEIGHT // 2), 20)

    # 渲染已经走的时间文本
    time_text = font.render(f"Time: {elapsed_time}s", True, WHITE)
    screen.blit(time_text, (10, 10))  # 在窗口的左上角显示时间

    # 更新屏幕
    pygame.display.flip()

    # 控制更新速度
    pygame.time.Clock().tick(60)
