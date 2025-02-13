import pygame
from time import sleep
import random
from pygame.sprite import collide_rect

#初始化pygame
# pygame.init()
# #创建一个窗口
# pygame.display.set_mode((800,600))
# pygame.display.set_caption('坦克小战')
# running = True

bg_color =pygame.Color(255,255,255)
text_color = (0,0,0)
SCREEN_WIDTH = 1200
SCREEN_HEIGHT =600
class tank:
    '''坦克类'''
    def __init__(self):
        self.living=True
        #记录老位置
        self.old_left=0
        self.old_top=0
    def display_tank(self):
        '''坦克显示'''
        self.image = self.images.get(self.direction)   #获取最新朝向位置
        main.window.blit(self.image, self.rect)
    def move(self):
        '''坦克移动'''
        self.old_left=self.rect.left  #记录原来位置
        self.old_top=self.rect.top
        if self.direction == 'u':
            if self.rect.top > 0:
                self.rect.top=self.rect.top-self.speed
        if self.direction == 'd':
            if self.rect.top+self.rect.height < SCREEN_HEIGHT:
                self.rect.top=self.rect.top+self.speed
        if self.direction == 'l':
            if self.rect.left>0:
                self.rect.left=self.rect.left-self.speed
        if self.direction == 'r':
            if self.rect.left+self.rect.height< SCREEN_WIDTH:
                self.rect.left=self.rect.left+self.speed
    def tank_hit_wall(self):
        for wall in main.walls:
            if pygame.sprite.collide_rect(self,wall):
                #还原记录位置
                self.rect.left=self.old_left
                self.rect.top=self.old_top
    def shot(self):
        '''坦克射击'''
        pass
    def tank_hit_tank(self,tank):
        '''检测坦克碰撞'''
        if self and tank and self.living and tank.living:
            if pygame.sprite.collide_rect(self,tank):
                self.rect.left=self.old_left
                self.rect.top=self.old_top
class user_tank(tank):
    def __init__(self,left,top):
        '''构造坦克类'''
        super(user_tank, self).__init__()
        self.images = {
            'u': pygame.image.load('img/p1tankU.gif'),
            'd': pygame.image.load('img/p1tankD.gif'),
            'r': pygame.image.load('img/p1tankR.gif'),
            'l': pygame.image.load('img/p1tankL.gif')
        }
        self.direction = 'u'  # 设置方向
        self.image = self.images.get(self.direction)  # 获取图形信息
        self.rect = self.image.get_rect()       #获取图片的矩形
        self.rect.left = left
        self.rect.top = top
        self.speed =6
        self.remove = False
class enemytank(tank):
    def __init__(self,left,top,speed):
        super(enemytank, self).__init__()
        self.images={
            'u': pygame.image.load('img/enemy1U.gif'),
            'd': pygame.image.load('img/enemy1D.gif'),
            'r': pygame.image.load('img/enemy1R.gif'),
            'l': pygame.image.load('img/enemy1L.gif')
        }
        self.direction=self.rand_direction()
        self.image=self.images[self.direction]
        self.rect=self.image.get_rect()
        self.rect.top=top
        self.rect.left=left
        self.speed=speed
        self.step=20
    def rand_direction(self):
        return random.choice(['u','d','r','l'])
    def rand_move(self):
        if self.step <=0:              #判断步长
            self.direction=self.rand_direction()
            self.step=20
        else:
            self.move()
            self.step-=1
    def e_shot(self):
        numbers=random.randint(1,100)
        if numbers<=2:
            return fire(self)

