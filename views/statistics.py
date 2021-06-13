import pygame


class Statistics:
    def __init__(self, text, x, y, color, font):
        self.font = font
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 100
        self.height = 50

    def draw(self, sc):
        text = self.font.render(self.text, 1, self.color)
        sc.blit(text, (self.x, self.y))
