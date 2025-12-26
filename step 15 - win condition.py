import pygame
import random
import os

pygame.init()
pygame.mouse.set_visible(False)

pygame.mixer.init()
pygame.mixer.music.load(os.path.join("assets", "sounds", "game-gaming-minecraft-background-music-379533.mp3"))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)




coin_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "90s-game-ui-6-185099.mp3"))
game_over_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "8-bit-video-game-lose-sound-version-1-145828.mp3"))
zombie_collide_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "forceField_000.ogg"))

# Screen setup
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("The Annoying Zombie")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)


HIGH_SCORE_FILE = "highscore.txt"
high_score = 0

# Clock for controlling frame rate
clock = pygame.time.Clock()

def load_high_score():
    global high_score
    try:
        with open(HIGH_SCORE_FILE,"r") as f:
            high_score = int(f.read())

    except FileNotFoundError:
        high_score = 0#if the file is not exist,the high_score =0
    except ValueError:
        high_score = 0

def save_high_score(score):
    global high_score
    if score > high_score:
        high_score = score
        with open(HIGH_SCORE_FILE,'w') as f:
            f.write(str(high_score))
            


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
        placeholder.fill((255, 0, 255))
        return placeholder

load_high_score()


background_image = load_image("light-brown-free-solidcolor-background.jpg")
button_normal_image = load_image("button_square_depth_flat.png")
button_hover_image = load_image("button_square_depth_gradient.png")
cursor_image = load_image("cursorHand_beige.png")
heart_full_image = load_image("hud_heartFull.png")
heart_empty_image = load_image("hud_heartEmpty.png")

# --- Game Object Classes ---

