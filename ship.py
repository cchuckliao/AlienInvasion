import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.image = pygame.image.load('image/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect() #get_rect()是个什么方法？获得矩形属性.rect对象有上下左右坐标的数据

        self.rect.centerx = self.screen_rect.centerx #把属性传递
        self.rect.bottom = self.screen_rect.bottom
        #将飞船放在屏幕底部中央
        self.center = float(self.rect.centerx)
        self.moving_right = False
        self.moving_left = False

    def blit_ship(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        self.rect.centerx = self.center

    def center_ship(self):
        self.center = self.screen_rect.centerx





