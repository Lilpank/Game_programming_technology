import pygame


class Button:
    def __init__(self, text, x, y, color, width: int = 150, height: int = 100, callback: callable = None):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.callback = callback
        self.button_down = False
        self.showing = False
        self.button_rect = pygame.Rect(x, y, width, height)

    def draw(self, sc):
        pygame.draw.rect(sc, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255, 255, 255))
        sc.blit(
            text,
            (
                self.x + round(self.width / 2) - round(text.get_width() / 2),
                self.y + round(self.height / 2) - round(text.get_height() / 2))
        )
        self.showing = True

    def handle_event(self, event: pygame.event):
        if self.x <= pygame.mouse.get_pos()[0] <= (self.x + self.width) and \
                self.y <= pygame.mouse.get_pos()[1] <= (self.y + self.height):

            if not self.showing:
                return None

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.button_down:
                    self.button_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.button_down and self.callback:
                    self.callback()

                self.button_down = False