# Player class
class Player:
    def __init__(self):
        self.walk_frames = [load_image("female_walk1.png"), load_image("female_walk2.png")]
        self.current_frame = 0
        self.image = self.walk_frames[self.current_frame]
        self.rect = self.image.get_rect(center=(screen_width // 2, screen_height // 2))
        self.speed = 5
        self.animation_time = 0
        self.animation_delay = 100
        self.max_lives = 3
        self.lives = self.max_lives
        self.invincibility_timer = 0

    def update(self, keys):
        self.animation_time += clock.get_time()
        if self.animation_time >= self.animation_delay:
            self.animation_time = 0
            self.current_frame = (self.current_frame + 1) % len(self.walk_frames)
            self.image = self.walk_frames[self.current_frame]
            self.rect = self.image.get_rect(center=self.rect.center)
        if self.invincibility_timer > 0:
            self.invincibility_timer -= clock.get_time()

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        self.rect.clamp_ip(screen.get_rect()) # A simpler way to keep player on screen

    def draw(self, surface):
        if (self.invincibility_timer <= 0) or (self.invincibility_timer % 200 < 100):
            surface.blit(self.image, self.rect)

# Enemy class
class Enemy:
    def __init__(self):
        self.walk_frames = [load_image("zombie_walk1.png"),
                            load_image("zombie_walk2.png")]
        self.current_frame = 0
        self.image = self.walk_frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=(100, 100))
        self.speed_x = random.choice([-3, 3])
        self.speed_y = random.choice([-3, 3])
        self.animation_time = 0
        self.animation_delay = 200

    def update(self):
        self.animation_time += clock.get_time()
        if self.animation_time >= self.animation_delay:
            self.animation_time = 0
            self.current_frame = (self.current_frame + 1) % len(self.walk_frames)
            self.image = self.walk_frames[self.current_frame]
            self.rect = self.image.get_rect(center=self.rect.center)

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed_x *= -1
        if self.rect.top < 0 or self.rect.bottom > screen_height:
            self.speed_y *= -1

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Coin class
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

# Button class
class Button:
    def __init__(self, x, y, width, height, text, font, image_normal, image_hover):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.image_normal = pygame.transform.scale(image_normal, (width, height))
        self.image_hover = pygame.transform.scale(image_hover, (width, height))
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
        surface.blit(self.image, self.rect)
        text_surface = self.font.render(self.text, True, black)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

# --- NEW: Fire class for obstacles ---
class Fire:
    def __init__(self, x, y):
        self.image = load_image("tochLit2.png") # Make sure you have this image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 4 # Added speed attribute

    def update(self):
        self.rect.y += self.speed # Move the fire down

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# --- Game State Management ---
title_font = pygame.font.Font(None, 74)
info_font = pygame.font.Font(None, 36)

# --- REVISED: Define game states ---
MENU = "MENU"
LEVEL_SELECT = "LEVEL_SELECT" # NEW STATE
PLAYING = "PLAYING"
GAME_OVER = "GAME_OVER"
WIN ="WIN"
# Set the initial state
game_state = MENU

# Variables for level management
current_level = "Beginner"
enemies = []
fires = []

# --- REVISED: Create buttons for all menus ---
# Main Menu Buttons
new_game_button = Button(screen_width / 2 - 100, screen_height / 2 - 30, 200, 50,
                         "New Game", info_font, button_normal_image, button_hover_image)
quit_button = Button(screen_width / 2 - 100, screen_height / 2 + 40, 200, 50,
                    "Quit", info_font, button_normal_image, button_hover_image)

# Level Select Buttons
beginner_button = Button(screen_width / 2 - 100, screen_height / 2 - 80, 200, 50,
                         "Beginner", info_font, button_normal_image, button_hover_image)
intermediate_button = Button(screen_width / 2 - 100, screen_height / 2 - 20, 200, 50,
                             "Intermediate", info_font, button_normal_image, button_hover_image)
hard_button = Button(screen_width / 2 - 100, screen_height / 2 + 40, 200, 50,
                    "Hard", info_font, button_normal_image, button_hover_image)
back_button = Button(50, screen_height - 80, 150, 50,
                     "Back", info_font, button_normal_image, button_hover_image)

# Game objects
player = Player()
coin = Coin()
score = 0
COINS_TO_WIN = 6
# --- CORRECTED: reset_game function now uses the 'level' argument ---
def reset_game(level):
    global player, enemies, fires, coin, score, current_level
    current_level = level # CRITICAL FIX: Use the level passed to the function
    player = Player()
    coin = Coin()
    score = 0
    enemies = []
    fires = []

    # --- Setup based on the chosen level ---
    if current_level == "Beginner":
        enemies.append(Enemy())
    elif current_level == "Intermediate":
        enemies.append(Enemy())
        enemies.append(Enemy())
        fires.append(Fire(300, 400))
        fires.append(Fire(500, 200))
    elif current_level == "Hard":
        enemies.append(Enemy())
        enemies.append(Enemy())
        enemies.append(Enemy())
        # Fire rain will be handled in the main loop

# --- Main Game Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # --- REVISED: Event handling for each state ---
        if game_state == MENU:
            if new_game_button.is_clicked(event):
                game_state = LEVEL_SELECT
            if quit_button.is_clicked(event):
                running = False

        elif game_state == LEVEL_SELECT:
            if beginner_button.is_clicked(event):
                game_state = PLAYING
                reset_game("Beginner")
            if intermediate_button.is_clicked(event):
                game_state = PLAYING
                reset_game("Intermediate")
            if hard_button.is_clicked(event):
                game_state = PLAYING
                reset_game("Hard")
            if back_button.is_clicked(event):
                game_state = MENU

        elif game_state == GAME_OVER:
            # Using buttons for game over options
            if new_game_button.is_clicked(event): # Re-using as "Play Again"
                game_state = LEVEL_SELECT # Go to level select, not directly to game
            if quit_button.is_clicked(event): # Re-using as "Main Menu"
                #game_state = MENU
                running = False

    # --- REVISED: Game State Logic for drawing ---
    if game_state == MENU:
        screen.blit(background_image, (0, 0))
        title_text = title_font.render("The Annoying Zombie", True, white)
        title_rect = title_text.get_rect(center=(screen_width / 2, screen_height / 3))
        screen.blit(title_text, title_rect)

        high_score_text = info_font.render(f"High Score:{high_score}",True,white)
        high_score_rect = high_score_text.get_rect(center=(screen_width/2,screen_height/3))
        screen.blit(title_text,title_rect)

        new_game_button.update()
        new_game_button.draw(screen)
        quit_button.update()
        quit_button.draw(screen)

        mouse_x, mouse_y = pygame.mouse.get_pos()##
        screen.blit(cursor_image, (mouse_x - 16, mouse_y -16)) ##

    elif game_state == LEVEL_SELECT:
        screen.blit(background_image, (0, 0))
        title_text = title_font.render("Select Level", True, white)
        title_rect = title_text.get_rect(center=(screen_width / 2, screen_height / 4))
        screen.blit(title_text, title_rect)

        beginner_button.update()
        beginner_button.draw(screen)
        intermediate_button.update()
        intermediate_button.draw(screen)
        hard_button.update()
        hard_button.draw(screen)
        back_button.update()
        back_button.draw(screen)

        mouse_x, mouse_y = pygame.mouse.get_pos() ##
        screen.blit(cursor_image, (mouse_x - 16, mouse_y -16)) ##

    elif game_state == PLAYING:
        keys = pygame.key.get_pressed()
        player.update(keys)

        # Handle Fire Rain for Hard mode
        if current_level == "Hard":
            if random.randint(1, 60) == 1: # 1 in 60 chance each frame
                fire_x = random.randint(0, screen_width - 50)
                fires.append(Fire(fire_x, -50))

        # Update all game objects
        for enemy in enemies:
            enemy.update()
        for fire in fires[:]: # Use a slice copy to safely remove items while iterating
            fire.update()
            if fire.rect.top > screen_height:
                fires.remove(fire)

        # Check for collisions
        for enemy in enemies:
            if player.rect.colliderect(enemy.rect) and player.invincibility_timer <= 0:
                player.lives -= 1
                player.invincibility_timer = 2000
                zombie_collide_sound.play()
                if player.lives <= 0:
                    game_state = GAME_OVER
                    game_over_sound.play()

        for fire in fires:
            if player.rect.colliderect(fire.rect) and player.invincibility_timer <= 0:
                player.lives -= 1
                player.invincibility_timer = 2000
                zombie_collide_sound.play()
                if player.lives <= 0:
                    game_state = GAME_OVER
                    game_over_sound.play()

        if player.rect.colliderect(coin.rect):
            score += 10
            coin.reset_position()
            coin_sound.play()
            
        if score/10 >= COINS_TO_WIN:
            game_state = 'WIN'
        
        # Drawing
        screen.blit(background_image, (0, 0))
        player.draw(screen)
        coin.draw(screen)
        for fire in fires:
            fire.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)

        # Draw UI
        score_text = info_font.render(f"Score: {score}", True, white)
        screen.blit(score_text, (10, 10))

        # --- CORRECTED: Heart drawing with integer coordinates ---
        for i in range(player.max_lives):
            screen.blit(heart_empty_image, (int(10 + 1.5 * i * 35), 45))
        for i in range(player.lives):
            screen.blit(heart_full_image, (int(10 + 1.5 * i * 35), 45))

    elif game_state == WIN:
        
        screen.blit(background_image,(0,0))##
        win_text = title_font.render("YOU WIN",True,(0,255,0))
        win_rect = win_text.get_rect(center=(screen_width/2,screen_height/3))
        screen.blit(win_text,win_rect)
        
        play_again_text = info_font.render("Play Again", True, black)
        play_again_rect = play_again_text.get_rect(center=new_game_button.rect.center)
        screen.blit(play_again_text, play_again_rect)

        new_game_button.update()
        new_game_button.draw(screen)
        quit_button.update()
        quit_button.draw(screen)
        
        if new_game_button.is_clicked(event):
            save_high_score(score)
            game_state = LEVEL_SELECT

        if quit_button.is_clicked(event):
            save_high_score(score)
            running = False

        mouse_x, mouse_y = pygame.mouse.get_pos()##
        screen.blit(cursor_image, (mouse_x - 16, mouse_y -16)) ##
        



    elif game_state == GAME_OVER:
        screen.blit(background_image, (0, 0))
        # --- CORRECTED: game_over_text.render() had an extra argument ---
        game_over_text = title_font.render("GAME OVER", True, (255, 0, 0))
        over_rect = game_over_text.get_rect(center=(screen_width / 2, screen_height / 3))
        screen.blit(game_over_text, over_rect)

        final_score_text = info_font.render(f"Final Score: {score}", True, white)
        score_rect = final_score_text.get_rect(center=(screen_width / 2, screen_height / 2))
        screen.blit(final_score_text, score_rect)

        # Draw buttons to restart or quit
        play_again_text = info_font.render("Play Again", True, black)
        play_again_rect = play_again_text.get_rect(center=new_game_button.rect.center)
        screen.blit(play_again_text, play_again_rect)

        main_menu_text = info_font.render("Main Menu", True, black)
        main_menu_rect = main_menu_text.get_rect(center=quit_button.rect.center)
        screen.blit(main_menu_text, main_menu_rect)

        new_game_button.update()
        quit_button.update()
        new_game_button.draw(screen)
        quit_button.draw(screen)
        
    if new_game_button.is_clicked(event):
        save_high_score(score)
        game_state = LEVEL_SELECT
    if quit_button.is_clicked(event):
        save_high_score(score)
        running = False

        
        

        mouse_x, mouse_y = pygame.mouse.get_pos()##
        screen.blit(cursor_image, (mouse_x - 16, mouse_y -16)) ##

    # Draw the custom cursor last so it's on top
    #mouse_x, mouse_y = pygame.mouse.get_pos()
    #screen.blit(cursor_image, (mouse_x - 16, mouse_y - 16))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
