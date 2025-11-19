
# Data Structures & Algorithms (DSA) - Atlassian Interview Questions

This document consolidates frequently asked DSA problems from Atlassian interviews. Each problem includes a detailed description, observed variations/follow-ups, and analysis based on candidate experiences.

---

## Atlassian DSA Round Format & Expectations

### HR/Recruiter Screening (Before Technical Rounds)
**Surprise Factor:** Atlassian HR may ask **technical questions** during the initial screening call!

**Common HR Technical Questions:**
1.  "What data structures are used in LRU Cache?"
2.  "How would you design an in-memory cache to store a stream of integer values?"
3.  "What are the major pros and cons of using a hashing data structure?"
4.  "What are the key factors that define good code?"
5.  "What are microservices? How many do you own in your current role?"
6.  "Have you contributed to the architecture or design for any projects?" (Critical question for senior roles)

**Why this matters:**
*   This is not just a "fit" call; they're assessing technical baseline.
*   Be prepared to give concise, clear answers.
*   For senior roles, emphasize architectural contributions and ownership.

### Interview Environment
*   **Local System:** Interviews happen on your local machine (not on online coding platforms)
*   **No Expected Output:** Unlike LeetCode, you don't get sample inputs/outputs in the question
*   **Input Identification:** You must identify correct input/output format based on problem statement
*   **Time Management:** Spend time upfront to clarify input/output formats; don't rush into coding

### Common Challenges
1.  **Ambiguous Inputs:** Take time to identify the correct input format from the problem description
2.  **Follow-up Questions:** Initial problem is usually medium difficulty, but follow-ups can be hard
3.  **Multiple Strategies:** Interviewer may ask you to implement multiple approaches for the same problem

### Success Criteria
*   Solve the main problem correctly with working code
*   Handle at least one follow-up question
*   Write clean, readable code (avoid overly complex solutions)
*   Ask clarifying questions about edge cases

### Intern/New Grad Online Assessment (OA)
*   **Platform:** HackerRank
*   **Duration:** 90 minutes
*   **Questions:** 4 coding problems
*   **Difficulty:** 1 Easy (Arrays) + 2 Medium (Strings, DP) + 1 Hard (3D DP or similar)
*   **Expected Performance:** Solve at least 3 fully + 1 partially (e.g., 11/15 test cases) to proceed
*   **Topics:** Arrays, Strings, Dynamic Programming, Recursion

### What Happens After Partial Solutions?
*   If you solve the main problem but only partially solve follow-ups, **you may still proceed** to further rounds.
*   If your code fails on one test case due to a minor bug but approach is correct, **you may still proceed** if you can explain alternative approaches.
*   However, completely incorrect solutions or inability to explain your logic will likely result in rejection.

---

## 1. Company Hierarchy / Closest Common Ancestor
**Frequency:** Very High
**Core Concept:** Graph/Tree Traversal, Lowest Common Ancestor (LCA)

### Problem Description
You are given a company hierarchy which can be represented as a graph where:
- Nodes are Employees or Departments.
- Edges represent "belongs to" relationships (e.g., Employee A belongs to Department X).
- The structure might not be a strict tree (one employee might belong to multiple teams/departments).

**Task:** Given a list of employees, find the "closest" common department or group that all of them belong to.

### Variations & Follow-ups
1.  **Standard LCA:** If the hierarchy is a strict tree, this is finding the Lowest Common Ancestor.
2.  **Multiple Parents:** Employees can be in multiple departments, and departments can be in multiple parent departments (DAG structure).
3.  **N-ary Tree:** Each node can have $N$ children.
4.  **Closest Group:** Find the group that is "closest" in terms of distance (edges) from the employees.
5.  **Edge Cases:**
    *   Employee doesn't exist.
    *   No common department exists.
    *   Input list contains duplicates.
6.  **Efficiency:**
    *   Optimize for multiple queries (Pre-computation).
    *   Store paths from root to leaves.
7.  **Parent Groups:** Given a target set of employees, find the closest common parent group (Level 2/Medium-Hard variation).

### Analysis & Tips
*   **Clarify the Graph Structure:** Always ask if it's a tree or a general graph (DAG). The approach changes significantly (Tree LCA vs Graph traversals/Intersection of parent sets).
*   **Input Format:** Understand how the input is given (Adjacency list, list of edges, or object references).
*   **Time Complexity:** Be careful with $O(N)$ vs $O(H)$ (height) vs $O(N^2)$ explanations. Pre-computing parents can speed up queries to $O(1)$ or $O(H)$ at the cost of space.
*   **Fail-safe:** Always handle cases where employees don't exist in the graph.

---

## 2. Snake Game
**Frequency:** Very High
**Core Concept:** Simulation, Deque, Hashing

