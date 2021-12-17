import pygame as pg
from constants import WHITE, BLACK, RED, ROWS, COLS, SQUARE_SIZE
from piece import Piece


class Board:
    def __init__(self):
        """
        creates the shogi board
        """
        self.board = []
        self.create_board()

    def get_board(self):
        return self.board

    def draw_board(self, win):

        win.fill(WHITE)
        for row in range(ROWS):
            for col in range(ROWS):
                pg.draw.rect(win, BLACK, pg.Rect(row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 2)

    def create_board(self):
        self.board.append([Piece(0, col, RED) for col in range(9)])
        for i in range(7):
            self.board.append([0 for space in range(9)])
        self.board.append([Piece(8, col, BLACK) for col in range(9)])

    def draw(self, win):
        self.draw_board(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def get_piece(self, row, col):
        return self.board[row][col]

    def get_valid_moves(self, piece):
        moves = []
        row = piece.row
        col = piece.col
        down = piece.row + 1
        right = piece.col + 1
        up = piece.row - 1
        left = piece.col - 1
        while down < 9:
            if self.board[down][col] == 0:
                moves.append((down, col))
                down += 1
            else:
                break
        while up >= 0:
            if self.board[up][col] == 0:
                moves.append((up, col))
                up -= 1
            else:
                break
        while right < 9:
            if self.board[row][right] == 0:
                moves.append((row, right))
                right += 1
            else:
                break
        while left >= 0:
            if self.board[row][left] == 0:
                moves.append((row, left))
                left -= 1
            else:
                break
        return moves