import pygame


class Button:
    def __init__(self, x, y, width, height, callback: callable = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.callback = callback
        self.button_down = False
        self.showing = False
        self.button_rect = pygame.Rect(x, y, width, height)

    def draw(self) -> None:
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

    def is_button_down(self) -> bool:
        return self.button_down
