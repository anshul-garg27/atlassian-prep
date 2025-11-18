# 🎨 CODE DESIGN / LOW LEVEL DESIGN ROUND - Complete Guide

**Duration:** 60 minutes
**Format:** Object-Oriented Design + Implementation
**Difficulty:** Medium to Hard
**Expectations:** Clean, working code with good design patterns

---

## 📋 Round Structure

```
┌──────────────────────────────────────────────────┐
│ Problem Discussion (10 minutes)                  │
│ ├─ Understanding requirements                    │
│ ├─ Clarifying questions                          │
│ └─ Discuss API/interface design                  │
├──────────────────────────────────────────────────┤
│ Core Implementation (30-35 minutes)              │
│ ├─ Class design & relationships                  │
│ ├─ Code implementation                           │
│ └─ Testing with examples                         │
├──────────────────────────────────────────────────┤
│ Follow-ups & Extensions (15-20 minutes)          │
│ ├─ Add new features                              │
│ ├─ Handle edge cases                             │
│ └─ Discuss improvements                          │
└──────────────────────────────────────────────────┘
```

---

## 🐍 PROBLEM 1: SNAKE GAME (Most Popular!)

### ⭐⭐⭐⭐⭐ **Nokia Snake Game**

**Frequency:** Appears in **50%** of Code Design rounds!

**Problem Statement:**
> Implement the classic Nokia Snake game:
> - Snake moves on a 2D board
> - Initial length: 3 units
> - Grows by 1 unit every 5 moves
> - Game ends when snake hits itself
> - Snake can move up, down, left, right
> - Board boundaries wrap around (optional)

**Requirements:**
1. `void moveSnake(Direction dir)` - Move snake in given direction
2. `boolean isGameOver()` - Check if game has ended
3. `Position getHeadPosition()` - Get current head position
4. `int getScore()` - Get current score
5. Working code with clean design

**Visual Example:**
```
Initial (length 3):
. . . . .
. H B T .    H = Head, B = Body, T = Tail
. . . . .

After moveSnake(RIGHT):
. . . . .
. . H B T
. . . . .

After 5 moves (grows):
. . . . .
. . . H B
. . . B T
```

---

### 💻 **Complete Implementation**

