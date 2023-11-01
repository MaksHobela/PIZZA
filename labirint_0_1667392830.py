from pygame import *

#клас-батько для інших спрайтів
class GameSprite(sprite.Sprite):
    #конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        # Викликаємо конструктор класу (Sprite):
        sprite.Sprite.__init__(self)
 
        #кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(image.load(player_image), (size_x, size_y))

        #кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    #метод, що малює героя на вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    #метод, у якому реалізовано управління спрайтом за кнопками стрілочкам клавіатури
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed,player_y_speed):
        # Викликаємо конструктор класу (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)

        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
    ''' переміщає персонажа, застосовуючи поточну горизонтальну та вертикальну швидкість'''
    def update(self): 
        # Спершу рух по горизонталі
        if packman.rect.x <= win_width-80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed
            # якщо зайшли за стінку, то встанемо впритул до стіни
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0: # йдемо праворуч, правий край персонажа - впритул до лівого краю стіни
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left) # якщо торкнулися відразу кількох, то правий край - мінімальний із можливих
        elif self.x_speed < 0: # йдемо ліворуч, ставимо лівий край персонажа впритул до правого краю стіни
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right) # якщо торкнулися кількох стін, то лівий край - максимальний
        if packman.rect.y <= win_height-80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
            self.rect.y += self.y_speed
        # якщо зайшли за стінку, то встанемо впритул до стіни
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0: # йдемо вниз
            for p in platforms_touched:
                # Перевіряємо, яка з платформ знизу найвища, вирівнюємося по ній, запам'ятовуємо її як свою опору:
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0: # йдемо вгору
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom) # вирівнюємо верхній край по нижніх краях стінок, на які наїхали
    def fire(self):
        bullet = Bullet('egg.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

#клас спрайту-ворога
class Enemy_h(GameSprite):
    side = "left"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, x1, x2):
        # Викликаємо конструктор класу (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
        self.x1 =x1
        self.x2 =x2
    #рух ворога
    def update(self):
        if self.rect.x <= self.x1: 
            self.side = "right"
        if self.rect.x >= self.x2:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Enemy_v(GameSprite):
    side = "up"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, y1, y2):
        # Викликаємо конструктор класу (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
        self.y1 =y1
        self.y2 =y2

   #рух ворога
    def update(self):
        if self.rect.y <= self.y1: #w1.wall_x + w1.wall_width
            self.side = "down"
        if self.rect.y >= self.y2:
            self.side = "up"
        if self.side == "up":
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed

