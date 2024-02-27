import pygame
import math

pygame.init()

# 设置屏幕大小
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Draw Circle with Inner Circle and Lines")

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 设置游戏运行的标志
running = True

# 设置大圆的半径
radius = 50
flag = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 获取鼠标位置
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # 创建圆的矩形区域
    circle_rect = pygame.Rect(
        mouse_x - radius, mouse_y - radius, 2 * radius, 2 * radius
    )
    if flag is False:
        flag = True
        old_subsurface = screen.subsurface(circle_rect).copy()
        old_rect = circle_rect

    screen.blit(old_subsurface, old_rect)
    old_rect = circle_rect
    old_subsurface = screen.subsurface(circle_rect).copy()

    # 清除屏幕
    screen.fill(BLACK)

    # 绘制大圆
    pygame.draw.circle(screen, WHITE, (mouse_x, mouse_y), radius, 1)

    # 计算并绘制小圆
    inner_radius = radius // 2
    pygame.draw.circle(screen, WHITE, (mouse_x, mouse_y), inner_radius, 1)

    # 计算并绘制线条
    angles = [45, 135, 225, 315]
    for angle in angles:
        outer_x = mouse_x + radius * math.cos(math.radians(angle))
        outer_y = mouse_y + radius * math.sin(math.radians(angle))
        inner_x = mouse_x + inner_radius * math.cos(math.radians(angle))
        inner_y = mouse_y + inner_radius * math.sin(math.radians(angle))
        pygame.draw.line(screen, WHITE, (outer_x, outer_y), (inner_x, inner_y))

    # 更新屏幕
    pygame.display.update()

pygame.quit()
