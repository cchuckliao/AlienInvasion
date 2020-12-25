import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


# 不需要任何形参


def check_keydown_events(event, ai_settings, screen, ship, stats, bullets):
    if event.key == pygame.K_RIGHT:  # 向右移动
        ship.moving_right = True
    if event.key == pygame.K_LEFT:  # 向左移动
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        with open('high_score.txt','w') as score_file:
            score_file.write(str(stats.high_score))
        sys.exit()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, stats, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:  # 响应鼠标事件
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    # 在玩家单机play按钮时开始游戏。cillidepoint用来检查鼠标坐标是否在play_button的rect里面。
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # reset the game speed
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True
        # 重置记分牌
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        # 清空子弹和外星人
        aliens.empty()
        bullets.empty()
        # 创建一群外星人，并让飞船居中
        creat_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blit_ship()
    aliens.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()  # 让最近绘制的屏幕可见


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # 更新子弹位置，并且删除已经消除的子弹
    bullets.update()
    # delete bullets outside of scrren
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)
    # groupcollide验证两个sprite group的碰撞，告诉pygame删除他们。
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        creat_fleet(ai_settings, screen, ship, aliens)
        stats.level += 1
        sb.prep_level()  # 每次更新等级就要用到，重新转换字符成图片


def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))  # 给外星人留空右边空间
    return number_aliens_x


def creat_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    # 创建第一行外星人

    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number  # 指定每行外星人的y坐标
    aliens.add(alien)


def creat_fleet(ai_settings, screen, ship, aliens):
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            creat_alien(ai_settings, screen, aliens, alien_number, row_number)


def get_number_rows(ai_settings, ship_height, alien_height):
    # 计算可容纳多少行外星人
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def check_fleet_edge(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edge():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()
        # clear the ship and aliens on the screen
        aliens.empty()
        bullets.empty()
        # create new aliens fleet and put them on the middle bottom of the screen
        creat_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # 检查是否有外星人位于屏幕边缘，更新其位置
    check_fleet_edge(ai_settings, aliens)
    aliens.update()
    # 检测外星人和飞船的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):  # 检测实参和遍历编组是否发生碰撞，返回碰撞的那一个外星人
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()