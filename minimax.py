import numpy as np
from enum import Enum
from collections import namedtuple
import math
from typing import List
import random

from grid import Grid, Piece, Point, PDICT, GRIDREF, WinState, print_grid, string_to_grid
from score import score_by_piece, score_by_line

countr = 0

WinState = namedtuple('WinState', ['is_ended', 'winner'])
Point = namedtuple('Point', ['r', 'c'])
ColScore = namedtuple('Colscore', ['c', 'score'])
PlayerState = namedtuple('PlayerState', ['minmax', 'score', 'print'])

class GridChild(Grid): 
    # update grid, declare if winner, score func, get valid inputs - make children
    def __init__(self, 
                 grid: np.ndarray, 
                 space: np.ndarray, 
                 parent: Grid, 
                 current_player: Piece, 
                 column: int):
        self.grid = grid
        self.space = space
        self.last_move = Point(0, 0)
        self.parent = parent
        self.current_player = current_player
        self.win_state = self.update(self.current_player, column)
        self.children = {}
        
    def change_player(self):
        return Piece.RED if self.current_player == Piece.YELLOW else Piece.YELLOW
    
    def update(self, player: Piece, column: int) -> WinState:
        if column != None:
            return super().update(player, column)
        else:
            return WinState(False, Piece.EMPTY)
        
    def score(self):
        if self.win_state.is_ended:
            return ColScore(self.last_move.c, self.get_win_state_score(self.current_player))
        lsts = GRIDREF.get_lines(self.grid)
        score = score_by_line(lsts)
        return ColScore(self.last_move.c, score)
    
    def make_children(self):
    # the children are the possible moves from the current grid. The depth is how many times this iterates.
        for col in self.valid_moves():
            self.children[col] = GridChild(self.grid.copy(), 
                                            self.space.copy(), 
                                            self, 
                                            self.change_player(), 
                                            col)
        
    def get_win_state_score(self, player: Piece) -> WinState:
        state = super().get_win_state(player)
        if state.winner != Piece.EMPTY:
            return PDICT[state.winner].score * math.inf
        return 0
            
    def print_grid(self):
        # flips grid upside down and prints grid
        print()
        for line in np.flipud(self.grid):
            print('|' + ' '.join([PDICT[p].print for p in line]) + '|')
            
class ChildStart(GridChild):
    def make_children(self):
    # the children are the possible moves from the current grid. The depth is how many times this iterates.
        for col in self.valid_moves():
            self.children[col] = GridChild(self.grid.copy(), 
                                            self.space.copy(), 
                                            self, 
                                            self.current_player, 
                                            col)
    
class GridChildP(GridChild):
    def score(self):
        if self.win_state.is_ended:
            # print('score true', ColScore(self.last_move.c, self.get_win_state_score(self.current_player)))
            return ColScore(self.last_move.c, self.get_win_state_score(self.current_player))
        lsts = GRIDREF.get_lines(self.grid)
        score = score_by_piece(lsts)
        return ColScore(self.last_move.c, score)
    
    def make_children(self):
    # the children are the possible moves from the current grid. The depth is how many times this iterates.
        for col in self.valid_moves():
            self.children[col] = GridChildP(self.grid.copy(), 
                                            self.space.copy(), 
                                            self, 
                                            self.change_player(), 
                                            col)
            
class ChildStartP(GridChild):
    def make_children(self):
    # the children are the possible moves from the current grid. The depth is how many times this iterates.
        for col in self.valid_moves():
            self.children[col] = GridChildP(self.grid.copy(), 
                                            self.space.copy(), 
                                            self, 
                                            self.current_player, 
                                            col)
        
