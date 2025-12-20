import pygame
import random
import os  # to handle file paths

pygame.init()

pygame.mouse.set_visible(False)



pygame.mixer.init()
pygame.mixer.music.load(os.path.join("assets","sounds","game-gaming-minecraft-background-music-379533.mp3"))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

coin_sound = pygame.mixer.Sound(os.path.join("assets","sounds","90s-game-ui-6-185099.mp3"))
game_over_sound = pygame.mixer.Sound(os.path.join("assets","sounds","8-bit-video-game-lose-sound-version-1-145828.mp3"))
zombie_collide_sound = pygame.mixer.Sound(os.path.join("assets","sounds","forceField_000.ogg")) 

# Screen setup
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My First Game")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

# Clock for controlling frame rate
clock = pygame.time.Clock()


# --- Asset Loading ---
def load_image(filename):
    filepath = os.path.join("assets", "images", filename)
    try:
        if "background" in filename.lower():
            image = pygame.image.load(filepath).convert()
        else:
            image = pygame.image.load(filepath).convert_alpha()
        return image
    except pygame.error as e:
        print(f"Unable to load image {filename}: {e}")
        placeholder = pygame.Surface((50, 50))
        placeholder.fill((255, 0, 255))  # if an asset is missing -> magenta
        return placeholder

# Load background
background_image = load_image("light-brown-free-solidcolor-background.jpg")

#loadd button images
button_normal_image = load_image("button_square_depth_flat.png")
button_hover_image = load_image("button_square_depth_gradient.png")

#load cursor image
cursor_image = load_image("cursorHand_beige.png")##

#load hearts
heart_full_image = load_image("hud_heartFull.png")
heart_empty_image = load_image("hud_heartEmpty.png")

# --- Game Object Classes ---

