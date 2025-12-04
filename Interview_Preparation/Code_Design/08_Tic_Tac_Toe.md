# ⭕❌ PROBLEM 8: TIC TAC TOE GAME

### ⭐⭐⭐ **Design Tic Tac Toe with Clean OOP**

**Frequency:** MEDIUM at Atlassian
**Difficulty:** Easy-Medium
**Time to Solve:** 30-40 minutes
**Focus:** Game Logic, Win Detection, State Pattern, Extensibility

---

## 📋 Problem Statement

Design Tic Tac Toe game with:
- N×N board (3×3 default)
- 2 players (X and O)
- Win detection (row, column, diagonal)
- Support for human vs AI (extension)
- Undo/Redo functionality (extension)

**Core Requirements:**
- `make_move(row, col)`: Place current player's mark
- `check_winner()`: Detect if game is won
- `is_draw()`: Check for draw condition
- `reset()`: Start new game

**Constraints:**
- Board size: 3×3 to 10×10
- Two players alternating turns
- Win requires full row/column/diagonal
- No overwriting existing marks

---

## 🎯 INTERVIEW FLOW: Step-by-Step Guide

### **PHASE 1: Clarify Requirements (2-3 minutes)**

**SAY THIS:**
> "Before I start designing, let me clarify a few requirements:"

**Questions to Ask:**
1. "Board size - fixed 3×3 or configurable N×N?"
2. "Players - always 2? Human vs Human or vs AI?"
3. "Win condition - standard (full row/col/diagonal)?"
4. "Should we support undo/redo?"
5. "Do we need to track move history?"
6. "Is there a timer or is it turn-based?"

**WRITE DOWN the answers. This shows you're thorough.**

---

### **PHASE 2: Discuss Key Design Decisions (3-4 minutes)**

**SAY THIS:**
> "There's a key optimization opportunity for win detection."

#### **Win Detection: Naive vs Optimized**

```text
Naive Approach: O(N) per move
- After each move, scan entire row, column, and diagonals
- Total: O(N) time

Optimized Approach: O(1) per move ⭐
- Maintain counters for each row, column, and diagonal
- X adds +1, O adds -1
- Win when any counter reaches +N or -N
- Total: O(1) time
```

**Explain:**
> "I'll use the optimized approach. We track 4 things:
> - N row counters
> - N column counters
> - 1 main diagonal counter
> - 1 anti-diagonal counter
> 
> After each move, we only update the affected counters and check if any equals ±N."

---

### **PHASE 3: High-Level Design (2-3 minutes)**

**SAY THIS:**
> "Let me draw the class structure."

**Draw on whiteboard:**
```
┌─────────────────────────────────────────────────────────┐
│                   TicTacToeGame                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Game controller - state machine                │   │
│  │                                                  │   │
│  │  - board: Board                                 │   │
│  │  - current_player: Player                       │   │
│  │  - state: GameState                             │   │
│  │  - move_history: List[Move]                     │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  + make_move(row, col) → bool                          │
│  + undo() → bool                                       │
│  + reset() → void                                      │
└─────────────────────────────────────────────────────────┘

┌─────────────────────┐     ┌─────────────────────┐
│       Board         │     │      Player         │
├─────────────────────┤     ├─────────────────────┤
│ - grid: 2D array    │     │ X = "X"             │
│ - row_counts[]      │     │ O = "O"             │
│ - col_counts[]      │     │ EMPTY = " "         │
│ - diag_count        │     └─────────────────────┘
│ - anti_diag_count   │
├─────────────────────┤     ┌─────────────────────┐
│ + place(r, c, p)    │     │    GameState        │
│ + remove(r, c)      │     ├─────────────────────┤
│ + check_winner_at() │     │ IN_PROGRESS         │
└─────────────────────┘     │ X_WINS              │
                            │ O_WINS              │
                            │ DRAW                │
                            └─────────────────────┘
```

---

### **PHASE 4: Design Patterns & Principles (2 minutes)**

**SAY THIS:**
> "I'm following these design principles:"

#### **1. Single Responsibility Principle (SRP)** ⭐⭐⭐

