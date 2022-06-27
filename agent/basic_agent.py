"""basic agent for game: random, greedy"""

import random
from config_main import *

class Agent:
    
    def __init__(self, color):
        self.color = color # 'BLACK' or 'WHITE'

    @classmethod
    def terminal_test(cls, board):
        return board.winner is not None

    def get_action(self, board: Board):
        raise NotImplementedError

class RandomAgent(Agent):
    
    def __init__(self, color):
        super().__init__(color)

    def get_action(self, board):
        actions = board.get_legal_actions()
        return random.choice(actions) if actions else None


class GreedyAgent(Agent):
    
    """Pick the action that kills the liberty of most opponent's groups"""
    def __init__(self, color):
        super().__init__(color)

    def get_action(self, board):
        actions = board.get_legal_actions()
        num_groups = [len(board.liberty_dict.get_groups(opponent_color(self.color), action)) for action in actions]
        max_num_groups = max(num_groups)
        candidates = []
        for action in actions:
            if len(board.liberty_dict.get_groups(opponent_color(self.color), action)) == max_num_groups:
                candidates.append(action)
        return random.choice(candidates) if actions else None