# Player class with corrected update logic
class Player:
    def __init__(self):
        self.walk_frames = [
            load_image("female_walk1.png"),
            load_image("female_walk2.png"),
        ]
        self.current_frame = 0
        self.image = self.walk_frames[self.current_frame]
        self.rect = self.image.get_rect(center=(screen_width // 2, screen_height // 2))
        self.speed = 5
        self.animation_time = 0
        self.animation_delay = 100
        self.max_lives=3 #num of max lives
        self.lives = self.max_lives  #start with max lives
        self.invincibility_timer = 0
        
    #Combined animation and movement into one update method
    def update(self, keys):
        # Handle animation
        self.animation_time += clock.get_time()
        if self.animation_time >= self.animation_delay:
            self.animation_time = 0
            self.current_frame = (self.current_frame + 1) % len(self.walk_frames)
            self.image = self.walk_frames[self.current_frame]
            # Important: Update the rect if the new image has a different size
            self.rect = self.image.get_rect(center=self.rect.center)
        if self.invincibility_timer > 0:
            self.invincibility_timer -= clock.get_time()

        # Handle movement
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Boundary checks
        if self.rect.left < 0:
            self.rect.x = 0
        if self.rect.right > screen_width:
            self.rect.x = screen_width - self.rect.width
        if self.rect.top < 0:
            self.rect.y = 0
        if self.rect.bottom > screen_height:
            self.rect.y = screen_height - self.rect.height

    def draw(self, surface):
        #surface.blit(self.image, self.rect)
        if (self.invincibility_timer <= 0) or (self.invincibility_timer % 200 < 100): #blink every 100ms
            surface.blit(self.image,self.rect)



# Enemy class with update logic
class Enemy:
    def __init__(self):
        self.walk_frames = [
            load_image("zombie_walk1.png"),
            load_image("zombie_walk2.png"),
        ]
        self.current_frame = 0
        self.image = self.walk_frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=(100, 100))
        self.speed_x = 3
        self.speed_y = 3
        self.animation_time = 0
        self.animation_delay = 200

    # Combined animation and movement into one update method
    def update(self):
        # Handle animation
        self.animation_time += clock.get_time()
        if self.animation_time >= self.animation_delay:
            self.animation_time = 0
            self.current_frame = (self.current_frame + 1) % len(self.walk_frames)
            self.image = self.walk_frames[self.current_frame]
            self.rect = self.image.get_rect(center=self.rect.center)

        # Handle movement
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed_x *= -1
        if self.rect.top < 0 or self.rect.bottom > screen_height:
            self.speed_y *= -1

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Coin:
    def __init__(self):
        self.image = load_image("coinGold.png")
        self.rect = self.image.get_rect()
        self.reset_position()

    def reset_position(self):
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(0, screen_height - self.rect.height)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
#New
class Button:
    def __init__(self,x,y,width,height,text,font,image_normal,image_hover):
        self.rect = pygame.Rect(x,y,width,height)
        self.text = text
        self.font = font
        
        self.image_normal = pygame.transform.scale(image_normal,(width,height))
        self.image_hover = pygame.transform.scale(image_hover,(width,height))
        self.image = self.image_normal
        
        self.is_hovered = False

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.image = self.image_hover
            self.is_hovered = True
        else:
            self.image = self.image_normal
            self.is_hovered = False

    def draw(self, surface):
        surface.blit(self.image,self.rect)
        text_surface = self.font.render(self.text, True,black) #Munu texts
        text_rect = text_surface.get_rect(center = self.rect.center)
        surface.blit(text_surface,text_rect)

    def is_clicked(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
            return False
            
        


# Define fonts here so they are accessible
title_font = pygame.font.Font(None, 74)
info_font = pygame.font.Font(None, 36)

# Define game states
MENU = "MENU"
PLAYING = "PLAYING"
GAME_OVER = "GAME_OVER"

# Set the initial state
game_state = MENU

# Initialize score and font here
score = 0
player_lives = 3


new_game_button = Button(screen_width / 2 - 100,screen_height/2  - 30,200,50,
                         "New Game",info_font,button_normal_image,button_hover_image)

quit_button = Button(screen_width / 2 - 100,screen_height/2  + 30,200,50,
                         "Quit Game",info_font,button_normal_image,button_hover_image)






# Create game objects
player = Player()
enemy = Enemy()
coin = Coin()

# Function to reset the game
def reset_game():
    global player, enemy, coin, score,player_lives
    player = Player()
    enemy = Enemy()
    coin = Coin()
    score = 0
    #player_lives = 3,now we have define max_lives in player cls ,so no need of this

# --- REVISED: Main Game Loop ---
running = True
while running:
    # Event handling (always check for quit)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == MENU:
            if new_game_button.is_clicked(event):
                game_state = PLAYING
                reset_game()
                
            if quit_button.is_clicked(event):
                running = False

        elif game_state == GAME_OVER:
            if new_game_button.is_clicked(event):
                game_state = PLAYING
                reset_game()
            if quit_button.is_clicked(event):
                running = False
            
    # --- Game State Logic ---
    #  The if/elif structure is now flat, not nested
    if game_state == MENU:
        # Draw the menu screen
        screen.blit(background_image, (0, 0))###Menu background

        title_text = title_font.render("The Annoying Zombie", True, white)
        title_rect = title_text.get_rect(center=(screen_width / 2, screen_height / 3))
        screen.blit(title_text, title_rect)

        new_game_button.update()
        quit_button.update()
        new_game_button.draw(screen)
        quit_button.draw(screen)

        #draw the cursor
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(cursor_image, (mouse_x - 16, mouse_y -16))        


##        start_text = info_font.render("Press SPACE to Start the Game", True, white)
##        start_rect = start_text.get_rect(center=(screen_width / 2, screen_height / 2))
##        screen.blit(start_text, start_rect)

        # Check for input to start the game
##        keys = pygame.key.get_pressed()
##        if keys[pygame.K_SPACE]:
##            game_state = PLAYING
##            reset_game()  # Reset the game for a new start

    elif game_state == PLAYING:
        # This is the game logic
        keys = pygame.key.get_pressed()
        player.update(keys)
        enemy.update()

        if player.rect.colliderect(enemy.rect) and player.invincibility_timer <=0:
            player.lives -=1
            player.invincibility_timer = 2000 # 20000 miliseconds= 2s
            zombie_collide_sound.play()
            if player.lives <=0: 
                game_state = GAME_OVER
                game_over_sound.play()

        if player.rect.colliderect(coin.rect):
            score += 10
            coin.reset_position()
            coin_sound.play()

        # Drawing

        screen.blit(background_image, (0, 0))
        player.draw(screen)
        enemy.draw(screen)
        coin.draw(screen)
        lives_text = info_font.render(f"Lives: {player.lives}",True,white)
        screen.blit(lives_text,(10,50))

        score_text = info_font.render(f"Score: {score}", True, white)
        screen.blit(score_text, (10, 10))

        #Draw the lives (hearts)
        #first draw the empty hearts for total possible lives
        for i in range(player.max_lives):
            screen.blit(heart_empty_image,(75+1.5*i*35,45))

        #Then top of the empty hearts, draw the remaining lives(full hearts) that player has
        for i in range(player.lives):
            screen.blit(heart_full_image,(75+1.5*i*35,45))
        

    elif game_state == GAME_OVER:
        # Draw the game over screen
        screen.blit(background_image, (0, 0))

        game_over_text = title_font.render("GAME OVER", True, (255, 0, 0),black)
        over_rect = game_over_text.get_rect(center=(screen_width / 2, screen_height / 3))
        screen.blit(game_over_text, over_rect)

        final_score_text = info_font.render(f"Final Score: {score}", True, white)
        score_rect = final_score_text.get_rect(center=(screen_width / 2, screen_height / 2))
        screen.blit(final_score_text, score_rect)

        new_game_button.update()
        quit_button.update()
        new_game_button.draw(screen)
        quit_button.draw(screen)


        #draw the cursor
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(cursor_image, (mouse_x - 16, mouse_y -16))        

##        restart_text = info_font.render("Press SPACE for Menu, ESC to Quit", True, white)
##        restart_rect = restart_text.get_rect(center=(screen_width / 2, screen_height / 2 + 50))
##        screen.blit(restart_text, restart_rect)

        # Check for input to restart or quit
##        keys = pygame.key.get_pressed()
##        if keys[pygame.K_SPACE]:
##            game_state = MENU  # CORRECTED: Fixed typo from game_sate to game_state
##        if keys[pygame.K_ESCAPE]:
##            running = False

    #  These two lines are now at the end of the main loop,
    # so they run every frame regardless of the game state.

   # mouse_x, mouse_y = pygame.mouse.get_pos()
    #screen.blit(cursor_image, (mouse_x - 16, mouse_y -16))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
