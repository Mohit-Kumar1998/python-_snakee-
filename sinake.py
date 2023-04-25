import pygame
import speech_recognition as sr

# initialize Pygame
pygame.init()

# set up the game window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game with Voice Control")

# set up the snake
snake_block_size = 10
snake_speed = 15
snake_list = []
snake_length = 1
snake_x = screen_width / 2
snake_y = screen_height / 2

# set up the food
food_x = round((screen_width / 2) / 10.0) * 10.0
food_y = round((screen_height / 2) / 10.0) * 10.0

# set up the font
font_style = pygame.font.SysFont(None, 50)

# initialize the speech recognition system
r = sr.Recognizer()
mic = sr.Microphone()

# function to display the score
def show_score(score):
    score_text = font_style.render("Score: " + str(score), True, pygame.Color('black'))
    screen.blit(score_text, [0, 0])

# function to draw the snake
def draw_snake(snake_block_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, pygame.Color('green'), [x[0], x[1], snake_block_size, snake_block_size])

# function to detect collisions with the food
def check_food_collision(snake_x, snake_y, food_x, food_y):
    if snake_x == food_x and snake_y == food_y:
        return True
    else:
        return False

# function to display the message
def message(msg, color):
    msg_text = font_style.render(msg, True, color)
    screen.blit(msg_text, [screen_width / 6, screen_height / 3])

# main game loop
def game_loop():
    # set up the initial direction of the snake
    direction = "right"
    change_to = direction

    # set up the initial score
    score = 0

    # set up the initial state of the game
    game_over = False

    while not game_over:
        # detect voice commands
        with mic as source:
            print("Say something!")
            audio = r.listen(source)
            try:
                command = r.recognize_google(audio)
                print("You said: " + command)
                if command == "up":
                    change_to = "up"
                elif command == "down":
                    change_to = "down"
                elif command == "left":
                    change_to = "left"
                elif command == "right":
                    change_to = "right"
            except sr.UnknownValueError:
                pass

        # update the direction of the snake based on user input
        if change_to == "up" and direction != "down":
            direction = "up"
        elif change_to == "down" and direction != "up":
            direction = "down"
        elif change_to == "left" and direction != "right":
            direction = "left"
        elif change_to == "right" and direction != "left":
            direction = "right"

        # update the position of the snake
        if direction == "up":
            snake_y -= snake_block_size
        elif direction == "down":
            snake_y += snake_block_size
        elif direction == "left":
            snake_x -= snake_block_size
        elif direction == "right":
            snake_x += snake_block_size

    # check for collisions with the edge of the game window
    if snake_x < 0 or snake_x >= screen_width or snake_y < 0 or snake_y >= screen_height:
        game_over = True

    # check for collisions with the snake's own body
    head = []
    head.append(snake_x)
    head.append(snake_y)
    snake_list.append(head)
    if len(snake_list) > snake_length:
        del snake_list[0]

    for x in snake_list[:-1]:
        if x == head:
            game_over = True

    # check for collisions with the food
    if check_food_collision(snake_x, snake_y, food_x, food_y):
        food_x = round((screen_width / 2) / 10.0) * 10.0
        food_y = round((screen_height / 2) / 10.0) * 10.0
        snake_length += 1
        score += 10

    # clear the screen
    screen.fill(pygame.Color('white'))

    # draw the snake and the food
    draw_snake(snake_block_size, snake_list)
    pygame.draw.rect(screen, pygame.Color('red'), [food_x, food_y, snake_block_size, snake_block_size])

    # display the score
    show_score(score)

    # update the screen
    pygame.display.update()

    # set up the game clock
    clock = pygame.time.Clock()
    clock.tick(snake_speed)

# display the game over message and wait for the user to quit
message("Game over! Press Q to quit or C to play again.", pygame.Color('red'))
pygame.display.update()
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                quit()
            elif event.key == pygame.K_c:
                game_loop()

game_loop()