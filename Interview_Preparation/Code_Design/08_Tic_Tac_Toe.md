# ⭕❌ PROBLEM 8: TIC TAC TOE GAME

### ⭐⭐⭐ **Design Tic Tac Toe with Clean OOP**

**Frequency:** MEDIUM at Atlassian
**Difficulty:** Easy-Medium
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

---

## 🎯 Interview Approach

### Step 1: Clarify Requirements (1 min)
```
"Let me clarify:
1. Board size - fixed 3x3 or configurable NxN?
2. Players - always 2? Human vs Human or AI?
3. Win condition - same as standard (row/col/diagonal)?
4. Should we support undo/redo?"
```

### Step 2: Design Overview (1 min)
```
"I'll design with:
- Board class: Grid state and win detection
- Player enum: X and O
- Game class: Game state machine, turn management
- O(1) win checking optimization (optional)"
```

---

## 🎨 Visual Example

```text
Game Flow:
┌───┬───┬───┐     ┌───┬───┬───┐     ┌───┬───┬───┐
│   │   │   │     │ X │   │   │     │ X │ O │   │
├───┼───┼───┤ --> ├───┼───┼───┤ --> ├───┼───┼───┤
│   │   │   │     │   │   │   │     │   │   │   │
├───┼───┼───┤     ├───┼───┼───┤     ├───┼───┼───┤
│   │   │   │     │   │   │   │     │   │   │   │
└───┴───┴───┘     └───┴───┴───┘     └───┴───┴───┘
   Initial        X plays (0,0)      O plays (0,1)

Win Detection:
┌───┬───┬───┐
│ X │ O │ O │  Check Row 2: X X X → X WINS!
├───┼───┼───┤
│ O │ X │   │
├───┼───┼───┤
│ X │ X │ X │  ← Winning row
└───┴───┴───┘
```

---

## 💻 Python Implementation

