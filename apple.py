import pygame
import random
import config


class Apple:
    def __init__(self):
        self.r = 5
        self.x = random.randint(20, config.game_width - 20) // 10*10
        self.y = random.randint(20, config.game_height - 20) // 10*10
        self.color = (255, 0, 0)

    def draw(self, display):
        pygame.draw.circle(surface=display, color=self.color, center = [self.x, self.y], radius=self.r)
