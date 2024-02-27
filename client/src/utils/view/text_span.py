import pygame


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

    line_surfs: list[pygame.Surface] = []
    line_rects: list[pygame.Rect] = []

    for line in lines:
        line_surf = font.render(line, True, color)
        line_rect = line_surf.get_rect()
        line_rect.top = y
        line_rect.left = rect.left  # Align text to the left
        # screen.blit(line_surf, line_rect)
        line_surfs.append(line_surf)
        line_rects.append(line_rect)
        y += font.get_height()  # Move down to render the next line

    return line_surfs, line_rects, y
