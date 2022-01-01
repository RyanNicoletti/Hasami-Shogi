import pygame as pg
from constants import RED, BLACK, BLUE, SQUARE_SIZE
from board import Board
from piece import Piece
from .base_state import BaseState


class Hasamishogigame(BaseState):
    """
    represents the board game hasami shogi
    """

    def __init__(self, win):
        super().__init__()
        """
        Creates a new instance of the hasami shogi game with a new board.
        Initializes current player as black and opposing player as red (black goes first).
        Initializes captured pieces (count) to 0 for both players
        """

        self._init()
        self.win = win
        self.store_pos = []
        self.red_count = 0
        self.black_count = 0
        self.next_state = "GAME_OVER"

    def _init(self):
        self.selected = None
        self.board = Board()
        self.active_player = BLACK
        self.opponent = RED
        self.valid_moves = {}

    def draw(self, surface):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True

        def get_row_col_from_mouse(pos):
            x, y = pos
            row = y // SQUARE_SIZE  # invert, SQUARE_SIZE = WIDTH//COLS, width=800, cols = 9
            col = x // SQUARE_SIZE
            return row, col

        if event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            row, col = get_row_col_from_mouse(pos)
            self.select_move(row, col)

    def inc_captured_pieces(self):
        """
        increases the number of the current opponents captured pieces by one
        """
        if self.opponent == RED:
            self.red_count += 1
        else:
            self.black_count += 1

    def change_turn(self):
        """
        changes the current active player to the opposite color
        and changes the opponent to the opposite color
        """
        self.valid_moves = {}
        if self.active_player == BLACK:
            self.active_player = RED
            self.opponent = BLACK
        else:
            self.active_player = BLACK
            self.opponent = RED

    def check_for_win(self):
        """
        checks for winner, if winner, update state
        """
        if self.opponent == RED and self.red_count >= 8:
            self.persist["black_wins"] = True
            self.done = True
        elif self.opponent == BLACK and self.black_count >= 8:
            self.persist["red_wins"] = True
            self.done = True

    def select_move(self, row, col):
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.active_player:
            self.store_pos = [(row, col)]
            self.selected = None
        else:
            self.store_pos.append((row, col))
        if self.selected:
            start_row_num = self.store_pos[0][0]
            start_col_num = self.store_pos[0][1]
            end_row_num = self.store_pos[1][0]
            end_col_num = self.store_pos[1][1]
            result = self.make_move(start_row_num, start_col_num, end_row_num, end_col_num)
            if not result or (piece != 0 and piece.color != self.active_player):
                if self.store_pos:
                    del self.store_pos[-1]
            else:
                self.selected = None
                self.store_pos.clear()

        if piece != 0 and piece.color == self.active_player:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)

            return True
        return False

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pg.draw.circle(self.win, BLUE,
                           (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def make_move(self, start_row_num, start_col_num, end_row_num, end_col_num):

        board = self.board.get_board()

        # if the end position is off the board, return False
        if end_row_num < 0 or end_row_num > 8 or end_col_num < 0 or end_col_num > 8:
            return False

        # check for only verticle and horizontal movement
        if end_row_num != start_row_num and end_col_num != start_col_num:
            return False

        if start_row_num > end_row_num:
            # move up
            start_pos = end_row_num
            for i in reversed(range(start_row_num - end_row_num)):
                if board[i + start_pos][start_col_num] != 0:
                    return False

        if end_row_num > start_row_num:
            # move down
            start_pos = start_row_num + 1
            for i in range(end_row_num - start_row_num):
                if board[i + start_pos][start_col_num] != 0:
                    return False

        if end_col_num > start_col_num:
            # move right
            start_pos = start_col_num + 1
            for i in range(end_col_num - start_col_num):
                if board[start_row_num][i + start_pos] != 0:
                    return False

        if start_col_num > end_col_num:
            # move left
            start_pos = end_col_num
            for i in reversed(range(start_col_num - end_col_num)):
                if board[start_row_num][i + start_pos] != 0:
                    return False

        board[end_row_num][end_col_num] = Piece(end_row_num, end_col_num, self.active_player)
        board[start_row_num][start_col_num] = 0

        self.check_capture_helper(end_row_num, end_col_num)
        self.check_for_win()
        self.change_turn()
        return True

    def check_capture_helper(self, row, col):
        """
        takes two integers, corresponding to the row and column of the pawns current position
        on the board (after making a move).
        Checks for neighboring opponent pawns in all directions.
        If found, call the function rec_check_captures with the position of the opponents pawn
        to be potentially captured.
        Accounts for cases where the pawn is captured in the corner of the board
        """
        board = self.board.get_board()

        opponent = self.opponent

        if row < 8 and board[row + 1][col] != 0 and self.board.get_piece(row+1, col).color == opponent:
            self.rec_check_captures(row + 1, col, 'down')

        if row > 1 and board[row - 1][col] != 0 and self.board.get_piece(row-1, col).color == opponent: #== self.board.get_piece(row-1, col):
            self.rec_check_captures(row - 1, col, 'up')

        if col < 8 and board[row][col + 1] != 0 and self.board.get_piece(row, col+1).color == opponent: #== self.board.get_piece(row, col+1):
            self.rec_check_captures(row, col + 1, 'right')

        if col > 1 and board[row][col - 1] != 0 and self.board.get_piece(row, col-1).color == opponent:
            self.rec_check_captures(row, col - 1, 'left')

        if row == 1 and board[row - 1][col] != 0 and self.board.get_piece(row-1, col).color == opponent:
            self.rec_check_captures(row - 1, col, 'right')
            self.rec_check_captures(row - 1, col, 'left')

        if col == 7 and board[row][col + 1] != 0 and self.board.get_piece(row, col+1).color == opponent:
            self.rec_check_captures(row, col + 1, 'down')
            self.rec_check_captures(row, col + 1, 'up')

        if col == 1 and board[row][col - 1] != 0 and self.board.get_piece(row, col-1).color == opponent:
            self.rec_check_captures(row, col - 1, 'down')
            self.rec_check_captures(row, col - 1, 'up')

        if row == 7 and board[row + 1][col] != 0 and self.board.get_piece(row+1, col).color == opponent:
            self.rec_check_captures(row - 1, col, 'right')
            self.rec_check_captures(row - 1, col, 'left')
        return

    def rec_check_captures(self, row, col, direction):
        """
        takes the current position of the board which contains an enemy pawn,
        and the direction in which to travers the board to check for more
        enemy pieces to potentially capture.
        traverse the board in the given direction recursively.
        if an active players pawn is found, back track and capture all of
        the enemy pawns.
        Otherwise return.
        """
        board = self.board.get_board()
        opponent = self.opponent

        if direction == 'down':
            # top right corner
            if row == 0 and col == 8 and self.board.get_piece(row+1, col).color == self.active_player:
                board[row][col] = 0
                self.inc_captured_pieces()
                return
            # top left corner
            if row == 0 and col == 0 and self.board.get_piece(row+1, col).color == self.active_player:
                board[row][col] = 0
                self.inc_captured_pieces()
                return

            if row + 1 > 8 or board[row + 1][col] == 0:
                return

            piece = self.board.get_piece(row + 1, col)
            if piece.color == self.active_player:
                remove_pieces = True
                while remove_pieces:
                    piece = self.board.get_piece(row, col)
                    if piece != 0 and piece.color == self.active_player:
                        break
                    board[row][col] = 0
                    self.inc_captured_pieces()
                    row -= 1
                return

            return self.rec_check_captures(row + 1, col, 'down')

        if direction == 'up':
            # bottom right corner
            if row == 8 and col == 8 and self.board.get_piece(row-1, col).color == self.active_player:
                board[row][col] = 0
                self.inc_captured_pieces()
                return
            # bottom left corner
            if row == 8 and col == 0 and self.board.get_piece(row-1, col).color == self.active_player:
                board[row][col] = 0
                self.inc_captured_pieces()
                return

            if row - 1 < 0 or board[row - 1][col] == 0:
                return

            piece = self.board.get_piece(row-1, col)
            if piece.color == self.active_player:
                remove_pieces = True
                while remove_pieces:
                    piece = self.board.get_piece(row, col)
                    if piece != 0 and piece.color == self.active_player:
                        break
                    board[row][col] = 0
                    self.inc_captured_pieces()
                    row += 1
                return

            return self.rec_check_captures(row - 1, col, 'up')

        if direction == 'right':
            # top left corner
            if row == 0 and col == 0 and self.board.get_piece(row, col+1).color == self.active_player:
                board[row][col] = 0
                self.inc_captured_pieces()
                return
            # bottom left corner
            if row == 8 and col == 0 and self.board.get_piece(row, col+1).color == self.active_player:
                board[row][col] = 0
                self.inc_captured_pieces()
                return

            if col + 1 > 8 or self.board.get_piece(row, col + 1) == 0:
                return

            piece = self.board.get_piece(row, col+1)
            if piece.color == self.active_player:
                remove_pieces = True
                while remove_pieces:
                    piece = self.board.get_piece(row, col)
                    if piece != 0 and piece.color == self.active_player:
                        break
                    board[row][col] = 0
                    self.inc_captured_pieces()
                    col -= 1
                return

            return self.rec_check_captures(row, col + 1, 'right')

        if direction == 'left':
            # top right corner
            if row == 0 and col == 8 and self.board.get_piece(row, col-1).color == self.active_player:
                board[row][col] = 0
                self.inc_captured_pieces()
                return
            # bottom right corner
            if row == 8 and col == 8 and self.board.get_piece(row, col-1).color == self.active_player:
                board[row][col] = 0
                self.inc_captured_pieces()
                return

            if col - 1 < 0 or board[row][col - 1] == 0:
                return

            piece = self.board.get_piece(row, col - 1)
            if piece.color == self.active_player:
                remove_pieces = True
                while remove_pieces:
                    piece = self.board.get_piece(row, col)
                    if piece != 0 and piece.color == self.active_player:
                        break
                    board[row][col] = 0
                    self.inc_captured_pieces()
                    col += 1
                return

            return self.rec_check_captures(row, col - 1, 'left')
