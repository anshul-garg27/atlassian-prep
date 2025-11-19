# 🐍 PROBLEM 2: SNAKE GAME

### ⭐⭐⭐⭐⭐ **Design and Implement Snake Game**

**Frequency:** Very High (Appears in ~50% of rounds)
**Difficulty:** Medium
**Similar to:** [LeetCode 353. Design Snake Game](https://leetcode.com/problems/design-snake-game/)

---

## 📋 Problem Statement

Design a Snake game that runs on a 2D grid. The snake starts at position (0, 0) with initial length of 1 and grows as it eats food.

**Game Rules:**
1. The snake starts at the top-left corner (0, 0) with length 1
2. The snake moves in one of four directions: UP, DOWN, LEFT, RIGHT
3. The snake grows by 1 unit when it eats food
4. The game ends if:
   - The snake hits the boundary (goes out of bounds)
   - The snake hits itself (head collides with body)
5. Return the current score (number of foods eaten) or -1 if game over

**API to Implement:**
```python
class SnakeGame:
    def __init__(self, width, height, food):
        """
        Initialize game with board size and food positions.
        
        Args:
            width: Width of the board
            height: Height of the board  
            food: List of food positions [[row1, col1], [row2, col2], ...]
        """
        
    def move(self, direction):
        """
        Move snake in the given direction.
        
        Args:
            direction: One of "U", "D", "L", "R"
            
        Returns:
            Current score (foods eaten), or -1 if game over
        """
```

**Constraints:**
- 1 ≤ width, height ≤ 10⁴
- 0 ≤ food.length ≤ 50
- Direction is guaranteed to be one of: "U", "D", "L", "R"
- Food appears one at a time (eat current food to see next)

---

## 🎨 Visual Example

### Initial State

```text
Grid: 3x3
Snake: [(0,0)]  (length = 1)
Food: [(1,2), (0,1)]

  0   1   2
┌───┬───┬───┐
│ S │   │   │ 0
├───┼───┼───┤
│   │   │ F │ 1
├───┼───┼───┤
│   │   │   │ 2
└───┴───┴───┘

S = Snake Head
F = Food (only first food is visible)
```

### Move Sequence

**Move 1: move("R") → Score 0**
```text
  0   1   2
┌───┬───┬───┐
│   │ S │   │ 0    Snake moved right: (0,0) → (0,1)
├───┼───┼───┤       Food at (1,2) not reached yet
│   │   │ F │ 1
├───┼───┼───┤
│   │   │   │ 2
└───┴───┴───┘
```

**Move 2: move("D") → Score 0**
```text
  0   1   2
┌───┬───┬───┐
│   │   │   │ 0    
├───┼───┼───┤
│   │ S │ F │ 1    Snake moved down: (0,1) → (1,1)
├───┼───┼───┤
│   │   │   │ 2
└───┴───┴───┘
```

**Move 3: move("R") → Score 1 (Ate food!)**
```text
  0   1   2
┌───┬───┬───┐
│   │   │ F │ 0    Snake ate food at (1,2)!
├───┼───┼───┤       Snake grows: [(1,2), (1,1)]
│   │ ● │ S │ 1    Next food appears at (0,2)
├───┼───┼───┤       ● = Snake body, S = Snake head
│   │   │   │ 2
└───┴───┴───┘
```

**Move 4: move("U") → Score 1**
```text
  0   1   2
┌───┬───┬───┐
│   │   │ S │ 0    Snake moved up: [(0,2), (1,2)]
├───┼───┼───┤       Tail removed from (1,1), head added at (0,2)
│   │   │ ● │ 1    Food at (0,2) reached!
├───┼───┼───┤
│   │   │   │ 2
└───┴───┴───┘
```

**Move 5: move("U") → Score -1 (Hit boundary!)**
```text
  ╔═══════════╗
  ║ GAME OVER ║    Snake tried to move from (0,2) to (-1,2)
  ╚═══════════╝    Out of bounds! Return -1
```

---

## 💡 Examples

### Example 1: Basic Movement
```python
game = SnakeGame(3, 2, [[1, 2], [0, 1]])
# Grid: 3x2 (width=3, height=2)
# Food at: (1,2) then (0,1)

game.move("R")  # → 0  Snake at (0,1)
game.move("D")  # → 0  Snake at (1,1)
game.move("R")  # → 1  Snake eats food at (1,2), grows to length 2
game.move("U")  # → 1  Snake at (0,2)
game.move("L")  # → 2  Snake eats food at (0,1), grows to length 3
game.move("U")  # → -1 Out of bounds!
```

### Example 2: Self-Collision
```python
game = SnakeGame(3, 3, [[2, 0]])
game.move("R")  # → 0  Snake: [(0,1)]
game.move("D")  # → 0  Snake: [(1,1)]
game.move("L")  # → 0  Snake: [(1,0)]
game.move("D")  # → 1  Snake: [(2,0), (1,0)] - ate food!
game.move("R")  # → 1  Snake: [(2,1), (2,0)]
game.move("U")  # → 1  Snake: [(1,1), (2,1)]
game.move("L")  # → -1 Snake head at (1,0) hits body at (1,0)!
```

### Example 3: Long Snake Growth
```python
game = SnakeGame(3, 3, [[0,1], [0,2], [1,2], [2,2]])
# Snake will grow to length 5 by eating 4 foods
```

---

## 🗣️ Interview Conversation Guide

### Phase 1: Clarification (3-5 min)

**Candidate:** "What's the initial position and length of the snake?"
**Interviewer:** "Snake starts at (0, 0) with length 1."

**Candidate:** "Does the snake grow every move or only when eating food?"
**Interviewer:** "Only when eating food. Each food item increases length by 1."

**Candidate:** "Are the food positions given all at once?"
**Interviewer:** "Yes, you get a list of food positions, but only the first one is active. After eating it, the next becomes active."

**Candidate:** "What defines game over?"
**Interviewer:** "Two conditions: hitting the boundary or hitting the snake's own body."

**Candidate:** "For self-collision, does the head need to hit the body, or can we count if it goes to the same position?"
**Interviewer:** "Head colliding with any body segment (but not the tail if the tail just moved away)."

**Candidate:** "What should I return for each move?"
**Interviewer:** "Return the current score (number of foods eaten), or -1 if the game is over."

### Phase 2: Approach Discussion (5-8 min)

**Candidate:** "This is a simulation problem. I need to:
1. Track the snake's body positions efficiently
2. Check boundary and collision conditions
3. Handle growth mechanics when eating food

For the data structure, I'm thinking:
- **Deque** for the snake body (O(1) add head, O(1) remove tail)
- **HashSet** for O(1) collision detection
- **Queue/Index** to track which food is next"

**Candidate:** "The algorithm for each move:
1. Calculate new head position based on direction
2. Check if out of bounds → return -1
3. Check if new head position is food → grow snake
4. If not food, remove tail from body and HashSet
5. Add new head to body and HashSet
6. Check if new head hits body (self-collision) → return -1
7. Return current score"

**Interviewer:** "Good! One edge case: when you eat food and grow, you don't remove the tail. How does that affect collision checking?"

**Candidate:** "Right! If I'm checking for self-collision, I need to be careful. When we grow, the old tail stays, so I need to check collision BEFORE adding the new head to the set, or handle the timing correctly."

### Phase 3: Coding (15-20 min)

**Candidate:** "I'll implement using:
1. `deque` for snake body (stores coordinates)
2. `set` for fast collision detection
3. Track current food index and score"

---

## 🧠 Intuition & Approach

### Why Deque + HashSet?

**Problem:** We need to:
1. **Add to front** (new head position) → O(1)
2. **Remove from back** (tail when not growing) → O(1)
3. **Check membership** (is position occupied by body?) → O(1)

**Solution:**
- **Deque (Double-Ended Queue):** Perfect for adding/removing from both ends in O(1)
- **HashSet:** Stores all body positions for O(1) collision checking

**Why NOT just use:**
- **List:** Removing from front is O(N)
- **Only HashSet:** Can't maintain order of body segments
- **2D Array:** Sparse representation wastes space for large grids

### Movement Algorithm

```text
For each move(direction):

┌─────────────────────────┐
│ 1. Calculate new head   │
│    based on direction   │
└────────┬────────────────┘
         │
┌────────▼────────────────┐
│ 2. Check out of bounds  │──Yes──> Return -1
└────────┬────────────────┘
         │ No
┌────────▼────────────────┐
│ 3. Check if food eaten  │
└────┬──────────┬─────────┘
     │          │
     │ Yes      │ No
     │          │
┌────▼──────┐  ┌▼──────────────┐
│ Grow      │  │ Remove tail   │
│ (keep     │  │ from body     │
│  tail)    │  │ and set       │
└────┬──────┘  └┬──────────────┘
     │          │
     └────┬─────┘
          │
┌─────────▼──────────────┐
│ 4. Add new head        │
│    to body and set     │
└─────────┬──────────────┘
          │
┌─────────▼──────────────┐
│ 5. Check self-collision│──Yes──> Return -1
└─────────┬──────────────┘
          │ No
┌─────────▼──────────────┐
│ 6. Return score        │
└────────────────────────┘
```

### Edge Case: Collision After Growth

**Tricky Case:** After eating food, can the snake immediately collide with itself?

```text
Before:        After eating food at (1,2):
  
  ●─●            ●─●─S
    S            
    F
    
If next move is LEFT, head goes to (1,1):
  ●─S─●  ← Head collides with body!
```

**Solution:** Check collision AFTER adding new head, but account for tail that was just removed (if not growing).

---

## 📝 Complete Solution

```python
from collections import deque
from typing import List

class SnakeGame:
    """
    Snake Game implementation using Deque + HashSet.
    
    Time Complexity: O(1) per move
    Space Complexity: O(W × H) worst case if snake fills entire grid
    """
    
    def __init__(self, width: int, height: int, food: List[List[int]]):
        """
        Initialize the snake game.
        
        Args:
            width: Width of the board (columns)
            height: Height of the board (rows)
            food: List of food positions [[row, col], ...]
        """
        self.width = width
        self.height = height
        self.food = food
        self.food_index = 0  # Index of next food to eat
        self.score = 0
        
        # Snake body as deque: head at right, tail at left
        # Format: deque([(row, col), ...])
        self.snake = deque([(0, 0)])
        
        # Set for O(1) collision detection
        # Note: Initial position (0,0) is in the set
        self.snake_set = {(0, 0)}
        
        # Direction mappings
        self.directions = {
            'U': (-1, 0),  # Up: row-1
            'D': (1, 0),   # Down: row+1
            'L': (0, -1),  # Left: col-1
            'R': (0, 1)    # Right: col+1
        }
    
    def move(self, direction: str) -> int:
        """
        Move the snake in the given direction.
        
        Args:
            direction: One of "U", "D", "L", "R"
            
        Returns:
            Current score (number of foods eaten), or -1 if game over
            
        Time: O(1)
        Space: O(1)
        """
        # 1. Calculate new head position
        d_row, d_col = self.directions[direction]
        head_row, head_col = self.snake[-1]  # Current head (rightmost)
        new_head_row = head_row + d_row
        new_head_col = head_col + d_col
        new_head = (new_head_row, new_head_col)
        
        # 2. Check boundary conditions
        if (new_head_row < 0 or new_head_row >= self.height or
            new_head_col < 0 or new_head_col >= self.width):
            return -1  # Hit boundary - game over
        
        # 3. Check if food is eaten
        is_food = False
        if (self.food_index < len(self.food) and
            new_head_row == self.food[self.food_index][0] and
            new_head_col == self.food[self.food_index][1]):
            is_food = True
            self.score += 1
            self.food_index += 1
        
        # 4. Handle tail (remove if not growing)
        if not is_food:
            # Not eating food: remove tail
            tail = self.snake.popleft()
            self.snake_set.remove(tail)
        # If eating food: don't remove tail (snake grows)
        
        # 5. Add new head
        self.snake.append(new_head)
        
        # 6. Check self-collision
        # Important: Check AFTER adding new head
        if new_head in self.snake_set:
            return -1  # Hit itself - game over
        
        # Add to set AFTER collision check
        self.snake_set.add(new_head)
        
        # 7. Return current score
        return self.score


# ============================================
# COMPLETE RUNNABLE EXAMPLE
# ============================================

if __name__ == "__main__":
    print("=" * 50)
    print("SNAKE GAME SIMULATION")
    print("=" * 50)
    
    # Test Case 1: Basic Movement and Food
    print("\n[Test 1] Basic Movement")
    game = SnakeGame(3, 2, [[1, 2], [0, 1]])
    
    moves = ["R", "D", "R", "U", "L", "U"]
    expected = [0, 0, 1, 1, 2, -1]
    
    for i, (move, exp) in enumerate(zip(moves, expected)):
        result = game.move(move)
        status = "✓" if result == exp else "✗"
        print(f"{status} Move {i+1}: {move} → Score: {result} (expected {exp})")
    
    # Test Case 2: Self-Collision
    print("\n[Test 2] Self-Collision")
    game2 = SnakeGame(3, 3, [[2, 0]])
    
    moves2 = ["R", "D", "L", "D", "R", "U", "L"]
    for i, move in enumerate(moves2):
        result = game2.move(move)
        print(f"Move {i+1}: {move} → Score: {result}")
        if result == -1:
            print("   Game Over (Self-collision)")
            break
    
    # Test Case 3: Boundary Check
    print("\n[Test 3] Boundary Check")
    game3 = SnakeGame(2, 2, [[0, 1]])
    
    result1 = game3.move("R")  # (0,0) → (0,1) - eat food
    print(f"Move R: Score {result1} (ate food)")
    
    result2 = game3.move("R")  # (0,1) → (0,2) - out of bounds!
    print(f"Move R: Score {result2} (out of bounds)")
    
    print("\nAll test cases completed! ✓")
```

---

## 🔍 Explanation with Example

Let's trace through **Example 1** step by step:

**Setup:**
```python
game = SnakeGame(3, 2, [[1, 2], [0, 1]])
# Board: 3 wide, 2 tall
# Foods: [1,2] then [0,1]
# Snake starts at (0,0)
```

**State Variables:**
```
snake = deque([(0,0)])
snake_set = {(0,0)}
score = 0
food_index = 0
```

---

**Move 1: move("R")**

1. Calculate new head: (0,0) + (0,1) = (0,1)
2. Check bounds: 0 ≤ 0 < 2 ✓, 0 ≤ 1 < 3 ✓
3. Check food: (0,1) ≠ (1,2) → No food
4. Remove tail: Remove (0,0) from snake and set
5. Add head: Add (0,1) to snake and set
6. Check collision: (0,1) not in old set ✓
7. Return score = 0

```
snake = deque([(0,1)])
snake_set = {(0,1)}
```

---

**Move 2: move("D")**

1. New head: (0,1) + (1,0) = (1,1)
2. Bounds: OK ✓
3. Food: (1,1) ≠ (1,2) → No food
4. Remove tail: (0,1)
5. Add head: (1,1)
6. No collision ✓
7. Return score = 0

```
snake = deque([(1,1)])
snake_set = {(1,1)}
```

---

**Move 3: move("R")**

1. New head: (1,1) + (0,1) = (1,2)
2. Bounds: OK ✓
3. Food: (1,2) == (1,2) → **FOOD EATEN!**
   - score = 1
   - food_index = 1
   - is_food = True
4. **Don't remove tail** (growing!)
5. Add head: (1,2)
6. No collision ✓
7. Return score = 1

```
snake = deque([(1,1), (1,2)])  ← Length 2!
snake_set = {(1,1), (1,2)}
```

---

**Move 4: move("U")**

1. New head: (1,2) + (-1,0) = (0,2)
2. Bounds: OK ✓
3. Food: (0,2) ≠ (0,1) → No food
4. Remove tail: (1,1)
5. Add head: (0,2)
6. No collision ✓
7. Return score = 1

```
snake = deque([(1,2), (0,2)])
snake_set = {(1,2), (0,2)}
```

---

**Move 5: move("L")**

1. New head: (0,2) + (0,-1) = (0,1)
2. Bounds: OK ✓
3. Food: (0,1) == (0,1) → **FOOD EATEN!**
   - score = 2
   - food_index = 2
4. Don't remove tail (growing!)
5. Add head: (0,1)
6. No collision ✓
7. Return score = 2

```
snake = deque([(1,2), (0,2), (0,1)])  ← Length 3!
snake_set = {(1,2), (0,2), (0,1)}
```

---

**Move 6: move("U")**

1. New head: (0,1) + (-1,0) = (-1,1)
2. Bounds: -1 < 0 → **OUT OF BOUNDS!**
3. Return -1 (Game Over)

---

## 🔍 Complexity Analysis

### Time Complexity: **O(1) per move**

**Breakdown:**
- **Calculate new position:** O(1) arithmetic
- **Boundary check:** O(1) comparison
- **Food check:** O(1) comparison
- **Deque operations:**
  - `popleft()`: O(1)
  - `append()`: O(1)
- **Set operations:**
  - `remove()`: O(1) average
  - `add()`: O(1) average
  - `in` check: O(1) average
- **Total:** O(1)

### Space Complexity: **O(N) where N = snake length**

**Breakdown:**
- **Deque storage:** O(N) for N body segments
- **Set storage:** O(N) for N positions
- **Food list:** O(F) where F = number of foods (given as input)
- **Total:** O(N + F)

**Worst Case:** Snake fills entire grid → N = W × H → O(W × H)

**Typical Case:** Snake length << grid size → Much less space

---

## ⚠️ Common Pitfalls

### 1. **Wrong Collision Check Timing**

**Problem:**
```python
# ❌ WRONG: Check collision BEFORE removing tail
if new_head in self.snake_set:
    return -1

if not is_food:
    tail = self.snake.popleft()
    self.snake_set.remove(tail)
```

**Why it fails:** If snake moves to where its tail was, it incorrectly detects collision.

**Fix:** Remove tail BEFORE checking collision (or check collision AFTER adding head).

---

### 2. **Forgetting to Update Set**

**Problem:**
```python
# ❌ WRONG: Update deque but forget set
self.snake.append(new_head)
# Missing: self.snake_set.add(new_head)
```

**Why it fails:** Set becomes out of sync with deque, collision detection fails.

**Fix:** Always update both deque AND set together.

---

### 3. **Growing Logic Error**

**Problem:**
```python
# ❌ WRONG: Always remove tail
tail = self.snake.popleft()  # Bug: removes tail even when eating
self.snake_set.remove(tail)

if is_food:
    # Try to add tail back? Too complicated!
```

**Why it fails:** Snake doesn't grow when eating food.

**Fix:** Conditionally remove tail only when NOT eating food.

---

### 4. **Coordinate Confusion**

**Problem:** Mixing up row vs col, or (x,y) vs (row,col).

**Why it fails:**
- Food given as `[row, col]`
- "U" and "D" change row, "L" and "R" change col
- Easy to swap them!

**Fix:** Use consistent naming (`row`, `col`) and comment clearly.

---

### 5. **Self-Collision with Tail**

**Edge Case:**
```python
# Snake: [(1,1), (1,2), (2,2)]
# After removing tail (1,1) and adding head (2,1)
# New snake: [(1,2), (2,2), (2,1)]

# If tail was just removed, new head might be at old tail position
# This is OK! Not a collision.
```

**Solution:** Our implementation handles this by removing tail BEFORE checking collision.

---

## 🔄 Follow-up Questions

### Follow-up 1: Wraparound Boundaries

**Problem Statement:**
> "Instead of game over when hitting boundaries, make the board wrap around (like Pac-Man). If snake exits the right edge, it appears on the left edge."

**Visual Example:**
```text
Normal Boundary:          Wraparound Boundary:

     │                         
   S │   (move right)      
     │                         
─────┴─────               ─────┬─────
 Game Over!                S   │
                          (appears on left!)
```

**Solution:**

The change is minimal - just modify the boundary check:

```python
def move(self, direction: str) -> int:
    """Modified move with wraparound boundaries."""
    
    # 1. Calculate new head position
    d_row, d_col = self.directions[direction]
    head_row, head_col = self.snake[-1]
    new_head_row = head_row + d_row
    new_head_col = head_col + d_col
    
    # 2. Wraparound instead of boundary check
    new_head_row = new_head_row % self.height
    new_head_col = new_head_col % self.width
    new_head = (new_head_row, new_head_col)
    
    # Remove old boundary check:
    # if (new_head_row < 0 or new_head_row >= self.height or ...):
    #     return -1
    
    # 3-7. Rest remains the same
    # ... (food check, tail removal, collision check, etc.)
```

**Explanation:**

Modulo operator `%` wraps coordinates:
- `-1 % 3 = 2` (left edge wraps to right)
- `3 % 3 = 0` (right edge wraps to left)
- `5 % 3 = 2` (wraps around multiple times)

**Test Case:**
```python
game = SnakeGame(3, 3, [[0, 1]])

# Snake at (0, 2)
result = game.move("R")  # (0, 2) + (0, 1) = (0, 3)
# Wraparound: (0, 3 % 3) = (0, 0)
# Snake now at left edge!
assert result != -1  # Game continues
```

**Time Complexity:** Still O(1) per move
**Space Complexity:** Unchanged

---

### Follow-up 2: Multiple Food Items Visible

**Problem Statement:**
> "Instead of showing one food at a time, show all remaining food on the board. Snake can eat any visible food."

**Visual Example:**
```text
Single Food (Original):     Multiple Foods (Follow-up):

  S   ·   ·                  S   F₂  F₃
  ·   ·   F₁                 ·   ·   F₁
  ·   ·   ·                  F₄  ·   ·

Only F₁ is visible           All foods visible!
```

**Solution:**

```python
from collections import deque
from typing import List, Set, Tuple

class SnakeGameMultiFood:
    """
    Snake game where all remaining foods are visible.
    Snake can eat any food on the board.
    """
    
    def __init__(self, width: int, height: int, food: List[List[int]]):
        self.width = width
        self.height = height
        self.score = 0
        
        self.snake = deque([(0, 0)])
        self.snake_set = {(0, 0)}
        
        # Store all remaining foods as a set for O(1) lookup
        self.food_set: Set[Tuple[int, int]] = set()
        for f in food:
            self.food_set.add((f[0], f[1]))
        
        self.directions = {
            'U': (-1, 0),
            'D': (1, 0),
            'L': (0, -1),
            'R': (0, 1)
        }
    
    def move(self, direction: str) -> int:
        """
        Move snake. Can eat any visible food.
        
        Time: O(1)
        """
        # 1. Calculate new head
        d_row, d_col = self.directions[direction]
        head_row, head_col = self.snake[-1]
        new_head_row = head_row + d_row
        new_head_col = head_col + d_col
        new_head = (new_head_row, new_head_col)
        
        # 2. Boundary check
        if (new_head_row < 0 or new_head_row >= self.height or
            new_head_col < 0 or new_head_col >= self.width):
            return -1
        
        # 3. Check if ANY food is at new position
        is_food = new_head in self.food_set
        
        if is_food:
            self.score += 1
            self.food_set.remove(new_head)  # Remove eaten food
        else:
            # Not eating: remove tail
            tail = self.snake.popleft()
            self.snake_set.remove(tail)
        
        # 4. Add new head
        self.snake.append(new_head)
        
        # 5. Check collision
        if new_head in self.snake_set:
            return -1
        
        self.snake_set.add(new_head)
        
        return self.score
    
    def get_visible_foods(self) -> List[Tuple[int, int]]:
        """Return all remaining food positions."""
        return list(self.food_set)


# Test
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("FOLLOW-UP 2: MULTIPLE VISIBLE FOODS")
    print("=" * 60)
    
    game = SnakeGameMultiFood(3, 3, [[0, 1], [1, 1], [2, 2]])
    
    print(f"\nInitial foods: {game.get_visible_foods()}")
    print(f"Snake starts at: {list(game.snake)}")
    
    # Move right and eat food at (0, 1)
    score = game.move("R")
    print(f"\nMove R: Score = {score}")
    print(f"Remaining foods: {game.get_visible_foods()}")
    print(f"Snake: {list(game.snake)}")
    
    # Move down and eat food at (1, 1)
    score = game.move("D")
    print(f"\nMove D: Score = {score}")
    print(f"Remaining foods: {game.get_visible_foods()}")
    print(f"Snake: {list(game.snake)}")
```

**Key Changes:**
1. Store food as `Set[Tuple]` instead of list with index
2. Check `new_head in self.food_set` instead of comparing with specific food
3. Remove eaten food from set

**Time Complexity:** Still O(1) per move
**Space Complexity:** O(F) for food set where F = number of foods

---

### Follow-up 3: Growth Every K Moves

**Problem Statement:**
> "Snake grows by 1 every K moves (e.g., every 5 moves) instead of eating food. Food provides bonus points but doesn't cause growth."

**Example:**
```text
Move 1-4: Snake length = 1
Move 5: Snake grows to length = 2
Move 10: Snake grows to length = 3
Move 15: Snake grows to length = 4
...
```

**Solution:**

```python
class SnakeGameTimedGrowth:
    """
    Snake game where growth happens every K moves.
    Food gives bonus points but doesn't affect growth.
    """
    
    def __init__(self, width: int, height: int, food: List[List[int]], k: int):
        self.width = width
        self.height = height
        self.food = food
        self.food_index = 0
        self.score = 0
        self.k = k  # Growth interval
        self.move_count = 0  # Track total moves
        
        self.snake = deque([(0, 0)])
        self.snake_set = {(0, 0)}
        
        self.directions = {
            'U': (-1, 0),
            'D': (1, 0),
            'L': (0, -1),
            'R': (0, 1)
        }
    
    def move(self, direction: str) -> int:
        """
        Move snake. Grows every K moves instead of when eating food.
        
        Time: O(1)
        """
        self.move_count += 1
        
        # 1. Calculate new head
        d_row, d_col = self.directions[direction]
        head_row, head_col = self.snake[-1]
        new_head_row = head_row + d_row
        new_head_col = head_col + d_col
        new_head = (new_head_row, new_head_col)
        
        # 2. Boundary check
        if (new_head_row < 0 or new_head_row >= self.height or
            new_head_col < 0 or new_head_col >= self.width):
            return -1
        
        # 3. Check if food is eaten (gives points, not growth!)
        if (self.food_index < len(self.food) and
            new_head_row == self.food[self.food_index][0] and
            new_head_col == self.food[self.food_index][1]):
            self.score += 10  # Bonus points!
            self.food_index += 1
        
        # 4. Determine if growth happens (every K moves)
        should_grow = (self.move_count % self.k == 0)
        
        if not should_grow:
            # Not growing: remove tail
            tail = self.snake.popleft()
            self.snake_set.remove(tail)
        # If growing: keep tail
        
        # 5. Add new head
        self.snake.append(new_head)
        
        # 6. Check collision
        if new_head in self.snake_set:
            return -1
        
        self.snake_set.add(new_head)
        
        return self.score


# Test
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("FOLLOW-UP 3: TIMED GROWTH (Every K Moves)")
    print("=" * 60)
    
    game = SnakeGameTimedGrowth(5, 5, [[1, 1]], k=3)
    
    moves = ["R", "R", "D", "D", "L"]
    
    for i, move in enumerate(moves, 1):
        score = game.move(move)
        length = len(game.snake)
        print(f"Move {i} ({move}): Score = {score}, Length = {length}")
        
        if i % game.k == 0:
            print(f"  → Growth at move {i}!")
```

**Output:**
```
Move 1 (R): Score = 0, Length = 1
Move 2 (R): Score = 0, Length = 1
Move 3 (D): Score = 0, Length = 2
  → Growth at move 3!
Move 4 (D): Score = 0, Length = 2
Move 5 (L): Score = 0, Length = 2
```

**Time Complexity:** O(1) per move
**Space Complexity:** O(N) where N = snake length

---

## 🧪 Test Cases

```python
def test_snake_game():
    """Comprehensive test suite for Snake Game."""
    
    # Test 1: Basic Movement
    game = SnakeGame(3, 2, [[1, 2], [0, 1]])
    assert game.move("R") == 0  # Move right
    assert game.move("D") == 0  # Move down
    assert game.move("R") == 1  # Eat food at (1,2)
    assert game.move("U") == 1  # Move up
    assert game.move("L") == 2  # Eat food at (0,1)
    assert game.move("U") == -1  # Out of bounds
    print("✓ Test 1: Basic Movement")
    
    # Test 2: Self-Collision
    game2 = SnakeGame(3, 3, [[2, 0]])
    game2.move("R")  # (0,1)
    game2.move("D")  # (1,1)
    game2.move("L")  # (1,0)
    game2.move("D")  # (2,0) - eat food, length=2
    game2.move("R")  # (2,1), body at (2,0)
    game2.move("U")  # (1,1), body at (2,1)
    assert game2.move("L") == -1  # (1,0) - hits body!
    print("✓ Test 2: Self-Collision")
    
    # Test 3: No Food
    game3 = SnakeGame(3, 3, [])
    assert game3.move("R") == 0
    assert game3.move("R") == 0
    assert game3.move("R") == -1  # Out of bounds
    print("✓ Test 3: No Food")
    
    # Test 4: Immediate Boundary
    game4 = SnakeGame(1, 1, [])
    assert game4.move("R") == -1  # Immediate boundary
    print("✓ Test 4: Immediate Boundary")
    
    # Test 5: Long Snake
    game5 = SnakeGame(10, 10, [[0,1], [0,2], [0,3], [0,4]])
    assert game5.move("R") == 1  # Length 2
    assert game5.move("R") == 2  # Length 3
    assert game5.move("R") == 3  # Length 4
    assert game5.move("R") == 4  # Length 5
    assert len(game5.snake) == 5
    print("✓ Test 5: Long Snake")
    
    # Test 6: U-Turn (should not hit itself)
    game6 = SnakeGame(3, 3, [[1,0]])
    game6.move("D")  # (1,0) - eat food, length=2
    game6.move("R")  # (1,1)
    game6.move("U")  # (0,1)
    assert game6.move("L") == 1  # (0,0) - OK, tail moved
    print("✓ Test 6: U-Turn")
    
    # Test 7: Eating Multiple Foods Quickly
    game7 = SnakeGame(2, 2, [[0,1], [1,1]])
    assert game7.move("R") == 1  # Eat first
    assert game7.move("D") == 2  # Eat second immediately
    assert len(game7.snake) == 3  # Length should be 3
    print("✓ Test 7: Multiple Foods")
    
    print("\nAll test cases passed! ✓")


if __name__ == "__main__":
    test_snake_game()
```

---

## 🎯 Key Takeaways

1. **Deque + HashSet Pattern:** Essential for O(1) operations on both ends + membership check
2. **Careful Timing:** Remove tail BEFORE collision check (or check AFTER adding head)
3. **Growth Logic:** Conditionally remove tail only when NOT eating food
4. **Coordinate System:** Be consistent with (row, col) vs (x, y)
5. **Edge Cases:** Boundary, self-collision, no food, single cell board

---

## 📚 Related Problems

- **LeetCode 353:** Design Snake Game (exact problem)
- **LeetCode 362:** Design Hit Counter (similar Deque pattern)
- **LeetCode 346:** Moving Average from Data Stream (Deque fundamentals)
- **LeetCode 641:** Design Circular Deque (Deque implementation)

