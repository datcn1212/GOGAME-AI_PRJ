"""utilities for agents"""

from config_main import *
import numpy as np

# number of endangered groups
def num_endangeredgroups(board: Board, color):
    num_endangered_self = 0
    num_endangered_oppo = 0
    for group in board.endangered_groups:
        if group.color == color:
            num_endangered_self += 1
        else:
            num_endangered_oppo += 1
    return num_endangered_self, num_endangered_oppo

# number of groups which has k liberties
def num_k_liberties_groups(board: Board, color, k):
    num_self = 0
    num_oppo = 0
    for group in board.groups[color]:
        if group.num_liberty == k:
            num_self += 1
    for group in board.groups[opponent_color(color)]:
        if group.num_liberty == k:
            num_oppo += 1
    return num_self, num_oppo

# get all liberties for each color
def get_liberties(board: Board, color):
    liberties_self = set()
    liberties_oppo = set()
    for group in board.groups[color]:
        liberties_self = liberties_self | group.liberties
    for group in board.groups[opponent_color(color)]:
        liberties_oppo = liberties_oppo | group.liberties
    return liberties_self, liberties_oppo

# 2 groups have this liberty, each has 2 liberties
def is_dangerous_liberty(board: Board, point, color):
    self_groups = board.liberty_dict.get_groups(color, point)
    return len(self_groups) == 2 and self_groups[0].num_liberty == 2 and self_groups[1].num_liberty == 2
