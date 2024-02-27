import pygame

# 初始化pygame
pygame.init()

# 设置屏幕大小
screen = pygame.display.set_mode((800, 600))

# 设置颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# 创建精灵类
class MovingSprite(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.old_bg_image = pygame.Surface((width, height))
        pygame.draw.rect(self.image, (0, 100, 0), (0, 0, 10, 10))  # 相对精灵画装饰
        self.rect = self.image.get_rect()

    def update(self, x_shift, y_shift):
        """计算更新位置并返回更新区域的矩形"""
        self.old_rect = self.rect.copy()
        screen.blit(self.old_bg_image, self.old_rect)

        # 更新位置
        self.rect.x += x_shift
        self.rect.y += y_shift

        self.old_bg_image = screen.subsurface(self.rect).copy()

        # 返回需要更新的区域
        return self.old_rect.union(self.rect)


# 创建两个精灵实例
sprite1 = MovingSprite(WHITE, 50, 50)
sprite1.old_bg_image = screen.subsurface((100, 100, 50, 50)).copy()

sprite1.rect.x = 100
sprite1.rect.y = 100

sprite2 = MovingSprite(WHITE, 50, 50)
sprite2.old_bg_image = screen.subsurface((200, 200, 50, 50)).copy()
sprite2.rect.x = 200
sprite2.rect.y = 200

# 游戏主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 移动精灵并获取更新区域
    update_rects = []
    update_rects.append(sprite1.update(1, 0))  # 向右移动sprite1
    update_rects.append(sprite2.update(0, 1))  # 向下移动sprite2

    # 重绘屏幕背景（如果需要）
    # screen.fill(BLACK)  # 如果不需要保留背景，则不必执行此步

    # 重绘移动的精灵
    sprites = [sprite1, sprite2]
    for sprite in sprites:
        # screen.blit(sprite.replace_image, sprite.old_rect)
        screen.blit(sprite.image, sprite.rect)

    # 只更新有变化的屏幕区域
    pygame.display.update(update_rects)

    # 控制游戏帧率
    pygame.time.Clock().tick(60)

pygame.quit()