| Class | Responsibility |
|-------|---------------|
| `Board` | Grid state, win detection |
| `TicTacToeGame` | Game rules, turn management |
| `Player` (Enum) | Player markers |
| `GameState` (Enum) | Game status |

---

#### **2. Open/Closed Principle (OCP)** ⭐⭐

```python
# Easy to add AI players without modifying game
class AIPlayer(ABC):
    @abstractmethod
    def get_move(self, board: Board) -> Tuple[int, int]:
        pass

class MinimaxAI(AIPlayer):
    def get_move(self, board: Board) -> Tuple[int, int]:
        # AI logic here
        pass
```

---

### **PHASE 5: Data Structures & Why (2 minutes)**

**SAY THIS:**
> "Let me explain my data structure choices."

| Data Structure | Used For | Why This Choice |
|----------------|----------|-----------------|
| `List[List[Player]]` | Grid | 2D indexing, simple |
| `List[int]` | Row/col counters | O(1) update |
| `int` | Diagonal counters | O(1) update |
| `Enum` | Player, GameState | Type safety |
| `List[Move]` | Move history | Undo/redo support |
| `dataclass` | Move | Clean data container |

**O(1) Win Detection Trick:**
> "Use integers: X = +1, O = -1
> Win when any counter reaches +N (X wins) or -N (O wins)
> This avoids scanning the entire row/column every move."

---

### **PHASE 6: Write the Code (15-20 minutes)**

**SAY THIS:**
> "Now let me implement this with O(1) win detection."

