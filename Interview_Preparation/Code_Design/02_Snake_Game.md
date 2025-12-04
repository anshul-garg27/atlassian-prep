# 🐍 PROBLEM 2: SNAKE GAME (LOW-LEVEL DESIGN)

### ⭐⭐⭐⭐⭐ **Design and Implement Snake Game**

**Frequency:** Appears in **50%** of Atlassian Code Design rounds!
**Difficulty:** Medium
**Time to Solve:** 35-45 minutes
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

## 🎯 INTERVIEW FLOW: Step-by-Step Guide

### **PHASE 1: Clarify Requirements (2-3 minutes)**

**SAY THIS:**
> "Before I start designing, let me clarify a few requirements:"

**Questions to Ask:**
1. "What's the board size? Fixed or configurable?"
2. "How does the snake grow - immediately or after next move?"
3. "Can the snake wrap around the board edges?"
4. "Should I implement the game loop or just the core logic?"
5. "Do we need to support obstacles or power-ups?"

**WRITE DOWN the answers. This shows you're thorough.**

---

### **PHASE 2: Discuss Data Structure Options (3-4 minutes)**

**SAY THIS:**
> "Let me discuss the key data structure choices for efficient snake operations."

#### **Snake Body Storage: List vs Deque**

```text
Operation       | List      | Deque
----------------|-----------|--------
Add head        | O(N)      | O(1)    ← Winner!
Remove tail     | O(1)      | O(1)
Access by index | O(1)      | O(N)
```

**Explain:**
> "I'll use `deque` because snake movement requires frequent head/tail operations. 
> Adding to the front of a list is O(N), but deque gives us O(1) for both ends."

---

#### **Collision Detection: List vs Set**

```text
Check if position in snake body:
- List: O(N) - must scan entire body
- Set: O(1) - hash lookup

For a snake of length 100, that's 100x faster!
```

**Explain:**
> "I'll maintain a parallel `set` of occupied positions for O(1) collision detection.
> This is the key optimization interviewers look for."

---

### **PHASE 3: High-Level Design (2-3 minutes)**

**SAY THIS:**
> "Let me draw the class structure following Single Responsibility Principle."

**Draw on whiteboard:**
```
┌─────────────────────────────────────────────────────────┐
│                     SnakeGame                           │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Main controller - orchestrates game flow       │   │
│  │                                                  │   │
│  │  - snake: Snake                                 │   │
│  │  - board: Board                                 │   │
│  │  - food: Position                               │   │
│  │  - score: int                                   │   │
│  │  - game_over: bool                              │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  + move(direction) → bool                              │
│  + is_game_over() → bool                               │
│  + get_score() → int                                   │
└─────────────────────────────────────────────────────────┘
            │
            ├──────────────┬──────────────┐
            │              │              │
   ┌─────────────┐   ┌──────────┐   ┌───────────┐
   │    Snake    │   │   Board  │   │ Direction │
   ├─────────────┤   ├──────────┤   ├───────────┤
   │ - body:deque│   │ - rows   │   │ UP=(-1,0) │
   │ - occupied  │   │ - cols   │   │ DOWN=(1,0)│
   │ - direction │   │          │   │ LEFT=(0,-1)
   └─────────────┘   └──────────┘   │ RIGHT=(0,1)
                                    └───────────┘
```

