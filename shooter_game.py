#Создай собственный Шутер!
from pygame import *
from random import randint
from time import time as timer
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Shooter Game')
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))



mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
kick = mixer.Sound("fire.ogg")
FPS = 360
clock = time.Clock()
run = True
finish = False
lost = 0
score = 0 






class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.direction = "left"
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top,  -5, 10, 20)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(80, 620)
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= 0:
            self.kill()

first = (255, 169, 146)
second = (0, 0, 0)

player = Player("rocket.png", 315, 400, 2, 80, 80)
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
lifes = 3
for i in range(5):
    monster = Enemy("ufo.png", randint(80, 620), 0, randint(1, 2), 90, 65)
    monsters.add(monster)

for i in range(3):
    asteroid = Enemy("asteroid.png", randint(80, 620), 0, randint(1, 2), 90, 65)
    asteroids.add(asteroid)

font.init()



font1 = font.Font(None,36)
font2 = font.Font(None,36)
font3 = font.Font(None,70)
font4 = font.Font(None,70)

win = font3.render("You Win! :>", True, (255, 200, 10))
loose = font3.render("You Loose... :<", True, (255, 200, 10))

rel_time = False
num_fire = 0

while run:  
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    player.fire()
                    kick.play()
                    
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True             

            
                
            
    if finish != True:
        window.blit(background,(0,0))
        player.update()
        player.reset()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)

        sprites_list = sprite.groupcollide(bullets, monsters, True, True)
        for evil in sprites_list:
            score = score + 1
            monster = Enemy('ufo.png', randint(80,620), 0, randint(1,2), 90, 65)
            monsters.add(monster)

        if rel_time == True:
            new_time = timer()

            if last_time - new_time < 3:
                reload = font2.render('Перезарядка...', 1, (150, 0, 0))
                window.blit(reload, (260,460))
            else:
                num_fire = 0
                rel_time = False
            
        if score >= 10:
            finish = True
            window.blit(win, (250, 350))

        if lost >= 300 or sprite.spritecollide(player, monsters, False):
            finish = True
            window.blit(loose,(200, 200))

        if sprite.spritecollide(player, asteroids, False):
            lifes -= 1
            sprite.spritecollide(player, asteroids, True)

        if lifes <= 0:
            finish = True
            window.blit(loose,(200, 200))

        
            


        text_lose = font1.render('Пропущено: ' + str(lost), 1, (255,255,255))
        text_win = font2.render('Счёт: ' + str(score), 1, (255,255,255))
        text_lifes = font4.render(str(lifes), 1, first, second)
        window.blit(text_lose,(5,10))
        window.blit(text_win,(5,40))
        window.blit(text_lifes,(650,40))
    
    
    
    
    display.update()
    clock.tick(FPS)

    