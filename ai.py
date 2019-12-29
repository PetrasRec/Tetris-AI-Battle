from game import State
import pygame


# returns dictionary of keys, if it's true, the the key needs to be pressed
def get_next_move(state: State) -> dict:

    givenState = state.clone(False) 

    keys = dict()
    
    return keys


def simulate(state: State):
    while True:
        # Try to go left in every possible scenario and the right
            keys = dict()
            # Every possible key combination
            keys[pygame.K_a] = False
            keys[pygame.K_d] = False
            keys[pygame.K_w] = False
            keys[pygame.K_s] = False
