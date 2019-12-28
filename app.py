"""pygame engine module"""
import pygame
from game import State

WIDTH = 200
HEIGHT = 400

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
GAME_CLOSED = False

state = State(WIDTH, HEIGHT)

while not GAME_CLOSED:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_CLOSED = True

    state.update(pygame.key.get_pressed())


    state.draw(screen)
    pygame.display.flip()
