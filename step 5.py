#step 5
#class coin
import pygame
import random

class Coin:
    def __init__(self):
        self.size = 25
        self.color = (255,255,0)#Yellow

        self.pos = [random.randint(0,screen_width - self.size),random.randint(0,screen_height - self.size)]
        self.rect = pygame.Rect(self.pos[0],self.pos[1],self.size,self.size)


        def draw(self,surface):
            pygame.draw.rect(surface,self.color,self.rect)


import random
coin=Coin()
score = 0
font = pygame.font.Font(None,36)


if player.rect.colliderect(coin.rect):
    score+=10
    coin = Coin()

score_text = font.render(f"Score: {score}",True,(255,255,255))
screen.blit(score_text,(10,10))

coin.draw(screen)
