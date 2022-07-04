"""Main file to play match"""

import pygame
import time
import sys

from config_main import *
from ui import *
from agent.basic_agent import *
from agent.alpha_beta import *
#from agent.rl_agent import *
from os.path import join

class Match:
    
    def __init__(self, black_agent = None, white_agent = None, gui = True, dir_save=None):
        """
        BLACK always has the first move on the center of the board.
        :param black_agent: agent or None(human)
        :param white_agent: agent or None(human)
        :param gui: if show GUI; always true if there are human playing
        :param dir_save: directory to save board image if GUI is shown; no save for None
        """
        self.black_agent = black_agent
        self.white_agent = white_agent

        self.board = Board(next_color = 'BLACK')

        gui = gui if black_agent and white_agent else True
        self.ui = UI() if gui else None
        self.dir_save = dir_save

        # Metadata
        self.time_elapsed = None

    @property
    def winner(self):
        return self.board.winner

    @property
    def next(self):
        return self.board.next

    @property
    def counter_move(self):
        return self.board.counter_move

    # func to start game
    def start(self):
        if self.ui:
            self._start_with_ui()
        else:
            self._start_without_ui()
        
    # start game with gui
    def _start_with_ui(self):
        self.ui.init_pygame() # draw board, gridlines, guide dots
        self.time_elapsed = time.time() # time at game starting
        
        # First move - center of board
        first_move = (9, 9)
        self.board.put_stone(first_move, check_legal = False)
        self.ui.draw(first_move, opponent_color(self.board.next))
        
        for action in self.board.legal_actions:
                    self.ui.draw(action, 'BLUE', 5)

        # Take turns to play move
        while self.board.winner is None:
            if self.board.next == 'BLACK':
                point = self.perform_one_move(self.black_agent)
            else:
                point = self.perform_one_move(self.white_agent)

            # Check if action is legal
            if point not in self.board.legal_actions:
                continue

            # Apply action
            prev_legal_actions = self.board.legal_actions.copy()
            self.board.put_stone(point, check_legal=False)
            
            # Remove previous legal actions on board
            for action in prev_legal_actions:
                self.ui.remove(action, 5)
                
            # Draw new point
            self.ui.draw(point, opponent_color(self.board.next))
            
            # Update new legal actions and any removed groups
            if self.board.winner:
                for group in self.board.removed_groups:
                    for point in group.points:
                        self.ui.remove(point, STONE_RADIUS)
                if self.board.end_by_no_legal_actions:
                    print('Game ends early (no legal action is available for %s)' % self.board.next)
            else:
                for action in self.board.legal_actions:
                    self.ui.draw(action, 'BLUE', 5)

        self.time_elapsed = time.time() - self.time_elapsed
        if self.dir_save:
            path_file = join(self.dir_save, 'go_' + str(time.time()) + '.jpg')
            self.ui.save_image(path_file)
            print('Board image saved in file ' + path_file)

    # start game without gui
    def _start_without_ui(self):
        """Start the game without GUI. Only possible when no human is playing."""
        # First move is fixed on the center of board
        self.time_elapsed = time.time()
        first_move = (9, 9)
        self.board.put_stone(first_move, check_legal=False)

        # Take turns to play move
        while self.board.winner is None:
            if self.board.next == 'BLACK':
                point = self.perform_one_move(self.black_agent)
            else:
                point = self.perform_one_move(self.white_agent)

            # Apply action
            self.board.put_stone(point, check_legal=False)  # Assuming agent always gives legal actions

        if self.board.end_by_no_legal_actions:
            print('Game ends early (no legal action is available for %s)' % self.board.next)

        self.time_elapsed = time.time() - self.time_elapsed

    def perform_one_move(self, agent):
        if agent:
            return self._move_by_agent(agent)
        else:
            return self._move_by_human()

    def _move_by_agent(self, agent):
        if self.ui:
            pygame.time.wait(100)
            pygame.event.get()
        return agent.get_action(self.board)

    def _move_by_human(self):
        while True:
            pygame.time.wait(100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    inc = (BOARD_WIDTH - 2 * BOARD_BORDER) / (19 - 1)
                    if event.button == 1 and self.ui.outline.collidepoint(event.pos):
                        x = int(round(((event.pos[0] - BOARD_BORDER) / inc), 0))
                        y = int(round(((event.pos[1] - BOARD_BORDER) / inc), 0))
                        point = (x, y)
                        stone = self.board.exist_stone(point)
                        if not stone:
                            return point


def get_agent(agent, color, depth):
    if agent == 0:
        return None, 'HUMAN'
    elif agent == 1:
        return RandomAgent(color), 'Random Agent'
    elif agent == 2:
        return GreedyAgent(color), 'Greedy Agent'
    elif agent == 3:
        return MinimaxAgent(color, depth=depth), 'Minimax Agent'
    elif agent == 4:
        return AlphaBetaAgent(color, depth=depth), 'AlphaBeta Agent'
    # elif agent == 5:
    #     agent = ApproxQAgent(color, RlEnv())
    #     agent.load('ApproxQAgent.npy')
    #     return agent, 'RL Agent'
    else:
        raise ValueError('Invalid agent for ' + color)


def main():
    
    print('\nLet\'s answer some questions! \n')
    depth1 = depth2 = black_agent = white_agent = -1
    
    while black_agent not in [0,1,2,3,4,5]:
        black_agent = int(input("Choose your agent for black - 0 (human); 1 (random); 2 (greedy); 3 (minimax); 4 (alpha-beta prunning) : "))
        if black_agent in [3,4]:
            while depth1 <= 0:
                depth1 = int(input("Choose depth for black agent (depth > 0): "))
    black_agent = get_agent(black_agent,'BLACK',depth1)
        
    while white_agent not in [0,1,2,3,4,5]:
        white_agent = int(input("Choose your agent for white - 0 (human); 1 (random); 2 (greedy); 3 (minimax); 4 (alpha-beta prunning) : "))
        if white_agent in [3,4]:
            while depth2 <= 0:
                depth2 = int(input("Choose depth for white agent (depth > 0): "))
    white_agent = get_agent(white_agent,'WHITE',depth2)
    
    gg = 2
    while gg not in [0, 1]: 
        gg = int(input("play game with (1) or without (0) gui: "))
    
    dir_save = "img"

    print('Agent for BLACK: ' + black_agent[1])
    print('Agent for WHITE: ' + white_agent[1])
    if dir_save:
        print('Directory to save board image: ' + dir_save)

    match = Match(black_agent[0], white_agent[0], gui = (True if gg==1 else False), dir_save = dir_save)

    if gg == 1:
        print('Match starts!')
        match.start()
        
        #sound for black or white win: (need updating)
        pygame.mixer.Sound("wav/zoink.wav").play()
        pygame.time.wait(5000)
    
    else:
        print('Match starts without gui, please wait!')
        match.start()
    
    print(match.winner + ' wins!')
    print('Match ends in ' + str(round(match.time_elapsed,2)) + ' seconds')
    print('Match ends in ' + str(match.counter_move) + ' moves')


if __name__ == '__main__':
    
    main()
