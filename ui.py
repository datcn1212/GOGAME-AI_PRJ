"""Game UI"""

import pygame
import numpy as np
import collections
import itertools
from pygame import gfxdraw

BOARD_BROWN = (180, 120, 40) # color for board
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BOARD_WIDTH = 750
BOARD_BORDER = 75
STONE_RADIUS = 12
DOT_RADIUS = 4

TURN_POS = (BOARD_BORDER, 20)
SCORE_POS = (BOARD_BORDER, BOARD_WIDTH - BOARD_BORDER + 30)

def get_rbg(color):   
    if color == 'WHITE':
        return 255, 255, 255
    elif color == 'BLACK':
        return 0, 0, 0
    else:
        return 0, 133, 211
   
# convert coordinates to intersections  
def xy_to_colrow(x, y, size):    
    inc = (BOARD_WIDTH - 2 * BOARD_BORDER) / (size - 1) # side of 1 box
    x_dist = x - BOARD_BORDER
    y_dist = y - BOARD_BORDER
    col = int(round(x_dist / inc))
    row = int(round(y_dist / inc))
    return col, row

# convert intersections to coordinates
def colrow_to_xy(col, row, size):    
    inc = (BOARD_WIDTH - 2 * BOARD_BORDER) / (size - 1)
    x = int(BOARD_BORDER + col * inc)
    y = int(BOARD_BORDER + row * inc)
    return x, y
  
# create start and end point to draw gridlines  
def make_grid(size):
    """Return list of (start_point, end_point pairs) defining gridlines

    Args:
        size (int): size of grid

    Returns:
        Tuple[List[Tuple[float, float]]]: start and end points for gridlines
    """    
    start_points, end_points = [], []

    # vertical start points (constant y) : 19 diem nam o duoi cung
    xs = np.linspace(BOARD_BORDER, BOARD_WIDTH - BOARD_BORDER, size)
    ys = np.full((size), BOARD_BORDER)
    start_points += list(zip(xs, ys))

    # horizontal start points (constant x) : 19 diem nam o canh trai
    xs = np.full((size), BOARD_BORDER)
    ys = np.linspace(BOARD_BORDER, BOARD_WIDTH - BOARD_BORDER, size)
    start_points += list(zip(xs, ys))

    # vertical end points (constant y) : 19 diem nam o tren cung
    xs = np.linspace(BOARD_BORDER, BOARD_WIDTH - BOARD_BORDER, size)
    ys = np.full((size), BOARD_WIDTH - BOARD_BORDER)
    end_points += list(zip(xs, ys))

    # horizontal end points (constant x) : 19 diem nam o canh phai
    xs = np.full((size), BOARD_WIDTH - BOARD_BORDER)
    ys = np.linspace(BOARD_BORDER, BOARD_WIDTH - BOARD_BORDER, size)
    end_points += list(zip(xs, ys))

    return (start_points, end_points)

class UI:
    
    def __init__(self, size):
        self.size = size
        self.start_points, self.end_points = make_grid(self.size)

    def init_pygame(self):
        pygame.init()
        screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_WIDTH))
        self.screen = screen
        self.ZOINK = pygame.mixer.Sound("wav/zoink.wav")
        self.CLICK = pygame.mixer.Sound("wav/click.wav")
        self.font = pygame.font.SysFont("arial", 30)
      
     
    def clear_screen(self): 
        
        # fill board and add gridlines 
        self.screen.fill(BOARD_BROWN)
        for start_point, end_point in zip(self.start_points, self.end_points):
            pygame.draw.line(self.screen, BLACK, start_point, end_point)

        # add guide dots
        guide_dots = [3, self.size // 2, self.size - 4]
        for col, row in itertools.product(guide_dots, guide_dots):
            x, y = colrow_to_xy(col, row, self.size)
            gfxdraw.aacircle(self.screen, x, y, DOT_RADIUS, BLACK)
            gfxdraw.filled_circle(self.screen, x, y, DOT_RADIUS, BLACK)

        pygame.display.flip()
    
    #save the image of the game
    def save_image(self, path_to_save):
        pygame.image.save(self.screen, path_to_save)


