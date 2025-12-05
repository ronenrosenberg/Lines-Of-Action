"""Tests for the Piece class."""

from lines_of_action.piece import Piece


def test_different_pieces():
    """Test that different piece instances are not equal."""
    first = Piece("black", (1, 2))
    second = Piece("black", (1, 2))
    assert first != second


def test_pieces_team():
    """Test that get_team returns the correct team."""
    piece = Piece("black", (1, 2))
    team = piece.get_team()
    assert team == "black"


def test_location_pieces():
    """Test that get_location returns the correct location."""
    piece = Piece("black", (1, 2))
    location = piece.get_location()
    assert location == (1, 2)


def test_set_location():
    """Test that set_location updates the piece location."""
    piece = Piece("white", (1, 2))
    piece.set_location((3, 4))
    assert piece.get_location() == (3, 4)


def test_is_same_team():
    """Test that is_same_team correctly identifies team membership."""
    piece1 = Piece("black", (1, 2))
    piece2 = Piece("black", (3, 4))
    piece3 = Piece("white", (5, 6))
    
    assert piece1.is_same_team(piece2) is True
    assert piece1.is_same_team(piece3) is False
