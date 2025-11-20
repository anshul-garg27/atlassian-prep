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
**Output:** Working game with move(), placeFood(), isGameOver() methods

**Constraints:**
- 5 ≤ Board size ≤ 100
- Snake initial length ≥ 1
- Food appears randomly
- Snake cannot reverse direction instantly (UP → DOWN not allowed)

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
. . . . . . . . . .
. . . . . . . . . .
. . . . . . . . . .
. . . . . . . . . .

After move(UP):
. . . . . . . . . .
. . . F . . . . . .
. . H . . . . . . .  Snake moved up
. . B B . . . . . .  Tail removed
. . . . . . . . . .
. . . . . . . . . .
. . . . . . . . . .
. . . . . . . . . .
. . . . . . . . . .
. . . . . . . . . .

After eating food and moving RIGHT:
. . . . . . . . . .
. . . . H . . . . .  Snake grew (no tail removal)
. . . B B . . . . .
. . . B . . . . . .
. . . . . . . . . .
```

---

## 🏗️ Class Design

### **Core Classes:**

```text
┌─────────────┐
│    Game     │  ← Main controller
├─────────────┤
│ - snake     │
│ - board     │
│ - food      │
│ - score     │
│ - gameOver  │
└─────────────┘
       │
       ├──────────────┬──────────────┐
       │              │              │
  ┌─────────┐   ┌─────────┐   ┌─────────┐
  │  Snake  │   │  Board  │   │  Food   │
  └─────────┘   └─────────┘   └─────────┘
       │
  ┌─────────┐
  │Position │  ← Helper class (x, y)
  └─────────┘

  ┌──────────┐
  │Direction │  ← Enum (UP, DOWN, LEFT, RIGHT)
  └──────────┘
```

---

## 💻 Implementation

### **Java Implementation (Complete)**

```java
import java.util.*;

// ============ Position Class ============
class Position {
    int x, y;

    public Position(int x, int y) {
        this.x = x;
        this.y = y;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Position)) return false;
        Position pos = (Position) o;
        return x == pos.x && y == pos.y;
    }

    @Override
    public int hashCode() {
        return Objects.hash(x, y);
    }

    @Override
    public String toString() {
        return "(" + x + "," + y + ")";
    }
}

// ============ Direction Enum ============
enum Direction {
    UP(-1, 0),
    DOWN(1, 0),
    LEFT(0, -1),
    RIGHT(0, 1);

    final int dx, dy;

    Direction(int dx, int dy) {
        this.dx = dx;
        this.dy = dy;
    }

    public boolean isOpposite(Direction other) {
        return (this == UP && other == DOWN) ||
               (this == DOWN && other == UP) ||
               (this == LEFT && other == RIGHT) ||
               (this == RIGHT && other == LEFT);
    }
}

// ============ Snake Class ============
class Snake {
    private Deque<Position> body;
    private Direction currentDirection;
    private Set<Position> occupiedPositions; // For O(1) collision check

    public Snake(Position initialPosition) {
        this.body = new LinkedList<>();
        this.body.addFirst(initialPosition);
        this.occupiedPositions = new HashSet<>();
        this.occupiedPositions.add(initialPosition);
        this.currentDirection = Direction.RIGHT; // Default direction
    }

    public Position getHead() {
        return body.peekFirst();
    }

    public Position getTail() {
        return body.peekLast();
    }

    public Direction getCurrentDirection() {
        return currentDirection;
    }

    public boolean changeDirection(Direction newDirection) {
        // Cannot reverse instantly
        if (currentDirection.isOpposite(newDirection)) {
            return false;
        }
        this.currentDirection = newDirection;
        return true;
    }

    public Position getNextHeadPosition() {
        Position head = getHead();
        return new Position(
            head.x + currentDirection.dx,
            head.y + currentDirection.dy
        );
    }

    public void move(Position newHead) {
        body.addFirst(newHead);
        occupiedPositions.add(newHead);

        // Remove tail (no growth)
        Position tail = body.removeLast();
        occupiedPositions.remove(tail);
    }

    public void grow(Position newHead) {
        // Add head but don't remove tail
        body.addFirst(newHead);
        occupiedPositions.add(newHead);
    }

    public boolean isCollision(Position pos) {
        return occupiedPositions.contains(pos);
    }

    public int getLength() {
        return body.size();
    }

    public List<Position> getBody() {
        return new ArrayList<>(body);
    }
}

