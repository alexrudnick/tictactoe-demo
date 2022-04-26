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

class BoardState:
    def __init__(self):
        self.board = [" "] * 9

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
                # print("same:", index_list)
                if entries[0] in "XO":
                    return entries[0]
        # nobody won yet.
        return None

    def available_moves(self):
        # all the indices that have not yet been taken
        return [i for i in range(9)
                if self.board[i] == " "]
        
    def make_move(self, player, position):
        """Returns either a new BoardState when given a valid move.

        Assumes the outside game logic is keeping track of whose turn it is.
        """
        # 1-based indices for the input
        index = position - 1
        if player not in "XO":
            print("error: invalid player?")
            return self

        if index not in self.available_moves():
            print("can't make that move")
            return self
        # now we know that's a valid move
        newboard = BoardState()
        newboard.board = self.board[:]
        newboard.board[index] = player
        return newboard

    def printme(self):
        print("""\
{} | {} | {}
---------
{} | {} | {}
---------
{} | {} | {}
""".format(*self.board))


def main():
    board = BoardState()

    cur_player = "X"
    while (not board.winner()) and (board.available_moves()):
        board.printme()
        position = input("player {} make a move:".format(cur_player))

        try:
            position = int(position)
        except ValueError:
            position = -1

        newboard = board.make_move(cur_player, position)
        if newboard != board:
            cur_player = "O" if cur_player == "X" else "X"
            board = newboard

    winner = board.winner()
    print("\n**** CONLUSION!! ****")
    board.printme()
    if winner:
        print("We have a winner!! Congratulations, Player {}\n".format(winner))
    else:
        print("draw game!\n")

if __name__ == "__main__": main()
