import pygame
import math, random,sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
screenWidth = 288
screenHeight = 512
gameWindow = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Flappy Bird")

# Load assets
gameOver_overlay = pygame.image.load("Assets/UI/gameover.png")
bg = pygame.image.load("Assets/Game Objects/homeBg.png")
bird_down = pygame.image.load("Assets/Game Objects/yellowbird-downflap.png")
bird_up = pygame.image.load("Assets/Game Objects/yellowbird-upflap.png")
base = pygame.image.load("Assets/Game Objects/base.png")
welcome_overlay = pygame.image.load("Assets/UI/overlay.png")
pipe_img = pygame.image.load("Assets/Game Objects/pipe-green.png")
pipe_flipped = pygame.transform.flip(pipe_img, False, True)
my_font = pygame.font.Font(r"Assets\Text\rr.ttf", 35)
point= pygame.mixer.Sound("Assets\Sound Efects\point.wav")
hit = pygame.mixer.Sound("Assets/Sound Efects/hit.wav")
die = pygame.mixer.Sound("Assets\Sound Efects\die.ogg")
wing = pygame.mixer.Sound("Assets/Sound Efects/wing.wav")
# Resize background to fit height
bg_width = bg.get_width()
bg = pygame.transform.scale(bg, (bg_width, screenHeight))

# Global constants
bird_x = 85
JUMP_STRENGTH = -8
GRAVITY = 0.5
MAX_FALL_SPEED = 10
pipe_gap = 110
pipe_velocity = 4
panels = math.ceil(screenWidth / bg_width) + 2
clock = pygame.time.Clock()

# Pipe logic
def create_pipe():
    pipe_height = random.randint(100, 300)
    bottom_pipe = pipe_img.get_rect(midtop=(screenWidth + 50, pipe_height + pipe_gap))
    top_pipe = pipe_flipped.get_rect(midbottom=(screenWidth + 50, pipe_height))
    return top_pipe, bottom_pipe

def gameloop():
    bird_y = 250
    Y_VELOCITY = 0
    scroll = 0
    game_state = "welcome"
    gameOver = False
    pipe_list = list(create_pipe())
    score = 0
    gameOverSoundPlayed = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if game_state == "welcome":
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                   
                        game_state = "playing"
                        Y_VELOCITY = JUMP_STRENGTH
                elif game_state == "playing":
                    if event.key == pygame.K_SPACE:
                        pygame.mixer.Sound.play(wing)
                        Y_VELOCITY = JUMP_STRENGTH

        # Draw background
        for i in range(panels):
            gameWindow.blit(bg, (i * bg_width + scroll - bg_width, 0))

        if game_state == "playing" and not gameOver:
            scroll -= 1
            if abs(scroll) > bg_width:
                scroll = 0

            Y_VELOCITY += GRAVITY
            if Y_VELOCITY > MAX_FALL_SPEED:
                Y_VELOCITY = MAX_FALL_SPEED
            bird_y += Y_VELOCITY

            for pipe in pipe_list:
                pipe.centerx -= pipe_velocity

            if pipe_list[0].centerx < -50:
                pipe_list = pipe_list[2:]
                pipe_list.extend(create_pipe())
                score += 1
                pygame.mixer.Sound.play(point)

        # Draw pipes
        for i, pipe in enumerate(pipe_list):
            if i % 2 == 0:
                gameWindow.blit(pipe_flipped, pipe)
            else:
                gameWindow.blit(pipe_img, pipe)

        # Bird display
        if Y_VELOCITY < 0:
            bird_rect = bird_up.get_rect(center=(bird_x, bird_y))
            gameWindow.blit(bird_up, bird_rect)
        else:
            bird_rect = bird_down.get_rect(center=(bird_x, bird_y))
            gameWindow.blit(bird_down, bird_rect)

        # Welcome overlay
        if game_state == "welcome":
            overlay_rect = welcome_overlay.get_rect(center=(screenWidth // 2, screenHeight // 2))
            gameWindow.blit(welcome_overlay, overlay_rect)

        # Base
        base_rect = base.get_rect(midbottom=(screenWidth // 2, screenHeight))
        gameWindow.blit(base, base_rect)

        # Collision detection
        if bird_rect.colliderect(base_rect):
            gameOver = True
            Y_VELOCITY = 0
            bird_y = base_rect.top - bird_rect.height // 2

        if bird_y <= 0:
            bird_y = 0
            gameOver = True
            Y_VELOCITY = 0
            if not gameOverSoundPlayed:
              pygame.mixer.Sound.play(die)
              gameOverSoundPlayed = True   
        for pipe in pipe_list:
            if bird_rect.colliderect(pipe):
                
                gameOver = True
        text_surface = my_font.render(str(score), False,(255,255,255 ))
        gameWindow.blit(text_surface,  [screenWidth /2-10, screenHeight /2 -250])
        if gameOver:
         overlay_rect = gameOver_overlay.get_rect(center=(screenWidth // 2, screenHeight // 2))
         gameWindow.blit(gameOver_overlay, overlay_rect)
         if not gameOverSoundPlayed:
              pygame.mixer.Sound.play(die)
              gameOverSoundPlayed = True     
         pygame.mixer.pause()
         pygame.display.update()
         pygame.time.delay(1000) 
         print("Congrats, Your Score is: "+str(score))
         sys.exit()
         

        pygame.display.update()
        clock.tick(65)

    pygame.quit()
    quit()

# Run the game
gameloop()