# клас спрайту-кулі
class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Викликаємо конструктор класу (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    #рух ворога
    def update(self):
        self.rect.x += self.speed
        # зникає, якщо дійде до краю екрана
        if self.rect.x > win_width+10:
            self.kill()


#Створюємо віконце
win_width = 1400
win_height = 800
display.set_caption("PIZZA")
window = display.set_mode((win_width, win_height))
back = transform.scale(image.load("chess.png"), (win_width, win_height)) # задаємо колір відповідно до колірної схеми RGB

#Створюємо групу для стін
barriers = sprite.Group()

monsters = sprite.Group()

#створюємо групу для куль
bullets = sprite.Group()

bonuses= sprite.Group()

bon_count=0

#Створюємо стіни картинки
#1-х, 2у, 3-довжина, 4-висота
w1 = GameSprite('wall1.png',156, 498, 390, 78)
w2 = GameSprite('wall2.png', 156, 576, 78, 576)
w3 = GameSprite('wall1.png',0, 294, 390, 78)
w4 = GameSprite('wall2.png', 546, 420, 78, 234)
w5 = GameSprite('wall2.png', 468, 0, 78, 234)
w6 = GameSprite('wall1.png',0, 78, 390, 78)
w7 = GameSprite('wall1.png',546, 78, 390, 78)
w8 = GameSprite('wall2.png', 780, 448, 78, 576)
w9 = GameSprite('wall1.png',1010, 498, 390, 78)
w10 = GameSprite('wall1.png',940, 342, 460, 78)

#додаємо стіни до групи
barriers.add(w1)
barriers.add(w2)
barriers.add(w3)
barriers.add(w4)
barriers.add(w5)
barriers.add(w6)
barriers.add(w7)
barriers.add(w8)
barriers.add(w9)
barriers.add(w10)

bonus1=GameSprite('money.png',0,0,80,80)
bonus2=GameSprite('money.png',0,150,80,80)
bonus3=GameSprite('money.png',550,0,80,80)
bonus4=GameSprite('money.png',1200,100,80,80)
bonus5=GameSprite('money.png',300,650,80,80)

bonuses.add(bonus1)
bonuses.add(bonus2)
bonuses.add(bonus3)
bonuses.add(bonus4)
bonuses.add(bonus5)



#створюємо спрайти
packman = Player('наггетс2.png', 20, win_height - 70, 70, 80, 0, 0)
monster = Enemy_h('наггетс39.png', win_width - 80, 250, 80, 80, 30, 400, 1400)
monster2 = Enemy_h('наггетс39.png', win_width - 80, 250, 80, 80, 50, 400, 1400)
monster3 = Enemy_v('наггетс39.png', win_width - 740, 100, 80, 80, 30, 100, 800)
monster4 = Enemy_v('наггетс39.png', win_width - 1010, 90, 80, 80, 20, 0, 400)
monster5 = Enemy_v('наггетс39.png', win_width - 400, 680, 80, 80, 50, 600, 800)
final_sprite = GameSprite('pizza.png', win_width - 85, win_height - 100, 80, 80)

#додаємо монстра до групи
monsters.add(monster)
monsters.add(monster2)
monsters.add(monster3)
monsters.add(monster4)
monsters.add(monster5)

#змінна, що відповідає за те, як закінчилася гра
finish = False
#ігровий цикл
run = True

mixer.init()
mixer.music.load('funky.mp3')
mixer.music.set_volume(0.02)
mixer.music.play(loops=6)
plop=mixer.Sound('plop.ogg')
plop.set_volume(0.4)
quack=mixer.Sound('quack.ogg')
quack.set_volume(0.4)
win=mixer.Sound('win.ogg')
win.set_volume(0.07)
lose=mixer.Sound('lose.ogg')
lose.set_volume(0.07)
money=mixer.Sound('money.ogg')
money.set_volume(0.07)
rich=mixer.Sound('rich.ogg')
rich.set_volume(0.2)
ding=mixer.Sound('ding.ogg')
ding.set_volume(0.07)

while run:
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -5
            elif e.key == K_RIGHT:
                packman.x_speed = 5
            elif e.key == K_UP :
                packman.y_speed = -5
            elif e.key == K_DOWN :
                packman.y_speed = 5
            elif e.key == K_SPACE:
                packman.fire()
                plop.play()
                quack.play()

 
        elif e.type == KEYUP:
            if e.key == K_LEFT :
                packman.x_speed = 0
            elif e.key == K_RIGHT:
                packman.x_speed = 0
            elif e.key == K_UP:
                packman.y_speed = 0
            elif e.key == K_DOWN:
                packman.y_speed = 0
    if not finish:
        #оновлюємо фон кожну ітерацію
        window.blit(back, (0, 0))#зафарбовуємо вікно кольором
        
        #запускаємо рухи спрайтів
        packman.update()
        bullets.update()

        #оновлюємо їх у новому місці при кожній ітерації циклу
        packman.reset()
        #рисуємо стіни 2
        bullets.draw(window)
        barriers.draw(window)
        bonuses.draw(window)
        final_sprite.reset()

        sprite.groupcollide(monsters, bullets, True, True)
        monsters.update()
        monsters.draw(window)
        sprite.groupcollide(bullets, barriers, True, False)

        if sprite.spritecollide(packman, bonuses, True):
            bon_count+=1
            ding.play()
            money.play()

        #Перевірка зіткнення героя з ворогом та стінами
        if sprite.spritecollide(packman, monsters, False):
            quack.play()
            lose.play()
            mixer.music.pause()
            finish = True
            img = image.load('lose.png')
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))

        if sprite.collide_rect(packman, final_sprite) and bon_count<5:
            win.play()
            mixer.music.pause()
            finish = True
            img = image.load('win.png')
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))

        if sprite.collide_rect(packman, final_sprite) and bon_count==5:
            rich.play()
            mixer.music.pause()
            finish = True
            img = image.load('rich.png')
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))


    
        #цикл спрацьовує кожну 0.05 секунд
        display.update()