```python
"""
Tic Tac Toe - Low-Level Design
==============================
Clean OOP with O(1) win detection optimization.

Design Patterns:
- SRP: Board and Game separated
- OCP: AI players as extensions

Key Optimization:
- O(1) win detection using row/col/diagonal counters
- X = +1, O = -1, win when |sum| = N

Features:
- Configurable board size (N×N)
- Undo/redo support
- AI player interface
"""

from enum import Enum
from typing import Optional, List, Tuple
from dataclasses import dataclass
from abc import ABC, abstractmethod


# ============ Enums ============

class Player(Enum):
    """Player markers with integer values for counting."""
    X = 1      # +1 for counting
    O = -1     # -1 for counting
    EMPTY = 0
    
    def __str__(self):
        if self == Player.X:
            return "X"
        elif self == Player.O:
            return "O"
        return " "
    
    def opponent(self) -> 'Player':
        """Get the opponent player."""
        if self == Player.X:
            return Player.O
        elif self == Player.O:
            return Player.X
        return Player.EMPTY


class GameState(Enum):
    """Game states."""
    IN_PROGRESS = "in_progress"
    X_WINS = "x_wins"
    O_WINS = "o_wins"
    DRAW = "draw"


# ============ Move Record ============

@dataclass
class Move:
    """Represents a single move (for undo/redo)."""
    row: int
    col: int
    player: Player


# ============ Board Class ============

class Board:
    """
    Game board with O(1) win detection.
    
    Win Detection Optimization:
    - Maintain counters for rows, columns, diagonals
    - X adds +1, O adds -1
    - Win when any counter reaches ±N
    
    Why this works:
    - If X fills a row: counter = N (all +1)
    - If O fills a row: counter = -N (all -1)
    - Mixed row: counter between -N and N (no win)
    """
    
    def __init__(self, size: int = 3):
        if size < 3:
            raise ValueError("Board size must be at least 3")
        
        self.size = size
        self._grid: List[List[Player]] = [
            [Player.EMPTY for _ in range(size)] 
            for _ in range(size)
        ]
        self._move_count = 0
        
        # O(1) win detection counters
        self._row_counts = [0] * size      # +1 for X, -1 for O
        self._col_counts = [0] * size
        self._diag_count = 0               # Main diagonal (r == c)
        self._anti_diag_count = 0          # Anti-diagonal (r + c == size-1)
    
    def place(self, row: int, col: int, player: Player) -> bool:
        """
        Place a player's mark on the board.
        
        Returns: True if successful, False if invalid
        Time: O(1)
        """
        if not self._is_valid_position(row, col):
            return False
        
        if self._grid[row][col] != Player.EMPTY:
            return False
        
        self._grid[row][col] = player
        self._move_count += 1
        
        # Update counters for O(1) win detection
        delta = player.value  # +1 for X, -1 for O
        self._row_counts[row] += delta
        self._col_counts[col] += delta
        
        if row == col:  # Main diagonal
            self._diag_count += delta
        if row + col == self.size - 1:  # Anti-diagonal
            self._anti_diag_count += delta
        
        return True
    
    def remove(self, row: int, col: int) -> bool:
        """
        Remove a mark (for undo).
        
        Time: O(1)
        """
        if not self._is_valid_position(row, col):
            return False
        
        player = self._grid[row][col]
        if player == Player.EMPTY:
            return False
        
        # Reverse the counter updates
        delta = player.value
        self._row_counts[row] -= delta
        self._col_counts[col] -= delta
        
        if row == col:
            self._diag_count -= delta
        if row + col == self.size - 1:
            self._anti_diag_count -= delta
        
        self._grid[row][col] = Player.EMPTY
        self._move_count -= 1
        return True
    
    def get(self, row: int, col: int) -> Player:
        """Get player at position."""
        if not self._is_valid_position(row, col):
            return Player.EMPTY
        return self._grid[row][col]
    
    def _is_valid_position(self, row: int, col: int) -> bool:
        """Check if position is within bounds."""
        return 0 <= row < self.size and 0 <= col < self.size
    
    def is_full(self) -> bool:
        """Check if board is completely filled."""
        return self._move_count == self.size * self.size
    
    def check_winner_at(self, row: int, col: int) -> Optional[Player]:
        """
        O(1) win check after a move at (row, col).
        
        Only checks lines affected by this position.
        
        Time: O(1) - just 4 comparisons!
        """
        target = self.size  # Win requires N in a row
        
        # Check row
        if abs(self._row_counts[row]) == target:
            return Player.X if self._row_counts[row] > 0 else Player.O
        
        # Check column
        if abs(self._col_counts[col]) == target:
            return Player.X if self._col_counts[col] > 0 else Player.O
        
        # Check main diagonal (only if position is on it)
        if row == col and abs(self._diag_count) == target:
            return Player.X if self._diag_count > 0 else Player.O
        
        # Check anti-diagonal (only if position is on it)
        if row + col == self.size - 1 and abs(self._anti_diag_count) == target:
            return Player.X if self._anti_diag_count > 0 else Player.O
        
        return None
    
    def check_winner(self) -> Optional[Player]:
        """
        Check for winner (slower, checks all).
        
        Time: O(N) - use check_winner_at() for O(1)
        """
        # Check rows and columns
        for i in range(self.size):
            if abs(self._row_counts[i]) == self.size:
                return Player.X if self._row_counts[i] > 0 else Player.O
            if abs(self._col_counts[i]) == self.size:
                return Player.X if self._col_counts[i] > 0 else Player.O
        
        # Check diagonals
        if abs(self._diag_count) == self.size:
            return Player.X if self._diag_count > 0 else Player.O
        if abs(self._anti_diag_count) == self.size:
            return Player.X if self._anti_diag_count > 0 else Player.O
        
        return None
    
    def get_empty_cells(self) -> List[Tuple[int, int]]:
        """Get all empty cell positions."""
        return [
            (row, col)
            for row in range(self.size)
            for col in range(self.size)
            if self._grid[row][col] == Player.EMPTY
        ]
    
    def reset(self) -> None:
        """Reset the board to initial state."""
        for row in range(self.size):
            for col in range(self.size):
                self._grid[row][col] = Player.EMPTY
        
        self._row_counts = [0] * self.size
        self._col_counts = [0] * self.size
        self._diag_count = 0
        self._anti_diag_count = 0
        self._move_count = 0
    
    def display(self) -> str:
        """Get string representation."""
        lines = []
        separator = "───┼" * (self.size - 1) + "───"
        
        for row in range(self.size):
            row_str = " │ ".join(str(self._grid[row][col]) for col in range(self.size))
            lines.append(f" {row_str} ")
            if row < self.size - 1:
                lines.append(separator)
        
        return "\n".join(lines)
    
    def __str__(self):
        return self.display()


# ============ Game Class ============

class TicTacToeGame:
    """
    Main game controller.
    
    Responsibilities:
    - Manage game state machine
    - Handle turns
    - Validate moves
    - Support undo/redo
    
    Example:
        >>> game = TicTacToeGame(board_size=3)
        >>> game.make_move(0, 0)  # X plays
        >>> game.make_move(1, 1)  # O plays
        >>> game.undo()          # Undo O's move
    """
    
    def __init__(self, board_size: int = 3):
        self._board = Board(board_size)
        self._current_player = Player.X
        self._state = GameState.IN_PROGRESS
        self._move_history: List[Move] = []
        self._redo_stack: List[Move] = []
    
    @property
    def current_player(self) -> Player:
        return self._current_player
    
    @property
    def state(self) -> GameState:
        return self._state
    
    @property
    def board(self) -> Board:
        return self._board
    
    def make_move(self, row: int, col: int) -> bool:
        """
        Make a move at the specified position.
        
        Returns: True if move successful
        Time: O(1) with optimized win detection
        """
        if self._state != GameState.IN_PROGRESS:
            return False
        
        if not self._board.place(row, col, self._current_player):
            return False
        
        # Record move for undo
        move = Move(row, col, self._current_player)
        self._move_history.append(move)
        self._redo_stack.clear()  # Clear redo on new move
        
        # Check for winner (O(1)!)
        winner = self._board.check_winner_at(row, col)
        
        if winner:
            self._state = GameState.X_WINS if winner == Player.X else GameState.O_WINS
        elif self._board.is_full():
            self._state = GameState.DRAW
        else:
            self._switch_player()
        
        return True
    
    def _switch_player(self) -> None:
        """Switch to the other player."""
        self._current_player = self._current_player.opponent()
    
    def undo(self) -> bool:
        """
        Undo the last move.
        
        Returns: True if undo successful
        """
        if not self._move_history:
            return False
        
        last_move = self._move_history.pop()
        self._board.remove(last_move.row, last_move.col)
        self._redo_stack.append(last_move)
        
        # Restore game state
        self._state = GameState.IN_PROGRESS
        self._current_player = last_move.player
        
        return True
    
    def redo(self) -> bool:
        """
        Redo an undone move.
        
        Returns: True if redo successful
        """
        if not self._redo_stack:
            return False
        
        move = self._redo_stack.pop()
        self._board.place(move.row, move.col, move.player)
        self._move_history.append(move)
        
        # Check game state after redo
        winner = self._board.check_winner_at(move.row, move.col)
        if winner:
            self._state = GameState.X_WINS if winner == Player.X else GameState.O_WINS
        elif self._board.is_full():
            self._state = GameState.DRAW
        else:
            self._switch_player()
        
        return True
    
    def reset(self) -> None:
        """Reset game to initial state."""
        self._board.reset()
        self._current_player = Player.X
        self._state = GameState.IN_PROGRESS
        self._move_history.clear()
        self._redo_stack.clear()
    
    def display(self) -> None:
        """Display current game state."""
        print(self._board)
        print(f"\nCurrent Player: {self._current_player}")
        print(f"Game State: {self._state.value}")


# ============ AI Player Interface ============

class AIPlayer(ABC):
    """Abstract base for AI players."""
    
    @abstractmethod
    def get_move(self, board: Board, player: Player) -> Tuple[int, int]:
        """Get AI's next move."""
        pass


class RandomAI(AIPlayer):
    """AI that plays randomly."""
    
    def get_move(self, board: Board, player: Player) -> Tuple[int, int]:
        import random
        empty_cells = board.get_empty_cells()
        return random.choice(empty_cells) if empty_cells else (-1, -1)


class MinimaxAI(AIPlayer):
    """
    AI using Minimax algorithm (optimal play).
    
    For 3×3: Always draws against perfect opponent
    Time: O(b^d) where b=branching, d=depth
    """
    
    def get_move(self, board: Board, player: Player) -> Tuple[int, int]:
        best_score = float('-inf')
        best_move = (-1, -1)
        
        for row, col in board.get_empty_cells():
            board.place(row, col, player)
            score = self._minimax(board, 0, False, player)
            board.remove(row, col)
            
            if score > best_score:
                best_score = score
                best_move = (row, col)
        
        return best_move
    
    def _minimax(self, board: Board, depth: int, is_maximizing: bool, 
                 ai_player: Player) -> int:
        winner = board.check_winner()
        
        if winner == ai_player:
            return 10 - depth  # Prefer faster wins
        elif winner == ai_player.opponent():
            return depth - 10  # Prefer slower losses
        elif board.is_full():
            return 0  # Draw
        
        if is_maximizing:
            best_score = float('-inf')
            for row, col in board.get_empty_cells():
                board.place(row, col, ai_player)
                score = self._minimax(board, depth + 1, False, ai_player)
                board.remove(row, col)
                best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            opponent = ai_player.opponent()
            for row, col in board.get_empty_cells():
                board.place(row, col, opponent)
                score = self._minimax(board, depth + 1, True, ai_player)
                board.remove(row, col)
                best_score = min(best_score, score)
            return best_score


# ============ Demo ============
def main():
    """Demonstrate Tic Tac Toe functionality."""
    print("=" * 50)
    print("TIC TAC TOE DEMO")
    print("=" * 50)
    
    game = TicTacToeGame(board_size=3)
    
    # Play some moves
    print("\n--- Playing a Game ---")
    moves = [(0, 0), (1, 1), (0, 1), (0, 2), (2, 2), (1, 0), (2, 0)]
    
    for row, col in moves:
        print(f"\n{game.current_player} plays ({row}, {col})")
        game.make_move(row, col)
        game.display()
        
        if game.state != GameState.IN_PROGRESS:
            break
    
    print(f"\n🏆 Final Result: {game.state.value}")
    
    # Demo undo
    print("\n" + "=" * 50)
    print("UNDO DEMO")
    print("=" * 50)
    
    game.undo()
    print("After undo:")
    game.display()
    
    # Demo AI
    print("\n" + "=" * 50)
    print("AI DEMO (Minimax)")
    print("=" * 50)
    
    game.reset()
    ai = MinimaxAI()
    
    # Human plays first
    game.make_move(0, 0)
    print("Human plays (0, 0):")
    game.display()
    
    # AI responds
    ai_move = ai.get_move(game.board, game.current_player)
    game.make_move(*ai_move)
    print(f"\nAI plays {ai_move}:")
    game.display()


if __name__ == "__main__":
    main()
```

