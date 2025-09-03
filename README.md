# Python Chess Engine with Pygame

A complete 2-player chess game built from scratch in Python. This project features a robust, object-oriented chess engine that handles all game logic, integrated with an interactive graphical user interface (GUI) built using Pygame.

The engine is designed for correctness and efficiency, implementing advanced move validation that considers pins and checks, along with all special moves including castling, en passant, and pawn promotion.

---

# ✨ Core Features

This chess engine supports a comprehensive set of features for a complete gameplay experience:

- **Full Ruleset Implementation**: Accurately handles all standard and special chess moves:
  - Pawn Promotion (auto-promotes to Queen)
  - Castling (king-side and queen-side)
  - En Passant
- **Advanced Move Validation**: The engine uses an efficient algorithm to generate only legal moves by first identifying all pins and checks on the king.
- **Game State Detection**: Robust logic to correctly identify check, checkmate, and stalemate conditions.
- **Interactive Gameplay**:
  - Undo Move: Step backward through the game history by pressing 'Z'.
  - Move Log: A complete history of moves is tracked internally.
- **Clean GUI**: A simple and intuitive graphical interface built with Pygame for piece movement and game interaction.

---

# 🛠️ Technical Deep Dive

- **Object-Oriented Architecture**: The project is built using Object-Oriented Programming (OOP) principles. The `GameState` class manages the board, move history, and all game rules, while the `Move` class encapsulates individual move details, making the code modular and maintainable.
- **Efficient Move Generation**: Unlike brute-force approaches, the engine's `getValidMoves()` function first calculates all pins and checks. This allows it to generate only legal moves for each piece, significantly improving performance by avoiding the need to make and undo thousands of illegal moves.
- **Clean Separation of Concerns**: The application is split into two logical parts:
  - `chessengine.py`: Contains all the game's state, rules, and logic.
  - `chessmain.py`: Handles all visuals, user input (mouse/keyboard), and the main game loop.

---

# 🚀 Getting Started

Follow these steps to get the game running on your local machine.

## ✅ Prerequisites

- Python 3.8 or later
- Pygame library

## 📦 Installation

### Clone the Repository
```bash
git clone https://github.com/hacketthadwin/ChessEngine.git
cd ChessEngine
```

### Install Dependencies

This project uses Pygame for the graphical interface. Install it using pip:

```bash
pip install pygame
```

### Ensure Assets are Present

Make sure you have a folder named `Chess pieces` in the root directory containing all the `.png` images for the chess pieces (e.g., `wp.png`, `bR.png`).

---

# ▶️ Running the Game

Execute the main Python script to start the game:

```bash
python chessmain.py
```

# 🕹️ How to Play

- **Select a Piece**: Click on one of your pieces.
- **Move a Piece**: Click on a valid destination square to move the selected piece.
- **Undo Move**: Press the `Z` key to undo the last move made.

---

# 📄 License

This project is licensed under the MIT License. See the LICENSE file for more details.