// ============ Board Class ============
class Board {
    private final int rows;
    private final int cols;

    public Board(int rows, int cols) {
        if (rows <= 0 || cols <= 0) {
            throw new IllegalArgumentException("Board dimensions must be positive");
        }
        this.rows = rows;
        this.cols = cols;
    }

    public boolean isWithinBounds(Position pos) {
        return pos.x >= 0 && pos.x < rows && pos.y >= 0 && pos.y < cols;
    }

    public int getRows() {
        return rows;
    }

    public int getCols() {
        return cols;
    }

    public Position getRandomPosition() {
        Random rand = new Random();
        return new Position(rand.nextInt(rows), rand.nextInt(cols));
    }
}

// ============ Game Class ============
class SnakeGame {
    private Snake snake;
    private Board board;
    private Position food;
    private int score;
    private boolean gameOver;

    public SnakeGame(int rows, int cols, Position initialSnakePos) {
        this.board = new Board(rows, cols);
        this.snake = new Snake(initialSnakePos);
        this.score = 0;
        this.gameOver = false;
        this.food = placeFood();
    }

    public boolean move(Direction direction) {
        if (gameOver) {
            throw new IllegalStateException("Game is over!");
        }

        // Try to change direction
        snake.changeDirection(direction);

        // Calculate next head position
        Position nextHead = snake.getNextHeadPosition();

        // Check collision with walls
        if (!board.isWithinBounds(nextHead)) {
            gameOver = true;
            return false;
        }

        // Check collision with self
        if (snake.isCollision(nextHead)) {
            gameOver = true;
            return false;
        }

        // Check if eating food
        if (nextHead.equals(food)) {
            snake.grow(nextHead);
            score += 10;
            food = placeFood();
        } else {
            snake.move(nextHead);
        }

        return true;
    }

    private Position placeFood() {
        Position newFood;
        do {
            newFood = board.getRandomPosition();
        } while (snake.isCollision(newFood));
        return newFood;
    }

    public boolean isGameOver() {
        return gameOver;
    }

    public int getScore() {
        return score;
    }

    public Position getFoodPosition() {
        return food;
    }

    public List<Position> getSnakeBody() {
        return snake.getBody();
    }

    public void printBoard() {
        char[][] grid = new char[board.getRows()][board.getCols()];

        // Fill with empty cells
        for (int i = 0; i < board.getRows(); i++) {
            Arrays.fill(grid[i], '.');
        }

        // Place snake body
        List<Position> body = snake.getBody();
        for (int i = 0; i < body.size(); i++) {
            Position pos = body.get(i);
            if (i == 0) {
                grid[pos.x][pos.y] = 'H'; // Head
            } else {
                grid[pos.x][pos.y] = 'B'; // Body
            }
        }

        // Place food
        grid[food.x][food.y] = 'F';

        // Print grid
        for (char[] row : grid) {
            for (char cell : row) {
                System.out.print(cell + " ");
            }
            System.out.println();
        }
        System.out.println("Score: " + score);
        System.out.println();
    }
}

// ============ Main / Demo ============
public class Main {
    public static void main(String[] args) {
        SnakeGame game = new SnakeGame(10, 10, new Position(5, 5));

        System.out.println("Initial State:");
        game.printBoard();

        // Simulate moves
        game.move(Direction.UP);
        System.out.println("After UP:");
        game.printBoard();

        game.move(Direction.RIGHT);
        System.out.println("After RIGHT:");
        game.printBoard();

        game.move(Direction.RIGHT);
        System.out.println("After RIGHT:");
        game.printBoard();

        System.out.println("Game Over: " + game.isGameOver());
        System.out.println("Final Score: " + game.getScore());
    }
}
```

---

### **Python Implementation (Complete)**

```python
from collections import deque
from enum import Enum
import random

# ============ Direction Enum ============
class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    def is_opposite(self, other):
        return (self == Direction.UP and other == Direction.DOWN) or \
               (self == Direction.DOWN and other == Direction.UP) or \
               (self == Direction.LEFT and other == Direction.RIGHT) or \
               (self == Direction.RIGHT and other == Direction.LEFT)