---

### **PHASE 7: Walk Through Edge Cases (3-4 minutes)**

**SAY THIS:**
> "Let me discuss the edge cases I've handled."

| Edge Case | How Handled | Code Location |
|-----------|-------------|---------------|
| **Already occupied cell** | Return False | `place()` check |
| **Out of bounds move** | Return False | `_is_valid_position()` |
| **Move after game over** | Return False | `make_move()` state check |
| **Undo with no history** | Return False | `undo()` empty check |
| **Board too small** | Raise ValueError | `__init__` validation |
| **Draw detection** | Check `is_full()` | After win check |

**O(1) Win Detection Proof:**
> "Why does the counter approach work?
> - Each cell is either X (+1), O (-1), or empty (0)
> - A row with all X has sum = N
> - A row with all O has sum = -N
> - Any mix has sum between -N and N (exclusive)
> - So |sum| = N means someone won!"

---

### **PHASE 8: Testing Strategy (2-3 minutes)**

```python
import pytest

class TestTicTacToe:
    
    def test_basic_win_row(self):
        """X wins with row."""
        game = TicTacToeGame(3)
        game.make_move(0, 0)  # X
        game.make_move(1, 0)  # O
        game.make_move(0, 1)  # X
        game.make_move(1, 1)  # O
        game.make_move(0, 2)  # X wins!
        
        assert game.state == GameState.X_WINS
    
    def test_basic_win_column(self):
        """O wins with column."""
        game = TicTacToeGame(3)
        game.make_move(0, 0)  # X
        game.make_move(0, 1)  # O
        game.make_move(1, 0)  # X
        game.make_move(1, 1)  # O
        game.make_move(2, 2)  # X
        game.make_move(2, 1)  # O wins!
        
        assert game.state == GameState.O_WINS
    
    def test_basic_win_diagonal(self):
        """X wins with diagonal."""
        game = TicTacToeGame(3)
        game.make_move(0, 0)  # X
        game.make_move(0, 1)  # O
        game.make_move(1, 1)  # X
        game.make_move(0, 2)  # O
        game.make_move(2, 2)  # X wins!
        
        assert game.state == GameState.X_WINS
    
    def test_draw(self):
        """Game ends in draw."""
        game = TicTacToeGame(3)
        # X O X
        # X O O
        # O X X
        moves = [(0,0), (0,1), (0,2), (1,1), (1,0), (1,2), (2,1), (2,0), (2,2)]
        for r, c in moves:
            game.make_move(r, c)
        
        assert game.state == GameState.DRAW
    
    def test_cannot_overwrite(self):
        """Cannot place on occupied cell."""
        game = TicTacToeGame(3)
        game.make_move(0, 0)  # X
        result = game.make_move(0, 0)  # Try same cell
        
        assert result == False
        assert game.board.get(0, 0) == Player.X  # Unchanged
    
    def test_undo_redo(self):
        """Undo and redo work correctly."""
        game = TicTacToeGame(3)
        game.make_move(0, 0)  # X
        game.make_move(1, 1)  # O
        
        assert game.current_player == Player.X
        
        game.undo()
        assert game.board.get(1, 1) == Player.EMPTY
        assert game.current_player == Player.O
        
        game.redo()
        assert game.board.get(1, 1) == Player.O
        assert game.current_player == Player.X
    
    def test_o1_win_detection(self):
        """Win detection is O(1)."""
        board = Board(3)
        
        # Fill a row with X
        board.place(0, 0, Player.X)
        board.place(0, 1, Player.X)
        board.place(0, 2, Player.X)
        
        # check_winner_at should detect win
        winner = board.check_winner_at(0, 2)
        assert winner == Player.X
    
    def test_larger_board(self):
        """Works with larger boards."""
        game = TicTacToeGame(board_size=5)
        
        # X wins with 5 in a row
        for i in range(5):
            game.make_move(0, i)  # X in row 0
            if i < 4:
                game.make_move(1, i)  # O in row 1
        
        assert game.state == GameState.X_WINS
```