### Problem Description
Design a game of Snake. The snake moves on a 2D grid.
*   **Rules:**
    *   Snake starts at a fixed position with size 3.
    *   Moves in directions: UP, DOWN, LEFT, RIGHT.
    *   Grows by 1 unit every 5 moves (or when eating food - variation dependent).
    *   Game ends if the snake hits itself or the boundaries (sometimes boundaries are wraparound).

### Variations & Follow-ups
1.  **Wraparound Boundaries:** If snake hits the wall, it appears on the other side.
2.  **Food Logic:** Standard game where food appears randomly.
3.  **Growth Logic:** Grow every $k$ moves vs. grow on eating food.
4.  **Collision Detection:** Efficiently check if snake hits its own body.

### Analysis & Tips
*   **Data Structure:** Use a **Deque** (Double Ended Queue) to store snake body coordinates. This allows $O(1)$ addition to head and removal from tail.
*   **Collision:** Use a **HashSet** of coordinates to check for self-collision in $O(1)$.
*   **Modularity:** Separate `Snake`, `Board`, and `Game` logic.

---

## 3. Stock Price Fluctuation / Commodity Prices
**Frequency:** Medium
**Core Concept:** Hash Map + Heap / TreeMap

### Problem Description
You receive a stream of `(timestamp, price)` data points.
*   Timestamps can be out of order.
*   Update price if timestamp exists.
*   **Queries:**
    *   `update(timestamp, price)`
    *   `current()`: Price at the latest timestamp.
    *   `max()`: Maximum price observed so far.
    *   `min()`: Minimum price observed so far.

### Variations & Follow-ups
1.  **Checkpointing:** Given a timestamp and checkpoint, find max price "till then".
2.  **Space/Time Constraints:** Can you do this in $O(1)$? (Usually $O(\log N)$ is acceptable with TreeMap/Heaps).
3.  **Time Complexity Debate:** Be prepared to defend `TreeMap` ($O(\log N)$) vs Hash+Heap ($O(1)$ average/amortized but lazy removal overhead).

### Analysis & Tips
*   **Hash Map:** To store `timestamp -> price` for $O(1)$ lookup/updates.
*   **Two Heaps (Min/Max):** To store prices for min/max queries. *Lazy removal* is key here \u2013 when updating a price, just add the new one to heaps. When popping from top of heap, check if it matches the current price in the Hash Map; if not, discard it.
*   **TreeMap:** In Java, `TreeMap` can handle ordering but adds $O(\log N)$ overhead.

---

