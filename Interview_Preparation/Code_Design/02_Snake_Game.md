# 🐍 PROBLEM 2: SNAKE GAME (LOW-LEVEL DESIGN)

### ⭐⭐⭐⭐⭐ **Design and Implement Snake Game**

**Frequency:** Appears in **50%** of Atlassian Code Design rounds!
**Difficulty:** Medium
**Focus:** Object-Oriented Design, Game Loop, Data Structures

---

## 📋 Problem Statement

Design and implement the classic Snake Game with clean, modular, and extensible code.

**Core Requirements:**
- Snake moves on a grid (N × M board)
- Snake grows when eating food
- Game over when snake hits wall or itself
- Support multiple directions (UP, DOWN, LEFT, RIGHT)
- Track game state (score, game over)

**Input:** Board size, initial snake position, food positions
**Output:** Working game with `move()`, `place_food()`, `is_game_over()` methods

**Constraints:**
- 5 ≤ Board size ≤ 100
- Snake initial length ≥ 1
- Food appears randomly
- Snake cannot reverse direction instantly (UP → DOWN not allowed)

---

## 🎤 How to Explain in Interview

### **Opening Statement (30 seconds)**
> "I'll design the Snake Game using clean OOP principles with Python's `dataclasses` for cleaner code. I'll use a `deque` for O(1) snake operations and a `set` for O(1) collision detection."

### **Key Points to Mention:**
1. "Using `deque` for O(1) head/tail operations instead of list"
2. "Using `set` for O(1) collision detection instead of O(n) list search"
3. "Using `Enum` for directions with built-in opposite checking"
4. "Following **Single Responsibility Principle** - separate Snake, Board, Game classes"

---

## 🎨 Visual Example

```text
Initial State (10×10 board):
. . . . . . . . . .
. . . F . . . . . .  F = Food
. . . . . . . . . .  H = Head
. . H B B . . . . .  B = Body
. . . . . . . . . .
. . . . . . . . . .

After move(UP):
. . . . . . . . . .
. . . F . . . . . .
. . H . . . . . . .  Snake moved up
. . B B . . . . . .  Tail removed
. . . . . . . . . .

After eating food and moving:
. . . . . . . . . .
. . . . H . . . . .  Snake grew (no tail removal)
. . . B B . . . . .
. . . B . . . . . .
. . . . . . . . . .
```

---

## 🎯 Design Patterns Used

### **1. Single Responsibility Principle (SRP)** ⭐
Each class has ONE clear responsibility:
- `Snake`: Manage body positions and movement
- `Board`: Manage grid boundaries
- `SnakeGame`: Orchestrate game logic

### **2. Open/Closed Principle (OCP)** ⭐
Easy to extend without modifying existing code:
```python
# Add obstacles without changing Snake/Board
class SnakeGameWithObstacles(SnakeGame):
    def __init__(self, ...):
        super().__init__(...)
        self.obstacles: Set[Position] = set()
```

### **3. Encapsulation** ⭐
- Private state (body positions) not directly accessible
- Public methods provide controlled access

---

## 🏗️ Class Design

```text
┌─────────────────┐
│   SnakeGame     │  ← Main controller (orchestrates)
├─────────────────┤
│ - snake: Snake  │
│ - board: Board  │
│ - food: Position│
│ - score: int    │
│ - game_over: bool
└─────────────────┘
        │
        ├──────────────┬──────────────┐
        │              │              │
   ┌─────────┐   ┌─────────┐   ┌───────────┐
   │  Snake  │   │  Board  │   │ Direction │
   ├─────────┤   ├─────────┤   ├───────────┤
   │- body   │   │- rows   │   │ UP        │
   │- occupied│  │- cols   │   │ DOWN      │
   │- direction  └─────────┘   │ LEFT      │
   └─────────┘                 │ RIGHT     │
                               └───────────┘
```

---

## 💻 Python Implementation (Production-Ready)

