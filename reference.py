import numpy as np
from collections import namedtuple
from typing import List

Lines = namedtuple('Lines', ['r', 'c', 'dd', 'du'])

class ListFlatten:
    def __init__(self, group):
        self.result = []
        self.backtrack(group)
        
    def backtrack(self, group):
        if type(group[0]) != list:
            self.result.append(group)
        else:
            for item in group:
                self.backtrack(item)

class GridRef:
    # a Grid Reference class to locate lines from a specific coordinate
    def __init__(self, n_r: int, n_c: int, to_win: int):
        self.lines_dict = {}
        self.all_lines = {}
        self.apply_lines_to_lines_dict(n_r, n_c, to_win)
        
    def apply_lines_to_lines_dict(self, n_r: int, n_c: int, to_win: int):
        dct = {l: set() for l in ['r', 'c', 'dd', 'du']}
        for r in range(n_r):
            for c in range(n_c):   
                bottom_right = min(n_r - r - 1, n_c - c - 1)
                top_right = min(r, n_c - c - 1)
                top_left = min(r,c)
                bottom_left = min(n_r - r - 1, c)
                row, col = r, c
                if to_win > n_r:
                    row = None
                else:
                    dct['r'].add(r)
                if to_win > n_c:
                    col = None
                else:
                    dct['c'].add(c)
                if top_left + bottom_right  + 1>= to_win:
                    diag_down = c - r
                    dct['dd'].add(diag_down)
                else:
                    diag_down = None
                if bottom_left + top_right + 1 >= to_win:
                    diag_up = r + c - n_r + 1
                    dct['du'].add(diag_up)
                else:
                    diag_up = None
                self.lines_dict[(r, c)] = Lines(row, col, diag_down, diag_up)
        self.all_lines = {key: list(dct[key]) for key in dct.keys()}
        
    def get_lines_from_position(self, r: int, c: int, grid: np.ndarray) -> List[list]:
    #   gets the lines from coordinates[x,y]
        lines_from_pos = self.lines_dict[(r,c)]
        lines = []
        if lines_from_pos.r != None:
            lines.append(list(grid[lines_from_pos.r,:]))
        if lines_from_pos.c != None:
            lines.append(list(grid[:,lines_from_pos.c]))
        if lines_from_pos.dd != None:
            lines.append(list(np.diag(grid, lines_from_pos.dd)))
        if lines_from_pos.du != None:
            lines.append(list(np.diag(np.flipud(grid), lines_from_pos.du)))
        return lines
        
    def get_lines(self, grid: np.ndarray) -> List[list]:
        return ListFlatten([[list(grid[r,:]) for r in self.all_lines['r']],
                [list(grid[:,c]) for c in self.all_lines['c']],
                [list(np.diag(grid, dd)) for dd in self.all_lines['dd']],
                [list(np.diag(np.flipud(grid), du)) for du in self.all_lines['du']]]).result   