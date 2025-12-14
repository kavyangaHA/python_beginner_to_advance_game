#step 1
import pygame
pygame.init()

#screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("My Very First Game")

#colors
blue = (0,0,255)
player_pos = [400,300]
player_speed = 0.5

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #closing the window ,still there is no
                                      #any other quit option              
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -=player_speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] +=player_speed
    if keys[pygame.K_UP]:
        player_pos[1] -=player_speed
    if keys[pygame.K_DOWN]:
        player_pos[1] += player_speed

    screen.fill((0,0,0))
    pygame.draw.rect(screen,blue,(player_pos[0],player_pos[1],50,50))

    pygame.display.flip()
pygame.quit()    

            
