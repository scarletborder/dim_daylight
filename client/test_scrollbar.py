import pygame


class ViewScrollBar:
    def __init__(self, screen, resolution):
        self.screen: pygame.Surface = screen
        self.resolution = resolution
        self.width = resolution[0] * 0.2  # 20% of the screen width
        self.height = resolution[1]  # Full height of the screen
        self.x = resolution[0] - self.width  # Positioned at the right side
        self.y = 0
        self.items = []
        self.font = pygame.font.Font(None, 30)  # Default font and size
        self.start_index = 0  # Index of the topmost item in the view
        self.end_index = -1  # 最下方的那个index
        self.item_heights = []  # Store the height of each item
        self.item_tops = []  # Store the top Y coordinate of each item
        self.wrapped_texts = []

    def bind(self, list: list):
        self.items = list
        self.start_index = 0  # Reset the start index when a new list is bound
        self.end_index = 0  # 最下方的那个index
        self.item_heights = []
        self.item_tops = []
        self.wrapped_texts = []

        for i in range(len(self.items)):
            wrapped_text = self.wrap_text(self.items[i], self.width)
            # 一个多行文本的高度
            item_height = sum([self.font.get_height() for _ in wrapped_text])
            # print(item_height)

            self.item_heights.append(item_height)
            self.wrapped_texts.append(wrapped_text)

        total_height = 0
        while total_height + self.item_heights[self.end_index] < self.height:
            total_height += self.item_heights[self.end_index]
            self.end_index += 1

    def update(self, screen, method):
        if method == "up" and self.start_index > 0:
            self.start_index -= 1
            print(
                "-" * 10,
                "start_index",
                self.start_index,
                "self.height",
                self.height,
                sep="\n",
            )
        elif method == "down" and self.end_index + 1 < len(self.items):
            self.start_index += 1
            self.end_index += 1
            next_total_height = sum(
                self.item_heights[self.start_index : self.end_index + 1]
            )
            while next_total_height > self.height:
                next_total_height -= self.item_heights[self.start_index]
                self.start_index += 1
            print(
                "-" * 10,
                "start_index",
                self.start_index,
                "total_height",
                next_total_height,
                "分辨率高度",
                self.height,
                sep="\n",
            )
        self.render()

    def wrap_text(self, text, max_width):
        lines = []
        for paragraph in text.split("\n"):  # Handle explicit line breaks
            words = paragraph.split(" ")
            line = words[0]
            for word in words[1:]:
                if self.font.size(line + " " + word)[0] <= max_width:
                    line += " " + word
                else:
                    lines.append(line)
                    line = word
            lines.append(line)
        return lines

    def render(self):
        pygame.draw.rect(
            self.screen, (200, 200, 200), (self.x, self.y, self.width, self.height)
        )
        self.item_tops = []
        y_offset = 0
        for i in range(self.start_index, len(self.items)):
            if y_offset + self.item_heights[i] > self.height:
                break  # Stop drawing if we run out of vertical space
            self.item_tops.append(self.y + y_offset)
            for line in self.wrapped_texts[i]:
                text_surface = self.font.render(line, True, (0, 0, 0))
                self.screen.blit(text_surface, (self.x, self.y + y_offset))
                y_offset += self.font.get_height()
            pygame.draw.line(
                screen,
                (140, 14, 14),
                (self.x, self.y + y_offset),
                (self.resolution[0], self.y + y_offset),
            )

    def choose(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.x <= mouse_pos[0] <= self.x + self.width:
            relative_y = mouse_pos[1]
            for i, top in enumerate(self.item_tops):
                if top <= relative_y < top + self.item_heights[i]:
                    print(f"Chosen item: {self.items[self.start_index + i]}")
                    return
        print("No item chosen.")


# Initialize pygame
pygame.init()
resolution = (800, 600)
screen = pygame.display.set_mode(resolution)

# Create the ViewScrollBar instance and bind a list of items
view_scroll_bar = ViewScrollBar(screen, resolution)
view_scroll_bar.bind(
    [
        "Item \nIt is a long string And It is a very long string" + str(i)
        for i in range(1, 51)
    ]
)  # Example items

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                view_scroll_bar.choose()
        elif event.type == pygame.MOUSEWHEEL:
            if event.y > 0:  # Scroll up
                view_scroll_bar.update(screen, "up")
            elif event.y < 0:  # Scroll down
                view_scroll_bar.update(screen, "down")

    screen.fill((0, 0, 0))  # Clear the screen with black
    view_scroll_bar.render()  # Render the scroll list
    pygame.display.flip()  # Update the full display Surface to the screen

pygame.quit()
