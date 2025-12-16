import pygame
import random
import os #to handle file paths

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


#blue = (0,0,255)
#red = (255,0,0)
#yellow = (255,255,0)
black = (0,0,0)
white = (255,255,255)


clock = pygame.time.Clock()


def load_image(filename):
    filepath=os.path.join("assets","images",filename)
    try:
        if "background" in filename.lower():
            image = pygame.image.load(filepath).convert()
            
        else:
            image = pygame.image.load(filepath).convert_alpha()
        return image
    except pygame.error as e:
        print(f"Unable to load image {filename}:{e}")
        placeholder = pygame.Surface((50,50))
        placeholder.fill((255,0,255)) #if an assent is missing then ->magenta
        return placeholder
    
#loading background    
background_image = load_image("light-brown-free-solidcolor-background.jpg")

#update-player with more animation -no changes here
class Player:
    def __init__(self):
        #self.image = load_image("female_stand.png")
        #self.color = blue
        self.walk_frames = [load_image("female_walk1.png"),
                            load_image("female_walk2.png"),
            ]
        self.current_frame = 0
        self.image = self.walk_frames[self.current_frame]
        self.rect = self.image.get_rect(center =(screen_width//2, screen_height //2))
        self.speed = 5

        self.animation_time = 0
        self.animation_delay = 100

    #To handle animations
    def update(self,keys):
        self.animation_time +=clock.get_time()
        if self.animation_time >= self.animation_delay:
            self.animation_time = 0
            self.current_frame = (self.current_frame+1)% len(self.walk_frames)
            self.image = self.walk_frames[self.current_frame]
            self.rect = self.image.get_rect(center=self.rect.center)


    #def move(self,keys):
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
        #pygame.draw.rect(surface,self.color,self.rect)
        surface.blit(self.image,self.rect)

#update with animations - no changes here
class Enemy:
    def __init__(self):
        #self.image = load_image("zombie_kick.png")
        #self.rect = pygame.Rect((100,100),(40,40))
        #self.color = red
        self.walk_frames = [load_image("zombie_walk1.png"),
                            load_image("zombie_walk2.png"),
                
            ]
        self.current_frame = 0
        self.image = self.walk_frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=(100,100))
        self.speed_x = 3
        self.speed_y = 3

        self.animation_time = 0
        self.animation_delay = 200

    def update(self):
        self.animation_time +=clock.get_time()
        if self.animation_time >= self.animation_delay:
            self.animation_time = 0
            self.current_frame = (self.current_frame+1)% len(self.walk_frames)
            self.image = self.walk_frames[self.current_frame]
            self.rect = self.image.get_rect(center=self.rect.center)

    #def move(self):
        self.rect.x +=self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left <0 or self.rect.right > screen_width:
            self.speed_x *= -1
        if self.rect.top < 0 or self.rect.bottom > screen_height:
            self.speed_y *=-1

    def draw(self,surface):
        #pygame.draw.rect(surface,self.color,self.rect)
        surface.blit(self.image,self.rect)

        
class Coin: # - no changes here
    def __init__(self):
        #self.size = 25
        #self.color = yellow
        #self.rect = pygame.Rect((0,0),(self.size,self.size))
        self.image = load_image("coinGold.png")
        self.rect = self.image.get_rect()
        self.reset_position()

    def reset_position(self):
        self.rect.x = random.randint(0,screen_width - self.rect.width)#gives a random
        #num between 0 and screen_width - self.size
        self.rect.y = random.randint(0,screen_height - self.rect.height)


    def draw(self,surface):
        #pygame.draw.rect(surface,self.color,self.rect)
        surface.blit(self.image,self.rect)
        
player = Player()
enemy = Enemy()
coin = Coin()
score = 0
font = pygame.font.Font(None,36)

running = True
game_over = False


while running:
    
    dt = clock.tick(60) / 1000.0 # dt =time in seconds since last frame
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    if not game_over:
        keys = pygame.key.get_pressed()
        #player.move(keys)
        player.update(keys)
        enemy.update()
        #enemy.move()

        if player.rect.colliderect(enemy.rect):
            game_over = True

        if player.rect.colliderect(coin.rect):
            score +=10
            coin.reset_position()

    #screen.fill(black)
    screen.blit(background_image,(0,0))        
    player.draw(screen)
    enemy.draw(screen)
    coin.draw(screen)

    score_text = font.render(f"Score:{score}",True,white)
    screen.blit(score_text,(10,10))

    if game_over:
        game_over_text = font.render("GAME OVER! Press ESC to quit.", True, white)
        text_rect = game_over_text.get_rect(center = (screen_width//2,screen_height//2))
        screen.blit(game_over_text,text_rect)
        #blit = Block Image Transfer(paste this image/text onto the screen, at a certain position)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

    pygame.display.flip()
    #clock.tick(60)

pygame.quit()    
        






            
            