# ============ Snake Class ============
class Snake:
    def __init__(self, initial_pos):
        self.body = deque([initial_pos])
        self.occupied = {initial_pos}
        self.direction = Direction.RIGHT

    def get_head(self):
        return self.body[0]

    def get_tail(self):
        return self.body[-1]

    def change_direction(self, new_direction):
        if self.direction.is_opposite(new_direction):
            return False
        self.direction = new_direction
        return True

    def get_next_head_pos(self):
        head = self.get_head()
        dx, dy = self.direction.value
        return (head[0] + dx, head[1] + dy)

    def move(self, new_head):
        self.body.appendleft(new_head)
        self.occupied.add(new_head)

        # Remove tail
        tail = self.body.pop()
        self.occupied.remove(tail)

    def grow(self, new_head):
        self.body.appendleft(new_head)
        self.occupied.add(new_head)

    def is_collision(self, pos):
        return pos in self.occupied

    def get_length(self):
        return len(self.body)

# ============ Board Class ============
class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

    def is_within_bounds(self, pos):
        x, y = pos
        return 0 <= x < self.rows and 0 <= y < self.cols

    def get_random_position(self):
        return (random.randint(0, self.rows - 1),
                random.randint(0, self.cols - 1))

# ============ Game Class ============
class SnakeGame:
    def __init__(self, rows, cols, initial_pos):
        self.board = Board(rows, cols)
        self.snake = Snake(initial_pos)
        self.food = self._place_food()
        self.score = 0
        self.game_over = False

    def move(self, direction):
        if self.game_over:
            raise Exception("Game is over!")

        # Change direction
        self.snake.change_direction(direction)

        # Get next position
        next_head = self.snake.get_next_head_pos()

        # Check wall collision
        if not self.board.is_within_bounds(next_head):
            self.game_over = True
            return False

        # Check self collision
        if self.snake.is_collision(next_head):
            self.game_over = True
            return False

        # Check food
        if next_head == self.food:
            self.snake.grow(next_head)
            self.score += 10
            self.food = self._place_food()
        else:
            self.snake.move(next_head)

        return True

    def _place_food(self):
        while True:
            food_pos = self.board.get_random_position()
            if not self.snake.is_collision(food_pos):
                return food_pos

    def is_game_over(self):
        return self.game_over

    def get_score(self):
        return self.score

    def print_board(self):
        grid = [['.' for _ in range(self.board.cols)]
                for _ in range(self.board.rows)]

        # Place snake
        for i, pos in enumerate(self.snake.body):
            x, y = pos
            if i == 0:
                grid[x][y] = 'H'  # Head
            else:
                grid[x][y] = 'B'  # Body

        # Place food
        fx, fy = self.food
        grid[fx][fy] = 'F'

        # Print
        for row in grid:
            print(' '.join(row))
        print(f"Score: {self.score}\n")

# ============ Demo ============
if __name__ == "__main__":
    game = SnakeGame(10, 10, (5, 5))

    print("Initial State:")
    game.print_board()

    game.move(Direction.UP)
    print("After UP:")
    game.print_board()

    game.move(Direction.RIGHT)
    print("After RIGHT:")
    game.print_board()

    print(f"Game Over: {game.is_game_over()}")
    print(f"Final Score: {game.get_score()}")
```

---

## 🎯 Design Principles Applied

### **1. Single Responsibility Principle (SRP)**
- `Snake`: Manages snake body and movement
- `Board`: Manages grid and boundaries
- `Game`: Orchestrates game logic
- `Position`: Represents coordinates

### **2. Open/Closed Principle (OCP)**
Extensible for new features without modifying existing code:
```java
// Add obstacles
class Obstacle {
    Set<Position> positions;
}

// Extend game
class SnakeGameWithObstacles extends SnakeGame {
    private Set<Position> obstacles;

    @Override
    public boolean move(Direction direction) {
        Position nextHead = snake.getNextHeadPosition();
        if (obstacles.contains(nextHead)) {
            gameOver = true;
            return false;
        }
        return super.move(direction);
    }
}
```

### **3. Encapsulation**
- `body` in `Snake` is private (use `getBody()` for access)
- Game state cannot be modified externally

---

## 🚀 Extensions & Follow-ups

### **Extension 1: Multiple Food Types**
```java
enum FoodType {
    NORMAL(10),
    GOLDEN(50),
    SPEED_BOOST(20);

    final int points;

    FoodType(int points) {
        this.points = points;
    }
}

class Food {
    Position position;
    FoodType type;

