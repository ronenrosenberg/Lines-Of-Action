"""Tests for the Board class."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from lines_of_action.board import Board


def test_different_boards():
    """Test that different board instances are not equal."""
    first = Board(10)
    second = Board(10)
    assert first != second


def test_num_row():
    """Test that num_row counts pieces in a row correctly."""
    board = Board(10)
    piece = board.get_board()[0][2]
    answer = board.num_row(piece)
    assert answer == 8


def test_num_col():
    """Test that num_col counts pieces in a column correctly."""
    board = Board(10)
    piece = board.get_board()[0][2]
    answer = board.num_col(piece)
    assert answer == 2


def test_num_pos_diagonal():
    """Test that num_pos_diagonal counts pieces correctly."""
    board = Board(10)
    piece = board.get_board()[2][0]
    answer = board.num_pos_diagonal(piece)
    assert answer == 2


def test_num_neg_diagonal():
    """Test that num_neg_diagonal counts pieces correctly."""
    board = Board(10)
    piece = board.get_board()[2][0]
    answer = board.num_neg_diagonal(piece)
    assert answer == 2


def test_board_initialization():
    """Test that the board is initialized with correct piece placement."""
    board = Board(8)
    # Check that corners are empty
    assert board.get_board()[0][0] is None
    assert board.get_board()[7][7] is None
    # Check that pieces are placed correctly
    assert board.get_board()[0][1] is not None
    assert board.get_board()[0][1].get_team() == "black"


def test_move():
    """Test that move correctly updates piece location."""
    board = Board(8)
    piece = board.get_board()[0][1]
    old_location = piece.get_location()
    new_location = (2, 3)
    
    board.move(piece, new_location)
    
    # Check old location is empty
    assert board.get_board()[old_location[0]][old_location[1]] is None
    # Check new location has the piece
    assert board.get_board()[new_location[0]][new_location[1]] == piece
    # Check piece knows its new location
    assert piece.get_location() == new_location


def test_team_total_pieces():
    """Test that team_total_pieces counts correctly."""
    board = Board(8)
    white_count, black_count = board.team_total_pieces()
    # Each team starts with 6 pieces on an 8x8 board
    assert white_count == 12
    assert black_count == 12
