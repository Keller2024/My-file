#Создай собственный Шутер!
from pygame import *
from random import randint

score = 0 #сбито кораблей
goal = 10#столько кораблей нужно сбить для победы
lost = 0#пропущено кораблей
max_lost = 3#проиграли, если пропустили столько

#класс-родитель для спрайтов
class GameSprite(sprite.Sprite):
   #конструктор класса
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
      super().__init__()
      # каждый спрайт должен хранить свойство image - изображение
      self.image = transform.scale(image.load(player_image), (size_x, size_y))
      self.speed = player_speed
      # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
      self.rect = self.image.get_rect()
      self.rect.x = player_x
      self.rect.y = player_y

   def reset(self):
      window.blit(self.image, (self.rect.x, self.rect.y))

#класс-наследник для спрайта-игрока (управляется стрелками)
class Player(GameSprite):
   def update(self):
      keys = key.get_pressed()
      if keys[K_LEFT] and self.rect.x > 5:
         self.rect.x -= self.speed
      if keys[K_RIGHT] and self.rect.x < win_width - 80:
         self.rect.x += self.speed
   #метод выстрел
   def fire(self):
      bullet = Bullet('diamond_picax.png', self.rect.centerx, self.rect.top, 15, 20, -15)
      bullets.add(bullet)

#класс-наследник для спрайта-врага (перемещается сам)
class Enemy(GameSprite):
   def update(self):
      self.rect.y += self.speed
      global lost
      #исчезает если дойдёт до края экрана
      if self.rect.y > win_height:
         self.rect.x = randint(80, win_width - 80)
         self.rect.y = 0
         lost = lost + 1

#класс спрайта-пули
class Bullet(GameSprite):
   def update(self):
      self.rect.y < 0
   #исчезает если дойдёт до края экрана
      if self.rect.y < 0:
         self.kill()

#Игровая сцена:
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = transform.scale(image.load("mine.png"), (win_width, win_height))
lost = 0

#создаём группы спрайтов-врагов
monsters = sprite.Group()
for i in range(1, 6):
   monster = Enemy('zombi.png', randint(80, win_width - 80), -40, 80, 50, randint(1,5))
   monsters.add(monster)
bullets = sprite.Group()

#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False

#основной цикл игры:
run = True#флаг сбрасывается кнопкой закрытия окна
while run:
   #событие нажатия на кнопку Закрыть
   for e in event.get():
      if e.type == QUIT:
         run = False

      #событие нажатия на пробел - спрайт стреляет
      elif e.type == KEYDOWN:
         if e.key == K_SPACE:
            fire_sound.play()
            ship.fire()

#сама игра: действия спрайтов, проверка правил игры, перерисовка
   if not finish:
      #обновляем фон
      window.blit(background,(0,0))

score = 0 #сбито кораблей
lost = 0 #пропущено кораблей

#Персонажи игры:
player = Player('Steve.png', 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
   monster = Enemy('zombi.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
   monsters.add(monster)

#музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

#шрифты и надписи
font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN', True, (255, 255, 255))
lose = font1.render('YOU LOSE', True, (180, 0, 0))

font2 = font.SysFont('Arial', 36)

game = True
finish = False
clock = time.Clock()
FPS = 60

while game:
   for e in event.get():
      if e.type == QUIT:
         game = False
  
   if finish != True:

      window.blit(background,(0, 0))
      
      text = font2.render('Счёт:' + str(score), 1, (255, 255, 255))
      window.blit(text, (10, 20))

      text_lose = font2.render('Пропущено:' + str(lost), 1, (255, 255, 255))
      window.blit(text_lose, (10, 50))

      player.update()
      monster.update()

      player.reset()
      monster.reset()

   monsters.draw(window)

   display.update()
   clock.tick(FPS)
   