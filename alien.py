import pygame
from pygame.sprite import Sprite
from bomb import Bomb
import random
class Alien(Sprite):
    """表示单个外星人的类"""

    def __init__(self,ai_settings,screen):
        """初始化外星人并设置其起始的位置"""
        super(Alien,self).__init__()
        self.screen=screen
        self.ai_settings=ai_settings
        #加载外星人图像，并设置其rect属性
        self.image=pygame.image.load('images/alien.png')
        #改变外星人图像大小
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect=self.image.get_rect()
        #每个外星人最初都在屏幕左上角附近
        self.rect.x=self.rect.width
        self.rect.y=self.rect.height
        #存储外星人的准确位置
        self.x=float(self.rect.x)
        #添加heath实例变量，表示生命值
        self.health=3

        # 加载并缩放爆炸效果图片


       # self.explosion_images = [
       #     pygame.transform.scale(pygame.image.load("picture/bomb-" + str(v) + ".png"), (80, 80))
        #    for v in range(1, 7)
        #]
       # self.explosion_position = [0, 0]
        #self.explosion_index = 0
       # self.explosion_interval = 20
       # self.explosion_interval_index = 0
       # self.explosion_visible = False


    def blitme(self):
        """在指定位置绘制外星人"""
        self.screen.blit(self.image,self.rect)



    def check_edges(self):
        """如果外星人位于屏幕边缘，就返回True"""
        screen_rect=self.screen.get_rect()
        if self.rect.right>=screen_rect.right:
            return True
        elif self.rect.left<=0:
            return True


    def update(self):
        """向右或左移动外星人"""
        self.x+=(self.ai_settings.alien_speed_factor*self.ai_settings.fleet_direction)
        self.rect.x=self.x

        if self.is_dead():
            #如果外星人已经， 则设置爆炸效果的初始位置和可见性
            self.explosion_position[0] = self.rect.centerx - 38
            self.explosion_position[1] = self.rect.centery - 38
            self.explosion_visible = True


    def is_dead(self):
        """检查是否死亡"""
        return self.health<=0;
    def take_damage(self,ai_settings,screen,explosions):
        """扣除一点生命值"""
        self.heatlh-=1
        if self.health==0:
            x,y=self.rect.centerx,self.rect.centery
            explosion=Bomb(ai_settings,screen)
            explosion.set_pos(x,y)
            explosions.add(explosion)

    def draw_explosion(self, explosion_group):
        """在屏幕上绘制爆炸效果"""
        if not self.explosion_visible:
            return

        if self.explosion_index >= len(self.explosion_images):
            self.explosion_index = 0
            self.explosion_visible = False
            return

        explosion_group.add(Bomb(self.explosion_images[self.explosion_index], self.explosion_position))
        self.explosion_index += 1