## 4. Content Popularity Tracker (All O(1) Data Structure)
**Frequency:** Very High (~40% of rounds)
**Core Concept:** Hash Map + Doubly Linked List (Bucket System)
**Similar to:** LeetCode 432 - All O`one Data Structure

### Problem Description
Implement a data structure to track popularity of content items (pages, posts, videos) in **real-time**.

**Required Operations (ALL MUST BE O(1)):**
*   `increasePopularity(contentId)`: Increase popularity count by 1.
*   `decreasePopularity(contentId)`: Decrease popularity count by 1. If count drops to 0, remove item.
*   `mostPopular()`: Return the contentId with highest popularity. If ties, return any one. If no content, return -1.

**Critical Constraint:** All operations must be **O(1) time complexity**.

**Constraints:**
*   1 ≤ contentId ≤ 10⁹ (or string)
*   At most 10⁵ total operations

**Example:**
```
increasePopularity(5)      // 5 has count 1
increasePopularity(5)      // 5 has count 2
increasePopularity(7)      // 7 has count 1
mostPopular()              // returns 5 (count = 2)
decreasePopularity(5)      // 5 has count 1
mostPopular()              // returns 5 or 7 (both count = 1, either valid)
```

### Why This is NOT Simple Voting
This is fundamentally different from "count votes and sort":
*   **Real-time updates:** Must handle increments/decrements continuously
*   **O(1) requirement:** Cannot sort after every operation (that would be O(N log N))
*   **Dynamic tracking:** Content can increase and decrease in popularity over time

### Solution Approach: Doubly Linked List + HashMap

**Key Insight:** We need O(1) access to both:
1.  The current count of any contentId (HashMap)
2.  The maximum count (head/tail of linked list)

**Data Structures:**
1.  **HashMap:** `contentId -> Node` (which bucket/count this content is in)
2.  **Doubly Linked List of Buckets:** Each bucket node contains:
    *   `count`: The popularity count this bucket represents
    *   `contentIds`: Set of all content IDs with this count
    *   `prev`, `next`: Pointers to adjacent buckets

**Visual Representation:**
```
HEAD <-> [count=1, {id1, id3}] <-> [count=2, {id2}] <-> [count=5, {id4}] <-> TAIL
```

**Operations:**

**increasePopularity(contentId):**
1.  If contentId doesn't exist, create bucket for count=1 if needed, add contentId.
2.  If exists, remove from current bucket (count=C), add to bucket for count=C+1.
3.  If old bucket is empty, remove it from list.
4.  Update HashMap to point to new bucket.

**decreasePopularity(contentId):**
1.  Remove from current bucket (count=C).
2.  If C==1, remove from HashMap (count drops to 0).
3.  If C>1, add to bucket for count=C-1.
4.  If old bucket is empty, remove it from list.

**mostPopular():**
1.  Return any contentId from `tail.prev` bucket (highest count).
2.  If list is empty (only HEAD and TAIL), return -1.

**Time Complexity:** O(1) for all operations
**Space Complexity:** O(N) where N = number of unique content IDs

### Variations & Follow-ups
1.  **Return Top K:** Modify to return K most popular items (traverse from tail).
2.  **Least Popular:** Add `leastPopular()` method (return from `head.next`).
3.  **Get Count:** Add `getCount(contentId)` to return current popularity.
4.  **Temporal Tracking:** Track when each content reached peak popularity.
5.  **Tie-Breaking:** If ties, return most recently modified (use LinkedHashSet for insertion order).

### Common Implementation Bugs (Real Candidate Mistakes)
1.  **Wrong Return Value:** `mostPopular()` should return `contentId`, not the popularity value itself!
2.  **Max Tracking Issues:** When using `max_pop` variable, remember to update it when the last item at `max_pop` is removed.
3.  **Set/Collection Copy Issues (C++):** Doing `auto collection = pop_to_id[initial_pop]` creates a copy, not a reference. Use `auto& collection` or directly modify `pop_to_id[initial_pop]`.
4.  **Negative Popularity Handling:** Should content be allowed to have negative popularity? Clarify with interviewer.
5.  **Empty Case:** Return `-1` or throw exception when no content exists?

---

## 5. Vote Counting & Election Leaderboard
**Frequency:** Medium (~25% of rounds)
**Core Concept:** HashMap + Sorting with Custom Comparators
**Similar to:** LeetCode 347 - Top K Frequent Elements, LeetCode 1366 - Rank Teams by Votes

### Problem Description
Implement a voting system for an election. Given a list of votes (candidate names), determine winners and rankings.

**Parts:**
1.  **Part 1 (Basic):** Who is the winner? (Most votes)
2.  **Part 2 (Tie-Breaking):** If multiple candidates have same highest count, choose based on tie-breaking rule (e.g., alphabetically last name).
3.  **Part 3 (Leaderboard):** Return Top K candidates in order.
4.  **Part 4 (Weighted Voting):** Each vote has a weight (points). Calculate scores.

**Constraints:**
*   1 ≤ number of votes ≤ 10⁶
*   Candidate names are non-empty strings
*   Tie-breaking rule varies by problem

**Example:**
```
votes = ["Alice", "Bob", "Alice", "Charlie", "Bob", "Alice"]

Part 1: Winner = Alice (3 votes)
Part 2: If Alice and Bob both had 3 votes:
  - Alphabetically first: Alice wins
  - Alphabetically last: Bob wins
Part 3 (K=2): ["Alice", "Bob"]
Part 4 (weighted: 1st vote=3pts, 2nd=2pts, 3rd=1pt):
  votes = [["Alice", "Bob"], ["Charlie", "Alice"], ["Bob", "Charlie"]]
  Alice: 3+2=5, Bob: 2+3=5, Charlie: 3+1=4
  Winner: Alice or Bob (need tie-breaker)
```

### Key Difference from Content Popularity Tracker
This is **batch processing** (all votes at once), not real-time streaming:
*   Process votes → Count → Sort → Return result
*   O(N log N) sorting is acceptable (no O(1) requirement)
*   One-time calculation, not continuous updates

### Solution Approach

**Part 1 & 2: Basic Winner with Tie-Breaking**
```python
from collections import Counter

def findWinner(votes, tieBreaker='alphabetical_first'):
    # Count votes
    counts = Counter(votes)
    
    # Find max count
    max_count = max(counts.values())
    
    # Get all candidates with max count
    winners = [name for name, count in counts.items() if count == max_count]
    
    # Apply tie-breaker
    if tieBreaker == 'alphabetical_first':
        return min(winners)
    elif tieBreaker == 'alphabetical_last':
        return max(winners)
    else:
        return winners[0]  # Return any
```

**Part 3: Top K Leaderboard**
```python
def topKCandidates(votes, k):
    counts = Counter(votes)
    
    # Sort by count (descending), then by name (ascending) for ties
    sorted_candidates = sorted(
        counts.items(),
        key=lambda x: (-x[1], x[0])
    )
    
    # Return top K
    return [name for name, count in sorted_candidates[:k]]
```

**Part 4: Weighted Voting (Rank Teams by Votes)**
```python
def rankTeamsByVotes(votes):
    from collections import defaultdict
    
    # votes[i] = "ABC" means A gets 3 points, B gets 2, C gets 1
    num_positions = len(votes[0])
    
    # Track position counts: {candidate: [pos0_count, pos1_count, ...]}
    position_counts = defaultdict(lambda: [0] * num_positions)
    
    for vote in votes:
        for pos, candidate in enumerate(vote):
            position_counts[candidate][pos] += 1
    
    # Sort by position counts (descending), then by name (ascending)
    result = sorted(
        position_counts.keys(),
        key=lambda x: ([-count for count in position_counts[x]], x)
    )
    
    return ''.join(result)
