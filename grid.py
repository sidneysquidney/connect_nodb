from typing import Tuple
import numpy as np
from enum import Enum
from collections import namedtuple

from reference import GridRef

class Piece(Enum):
    EMPTY = ' '
    RED = 'R'
    YELLOW = 'Y'
    
WinState = namedtuple('WinState', ['is_ended', 'winner'])
Point = namedtuple('Point', ['r', 'c'])
PlayerState = namedtuple('PlayerState', ['max', 'score', 'print'])

NR, NC, TW = 6, 7, 4
P1 = PlayerState(True, 1, '⚈')
P2 = PlayerState(False, -1, '◯')
P0 = PlayerState(None, 0, '_')
PDICT = {Piece.RED: P1, Piece.YELLOW: P2, Piece.EMPTY: P0}
OPDICT = {'⚈': Piece.RED, '◯': Piece.YELLOW, '_': Piece.EMPTY}
GRIDREF = GridRef(NR, NC, TW)

class Grid:
    def __init__(self): 
        self.grid = np.full((NR,NC), Piece.EMPTY, dtype = Piece)
        self.space = np.zeros(NC, dtype = int)
        self.last_move = Point(0,0)
        
    def valid_moves(self) -> np.ndarray:
    # returns an array of indexes that have space
        return np.nonzero(self.space < NR)[0] # type: ignore

    def make_move(self, player: Piece, column: int):
    # inputs the player counter into the next available space in the column
        if self.space[column] == NR:
            raise ValueError(f'Column {column} is full')
        else:
            self.grid[self.space[column], column] = player
            self.last_move = Point(self.space[column], column)
            self.space[column] += 1
            
    def update(self, player: Piece, column: int) -> WinState:
    # makes a move in col, then returns the WinState tuple
        self.make_move(player, column)
        return self.get_win_state(player)
    
    def get_winner(self, player: Piece) -> bool:
    # searches through the lines at the coordinates of the last move. if 4 in a row found returns True
        lines = GRIDREF.get_lines_from_position(self.last_move.r, self.last_move.c, self.grid)
        for line in lines:
            count = 1
            for i in range(1, len(line)):
                if line[i] == line[i - 1]:
                    count += 1
                else:
                    count = 1
                if count == TW:
                    if line[i] == player:
                        return True
        return False
        
    def get_win_state(self, player: Piece) -> WinState:
        # returns a WinState tuple [0] is a bool telling 'is_ended', [1] tells the winner/ empty
        if self.get_winner(player):
            return WinState(True, player)
        elif len(self.valid_moves()) == 0:
            return WinState(True, Piece.EMPTY)
        else:
            return WinState(False, Piece.EMPTY)
        
def print_grid(grid: np.ndarray) -> str:
    # flips grid upside down and prints grid
    print()
    for line in np.flipud(grid):
        print('|' + ' '.join([PDICT[p].print for p in line]) + '|')

def string_to_grid(s: str) -> Tuple[np.ndarray]:
    # turns string representation of a grid into a useable grid
    grid = np.array(np.flipud([[OPDICT[x] for x in l if OPDICT.get(x)] for l in s.split('\n')]))
    space = []
    for col in range(NC):
        c = grid[:,col]
        if np.nonzero(c == Piece.EMPTY)[0].size > 0:
            space.append(np.nonzero(c == Piece.EMPTY)[0][0])
        else:
            space.append(NR)
    return grid, np.array(space)

# g = Grid()
# print(g.valid_moves())