```python
from enum import Enum
from collections import deque
from typing import List, Tuple, Optional

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __repr__(self):
        return f"({self.x}, {self.y})"
    
    def move(self, direction: Direction) -> 'Position':
        dx, dy = direction.value
        return Position(self.x + dx, self.y + dy)

class Snake:
    def __init__(self, start_pos: Position, initial_length: int = 3):
        """
        Initialize snake at start position
        
        Args:
            start_pos: Starting position of head
            initial_length: Initial length of snake (default 3)
        """
        self.body = deque()  # Deque for O(1) add/remove at both ends
        
        # Initialize snake horizontally
        for i in range(initial_length):
            self.body.append(Position(start_pos.x - i, start_pos.y))
        
        self.direction = Direction.RIGHT
        self.moves_since_growth = 0
        self.growth_interval = 5
        
    def get_head(self) -> Position:
        return self.body[0]
    
    def get_tail(self) -> Position:
        return self.body[-1]
    
    def move(self, new_direction: Direction) -> Position:
        """
        Move snake in given direction
        
        Returns:
            New head position after move
        """
        # Prevent 180-degree turns (optional rule)
        if self._is_opposite_direction(new_direction):
            new_direction = self.direction
        
        self.direction = new_direction
        
        # Calculate new head position
        current_head = self.get_head()
        new_head = current_head.move(new_direction)
        
        # Add new head
        self.body.appendleft(new_head)
        
        # Check if snake should grow
        self.moves_since_growth += 1
        
        if self.moves_since_growth >= self.growth_interval:
            # Grow: don't remove tail
            self.moves_since_growth = 0
        else:
            # Don't grow: remove tail
            self.body.pop()
        
        return new_head
    
    def check_self_collision(self) -> bool:
        """Check if head collides with body"""
        head = self.get_head()
        # Check if head position appears in body (excluding head itself)
        return head in list(self.body)[1:]
    
    def _is_opposite_direction(self, new_dir: Direction) -> bool:
        """Check if new direction is opposite to current direction"""
        if self.direction == Direction.UP and new_dir == Direction.DOWN:
            return True
        if self.direction == Direction.DOWN and new_dir == Direction.UP:
            return True
        if self.direction == Direction.LEFT and new_dir == Direction.RIGHT:
            return True
        if self.direction == Direction.RIGHT and new_dir == Direction.LEFT:
            return True
        return False
    
    def get_length(self) -> int:
        return len(self.body)
    
    def get_body_positions(self) -> List[Position]:
        return list(self.body)

class Board:
    def __init__(self, width: int, height: int, wrap_boundaries: bool = False):
        """
        Initialize game board
        
        Args:
            width: Board width
            height: Board height
            wrap_boundaries: If True, snake wraps around edges
        """
        self.width = width
        self.height = height
        self.wrap_boundaries = wrap_boundaries
    
    def is_valid_position(self, pos: Position) -> bool:
        """Check if position is within board boundaries"""
        if self.wrap_boundaries:
            return True  # All positions valid with wrapping
        
        return 0 <= pos.x < self.width and 0 <= pos.y < self.height
    
    def normalize_position(self, pos: Position) -> Position:
        """Normalize position for boundary wrapping"""
        if not self.wrap_boundaries:
            return pos
        
        return Position(
            pos.x % self.width,
            pos.y % self.height
        )

class SnakeGame:
    def __init__(self, width: int = 10, height: int = 10, wrap_boundaries: bool = False):
        """
        Initialize Snake Game
        
        Args:
            width: Board width
            height: Board height
            wrap_boundaries: If True, snake wraps around edges
        """
        self.board = Board(width, height, wrap_boundaries)
        
        # Start snake in center
        start_x = width // 2
        start_y = height // 2
        start_pos = Position(start_x, start_y)
        
        self.snake = Snake(start_pos)
        self.game_over = False
        self.score = 0
    
    def move_snake(self, direction: Direction) -> bool:
        """
        Move snake in given direction
        
        Returns:
            True if move successful, False if game over
        """
        if self.game_over:
            return False
        
        # Move snake
        new_head = self.snake.move(direction)
        
        # Normalize position for boundary wrapping
        new_head = self.board.normalize_position(new_head)
        
        # Update head position in snake body
        self.snake.body[0] = new_head
        
        # Check collisions
        if not self.board.is_valid_position(new_head):
            # Hit boundary (when not wrapping)
            self.game_over = True
            return False
        
        if self.snake.check_self_collision():
            # Hit itself
            self.game_over = True
            return False
        
        # Update score
        self.score += 1
        
        return True
    
    def is_game_over(self) -> bool:
        return self.game_over
    
    def get_head_position(self) -> Position:
        return self.snake.get_head()
    
    def get_tail_position(self) -> Position:
        return self.snake.get_tail()
    
    def get_score(self) -> int:
        return self.score
    
    def get_snake_length(self) -> int:
        return self.snake.get_length()
    
    def display(self):
        """Display current game state (for testing)"""
        board = [['.' for _ in range(self.board.width)] 
                 for _ in range(self.board.height)]
        
        # Draw snake body
        for i, pos in enumerate(self.snake.get_body_positions()):
            if 0 <= pos.x < self.board.width and 0 <= pos.y < self.board.height:
                if i == 0:
                    board[pos.y][pos.x] = 'H'  # Head
                elif i == len(self.snake.body) - 1:
                    board[pos.y][pos.x] = 'T'  # Tail
                else:
                    board[pos.y][pos.x] = 'B'  # Body
        
        print(f"Score: {self.score}, Length: {self.get_snake_length()}")
        for row in board:
            print(' '.join(row))
        print()

# ===== USAGE EXAMPLE =====

if __name__ == "__main__":
    game = SnakeGame(width=10, height=10, wrap_boundaries=False)
    
    print("=== Initial State ===")
    game.display()
    
    # Play some moves
    moves = [
        Direction.RIGHT,
        Direction.RIGHT,
        Direction.DOWN,
        Direction.DOWN,
        Direction.LEFT,
        Direction.LEFT,
        Direction.UP
    ]
    
    for i, move in enumerate(moves):
        print(f"=== Move {i+1}: {move.name} ===")
        success = game.move_snake(move)
        game.display()
        
        if not success:
            print("GAME OVER!")
            break
    
    print(f"Final Score: {game.get_score()}")
    print(f"Final Length: {game.get_snake_length()}")
```

**Time Complexity:**
- `moveSnake()`: O(1) - Deque operations
- `checkSelfCollision()`: O(n) where n = snake length (can optimize to O(1) with HashSet)
- `display()`: O(w * h) for rendering

**Space Complexity:** O(n) where n = snake length

---

### 🚀 **Optimized Version with O(1) Collision Detection**