```

**Time Complexity:**
*   Counting: O(N) where N = number of votes
*   Sorting: O(M log M) where M = number of unique candidates
*   Total: O(N + M log M)

### Variations & Tie-Breaking Strategies
1.  **Alphabetical:** First or last alphabetically
2.  **Lexicographical (by name length):** Shorter names first
3.  **Position-based (Weighted):** Compare vote counts at each position
    *   Most 1st-place votes wins
    *   If tie, most 2nd-place votes
    *   Continue for all positions
4.  **First to Reach:** Whoever reached max count first chronologically (requires timestamp tracking)

### Analysis & Tips
*   **Heap for Top K:** Use Min-Heap of size K for O(N log K) instead of O(N log N) full sort.
*   **Custom Comparator:** Master sorting with `key=lambda` or custom `__lt__` method.
*   **Edge Cases:**
    *   Single candidate → automatic winner
    *   All candidates tied → apply tie-breaker to all
    *   Empty votes → no winner
*   **For Weighted Voting:** Store arrays of position counts for comparison.

---

## 6. File Collection / Report Generator
**Frequency:** Medium
**Core Concept:** Aggregation, Hash Maps, Sorting/Heaps

### Problem Description
Given a list of files with: `Name`, `Size`, `Collection` (optional).
A file can belong to multiple collections.
**Task:** Generate a report:
1.  Total size of all files.
2.  Top N collections by size.

### Variations & Follow-ups
1.  **Nested Collections:** Collections can contain other collections.
2.  **Updates:** How to handle dynamic updates to file sizes?
3.  **Scale:** Process large file that cannot fit in memory (External Sort / MapReduce).

### Analysis & Tips
*   **Nesting:** This implies a Tree/Graph structure. Recursive size calculation (DFS) with memoization might be needed.
*   **Top N:** Use a Min-Heap of size N to maintain the top elements efficiently.

---

## 7. Router / Middleware Design with Wildcards
**Frequency:** Medium (~25-30% of rounds)
**Core Concept:** Trie (Prefix Tree), Pattern Matching
**Similar to:** LeetCode 208 - Implement Trie, LeetCode 677 - Map Sum Pairs

### Problem Description
Design an HTTP router that matches URL paths to handlers. Support:
*   **Exact Matching:** `/api/users` matches only `/api/users`
*   **Wildcard Matching:** `/api/*/profile` where `*` matches any single segment
*   **Priority:** Exact matches take precedence over wildcards

**Operations:**
*   `addRoute(path, handler)`: Register a route (handler is string or function)
*   `matchRoute(path)`: Return handler for matching route, or `null` if no match

**Constraints:**
*   Paths are case-sensitive
*   `*` matches exactly **one** segment (not zero, not multiple)
*   1 ≤ number of routes ≤ 1000
*   1 ≤ segments per path ≤ 10

**Example:**
```
addRoute("/api/users", "getUsersHandler")
addRoute("/api/*/profile", "getProfileHandler")
addRoute("/api/*/settings/*", "getSettingsHandler")

