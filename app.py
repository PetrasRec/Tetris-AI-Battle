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

state = State(GAME_WIDTH, GAME_HEIGHT)

while not GAME_CLOSED:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_CLOSED = True

    state.update(pygame.key.get_pressed())

    screen.fill((0,0,0))
    state.draw(screen)
    state.draw(screen, (200, 0))
    state.draw_next_figures(screen, (420, HEIGHT / 2))
    pygame.display.flip()