```python
"""
Snake Game - Low-Level Design Implementation
============================================
Clean OOP implementation using Python's modern features.

Design Patterns:
- Single Responsibility Principle (SRP)
- Open/Closed Principle (OCP) - easy to extend
- Encapsulation - controlled state access

Data Structures:
- deque: O(1) for head/tail operations
- set: O(1) for collision detection

Time Complexity: O(1) per move
Space Complexity: O(snake_length + board_size)
"""

from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Set, Tuple, Optional
import random


# Type alias for position (row, col)
Position = Tuple[int, int]


class Direction(Enum):
    """
    Movement directions with delta values.
    
    Using Enum prevents magic strings and provides type safety.
    """
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)
    
    def is_opposite(self, other: 'Direction') -> bool:
        """Check if two directions are opposite (invalid move)."""
        opposites = {
            (Direction.UP, Direction.DOWN),
            (Direction.DOWN, Direction.UP),
            (Direction.LEFT, Direction.RIGHT),
            (Direction.RIGHT, Direction.LEFT),
        }
        return (self, other) in opposites
    
    @property
    def delta(self) -> Position:
        """Get (row_delta, col_delta) for this direction."""
        return self.value


@dataclass
class Snake:
    """
    Snake entity managing body positions and movement.
    
    Key Design Decisions:
    - Uses deque for O(1) head/tail operations
    - Uses set for O(1) collision detection
    - Prevents instant direction reversal
    
    Attributes:
        body: Deque of positions (head at index 0)
        occupied: Set of all body positions (for O(1) collision check)
        direction: Current movement direction
    """
    initial_position: Position
    body: deque = field(init=False)
    occupied: Set[Position] = field(init=False)
    direction: Direction = field(default=Direction.RIGHT)
    
    def __post_init__(self):
        """Initialize body and occupied set."""
        self.body = deque([self.initial_position])
        self.occupied = {self.initial_position}
    
    @property
    def head(self) -> Position:
        """Get current head position."""
        return self.body[0]
    
    @property
    def tail(self) -> Position:
        """Get current tail position."""
        return self.body[-1]
    
    @property
    def length(self) -> int:
        """Get current snake length."""
        return len(self.body)
    
    def change_direction(self, new_direction: Direction) -> bool:
        """
        Change snake direction (validates not opposite).
        
        Args:
            new_direction: Desired new direction
            
        Returns:
            True if direction changed, False if invalid (opposite)
        """
        if self.direction.is_opposite(new_direction):
            return False
        self.direction = new_direction
        return True
    
    def get_next_head_position(self) -> Position:
        """Calculate where head will be after moving."""
        row, col = self.head
        d_row, d_col = self.direction.delta
        return (row + d_row, col + d_col)
    
    def move(self, new_head: Position) -> None:
        """
        Move snake to new position (normal move, no growth).
        
        Args:
            new_head: New head position
        """
        # Add new head
        self.body.appendleft(new_head)
        self.occupied.add(new_head)
        
        # Remove tail
        tail = self.body.pop()
        self.occupied.remove(tail)
    
    def grow(self, new_head: Position) -> None:
        """
        Grow snake by adding head without removing tail.
        
        Args:
            new_head: New head position after eating food
        """
        self.body.appendleft(new_head)
        self.occupied.add(new_head)
    
    def is_collision(self, position: Position) -> bool:
        """
        Check if position collides with snake body.
        O(1) lookup using set.
        
        Args:
            position: Position to check
            
        Returns:
            True if position is occupied by snake
        """
        return position in self.occupied
    
    def get_body_positions(self) -> List[Position]:
        """Get list of all body positions (for rendering)."""
        return list(self.body)


@dataclass
class Board:
    """
    Game board managing grid boundaries.
    
    Attributes:
        rows: Number of rows
        cols: Number of columns
    """
    rows: int
    cols: int
    
    def __post_init__(self):
        """Validate board dimensions."""
        if self.rows <= 0 or self.cols <= 0:
            raise ValueError("Board dimensions must be positive")
    
    def is_within_bounds(self, position: Position) -> bool:
        """
        Check if position is within board boundaries.
        
        Args:
            position: (row, col) tuple
            
        Returns:
            True if position is valid
        """
        row, col = position
        return 0 <= row < self.rows and 0 <= col < self.cols
    
    def get_random_position(self) -> Position:
        """Get random position on the board."""
        return (
            random.randint(0, self.rows - 1),
            random.randint(0, self.cols - 1)
        )


class SnakeGame:
    """
    Main game controller orchestrating Snake, Board, and Food.
    
    Example:
        >>> game = SnakeGame(rows=10, cols=10, initial_pos=(5, 5))
        >>> game.move(Direction.UP)    # True - moved successfully
        >>> game.move(Direction.RIGHT) # True - moved successfully
        >>> game.is_game_over          # False
        >>> game.score                 # 0 (or 10 if food eaten)
    """
    
    def __init__(self, rows: int, cols: int, initial_pos: Position):
        """
        Initialize game.
        
        Args:
            rows: Board height
            cols: Board width
            initial_pos: Starting position for snake (row, col)
            
        Raises:
            ValueError: If initial position is out of bounds
        """
        self.board = Board(rows, cols)
        
        if not self.board.is_within_bounds(initial_pos):
            raise ValueError(f"Initial position {initial_pos} is out of bounds")
        
        self.snake = Snake(initial_pos)
        self.food: Position = self._place_food()
        self.score: int = 0
        self.game_over: bool = False
    
    @property
    def is_game_over(self) -> bool:
        """Check if game has ended."""
        return self.game_over
    
    def move(self, direction: Direction) -> bool:
        """
        Execute one game tick with given direction.
        
        Args:
            direction: Direction to move
            
        Returns:
            True if move successful, False if game over
            
        Raises:
            RuntimeError: If called after game is over
        """
        if self.game_over:
            raise RuntimeError("Game is already over!")
        
        # Try to change direction (ignored if opposite)
        self.snake.change_direction(direction)
        
        # Calculate next head position
        next_head = self.snake.get_next_head_position()
        
        # Check wall collision
        if not self.board.is_within_bounds(next_head):
            self.game_over = True
            return False
        
        # Check self collision (but not with current tail position)
        # Note: When moving, tail will vacate before head arrives
        # But if eating food, tail stays - need to check carefully
        if self.snake.is_collision(next_head):
            # Exception: if next_head is current tail AND not eating food,
            # the tail will move away, so no collision
            if next_head != self.snake.tail or next_head == self.food:
                self.game_over = True
                return False
        
        # Check if eating food
        if next_head == self.food:
            self.snake.grow(next_head)
            self.score += 10
            self.food = self._place_food()
        else:
            self.snake.move(next_head)
        
        return True
    
    def _place_food(self) -> Position:
        """Place food at random empty position."""
        while True:
            food_pos = self.board.get_random_position()
            if not self.snake.is_collision(food_pos):
                return food_pos
    
    def get_state(self) -> dict:
        """Get current game state (for rendering/debugging)."""
        return {
            "snake_body": self.snake.get_body_positions(),
            "snake_head": self.snake.head,
            "food": self.food,
            "score": self.score,
            "game_over": self.game_over,
            "direction": self.snake.direction.name,
        }
    
    def print_board(self) -> None:
        """Print visual representation of the game."""
        # Create grid
        grid = [['.' for _ in range(self.board.cols)] 
                for _ in range(self.board.rows)]
        
        # Place snake
        for i, pos in enumerate(self.snake.body):
            row, col = pos
            grid[row][col] = 'H' if i == 0 else 'B'
        
        # Place food
        food_row, food_col = self.food
        if grid[food_row][food_col] == '.':
            grid[food_row][food_col] = 'F'
        
        # Print
        print("+" + "-" * (self.board.cols * 2 - 1) + "+")
        for row in grid:
            print("|" + " ".join(row) + "|")
        print("+" + "-" * (self.board.cols * 2 - 1) + "+")
        print(f"Score: {self.score} | Direction: {self.snake.direction.name}")
        print()


# ============ Demo / Usage ============
if __name__ == "__main__":
    print("=== Snake Game Demo ===\n")
    
    # Create game
    game = SnakeGame(rows=10, cols=10, initial_pos=(5, 5))
    
    print("Initial State:")
    game.print_board()
    
    # Simulate moves
    moves = [Direction.UP, Direction.UP, Direction.RIGHT, 
             Direction.RIGHT, Direction.DOWN]
    
    for move in moves:
        success = game.move(move)
        print(f"After moving {move.name}:")
        game.print_board()
        
        if not success:
            print("Game Over!")
            break
    
    print(f"\nFinal Score: {game.score}")
    print(f"Game Over: {game.is_game_over}")
```

