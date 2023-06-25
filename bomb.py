import pygame
class Bomb(pygame.sprite.Sprite):
    #初始化爆炸
    def __init__(self,ai_settings,scene):
        super(Bomb, self).__init__()
        self.main_scene = scene
        # 加载爆炸资源
        self.image = [pygame.image.load("picture/bomb-" + str(v) + ".png") for v in range(1, 7)]
        # 改变飞船大小
        for i in range(len(self.image)):
            self.image[i]=pygame.transform.scale(self.image[i],(80,80))

        # 设置当前爆炸播放索引
        self.index = 0
        # 图片爆炸播放间隔
        self.interval = 20
        self.interval_index = 0
        # 爆炸位置
        self.position = [600, 600]
        # 是否可见
        self.visible = False
        self.rect=self.image[0].get_rect()

        # 设置爆炸播放的位置

    def set_pos(self, x, y):
        self.position[0] = x
        self.position[1] = y

        # 爆炸播放

    def action(self):
        # 如果爆炸对象状态不可见，则不计算坐标
        if not self.visible:
            return
        now = pygame.time.get_ticks()

        # 控制每帧图片的播放速度
        if now - self.last_update > self.frame_duration:
            self.current_frame = (self.current_frame + 1) % len(self.explosion_images)
            self.image = self.explosion_images[self.current_frame]
            self.last_update = now

        # 根据爆炸动画的持续时间，将 visible 属性设为 False 来删除这个精灵实例
        if now - self.start_time > self.duration:
            self.visible = False



        # 绘制爆炸

    def draw(self):
        # 如果对象不可见，则不绘制
        if not self.visible:
            return
        self.main_scene.blit(self.image[self.index], (self.position[0], self.position[1]))