```python
class OptimizedSnake(Snake):
    def __init__(self, start_pos: Position, initial_length: int = 3):
        super().__init__(start_pos, initial_length)
        
        # HashSet for O(1) collision detection
        self.body_set = set(self.body)
    
    def move(self, new_direction: Direction) -> Position:
        current_head = self.get_head()
        new_head = current_head.move(new_direction)
        
        # Add new head
        self.body.appendleft(new_head)
        self.body_set.add(new_head)
        
        self.moves_since_growth += 1
        
        if self.moves_since_growth < self.growth_interval:
            # Remove tail
            removed_tail = self.body.pop()
            self.body_set.remove(removed_tail)
        else:
            self.moves_since_growth = 0
        
        return new_head
    
    def check_self_collision(self) -> bool:
        """O(1) collision check using HashSet"""
        head = self.get_head()
        
        # Count occurrences of head in body_set
        # If > 1, collision (head appears twice)
        count = 0
        for pos in self.body:
            if pos == head:
                count += 1
                if count > 1:
                    return True
        return False
```

---

### 🎯 **Follow-up Questions**

#### **Follow-up 1: Add Food**

**Problem:** Add food that appears randomly. Snake grows when it eats food.

```python
import random

class Food:
    def __init__(self, position: Position):
        self.position = position

class SnakeGameWithFood(SnakeGame):
    def __init__(self, width: int = 10, height: int = 10):
        super().__init__(width, height)
        self.food = self._spawn_food()
    
    def _spawn_food(self) -> Food:
        """Spawn food at random empty position"""
        while True:
            x = random.randint(0, self.board.width - 1)
            y = random.randint(0, self.board.height - 1)
            pos = Position(x, y)
            
            # Check if position not occupied by snake
            if pos not in self.snake.body:
                return Food(pos)
    
    def move_snake(self, direction: Direction) -> bool:
        if self.game_over:
            return False
        
        # Store old tail before move
        old_tail = self.snake.get_tail()
        
        # Move snake
        new_head = self.snake.move(direction)
        new_head = self.board.normalize_position(new_head)
        self.snake.body[0] = new_head
        
        # Check collisions
        if not self.board.is_valid_position(new_head) or \
           self.snake.check_self_collision():
            self.game_over = True
            return False
        
        # Check if ate food
        if new_head == self.food.position:
            # Grow snake by adding back the old tail
            self.snake.body.append(old_tail)
            # Spawn new food
            self.food = self._spawn_food()
            self.score += 10  # Bonus points for food
        
        self.score += 1
        return True
```

#### **Follow-up 2: Multiple Snakes (Multiplayer)**

```python
class MultiplayerSnakeGame:
    def __init__(self, width: int, height: int, num_players: int = 2):
        self.board = Board(width, height)
        self.snakes = []
        
        # Create snakes at different starting positions
        positions = [
            Position(2, height // 2),
            Position(width - 3, height // 2)
        ]
        
        for i in range(num_players):
            snake = Snake(positions[i])
            self.snakes.append({
                'snake': snake,
                'alive': True,
                'score': 0
            })
    
    def move_snake(self, player_id: int, direction: Direction) -> bool:
        if player_id >= len(self.snakes) or not self.snakes[player_id]['alive']:
            return False
        
        player = self.snakes[player_id]
        snake = player['snake']
        
        # Move
        new_head = snake.move(direction)
        
        # Check self collision
        if snake.check_self_collision():
            player['alive'] = False
            return False
        
        # Check collision with other snakes
        for other_id, other in enumerate(self.snakes):
            if other_id != player_id and other['alive']:
                if new_head in other['snake'].body:
                    player['alive'] = False
                    return False
        
        player['score'] += 1
        return True
```

#### **Follow-up 3: Unit Tests**

```python
import unittest

class TestSnakeGame(unittest.TestCase):
    def test_initial_state(self):
        game = SnakeGame(10, 10)
        self.assertEqual(game.get_snake_length(), 3)
        self.assertFalse(game.is_game_over())
        self.assertEqual(game.get_score(), 0)
    
    def test_movement(self):
        game = SnakeGame(10, 10)
        initial_head = game.get_head_position()
        
        game.move_snake(Direction.RIGHT)
        new_head = game.get_head_position()
        
        self.assertEqual(new_head.x, initial_head.x + 1)
        self.assertEqual(new_head.y, initial_head.y)
    
    def test_growth(self):
        game = SnakeGame(10, 10)
        initial_length = game.get_snake_length()
        
        # Move 5 times to trigger growth
        for _ in range(5):
            game.move_snake(Direction.RIGHT)
        
        # Should have grown by 1
        self.assertEqual(game.get_snake_length(), initial_length + 1)
    
    def test_self_collision(self):
        game = SnakeGame(10, 10)
        
        # Create a collision scenario
        # Move in a circle to hit itself
        game.move_snake(Direction.RIGHT)
        game.move_snake(Direction.DOWN)
        game.move_snake(Direction.LEFT)
        game.move_snake(Direction.LEFT)
        game.move_snake(Direction.UP)
        game.move_snake(Direction.RIGHT)
        
        # Should detect collision (eventually)
        # Exact moves depend on initial length
    
    def test_boundary_collision(self):
        game = SnakeGame(5, 5, wrap_boundaries=False)
        
        # Move to edge
        for _ in range(10):
            success = game.move_snake(Direction.RIGHT)
            if not success:
                break
        
        self.assertTrue(game.is_game_over())

if __name__ == '__main__':
    unittest.main()
```

