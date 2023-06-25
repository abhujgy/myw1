import sys
import pygame
from bullet import  Bullet
from time import sleep
from bomb import Bomb
from alien import Alien
from button import Button
def check_keydown_events(event,ai_settings,screen,ship,bullets,stats,aliens,sb):
    #响应按键
    if event.key == pygame.K_RIGHT:
        # 向右移飞船
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)
    elif event.key==pygame.button or event.key==pygame.K_ESCAPE:
        stats.save_high_score()
        sys.exit()


def fire_bullet(ai_settings,screen,ship,bullets):
    """如果还没有达到限制就发射一颗子弹"""
    # 创建一颗子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
def check_keyup_events(event,ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    """鼠标与响应事件"""
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            stats.save_high_score()
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets,stats,aliens,sb)
        elif event.type==pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type==pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y)

def check_play_button(ai_settings,screen,stats,sb1,play_button,ship,aliens,bullets,mouse_x,mouse_y):
    """玩家单击play按钮时且此时游戏为非活动状态开始新游戏"""
    button_clicked=play_button.rect.collidepoint(mouse_x,mouse_y)

    if button_clicked and not stats.game_active:
        #重置游戏设置
        ai_settings.initialize_dynamic_settings()
        #隐藏光标
        pygame.mouse.set_visible(False)
        #重置游戏统计信息
        stats.reset_stats()
        stats.game_active=True
        #重置记分牌图像
        sb1.prep_score()
        sb1.prep_high_score()
        sb1.prep_level()#
        sb1.prep_ships()
        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        #创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()


def update_screen(screen,stats,sb,ship,aliens,bullets,play_button,bomb):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环都重绘屏幕
    #screen.fill(ai_settings.bg_color)

    #在飞船和外星人后面重回所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    #绘制爆炸图片

    bomb.draw()
    #显示得分
    sb.show_score()
    #如果游戏处于非活动状态，就绘制Play按钮
    if  not stats.game_active and stats.ships_left>0:
        play_button.draw_button()


    # 让最近绘制的屏幕可见
    pygame.display.flip()
def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets,bomb):
    """更新子弹的位置并删除已经消失的子弹"""
    bullets.update()
    #删除已经消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom<=0:
            bullets.remove(bullet)

    #check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets,bomb)
    collisions=pygame.sprite.groupcollide(bullets,aliens,True,False)
    for alien in collisions.values():
        for each_alien in alien:
            each_alien.health-=1
            if each_alien.health==0:
                diex = 0
                diey = 0
                diex=each_alien.rect.x
                diey=each_alien.rect.y
                stats.score+=ai_settings.alien_points
                sb.prep_score()
                print(diex,diey)
                aliens.remove(each_alien)
                dieimg1 = pygame.image.load("picture/bomb-1.png")
                dieimg1 = pygame.transform.scale(dieimg1, (80, 80))
                screen.blit(dieimg1, (diex, diey))
                pygame.display.update()  # 刷新
                dieimg2 = pygame.image.load("picture/bomb-2.png")
                dieimg2 = pygame.transform.scale(dieimg2, (80, 80))
                screen.blit(dieimg2, (diex, diey))
                pygame.display.update()  # 刷新
                dieimg3 = pygame.image.load("picture/bomb-3.png")
                dieimg3 = pygame.transform.scale(dieimg3, (80, 80))
                screen.blit(dieimg3, (diex, diey))
                pygame.display.update()  # 刷新
                dieimg4 = pygame.image.load("picture/bomb-4.png")
                dieimg4 = pygame.transform.scale(dieimg4, (80, 80))
                screen.blit(dieimg4, (diex, diey))
                pygame.display.update()  # 刷新
                dieimg5 = pygame.image.load("picture/bomb-5.png")
                dieimg5 = pygame.transform.scale(dieimg5, (80, 80))
                screen.blit(dieimg5, (diex, diey))
                pygame.display.update()  # 刷新
                dieimg6 = pygame.image.load("picture/bomb-6.png")
                dieimg6 = pygame.transform.scale(dieimg6, (80, 80))
                screen.blit(dieimg6, (diex, diey))
                pygame.display.update()  # 刷新
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens,bullets, bomb)


def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets,bomb):
    """响应子弹和外星人的碰撞"""
    #删除已经发生碰撞的子弹和外星人

    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            for alien in aliens:
                alien.take_damage()
            stats.score+=ai_settings.alien_points*len(aliens)
            sb.prep_score()
            check_high_score(stats,sb)


    if len(aliens) == 0:
        # 删除现有的子弹和外星人
        bullets.empty()
        ai_settings.increase_speed()
        #提高等级
        stats.level+=1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)
def get_number_aliens_x(ai_settings,alien_width):
    """计算每行可容纳多少个外星人"""
    avaliable_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(avaliable_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings,ship_height,alien_height):
    """计算屏幕可容纳多少行外星人"""
    avaliable_space_y = (ai_settings.screen_height-(3*alien_height)-ship_height)
    number_rows=int(avaliable_space_y/(2*alien_height))
    return number_rows


def create_alien(ai_settings,screen,aliens,alien_number,row_number):

    """创建一个外星人并将其放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width*alien_number
    alien.rect.x=alien.x
    alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
    aliens.add(alien)



def check_fleet_edages(ai_settings,aliens):
    """有外星人到达边缘采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break
def change_fleet_direction(ai_settings,aliens):
    """将外星人整体下移，并改变他们的方向"""
    for alien in aliens.sprites():
        alien.rect.y+=ai_settings.fleet_drop_speed
    ai_settings.fleet_direction*=-1

def ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """相应外星人撞到飞船"""
    if stats.ships_left>0:
      #将ships_left减1
      stats.ships_left-=1
      #更新记分牌
      sb.prep_ships()

      #清空外星人列表和子弹列表
      aliens.empty()
      bullets.empty()
      #创建一群新的外星人，并将飞创放到屏幕底端中央
      create_fleet(ai_settings,screen,ship,aliens)
      ship.center_ship()
      #暂停
      sleep(0.5)

    else:
        stats.game_active=False
        pygame.mouse.set_visible(True)
def update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets,bomb):
    """更新外星人的位置"""
    """检查是否有外星人位于屏幕边缘，并更新整群外星人的位置"""
    bomb.action()
    check_fleet_edages(ai_settings,aliens)
    aliens.update()
    #检查外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
       ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
    #检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets)
def check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect=screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom>=screen_rect.bottom:
            #像飞船被撞到一样进行处理
            ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
            break
def create_fleet(ai_settings,screen,ship,aliens):
    """"""
    #创建一个外星人，并计算一行可容乃多少个外星人
    #外星人间距为外星人的宽度
    alien=Alien(ai_settings,screen)
    
    number_aliens_x=get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows=get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    #创建第一行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
          #创建一个外星人并将其加入当前行
          create_alien(ai_settings,screen,aliens,alien_number,row_number)
def check_high_score(stats,sb):
    """检查是否诞生了新的最高分"""
    if stats.score>stats.high_score:
        stats.high_score=stats.score
        sb.prep_high_score()