---

## 🚀 Extensions & Follow-ups

### **Extension 1: Add Obstacles**
```python
class SnakeGameWithObstacles(SnakeGame):
    """Snake game with obstacles on the board."""
    
    def __init__(self, rows: int, cols: int, initial_pos: Position, 
                 obstacles: Set[Position] = None):
        self.obstacles = obstacles or set()
        super().__init__(rows, cols, initial_pos)
    
    def move(self, direction: Direction) -> bool:
        next_head = self.snake.get_next_head_position()
        
        # Check obstacle collision
        if next_head in self.obstacles:
            self.game_over = True
            return False
        
        return super().move(direction)
```

### **Extension 2: Multiple Food Types**
```python
from enum import Enum

class FoodType(Enum):
    NORMAL = (10, False)    # (points, speed_boost)
    GOLDEN = (50, False)    # More points
    SPEED = (20, True)      # Speed boost
    
    @property
    def points(self) -> int:
        return self.value[0]

@dataclass
class Food:
    position: Position
    food_type: FoodType = FoodType.NORMAL
```

### **Extension 3: Multiplayer**
```python
class MultiplayerSnakeGame:
    """Two-player snake game."""
    
    def __init__(self, rows: int, cols: int):
        self.board = Board(rows, cols)
        self.snakes = [
            Snake((2, 2)),   # Player 1
            Snake((7, 7)),   # Player 2
        ]
        self.food = self._place_food()
    
    def move(self, player_id: int, direction: Direction) -> bool:
        snake = self.snakes[player_id]
        # Check collision with other snakes too
        for other_snake in self.snakes:
            if other_snake != snake:
                if other_snake.is_collision(next_head):
                    return False
        # ... rest of logic
```

