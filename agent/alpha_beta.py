"""minimax & alpha-beta prunning"""

from agent.basic_agent import Agent
from config_main import Board, opponent_color
from agent.util_agent import num_endangeredgroups, get_liberties, is_dangerous_liberty, num_k_liberties_groups
from numpy.random import normal
import random
import numpy as np

def evaluate(board: Board, color):  # color has the next action
    # Score for win or lose
    score_win = 1000 - board.counter_move  # Prefer faster game
    if board.winner:
        return score_win if board.winner == color else -score_win

    oppo = opponent_color(color)
    # Score for endangered groups
    num_endangered_self, num_endangered_oppo = num_endangeredgroups(board, color)
    if num_endangered_oppo > 0:
        return score_win - 10  # Win in the next move
    elif num_endangered_self > 1:
        return -(score_win - 10)  # Lose in the next move

    # Score for dangerous liberties
    liberties_self, liberties_oppo = get_liberties(board, color)
    for liberty in liberties_oppo:
        if is_dangerous_liberty(board, liberty, oppo):
            return score_win / 2 
            # Good probability to win in the next next move by putting stone in this dangerous liberty
            
    for liberty in liberties_self:
        if is_dangerous_liberty(board, liberty, color):
            self_groups = board.liberty_dict.get_groups(color, liberty)
            liberties = self_groups[0].liberties | self_groups[1].liberties
            save = False
            for lbt in liberties:
                if len(board.liberty_dict.get_groups(oppo, lbt)) > 0:
                    save = True
                    break                                                                                                                                                                                                     
            if not save:
                return -score_win / 2  # Good probability to lose in the next next move

    # Score for groups
    num_groups_2lbt_self, num_groups_2lbt_oppo = num_k_liberties_groups(board, color, 2)
    score_groups = num_groups_2lbt_oppo - num_groups_2lbt_self

    # Score for liberties
    num_shared_liberties_self = 0
    num_shared_liberties_oppo = 0
    for liberty in liberties_self:
        num_shared_liberties_self += len(board.liberty_dict.get_groups(color, liberty)) - 1
    for liberty in liberties_oppo:
        num_shared_liberties_oppo += len(board.liberty_dict.get_groups(oppo, liberty)) - 1
    score_liberties = num_shared_liberties_oppo - num_shared_liberties_self

    return score_groups * normal(1, 0.1) + score_liberties * normal(1, 0.1)

class SearchAgent(Agent):
    def __init__(self, color, depth, eval_func):
        """
        :param color:
        :param depth: search depth
        :param eval_func: evaluation function from the evaluation module
        """
        super().__init__(color)
        self.depth = depth
        self.eval_func = eval_func
        self.pruning_actions = None

    def get_action(self, board):
        raise NotImplementedError

    def __str__(self):
        return '%s; color: %s; search_depth: %d' % (self.__class__.__name__, self.color, self.depth)


class MinimaxAgent(SearchAgent):
    
    def __init__(self, color, depth, eval_func=evaluate):
        super().__init__(color, depth, eval_func)

    def get_action(self, board):
        
        if len(board._get_legal_actions()) == 1:
            return board._get_legal_actions()[0]
        
        score, actions = self.max_value(board, 0)

        return actions[0] if len(actions) > 0 else None

    def max_value(self, board, depth):
        
        if self.terminal_test(board) or depth == self.depth:
            return self.eval_func(board, self.color), []

        max_score = float("-inf")
        max_score_actions = []
       
        legal_actions = board.get_legal_actions()
        
        for action in legal_actions:
            score, actions = self.min_value(board.generate_successor_state(action), depth+1)
            if score > max_score:
                max_score = score
                max_score_actions = [action] 

        return max_score, max_score_actions

    def min_value(self, board, depth):
        
        if self.terminal_test(board) or depth == self.depth:
            return self.eval_func(board, self.color), []

        min_score = float("inf")
        min_score_actions = []
        
        legal_actions = board.get_legal_actions()
        
        for action in legal_actions:
            score, actions = self.max_value(board.generate_successor_state(action), depth+1)
            if score < min_score:
                min_score = score
                min_score_actions = [action] 
                
        return min_score, min_score_actions

class AlphaBetaAgent(SearchAgent):
    
    def __init__(self, color, depth, eval_func=evaluate):
        super().__init__(color, depth, eval_func)

    def get_action(self, board):

        if len(board._get_legal_actions()) == 1:
            return board._get_legal_actions()[0]
        
        score, actions = self.max_value(board, 0, float("-inf"), float("inf"))

        return actions[0] if len(actions) > 0 else None

    def max_value(self, board, depth, alpha, beta):
        
        if self.terminal_test(board) or depth == self.depth:
            return self.eval_func(board, self.color), []

        max_score = float("-inf")
        max_score_actions = None
        
        legal_actions = board.get_legal_actions()

        for action in legal_actions:
            score, actions = self.min_value(board.generate_successor_state(action), depth+1, alpha, beta)
            if score > max_score:
                max_score = score
                max_score_actions = [action]

            if max_score > beta:
                return max_score, max_score_actions  #prunning

            if max_score > alpha:
                alpha = max_score

        return max_score, max_score_actions

    def min_value(self, board, depth, alpha, beta):
        
        if self.terminal_test(board) or depth == self.depth:
            return self.eval_func(board, self.color), []

        min_score = float("inf")
        min_score_actions = None
        
        legal_actions = board.get_legal_actions()
    
        for action in legal_actions:
            score, actions = self.max_value(board.generate_successor_state(action), depth+1, alpha, beta)
            if score < min_score:
                min_score = score
                min_score_actions = [action]

            if min_score < alpha:
                return min_score, min_score_actions  #prunning

            if min_score < beta:
                beta = min_score

        return min_score, min_score_actions