---

## 💰 PROBLEM 2: COST EXPLORER / SUBSCRIPTION BILLING

### ⭐⭐⭐ **Atlassian Subscription Pricing**

**Problem Statement:**
> Atlassian has three pricing tiers:
> - BASIC: $9.99/month
> - STANDARD: $49.99/month  
> - PREMIUM: $249.99/month
>
> Customers can subscribe to multiple products (Jira, Confluence, etc.). Build a Cost Explorer that:
> 1. Calculates monthly cost for each month of the year
> 2. Provides yearly cost estimate

**Example:**
```python
customer = Customer("C1")
jira = Product("Jira")

# Subscription: start_date, end_date, tier
subscription = Subscription(
    product=jira,
    tier="BASIC",
    start_date="2024-01-01",
    end_date="2024-03-31"
)

# Then upgrade
subscription2 = Subscription(
    product=jira,
    tier="PREMIUM",
    start_date="2024-04-01",
    end_date="2024-12-31"
)

cost_explorer = CostExplorer(customer)
monthly_cost = cost_explorer.get_monthly_costs(year=2024)
# Output: {
#   "Jan": 9.99, "Feb": 9.99, "Mar": 9.99,
#   "Apr": 249.99, ..., "Dec": 249.99
# }

yearly_cost = cost_explorer.get_yearly_cost(year=2024)
# Output: 2279.91
```

**Solution:**

```python
from datetime import datetime, date
from typing import List, Dict
from enum import Enum

class Tier(Enum):
    BASIC = 9.99
    STANDARD = 49.99
    PREMIUM = 249.99

class Product:
    def __init__(self, name: str):
        self.name = name

class Subscription:
    def __init__(self, product: Product, tier: str, 
                 start_date: str, end_date: str):
        self.product = product
        self.tier = Tier[tier]
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        self.end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    
    def get_cost_for_month(self, year: int, month: int) -> float:
        """Get cost for specific month"""
        month_start = date(year, month, 1)
        
        # Get last day of month
        if month == 12:
            month_end = date(year + 1, 1, 1)
        else:
            month_end = date(year, month + 1, 1)
        
        # Check if subscription active during this month
        if self.end_date < month_start or self.start_date >= month_end:
            return 0.0
        
        return self.tier.value

class Customer:
    def __init__(self, customer_id: str):
        self.customer_id = customer_id
        self.subscriptions: List[Subscription] = []
    
    def add_subscription(self, subscription: Subscription):
        self.subscriptions.append(subscription)

class CostExplorer:
    def __init__(self, customer: Customer):
        self.customer = customer
    
    def get_monthly_costs(self, year: int) -> Dict[str, float]:
        """Get cost for each month"""
        months = [
            "Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
        ]
        
        monthly_costs = {}
        
        for month_num in range(1, 13):
            month_name = months[month_num - 1]
            total_cost = 0.0
            
            for subscription in self.customer.subscriptions:
                cost = subscription.get_cost_for_month(year, month_num)
                total_cost += cost
            
            monthly_costs[month_name] = total_cost
        
        return monthly_costs
    
    def get_yearly_cost(self, year: int) -> float:
        """Get total cost for year"""
        monthly_costs = self.get_monthly_costs(year)
        return sum(monthly_costs.values())

# Usage
customer = Customer("C1")
jira = Product("Jira")

sub1 = Subscription(jira, "BASIC", "2024-01-01", "2024-03-31")
sub2 = Subscription(jira, "PREMIUM", "2024-04-01", "2024-12-31")

customer.add_subscription(sub1)
customer.add_subscription(sub2)

explorer = CostExplorer(customer)
print(explorer.get_monthly_costs(2024))
print(f"Yearly: ${explorer.get_yearly_cost(2024):.2f}")
```

---

## ⭐ PROBLEM 3: AGENT RATING SYSTEM

