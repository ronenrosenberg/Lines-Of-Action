# Lines of Action

A graphical implementation of the strategic board game [Lines of Action](https://en.wikipedia.org/wiki/Lines_of_Action).

> **Note**: This project has been restructured. The old root-level Python files (`Board.py`, `Piece.py`, `LinesOfAction.py`, `*_test.py`) are deprecated. Please use the new `src/` structure going forward.

## About the Game

Lines of Action is a two-player abstract strategy board game. Players move their pieces in a line (horizontally, vertically, or diagonally) by exactly as many spaces as there are pieces of either color on that line. The goal is to connect all your pieces into a single contiguous group.

## Features

- Clean, object-oriented Python implementation
- Graphical interface using stddraw
- Move validation and win detection
- Two-player hot-seat gameplay

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- stddraw library (note: this may need to be installed manually as it's not available on PyPI)

### Install from source

```bash
# Clone the repository
git clone https://github.com/ronenrosenberg/Lines-Of-Action.git
cd Lines-Of-Action

# Install the package
pip install -e .

# Note: stddraw is required to run the game but is not available on PyPI
# You may need to install it manually if it's not already available
```

## Usage

### Running the game

After installation, you can run the game in several ways:

```bash
# If installed with pip
lines-of-action

# Or run directly with Python
python -m lines_of_action.game

# Or from the src directory
cd src
python -m lines_of_action.game
```

### How to Play

1. **Black starts first**
2. Click on a piece of your color to select it
3. Valid moves will be highlighted in yellow
4. Click on a highlighted square to move the piece
5. **Win condition**: Connect all your pieces into a single contiguous group
6. Pieces can capture opponent pieces by landing on their square

### Game Rules

- Pieces move in straight lines (horizontal, vertical, or diagonal)
- A piece moves exactly as many spaces as there are total pieces (both colors) in that line
- Pieces can jump over friendly pieces but not over enemy pieces
- Pieces can capture enemy pieces by landing on them
- The first player to connect all their pieces wins

## Development

### Running Tests

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run tests with coverage
pytest --cov=src/lines_of_action --cov-report=html
```

### Code Quality

```bash
# Format code with black
black src/ tests/

# Lint with flake8
flake8 src/ tests/

# Type checking with mypy
mypy src/
```

## Project Structure

```
Lines-Of-Action/
├── src/
│   └── lines_of_action/
│       ├── __init__.py
│       ├── game.py          # Main game logic and UI
│       ├── board.py         # Board state and move logic
│       └── piece.py         # Piece representation
├── tests/
│   ├── test_board.py
│   └── test_piece.py
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── setup.py                 # Package setup
├── pyproject.toml          # Build configuration
└── README.md               # This file
```

## Authors

- Suri Castro
- Ronen Rosenberg

## License

MIT License - feel free to use this code for learning or personal projects.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Acknowledgments

- Based on the classic Lines of Action board game
- Uses the stddraw library for graphics rendering