matchRoute("/api/users")          → "getUsersHandler" (exact match)
matchRoute("/api/123/profile")    → "getProfileHandler" (wildcard match)
matchRoute("/api/123/settings/privacy") → "getSettingsHandler"
matchRoute("/api/unknown")        → null (no match)
```

### Variations & Follow-ups
1.  **Multiple Wildcards in One Path:** `/api/*/profile/*` (multiple `*` per path).
2.  **Precedence Conflicts:** What if both `/api/*/profile` and `/api/users/profile` exist and we query `/api/users/profile`? (Exact wins).
3.  **Parameter Extraction:** Instead of just matching, extract dynamic segments: `/user/:id` → extract `{id: 123}`.
4.  **Greedy Wildcards:** `**` matches multiple segments (e.g., `/files/**` matches `/files/a/b/c`).
5.  **Performance:** Optimize for 10,000 routes; consider caching.

### Solution Approach

**Data Structure: Trie (Prefix Tree)**
*   Each node represents a path segment.
*   Nodes have:
    *   `children`: Map of `segment -> TrieNode`
    *   `isWildcard`: Boolean (true if this node is `*`)
    *   `handler`: Stored at terminal nodes (end of path)

**Algorithm:**

**addRoute(path, handler):**
1.  Split path by `/` → segments.
2.  Traverse/create Trie nodes for each segment.
3.  Mark last node with `handler`.

**matchRoute(path):**
1.  Split path by `/` → segments.
2.  **DFS Traversal** with two branches at each level:
    *   Try exact match (`children[segment]`)
    *   Try wildcard match (`children['*']`)
3.  **Priority:** If both exact and wildcard match, return exact first.
4.  If reach end of path, return `handler` or `null`.

**Time Complexity:**
*   `addRoute`: O(L) where L = number of segments
*   `matchRoute`: O(L * W) where W = number of wildcards (worst case DFS branches)

### Code Structure (Python)
```python
class TrieNode:
    def __init__(self):
        self.children = {}  # {segment: TrieNode}
        self.handler = None
        
class Router:
    def __init__(self):
        self.root = TrieNode()
    
    def addRoute(self, path, handler):
        segments = [s for s in path.split('/') if s]  # Remove empty
        node = self.root
        
        for segment in segments:
            if segment not in node.children:
                node.children[segment] = TrieNode()
            node = node.children[segment]
        
        node.handler = handler
    
    def matchRoute(self, path):
        segments = [s for s in path.split('/') if s]
        return self._dfs(self.root, segments, 0)
    
    def _dfs(self, node, segments, index):
        # Base case: reached end of path
        if index == len(segments):
            return node.handler
        
        segment = segments[index]
        
        # Priority 1: Try exact match first
        if segment in node.children:
            result = self._dfs(node.children[segment], segments, index + 1)
            if result is not None:
                return result
        
        # Priority 2: Try wildcard match
        if '*' in node.children:
            result = self._dfs(node.children['*'], segments, index + 1)
            if result is not None:
                return result
        
        return None  # No match found
```

### Analysis & Tips
*   **Wildcard Node:** Treat `*` as a special segment in the Trie.
*   **Priority Handling:** Always try exact match before wildcard (order matters in DFS).
*   **Edge Cases:**
    *   Empty path: `""` or `"/"` → clarify if this should match root.
    *   Trailing slash: `/api/users` vs `/api/users/` → usually treated as same.
    *   Multiple consecutive slashes: `/api//users` → normalize input.
*   **Optimization:** For static routes (no wildcards), use a HashMap for O(1) lookup instead of Trie.
*   **Parameter Extraction (Follow-up):** Store param name in node (e.g., `:id`), collect during traversal.

---

## 8. Robot Parts Assembly / Inventory Management
**Frequency:** Low-Medium (~20% of rounds)
**Core Concept:** Hash Map, Multiset Matching
**Similar to:** LeetCode 383 - Ransom Note, LeetCode 1657 - Determine if Two Strings Are Close

### Problem Description
You manage a robot assembly factory. Each robot requires a specific **multiset** of parts (e.g., 2 wheels, 1 motor, 3 sensors).

**Operations:**
1.  `canBuild(requirements)`: Check if inventory has enough parts.
2.  `build(requirements)`: If possible, consume parts and return success. Otherwise, return list of missing parts.

**Constraints:**
*   Part names are case-sensitive strings
*   Duplicates matter (robot might need 4 identical wheels)
*   1 ≤ inventory size ≤ 10⁶
*   1 ≤ requirements size ≤ 100

**Example:**
```
Inventory: ["wheel", "wheel", "wheel", "motor", "sensor", "sensor"]
Requirements: ["wheel", "wheel", "motor"]

canBuild(requirements) → True
build(requirements) → Success
  New Inventory: ["wheel", "sensor", "sensor"]

Requirements: ["wheel", "wheel", "wheel"]
canBuild(requirements) → False (only 1 wheel left)
build(requirements) → ["wheel: need 2 more"]
```

### Variations & Follow-ups
1.  **Multiple Robot Types:** Build different robots with different requirements.
2.  **Priority Queue:** Some orders have higher priority; fulfill them first.
3.  **Partial Builds:** Allow building if we have ≥80% of parts (with penalty).
4.  **Replenishment:** Add parts to inventory over time.
5.  **Return Missing Counts:** Instead of just `canBuild`, return how many more of each part is needed.

### Solution Approach

**Data Structure: Hash Map (Counter)**
*   `inventory_map`: `{part_name: count}`
*   `requirements_map`: `{part_name: count}`

**Algorithm:**

**canBuild(requirements):**
```python
def canBuild(requirements):
    req_count = Counter(requirements)
    inv_count = Counter(inventory)
    
    for part, needed in req_count.items():
        if inv_count[part] < needed:
            return False
    return True
```

**build(requirements):**
```python
def build(requirements):
    req_count = Counter(requirements)
    inv_count = Counter(inventory)
    
    missing = []
    for part, needed in req_count.items():
        if inv_count[part] < needed:
            missing.append(f"{part}: need {needed - inv_count[part]} more")
    
    if missing:
        return {"success": False, "missing": missing}
    
    # Consume parts
    for part, needed in req_count.items():
        for _ in range(needed):
            inventory.remove(part)  # O(N) per remove
    
    return {"success": True}
```

**Time Complexity:**
*   `canBuild`: O(R) where R = size of requirements
*   `build`: O(R + I) where I = inventory size (due to `remove` operations)

**Optimization:** Instead of list, use `inventory_map` and decrement counts → O(R).

### Optimized Implementation
```python
class RobotFactory:
    def __init__(self, inventory):
        from collections import Counter
        self.inventory = Counter(inventory)
    
    def canBuild(self, requirements):
        req_count = Counter(requirements)
        for part, needed in req_count.items():
            if self.inventory[part] < needed:
                return False
        return True
    
    def build(self, requirements):
        req_count = Counter(requirements)
        
        # Check availability
        missing = {}
        for part, needed in req_count.items():
            if self.inventory[part] < needed:
                missing[part] = needed - self.inventory[part]
        
        if missing:
            return {"success": False, "missing": missing}
        
        # Consume parts
        for part, needed in req_count.items():
            self.inventory[part] -= needed
        
        return {"success": True}
```

### Analysis & Tips
*   **Counter vs Manual HashMap:** Python's `Counter` is a HashMap that defaults to 0 for missing keys.
*   **Edge Cases:**
    *   Empty requirements → can always build.
    *   Part not in inventory → treat as 0 available.
    *   Negative counts → invalid input (clarify with interviewer).
*   **Follow-up (Multiple Robots):** Iterate through robots in priority order, build if possible.
*   **Testing:** Test with: exact match, insufficient parts, extra parts, duplicates.

---

## 9. Badge Access / Security System
**Frequency:** Low
**Core Concept:** Set/Map Operations

### Problem Description
Given a list of badge records `[Name, Action(Enter/Exit)]`.
**Task:** Find:
1.  Employees who entered without exiting.
2.  Employees who exited without entering.

### Analysis & Tips
*   **State Tracking:** Maintain a `Set` of users currently "inside".
*   **Validation:**
    *   If `Exit` and user NOT in set -> Exit without Enter.
    *   If `Enter` and user ALREADY in set -> Missing previous Exit? (Clarify requirement).
    *   At end of logs, anyone left in Set -> Enter without Exit.

---

## Tic Tac Toe (See Code_Design_LLD.md)
**Frequency:** Low
**Core Concept:** Matrix / Simulation

### Problem Description
Implement a fully functional Tic Tac Toe game (often as a React component in frontend interviews, or class design in backend).

### Requirements
*   3x3 Grid.
*   Two players (X and O).
*   Win detection (Horizontal, Vertical, Diagonal).
*   Draw detection.
*   Restart functionality.

### Analysis & Tips
*   **Win Check:** $O(1)$ check possible by storing row/col/diagonal sums (Player 1 adds +1, Player 2 adds -1). If `abs(sum) == 3`, someone won.
*   **Frontend:** Focus on State Management (React `useState`) and Component modularity.

---

## 10. Tennis Court Booking / Interval Assignment
**Frequency:** Medium (~30% of rounds)
**Core Concept:** Greedy, Sorting, Min-Heap
**Similar to:** LeetCode 253 - Meeting Rooms II

### Problem Description
You manage a tennis club with unlimited courts. Given a list of booking requests with `[start_time, finish_time]`:
*   **Goal:** Assign each booking to a court such that no two bookings on the same court overlap.
*   **Objective:** Minimize the total number of courts used.

**Key Rule:** If one booking ends at time T and another starts at T, they do NOT overlap (can use the same court).

**Constraints:**
*   1 ≤ N ≤ 10⁵ bookings
*   0 ≤ start_time < finish_time ≤ 10⁹

**Example:**
```
Input: [[0, 30], [5, 10], [15, 20]]
Output: 2 courts needed
Explanation:
  Court 1: [0, 30]
  Court 2: [5, 10], [15, 20]
```

### Variations & Follow-ups
1.  **Maximize Utilization:** Instead of minimizing courts, maximize bookings given a fixed number of courts.
2.  **Priority Bookings:** Some bookings have higher priority; assign them first.
3.  **Return Court Assignments:** Not just the count, but which court each booking goes to.
4.  **Multiple Resources:** Extend to multiple types of courts (clay, grass, hard).

### Solution Approach

**Algorithm: Greedy + Min-Heap**
1.  **Sort** bookings by `start_time`.
2.  Use a **Min-Heap** to track the `end_time` of currently occupied courts.
3.  For each booking:
    *   If `heap.min <= current.start`, reuse that court (pop from heap).
    *   Otherwise, allocate a new court (increase count).
    *   Push `current.end_time` to heap.
4.  **Answer:** Size of heap (or max size of heap during iteration).

**Time Complexity:** O(N log N) for sorting + O(N log N) for heap operations = O(N log N)
**Space Complexity:** O(N) for heap

### Code Structure (Python)
```python
import heapq

def minCourts(bookings):
    if not bookings:
        return 0
    
    # Sort by start time
    bookings.sort(key=lambda x: x[0])
    
    # Min-heap to store end times
    heap = []
    
    for start, end in bookings:
        # If earliest ending court is free, reuse it
        if heap and heap[0] <= start:
            heapq.heappop(heap)
        
        # Assign this booking (either reuse or new court)
        heapq.heappush(heap, end)
    
    return len(heap)  # Number of courts needed
```

### Analysis & Tips
*   **Edge Case:** Empty bookings → return 0.
*   **Boundary Condition:** If `end_time == start_time` of next booking, they can share (clarify with interviewer).
*   **Heap Choice:** Min-Heap because we want to know the earliest finishing court.
*   **Why Sort by Start?** Processing in chronological order ensures we always make optimal decisions.
*   **Follow-up (Court Assignments):** Maintain a dictionary `{court_id: end_time}` instead of just a heap.

---

## 11. Word Wrap / Text Justification
**Frequency:** Medium-High (~30-35% of rounds)
**Core Concept:** Greedy, String Manipulation, Dynamic Programming
**Similar to:** LeetCode 68 - Text Justification

### Problem Description
Given a list of `words` and a `maxWidth`, format the text such that:
*   Each line has **exactly** `maxWidth` characters.
*   Text is **fully justified** (except the last line, which is left-justified).

**Justification Rules:**
1.  **Pack Greedily:** Fit as many words as possible per line.
2.  **Distribute Spaces:** Pad extra spaces evenly between words.
3.  **Left-Heavy Distribution:** If spaces don't divide evenly, assign more to left gaps.
4.  **Last Line:** Left-justified only (single space between words, pad end with spaces).

**Constraints:**
*   1 ≤ words.length ≤ 300
*   1 ≤ words[i].length ≤ maxWidth
*   1 ≤ maxWidth ≤ 100
*   Words consist of non-space characters only

**Example:**
```
Input: words = ["This", "is", "an", "example", "of", "text", "justification."], maxWidth = 16

Output:
[
   "This    is    an",  // 3 spaces between "This" and "is", 4 between "is" and "an"
   "example  of text",  // 2 spaces each
   "justification.  "   // Last line: left-justified with trailing spaces
]
```

### Variations & Follow-ups
1.  **Line Count Constraint:** Fit text in exactly K lines (may require splitting words).
2.  **Hyphenation:** Break long words with hyphens if they don't fit.
3.  **Cost Function:** Minimize total "raggedness" (sum of squared extra spaces).
4.  **Dynamic Width:** Lines can have variable width (e.g., HTML text flow).

### Solution Approach

**Algorithm: Greedy Line Packing + Space Distribution**

**Step 1: Pack Words into Lines**
```python
def packLines(words, maxWidth):
    lines = []
    i = 0
    
    while i < len(words):
        # Determine which words fit on this line
        line_length = len(words[i])
        j = i + 1
        
        while j < len(words):
            # Need at least 1 space between words
            if line_length + 1 + len(words[j]) > maxWidth:
                break
            line_length += 1 + len(words[j])
            j += 1
        
        # words[i:j] go on this line
        lines.append((i, j))  # (start_index, end_index)
        i = j
    
    return lines
```

**Step 2: Justify Each Line**
```python
def justify(words, L, R, maxWidth, isLastLine):
    num_words = R - L
    
    # Last line: left-justified
    if isLastLine or num_words == 1:
        line = ' '.join(words[L:R])
        return line + ' ' * (maxWidth - len(line))
    
    # Calculate spaces needed
    total_word_length = sum(len(words[i]) for i in range(L, R))
    total_spaces = maxWidth - total_word_length
    gaps = num_words - 1
    
    # Distribute spaces
    space_per_gap = total_spaces // gaps
    extra_spaces = total_spaces % gaps  # Extra spaces go to leftmost gaps
    
    line = []
    for i in range(L, R):
        line.append(words[i])
        if i < R - 1:  # Not the last word
            # Add base spaces + 1 extra for first 'extra_spaces' gaps
            spaces = space_per_gap + (1 if i - L < extra_spaces else 0)
            line.append(' ' * spaces)
    
    return ''.join(line)
```

**Time Complexity:** O(N) where N = total characters in all words
**Space Complexity:** O(maxWidth) for building each line

### Complete Implementation
```python
def fullJustify(words, maxWidth):
    result = []
    i = 0
    
    while i < len(words):
        # Pack words for current line
        line_length = len(words[i])
        j = i + 1
        
        while j < len(words) and line_length + 1 + len(words[j]) <= maxWidth:
            line_length += 1 + len(words[j])
            j += 1
        
        # Justify this line
        num_words = j - i
        is_last_line = (j == len(words))
        
        if is_last_line or num_words == 1:
            # Left-justified
            line = ' '.join(words[i:j])
            line += ' ' * (maxWidth - len(line))
        else:
            # Fully justified
            total_word_len = sum(len(word) for word in words[i:j])
            total_spaces = maxWidth - total_word_len
            gaps = num_words - 1
            space_per_gap = total_spaces // gaps
            extra = total_spaces % gaps
            
            line = []
            for k in range(i, j):
                line.append(words[k])
                if k < j - 1:
                    spaces = space_per_gap + (1 if k - i < extra else 0)
                    line.append(' ' * spaces)
            line = ''.join(line)
        
        result.append(line)
        i = j
    
    return result
```

### Analysis & Tips
*   **Edge Cases:**
    *   Single word per line → left-justify with trailing spaces.
    *   Last line → always left-justified.
    *   One word total → pad with spaces to maxWidth.
*   **Space Distribution:** 
    *   If 10 spaces for 3 gaps: `[4, 3, 3]` (left-heavy).
    *   Use `extra_spaces` to track how many gaps get +1 space.
*   **Testing:** Verify with examples where spaces don't divide evenly.
*   **Common Mistakes:**
    *   Forgetting to left-justify last line.
    *   Not padding trailing spaces when words don't fill line.
    *   Off-by-one errors in gap counting.

---

## 12. Word Search / Anagram Search
**Frequency:** Low
**Core Concept:** Grid DFS/BFS, Hash Maps

### Problem Description
*   **Variation 1 (Grid):** Find a word in a 2D grid of characters (only move Down/Right).
*   **Variation 2 (List):** Given a main word and a list of words, find which word from the list is an anagram of the main word (or part of it).

### Analysis & Tips
*   **DFS/BFS:** Standard grid traversal.
*   **Anagrams:** Frequency arrays (size 26) or Hash Maps for character counting.

---

## 13. Find K Closest Elements
**Frequency:** Low-Medium
**Core Concept:** Binary Search, Two Pointers, Heap

### Problem Description
Given a sorted integer array `arr`, two integers `k` and `x`, return the `k` closest integers to `x` in the array. The result should also be sorted in ascending order. If there is a tie, the smaller elements are preferred.

**Example:**
*   Input: `arr = [1,2,3,4,5]`, `k = 4`, `x = 3`
*   Output: `[1,2,3,4]`

### Variations & Follow-ups
1.  **Unsorted Array:** If the array is not sorted, how would you approach it?
2.  **Distance Metric:** Define what "closest" means (absolute difference vs. other metrics).
3.  **Efficiency:** Optimize to $O(\log N + k)$ instead of $O(N)$.

### Analysis & Tips
*   **Binary Search + Two Pointers:** Find the position closest to `x` using binary search, then expand left and right using two pointers to collect `k` elements.
*   **Binary Search Window:** Binary search for the start of the k-element window. Compare `x - arr[mid]` vs `arr[mid + k] - x` to decide which side to search.
*   **Min-Heap:** For unsorted arrays, use a min-heap with custom comparator based on distance to `x`.
*   **LeetCode Reference:** This is LeetCode 658.

---

## Summary of DSA Problems

| # | Problem | Frequency | Key Data Structures | LeetCode Similar |
|---|---------|-----------|---------------------|------------------|
| 1 | Company Hierarchy | Very High | Tree/Graph, LCA | 236 |
| 2 | Snake Game | Very High | Deque, HashSet | 353 |
| 3 | Stock Price Fluctuation | Medium | HashMap + Heap/TreeMap | 2034 |
| 4 | Content Popularity Tracker | Very High (~40%) | HashMap + Doubly Linked List | 432 |
| 5 | Vote Counting & Leaderboard | Medium (~25%) | HashMap + Sorting | 347, 1366 |
| 6 | File Collections | Medium | HashMap, Min-Heap | 347 |
| 7 | Router with Wildcards | Medium (~25-30%) | Trie + DFS | 208, 677 |
| 8 | Robot Parts Assembly | Low-Medium (~20%) | HashMap (Counter) | 383, 1657 |
| 9 | Badge Access | Low | Set/HashMap | - |
| 10 | Tennis Court Booking | Medium (~30%) | Sorting, Min-Heap | 253 |
| 11 | Word Wrap / Text Justification | Medium-High (~30-35%) | Greedy, String | 68 |
| 12 | Word Search / Anagram | Low | DFS/BFS, HashMap | 79 |
| 13 | Find K Closest Elements | Low-Medium | Binary Search, Heap | 658 |

**Preparation Priority:**
1. **Must-Know (Very High):** Problems 1, 2, 4 - These are core Atlassian problems
2. **Should-Know (Medium-High):** Problems 5, 7, 10, 11 - Frequently asked
3. **Important (Medium):** Problems 3, 6, 10 - Common in DSA rounds
4. **Good-to-Know (Low-Medium):** Problems 8, 13 - Occasional appearances
5. **Nice-to-Have (Low):** Problems 9, 12 - Rare but possible

**Key Distinction:**
- **Problem 4 (Content Popularity):** Real-time O(1) operations, streaming data
- **Problem 5 (Vote Counting):** Batch processing, sorting acceptable, one-time calculation

---
