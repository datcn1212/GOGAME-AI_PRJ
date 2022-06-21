"""
    main file to play match
"""
from config import * 
from util import *

if __name__ == "__main__":
    
    board_size = 19

    g = Game(size = board_size)
    g.init_pygame()
    g.clear_screen()
    g.draw()

    while True:
        g.update()
        pygame.time.wait(100)