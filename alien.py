import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.image = pygame.image.load('image/alien.bmp')
        self.rect = self.image.get_rect()
        #外星人在左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def blit_alien(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def check_edge(self):
        screen_rect = self.screen.get_rect() #获取屏幕的右边缘
        if self.rect.right >= screen_rect.right: #自己的矩形右边缘和屏幕的比较
            return True
        elif self.rect.left <= 0:
            return True