### **Extension 4: Game Save/Load**
```python
import json

class SnakeGame:
    def save(self) -> str:
        """Serialize game state to JSON."""
        return json.dumps({
            "snake_body": list(self.snake.body),
            "direction": self.snake.direction.name,
            "food": self.food,
            "score": self.score,
            "board": (self.board.rows, self.board.cols),
        })
    
    @classmethod
    def load(cls, json_str: str) -> 'SnakeGame':
        """Deserialize game from JSON."""
        data = json.loads(json_str)
        # Reconstruct game state...
```

---

## 🧪 Testing Strategy

```python
import pytest

class TestSnakeGame:
    """Unit tests for Snake Game."""
    
    def test_initial_state(self):
        """Game starts with correct initial state."""
        game = SnakeGame(10, 10, (5, 5))
        
        assert not game.is_game_over
        assert game.score == 0
        assert game.snake.head == (5, 5)
        assert game.snake.length == 1
    
    def test_basic_movement(self):
        """Snake moves correctly."""
        game = SnakeGame(10, 10, (5, 5))
        
        result = game.move(Direction.UP)
        
        assert result == True
        assert game.snake.head == (4, 5)
        assert not game.is_game_over
    
    def test_wall_collision(self):
        """Game ends when snake hits wall."""
        game = SnakeGame(10, 10, (0, 5))  # At top edge
        
        result = game.move(Direction.UP)  # Hit top wall
        
        assert result == False
        assert game.is_game_over
    
    def test_self_collision(self):
        """Game ends when snake hits itself."""
        game = SnakeGame(10, 10, (5, 5))
        # Manually grow snake to create collision scenario
        game.snake.body = deque([(5, 5), (5, 6), (5, 7), (4, 7), (4, 6)])
        game.snake.occupied = set(game.snake.body)
        game.snake.direction = Direction.DOWN
        
        result = game.move(Direction.DOWN)  # Should hit body
        
        assert result == False
        assert game.is_game_over
    
    def test_cannot_reverse_direction(self):
        """Snake cannot instantly reverse."""
        game = SnakeGame(10, 10, (5, 5))
        game.snake.direction = Direction.RIGHT
        
        # Try to go left (opposite)
        game.move(Direction.LEFT)
        
        # Should continue RIGHT, not LEFT
        assert game.snake.direction == Direction.RIGHT
    
    def test_food_consumption(self):
        """Snake grows and score increases when eating."""
        game = SnakeGame(10, 10, (5, 5))
        game.food = (4, 5)  # Place food above snake
        initial_length = game.snake.length
        
        game.move(Direction.UP)  # Eat food
        
        assert game.snake.length == initial_length + 1
        assert game.score == 10
        assert game.food != (4, 5)  # New food placed
    
    def test_out_of_bounds_initial_position(self):
        """Raise error for invalid initial position."""
        with pytest.raises(ValueError):
            SnakeGame(10, 10, (100, 100))
    
    def test_move_after_game_over(self):
        """Raise error when moving after game over."""
        game = SnakeGame(10, 10, (0, 0))
        game.move(Direction.UP)  # Game over
        
        with pytest.raises(RuntimeError):
            game.move(Direction.RIGHT)
```

