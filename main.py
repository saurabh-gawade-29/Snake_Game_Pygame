import os
import pygame
import random


# Add Music
pygame.mixer.init()

# Init()  need to implement every time
pygame.init()

# Colors
purple = (233, 210, 229)
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

# Creating a Window for game
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

#Background Image
bgimg = pygame.image.load("snake.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

# Game Title
pygame.display.set_caption("Snake Game 1998")
pygame.display.update()

# Create a Clock
clock = pygame.time.Clock()

# Font - we use system font here
font = pygame.font.SysFont(None, 55)


# Display score on screen
def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    # Blit: built-in function of pygame
    gameWindow.blit(screen_text, [x, y])


# plotting snake and increase length of snake
def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])


# Welcome Screen
def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill(purple)
        text_screen("Welcome to Snakes", black, 260, 250)
        text_screen("Press Space Bar To Play", black, 232, 290)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # pygame.mixer.music.load('back.mp3')
                    # pygame.mixer.music.play()
                    game_loop()

        pygame.display.update()
        clock.tick(60)


# Creating a game loop
def game_loop():

    # Game Specific Variable
    exit_game = False
    game_over = False
    # snake position and size - game specific variable
    snake_x = 45
    snake_y = 55
    # Size of snake
    snake_size = 30
    # Food for snake
    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)
    # FPS - Frames per second
    fps = 60
    # Score
    score = 0
    # HighScore
    with open("hiscore.txt", "r") as f:
        hiscore = f.read()
    # Give velocity for automatic movement
    init_velocity = 5
    velocity_x = 0
    velocity_y = 0

    #  List use for increase length
    snk_list = []
    snk_length = 1

    # if hi score is not present in users comp
    if not os.path.exists("hiscore.txt"):
        with open("hiscore.txt", "w") as f:
            f.write("0")

    while not exit_game:
        if game_over:
            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))
            gameWindow.fill(purple)
            text_screen("Game Over! Please Enter to continue", red, 100, 250)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:

            for event in pygame.event.get():
                # print(event)
                # if we want to close directly from ( X ) BUTTON IN WINDOW WE NEED TO WRITE BELOW LINE
                if event.type == pygame.QUIT:
                    exit_game = True

                # TODO: keydown: its built in constant for keypress from keyboard
                # TODO: we need to set velocity_x and velocity_y as zero so our snake not move diagonally
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_q:
                        score += 10

            # Velocity Logic for automatic movement
            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x) < 6 and (snake_y - food_y) < 6:
                score += 10
                # display score on cli
                # print("SCORE: ", score * 10)
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snk_length += 5
                if score > int(hiscore):
                    hiscore = score

            gameWindow.fill(purple)
            gameWindow.blit(bgimg, (0, 0))
            text_screen("Score: " + str(score) + "  Hiscore: " + str(hiscore), red, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                # pygame.mixer.music.load('gameover.mp3')
                # pygame.mixer.music.play()

            if head in snk_list[:-1]:
                game_over = True
                # pygame.mixer.music.load('gameover.mp3')
                # pygame.mixer.music.play()

            plot_snake(gameWindow, black, snk_list, snake_size)
        pygame.display.update()
        # tick is clock method we need to defined clock for this
        clock.tick(fps)

    # after Loop completion
    pygame.quit()
    quit()


welcome()