#step 4
#Enemy cls
import pygame
class Enemy:
    def __init__(self):
        self.pos = [100,100]
        self.size = 40
        self.color = (255,0,0)#Red
        self.speed_x = 3
        self.speed_y =3
        self.rect = pygame.Rect(self.pos[0],self.pos[1],self.size,self.size)

    def move(self):
        self.rect.x +=self.speed_x
        self.rect.y +=self.speed_y


        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed_x *=-1
        if self.rect.top <0 or self.rect.bottom >screen_height:
            self.speed_y *=-1

    def draw(self,surface):
        pygame.draw.rect(surface,self.color,self.rect)

enemy =Enemy()
enemy.move()
enemy.draw(screen)
        