---

## ⚠️ Edge Cases

| Edge Case | How to Handle |
|-----------|---------------|
| **Snake fills entire board** | Cannot place food - declare win |
| **Initial position out of bounds** | Raise `ValueError` |
| **Board too small (1×1)** | Game ends immediately |
| **Food spawns on snake** | Loop until valid position found |
| **Move called after game over** | Raise `RuntimeError` |
| **Instant direction reversal** | Ignore invalid direction change |

---

## 📊 Complexity Analysis

| Operation | Time | Space | Why |
|-----------|------|-------|-----|
| `move()` | O(1) | O(1) | deque operations |
| `grow()` | O(1) | O(1) | appendleft only |
| `is_collision()` | O(1) | - | set lookup |
| `place_food()` | O(K) | O(1) | K = attempts |
| `print_board()` | O(R×C) | O(R×C) | Full grid |

**Total Space:** O(snake_length + board_size)

---

## ❌ Common Mistakes

### **MISTAKE 1: Using List instead of Deque** ❌
```python
# WRONG - O(N) for remove at end
body = []
body.pop()  # O(1)
body.insert(0, new_head)  # O(N)!

# CORRECT - O(1) for both ends
body = deque()
body.popleft()     # O(1)
body.appendleft()  # O(1)
```

### **MISTAKE 2: O(N) Collision Check** ❌
```python
# WRONG - O(N) every time
def is_collision(self, pos):
    return pos in self.body  # O(N) list search!

# CORRECT - O(1) with set
def is_collision(self, pos):
    return pos in self.occupied  # O(1) set lookup
```

### **MISTAKE 3: Not Preventing Reverse** ❌
```python
# WRONG - Snake can reverse and hit itself
def change_direction(self, new_dir):
    self.direction = new_dir  # Can go UP then DOWN!

# CORRECT - Check opposite
def change_direction(self, new_dir):
    if not self.direction.is_opposite(new_dir):
        self.direction = new_dir
```

---

## 💯 Interview Checklist

Before finishing, ensure you've mentioned:
- [ ] ✅ **deque** for O(1) head/tail operations
- [ ] ✅ **set** for O(1) collision detection
- [ ] ✅ **Enum** for directions (not magic strings)
- [ ] ✅ **SRP** - separate Snake, Board, Game classes
- [ ] ✅ **Preventing reverse direction**
- [ ] ✅ **Edge cases** (boundaries, null checks)
- [ ] ✅ **Extensibility** (obstacles, multiplayer)
- [ ] ✅ **Testing strategy**

---

**Related LeetCode Problems:**
- LeetCode 353: Design Snake Game

**Real-World Applications:**
- Nokia Snake (classic game)
- Slither.io (multiplayer version)
