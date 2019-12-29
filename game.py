from cell import Cell
import pygame
import random
import math
from enum import Enum
FIGURES = [
    [(-1, 0), (0, 0), (1, 0), (2, 0)],
    [(-1, 0), (0, 0), (1, 0), (0, 1)],
    [(0, 0),  (1, 0), (0, 1), (1, 1)],
    [(-1, 0), (0, 0), (0, 1), (1, 1)],
    [(-1, 0), (0, 0), (1, 0), (1, 1)]
]

class GameState(Enum):
    ANIMATION = 1
    ACTION = 2
    GAMEOVER = 3

class State:

    def __init__(self, screen_width, screen_height, enable_animations = True):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.game_state = GameState.ACTION
        
        self.width = 10
        self.height = 10
   
        self.animation_timer = 0
        self.row = screen_height//self.height
        self.col = screen_width//self.width
        self.grid = []
        self.figure = [[], (0, 0, 0)]
        self.next_figures_indexes = []
        self.generate_figure_indexes()
        # generate new figure
        self.new_figure()
        for y in range(self.row):
            row = []
            for x in range(self.col):
                row.append(Cell(x, y))
            self.grid.append(row)

        # for animation
        self.animated_rows = []
        self.enable_animations = enable_animations
       
    
    # This will clone the state, but without animations
    # IF NEEDED ADD CLONING OF THE ANIMATIONS
    def clone(self):
        state = State(self.screen_width, self.screen_height)
        for y in range(self.row):
            for x in range(self.col):
                state.grid[y][x].color = self.grid[y][x].color

        state.figure = [[x[:] for x in self.figure[0]], self.figure[1]]

        state.enable_animations = False
        state.next_figures_indexes = self.next_figures_indexes[:]

        return state

    def get_random_color(self):
        red = random.randint(100, 254)
        green = random.randint(100, 254)
        blue = random.randint(100, 254)
        return (red, green, blue)

    def multiply_matrix(self, a, b):
        matrix = []
        for k in range(len(a)):
            row = []
            for i in range(len(b)):
                value = 0
                for j in range(len(b)):
                    value += a[k][j] * b[j][i]
                row.append(value)
            matrix.append(row)
        return matrix


    def rotate_figure(self, figure):
        # trasformation matrix
        # [cosx  sinX 0]
        # [-sinX cosX 0]
        # [0     0    1]
        alpha = math.radians(90)
        move_transformation1 = [
            [1, 0, 0],
            [0, 1, 0],
            [-figure[0][0], -figure[0][1], 1]
        ]

        move_transformation2 = [
            [1, 0, 0],
            [0, 1, 0],
            [figure[0][0], figure[0][1], 1]
        ]

        rotation_transformation =  [
                           [math.cos(alpha)//1, math.sin(alpha)//1, 0],
                           [-math.sin(alpha)//1, math.cos(alpha)//1, 0],
                           [0, 0, 1]
                          ]
        finished_matrix = self.multiply_matrix(self.multiply_matrix(move_transformation1, rotation_transformation), move_transformation2)

        for i, point in enumerate(figure):
            coord_matrix = [[point[0], point[1], 1]]
            rotated_coords = self.multiply_matrix(coord_matrix, finished_matrix)
            figure[i] = [math.floor(rotated_coords[0][0]), math.floor(rotated_coords[0][1])]

        margin_of_error = self.get_figure_error(figure)
        for i in range(len(figure)):
            figure[i][0] += margin_of_error
        

    def get_figure_error(self, figure):
        best_move_x = 0
        for i, point in enumerate(figure):
            x = point[0]
            move_x = 0
            if x < 0:
                move_x = abs(x)
            elif x > self.col - 1:
                move_x = -(x - (self.col - 1))
            
            if abs(move_x) > abs(best_move_x):
                best_move_x = move_x

        return best_move_x
       

    def generate_figure_indexes(self):
        for i in range(3 - len(self.next_figures_indexes)):
            self.next_figures_indexes.append(random.randint(0, len(FIGURES) - 1))

    def get_figure_by_index(self, start_point, index):
        figure = []
        for figure_vector in FIGURES[index]:
            figure.append(([figure_vector[0] + start_point[0], figure_vector[1] + start_point[1]]))
        return figure
        
    def new_figure(self):
        if len(self.next_figures_indexes) == 0:
            print("BROKEN")
            return

        self.figure = None
        red = random.randint(100, 254)
        green = random.randint(100, 254)
        blue = random.randint(100, 254)
        self.figure = [[], (red, green, blue)]
        start_point = (self.col // 2, 0)
        rng_figure = FIGURES[self.next_figures_indexes[0]]
        for figure_vector in rng_figure:
            self.figure[0].append(([figure_vector[0] + start_point[0], figure_vector[1] + start_point[1]]))

        # delete first next_figures_indexes element
        self.next_figures_indexes.pop(0)
        # generetates more figures
        self.generate_figure_indexes()

    def is_valid(self, point):
        return point[0] >= 0 and point[0] <= self.col - 1 and point[1] >= 0 and point[1] <= self.row - 1  

    def add_gravity(self, figure):
        for i in range(len(figure)):
            figure[i][1] += 1

    def move_figure(self, figure, delta_x):
        if sum(int(not self.is_valid([x[0] + delta_x, x[1]])) or not self.grid[x[1]][x[0]+ delta_x].is_free() for x in figure) == 0:
            for i in range(len(figure)):
                figure[i][0] += delta_x
    

    def change_or_keep(self, new_figure_pos):
        if self.is_figure_valid(new_figure_pos):
            self.figure[0] = new_figure_pos
        else:
            self.place_figure()
    
    def get_end_figure(self, figure):
        while True:
            clone_figure = [x[:] for x in figure]
            self.add_gravity(clone_figure)
            if self.is_figure_valid(clone_figure):
                figure = clone_figure
            else:
                break
        return figure


    def resolve_finished_rows(self):
        for y in range(self.row):
            if sum([int(self.grid[y][x].is_free()) for x in range(self.col)]) == 0:
                # destroy this row and lower everythin above this
                self.animated_rows.append(y)

        # change gamestate to animation
        if len(self.animated_rows) > 0:
            if self.enable_animations:
                self.game_state = GameState.ANIMATION
                self.animation_timer = 4 * len(self.animated_rows)
            else:
                self.destory_animated_rows()

    
    def place_figure(self):
        for pt in self.figure[0]:
            self.grid[pt[1]][pt[0]].color = self.figure[1][:]
            # generate new figure
        # check if the row has been completed
        # if so, lower the game down
        self.resolve_finished_rows()

        self.new_figure()

    def is_figure_valid(self, figure):
        for new_pt in figure:
            if not self.is_valid(new_pt) or not self.grid[new_pt[1]][new_pt[0]].is_free():                
                return False
        return True
  
    def destory_animated_rows(self):
        for erase_row in self.animated_rows:    
            for cell in self.grid[erase_row]:
                cell.clear_cell()
            for y2 in reversed(range(1, erase_row+1)):
                for cell in self.grid[y2]:
                    cell.color = self.grid[y2 - 1][cell.x].color
        self.animated_rows = []
  
    def animate(self):
        for animate_row in self.animated_rows:
            color = self.get_random_color()
            for cell in self.grid[animate_row]:
                cell.color = color
        
        self.animation_timer-=1
        if self.animation_timer <= 0:
        # destroy animated rows and create new figure
            self.destory_animated_rows()
            self.game_state = GameState.ACTION             

    def update(self, keys):
        if self.game_state is GameState.ANIMATION:
            # animate
            self.animate()
            return


        if len(self.figure[0]) == 0:
            self.new_figure()
    
        new_figure_pos = [x[:] for x in self.figure[0]]
        # add gravity to the figure
        self.add_gravity(new_figure_pos)

        delta_x = 0
        if keys[pygame.K_a]:
            delta_x += -1
        if keys[pygame.K_d]:
            delta_x += 1

        self.move_figure(new_figure_pos, delta_x)
        # check if this figure is intersecting anything
        self.change_or_keep(new_figure_pos)
        new_figure_pos = [x[:] for x in self.figure[0]]
        if keys[pygame.K_w]:
            self.rotate_figure(new_figure_pos)
            self.figure[0] = new_figure_pos
                
        if keys[pygame.K_s]:
            self.figure[0] = self.get_end_figure(self.figure[0])
        

 
  
    def draw(self, window, relative_position=(0, 0)):
        for y in range(self.row):
            for x in range(self.col):
                pygame.draw.rect(window, self.grid[y][x].color, pygame.Rect(x * self.width + relative_position[0], y * self.height + relative_position[1], self.width, self.height))
        
              # draw future figure for referece for the player
        for pt in self.get_end_figure(self.figure[0]):
            pygame.draw.rect(window, (220, 220, 220), pygame.Rect(pt[0] * self.width + relative_position[0], pt[1] * self.height + relative_position[1], self.width, self.height), 1)
   
        # draw the figure
        for pt in self.figure[0]:
            if self.is_valid(pt):
                pygame.draw.rect(window, self.figure[1], pygame.Rect(pt[0] * self.width + relative_position[0], pt[1] * self.height + relative_position[1], self.width, self.height))
   
    def draw_next_figures(self, window, relative_position=(0,0)):
        y_pos = 0
        for index in self.next_figures_indexes:
            figure = self.get_figure_by_index((0, y_pos), index)
            for pt in figure:
                pygame.draw.rect(window, (0, 255, 0), pygame.Rect(pt[0] * self.width + relative_position[0], pt[1] * self.height + relative_position[1], self.width, self.height))
   
            y_pos += 3