class fire:
    '''子弹类'''
    def __init__(self,tank):
        self.image=pygame.image.load('img/enemymissile.gif') #加载图片
        self.direction=tank.direction      #获取子弹方向
        self.rect=self.image.get_rect()    #获取子弹图形
        if self.direction == "l":
            # 子弹的位置 = 坦克的位置 - 子弹的宽度
            self.rect.left = tank.rect.left - self.rect.width
            # 子弹的位置 = 坦克的位置 + 坦克的高度/2 - 子弹的高度/2
            self.rect.top = tank.rect.top + tank.rect.height / 2 - self.rect.height / 2
        elif self.direction == "r":
            # 子弹的位置 = 坦克的位置 + 坦克的宽度
            self.rect.left = tank.rect.left + tank.rect.width
            # 子弹的位置 = 坦克的位置 + 坦克的高度/2 - 子弹的高度/2
            self.rect.top = tank.rect.top + tank.rect.height / 2 - self.rect.height / 2
        elif self.direction == "u":
            # 子弹的位置 = 坦克的位置 + 坦克的宽度/2 - 子弹的宽度/2
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            # 子弹的位置 = 坦克的位置 - 子弹的高度
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == "d":
            # 子弹的位置 = 坦克的位置 + 坦克的宽度/2 - 子弹的宽度/2
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            # 子弹的位置 = 坦克的位置 + 坦克的高度
            self.rect.top = tank.rect.top + tank.rect.height
            # 设置子弹的速度
        self.speed = 8
        self.living=True
    def move(self):
        '''子弹移动'''
        if self.direction == "l":
            if self.rect.left > 0:
                self.rect.left-=self.speed
            else:
                self.living=False
        elif self.direction == "r":
            if self.rect.left+self.rect.width < SCREEN_WIDTH:
                self.rect.left+=self.speed
            else:
                self.living=False
        elif self.direction == "u":
            if self.rect.top > 0:
                self.rect.top-=self.speed
            else:
                self.living=False
        elif self.direction == "d":
            if self.rect.top+self.rect.height< SCREEN_HEIGHT:
                self.rect.top+=self.speed
            else:
                self.living=False
    def display_fire(self):
        '''子弹显示'''
        main.window.blit(self.image, self.rect)
    def hit_e_tank(self):
        for e_tank in main.enemy_tanks:
            if collide_rect(self,e_tank):        #判断是否击中
                bomn1=bomn(e_tank)
                main.bomns.append(bomn1)
                self.living=False
                e_tank.living=False
    def hit_my_tank(self):
        if main.my_tank:
            if collide_rect(self,main.my_tank):
                bomn1=bomn(main.my_tank)
                main.bomns.append(bomn1)
                self.living=False
                main.my_tank.living=False
    def hit_wall(self):
        for wall in main.walls:
            if collide_rect(self,wall):         #判断是否碰撞
                self.living=False
                wall.hp-=1
                if wall.hp<=0:
                    wall.living=False
                Music=music('img/hit.wav')
                Music.play_music()

class wall:
    '''墙'''
    def __init__(self,top,left):
        self.image=pygame.image.load("img/steels.gif")
        self.rect=self.image.get_rect()
        self.rect.top=top
        self.rect.left=left
        self.hp=3         #墙生命值
        self.living=True

    def display_wall(self):
        main.window.blit(self.image,self.rect)
class bomn:
    def __init__(self,tank:tank):
        self.images=[
            pygame.image.load("img/blast0.gif"),
            pygame.image.load("img/blast1.gif"),
            pygame.image.load("img/blast2.gif"),
            pygame.image.load("img/blast3.gif"),
            pygame.image.load("img/blast4.gif")
        ]               #加载爆炸图片
        self.rect=tank.rect    #设置爆炸位置
        self.step=0
        self.image=self.images[self.step]
        self.living=True
    def display_bomn(self):
        if self.step<len(self.images):   #判断是否播放完毕
            self.image=self.images[self.step]       #获取当前爆炸效果
            self.step+=1
            main.window.blit(self.image,self.rect)
        else:
            self.step=0
            self.living=False
class music:
    pygame.mixer.init()
    def __init__(self,filename:str):
        pygame.mixer.music.load(filename)
    def play_music(self):
        pygame.mixer.music.play()
