"""Board module for Lines of Action game.

This module defines the Board class that manages the game state and move logic.
"""

from typing import List, Tuple, Optional
from .piece import Piece


class Board:
    """Represents the game board for Lines of Action.
    
    Attributes:
        size: The size of the board (default 10x10)
        board: A 2D list representing the game board
    """
    
    def __init__(self, size: int = 10) -> None:
        """Initialize a board of the specified size for the game.
        
        Args:
            size: The size of the board (default 10)
        """
        self.size = size
        # Create board
        self.board = [[None for i in range(size)] for j in range(size)]
        # Place pieces on board
        for i in range(1, size - 1):
            self.board[0][i] = Piece("black", (0, i))
            self.board[size - 1][i] = Piece("black", (size - 1, i))
            self.board[i][0] = Piece("white", (i, 0))
            self.board[i][size - 1] = Piece("white", (i, size - 1))
        
        # Variables for recursive_piece_search()
        self._blacklist: List[Piece] = []
        self._total_connected_pieces: int = 0
    
    def get_board(self) -> List[List[Optional[Piece]]]:
        """Return the board as a 2D array.
        
        Returns:
            A 2D list representing the game board
        """
        return self.board
    
    def move(self, piece: Piece, new_location_tuple: Tuple[int, int]) -> None:
        """Move a piece from one location to another.
        
        Args:
            piece: The piece to move
            new_location_tuple: The (x, y) coordinates of the destination
        """
        # Old and new locations
        old_x, old_y = piece.get_location()
        x, y = new_location_tuple

        # Move piece
        self.board[old_x][old_y] = None
        self.board[x][y] = piece

        # Correct piece's location attribute
        piece.set_location(new_location_tuple)

    def _count_pieces_in_line(
        self, 
        piece: Piece, 
        dx: int, 
        dy: int
    ) -> int:
        """Count the number of pieces in a line (row, column, or diagonal).
        
        Args:
            piece: The piece to count from
            dx: The x-direction delta (-1, 0, or 1)
            dy: The y-direction delta (-1, 0, or 1)
            
        Returns:
            The number of pieces in the specified line
        """
        x, y = piece.get_location()
        counter = 0
        
        # Start from the beginning of the line
        start_x, start_y = x, y
        while 0 <= start_x - dx < self.size and 0 <= start_y - dy < self.size:
            start_x -= dx
            start_y -= dy
        
        # Count all pieces in the line
        curr_x, curr_y = start_x, start_y
        while 0 <= curr_x < self.size and 0 <= curr_y < self.size:
            if self.board[curr_x][curr_y] is not None:
                counter += 1
            curr_x += dx
            curr_y += dy
        
        return counter

    def num_row(self, piece: Piece) -> int:
        """Return the number of pieces in a row as an integer.
        
        Args:
            piece: The piece to count from
            
        Returns:
            The number of pieces in the row
        """
        return self._count_pieces_in_line(piece, 0, 1)

    def num_col(self, piece: Piece) -> int:
        """Return the number of pieces in a column as an integer.
        
        Args:
            piece: The piece to count from
            
        Returns:
            The number of pieces in the column
        """
        return self._count_pieces_in_line(piece, 1, 0)
    
    def num_pos_diagonal(self, piece: Piece) -> int:
        """Return the number of pieces in a positive diagonal as an integer.
        
        Args:
            piece: The piece to count from
            
        Returns:
            The number of pieces in the positive diagonal
        """
        return self._count_pieces_in_line(piece, 1, 1)

    def num_neg_diagonal(self, piece: Piece) -> int:
        """Return the number of pieces in a negative diagonal as an integer.
        
        Args:
            piece: The piece to count from
            
        Returns:
            The number of pieces in the negative diagonal
        """
        return self._count_pieces_in_line(piece, 1, -1)
    
    def team_total_pieces(self) -> Tuple[int, int]:
        """Return the total number of pieces for each team.
        
        Returns:
            A tuple of (num_white, num_black)
        """
        num_white, num_black = 0, 0
        for x in range(self.size):
            for y in range(self.size):
                square = self.board[x][y]
                if square is not None:
                    if square.get_team() == "white":
                        num_white += 1
                    else:
                        num_black += 1
        return (num_white, num_black)
    
    def _recursive_piece_search(self, piece: Piece) -> None:
        """Alter the value of total, counting the sum of a group of connected pieces.
        
        This is a helper method for find_connected_piece_size().
        
        Args:
            piece: The piece to start searching from
        """
        current_piece_x, current_piece_y = piece.get_location()
        
        # Check all adjacent squares (3x3 surrounding)
        for x in range(current_piece_x - 1, current_piece_x + 2):
            for y in range(current_piece_y - 1, current_piece_y + 2):
                # Make sure we're checking possible indices
                if 0 <= x < self.size and 0 <= y < self.size:
                    # If square has a piece, hasn't been counted, and is same team
                    if (
                        self.board[x][y] is not None
                        and self.board[x][y] not in self._blacklist
                        and piece.is_same_team(self.board[x][y])
                    ):
                        self._blacklist.append(self.board[x][y])
                        self._recursive_piece_search(self.board[x][y])
                        self._total_connected_pieces += 1

    def find_connected_piece_size(self, team: str) -> int:
        """Find the size of the largest connected group of pieces for a team.
        
        Args:
            team: The team color ('white' or 'black')
            
        Returns:
            The number of connected pieces of the given team
        """
        # Get a piece on the board of the specified team
        piece = None
        for x in self.board:
            for y in x:
                if y is not None and y.get_team() == team:
                    piece = y
                    break
            if piece is not None:
                break
        
        if piece is None:
            return 0
        
        # Find the number of contiguous pieces
        self._recursive_piece_search(piece)

        total = self._total_connected_pieces

        # Reset counters
        self._total_connected_pieces = 0
        self._blacklist = []

        return total
    
    def range(self, piece: Piece) -> List[Tuple[int, int]]:
        """Return a list of all locations that a piece can move to.
        
        Args:
            piece: The piece to get valid moves for
            
        Returns:
            A list of (x, y) tuples representing valid move locations
        """
        available = (
            self._range_direction(piece, 0, 1) +   # column
            self._range_direction(piece, 1, 0) +   # row
            self._range_direction(piece, 1, 1) +   # positive diagonal
            self._range_direction(piece, 1, -1)    # negative diagonal
        )
        return available

    def _range_direction(
        self, 
        piece: Piece, 
        dx: int, 
        dy: int
    ) -> List[Tuple[int, int]]:
        """Return the locations a piece can jump to in a given direction.
        
        Args:
            piece: The piece to check moves for
            dx: The x-direction delta (0 or 1)
            dy: The y-direction delta (-1, 0, or 1)
            
        Returns:
            A list of valid (x, y) move locations in the given direction
        """
        x, y = piece.get_location()
        available = []
        
        # Count pieces in this direction
        if dx == 0:  # column
            count = self.num_col(piece)
        elif dy == 0:  # row
            count = self.num_row(piece)
        elif dx == 1 and dy == 1:  # positive diagonal
            count = self.num_pos_diagonal(piece)
        else:  # negative diagonal (dx == 1, dy == -1)
            count = self.num_neg_diagonal(piece)
        
        # Check both positive and negative directions
        for direction in [1, -1]:
            new_x = x + direction * count * dx
            new_y = y + direction * count * dy
            
            # Check if destination is in range
            if 0 <= new_x < self.size and 0 <= new_y < self.size:
                dest_piece = self.board[new_x][new_y]
                # Can move to empty square or enemy piece
                if dest_piece is None or dest_piece.get_team() != piece.get_team():
                    # Check if path is blocked by enemy pieces
                    blocked = False
                    for i in range(1, count):
                        check_x = x + direction * i * dx
                        check_y = y + direction * i * dy
                        if 0 <= check_x < self.size and 0 <= check_y < self.size:
                            blocking_piece = self.board[check_x][check_y]
                            if (
                                blocking_piece is not None 
                                and blocking_piece.get_team() != piece.get_team()
                            ):
                                blocked = True
                                break
                    
                    if not blocked:
                        available.append((new_x, new_y))
        
        return available
