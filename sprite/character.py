import pygame
from constants import PRICE_WARRIOR, PRICE_WORKER

"""
Класс отвечающий за анимацию персонажей.
Персонажи: "Воин", "Рабочий".

Логика класса:
    Когда заканчиваются кристаллы персонажи должны "пропадать" с поля.
"""


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, file_name):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = pygame.image.load(file_name).convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.showing = False


class WarriorCharacter(Character):
    def __init__(self, x, y, file_name):
        Character.__init__(self, x, y, file_name)
        self.price = PRICE_WARRIOR

    def update(self, coins) -> None:
        self.showing = coins >= self.price
        if self.showing:
            self.image.set_alpha(255)
        else:
            self.image.set_alpha(100)


class Worker_Character(Character):
    def __init__(self, x, y, file_name):
        Character.__init__(self, x, y, file_name)
        self.price = PRICE_WORKER

    def update(self, coins) -> None:
        self.showing = coins >= self.price
        if self.showing:
            self.image.set_alpha(255)
        else:
            self.image.set_alpha(100)