class main:
    def __init__(self):
        pass
    window=None
    my_tank=None
    enemy_tanks=[]       #存储坦克列表
    enemy_tank_v=8
    my_fires=[]        #存储我方子弹
    e_fires=[]      #存储敌方子弹
    bomns=[]
    walls=[]
    live=5
    def create_enemy(self):
        for i in range(self.enemy_tank_v):
            left=random.randint(0,600)
            top=random.randint(0,200)
            speed=random.randint(1,7)
            enemy_tank=enemytank(left,top,speed)        #创建敌方坦克
            self.enemy_tanks.append(enemy_tank)
    def start_game(self):
        pygame.display.init()                       #初始化
        pygame.display.set_caption('坦克小战')              #标题
        main.window=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))        #窗口
        self.create_new_tank()
        self.create_enemy()
        self.create_wall()
        while True:
            sleep(0.02)
            main.window.fill(bg_color)      #背景
            text=self.get_text(f'敌方剩余坦克数量{len(main.enemy_tanks)}')           #要增加的文字内容
            main.window.blit(text,(10,10))          #如何加上文字
            text2=self.get_text(f'我方剩余生命{main.live}')
            main.window.blit(text2,(10,30))
            text3=self.get_text(f'wasd移动，j射击，esc复活')
            main.window.blit(text3,(10,50))
            self.get_event()                        #增加事件
            if main.my_tank and main.my_tank.living:
                main.my_tank.display_tank()              #显示我方坦克
            else:
                main.my_tank=None
            self.display_enemy()
            if main.my_tank and main.my_tank.living:
                if main.my_tank.remove:
                    main.my_tank.move()                     #移动我方坦克
                    main.my_tank.tank_hit_wall()            #判断我方坦克是否撞上敌方坦克
                    for i in main.enemy_tanks:
                        main.my_tank.tank_hit_tank(i)
            self.display_my_fire()                        #显示我方子弹
            self.display_e_fire()                       #显示敌方坦克
            self.display__bomn()
            self.display_wall()
            pygame.display.update()
    def create_wall(self):
        top=300
        for i in range(9):
            Wall=wall(top,i*142.5)
            main.walls.append(Wall)
    def display_wall(self):
        for Wall in main.walls:
            if Wall.living:
                Wall.display_wall()
            else:
                main.walls.remove(Wall)
    def create_new_tank(self):
        main.my_tank = user_tank(600, 400)
        Music=music('img/start.wav')        #创建音乐对象
        Music.play_music()
    def display__bomn(self):
        for i in main.bomns:
            if i.living == True:
                i.display_bomn()


    def display_my_fire(self):
        for i in main.my_fires:
            if i.living == True:
                i.display_fire()
                i.move()
                i.hit_e_tank()          #判断是否击中敌方坦克
                i.hit_wall()            #判断是否击中墙
            else:
                main.my_fires.remove(i)
    def display_enemy(self):
        for i in main.enemy_tanks:
            if i.living == True:
                i.display_tank()  #显示敌方坦克
                i.rand_move()      #随机移动
                i.tank_hit_wall()       #敌方坦克撞墙
                i.tank_hit_tank(main.my_tank)
                e_fire=i.e_shot()
                if e_fire:
                    main.e_fires.append(e_fire)
            else:
                self.enemy_tanks.remove(i)


    def display_e_fire(self):
        for i in main.e_fires:
            if i.living == True:
                i.display_fire()
                i.move()
                i.hit_my_tank()    #判断是否击中我方坦克
                i.hit_wall()
            else:
                main.e_fires.remove(i)
    def get_text(self,text:str):
        '''获取文字图片'''
        pygame.font.init()    #初始化字体模块
        font=pygame.font.SysFont('kaiti',18)                 #创建字体
        text=font.render(text,True,text_color)                  #绘制文字信息
        return text
    def get_event(self):
        '''监听事件'''
        event_list=pygame.event.get()
        for event in event_list:
            if event.type==pygame.QUIT:
                pygame.quit()
                self.end_game()
            if event.type==pygame.KEYDOWN:
                if not main.my_tank and event.key==pygame.K_ESCAPE:
                    if main.live>0:
                        self.create_new_tank()          #复活
                        main.live-=1
                    else:
                        self.end_game()
                if main.my_tank and main.my_tank.living:
                    if event.key==pygame.K_w:
                        print('up')
                        main.my_tank.direction='u'
                        main.my_tank.remove = True
                    if event.key==pygame.K_s:
                        print('Down')
                        main.my_tank.direction='d'
                        main.my_tank.remove = True
                    if event.key==pygame.K_a:
                        print('left')
                        main.my_tank.direction='l'
                        main.my_tank.remove = True
                    if event.key==pygame.K_d:
                        print('right')
                        main.my_tank.direction='r'
                        main.my_tank.remove =True
                    if event.key==pygame.K_j:
                        if len(main.my_fires)<5:
                            my_fire=fire(main.my_tank) #创建子弹
                            main.my_fires.append(my_fire)
                            Music=music('img/fire.wav')
                            Music.play_music()
            if event.type==pygame.KEYUP and event.key in(pygame.K_w,pygame.K_s,pygame.K_a,pygame.K_d):
                if main.my_tank and main.my_tank.living:
                    main.my_tank.remove =False
    def end_game(self):
        '''结束游戏'''
        print('结束')
        exit()
if __name__ == '__main__':
    main().start_game()