```python
from enum import Enum
from typing import Optional, List, Tuple
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

# ============ Enums ============

class Player(Enum):
    """Player markers"""
    X = "X"
    O = "O"
    EMPTY = " "
    
    def __str__(self):
        return self.value
    
    def opponent(self) -> 'Player':
        """Get the opponent player"""
        if self == Player.X:
            return Player.O
        elif self == Player.O:
            return Player.X
        return Player.EMPTY

class GameState(Enum):
    """Game states"""
    IN_PROGRESS = "in_progress"
    X_WINS = "x_wins"
    O_WINS = "o_wins"
    DRAW = "draw"

# ============ Move Record (for undo) ============

@dataclass
class Move:
    """Represents a single move"""
    row: int
    col: int
    player: Player

# ============ Board Class ============

class Board:
    """
    Represents the game board.
    
    Design Decisions:
    - Uses 2D list for simplicity
    - O(N) win checking (can optimize to O(1) with counters)
    - Immutable size after creation
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
    
    def place(self, row: int, col: int, player: Player) -> bool:
        """
        Place a player's mark on the board.
        
        Returns: True if placement successful, False otherwise
        Time: O(1)
        """
        if not self._is_valid_position(row, col):
            return False
        
        if self._grid[row][col] != Player.EMPTY:
            return False
        
        self._grid[row][col] = player
        self._move_count += 1
        return True
    
    def remove(self, row: int, col: int) -> bool:
        """Remove a mark (for undo)"""
        if not self._is_valid_position(row, col):
            return False
        
        if self._grid[row][col] == Player.EMPTY:
            return False
        
        self._grid[row][col] = Player.EMPTY
        self._move_count -= 1
        return True
    
    def get(self, row: int, col: int) -> Player:
        """Get the player at a position"""
        if not self._is_valid_position(row, col):
            return Player.EMPTY
        return self._grid[row][col]
    
    def _is_valid_position(self, row: int, col: int) -> bool:
        """Check if position is within bounds"""
        return 0 <= row < self.size and 0 <= col < self.size
    
    def is_full(self) -> bool:
        """Check if board is completely filled"""
        return self._move_count == self.size * self.size
    
    def check_winner(self) -> Optional[Player]:
        """
        Check if there's a winner.
        
        Time: O(N) where N = board size
        Space: O(1)
        """
        # Check rows
        for row in range(self.size):
            if self._check_line([(row, col) for col in range(self.size)]):
                return self._grid[row][0]
        
        # Check columns
        for col in range(self.size):
            if self._check_line([(row, col) for row in range(self.size)]):
                return self._grid[0][col]
        
        # Check main diagonal
        if self._check_line([(i, i) for i in range(self.size)]):
            return self._grid[0][0]
        
        # Check anti-diagonal
        if self._check_line([(i, self.size - 1 - i) for i in range(self.size)]):
            return self._grid[0][self.size - 1]
        
        return None
    
    def _check_line(self, positions: List[Tuple[int, int]]) -> bool:
        """Check if all positions in a line have the same non-empty player"""
        first = self._grid[positions[0][0]][positions[0][1]]
        
        if first == Player.EMPTY:
            return False
        
        return all(
            self._grid[row][col] == first 
            for row, col in positions
        )
    
    def get_empty_cells(self) -> List[Tuple[int, int]]:
        """Get all empty cell positions"""
        return [
            (row, col)
            for row in range(self.size)
            for col in range(self.size)
            if self._grid[row][col] == Player.EMPTY
        ]
    
    def reset(self) -> None:
        """Reset the board"""
        for row in range(self.size):
            for col in range(self.size):
                self._grid[row][col] = Player.EMPTY
        self._move_count = 0
    
    def display(self) -> str:
        """Get string representation of board"""
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

# ============ Optimized Board with O(1) Win Check ============

class OptimizedBoard(Board):
    """
    Board with O(1) win checking using counters.
    
    Optimization: Track count of each player's marks in:
    - Each row
    - Each column
    - Main diagonal
    - Anti-diagonal
    
    Win when any counter reaches board size.
    """
    
    def __init__(self, size: int = 3):
        super().__init__(size)
        
        # Counters: positive = X count, negative = O count
        self._row_counts = [0] * size
        self._col_counts = [0] * size
        self._diag_count = 0
        self._anti_diag_count = 0
    
    def place(self, row: int, col: int, player: Player) -> bool:
        if not super().place(row, col, player):
            return False
        
        # Update counters
        delta = 1 if player == Player.X else -1
        self._row_counts[row] += delta
        self._col_counts[col] += delta
        
        if row == col:
            self._diag_count += delta
        if row + col == self.size - 1:
            self._anti_diag_count += delta
        
        return True
    
    def remove(self, row: int, col: int) -> bool:
        player = self.get(row, col)
        if not super().remove(row, col):
            return False
        
        # Update counters
        delta = -1 if player == Player.X else 1
        self._row_counts[row] += delta
        self._col_counts[col] += delta
        
        if row == col:
            self._diag_count += delta
        if row + col == self.size - 1:
            self._anti_diag_count += delta
        
        return True
    
    def check_winner_at(self, row: int, col: int) -> Optional[Player]:
        """
        O(1) win check after a move at (row, col).
        Only checks lines affected by this position.
        """
        target = self.size  # X needs +size, O needs -size
        
        if abs(self._row_counts[row]) == target:
            return Player.X if self._row_counts[row] > 0 else Player.O
        
        if abs(self._col_counts[col]) == target:
            return Player.X if self._col_counts[col] > 0 else Player.O
        
        if row == col and abs(self._diag_count) == target:
            return Player.X if self._diag_count > 0 else Player.O
        
        if row + col == self.size - 1 and abs(self._anti_diag_count) == target:
            return Player.X if self._anti_diag_count > 0 else Player.O
        
        return None
    
    def reset(self) -> None:
        super().reset()
        self._row_counts = [0] * self.size
        self._col_counts = [0] * self.size
        self._diag_count = 0
        self._anti_diag_count = 0

# ============ Game Class ============

class TicTacToeGame:
    """
    Main game controller.
    
    Responsibilities:
    - Manage game state
    - Handle turns
    - Validate moves
    - Support undo/redo
    """
    
    def __init__(self, board_size: int = 3, use_optimized: bool = True):
        if use_optimized:
            self._board = OptimizedBoard(board_size)
        else:
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
        Time: O(1) with optimized board, O(N) otherwise
        """
        if self._state != GameState.IN_PROGRESS:
            return False
        
        if not self._board.place(row, col, self._current_player):
            return False
        
        # Record move for undo
        move = Move(row, col, self._current_player)
        self._move_history.append(move)
        self._redo_stack.clear()  # Clear redo on new move
        
        # Check for winner
        if isinstance(self._board, OptimizedBoard):
            winner = self._board.check_winner_at(row, col)
        else:
            winner = self._board.check_winner()
        
        if winner:
            self._state = GameState.X_WINS if winner == Player.X else GameState.O_WINS
        elif self._board.is_full():
            self._state = GameState.DRAW
        else:
            self._switch_player()
        
        return True
    
    def _switch_player(self) -> None:
        """Switch to the other player"""
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
        winner = self._board.check_winner()
        if winner:
            self._state = GameState.X_WINS if winner == Player.X else GameState.O_WINS
        elif self._board.is_full():
            self._state = GameState.DRAW
        else:
            self._switch_player()
        
        return True
    
    def reset(self) -> None:
        """Reset game to initial state"""
        self._board.reset()
        self._current_player = Player.X
        self._state = GameState.IN_PROGRESS
        self._move_history.clear()
        self._redo_stack.clear()
    
    def display(self) -> None:
        """Display current game state"""
        print(self._board)
        print(f"\nCurrent Player: {self._current_player}")
        print(f"Game State: {self._state.value}")

# ============ AI Player (Extension) ============

class AIPlayer(ABC):
    """Abstract base for AI players"""
    
    @abstractmethod
    def get_move(self, board: Board, player: Player) -> Tuple[int, int]:
        pass

class RandomAI(AIPlayer):
    """AI that plays randomly"""
    
    def get_move(self, board: Board, player: Player) -> Tuple[int, int]:
        import random
        empty_cells = board.get_empty_cells()
        return random.choice(empty_cells) if empty_cells else (-1, -1)

class MinimaxAI(AIPlayer):
    """
    AI using Minimax algorithm.
    
    For 3x3 board: O(9!) worst case, but with pruning much faster
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
            return 10 - depth
        elif winner == ai_player.opponent():
            return depth - 10
        elif board.is_full():
            return 0
        
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
    print("=== Tic Tac Toe Demo ===\n")
    
    game = TicTacToeGame(board_size=3)
    
    # Play some moves
    moves = [(0, 0), (1, 1), (0, 1), (0, 2), (2, 2), (1, 0), (2, 0)]
    
    for i, (row, col) in enumerate(moves):
        print(f"Move {i+1}: {game.current_player} at ({row}, {col})")
        game.make_move(row, col)
        game.display()
        print()
        
        if game.state != GameState.IN_PROGRESS:
            break
    
    print(f"Final State: {game.state.value}")
    
    # Demo undo
    print("\n=== Undo Demo ===")
    game.undo()
    print("After undo:")
    game.display()
    
    # Demo AI
    print("\n=== AI Demo ===")
    game.reset()
    ai = MinimaxAI()
    
    # Human vs AI
    game.make_move(0, 0)  # Human plays corner
    print("Human plays (0,0):")
    game.display()
    
    # AI's turn
    ai_move = ai.get_move(game.board, game.current_player)
    game.make_move(*ai_move)
    print(f"\nAI plays {ai_move}:")
    game.display()

if __name__ == "__main__":
    main()
```

