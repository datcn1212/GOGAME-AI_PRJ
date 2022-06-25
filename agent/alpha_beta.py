"""
    minimax with alpha-beta prunning
"""
from agent.basic_agent import Agent
import random
from config_main import Board, opponent_color
from agent.util_agent import get_num_endangered_groups, get_liberties, is_dangerous_liberty, get_num_groups_with_k_liberties
from numpy.random import normal

def evaluate(board: Board, color):
    """Color has the next action"""
    # Score for win or lose
    score_win = 1000 - board.counter_move  # Prefer faster game
    if board.winner:
        return score_win if board.winner == color else -score_win

    oppo = opponent_color(color)
    # Score for endangered groups
    num_endangered_self, num_endangered_oppo = get_num_endangered_groups(board, color)
    if num_endangered_oppo > 0:
        return score_win - 10  # Win in the next move
    elif num_endangered_self > 1:
        return -(score_win - 10)  # Lose in the next move

    # Score for dangerous liberties
    liberties_self, liberties_oppo = get_liberties(board, color)
    for liberty in liberties_oppo:
        if is_dangerous_liberty(board, liberty, oppo):
            return score_win / 2  # Good probability to win in the next next move
    for liberty in liberties_self:
        if is_dangerous_liberty(board, liberty, color):
            self_groups = board.liberty_dict.get_groups(color, liberty)
            liberties = self_groups[0].liberties | self_groups[1].liberties
            able_to_save = False
            for lbt in liberties:
                if len(board.liberty_dict.get_groups(oppo, lbt)) > 0:
                    able_to_save = True
                    break
            if not able_to_save:
                return -score_win / 2  # Good probability to lose in the next next move

    # Score for groups
    num_groups_2lbt_self, num_groups_2lbt_oppo = get_num_groups_with_k_liberties(board, color, 2)
    score_groups = num_groups_2lbt_oppo - num_groups_2lbt_self

    # Score for liberties
    num_shared_liberties_self = 0
    num_shared_liberties_oppo = 0
    for liberty in liberties_self:
        num_shared_liberties_self += len(board.liberty_dict.get_groups(color, liberty)) - 1
    for liberty in liberties_oppo:
        num_shared_liberties_oppo += len(board.liberty_dict.get_groups(oppo, liberty)) - 1
    score_liberties = num_shared_liberties_oppo - num_shared_liberties_self

    # Score for groups (doesn't help)
    # score_groups_self = []
    # score_groups_oppo = []
    # for group in board.groups[color]:
        # if group.num_liberty > 1:
            # score_groups_self.append(eval_group(group, board))
    # for group in board.groups[opponent_color(color)]:
        # if group.num_liberty > 1:
            # score_groups_oppo.append(eval_group(group, board))
    # score_groups_self.sort(reverse=True)
    # score_groups_self += [0, 0]
    # score_groups_oppo.sort(reverse=True)
    # score_groups_oppo += [0, 0]
    # finals = score_groups_oppo[0] - score_groups_self[0] + score_groups_oppo[1] - score_groups_self[1]

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


class AlphaBetaAgent(SearchAgent):
    def __init__(self, color, depth, eval_func=evaluate):
        super().__init__(color, depth, eval_func)

    def get_action(self, board, pruning_actions=20):

        self.pruning_actions = pruning_actions
        score, actions = self.max_value(board, 0, float("-inf"), float("inf"))

        return actions[0] if len(actions) > 0 else None

    def max_value(self, board, depth, alpha, beta):
        """Return the highest score and the corresponding subsequent actions"""
        if self.terminal_test(board) or depth == self.depth:
            return self.eval_func(board, self.color), []

        max_score = float("-inf")
        max_score_actions = None
        # Prune the legal actions
        legal_actions = board.get_legal_actions()
        if self.pruning_actions and len(legal_actions) > self.pruning_actions:
            legal_actions = random.sample(legal_actions, self.pruning_actions)

        for action in legal_actions:
            score, actions = self.min_value(board.generate_successor_state(action), depth, alpha, beta)
            if score > max_score:
                max_score = score
                max_score_actions = [action] + actions

            if max_score > beta:
                return max_score, max_score_actions

            if max_score > alpha:
                alpha = max_score

        return max_score, max_score_actions

    def min_value(self, board, depth, alpha, beta):
        """Return the lowest score and the corresponding subsequent actions"""
        if self.terminal_test(board) or depth == self.depth:
            return self.eval_func(board, self.color), []

        min_score = float("inf")
        min_score_actions = None
        # Prune the legal actions
        legal_actions = board.get_legal_actions()
        if self.pruning_actions and len(legal_actions) > self.pruning_actions:
            legal_actions = random.sample(legal_actions, self.pruning_actions)

        for action in legal_actions:
            score, actions = self.max_value(board.generate_successor_state(action), depth+1, alpha, beta)
            if score < min_score:
                min_score = score
                min_score_actions = [action] + actions

            if min_score < alpha:
                return min_score, min_score_actions

            if min_score < beta:
                beta = min_score

        return min_score, min_score_actions

class MinimaxAgent(SearchAgent):
    def __init__(self, color, depth, eval_func=evaluate):
        super().__init__(color, depth, eval_func)
        
class ExpectimaxAgent(SearchAgent):
    """Assume uniform distribution for opponent"""
    def __init__(self, color, depth, eval_func=evaluate):
        super().__init__(color, depth, eval_func)

    def get_action(self, board, pruning_actions=16):
        self.pruning_actions = pruning_actions
        score, actions = self.max_value(board, 0)
        return actions[0] if len(actions) > 0 else None

    def max_value(self, board, depth):
        if self.terminal_test(board) or depth == self.depth:
            return self.eval_func(board, self.color), []

        max_score = float("-inf")
        max_score_actions = None
        # Prune the legal actions
        legal_actions = board.get_legal_actions()
        if self.pruning_actions and len(legal_actions) > self.pruning_actions:
            legal_actions = random.sample(legal_actions, self.pruning_actions)

        for action in legal_actions:
            score, actions = self.expected_value(board.generate_successor_state(action), depth)
            if score > max_score:
                max_score = score
                max_score_actions = [action] + actions

        return max_score, max_score_actions

    def expected_value(self, board, depth):
        if self.terminal_test(board) or depth == self.depth:
            return self.eval_func(board, self.color), []

        expected_score = 0.0
        # Prune the legal actions
        legal_actions = board.get_legal_actions()
        if self.pruning_actions and len(legal_actions) > self.pruning_actions:
            legal_actions = random.sample(legal_actions, self.pruning_actions)

        for action in legal_actions:
            score, actions = self.max_value(board.generate_successor_state(action), depth+1)
            expected_score += score / len(legal_actions)

        return expected_score, []
