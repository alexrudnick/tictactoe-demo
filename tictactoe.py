#!/usr/bin/python3

"""a simple tictactoe game.

We're going to represent a board state with a single list, for simplicity. Every
spot can contain a string, which will be either X, O or a space to indicate an
empty spot.

Making a move will return a new BoardState, and a BoardState can tell you
whether somebody has won or not.

So to play the game, we'll take turns making moves, and just return a new board
state. The game loop will check if somebody has won after each move.
"""

import random

class BoardState:
    def __init__(self):
        self.board = [str(i) for i in range(1, 10)]

    def winner(self):
        # there are only eight different ways to win -- if we were working with
        # a larger board, we would do something fancier, but we can just
        # enumerate them here.
        indices_to_win = [
            # rows
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            # columns
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            # diagonals
            [0, 4, 8],
            [2, 4, 6], ]

        for index_list in indices_to_win:
            # grab what's in those spots -- if they're all taken by the same
            # player, then that player has won.
            entries = [self.board[i] for i in index_list]
            set_entries = set(entries)
            if len(set_entries) == 1:
                if entries[0] in "XO":
                    return entries[0]
        # nobody won yet.
        return None

    def available_moves(self):
        # all the indices that have not yet been taken
        return [i+1 for i in range(9)
                if self.board[i] not in "XO"]
        
    def make_move(self, player, position):
        """Returns either a new BoardState when given a valid move.

        Assumes the outside game logic is keeping track of whose turn it is.
        """
        if player not in "XO":
            print("error: invalid player?")
            return self

        if position not in self.available_moves():
            print("can't make that move", position)
            self.printme()
            return self
        # now we know that's a valid move
        newboard = BoardState()
        newboard.board = self.board[:]
        newboard.board[position - 1] = player
        return newboard

    def printme(self):
        print("""\
{} | {} | {}
---------
{} | {} | {}
---------
{} | {} | {}
""".format(*self.board))



# player O is the AI and they're trying to maximize.
# player X is the human and they're trying to minimize.

def minmax_search(board):
    # return the move that optimizes the utility for player O
    possible_moves = board.available_moves()
    print("considering making one of these:", possible_moves)
    # for each move that's possible here
    # pick the move that maximizes my utility if the subsequent move maximizes
    # the utility for the opponent

    # tuples of (score, dist, move)
    score_dist_move_triples = []

    bestscore = float('-inf')
    bestdist = float('inf')

    # This is very similar to the max_value function, below.
    for move in possible_moves:
        newboard = board.make_move("O", move)
        board_score, dist = min_value(newboard)
        if ((board_score > bestscore) or
            (board_score == bestscore and (dist < bestdist))):
            bestscore = board_score
            bestdist = dist + 1
            bestmove = move
    print("bestmove has score {}, it is {}".format(bestscore, bestmove))
    return bestmove

## these functions return (score, dist) tuples, where dist is the number of
## steps into the future that the score occurs.
def max_value(board):
    """find the maximal possible score, where O makes the next move"""
    if board.winner() == "O":
        return (1, 0)
    elif board.winner() == "X":
        return (-1, 0)
    elif not board.available_moves():
        return (0, 0)
    bestscore = float('-inf')
    bestdist = float('inf')
    possible_moves = board.available_moves()
    for move in possible_moves:
        newboard = board.make_move("O", move)
        board_score, dist = min_value(newboard)
        if ((board_score > bestscore) or
            (board_score == bestscore and (dist < bestdist))):
            bestscore = board_score
            bestdist = dist + 1
    return (bestscore, bestdist)

def min_value(board):
    """find the minimal possible score, where X makes the next move"""
    if board.winner() == "O":
        return (1, 0)
    elif board.winner() == "X":
        return (-1, 0)
    elif not board.available_moves():
        return (0, 0)
    bestscore = float('inf')
    bestdist = float('inf')
    possible_moves = board.available_moves()
    for move in possible_moves:
        newboard = board.make_move("X", move)
        board_score, dist = max_value(newboard)
        if ((board_score < bestscore) or
            (board_score == bestscore and (dist < bestdist))):
            bestscore = board_score
            bestdist = dist + 1
    return (bestscore, bestdist)
            
def main():
    board = BoardState()

    cur_player = "X"
    while (not board.winner()) and (board.available_moves()):
        board.printme()

        # if cur_player is the person, then ask for input
        if cur_player == "X":
            position = input("player {} make a move: ".format(cur_player))
        # if cur_player is the AI, then calculate optimal move
        elif cur_player == "O":
            # calculate optimal move
            bestmove = minmax_search(board)
            print("got the best move for the board:", bestmove)
            position = str(bestmove)
        else:
            print("oh no")
            return

        try:
            position = int(position)
        except ValueError:
            position = -1

        newboard = board.make_move(cur_player, position)
        if newboard != board:
            cur_player = "O" if cur_player == "X" else "X"
            board = newboard

    winner = board.winner()
    print("\n**** CONCLUSION!! ****")
    board.printme()
    if winner:
        print("We have a winner!! Congratulations, Player {}\n".format(winner))
    else:
        print("draw game!\n")

if __name__ == "__main__": main()
