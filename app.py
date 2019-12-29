"""pygame engine module"""
import pygame
from game import State

WIDTH = 500
HEIGHT = 400


GAME_WIDTH = 200
GAME_HEIGHT = 400

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
GAME_CLOSED = False

state = State(GAME_WIDTH, GAME_HEIGHT, True)

while not GAME_CLOSED:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_CLOSED = True

    
    # UPDATE THE GAME BASED ON USER INPUT
    state.update(pygame.key.get_pressed())

    # CLEAR THE GAME SCREEN
    screen.fill((0, 0, 0))

    # DRAW STATE TO THE LEFT
    state.draw(screen)
    # DRAW SAME STATE TO THE RIGHT
    # TODO : In the future when battle mode is activated, change this!
    state.draw(screen, (200, 0))

    # Draws next figures and displays them to the right of the screen
    state.draw_next_figures(screen, (420, HEIGHT / 2))

    pygame.display.flip()
    