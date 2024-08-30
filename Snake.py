# type: ignore
import pygame 
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 795
HEIGHT = 605
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Snake properties
SNAKE_SIZE = 20

# Score
best_score = 0

# Game speed
SPEED = 15

# Font
font = pygame.font.SysFont('arial', 35)

def init_game():
    global snake_pos, snake_body, direction, change_to, food_pos, food_spawn, score, game_over_flag
    snake_pos = [100, 50]
    snake_body = [[100, 50], [80, 50], [60, 50]]
    direction = 'RIGHT'
    change_to = direction
    food_pos = generate_food_position()
    food_spawn = True
    score = 0
    game_over_flag = False

def generate_food_position():
    return [random.randrange(0, WIDTH // SNAKE_SIZE) * SNAKE_SIZE,
            random.randrange(0, HEIGHT // SNAKE_SIZE) * SNAKE_SIZE]

def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render(f'Score : {score}', True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (WIDTH/10, 15)
    else:
        score_rect.midtop = (WIDTH/2, HEIGHT/1.25)
    win.blit(score_surface, score_rect)

def show_best_score():
    best_font = pygame.font.SysFont('arial', 25)
    best_surface = best_font.render(f'Best : {best_score}', True, WHITE)
    best_rect = best_surface.get_rect()
    best_rect.topright = (WIDTH - 10, 10)
    win.blit(best_surface, best_rect)

def game_over():
    global best_score, game_over_flag
    if score > best_score:
        best_score = score
    game_over_flag = True
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render('Your Score was : ' + str(score), True, RED)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (WIDTH/2, HEIGHT/4)
    win.fill(BLACK)
    win.blit(game_over_surface, game_over_rect)
    show_best_score()
    restart_font = pygame.font.SysFont('arial', 25)
    restart_surface = restart_font.render('Press SPACE to restart', True, WHITE)
    restart_rect = restart_surface.get_rect()
    restart_rect.midtop = (WIDTH/2, HEIGHT/2)
    win.blit(restart_surface, restart_rect)
    pygame.display.flip()

# Initialize game
init_game()
clock = pygame.time.Clock()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
            if event.key == pygame.K_SPACE and game_over_flag:
                init_game()

    if not game_over_flag:
        # Validate direction
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Move the snake
        if direction == 'UP':
            snake_pos[1] -= SNAKE_SIZE
        if direction == 'DOWN':
            snake_pos[1] += SNAKE_SIZE
        if direction == 'LEFT':
            snake_pos[0] -= SNAKE_SIZE
        if direction == 'RIGHT':
            snake_pos[0] += SNAKE_SIZE

        # Snake body growing mechanism
        snake_body.insert(0, list(snake_pos))
        
        # Check if snake has eaten the food
        if abs(snake_pos[0] - food_pos[0]) < SNAKE_SIZE and abs(snake_pos[1] - food_pos[1]) < SNAKE_SIZE:
            score += 1
            food_pos = generate_food_position()
        else:
            snake_body.pop()

        # Draw background
        win.fill(BLACK)

        # Draw snake
        for pos in snake_body:
            pygame.draw.rect(win, GREEN, pygame.Rect(pos[0], pos[1], SNAKE_SIZE, SNAKE_SIZE))

        # Draw food
        pygame.draw.rect(win, RED, pygame.Rect(food_pos[0], food_pos[1], SNAKE_SIZE, SNAKE_SIZE))

        # Game Over conditions
        if snake_pos[0] < 0 or snake_pos[0] >= WIDTH or snake_pos[1] < 0 or snake_pos[1] >= HEIGHT:
            game_over()
        for block in snake_body[1:]:
            if snake_pos == block:
                game_over()

        show_score(1, WHITE, 'consolas', 20)
        show_best_score()
        pygame.display.update()
        clock.tick(SPEED)
    else:
        game_over()

    pygame.display.update()