**Explain the flow:**
> "When `move()` is called:
> 1. Calculate new head position based on direction
> 2. Check wall collision (Board responsibility)
> 3. Check self collision (Snake's occupied set)
> 4. If eating food: grow (don't remove tail)
> 5. If not eating: move (add head, remove tail)"

---

### **PHASE 4: Design Patterns & Principles (2 minutes)**

**SAY THIS:**
> "I'm following these OOP principles:"

#### **1. Single Responsibility Principle (SRP)** ⭐⭐⭐

| Class | Single Responsibility |
|-------|----------------------|
| `Snake` | Manage body positions and movement |
| `Board` | Manage grid boundaries |
| `Direction` | Encapsulate direction logic |
| `SnakeGame` | Orchestrate game rules |

**Why it matters:**
> "If we want to add obstacles, we only modify `SnakeGame`, not `Snake` or `Board`."

---

#### **2. Encapsulation** ⭐⭐

```python
class Snake:
    def is_collision(self, pos: Position) -> bool:
        return pos in self._occupied  # O(1) - internal set
    
    # Client doesn't need to know about the internal set
```

---

#### **3. Open/Closed Principle (OCP)** ⭐

```python
# Easy to extend without modifying existing code
class SnakeGameWithObstacles(SnakeGame):
    def __init__(self, ...):
        super().__init__(...)
        self.obstacles: Set[Position] = set()
```

---

### **PHASE 5: Data Structures & Why (2 minutes)**

**SAY THIS:**
> "Let me explain my data structure choices."

| Data Structure | Used For | Why This Choice |
|----------------|----------|-----------------|
| `deque` | Snake body | O(1) head add, O(1) tail remove |
| `set` | Occupied positions | O(1) collision detection |
| `Enum` | Direction | Type safety, built-in opposite check |
| `tuple` | Position (row, col) | Immutable, hashable for sets |
| `dataclass` | Snake, Board | Clean initialization, less boilerplate |

**Key Insight:**
> "The combination of `deque` + `set` is crucial. 
> `deque` maintains order for rendering, `set` provides O(1) collision check.
> We update both in sync during move/grow operations."

---

### **PHASE 6: Write the Code (15-20 minutes)**

**SAY THIS:**
> "Now let me implement this. I'll start with Direction enum, then Snake, Board, and finally SnakeGame."

```python
"""
Snake Game - Low-Level Design Implementation
============================================
Clean OOP implementation using Python's modern features.

Design Principles:
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
    
    Using Enum provides:
    - Type safety (no magic strings)
    - Built-in opposite direction checking
    - Self-documenting code
    """
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)
    
    def is_opposite(self, other: 'Direction') -> bool:
        """
        Check if two directions are opposite.
        Snake cannot instantly reverse - this prevents that.
        """
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
    1. Uses deque for O(1) head/tail operations
    2. Uses set for O(1) collision detection
    3. Prevents instant direction reversal
    
    Why both deque AND set?
    - deque: Maintains order (head to tail) for rendering
    - set: Provides O(1) "is position occupied?" lookup
    - We keep them in sync during move/grow
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
        """Get current head position. O(1)"""
        return self.body[0]
    
    @property
    def tail(self) -> Position:
        """Get current tail position. O(1)"""
        return self.body[-1]
    
    @property
    def length(self) -> int:
        """Get current snake length."""
        return len(self.body)
    
    def change_direction(self, new_direction: Direction) -> bool:
        """
        Change snake direction.
        
        Validates that new direction is not opposite to current.
        This prevents the snake from reversing into itself.
        
        Returns: True if direction changed, False if invalid
        """
        if self.direction.is_opposite(new_direction):
            return False  # Ignore invalid direction change
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
        
        Operations (all O(1)):
        1. Add new head to front of deque
        2. Add new head to occupied set
        3. Remove tail from back of deque
        4. Remove tail from occupied set
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
        Called when snake eats food.
        """
        self.body.appendleft(new_head)
        self.occupied.add(new_head)

    def is_collision(self, position: Position) -> bool:
        """
        Check if position collides with snake body.
        O(1) lookup using set!
        """
        return position in self.occupied
    
    def get_body_positions(self) -> List[Position]:
        """Get list of all body positions (for rendering)."""
        return list(self.body)


@dataclass
class Board:
    """
    Game board managing grid boundaries.
    
    Responsibilities:
    - Validate positions are within bounds
    - Generate random positions (for food)
    """
    rows: int
    cols: int
    
    def __post_init__(self):
        """Validate board dimensions."""
        if self.rows <= 0 or self.cols <= 0:
            raise ValueError("Board dimensions must be positive")
    
    def is_within_bounds(self, position: Position) -> bool:
        """Check if position is within board boundaries."""
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
    
    This class owns the game rules:
    - Wall collision = game over
    - Self collision = game over
    - Eating food = grow + score
    
    Example:
        >>> game = SnakeGame(rows=10, cols=10, initial_pos=(5, 5))
        >>> game.move(Direction.UP)    # True - success
        >>> game.move(Direction.RIGHT) # True - success
        >>> game.is_game_over          # False
        >>> game.score                 # 0 (or 10 if food eaten)
    """
    
    SCORE_PER_FOOD = 10
    
    def __init__(self, rows: int, cols: int, initial_pos: Position):
        """
        Initialize game.
        
        Args:
            rows: Board height
            cols: Board width
            initial_pos: Starting position for snake (row, col)
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
        
        Game Loop:
        1. Try to change direction (ignored if opposite)
        2. Calculate next head position
        3. Check wall collision → game over
        4. Check self collision → game over
        5. Check food → grow or move
        
        Returns: True if move successful, False if game over
        """
        if self.game_over:
            raise RuntimeError("Game is already over!")

        # Step 1: Try to change direction (ignored if opposite)
        self.snake.change_direction(direction)

        # Step 2: Calculate next head position
        next_head = self.snake.get_next_head_position()

        # Step 3: Check wall collision
        if not self.board.is_within_bounds(next_head):
            self.game_over = True
            return False

        # Step 4: Check self collision
        # Special case: if next_head is current tail AND not eating,
        # the tail will move away, so no collision
        if self.snake.is_collision(next_head):
            if next_head != self.snake.tail or next_head == self.food:
            self.game_over = True
            return False

        # Step 5: Check if eating food
        if next_head == self.food:
            self.snake.grow(next_head)
            self.score += self.SCORE_PER_FOOD
            self.food = self._place_food()
        else:
            self.snake.move(next_head)

        return True

    def _place_food(self) -> Position:
        """
        Place food at random empty position.
        
        Note: In worst case (snake fills board), this could loop forever.
        Production code should handle this edge case.
        """
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


# ============ Demo ============
def main():
    """Demonstrate Snake Game functionality."""
    print("=" * 50)
    print("SNAKE GAME DEMO")
    print("=" * 50)
    
    game = SnakeGame(rows=10, cols=10, initial_pos=(5, 5))
    
    print("\nInitial State:")
    game.print_board()

    # Simulate moves
    moves = [Direction.UP, Direction.UP, Direction.RIGHT, 
             Direction.RIGHT, Direction.DOWN]
    
    for i, move in enumerate(moves):
        print(f"\n--- Move {i+1}: {move.name} ---")
        success = game.move(move)
    game.print_board()

        if not success:
            print("GAME OVER!")
            break
    
    print(f"\nFinal Score: {game.score}")


if __name__ == "__main__":
    main()
```

---

### **PHASE 7: Walk Through Edge Cases (3-4 minutes)**

**SAY THIS:**
> "Let me discuss the edge cases I've handled."

| Edge Case | How Handled | Code Location |
|-----------|-------------|---------------|
| **Snake reverses direction** | Ignore invalid direction change | `change_direction()` |
| **Hit wall** | Game over | `move()` - bounds check |
| **Hit self** | Game over | `move()` - collision check |
| **Snake moves to current tail** | Allow (tail moves away) | `move()` - special case |
| **Food spawns on snake** | Keep regenerating | `_place_food()` while loop |
| **Initial position out of bounds** | Raise ValueError | `__init__()` validation |
| **Move after game over** | Raise RuntimeError | `move()` check |

**Explain tail collision edge case:**
> "This is subtle: if the snake's next head position is exactly where its tail currently is,
> and it's NOT eating food, the tail will move away before the head arrives.
> So this is actually a valid move, not a collision."

---

### **PHASE 8: Testing Strategy (2-3 minutes)**

**SAY THIS:**
> "Here's how I would test this."

```python
import pytest
from collections import deque

class TestSnakeGame:
    """Comprehensive test suite for Snake Game."""
    
    def test_initial_state(self):
        """Game starts with correct initial state."""
        game = SnakeGame(10, 10, (5, 5))
        
        assert not game.is_game_over
        assert game.score == 0
        assert game.snake.head == (5, 5)
        assert game.snake.length == 1
    
    def test_basic_movement(self):
        """Snake moves correctly in given direction."""
        game = SnakeGame(10, 10, (5, 5))
        
        result = game.move(Direction.UP)
        
        assert result == True
        assert game.snake.head == (4, 5)
        assert not game.is_game_over
    
    def test_wall_collision_top(self):
        """Game ends when snake hits top wall."""
        game = SnakeGame(10, 10, (0, 5))  # At top edge
        
        result = game.move(Direction.UP)
        
        assert result == False
        assert game.is_game_over
    
    def test_wall_collision_all_sides(self):
        """Test wall collision on all four sides."""
        # Top wall
        game = SnakeGame(10, 10, (0, 5))
        assert game.move(Direction.UP) == False
        
        # Bottom wall
        game = SnakeGame(10, 10, (9, 5))
        assert game.move(Direction.DOWN) == False
        
        # Left wall
        game = SnakeGame(10, 10, (5, 0))
        assert game.move(Direction.LEFT) == False
        
        # Right wall
        game = SnakeGame(10, 10, (5, 9))
        assert game.move(Direction.RIGHT) == False
    
    def test_cannot_reverse_direction(self):
        """Snake cannot instantly reverse direction."""
        game = SnakeGame(10, 10, (5, 5))
        game.snake.direction = Direction.RIGHT
        
        # Try to go left (opposite)
        game.move(Direction.LEFT)
        
        # Should continue RIGHT, not LEFT
        assert game.snake.direction == Direction.RIGHT
        assert game.snake.head == (5, 6)  # Moved right
    
    def test_food_consumption_grows_snake(self):
        """Snake grows when eating food."""
        game = SnakeGame(10, 10, (5, 5))
        game.food = (4, 5)  # Place food above snake
        initial_length = game.snake.length
        
        game.move(Direction.UP)  # Eat food
        
        assert game.snake.length == initial_length + 1
        assert game.score == 10
        assert game.food != (4, 5)  # New food placed
    
    def test_self_collision(self):
        """Game ends when snake hits itself."""
        game = SnakeGame(10, 10, (5, 5))
        # Manually create a snake that will hit itself
        game.snake.body = deque([(5, 5), (5, 6), (5, 7), (4, 7), (4, 6)])
        game.snake.occupied = set(game.snake.body)
        game.snake.direction = Direction.DOWN
        
        result = game.move(Direction.DOWN)
        
        assert result == False
        assert game.is_game_over
    
    def test_collision_detection_O1(self):
        """Collision detection should be O(1) using set."""
        snake = Snake((5, 5))
        # Add many positions
        for i in range(1000):
            snake.body.append((i, 0))
            snake.occupied.add((i, 0))
        
        # This should still be O(1)
        assert snake.is_collision((500, 0)) == True
        assert snake.is_collision((999, 999)) == False
    
    def test_out_of_bounds_initial_position(self):
        """Raise error for invalid initial position."""
        with pytest.raises(ValueError):
            SnakeGame(10, 10, (100, 100))
    
    def test_move_after_game_over(self):
        """Raise error when moving after game over."""
        game = SnakeGame(10, 10, (0, 0))
        game.move(Direction.UP)  # Game over - hit wall
        
        with pytest.raises(RuntimeError):
            game.move(Direction.RIGHT)
```

---

### **PHASE 9: Complexity Analysis (1 minute)**

**SAY THIS:**
> "Let me summarize the complexity."

| Operation | Time | Space | Why |
|-----------|------|-------|-----|
| `move()` | O(1) | O(1) | deque operations + set operations |
| `grow()` | O(1) | O(1) | appendleft + set add |
| `is_collision()` | O(1) | - | set lookup |
| `place_food()` | O(K) | O(1) | K = attempts until empty spot |
| `change_direction()` | O(1) | O(1) | Simple comparison |

**Total Space:** O(S + R×C) where S = snake length, R×C = board size

**Why O(1) for move?**
> "Because I use `deque` (not list) for O(1) appendleft, and `set` for O(1) collision check.
> If I used a list for collision check, every move would be O(N) where N = snake length."

---

### **PHASE 10: Extensions & Follow-ups (5+ minutes)**

#### **Q1: "How would you add obstacles?"**

**SAY THIS:**
> "I'd extend SnakeGame without modifying existing classes."

```python
class SnakeGameWithObstacles(SnakeGame):
    """Snake game with obstacles - demonstrates OCP."""
    
    def __init__(self, rows: int, cols: int, initial_pos: Position, 
                 obstacles: Set[Position] = None):
        self.obstacles = obstacles or set()
        super().__init__(rows, cols, initial_pos)
    
    def move(self, direction: Direction) -> bool:
        next_head = self.snake.get_next_head_position()
        
        # Check obstacle collision BEFORE parent logic
        if next_head in self.obstacles:
            self.game_over = True
            return False
        
        return super().move(direction)
```

---

#### **Q2: "How would you add multiple food types?"**

```python
class FoodType(Enum):
    NORMAL = (10, 1)    # (points, growth)
    GOLDEN = (50, 1)    # More points
    MEGA = (20, 3)      # Grow 3 segments

@dataclass
class Food:
    position: Position
    food_type: FoodType = FoodType.NORMAL
    
    @property
    def points(self) -> int:
        return self.food_type.value[0]
    
    @property
    def growth(self) -> int:
        return self.food_type.value[1]
```

---

#### **Q3: "How would you implement multiplayer?"**

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
        self.scores = [0, 0]
    
    def move(self, player_id: int, direction: Direction) -> bool:
        snake = self.snakes[player_id]
        next_head = snake.get_next_head_position()
        
        # Check collision with OTHER snakes
        for i, other_snake in enumerate(self.snakes):
            if i != player_id and other_snake.is_collision(next_head):
                return False  # Hit other player
        
        # ... rest of logic
```

---

## ❌ Common Mistakes (What NOT to Do)

### **MISTAKE 1: Using List Instead of Deque** ❌

```python
# WRONG - O(N) for insert at front!
body = []
body.insert(0, new_head)  # O(N) - shifts all elements!
body.pop()  # O(1)

# CORRECT - O(1) for both operations
from collections import deque
body = deque()
body.appendleft(new_head)  # O(1)
body.pop()  # O(1)
```

---

### **MISTAKE 2: O(N) Collision Check** ❌

```python
# WRONG - O(N) every time!
def is_collision(self, pos):
    return pos in self.body  # O(N) list search!

# CORRECT - O(1) with set
def is_collision(self, pos):
    return pos in self.occupied  # O(1) set lookup
```

---

### **MISTAKE 3: Not Preventing Direction Reversal** ❌

```python
# WRONG - Snake can reverse and instantly hit itself
def change_direction(self, new_dir):
    self.direction = new_dir  # Can go UP then DOWN!

# CORRECT - Check for opposite
def change_direction(self, new_dir):
    if not self.direction.is_opposite(new_dir):
        self.direction = new_dir
```

---

### **MISTAKE 4: Using Magic Strings** ❌

```python
# WRONG - Error-prone, no type checking
direction = "up"
if direction == "UP":  # Bug! Case mismatch
    ...

# CORRECT - Enum with type safety
class Direction(Enum):
    UP = (-1, 0)
    ...
```

---

## 💯 Interview Checklist

Before saying "I'm done," make sure you've covered:

- [ ] ✅ **Clarified requirements** (asked questions first)
- [ ] ✅ **Discussed data structure trade-offs** (deque vs list, set vs list)
- [ ] ✅ **Drew class diagram** (SRP - separate classes)
- [ ] ✅ **Used deque** for O(1) head/tail operations
- [ ] ✅ **Used set** for O(1) collision detection
- [ ] ✅ **Used Enum** for directions (not magic strings)
- [ ] ✅ **Prevented direction reversal**
- [ ] ✅ **Handled edge cases** (walls, self-collision, tail case)
- [ ] ✅ **Discussed complexity** (O(1) per move)
- [ ] ✅ **Mentioned testing approach**
- [ ] ✅ **Prepared extensions** (obstacles, multiplayer, food types)

---

## 📚 Quick Reference Card

**Print this and review before interview!**

```
┌────────────────────────────────────────────────────────────┐
│                    SNAKE GAME CHEAT SHEET                  │
├────────────────────────────────────────────────────────────┤
│ DATA STRUCTURES:                                           │
│   - deque for snake body → O(1) head/tail ops             │
│   - set for occupied positions → O(1) collision           │
│   - Enum for directions → type safety                     │
│                                                            │
│ KEY OPERATIONS (all O(1)):                                │
│   - move: appendleft + pop + set updates                  │
│   - grow: appendleft only (no pop)                        │
│   - collision: set lookup                                  │
│                                                            │
│ DESIGN PRINCIPLES:                                        │
│   - SRP: Snake, Board, Game separate                      │
│   - OCP: Easy to extend (obstacles, multiplayer)          │
│   - Encapsulation: Internal set hidden                    │
│                                                            │
│ EDGE CASES:                                               │
│   - Direction reversal → ignore                           │
│   - Head moves to tail → allow (tail moves away)         │
│   - Food on snake → regenerate                           │
│   - Out of bounds → game over                            │
│                                                            │
│ COMPLEXITY:                                               │
│   - Time: O(1) per move                                   │
│   - Space: O(snake_length)                                │
└────────────────────────────────────────────────────────────┘
```

---

**Related Problems:**
- LeetCode 353: Design Snake Game

**Real-World Applications:**
- Nokia Snake (classic game)
- Slither.io (multiplayer version)
- Google Snake (browser game)

