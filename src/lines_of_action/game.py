"""Main game module for Lines of Action.

This module contains the main game logic and UI rendering.
"""

from typing import Optional, List, Tuple
from .board import Board
from .piece import Piece

try:
    import stddraw
except ImportError:
    stddraw = None
    print("Warning: stddraw not found. Install with: pip install stddraw")


# Constants
DEFAULT_SIZE = 8
PIECE_RADIUS_RATIO = 0.4
HIGHLIGHT_RADIUS_RATIO = 0.5
SQUARE_HIGHLIGHT_RATIO = 0.93
FRAME_DELAY = 0  # milliseconds


class LinesOfAction:
    """Main game class for Lines of Action.
    
    Attributes:
        board: The game board instance
        size: The size of the board
        side: The size of each square side
        half: Half the size of a square side
        state: Current game state ('idle', 'picking', 'moving')
        selected: Currently selected piece
        current_team: Current team's turn ('black' or 'white')
        legal_jumps: List of legal moves for the selected piece
    """
    
    def __init__(self, size: int = DEFAULT_SIZE) -> None:
        """Initialize the game.
        
        Args:
            size: The size of the board (default 8)
        """
        if stddraw is None:
            raise ImportError("stddraw is required to run the game")
        
        # The actual 2D array
        self.board = Board(size)

        # Useful for drawing
        self.size = size
        self.side = 1.0 / size
        self.half = self.side / 2.0

        # Logic variables
        self.state = "idle"
        self.selected: Optional[Piece] = None
        self.current_team = "black"
        self.legal_jumps: List[Tuple[int, int]] = []

    def display(self) -> None:
        """Draw a frame of the board in the current state."""
        stddraw.clear()

        # Blue background
        stddraw.setPenColor(stddraw.BOOK_LIGHT_BLUE)
        stddraw.filledSquare(0, 0, 1)
        
        # Draw the board
        self._draw_board()
        
        # Handle mouse interaction states
        if self.state != "idle":
            x = round((stddraw.mouseX() - self.half) / self.side)
            y = round((stddraw.mouseY() - self.half) / self.side)

            if self.state == "picking":
                self._handle_picking_state(x, y)
            elif self.state == "moving":
                self._handle_moving_state(x, y)
        
        # Update display (required for stddraw)
        stddraw.show(FRAME_DELAY)
    
    def _draw_board(self) -> None:
        """Draw all pieces and squares on the board."""
        for x in range(self.size):
            for y in range(self.size):
                square = self.board.get_board()[x][y]
                if square is not None:
                    self._draw_piece(x, y, square.get_team())
                # Draw black borders
                stddraw.setPenColor(stddraw.BLACK)
                stddraw.square(
                    x * self.side + self.half, 
                    y * self.side + self.half, 
                    self.half
                )
    
    def _draw_piece(self, x: int, y: int, team: str) -> None:
        """Draw a piece at the specified location.
        
        Args:
            x: X coordinate on the board
            y: Y coordinate on the board
            team: Team color ('white' or 'black')
        """
        color = stddraw.WHITE if team == "white" else stddraw.BLACK
        stddraw.setPenColor(color)
        radius = self.half / 0.5 * PIECE_RADIUS_RATIO
        stddraw.filledCircle(
            x * self.side + self.half, 
            y * self.side + self.half, 
            radius
        )
    
    def _draw_highlighted_piece(self, x: int, y: int, team: str) -> None:
        """Draw a highlighted piece at the specified location.
        
        Args:
            x: X coordinate on the board
            y: Y coordinate on the board
            team: Team color ('white' or 'black')
        """
        # Draw yellow highlight
        stddraw.setPenColor(stddraw.YELLOW)
        highlight_radius = self.half / 0.5 * HIGHLIGHT_RADIUS_RATIO
        stddraw.filledCircle(
            x * self.side + self.half, 
            y * self.side + self.half, 
            highlight_radius
        )
        # Draw piece on top
        self._draw_piece(x, y, team)
    
    def _handle_picking_state(self, x: int, y: int) -> None:
        """Handle the picking state when selecting a piece to move.
        
        Args:
            x: X coordinate of the mouse click
            y: Y coordinate of the mouse click
        """
        at_click_location = self.board.get_board()[x][y]
        
        # Make sure clicked square has a piece of the current team
        if (
            at_click_location is not None 
            and at_click_location.get_team() == self.current_team
        ):
            # Highlight selected piece
            self._draw_highlighted_piece(x, y, at_click_location.get_team())
            
            # Get and display legal moves
            self.legal_jumps = self.board.range(at_click_location)
            self._highlight_legal_moves()
            
            # Piece is "selected"
            self.selected = at_click_location
        else:
            # If no valid piece selected, go back to idle
            self.state = "idle"
    
    def _highlight_legal_moves(self) -> None:
        """Highlight all legal move locations for the selected piece."""
        for coord in self.legal_jumps:
            x, y = coord
            stddraw.setPenColor(stddraw.YELLOW)
            stddraw.filledSquare(
                x * self.side + self.half, 
                y * self.side + self.half, 
                self.half * SQUARE_HIGHLIGHT_RATIO
            )
            # Redraw piece if present at this location
            if self.board.get_board()[x][y] is not None:
                team = self.board.get_board()[x][y].get_team()
                self._draw_piece(x, y, team)
    
    def _handle_moving_state(self, x: int, y: int) -> None:
        """Handle the moving state when placing a selected piece.
        
        Args:
            x: X coordinate of the mouse click
            y: Y coordinate of the mouse click
        """
        jump_location = self.board.get_board()[x][y]
        
        # If clicking a different piece on the same team, switch selection
        if jump_location is not None and jump_location.is_same_team(self.selected):
            self.selected = self.board.get_board()[x][y]
            self.state = "picking"
        # If clicking on non-valid location, reset to idle
        elif (x, y) not in self.legal_jumps:
            self._reset_to_idle()
        # Otherwise move the piece and switch turns
        else:
            self.board.move(self.selected, (x, y))
            self._reset_to_idle()
            self._switch_turn()
    
    def _reset_to_idle(self) -> None:
        """Reset game state to idle."""
        self.state = "idle"
        self.selected = None
        self.legal_jumps = []
    
    def _switch_turn(self) -> None:
        """Switch to the opposite team's turn."""
        self.current_team = "white" if self.current_team == "black" else "black"
    
    def won(self) -> bool:
        """Check if the game has been won.
        
        Returns:
            True if a team has won, False otherwise
        """
        # Get total number of black and white pieces on board
        num_white, num_black = self.board.team_total_pieces()
        
        # Check if total pieces equals number in a contiguous bunch
        white_won = num_white == self.board.find_connected_piece_size("white")
        black_won = num_black == self.board.find_connected_piece_size("black")
        
        # Handle win states
        if white_won and black_won:
            print("Tie")
            return True
        elif white_won:
            print("White wins!")
            return True
        elif black_won:
            print("Black wins!")
            return True
        
        return False

    def play(self) -> None:
        """Execute one game loop iteration."""
        # Check if there has been a click since last time
        is_click = stddraw.mousePressed()

        # Condition from picking -> moving
        if is_click and self.selected is not None:
            self.state = "moving"
        # Condition from idle -> picking
        elif is_click:
            self.state = "picking"

        # Display the current game state
        self.display()

        # Check for win condition
        if self.won():
            quit()


def main() -> None:
    """Main entry point for the game."""
    game = LinesOfAction(DEFAULT_SIZE)
    while True:
        game.play()


if __name__ == "__main__":
    main()