---

## 🎯 Interview Explanation Flow

### 1. Start Simple (30 sec)
```
"I'll start with a clean 3x3 implementation:
- Board class handles grid state
- Game class manages turns and rules
- Simple O(N) win checking first"
```

### 2. Explain O(1) Optimization (1 min)
```
"For O(1) win detection after each move:
- Track row/column/diagonal sums
- Use +1 for X, -1 for O
- Win when any sum equals ±N
- Only check lines affected by the move"
```

### 3. Discuss Extensions (1 min)
```
"I've designed for extensibility:
- Board is separate from Game (SRP)
- Move history enables undo/redo
- AIPlayer interface for different AI strategies
- Works for NxN boards"
```

---

## 📊 Complexity Analysis

| Operation | Basic Board | Optimized Board |
|-----------|-------------|-----------------|
| make_move | O(1) | O(1) |
| check_winner | O(N) | O(1) |
| undo | O(1) | O(1) |
| is_full | O(1) | O(1) |

**Space:** O(N²) for the board

---

## 🚀 Extensions

### 1. Connect Four (Different Win Condition)
```python
class ConnectFourBoard(Board):
    """4 in a row to win, gravity-based placement"""
    
    def __init__(self, rows: int = 6, cols: int = 7):
        super().__init__(max(rows, cols))
        self.win_length = 4
    
    def drop(self, col: int, player: Player) -> int:
        """Drop piece in column, returns row where it landed"""
        for row in range(self.size - 1, -1, -1):
            if self.get(row, col) == Player.EMPTY:
                self.place(row, col, player)
                return row
        return -1
```

### 2. Multiplayer (More than 2 players)
```python
class MultiplayerGame:
    def __init__(self, num_players: int):
        self.players = [Player(str(i)) for i in range(num_players)]
        self.current_idx = 0
    
    def next_player(self):
        self.current_idx = (self.current_idx + 1) % len(self.players)
```

### 3. Network Multiplayer
```python
class NetworkGame:
    def __init__(self, game: TicTacToeGame):
        self.game = game
        self.observers: List[Callable] = []
    
    def notify_move(self, move: Move):
        for observer in self.observers:
            observer(move)
```

---

## 💡 Interview Tips

### What Interviewers Look For:
✅ **Clean OOP design** (separation of concerns)
✅ **O(1) win checking** optimization
✅ **Undo/Redo** support
✅ **Extensibility** (NxN, AI players)
✅ **Edge case handling**

### Common Mistakes:
❌ Not handling already-occupied cells
❌ O(N²) win checking when O(1) is possible
❌ Forgetting to check draw condition
❌ Not validating board size
❌ Tight coupling between Board and Game

### Questions to Ask:
- "Should the board size be configurable?"
- "Do we need undo/redo functionality?"
- "Should we support AI players?"
- "Network multiplayer needed?"

---

## 🔗 Related Problems

- **Connect Four**: Different win length, gravity
- **Gomoku**: 5 in a row on larger board
- **Ultimate Tic Tac Toe**: Nested boards
- **Checkers/Chess**: More complex game logic

