import pygame

"""
Класс отвечащий за анимацию кнопок: "Закончить ход", "Атака".

"""


class Snap(pygame.sprite.Sprite):
    def __init__(self, x, y, file_name):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = pygame.image.load(file_name).convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.showing = False

    def update(self, is_showing) -> None:
        if is_showing:
            self.image.set_alpha(100)
        else:
            self.image.set_alpha(255)
