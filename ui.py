"""Game UI"""

import pygame
import numpy as np
import itertools
from pygame import gfxdraw

BOARD_BROWN = (180, 120, 40) # color for board
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BOARD_WIDTH = 750
BOARD_BORDER = 25
STONE_RADIUS = 15
GUIDE_DOT_RADIUS = 4

size = 19 # size of board
inc = (BOARD_WIDTH - 2 * BOARD_BORDER) / (size-1) # side of 1 box

def get_rgb(color):   
    if color == 'WHITE':
        return 255, 255, 255
    elif color == 'BLACK':
        return 0, 0, 0
    else:
        return 0, 133, 211 # color for hỉnt
   
# convert coordinates to intersections  
def xy_to_colrow(x, y, size):    
    x = x - BOARD_BORDER
    y = y - BOARD_BORDER
    col = int(round(x / inc))
    row = int(round(y/ inc))
    return col, row

# convert intersections to coordinates
def colrow_to_xy(col, row, size):    
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

    # vertical start points (constant y)
    xs = np.linspace(BOARD_BORDER, BOARD_WIDTH - BOARD_BORDER, size)
    ys = np.full((size), BOARD_BORDER)
    start_points += list(zip(xs, ys))

    # horizontal start points (constant x)
    xs = np.full((size), BOARD_BORDER)
    ys = np.linspace(BOARD_BORDER, BOARD_WIDTH - BOARD_BORDER, size)
    start_points += list(zip(xs, ys))

    # vertical end points (constant y) 
    xs = np.linspace(BOARD_BORDER, BOARD_WIDTH - BOARD_BORDER, size)
    ys = np.full((size), BOARD_WIDTH - BOARD_BORDER)
    end_points += list(zip(xs, ys))

    # horizontal end points (constant x)
    xs = np.full((size), BOARD_WIDTH - BOARD_BORDER)
    ys = np.linspace(BOARD_BORDER, BOARD_WIDTH - BOARD_BORDER, size)
    end_points += list(zip(xs, ys))

    return (start_points, end_points)


class UI:
    
    def __init__(self):
        self.start_points, self.end_points = make_grid(size)
        self.screen = None
        self.outline = pygame.Rect(BOARD_BORDER, BOARD_BORDER, BOARD_WIDTH - 2*BOARD_BORDER, BOARD_WIDTH - 2*BOARD_BORDER) #outline for main board

    def init_pygame(self):
        pygame.init()
        pygame.display.set_caption('GO Game by CND_NHH')
        self.screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_WIDTH))
        self.background = pygame.image.load('BACKGROUND.jpg').convert()
        self.ZOINK = pygame.mixer.Sound("wav/zoink.wav")
        self.CLICK = pygame.mixer.Sound("wav/click.wav")
        self.font = pygame.font.SysFont("arial", 30)

        # fill board and add gridlines 
        self.screen.fill(BOARD_BROWN)
        for start_point, end_point in zip(self.start_points, self.end_points):
            pygame.draw.line(self.screen, BLACK, start_point, end_point)

        # add guide dots - "star points" - don't affect to game play
        guide_dots = [3, size // 2, size - 4]
        for col, row in itertools.product(guide_dots, guide_dots):
            x, y = colrow_to_xy(col, row, size)
            gfxdraw.aacircle(self.screen, x, y, GUIDE_DOT_RADIUS, BLACK)
            gfxdraw.filled_circle(self.screen, x, y, GUIDE_DOT_RADIUS, BLACK)

        pygame.display.flip()
    
    # draw stone each turn
    def draw(self, point, color, size = STONE_RADIUS):
        color = get_rgb(color)
        self.CLICK.play() # sound of click
        pygame.draw.circle(self.screen, color, colrow_to_xy(point[0], point[1], size), size, 0)
        pygame.display.update()

    # remove a stone - draw a red stone (or red legal action in previous step)
    def remove(self, point, size):
        # blt = -inc/2 + BOARD_BORDER + point[0] * inc, -inc/2 + BOARD_BORDER + point[1] * inc  # top_left-conner point
        # area_rect = pygame.Rect(blt, (inc, inc))
        # self.screen.blit(self.background, blt, area_rect)
        # pygame.display.update()
        color = (255,0,0)  # Red
        pygame.draw.circle(self.screen, color, colrow_to_xy(point[0], point[1], size), size, 0)
        pygame.display.update()
    
    #save the image of the game
    def save_image(self, path_to_save):
        pygame.image.save(self.screen, path_to_save)
        
        

    



