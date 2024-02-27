import pygame
import math
import time

# 初始化pygame
pygame.init()
pygame.display.set_caption("东方永昼日:grid and picture test")  # 设置窗口标题

resolution = (1366, 768)
# resolution = (1920, 1080)

# 网格位置
pixel_figure_scale = resolution[1] / 10
## 状态条矩形状态
my_bar_width = round(0.05 * resolution[0])
my_bar_height = round(0.008 * resolution[1])
### 同一行
bar_delta_width = round(0.08 * resolution[0])
bar_delta_height = round(0.095 * resolution[1])
### 相邻列
bar_near_width = round(0.15 * resolution[0])
bar_near_height = round(0.12 * resolution[1])
### 一些特殊的起始点
# bar_quid0_pos = (round(0.3155 * resolution[0]), round(0.2520 * resolution[1]))
# bar_quid10_pos = (round(0.6164 * resolution[0]), round(0.4726 * resolution[1]))
bar_quid0_pos = (round(0.38 * resolution[0]), round(0.20 * resolution[1]))
bar_quid10_pos = (round(0.6164 * resolution[0]), round(0.46 * resolution[1]))

bar_parallel = (
    bar_quid10_pos[0] - bar_quid0_pos[0],
    bar_quid10_pos[1] - bar_quid0_pos[1],
)

screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()
fps = 60


def wrap_text(text, font, rect_width):
    """
    Wrap text to fit within a given width when rendered with a specific font,
    considering explicit line breaks.
    """
    wrapped_lines = []
    for paragraph in text.split("\n"):  # Split the text into paragraphs
        words = paragraph.split(" ")
        current_line = []
        for word in words:
            test_line = " ".join(current_line + [word])
            test_rect = font.render(test_line, True, (0, 0, 0)).get_rect()
            if test_rect.width <= rect_width:
                current_line.append(word)
            else:
                wrapped_lines.append(" ".join(current_line))
                current_line = [word]
        wrapped_lines.append(
            " ".join(current_line)
        )  # Add the last line of the paragraph
    return wrapped_lines


def render_text_within_rect(
    screen, text, rect, font_name="SimSun", initial_font_size=24, color=(0, 0, 0)
):
    """
    Render text within a given pygame.Rect, adjusting font size or breaking lines as necessary,
    with explicit line breaks and left alignment.
    """
    font_size = initial_font_size
    font = pygame.font.SysFont(font_name, font_size)
    lines = wrap_text(text, font, rect.width)

    # Adjust font size if the text height is too high
    total_height = len(lines) * font.get_height()
    while total_height > rect.height and font_size > 0:
        font_size -= 1
        font = pygame.font.SysFont(font_name, font_size)
        lines = wrap_text(text, font, rect.width)
        total_height = len(lines) * font.get_height()

    if font_size == 0:
        raise ValueError(
            "Text cannot be accommodated within the given rect (too small)."
        )

    y = rect.top
    for line in lines:
        line_surf = font.render(line, True, color)
        line_rect = line_surf.get_rect()
        line_rect.top = y
        line_rect.left = rect.left  # Align text to the left
        screen.blit(line_surf, line_rect)
        y += font.get_height()  # Move down to render the next line


# 鼠标相关存储data
has_left_down = False
left_down_time = time.time()  # 左键按下的时刻

# 游戏主循环
running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                match event.button:
                    case 1:
                        left_down_time = time.time()
                        has_left_down = True
                ...
            case pygame.MOUSEBUTTONUP:
                match event.button:
                    case 1:
                        has_left_down = False

            case pygame.QUIT:
                running = False

    if has_left_down is True and time.time() - left_down_time > 0.3:
        # 长按
        pygame.draw.circle(screen, (64, 64, 78), event.pos, 40, 2)

    image = pygame.image.load("image.png").convert_alpha()
    rect = image.get_rect()
    image = pygame.transform.scale(image, (pixel_figure_scale, pixel_figure_scale))
    flipped_image = pygame.transform.flip(image, True, False)

    ## bottom left side-bar
    frame_rect = pygame.Rect(
        0, 0.75 * resolution[1], 0.2 * resolution[0], 0.25 * resolution[1]
    )
    pygame.draw.rect(screen, pygame.Color(112, 128, 144, 100), frame_rect)

    ## right side-bar
    pygame.draw.line(
        screen,
        (255, 255, 255),
        (0.75 * resolution[0], 0),
        (0.75 * resolution[0], resolution[1]),
    )

    pygame.draw.line(
        screen,
        (255, 255, 255),
        (0.75 * resolution[0], 0.8 * resolution[1]),
        (resolution[0], 0.8 * resolution[1]),
    )

    # reminder info text
    font_size = round(0.05 * resolution[1])
    font = pygame.font.SysFont("SimSun", font_size)

    my_rect = pygame.Rect(
        0, 0.955 * resolution[1], 0.2 * resolution[0], 1 * resolution[1]
    )
    render_text_within_rect(
        screen,
        "hello world",
        my_rect,
        initial_font_size=int(0.028 * resolution[1]),
        color=(244, 244, 244),
    )

    # main-content
    rect = image.get_rect()
    for idx in range(5):
        top_left = bar_quid0_pos[0] - (my_bar_width >> 1) - idx * bar_delta_width
        top_right = bar_quid0_pos[1] - my_bar_height + idx * bar_delta_height

        pygame.draw.rect(
            screen, (255, 255, 255), (top_left, top_right, my_bar_width, my_bar_height)
        )
        rect.x = top_left
        rect.bottom = top_right
        screen.blit(flipped_image, rect)

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (
                top_left + bar_parallel[0],
                top_right + bar_parallel[1],
                my_bar_width,
                my_bar_height,
            ),
        )
        rect.x = top_left + bar_parallel[0]
        rect.bottom = top_right + bar_parallel[1]
        screen.blit(image, rect)

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (
                top_left + bar_near_height,
                top_right + bar_near_height,
                my_bar_width,
                my_bar_height,
            ),
        )
        rect.x = top_left + bar_near_height
        rect.bottom = top_right + bar_near_height
        screen.blit(flipped_image, rect)

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (
                top_left + bar_near_height + bar_parallel[0],
                top_right + bar_near_height + bar_parallel[1],
                my_bar_width,
                my_bar_height,
            ),
        )
        rect.x = top_left + bar_near_height + bar_parallel[0]
        rect.bottom = top_right + bar_near_height + bar_parallel[1]
        screen.blit(image, rect)

    # 更新屏幕
    pygame.display.flip()

    # 控制游戏帧率
    clock.tick(fps)
