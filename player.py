import random

from grid import Grid, Piece, WinState
from minimax import MiniMax, MiniMaxP, MiniMaxN

class Player:
    # player class that parents Human and AI
    def __init__(self, token: Piece):
        self.token = token
        
class Human(Player):
    # human class that asks for user input of valid moves (0-6), then updates the board
    def make_move(self, grid: Grid) -> WinState:
        valid_moves = grid.valid_moves()
        while True:
            move = input(f'Make a move within {valid_moves}')
            if move.isdigit() and int(move) in valid_moves:
                return grid.update(self.token, int(move))
            
class AI(Player):
    pass
            
class RandomAI(AI):
    # random ai that makes a random move out of the available valid moves
    def make_move(self, grid: Grid) -> WinState:
        valid_moves = grid.valid_moves()
        move = random.choice(valid_moves)
        return grid.update(self.token, move)
    
class MiniMax0AI(AI):
    def make_move(self, grid: Grid) -> WinState:
        m = MiniMaxN(grid, self.token, 4)
        move = m.minimax_move()
        return grid.update(self.token, move)
    
class MiniMax1AI(AI):
    def make_move(self, grid: Grid) -> WinState:
        m = MiniMax(grid, self.token, 4)
        move = m.minimax_move()
        return grid.update(self.token, move)
    
class MiniMax2AI(AI):
    def make_move(self, grid: Grid) -> WinState:
        m = MiniMaxP(grid, self.token, 4)
        move = m.minimax_move()
        return grid.update(self.token, move)
    
class MiniMax3AI(AI):
    def make_move(self, grid: Grid) -> WinState:
        m = MiniMax(grid, self.token, 6)
        move = m.minimax_move()
        return grid.update(self.token, move)
    
class MiniMax4AI(AI):
    def make_move(self, grid: Grid) -> WinState:
        m = MiniMaxP(grid, self.token, 6)
        move = m.minimax_move()
        return grid.update(self.token, move)
    
class MiniMax5AI(AI):
    def make_move(self, grid: Grid) -> WinState:
        m = MiniMax(grid, self.token, 8)
        move = m.minimax_move()
        return grid.update(self.token, move)
    
class MiniMax6AI(AI):
    def make_move(self, grid: Grid) -> WinState:
        m = MiniMaxP(grid, self.token, 8)
        move = m.minimax_move()
        return grid.update(self.token, move)
    
class MediumAI(AI):
    def make_move(self, grid: Grid) -> WinState:
        m = MiniMaxP(grid, self.token, 2)
        move = m.minimax_move()
        return grid.update(self.token, move)
    
class HardAI(AI):
    def make_move(self, grid: Grid) -> WinState:
        m = MiniMaxP(grid, self.token, 6)
        move = m.minimax_move()
        return grid.update(self.token, move)
    
# class HardAI(AI):
#     def make_move(self, grid: Grid) -> WinState:
#         m = MiniMaxP(grid, self.token, 8)
#         move = m.minimax_move()
#         return grid.update(self.token, move)