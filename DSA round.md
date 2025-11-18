# 2. DSA/CODING ROUNDS

## 📊 Overview
- **Duration:** 45-60 minutes
- **Format:** 1-2 coding problems
- **Difficulty:** LeetCode Medium (mostly)
- **Focus:** Working solution, clean code, edge cases
- **Occurrences:** 65 rounds in dataset

---

## 🔥 MOST FREQUENTLY ASKED PROBLEMS

### ⭐⭐⭐ PROBLEM #1: Employee Hierarchy (LCA Variation)
**Frequency:** Asked in 15+ interviews  
**Difficulty:** Medium-Hard  
**Must Practice:** YES - This is THE most common problem

```python
"""
PROBLEM: Find Closest Common Department/Manager

Given: Company hierarchy as a graph/tree
       - Company → Departments → Sub-departments → Employees
       - Multiple levels of hierarchy

Task: Find the closest common department/manager for a list of employees

Example:
         Company
        /       \
    Engineering  Sales
    /     \         \
  Backend Frontend  US-Sales
  /   \      |        |
Alice Bob  Carol    David

Query 1: closestDepartment([Alice, Bob]) → Backend
Query 2: closestDepartment([Alice, Carol]) → Engineering  
Query 3: closestDepartment([Alice, David]) → Company
Query 4: closestDepartment([Alice, Bob, Carol]) → Engineering

Variations Asked:
1. Binary tree structure (classic LCA)
2. N-ary tree with departments
3. Graph with multiple parent references
4. Find distance between employees
5. Find all common ancestors
"""

# Solution Approach:
class Solution:
    def lowestCommonAncestor(self, root, employees):
        """
        Approach 1: DFS + Path finding
        1. Find path from root to each employee
        2. Compare paths to find divergence point
        """
        def findPath(node, target, path):
            if not node:
                return False
            
            path.append(node)
            
            if node == target:
                return True
            
            for child in node.children:
                if findPath(child, target, path):
                    return True
            
            path.pop()
            return False
        
        # Find paths for all employees
        paths = []
        for emp in employees:
            path = []
            findPath(root, emp, path)
            paths.append(path)
        
        # Find common prefix
        lca = root
        for i in range(min(len(p) for p in paths)):
            if all(paths[j][i] == paths[0][i] for j in range(len(paths))):
                lca = paths[0][i]
            else:
                break
        
        return lca

# Practice Problems:
# - LeetCode 236: Lowest Common Ancestor of Binary Tree
# - LeetCode 1676: LCA of Binary Tree IV (multiple nodes)
# - LeetCode 1650: LCA of Binary Tree III (with parent pointers)
```

**Interview Tips:**
- Start with clarifying questions about tree structure
- Ask about edge cases (employee not found, same employee, etc.)
- Discuss time/space complexity
- Code should handle N employees, not just 2
- Test with examples

---

### Problem #2: Snake Game Implementation

```python
"""
PROBLEM: Implement Snake Game Logic

Given: 2D board, snake can move up/down/left/right

Requirements:
1. Snake starts with size 3
2. Grows by 1 every 5 moves
3. Game ends when snake hits itself
4. Implement: moveSnake(), isGameOver()

interface SnakeGame {
    void moveSnake(Direction direction);
    boolean isGameOver();
}

Key Points:
- Track snake position (queue/deque)
- Check collision with self
- Handle growth every 5 moves
- Validate boundaries
"""

from collections import deque

class SnakeGame:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.snake = deque([(0, 0), (0, 1), (0, 2)])  # Initial size 3
        self.moves = 0
        self.game_over = False
    
    def moveSnake(self, direction):
        if self.game_over:
            return
        
        head = self.snake[-1]
        
        # Calculate new head position
        if direction == 'UP':
            new_head = (head[0] - 1, head[1])
        elif direction == 'DOWN':
            new_head = (head[0] + 1, head[1])
        elif direction == 'LEFT':
            new_head = (head[0], head[1] - 1)
        else:  # RIGHT
            new_head = (head[0], head[1] + 1)
        
        # Check collision with self
        if new_head in self.snake:
            self.game_over = True
            return
        
        # Check boundaries
        if (new_head[0] < 0 or new_head[0] >= self.height or 
            new_head[1] < 0 or new_head[1] >= self.width):
            self.game_over = True
            return
        
        # Add new head
        self.snake.append(new_head)
        self.moves += 1
        
        # Remove tail if not growing
        if self.moves % 5 != 0:
            self.snake.popleft()
    
    def isGameOver(self):
        return self.game_over
```

---

### Problem #3: Most Popular Content Tracker

