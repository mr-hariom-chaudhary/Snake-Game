import pygame
import random
import os

pygame.mixer.init()
pygame.init()

# Colors
white = (255,255,255)
red = (255,0,0)
black = (0,0,0)
green = (0,255,0)

# Creating Game Window
screen_width = 700
screen_height = 500
gameWindow = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Snake Game")
pygame.display.update()
clock = pygame.time.Clock()

# BackGround Image
strt_img = pygame.image.load("bg_image.webp")
strt_img = pygame.transform.scale(strt_img,(screen_width,screen_height)).convert_alpha()

# Adding Fonts
font = pygame.font.SysFont(None,40)

 # Adding Score To Game
def text_screen(text,color,x,y):
    screen_text = font.render(text,True,color)
    gameWindow.blit(screen_text,[x,y])

# Increase Snake Length
def plot_snake(gameWindow,color,snk_list,snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow,color,[x,y,snake_size,snake_size])

# Adding Game Start Image
def welcome():
    exit_Game = False
    while not exit_Game:
        wlc_img = pygame.image.load("snk_start_img.png")
        wlc_img = pygame.transform.scale(wlc_img,(screen_width,screen_height)).convert_alpha()
        gameWindow.blit(wlc_img, (0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_Game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameloop()

        clock.tick(30)
    pygame.quit()
    quit()

# Creating Game Loop
def gameloop():
    # Game Specific Variable
    exit_Game = False
    game_Over = False
    snake_x = 45
    snake_y = 55
    snake_size = 20
    fps = 30
    velocity_x = 0
    velocity_y = 0
    init_velocity = 4
    food_x = random.randint(20,screen_width//2)
    food_y = random.randint(20,screen_height//2)
    food_radius = 10
    score = 0
    snk_list = []
    snk_len = 1
    
# Reading HighScore
    if(not os.path.exists('High_Score.txt')):
        with open ('High_Score.txt', 'w') as f:
            f.write("0")
    with open("High_Score.txt","r") as f:
        High_Score = f.read()

    while not exit_Game:
        if game_Over:
            with open("High_Score.txt","w") as f:
                f.write(str(High_Score))
            exit_img = pygame.image.load("exit_img.png")
            exit_img = pygame.transform.scale(exit_img,(screen_width,screen_height)).convert_alpha()
            gameWindow.blit(exit_img, (0, 0))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_Game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        gameloop()

        else:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_Game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0
                    
                    # Cheat Code
                    if event.key == pygame.K_h:
                        score += 5
                    
            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x - food_x)<12 and abs(snake_y - food_y)<12:
                pygame.mixer.music.load('eat.mp3')
                pygame.mixer.music.play()
                score += 1
                food_x = random.randint(20,screen_width-20 - food_radius * 2)
                food_y = random.randint(20,screen_height-20 - food_radius * 2)
                snk_len += 5
                if score > int(High_Score):
                    High_Score = score

            gameWindow.fill(white)
            gameWindow.blit(strt_img,(0,0))
            text_screen ("Score : "+str(score) + "  High_Score : "+str(High_Score),red,5,5)
            pygame.draw.circle(gameWindow,red,(food_x + food_radius,food_y + food_radius),food_radius)

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_len:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_Over = True
                pygame.mixer.music.load('end_game.mp3')
                pygame.mixer.music.play()

            # Snake Over Logic
            if snake_x < 0 or snake_x>screen_width - snake_size or snake_y<0 or snake_y>screen_height-snake_size:
                game_Over = True
                pygame.mixer.music.load('end_game.mp3')
                pygame.mixer.music.play()
            plot_snake(gameWindow,green,snk_list,snake_size)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()
    
welcome()
gameloop()