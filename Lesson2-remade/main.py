import random
from os import path

import pygame

# TODO Refactor 將參數統一放到另外一個檔案
import self as self

SHOT_DELAY = 300

YELLOW = (255, 255, 0)

HEIGHT = 600

WIDTH = 600

BLACK = (0, 0, 0)

GREEN = (0, 255, 0)

RED = (255, 0, 0)

FPS = 30

img_dir = path.join(path.dirname(__file__), 'img')
sound_dir = path.join(path.dirname(__file__), 'sound')
font_name = pygame.font.match_font('arial')
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(path.join(sound_dir, "bgm.mp3"))
pygame.mixer.music.play(-1)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load(path.join(img_dir, "ship.png"))
        self.image = pygame.transform.scale(image, (50, 30))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedx = 8
        self.speedy=8
        self.shield =100

    def update(self):
        self.keyEventHandling()

    def keyEventHandling(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            player.move(-self.speedx, 0)
        if keystate[pygame.K_RIGHT]:
            player.move(self.speedx, 0)
        if keystate[pygame.K_UP]:
            player.move(0,-self.speedy)
        if keystate[pygame.K_DOWN]:
            player.move(0,self.speedy)
            # TODO 01.新增上下移動

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy


class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.size = random.randrange(3, 8)
        image = pygame.image.load(path.join(img_dir, "meteor.png"))
        self.image = pygame.transform.scale(image, (self.size * 8, self.size * 8))

        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH)
        self.rect.y = 0
        self.speedx = random.randint(-5, 5)
        self.speedy = random.randint(1, 5)
        self.image_origin = self.image
        self.rot_angle = 5
        self.angle =0

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        old_center = self.rect.center
        self.angle =self.angle+self.rot_angle
        self.image = pygame.transform.rotate(self.image_origin,self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = old_center

        if (self.rect.y > HEIGHT):
            newMeteor()
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(path.join(img_dir, "laser_gun.png"))
        self.rect = self.image.get_rect()
        self.rect.centerx = posx
        self.rect.centery = posy
        self.speedy = 10.

    def update(self):
        self.rect.y -= self.speedy
        if self.rect.bottom < 0:
            self.kill()


def newMeteor():
    global all_sprites
    m = Meteor()
    meteors.add(m)
    all_sprites.add(m)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
bg = pygame.image.load(path.join(img_dir,'background.png'))
bg_rect = bg.get_rect()
clock = pygame.time.Clock()

meteors = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
supports=pygame.sprite.Group()

last_shot = pygame.time.get_ticks()
now = 0
score = 0
player = Player(WIDTH / 2, HEIGHT - 50)

for i in range(8):
    newMeteor()

all_sprites.add(bullets)
all_sprites.add(player)
all_sprites.add(meteors)
running = True
sound_pew = pygame.mixer.Sound(path.join(sound_dir, "pew.wav"))




def check_meteor_hit_player():
    global running, meteors
    # TODO 05.修正碰撞偵測的規則
    # hits = pygame.sprite.spritecollide(player, meteors, False, pygame.sprite.collide_circle_ratio(0,7))
    hits = pygame.sprite.spritecollide(player,meteors,False,pygame.sprite.collide_circle_ratio(0.7))
    if hits:
        for hit in hits:
            hit.kill()
            # print("check_meteor_hit_player")
            newMeteor()
            # TODO 修改死亡的規則，改成扣血扣到0時，遊戲才結束
            player.shield = player.shield-10
            print(player.shield)
            if player.shield <= 0:
                running = False
def check_player_hit_support():
    hits=pygame.sprite.spritecollide(player, supports,False)
    for hit in hits:
        player.shield+=5
   # support = pygame.image.load(path.join(img_dir,  "bolt_gold.png"))
    # hit = pygame.sprite.spritecollide(player ,supports ,True)



class Explosion(pygame.sprite.Sprite):
    ani_list = []
    for i in range(0,9):
        ani_list.append(pygame.image.load(path.join(img_dir, "regularExplosion0{0}.png".format(i))))

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.ani_list[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.last_ani = pygame.time.get_ticks()
        self.ani_delay = 100
        self.ani_ind = 1

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_ani > self.ani_delay:
            self.ani_ind += 1
            # self.image = pygame.image.load(path.join(img_dir, "regularExplosion0{0}.png".format(self.ani_ind)))
            self.image = self.ani_list[self.ani_ind]
        if self.ani_ind >= 8:
            self.kill()


def play(self):
    pass

class Support(pygame.sprite.Sprite):
    def __init__(self,x,y,type):
        type = 0 or 1
        pygame.sprite.Sprite.__init__(self)
        if type==0:
            self.image = pygame.image.load(path.join(img_dir, "bolt_gold.png"))
        else:
            self.image = pygame.image.load(path.join(img_dir, "bolt_gold.png"))
        self.image =pygame.image.load(path.join(img_dir, "bolt_gold.png"))
        self.rect =self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedy = 7

    # if player.hit.pygame.image.load(path.join(img_dir,"bolt_gold.png"))
    #         self.shield +1
    #             pygame.image.load(path.join(img_dir,"bolt_gold.png")).hide


    def update(self):
        self.rect.centery = self.rect.centery + self.speedy
        if self.rect.centery > HEIGHT:
            self.kill()




def check_bullets_hit_meteor():
    global  score
    # TODO 05.修正碰撞偵測的規則
    hits = pygame.sprite.groupcollide(meteors, bullets, True, True)
    if hits:
        for hit in hits:
            hit.kill()
            # TODO 02.修改加分的機制
            score += hit.size
            hit.kill()
            # print("check_bullets_hit_meteor")
            newMeteor()

            # TODO 04.增加爆炸的動畫
            explosion = Explosion(hit.rect.centerx, hit.rect.centery)
            all_sprites.add(explosion)

        if random.randint(0 , 10) > 5:
            package = Support(hit.rect.centerx , hit.rect.centery ,random.randint(0,1))
            supports.add(package)
            all_sprites.add(package)
            # TODO 06.擊破隕石會掉出武器或是能量包 武器可以改變攻擊模式 能量包可以回血

def draw_score():
    font = pygame.font.Font(font_name, 14)
    text_surface = font.render(str(score), True, YELLOW)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (WIDTH/2, 20)
    screen.blit(text_surface, text_rect)
    pass


def shoot():
    sound_pew.play()
    bullet = Bullet(player.rect.centerx, player.rect.centery)
    bullets.add(bullet)
    all_sprites.add(bullet)

def draw_shield():
    shield_bar = pygame.rect.Rect(10,10,player.shield,30)
    outline_rect = pygame.rect.Rect(10,10,100,30)
    pygame.draw.rect(screen,GREEN,shield_bar)
    pygame.draw.rect(screen, (255,255,255), outline_rect,2)

while running:
    # clocks control how fast the loop will execute
    clock.tick(FPS)

    # event trigger
    # TODO 新增起始畫面 按下空白鍵才開始遊戲
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # TODO 03.修正成子彈可以連發
            if event.key == pygame.K_SPACE:
                shoot()
    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_SPACE]:
        now=pygame.time.get_ticks()
        if now-last_shot > SHOT_DELAY:
            last_shot = now
            shoot()


    # update the state of sprites
    check_meteor_hit_player()
    #
    check_bullets_hit_meteor()
    check_player_hit_support()
    all_sprites.update()

    # draw on screen

    # screen.fill(BLACK)
    screen.blit(bg,bg_rect)
    draw_score()
    draw_shield()

    all_sprites.draw(screen)
    # flip to display
    pygame.display.flip()

pygame.quit()
