import pygame
import random

pygame.init()


#important -in pygame coordinates are llike below
'''
(0,0) ─────────────> x(+)
  |
  |
  |
  v
  y(+)
'''



screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("My First Game")


blue = (0,0,255)
red = (255,0,0)
yellow = (255,255,0)
black = (0,0,0)
white = (255,255,255)


clock = pygame.time.Clock()


class Player:
    def __init__(self):
        self.rect = pygame.Rect((screen_width/2, screen_height /2),(50,50))
        self.color = blue
        self.speed = 5


    def move(self,keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -=self.speed #rect.x = x-position of the topleft corner
        if keys[pygame.K_RIGHT]:
            self.rect.x +=self.speed
        if keys[pygame.K_UP]:
            self.rect.y -=self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y +=self.speed

        #boundray
        if self.rect.left < 0:
            self.rect.x = 0
        if self.rect.right > screen_width:
            self.rect.x = screen_width - self.rect.width
        if self.rect.top <0:
            self.rect.y = 0
        if self.rect.bottom > screen_height:
            self.rect.y = screen_height - self.rect.height 

    def draw(self,surface):
        pygame.draw.rect(surface,self.color,self.rect)


class Enemy:
    def __init__(self):
        self.rect = pygame.Rect((100,100),(40,40))
        self.color = red
        self.speed_x = 3
        self.speed_y = 3

    def move(self):
        self.rect.x +=self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left <0 or self.rect.right > screen_width:
            self.speed_x *= -1
        if self.rect.top < 0 or self.rect.bottom > screen_height:
            self.speed_y *=-1

    def draw(self,surface):
        pygame.draw.rect(surface,self.color,self.rect)
        
class Coin:
    def __init__(self):
        self.size = 25
        self.color = yellow
        self.rect = pygame.Rect((0,0),(self.size,self.size))
        self.reset_position()

    def reset_position(self):
        self.rect.x = random.randint(0,screen_width - self.size)#gives a random
        #num between 0 and screen_width - self.size
        self.rect.y = random.randint(0,screen_height - self.size)


    def draw(self,surface):
        pygame.draw.rect(surface,self.color,self.rect)

player = Player()
enemy = Enemy()
coin = Coin()
score = 0
font = pygame.font.Font(None,36)

running = True
game_over = False


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    if not game_over:
        keys = pygame.key.get_pressed()
        player.move(keys)

        enemy.move()

        if player.rect.colliderect(enemy.rect):
            game_over = True

        if player.rect.colliderect(coin.rect):
            score +=10
            coin.reset_position()

    screen.fill(black)
    player.draw(screen)
    enemy.draw(screen)
    coin.draw(screen)

    score_text = font.render(f"Score:{score}",True,white)
    screen.blit(score_text,(10,10))

    if game_over:
        game_over_text = font.render("GAME OVER! Press ESC to quit.", True, white)
        text_rect = game_over_text.get_rect(center = (screen_width/2,screen_height/2))
        screen.blit(game_over_text,text_rect)
        #blit = Block Image Transfer(paste this image/text onto the screen, at a certain position)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()    
        






            
            