---

### **PHASE 9: Complexity Analysis (1 minute)**

| Operation | Naive | Optimized |
|-----------|-------|-----------|
| `make_move` | O(N) | **O(1)** |
| `check_winner_at` | O(N) | **O(1)** |
| `undo` | O(1) | O(1) |
| `is_full` | O(1) | O(1) |

**Space:** O(N²) for grid + O(N) for counters = O(N²)

**Why O(1)?**
> "After a move at (r, c):
> - Check row_counts[r]: O(1)
> - Check col_counts[c]: O(1)
> - Check diag_count (if on diagonal): O(1)
> - Check anti_diag_count (if on anti-diagonal): O(1)
> Total: 4 comparisons = O(1)"

---

### **PHASE 10: Extensions & Follow-ups (5+ minutes)**

#### **Q1: "How would you extend to Connect Four?"**

```python
class ConnectFourBoard(Board):
    """4-in-a-row, gravity-based placement."""
    
    def __init__(self, rows: int = 6, cols: int = 7):
        # Different dimensions, win requires 4
        self.rows = rows
        self.cols = cols
        self.win_length = 4
        # ... different counter structure
    
    def drop(self, col: int, player: Player) -> int:
        """Drop piece in column (gravity). Returns row landed."""
        for row in range(self.rows - 1, -1, -1):
            if self.get(row, col) == Player.EMPTY:
                self.place(row, col, player)
                return row
        return -1  # Column full
```