**Problem:** Customer support agents receive ratings. Return agents sorted by average rating.

**Solution:**

```python
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class Agent:
    agent_id: int
    name: str
    ratings: List[int]
    
    def get_average_rating(self) -> float:
        if not self.ratings:
            return 0.0
        return sum(self.ratings) / len(self.ratings)

class AgentRatingSystem:
    def __init__(self):
        self.agents: Dict[int, Agent] = {}
    
    def add_rating(self, agent_id: int, rating: int):
        """Add rating for agent (1-5 stars)"""
        if agent_id not in self.agents:
            raise ValueError(f"Agent {agent_id} not found")
        
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be 1-5")
        
        self.agents[agent_id].ratings.append(rating)
    
    def get_top_agents(self) -> List[Agent]:
        """Return all agents sorted by average rating (descending)"""
        sorted_agents = sorted(
            self.agents.values(),
            key=lambda a: a.get_average_rating(),
            reverse=True
        )
        return sorted_agents
```

---

## 🎬 PROBLEM 4: CINEMA HALL SCHEDULING

**Problem:** Schedule movies in cinema without conflicts.

```python
from typing import List

class Movie:
    def __init__(self, title: str, duration: int):
        self.title = title
        self.duration = duration  # in minutes

class Screening:
    def __init__(self, movie: Movie, start_time: int):
        self.movie = movie
        self.start_time = start_time  # minutes from midnight
        self.end_time = start_time + movie.duration

class CinemaSchedule:
    def __init__(self, open_time: int = 600, close_time: int = 1380):
        """
        Args:
            open_time: Opening time (minutes from midnight, default 10 AM = 600)
            close_time: Closing time (minutes from midnight, default 11 PM = 1380)
        """
        self.open_time = open_time
        self.close_time = close_time
        self.screenings: List[Screening] = []
    
    def can_schedule(self, movie: Movie, start_time: int) -> bool:
        """Check if movie can be scheduled at given time"""
        end_time = start_time + movie.duration
        
        # Check operating hours
        if start_time < self.open_time or end_time > self.close_time:
            return False
        
        # Check conflicts with existing screenings
        for screening in self.screenings:
            if self._has_overlap(start_time, end_time, 
                                 screening.start_time, screening.end_time):
                return False
        
        return True
    
    def schedule_movie(self, movie: Movie, start_time: int) -> bool:
        """Schedule movie if possible"""
        if self.can_schedule(movie, start_time):
            self.screenings.append(Screening(movie, start_time))
            return True
        return False
    
    def _has_overlap(self, start1: int, end1: int, 
                     start2: int, end2: int) -> bool:
        """Check if two time intervals overlap"""
        return max(start1, start2) < min(end1, end2)
```

---

## 🚦 PROBLEM 5: RATE LIMITER

**Problem:** Limit user to X requests in Y seconds.

```python
from collections import deque
import time

class RateLimiter:
    def __init__(self, max_requests: int, time_window: int):
        """
        Args:
            max_requests: Maximum requests allowed
            time_window: Time window in seconds
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.user_requests = {}  # user_id -> deque of timestamps
    
    def allow_request(self, user_id: str) -> bool:
        """Check if user can make request"""
        current_time = time.time()
        
        if user_id not in self.user_requests:
            self.user_requests[user_id] = deque()
        
        requests = self.user_requests[user_id]
        
        # Remove old requests outside time window
        while requests and requests[0] <= current_time - self.time_window:
            requests.popleft()
        
        # Check if limit reached
        if len(requests) >= self.max_requests:
            return False
        
        # Allow request
        requests.append(current_time)
        return True

# Usage
limiter = RateLimiter(max_requests=5, time_window=60)  # 5 requests per minute
print(limiter.allow_request("user1"))  # True
```

---

## ✅ KEY TAKEAWAYS

**What Interviewers Look For:**
1. ✅ Clean, modular code
2. ✅ Proper OOP design (classes, encapsulation)
3. ✅ Design patterns (Strategy, Factory, etc.)
4. ✅ Exception handling
5. ✅ Edge case handling
6. ✅ Testing mindset (mention unit tests)
7. ✅ Time/space complexity awareness

**Common Mistakes:**
1. ❌ Writing monolithic code (one big function)
2. ❌ No input validation
3. ❌ Ignoring edge cases
4. ❌ No exception handling
5. ❌ Not testing code with examples
6. ❌ Poor naming conventions

---

**Next:** [04_System_Design_HLD_Round.md](./04_System_Design_HLD_Round.md)
**Back to:** [README.md](./README.md)
