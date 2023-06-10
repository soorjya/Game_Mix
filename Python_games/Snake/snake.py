import random
import pygame
import sys
from pygame.locals import *

FPS = 15
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
CELL_SIZE = 20
CELL_WIDTH = int(WINDOW_WIDTH / CELL_SIZE)
CELL_HEIGHT = int(WINDOW_HEIGHT / CELL_SIZE)

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BACKGROUND_COLOR = (0, 0, 0)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
HEAD = 0

def main():
    global FPS_CLOCK, DISPLAY_SURFACE, FONT

    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    FONT = pygame.font.Font('dlxfont.ttf', 12)
    pygame.display.set_caption('Snake')

    show_start_screen()
    while True:
        run_game()
        show_game_over_screen()

def run_game():
    x = 12
    y = 12
    snake_coords = [{'x': x, 'y': y}, {'x': x - 1, 'y': y}, {'x': x - 2, 'y': y}]
    direction = RIGHT
    food = generate_food_position()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        if (snake_coords[HEAD]['x'] == -1 or snake_coords[HEAD]['x'] == CELL_WIDTH or
                snake_coords[HEAD]['y'] == -1 or snake_coords[HEAD]['y'] == CELL_HEIGHT):
            return
        for body in snake_coords[1:]:
            if body['x'] == snake_coords[HEAD]['x'] and body['y'] == snake_coords[HEAD]['y']:
                return

        if (snake_coords[HEAD]['x'] == food['x'] and snake_coords[HEAD]['y'] == food['y']):
            food_sound = pygame.mixer.Sound('food_sound.wav')
            food_sound.play()
            food = generate_food_position()
        else:
            del snake_coords[-1]

        if direction == UP:
            new_head = {'x': snake_coords[HEAD]['x'], 'y': snake_coords[HEAD]['y'] - 1}
        elif direction == DOWN:
            new_head = {'x': snake_coords[HEAD]['x'], 'y': snake_coords[HEAD]['y'] + 1}
        elif direction == LEFT:
            new_head = {'x': snake_coords[HEAD]['x'] - 1, 'y': snake_coords[HEAD]['y']}
        elif direction == RIGHT:
            new_head = {'x': snake_coords[HEAD]['x'] + 1, 'y': snake_coords[HEAD]['y']}

        snake_coords.insert(0, new_head)
        DISPLAY_SURFACE.fill(BACKGROUND_COLOR)
        draw_snake(snake_coords)
        draw_food(food)
        draw_score(len(snake_coords) - 3)
        pygame.display.update()
        FPS_CLOCK.tick(FPS)

def draw_snake(coords):
    for coord in coords:
        x = coord['x'] * CELL_SIZE
        y = coord['y'] * CELL_SIZE
        snake_segment = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(DISPLAY_SURFACE, GREEN, snake_segment)

def draw_food(coord):
    x = coord['x'] * CELL_SIZE
    y = coord['y'] * CELL_SIZE
    food_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(DISPLAY_SURFACE, RED, food_rect)

def draw_score(score):
    score_text = FONT.render('Points: %s' % score, True, WHITE)
    score_rect = score_text.get_rect()
    score_rect.topleft = (WINDOW_WIDTH - 625, 450)
    DISPLAY_SURFACE.blit(score_text, score_rect)

def terminate():
    pygame.quit()
    sys.exit()

def generate_food_position():
    return {'x': random.randint(0, CELL_WIDTH - 1), 'y': random.randint(0, CELL_HEIGHT - 1)}

def show_start_screen():
    img = pygame.image.load('start_screen.png')
    img_x = 165
    img_y = 100

    while True:
        draw_information()

        if is_key_pressed():
            pygame.event.get()
            return
        pygame.display.update()
        DISPLAY_SURFACE.blit(img, (img_x, img_y))
        FPS_CLOCK.tick(FPS)

def draw_information():
    draw_text('Press any key to play', WINDOW_WIDTH / 2, 275)
    draw_text('Press Esc to quit', WINDOW_WIDTH / 2, 300)
    

def draw_text(text, x, y):
    text_obj = FONT.render(text, True, WHITE)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    DISPLAY_SURFACE.blit(text_obj, text_rect)

def is_key_pressed():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    key_up_events = pygame.event.get(KEYUP)
    if len(key_up_events) == 0:
        return None
    if key_up_events[0].key == K_ESCAPE:
        terminate()
    return key_up_events[0].key

def show_game_over_screen():
    game_over_font = pygame.font.Font('dlxfont.ttf', 45)
    game_over_text = game_over_font.render('Game Over!', True, WHITE)
    game_over_rect = game_over_text.get_rect()
    game_over_rect.midtop = (330, 50)

    DISPLAY_SURFACE.blit(game_over_text, game_over_rect)
    draw_information()
    pygame.display.update()
    pygame.time.wait(500)
    is_key_pressed()

    while True:
        if is_key_pressed():
            pygame.event.get()
            return

main()