class MiniMax:
    def __init__(self, grid: Grid, current_player: Piece, depth_limit: int):
        self.current_player = current_player
        self.grid = grid
        self.depth_limit = depth_limit
        self.tree = self.create_tree()
        self.start = True
        self.countr = 0
        
    def create_tree(self):
        return ChildStart(self.grid.grid.copy(), 
                         self.grid.space.copy(), 
                         None, 
                         self.current_player, 
                         None)
        
    def minimax_move(self):
        return self.minimax(self.tree, self.depth_limit, -math.inf, math.inf, PDICT[self.current_player].max).c

    def minimax(self, current_node: GridChild, depth: int, alpha: int, beta: int, player: bool):
        if current_node.win_state.is_ended or depth == 0:
            self.countr += 1
            # print(current_node.score())
            # print(current_node.current_player)
            # current_node.print_grid()
            return current_node.score()
        elif player:
            current_node.make_children()
            children = sorted(current_node.children, key=lambda x: abs(x - 3))
            max_eval = ColScore(children[0], -math.inf)
            for child in children:
                eval = self.minimax(current_node.children[child], depth - 1, alpha, beta, False)
                if eval.score > max_eval.score:
                    max_eval = ColScore(child, eval.score)
                alpha = max(alpha, eval.score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            current_node.make_children()
            children = sorted(current_node.children, key=lambda x: abs(x - 3))
            min_eval = ColScore(children[0], math.inf)
            for child in children:
                eval = self.minimax(current_node.children[child], depth - 1, alpha, beta, True)
                if eval.score < min_eval.score:
                    min_eval = ColScore(child, eval.score)
                beta = min(beta, eval.score)
                if beta <= alpha:
                    break   
            return min_eval
        
class MiniMaxP(MiniMax):
    def create_tree(self):
        return ChildStartP(self.grid.grid.copy(), 
                         self.grid.space.copy(), 
                         None, 
                         self.current_player, 
                         None)
        
class MiniMaxN(MiniMax):
    def minimax_move(self):
        return self.minimax(self.tree, self.depth_limit, PDICT[self.current_player].max).c

    def minimax(self, current_node: GridChild, depth: int, player: bool):
        if current_node.win_state.is_ended or depth == 0:
            self.countr += 1
            return current_node.score()
        elif player:
            max_eval = ColScore(None, -math.inf)
            current_node.make_children()
            children = sorted(current_node.children, key=lambda x: abs(x - 3))
            for child in children:
                eval = self.minimax(current_node.children[child], depth - 1, False)
                if eval.score >= max_eval.score:
                    max_eval = ColScore(child, eval.score)
            return max_eval
        else:
            min_eval = ColScore(None, math.inf)
            current_node.make_children()
            children = sorted(current_node.children, key=lambda x: abs(x - 3))
            for child in children:
                eval = self.minimax(current_node.children[child], depth - 1, True)
                if eval.score <= min_eval.score:
                    min_eval = ColScore(child, eval.score)
            return min_eval
    


              
g2 = '''|_ ⚈ ⚈ ◯ _ ⚈ ◯|
|_ ◯ ◯ ⚈ ⚈ ◯ ⚈|
|_ ⚈ ⚈ ◯ ◯ ⚈ ◯|
|_ ◯ ◯ ⚈ ⚈ ◯ ⚈|
|⚈ ⚈ ⚈ ◯ ◯ ⚈ ◯|
|◯ ◯ ◯ ⚈ ⚈ ◯ ⚈|'''

g3 = '''|◯ ◯ ⚈ ◯ ⚈ _ _|
|⚈ ⚈ ◯ ⚈ ◯ _ _|
|⚈ ⚈ ⚈ ◯ ◯ ⚈ ◯|
|◯ ◯ ◯ ⚈ ⚈ ◯ ⚈|
|⚈ ⚈ ⚈ ◯ ◯ ⚈ ◯|
|◯ ◯ ◯ ⚈ ⚈ ◯ ⚈|'''

g2 = string_to_grid(g2)
g3 = string_to_grid(g3)

# print_grid(g3[0])
g20 = Grid()
g20.grid = g2[0]
g20.space = g2[1]

g30 = Grid()
g30.grid = g3[0]
g30.space = g3[1]
            
# g1 = Grid()
# print_grid(g30.grid)
# m = MiniMaxP(g30, Piece.RED, 4)

# print('MOVE', m.minimax_move())
# print(g30.update(Piece.RED, 0))

# minimax doesn't do winning move - should do

# print(m.countr)