---

#### **Q2: "How would you add Alpha-Beta pruning?"**

```python
def _minimax_ab(self, board: Board, depth: int, alpha: float, 
                beta: float, is_maximizing: bool, player: Player) -> int:
    """Minimax with Alpha-Beta pruning (much faster!)."""
    
    # Base cases (same as before)
    winner = board.check_winner()
    if winner:
        return (10 - depth) if winner == player else (depth - 10)
    if board.is_full():
        return 0
    
    if is_maximizing:
        max_eval = float('-inf')
        for r, c in board.get_empty_cells():
            board.place(r, c, player)
            eval = self._minimax_ab(board, depth+1, alpha, beta, False, player)
            board.remove(r, c)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Prune!
        return max_eval
    else:
        # Similar for minimizing...
```

---

#### **Q3: "How would you make it networked multiplayer?"**

```python
class NetworkGame:
    """Networked Tic Tac Toe."""
    
    def __init__(self, game: TicTacToeGame):
        self.game = game
        self.observers: List[Callable] = []  # For remote clients
    
    def make_move(self, row: int, col: int, player_id: str) -> bool:
        """Make move and notify all observers."""
        if not self._is_player_turn(player_id):
            return False
        
        result = self.game.make_move(row, col)
        if result:
            self._notify_all(Move(row, col, self.game.current_player))
        return result
    
    def _notify_all(self, move: Move):
        for observer in self.observers:
            observer(move)  # Send to remote clients
```