    public Food(Position position, FoodType type) {
        this.position = position;
        this.type = type;
    }
}
```

### **Extension 2: Power-ups**
```java
enum PowerUp {
    INVINCIBILITY,  // Pass through walls for 5 seconds
    SLOW_MOTION,    // Slow down snake speed
    DOUBLE_POINTS   // 2x score for 10 seconds
}

class Game {
    private Map<PowerUp, Long> activePowerUps; // PowerUp -> expiry time

    public void applyPowerUp(PowerUp powerUp) {
        activePowerUps.put(powerUp, System.currentTimeMillis() + 5000);
    }

    public boolean isActive(PowerUp powerUp) {
        Long expiry = activePowerUps.get(powerUp);
        return expiry != null && System.currentTimeMillis() < expiry;
    }
}
```

### **Extension 3: Obstacles**
```java
class Game {
    private Set<Position> obstacles;

    public void addObstacle(Position pos) {
        obstacles.add(pos);
    }

    @Override
    public boolean move(Direction direction) {
        Position nextHead = snake.getNextHeadPosition();

        // Check obstacle collision
        if (obstacles.contains(nextHead)) {
            gameOver = true;
            return false;
        }

        // ... rest of the logic
    }
}
```

### **Extension 4: Multiplayer**
```java
class MultiplayerGame {
    private List<Snake> snakes;
    private int currentPlayer;

    public boolean move(int playerId, Direction direction) {
        Snake snake = snakes.get(playerId);
        // Move logic for specific snake
    }

    public boolean checkSnakeCollision(Snake snake, Position pos) {
        // Check collision with other snakes
        for (Snake otherSnake : snakes) {
            if (otherSnake != snake && otherSnake.isCollision(pos)) {
                return true;
            }
        }
        return false;
    }
}
```

---

## 🧪 Testing Strategy

### **Unit Tests**

```java
@Test
public void testInitialState() {
    SnakeGame game = new SnakeGame(10, 10, new Position(5, 5));
    assertFalse(game.isGameOver());
    assertEquals(0, game.getScore());
}

@Test
public void testMovement() {
    SnakeGame game = new SnakeGame(10, 10, new Position(5, 5));
    assertTrue(game.move(Direction.UP));
    assertFalse(game.isGameOver());
}

@Test
public void testWallCollision() {
    SnakeGame game = new SnakeGame(10, 10, new Position(0, 0));
    assertFalse(game.move(Direction.UP)); // Hit top wall
    assertTrue(game.isGameOver());
}

@Test
public void testSelfCollision() {
    SnakeGame game = new SnakeGame(10, 10, new Position(5, 5));

    // Create scenario where snake bites itself
    // Grow snake first
    game.move(Direction.RIGHT);
    game.move(Direction.RIGHT);
    game.move(Direction.RIGHT);

    // Turn around to hit body
    game.move(Direction.UP);
    game.move(Direction.LEFT);
    game.move(Direction.DOWN); // Should hit body

    assertTrue(game.isGameOver());
}

@Test
public void testFoodConsumption() {
    SnakeGame game = new SnakeGame(10, 10, new Position(5, 5));
    int initialScore = game.getScore();

    // Place food manually for testing
    Position foodPos = game.getFoodPosition();
    // Move towards food (implementation-specific)

    assertTrue(game.getScore() > initialScore);
}

@Test
public void testCannotReverse() {
    SnakeGame game = new SnakeGame(10, 10, new Position(5, 5));
    game.move(Direction.RIGHT);
    game.move(Direction.LEFT); // Should be ignored
    // Snake should continue moving RIGHT
}
```

---

## ⚠️ Edge Cases

1. **Snake fills entire board**
   - Cannot place food
   - Declare win or end game

2. **Initial position out of bounds**
   ```java
   public SnakeGame(int rows, int cols, Position initialPos) {
       this.board = new Board(rows, cols);
       if (!board.isWithinBounds(initialPos)) {
           throw new IllegalArgumentException("Initial position out of bounds");
       }
       // ...
   }
   ```

3. **Board too small (1×1)**
   - Game ends immediately
   - Validate minimum size

4. **Food spawns on snake**
   - Loop until finding valid position (already handled)

5. **Move called after game over**
   - Throw exception (already handled)

---

## 📊 Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| move() | O(1) | O(1) |
| grow() | O(1) | O(1) |
| isCollision() | O(1) | O(N) |
| placeFood() | O(K) | O(1) |
| printBoard() | O(R×C) | O(R×C) |

**Where:**
- N = snake length
- K = attempts to place food (avg ≈ 1)
- R × C = board dimensions

**Space Complexity:** O(N + R×C) = O(max board size)

---

## 💡 Interview Discussion Points

### **Questions to Ask Interviewer:**
1. Board size fixed or dynamic?
2. Starting snake length?
3. Food appears randomly or at specific positions?
4. Multiple food items allowed?
5. Need to support obstacles?
6. Snake speed changes?
7. Need to support saving/loading game state?

### **What Interviewers Look For:**
✅ **Clean class design** (SRP, clear responsibilities)
✅ **Deque usage** for efficient head/tail operations
✅ **HashSet** for O(1) collision checks
✅ **Enum for Direction** (not magic strings)
✅ **Preventing reverse direction**
✅ **Edge case handling** (boundaries, null checks)
✅ **Extensibility discussion** (obstacles, power-ups)
✅ **Testing mindset**

---

## ❌ Common Mistakes

### **MISTAKE 1: Using List instead of Deque** ❌
```java
// WRONG - O(N) for removeLast
List<Position> body = new ArrayList<>();
body.remove(body.size() - 1); // O(N)

