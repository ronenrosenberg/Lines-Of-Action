"""Piece module for Lines of Action game.

This module defines the Piece class representing individual game pieces.
"""

from typing import Tuple


class Piece:
    """Represents a game piece in Lines of Action.
    
    Attributes:
        team: The team color ('white' or 'black')
        location: The (x, y) coordinates on the board
    """
    
    def __init__(self, team: str, location: Tuple[int, int]) -> None:
        """Initialize a piece.
        
        Args:
            team: The team color ('white' or 'black')
            location: The (x, y) coordinates on the board
        """
        self.team = team
        self.location = location
    
    def get_team(self) -> str:
        """Return the team of the piece.
        
        Returns:
            The team color ('white' or 'black')
        """
        return self.team
    
    def is_same_team(self, other: 'Piece') -> bool:
        """Check if this piece is on the same team as another piece.
        
        Args:
            other: Another piece to compare with
            
        Returns:
            True if both pieces are on the same team, False otherwise
        """
        return self.team == other.team
    
    def get_location(self) -> Tuple[int, int]:
        """Return the current location of the piece.
        
        Returns:
            A tuple (x, y) representing the board coordinates
        """
        return self.location
    
    def set_location(self, new_location: Tuple[int, int]) -> None:
        """Set a new location for the piece.
        
        Args:
            new_location: A tuple (x, y) representing the new board coordinates
        """
        self.location = new_location
