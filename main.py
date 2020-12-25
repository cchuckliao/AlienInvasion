import pygame
from settings import Settings
from ship import Ship
import game_function as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


# 加一个星星图片，随机分配
# 主函数的作用：实例化各个对象，传递参数，刷新屏幕达到游戏效果


def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))  # 屏幕对象
    pygame.display.set_caption('Alien Invasion')
    play_button = Button(ai_settings, screen, "play")
    stats = GameStats(ai_settings)
    ship = Ship(ai_settings, screen)  # 创建一个飞船,放在主循环前，避免每次循环都要创建一个飞船对象
    bullets = Group()
    aliens = Group()
    sb = Scoreboard(ai_settings, screen, stats)
    # 创建外星人群
    gf.creat_fleet(ai_settings, screen, ship, aliens)
    while True:  # 开始游戏
        # 键盘和鼠标
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)
        # s更新屏幕中显示的东西
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)
        # 放在创建背景后，使其出现在背景出面


run_game()
