import pygame


class Statistics:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 100
        self.height = 50

    def draw(self, sc):
        font = pygame.font.SysFont("comicsans", 45)
        text = font.render(self.text, 1, (0, 255, 255))
        sc.blit(text, (self.x, self.y))
