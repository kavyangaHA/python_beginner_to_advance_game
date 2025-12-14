#step 2

import pygame
pygame.init()
clock = pygame.time.Clock()


#screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("My Very First Game")

#colors
blue = (0,0,255)
player_pos = [400,300] #w,h
player_speed = 5 #kalin eke 0.5 damme clock ek set krl thibbe nathi nis

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #closing the window ,still there is no
                                      #any other quit option              
            running = False

    keys = pygame.key.get_pressed()
    player_rect = pygame.Rect(player_pos[0],player_pos[1],50,50)
    if keys[pygame.K_LEFT]:
        player_pos[0] -=player_speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] +=player_speed
    if keys[pygame.K_UP]:
        player_pos[1] -=player_speed
    if keys[pygame.K_DOWN]:
        player_pos[1] += player_speed


    if player_rect.left <0:
        player_pos[0] = 0
    if player_rect.right > screen_width:
        player_pos[0] = screen_width -50#bcs player's width is 50
    if player_rect.top <0:
        player_pos[1] = 0
    if player_rect.bottom > screen_height:
        player_pos[1] = screen_height - 50

    screen.fill((0,0,0))
    pygame.draw.rect(screen,blue,(player_pos[0],player_pos[1],50,50))

    pygame.display.flip()
    clock.tick(60)#without this our game runs as same fast as our pc,
pygame.quit()    

            