```python
"""
PROBLEM: Track Most Popular Content

Interface:
    void increasePopularity(Integer contentId);
    Integer mostPopular();
    void decreasePopularity(Integer contentId);

Requirements:
- mostPopular() returns content with highest popularity
- If tie, return most recently increased contentId
- O(1) operations preferred

Example:
tracker.increasePopularity(7);    // popularity[7] = 1
tracker.increasePopularity(7);    // popularity[7] = 2
tracker.increasePopularity(8);    // popularity[8] = 1
tracker.mostPopular();            // returns 7
tracker.increasePopularity(8);    // popularity[8] = 2
tracker.increasePopularity(8);    // popularity[8] = 3
tracker.mostPopular();            // returns 8
"""

class MostPopularTracker:
    def __init__(self):
        self.popularity = {}  # contentId -> count
        self.count_to_contents = defaultdict(OrderedDict)  # count -> {contentId: None}
        self.max_count = 0
    
    def increasePopularity(self, contentId):
        old_count = self.popularity.get(contentId, 0)
        new_count = old_count + 1
        self.popularity[contentId] = new_count
        
        # Remove from old count
        if old_count > 0:
            del self.count_to_contents[old_count][contentId]
        
        # Add to new count (most recent at end)
        self.count_to_contents[new_count][contentId] = None
        self.max_count = max(self.max_count, new_count)
    
    def mostPopular(self):
        # Return most recent contentId with max_count
        while self.max_count > 0 and not self.count_to_contents[self.max_count]:
            self.max_count -= 1
        
        if self.max_count == 0:
            return None
        
        # Return last (most recent) contentId
        return next(reversed(self.count_to_contents[self.max_count]))
    
    def decreasePopularity(self, contentId):
        if contentId not in self.popularity:
            return
        
        old_count = self.popularity[contentId]
        new_count = old_count - 1
        
        del self.count_to_contents[old_count][contentId]
        
        if new_count > 0:
            self.popularity[contentId] = new_count
            self.count_to_contents[new_count][contentId] = None
        else:
            del self.popularity[contentId]
```

---

### Problem #4: LRU Cache

```python
"""
PROBLEM: Implement LRU Cache

Standard LeetCode 146 - Very commonly asked

Requirements:
- get(key): Return value if exists, else -1
- put(key, value): Insert or update, evict LRU if at capacity
- O(1) for both operations

Expected: Doubly linked list + HashMap
"""

class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}  # key -> Node
        self.head = Node(0, 0)  # dummy head
        self.tail = Node(0, 0)  # dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def get(self, key):
        if key not in self.cache:
            return -1
        
        node = self.cache[key]
        self._remove(node)
        self._add(node)
        return node.val
    
    def put(self, key, value):
        if key in self.cache:
            self._remove(self.cache[key])
        
        node = Node(key, value)
        self._add(node)
        self.cache[key] = node
        
        if len(self.cache) > self.capacity:
            # Remove LRU (after head)
            lru = self.head.next
            self._remove(lru)
            del self.cache[lru.key]
    
    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
    
    def _add(self, node):
        # Add before tail (most recently used)
        node.prev = self.tail.prev
        node.next = self.tail
        self.tail.prev.next = node
        self.tail.prev = node
```

---

### Problem #5: Customer Care Agent Rating System

```python
"""
PROBLEM: Agent Rating and Sorting

Requirements:
- Store agent ratings
- Display agents sorted by rating (asc or desc)
- Test with JUnit-style tests

Key Points:
- Clean OOP design
- Sorting functionality
- Unit testable code
"""

class Agent:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.ratings = []
    
    def add_rating(self, rating):
        self.ratings.append(rating)
    
    def get_average_rating(self):
        return sum(self.ratings) / len(self.ratings) if self.ratings else 0

class AgentRatingSystem:
    def __init__(self):
        self.agents = {}
    
    def add_agent(self, agent_id, name):
        self.agents[agent_id] = Agent(agent_id, name)
    
    def add_rating(self, agent_id, rating):
        if agent_id in self.agents:
            self.agents[agent_id].add_rating(rating)
    
    def get_sorted_agents(self, ascending=True):
        sorted_agents = sorted(
            self.agents.values(),
            key=lambda a: a.get_average_rating(),
            reverse=not ascending
        )
        return sorted_agents
```

---

## 📚 Other Common Problems

### Array/String:
- **Find word in dictionary** with all letters from target
- **Merge intervals**
- **Subarray with given sum**
- **Longest substring without repeating characters**

### Tree/Graph:
- **Binary tree traversals** (all orders)
- **Validate BST**
- **Graph connectivity** (DFS/BFS)
- **Shortest path in grid**

### Dynamic Programming:
- **Coin change**
- **Longest increasing subsequence**
- **Edit distance** (mentioned but less common)