---

## ❌ Common Mistakes (What NOT to Do)

### **MISTAKE 1: O(N²) Win Check Every Move** ❌

```python
# WRONG - Scans entire board!
def check_winner(self):
    for row in range(self.size):
        for col in range(self.size):
            # Check if starting point of winning line
            ...

# CORRECT - O(1) with counters
def check_winner_at(self, row, col):
    if abs(self.row_counts[row]) == self.size:
        return Player.X if self.row_counts[row] > 0 else Player.O
```

---

### **MISTAKE 2: Not Validating Board State** ❌

```python
# WRONG - Allows invalid moves
def make_move(self, row, col):
    self.board[row][col] = self.current_player  # What if occupied?

# CORRECT - Validate first
def make_move(self, row, col):
    if self.board[row][col] != Player.EMPTY:
        return False  # Already occupied
```

---

### **MISTAKE 3: Forgetting Draw Check** ❌

```python
# WRONG - Only checks winner
def make_move(self, row, col):
    winner = self.check_winner()
    if winner:
        self.state = GameState.X_WINS
    # What if board is full with no winner?

# CORRECT - Check draw too
if winner:
    self.state = GameState.X_WINS if winner == Player.X else GameState.O_WINS
elif self.board.is_full():
    self.state = GameState.DRAW
```

---

## 💯 Interview Checklist

- [ ] ✅ **Clarified requirements** (board size, AI, undo)
- [ ] ✅ **Explained O(1) optimization** (row/col/diagonal counters)
- [ ] ✅ **Drew class diagram** (Board, Game, Player)
- [ ] ✅ **Used Enum** for Player and GameState
- [ ] ✅ **Implemented undo/redo** with move history
- [ ] ✅ **Separated Board from Game** (SRP)
- [ ] ✅ **Created AI interface** (OCP - extensible)
- [ ] ✅ **Handled edge cases** (occupied, out of bounds, game over)
- [ ] ✅ **Discussed extensions** (Connect Four, networking)

---

## 📚 Quick Reference Card

```
┌────────────────────────────────────────────────────────────┐
│                  TIC TAC TOE CHEAT SHEET                   │
├────────────────────────────────────────────────────────────┤
│ O(1) WIN DETECTION:                                       │
│   - row_counts[N]: sum of row                            │
│   - col_counts[N]: sum of column                         │
│   - diag_count: main diagonal sum                         │
│   - anti_diag_count: anti-diagonal sum                    │
│   - X = +1, O = -1                                        │
│   - Win when |sum| == N                                   │
│                                                            │
│ GAME STATES:                                              │
│   IN_PROGRESS → X_WINS / O_WINS / DRAW                   │
│                                                            │
│ UNDO/REDO:                                                │
│   - move_history: List[Move] for undo                    │
│   - redo_stack: List[Move] for redo                      │
│   - Clear redo stack on new move                         │
│                                                            │
│ AI:                                                       │
│   - Minimax: Optimal play                                │
│   - Alpha-Beta: Faster pruning                           │
│   - Score: +10 for win, -10 for loss, 0 for draw        │
│                                                            │
│ COMPLEXITY:                                               │
│   - make_move: O(1)                                      │
│   - check_winner_at: O(1)                                │
│   - Space: O(N²)                                         │
└────────────────────────────────────────────────────────────┘
```

---

**Related Problems:**
- LeetCode 348: Design Tic-Tac-Toe
- Connect Four (gravity + 4-in-a-row)
- Gomoku (5-in-a-row on large board)

