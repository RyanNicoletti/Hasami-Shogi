# Author: Ryan Nicoletti
# Date: 11/19/2021
# Description: Hasami Shogi Game in Python

class HasamiShogiGame:
    """
    represents the board game hasami shogi
    """

    def __init__(self):
        """
        Creates a new instance of the hasami shogi game with specified board
        """
        self._board = [["R" for pawn in range(9)], ['.' for space in range(9)], ['.' for space in range(9)],
                       ['.' for space in range(9)], ['.' for space in range(9)], ['.' for space in range(9)],
                       ['.' for space in range(9)], ['.' for space in range(9)], ["B" for pawn in range(9)]]
        self._row_map = {'a': 0,
                         'b': 1,
                         'c': 2,
                         'd': 3,
                         'e': 4,
                         'f': 5,
                         'g': 6,
                         'h': 7,
                         'i': 8}
        self._active_player = 'BLACK'
        self._curr_player_turn = 'B'
        self._opponent = 'R'
        self._game_state = 'UNFINISHED'
        self._red_count = 0
        self._black_count = 0

    def get_board(self):
        return self._board

    def print_board(self,):
        board = self.get_board()
        for row in board:
            for cell in row:
                print(cell, end=' ')
            print()

    def set_active_player(self, color):
        self._active_player = color
        self._opponent = 'B' if self._opponent == 'R' else 'R'

    def set_curr_player_turn(self):
        self._curr_player_turn = 'R'if self.get_active_player() == "RED" else 'B'

    def get_curr_player_turn(self):
        return self._curr_player_turn

    def set_opponent(self):
        self._opponent = 'B' if self.get_active_player() == 'RED' else 'R'

    def get_opponent(self):
        return self._opponent

    def inc_captured_pieces(self):
        if self._opponent == 'R':
            self._red_count += 1
        else:
            self._black_count += 1

    def get_op_count(self):
        return self._red_count if self._opponent == 'R' else self._black_count

    def get_num_captured_pieces(self, player):
        return self._red_count if player == "RED" else self._black_count

    def change_turn(self):
        if self.get_active_player() == 'BLACK':
            self.set_active_player('RED')
            self.set_opponent()
            self.set_curr_player_turn()
        else:
            self.set_active_player('BLACK')
            self.set_opponent()
            self.set_curr_player_turn()

    def get_active_player(self):
        return self._active_player

    def set_game_state(self, winner):
        """
        takes 'RED_WON' or 'BLACK_WON' as params and
        sets winner of the game to red or black
        """
        self._game_state = winner

    def get_game_state(self):
        return self._game_state

    def get_square_occupant(self, square):
        board = self.get_board()
        row = self._row_map[square[0]]
        col = int(square[1])
        if board[row][col] == 'R':
            return "RED"
        elif board[row][col] == 'B':
            return "BLACK"
        else:
            return 'NONE'

    def make_move(self, start_pos, end_pos):
        start_row_num = self._row_map[start_pos[0]]
        start_col_num = int(start_pos[1]) - 1        # align column to 0 indexed array
        end_row_num = self._row_map[end_pos[0]]
        end_col_num = int(end_pos[1]) - 1            # align column to 0 indexed array

        board = self.get_board()

        active_player = self.get_active_player()

        game_sate = self.get_game_state()

        # if starting at wrong players pawn, return false
        if (board[start_row_num][start_col_num] == 'B' and active_player == 'RED') or \
                (board[start_row_num][start_col_num] == 'R' and active_player == 'BLACK') or \
                board[start_row_num][start_col_num] == '.':
            return False

        # if the end position is off the board, return False
        if end_row_num < 0 or end_row_num > 8 or end_col_num < 0 or end_col_num > 8:
            return False

        # check for only verticle and horizontal movement
        if end_row_num != start_row_num and end_col_num != start_col_num:
            return False

        # if game has been won return false
        if game_sate == 'RED_WON' or game_sate == 'BLACK_WON':
            return False

        if start_row_num > end_row_num:
            # move up
            start_pos = end_row_num
            for i in reversed(range(start_row_num-end_row_num)):
                if board[i+start_pos][start_col_num] != '.':
                    return False
            board[end_row_num][end_col_num] = 'B' if active_player == 'BLACK' else 'R'
            board[start_row_num][start_col_num] = '.'

        if end_row_num > start_row_num:
            # move down
            start_pos = start_row_num+1
            for i in range(end_row_num-start_row_num):
                if board[i + start_pos][start_col_num] != '.':
                    return False
            board[end_row_num][end_col_num] = 'B' if active_player == 'BLACK' else 'R'
            board[start_row_num][start_col_num] = '.'

        if end_col_num > start_col_num:
            # move right
            start_pos = start_col_num + 1
            for i in range(end_col_num-start_col_num):
                if board[start_row_num][i+start_pos] != '.':
                    return False
            board[end_row_num][end_col_num] = 'B' if active_player == 'BLACK' else 'R'
            board[start_row_num][start_col_num] = '.'

        if start_col_num > end_col_num:
            # move left
            start_pos = end_col_num
            for i in reversed(range(start_col_num-end_col_num)):
                if board[start_row_num][i + start_pos] != '.':
                    return False
            board[end_row_num][end_col_num] = 'B' if active_player == 'BLACK' else 'R'
            board[start_row_num][start_col_num] = '.'
        self.check_capture_helper(end_row_num, end_col_num)
        self.change_turn()
        self.check_for_win()
        return True

    def check_capture_helper(self, row, col):
        """
        takes the current players pawn's new position on the board and checks for captures
        """
        board = self.get_board()

        opponent = self.get_opponent()

        if row < 8 and board[row + 1][col] == opponent:
            self.rec_check_captures(row+1, col, 'down')

        if row > 1 and board[row - 1][col] == opponent:
            self.rec_check_captures(row-1, col, 'up')

        if col < 8 and board[row][col + 1] == opponent:
            self.rec_check_captures(row, col+1, 'right')

        if col > 1 and board[row][col - 1] == opponent:
            self.rec_check_captures(row, col-1, 'left')

        if row == 1 and board[row-1][col] == opponent:
            self.rec_check_captures(row-1, col, 'right')
            self.rec_check_captures(row - 1, col, 'left')

        if col == 7 and board[row][col+1] == opponent:
            self.rec_check_captures(row, col+1, 'down')
            self.rec_check_captures(row, col + 1, 'up')

        if col == 1 and board[row][col-1] == opponent:
            self.rec_check_captures(row, col-1, 'down')
            self.rec_check_captures(row, col - 1, 'up')

        if row == 7 and board[row+1][col] == opponent:
            self.rec_check_captures(row - 1, col, 'right')
            self.rec_check_captures(row - 1, col, 'left')

        # self.change_turn()
        # self.check_for_win()
        # return True

    def rec_check_captures(self, row, col, direction):

        board = self.get_board()
        opponent = self.get_opponent()
        player = self.get_curr_player_turn()

        if direction == 'down':
            # top right corner
            if row == 0 and col == 8 and board[row+1][col] == player:
                board[row][col] = '.'
                self.inc_captured_pieces()
                return
            # top left corner
            if row == 0 and col == 0 and board[row+1][col] == player:
                board[row][col] = '.'
                self.inc_captured_pieces()
                return

            if row+1 > 8 or board[row+1][col] == '.':
                return

            if board[row+1][col] == player:
                remove_pieces = True
                while remove_pieces:
                    if board[row][col] == player:
                        break
                    board[row][col] = '.'
                    self.inc_captured_pieces()
                    row -= 1
                return

            return self.rec_check_captures(row+1, col, 'down')

        if direction == 'up':
            # bottom right corner
            if row == 8 and col == 8 and board[row - 1][col] == player:
                board[row][col] = '.'
                self.inc_captured_pieces()
                return
            # bottom left corner
            if row == 8 and col == 0 and board[row - 1][col] == player:
                board[row][col] = '.'
                self.inc_captured_pieces()
                return

            if row-1 < 0 or board[row - 1][col] == '.':
                return

            if board[row - 1][col] == player:
                remove_pieces = True
                while remove_pieces:
                    if board[row][col] == player:
                        break
                    board[row][col] = '.'
                    self.inc_captured_pieces()
                    row += 1
                return

            return self.rec_check_captures(row - 1, col, 'up')

        if direction == 'right':
            # top left
            if row == 0 and col == 0 and board[row][col+1] == player:
                board[row][col] = '.'
                self.inc_captured_pieces()
                return
            # bottom left
            if row == 8 and col == 0 and board[row][col+1] == player:
                board[row][col] = '.'
                self.inc_captured_pieces()
                return

            if col+1 > 8 or board[row][col+1] == '.':
                return

            if board[row][col+1] == player:
                remove_pieces = True
                while remove_pieces:
                    if board[row][col] == player:
                        break
                    board[row][col] = '.'
                    self.inc_captured_pieces()
                    col -= 1
                return

            return self.rec_check_captures(row, col+1, 'right')

        if direction == 'left':
            # top right
            if row == 0 and col == 8 and board[row][col-1] == player:
                board[row][col] = '.'
                self.inc_captured_pieces()
                return
            # bottom right
            if row == 8 and col == 8 and board[row][col-1] == player:
                board[row][col] = '.'
                self.inc_captured_pieces()
                return

            if col-1 < 0 or board[row][col-1] == '.':
                return

            if board[row][col-1] == player:
                remove_pieces = True
                while remove_pieces:
                    if board[row][col] == player:
                        break
                    board[row][col] = '.'
                    self.inc_captured_pieces()
                    col += 1
                return

            return self.rec_check_captures(row, col-1, 'left')

    def check_for_win(self):
        opponent = 'RED' if self.get_opponent() == 'R' else 'BLACK'
        if self.get_num_captured_pieces(opponent) >= 8:
            self.set_game_state("BLACK_WON") if opponent == 'RED' else self.set_game_state("RED_WON")
        return


game = HasamiShogiGame()
move_result = game.make_move('i6', 'e3')
print(game.get_active_player())
print(game.get_square_occupant('a4'))
print(game.get_game_state())