---

# 3. DATA STRUCTURE ROUNDS

## 📊 Overview
- **Duration:** 60 minutes
- **Focus:** Custom data structure design + implementation
- **Difficulty:** Medium-Hard
- **Key Skills:** OOP, clean design, efficiency

---

## 🎯 Common Problems

### Problem #1: Employee Directory - Closest Parent Group

```python
"""
PROBLEM: Find Closest Parent Group

Given: Employee directory with groups and departments
       - Hierarchical structure
       - Groups contain departments
       - Departments contain employees

Task: Find closest parent group/department for target set of employees

Example Tree:
              Company
            /         \
        Engineering   Sales
        /     \          \
    Backend  Frontend   US-Sales
    /   \      |          |
 Alice  Bob  Carol     David

Query: closestGroup([Alice, Lisa]) → Engineering
Query: closestGroup([Alice, Bob]) → Backend

Note: Similar to Employee Hierarchy but expects specific data structure design
"""

class Employee:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.department = None

class Department:
    def __init__(self, name):
        self.name = name
        self.employees = []
        self.parent = None
        self.children = []

class Group:
    def __init__(self, name):
        self.name = name
        self.departments = []
        self.parent = None

class EmployeeDirectory:
    def __init__(self, root):
        self.root = root
    
    def findClosestGroup(self, employees):
        # Build path to root for each employee
        paths = []
        for emp in employees:
            path = self._getPathToRoot(emp)
            paths.append(path)
        
        # Find common ancestor
        lca = None
        for i in range(min(len(p) for p in paths)):
            if all(paths[j][i] == paths[0][i] for j in range(len(paths))):
                lca = paths[0][i]
            else:
                break
        
        return lca
    
    def _getPathToRoot(self, employee):
        path = []
        current = employee.department
        
        while current:
            path.append(current)
            current = current.parent
        
        return list(reversed(path))
```

---

### Problem #2: Cinema Hall Movie Scheduling

```python
"""
PROBLEM: Movie Schedule Validator

Given: Cinema hall schedule
       - Opens at 10 AM (600 mins from midnight)
       - Closes at 11 PM (1380 mins from midnight)
       - Single screen, one movie at a time

Task: Implement canSchedule(Movie movie, MovieSchedule schedule)
      Check if new movie can be added without conflicts

Data Structure:
{
  "movies": [
    {
      "id": "abc-123",
      "name": "Movie A",
      "startTime": 780,  // 1 PM in minutes from midnight
      "duration": 120    // 2 hours
    },
    {
      "id": "def-456",
      "name": "Movie B",
      "startTime": 1000, // 4:40 PM
      "duration": 150
    }
  ]
}
"""

class Movie:
    def __init__(self, id, name, start_time, duration):
        self.id = id
        self.name = name
        self.start_time = start_time  # mins from midnight
        self.duration = duration
    
    def end_time(self):
        return self.start_time + self.duration

class MovieSchedule:
    OPEN_TIME = 600   # 10 AM
    CLOSE_TIME = 1380 # 11 PM
    
    def __init__(self):
        self.movies = []
    
    def canSchedule(self, new_movie):
        # Check cinema hours
        if new_movie.start_time < self.OPEN_TIME:
            return False
        if new_movie.end_time() > self.CLOSE_TIME:
            return False
        
        # Check conflicts with existing movies
        for movie in self.movies:
            # Check overlap
            if self._overlaps(new_movie, movie):
                return False
        
        return True
    
    def _overlaps(self, movie1, movie2):
        # Two movies overlap if one starts before the other ends
        return (movie1.start_time < movie2.end_time() and 
                movie1.end_time() > movie2.start_time)
    
    def addMovie(self, movie):
        if self.canSchedule(movie):
            self.movies.append(movie)
            # Keep sorted by start time
            self.movies.sort(key=lambda m: m.start_time)
            return True
        return False
    
    def getAvailableSlots(self):
        """Return list of available time slots"""
        if not self.movies:
            return [(self.OPEN_TIME, self.CLOSE_TIME)]
        
        slots = []
        
        # Before first movie
        if self.movies[0].start_time > self.OPEN_TIME:
            slots.append((self.OPEN_TIME, self.movies[0].start_time))
        
        # Between movies
        for i in range(len(self.movies) - 1):
            gap_start = self.movies[i].end_time()
            gap_end = self.movies[i + 1].start_time
            if gap_end > gap_start:
                slots.append((gap_start, gap_end))
        
        # After last movie
        if self.movies[-1].end_time() < self.CLOSE_TIME:
            slots.append((self.movies[-1].end_time(), self.CLOSE_TIME))
        
        return slots
```

---