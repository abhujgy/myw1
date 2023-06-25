import tkinter

from settings import Settings
from game_stats import GameStats
from ship import Ship
from scoreborad import Scoreborad
import pygame
from button import Button
from pygame.sprite import Group
import game_functions as gf
from bomb import Bomb

from pygame.locals import *

def run_game():
    #初始化并创建一个屏幕
    pygame.init()
    ai_settings=Settings()
    screen=pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    background=pygame.image.load('images/background.jpg').convert()

    #创建play按钮
    play_button=Button(ai_settings,screen,"Play")

    #创建一个用于存储游戏统计信息的实例
    stats=GameStats(ai_settings)
    sb=Scoreborad(ai_settings,screen,stats)
    #创建一艘飞船
    ship=Ship(ai_settings,screen)
    #创建一个用于存储子弹的编组
    bullets=Group()
    #创建一个外星人编组
    aliens =Group()
    #创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)
    #创建爆炸对象
    bomb=Bomb(ai_settings,screen)

    # 开始游戏主循环
    while True:
        # 监视键盘和鼠标事件
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active and stats.ships_left > 0:
            ship.update()
            # bullets.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, bomb)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, bomb)
        elif stats.game_active and stats.ships_left <= 0:
            asas = 0
            root = tkinter.Tk()
            screenwidth = root.winfo_screenwidth()
            screenheight = root.winfo_screenheight()
            root.geometry("%dx%d+%d+%d" % (400, 400, (screenwidth - 400) / 2, (screenheight - 400) / 2))
            tt = tkinter.Label(root, text='Game Over', fg="red", bg="yellow",
                               font=("微软雅黑", 50))
            tt.pack()
            againbutton = tkinter.Button(root, text="Again", command=onclick1)
            againbutton.pack()
            root.mainloop()
            if asas == 1:
                root.destroy()
            else:
                print(asas)
        screen.blit(background, (0, 0))
        gf.update_screen(screen, stats, sb, ship, aliens, bullets, play_button, bomb)


def onclick1():
    asas = 1
    run_game()
    return asas


run_game()

run_game()
