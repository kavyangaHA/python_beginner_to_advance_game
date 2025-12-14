#step 3
#creating a cls for the player

import pygame

blue = (0,0,255)
class Player:
    def __init__(self):
        self.pos = [400,300]
        self.speed = 5
        self.size = 50
        self.color = blue
        self.rect = pygame.Rect(self.pos[0],self.pos[1],self.size,self.size)

    def move(self,keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -=self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x +=self.speed
        if keys[pygame.K_UP]:
            self.rect.y -=self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y +=self.speed

        if self.rect.left <0:
            self.rect.x = 0
        if self.rect.right > screen_width:
            self.rect.x = screen_width - self.size
        if self.rect.top < 0:
            self.rect.y = 0
        if self.rect.bottom > screen_height:
            self.rect.y = screen_height - self.size
    def draw(self,surface):
        pygame.draw.rect(surface,self.color,self.rect)

player = Player()

keys = pygame.key.get_pressed()
player.move(keys)

player.draw(screen)

            
        