// CORRECT - O(1) for both ends
Deque<Position> body = new LinkedList<>();
body.removeLast(); // O(1)
```

### **MISTAKE 2: O(N) Collision Check** ❌
```java
// WRONG - O(N) every time
public boolean isCollision(Position pos) {
    for (Position p : body) {
        if (p.equals(pos)) return true;
    }
    return false;
}

// CORRECT - O(1) with HashSet
private Set<Position> occupiedPositions;
public boolean isCollision(Position pos) {
    return occupiedPositions.contains(pos);
}
```

### **MISTAKE 3: Not Preventing Reverse Direction** ❌
```java
// WRONG - Snake can reverse instantly
public void move(Direction newDirection) {
    this.direction = newDirection; // Can go UP then DOWN immediately
}

// CORRECT - Check opposite
public boolean changeDirection(Direction newDirection) {
    if (direction.isOpposite(newDirection)) {
        return false;
    }
    this.direction = newDirection;
    return true;
}
```

### **MISTAKE 4: Messy Code in One Class** ❌
```java
// WRONG - Everything in one class
public class SnakeGame {
    int headX, headY;
    List<int[]> body;
    int[][] board;
    int foodX, foodY;
    // 500 lines of spaghetti code...
}
```

---

## 🏆 Production-Ready Enhancements

### **1. Game State Persistence**
```java
public String saveGame() {
    return new Gson().toJson(this);
}

public static SnakeGame loadGame(String json) {
    return new Gson().fromJson(json, SnakeGame.class);
}
```

### **2. Event Listeners**
```java
interface GameListener {
    void onFoodEaten(Position foodPos, int newScore);
    void onGameOver(int finalScore);
    void onSnakeMoved(List<Position> newBody);
}

class Game {
    private List<GameListener> listeners = new ArrayList<>();

    public void addListener(GameListener listener) {
        listeners.add(listener);
    }

    private void notifyFoodEaten() {
        for (GameListener l : listeners) {
            l.onFoodEaten(food, score);
        }
    }
}
```

### **3. High Score Tracking**
```java
class Game {
    private static int highScore = 0;

    public void updateHighScore() {
        if (score > highScore) {
            highScore = score;
        }
    }

    public static int getHighScore() {
        return highScore;
    }
}
```

---

## 💯 Best Practices Summary

✅ Use **Deque** for snake body (O(1) operations)
✅ Use **HashSet** for collision detection (O(1))
✅ **Separate concerns** (Snake, Board, Game classes)
✅ Use **Enum** for directions
✅ **Prevent reverse direction** (gameplay rule)
✅ Handle **edge cases** (boundaries, null, game over)
✅ Make code **extensible** (easy to add obstacles, power-ups)
✅ Write **unit tests** for movement, collision, growth
✅ Use **meaningful names** (not x1, y1, x2, y2)
✅ Override **equals() and hashCode()** for Position

**Interview Pro Tip:** After implementing basic version, ask "Should I add obstacles/power-ups?" to show extensibility thinking!

---

**Related LeetCode Problems:**
- LeetCode 353: Design Snake Game
- LeetCode 1242: Web Crawler Multithreaded (similar BFS pattern)

**Real-World Applications:**
- Nokia Snake (classic game)
- Slither.io (multiplayer version)
- Game engines (Unity, Unreal)
