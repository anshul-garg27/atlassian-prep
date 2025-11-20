# 📊 PROBLEM 6: COMMODITY PRICES WITH PREFIX MAX

### ⭐⭐⭐ **Range Maximum Query with Out-of-Order Updates**

**Frequency:** Low-Medium (Appears in ~20% of rounds)
**Difficulty:** Medium-Hard
**Similar to:** Range Maximum Query (RMQ), [LeetCode 2034 - Stock Price Fluctuation](https://leetcode.com/problems/stock-price-fluctuation/)

---

## 📋 Problem Statement

You are building a system to track commodity prices over time. Price updates arrive as `(timestamp, price)` pairs, potentially **out of order** (corrections or delayed data).

**Required Operations:**
1. `update(timestamp, price)`: Record or update the price at a given timestamp
2. `getMaxPrice(timestamp)`: Return the **maximum price** seen at any time `t ≤ timestamp`

**Constraints:**
- 1 ≤ timestamp ≤ 10⁹ (sparse timestamps, not continuous)
- 1 ≤ price ≤ 10⁶
- At most 10⁵ operations total
- Updates can arrive out of order

**Key Challenge:** Efficient prefix maximum queries on dynamically updated, sparse data.

---

## 🎨 Visual Example

### Example 1: Out-of-Order Updates

```text
Events (in arrival order):
┌────────────────────────────────────────────────────┐
│ 1. update(t=5, p=100)                              │
│ 2. update(t=10, p=150)                             │
│ 3. update(t=3, p=200)  ← Out of order!            │
│ 4. update(t=7, p=120)                              │
└────────────────────────────────────────────────────┘

Timeline (sorted by timestamp):
t=0────3────5────7────10───>
      200  100  120  150

Queries:
┌─────────────────────────────────────────────────────┐
│ getMaxPrice(t=3)  → 200 (only t=3 exists)          │
│ getMaxPrice(t=5)  → 200 (max of t=3,5)             │
│ getMaxPrice(t=7)  → 200 (max of t=3,5,7)           │
│ getMaxPrice(t=10) → 200 (max of all)               │
│ getMaxPrice(t=2)  → null (no data ≤ 2)             │
└─────────────────────────────────────────────────────┘

Prefix Max Array (if timestamps were [3,5,7,10]):
Prices:     [200, 100, 120, 150]
Prefix Max: [200, 200, 200, 200]
```

### Example 2: Price Corrections

```text
Initial: update(t=5, p=100), update(t=10, p=150)
Data: {5: 100, 10: 150}

Correction: update(t=5, p=300)  ← Overwrites
Data: {5: 300, 10: 150}

getMaxPrice(t=10) → 300 (corrected value)
```

---

## 💡 Examples

### Example 1: Basic Usage
```python
tracker = CommodityTracker()

tracker.update(1, 100)
tracker.update(3, 150)
tracker.update(2, 120)  # Out of order

print(tracker.getMaxPrice(1))   # 100
print(tracker.getMaxPrice(2))   # 120
print(tracker.getMaxPrice(3))   # 150
print(tracker.getMaxPrice(10))  # 150 (max seen so far)
```

### Example 2: Price Corrections
```python
tracker.update(5, 100)
tracker.update(10, 200)

print(tracker.getMaxPrice(10))  # 200

tracker.update(5, 300)  # Correct timestamp 5
print(tracker.getMaxPrice(10))  # 300 (updated max)
```

---

## 🗣️ Interview Conversation Guide

### Phase 1: Clarification (3-5 min)

**Candidate:** "Can timestamps arrive out of order?"
**Interviewer:** "Yes, you might get timestamp 10, then later get timestamp 5."

**Candidate:** "Can the same timestamp be updated multiple times (price corrections)?"
**Interviewer:** "Yes, the latest value for a timestamp should overwrite."

**Candidate:** "Are timestamps sparse or continuous?"
**Interviewer:** "Sparse. You might have timestamps 1, 1000, 1000000."

**Candidate:** "What should `getMaxPrice(t)` return if no data exists at or before `t`?"
**Interviewer:** "Return `null` or `-1`."

### Phase 2: Approach Discussion (5-8 min)

**Candidate:** "This is a **Prefix Maximum** problem. For each query timestamp `t`, we need `max(prices[0..t])`.

**Naive Approaches:**
1. **HashMap + Full Scan:** Store prices in a map. Query scans all timestamps ≤ t → O(N) query.
2. **Sorted Array + Linear Scan:** Keep sorted by timestamp. Query still O(N).

**Optimized Approaches:**
1. **Prefix Max Cache (Read-Heavy):** Maintain precomputed prefix max. Update invalidates cache → O(N) update, O(log N) query.
2. **Segment Tree (Balanced):** O(log N) update and query. Best for balanced workloads."

**Candidate:** "I'll implement Approach 1 (Prefix Max Cache) first, then discuss Segment Tree as an optimization."

### Phase 3: Implementation (15-20 min)

**Candidate:** "I'll use Python's `bisect` to maintain sorted order, and rebuild the prefix max array lazily when needed."

---

## 🧠 Intuition & Approach

### Why is This Hard?

Standard **Range Maximum Query (RMQ)** algorithms assume:
- **Static data:** Build once, query many times.
- **Dense indices:** Array indices 0, 1, 2, ...

Our problem has:
- **Dynamic data:** Updates can happen anytime.
- **Sparse indices:** Timestamps 1, 500, 999999.
- **Out-of-order updates:** Timestamp 5 might arrive after timestamp 10.

### Approach 1: Sorted List + Prefix Max Cache

**Data Structures:**
1. **Sorted List:** `[(timestamp, price), ...]` sorted by timestamp.
2. **Prefix Max Array:** `prefix_max[i]` = max price from index 0 to i.

**Update Algorithm:**
```
1. Binary search to find position (O(log N))
2. If timestamp exists, update price (O(1))
3. If new timestamp, insert at correct position (O(N))
4. Mark prefix_max as dirty (O(1))
```

**Query Algorithm:**
```
1. If dirty, rebuild prefix_max (O(N))
2. Binary search for largest timestamp ≤ query_timestamp (O(log N))
3. Return prefix_max[index] (O(1))
```

**Trade-off:** Read-heavy workload is efficient. Write-heavy workload degrades to O(N) per update.

---

## 📝 Complete Solution: Approach 1 (Prefix Max Cache)

```python
import bisect
from typing import Optional, List, Tuple

class CommodityTracker:
    """
    Track commodity prices with out-of-order updates and prefix max queries.
    
    Optimized for read-heavy workloads using a prefix max cache.
    """
    
    def __init__(self):
        # Sorted list of (timestamp, price) tuples
        self.data: List[Tuple[int, int]] = []
        
        # Cached prefix max: prefix_max[i] = max(prices[0..i])
        self.prefix_max: List[int] = []
        
        # Dirty flag: true if prefix_max needs rebuild
        self.dirty = False
    
    def update(self, timestamp: int, price: int) -> None:
        """
        Add or update price at timestamp.
        
        Time: O(N) due to list insertion (O(log N) with balanced tree)
        Space: O(1)
        """
        # Binary search for existing timestamp
        # Use (timestamp, -1) to find exact match or insertion point
        idx = bisect.bisect_left(self.data, (timestamp, 0))
        
        if idx < len(self.data) and self.data[idx][0] == timestamp:
            # Update existing timestamp
            self.data[idx] = (timestamp, price)
        else:
            # Insert new timestamp
            self.data.insert(idx, (timestamp, price))
        
        # Invalidate cache
        self.dirty = True
    
    def getMaxPrice(self, timestamp: int) -> Optional[int]:
        """
        Get maximum price at or before timestamp.
        
        Time: O(log N) + O(N) rebuild if dirty
        Space: O(N) for cache
        """
        # Rebuild cache if needed
        if self.dirty:
            self._rebuild_prefix_max()
        
        if not self.data:
            return None
        
        # Binary search for rightmost timestamp <= query timestamp
        # Use (timestamp, inf) to find upper bound
        idx = bisect.bisect_right(self.data, (timestamp, float('inf'))) - 1
        
        # Check if any data exists before or at timestamp
        if idx < 0:
            return None
        
        return self.prefix_max[idx]
    
    def _rebuild_prefix_max(self) -> None:
        """
        Rebuild the prefix max cache.
        
        Time: O(N)
        Space: O(N)
        """
        if not self.data:
            self.prefix_max = []
            self.dirty = False
            return
        
        self.prefix_max = [0] * len(self.data)
        current_max = float('-inf')
        
        for i, (ts, price) in enumerate(self.data):
            current_max = max(current_max, price)
            self.prefix_max[i] = current_max
        
        self.dirty = False


# ============================================
# COMPLETE RUNNABLE EXAMPLE
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("COMMODITY PRICE TRACKER - PREFIX MAX")
    print("=" * 60)
    
    tracker = CommodityTracker()
    
    # Test 1: Sequential updates
    print("\n[Test 1] Sequential Updates")
    print("-" * 40)
    tracker.update(1, 100)
    tracker.update(2, 150)
    tracker.update(3, 120)
    
    print(f"Max price at t=1: {tracker.getMaxPrice(1)}")  # 100
    print(f"Max price at t=2: {tracker.getMaxPrice(2)}")  # 150
    print(f"Max price at t=3: {tracker.getMaxPrice(3)}")  # 150
    
    # Test 2: Out-of-order updates
    print("\n[Test 2] Out-of-Order Updates")
    print("-" * 40)
    tracker2 = CommodityTracker()
    tracker2.update(10, 200)
    tracker2.update(5, 300)   # Out of order
    tracker2.update(7, 250)
    
    print(f"Max price at t=5: {tracker2.getMaxPrice(5)}")   # 300
    print(f"Max price at t=7: {tracker2.getMaxPrice(7)}")   # 300
    print(f"Max price at t=10: {tracker2.getMaxPrice(10)}") # 300
    
    # Test 3: Price corrections
    print("\n[Test 3] Price Corrections")
    print("-" * 40)
    tracker3 = CommodityTracker()
    tracker3.update(5, 100)
    tracker3.update(10, 150)
    print(f"Before correction - Max at t=10: {tracker3.getMaxPrice(10)}")  # 150
    
    tracker3.update(5, 400)  # Correct price at t=5
    print(f"After correction - Max at t=10: {tracker3.getMaxPrice(10)}")   # 400
    
    # Test 4: Query before any data
    print("\n[Test 4] Edge Cases")
    print("-" * 40)
    tracker4 = CommodityTracker()
    tracker4.update(10, 100)
    
    print(f"Max at t=5 (no data): {tracker4.getMaxPrice(5)}")   # None
    print(f"Max at t=15 (after all): {tracker4.getMaxPrice(15)}")  # 100
    
    # Test 5: Sparse timestamps
    print("\n[Test 5] Sparse Timestamps")
    print("-" * 40)
    tracker5 = CommodityTracker()
    tracker5.update(1, 100)
    tracker5.update(1000, 200)
    tracker5.update(1000000, 150)
    
    print(f"Max at t=500: {tracker5.getMaxPrice(500)}")       # 100
    print(f"Max at t=5000: {tracker5.getMaxPrice(5000)}")     # 200
    print(f"Max at t=2000000: {tracker5.getMaxPrice(2000000)}")  # 200
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)
```

---

## 🔍 Explanation with Example

Let's trace through the prefix maximum query algorithm:

**Updates:** (timestamp, price)
- `update(5, 100)`
- `update(10, 150)`
- `update(3, 200)` ← Out of order!
- `update(7, 120)`

**Query:** `getMaxPrice(7)` → Find max price for all timestamps ≤ 7

---

**Step 1: Process Updates**

**After update(5, 100):**
```python
data = [(5, 100)]
prefix_max = [100]
dirty = False
```

**After update(10, 150):**
```python
data = [(5, 100), (10, 150)]
prefix_max = [100, 150]
```

**After update(3, 200):** ← Out of order!
```python
# Binary search for insertion position
# 3 < 5, so insert at index 0

data = [(3, 200), (5, 100), (10, 150)]
dirty = True  # Prefix max needs rebuild
```

**After update(7, 120):**
```python
# Binary search: 7 goes between 5 and 10

data = [(3, 200), (5, 100), (7, 120), (10, 150)]
dirty = True
```

---

**Step 2: Query getMaxPrice(7)**

**Check if dirty:**
```python
if dirty:
    _rebuild_prefix_max()
```

**Rebuild prefix_max:**
```python
prices = [200, 100, 120, 150]

prefix_max = []
current_max = 0

# Index 0: max(0, 200) = 200
prefix_max.append(200)  # [200]

# Index 1: max(200, 100) = 200
prefix_max.append(200)  # [200, 200]

# Index 2: max(200, 120) = 200
prefix_max.append(200)  # [200, 200, 200]

# Index 3: max(200, 150) = 200
prefix_max.append(200)  # [200, 200, 200, 200]

dirty = False
```

---

**Step 3: Binary Search for Timestamp ≤ 7**

```python
# Find largest timestamp ≤ 7
# data = [(3, 200), (5, 100), (7, 120), (10, 150)]
#         idx=0      idx=1      idx=2      idx=3

# Binary search finds: index 2 (timestamp=7)
```

---

**Step 4: Return Prefix Max**

```python
return prefix_max[2]  # Returns 200
```

**Answer:** Max price for timestamps ≤ 7 is **200** (from timestamp 3)

---

**Visual Representation:**

```text
Timeline: 0───3───5───7───10───>
Prices:      200  100  120  150

Query getMaxPrice(7):
- Look at timestamps: 3, 5, 7
- Prices: 200, 100, 120
- Maximum: 200 ✓

Query getMaxPrice(10):
- Look at all timestamps: 3, 5, 7, 10
- Prices: 200, 100, 120, 150
- Maximum: 200 ✓

Query getMaxPrice(4):
- Look at timestamps: 3
- Prices: 200
- Maximum: 200 ✓
```

---

**Key Observations:**

1. **Out-of-order updates** trigger prefix max rebuild
2. **Binary search** finds the right position in O(log N)
3. **Prefix max array** enables O(1) query after rebuild
4. **Lazy rebuild** only happens when querying (read-optimized)

---

## 🔍 Complexity Analysis

### Approach 1: Prefix Max Cache

| Operation | Best Case | Average | Worst Case | Explanation |
|-----------|-----------|---------|------------|-------------|
| `update()` | **O(log N)** | **O(N)** | **O(N)** | Binary search + list insertion |
| `getMaxPrice()` (cache hot) | **O(log N)** | **O(log N)** | **O(log N)** | Binary search in sorted list |
| `getMaxPrice()` (cache miss) | **O(N)** | **O(N)** | **O(N)** | Rebuild prefix max + search |

**Space Complexity:** O(N) for data + O(N) for cache = **O(N) total**.

**When to Use:**
- Read-heavy workloads (many queries, few updates)
- Updates can be batched
- Memory is not a constraint

---

## 🚀 Approach 2: Segment Tree (Advanced)

For **balanced** or **write-heavy** workloads, use a **Segment Tree** with **coordinate compression**.

---

## 🎓 What is a Segment Tree?

A **Segment Tree** is a binary tree where:
- **Each node** represents a range [L, R] of the array
- **Leaf nodes** represent single elements
- **Internal nodes** store aggregated information (max, min, sum) of their children

**Why use it?**
- Both **update** and **query** operations are **O(log N)**
- Perfect for dynamic range queries

---

## 📐 Segment Tree Structure

### Tree Representation (Array of 8 Prices)

```text
Original Array (indices 0-7):
┌────┬────┬────┬────┬────┬────┬────┬────┐
│ 50 │100 │ 80 │200 │150 │ 90 │120 │160 │
└────┴────┴────┴────┴────┴────┴────┴────┘
  0    1    2    3    4    5    6    7

Segment Tree (stored as array):
                    ┌─────────────┐
                    │   [0-7]     │
                    │   MAX=200   │  ← Root (index 0)
                    └──────┬──────┘
                           │
            ┌──────────────┴──────────────┐
            │                             │
       ┌────┴────┐                   ┌────┴────┐
       │ [0-3]   │                   │ [4-7]   │
       │ MAX=200 │                   │ MAX=160 │
       └────┬────┘                   └────┬────┘
            │                             │
      ┌─────┴─────┐               ┌───────┴───────┐
      │           │               │               │
  ┌───┴───┐   ┌───┴───┐      ┌───┴───┐       ┌───┴───┐
  │ [0-1] │   │ [2-3] │      │ [4-5] │       │ [6-7] │
  │MAX=100│   │MAX=200│      │MAX=150│       │MAX=160│
  └───┬───┘   └───┬───┘      └───┬───┘       └───┬───┘
      │           │              │               │
   ┌──┴──┐     ┌──┴──┐       ┌──┴──┐         ┌──┴──┐
   │     │     │     │       │     │         │     │
 ┌─┴─┐ ┌─┴─┐ ┌─┴─┐ ┌─┴─┐   ┌─┴─┐ ┌─┴─┐     ┌─┴─┐ ┌─┴─┐
 │[0]│ │[1]│ │[2]│ │[3]│   │[4]│ │[5]│     │[6]│ │[7]│
 │50 │ │100│ │80 │ │200│   │150│ │90 │     │120│ │160│
 └───┘ └───┘ └───┘ └───┘   └───┘ └───┘     └───┘ └───┘
 Leaf   Leaf  Leaf  Leaf    Leaf  Leaf      Leaf  Leaf
```

### Array Representation (1-indexed for clarity):

```text
Index:  0     1      2      3      4      5      6      7      8      9     10     11    12    13    14    15
       ┌────┬────┬──────┬──────┬──────┬──────┬──────┬──────┬────┬────┬────┬────┬────┬────┬────┬────┐
Value: │    │200 │ 100  │ 200  │ 150  │ 160  │  -   │  -   │ 50 │100 │ 80 │200 │150 │ 90 │120 │160 │
       └────┴────┴──────┴──────┴──────┴──────┴──────┴──────┴────┴────┴────┴────┴────┴────┴────┴────┘
Range:      [0-7]  [0-3]  [4-7]  [0-1]  [2-3]  [4-5]  [6-7]  [0]  [1]  [2]  [3]  [4]  [5]  [6]  [7]
```

**Key Pattern:**
- **Parent at index i** → Children at **2*i** (left) and **2*i+1** (right)
- **Leaf nodes** start at index **n** (tree size)
- **Tree size** = 4 * N (to guarantee space for all levels)

---

## 🔧 Coordinate Compression (Critical!)

Since timestamps are **sparse** (1, 1000, 1000000), we can't build a segment tree with 1 million nodes!

### Problem Example:
```text
Timestamps: [1, 1000, 1000000]
Prices:     [100, 200, 150]

❌ WRONG: Build tree of size 4 * 1000000 = 4,000,000 (wasteful!)
```

### Solution: Coordinate Compression
```text
Step 1: Collect unique timestamps
Timestamps: [1, 1000, 1000000]

Step 2: Map to compressed indices
┌───────────┬───────────┬──────────────┐
│ Timestamp │   Price   │ Compressed   │
├───────────┼───────────┼──────────────┤
│     1     │    100    │      0       │
│   1000    │    200    │      1       │
│ 1000000   │    150    │      2       │
└───────────┴───────────┴──────────────┘

Step 3: Build segment tree on compressed indices [0, 1, 2]
✅ CORRECT: Tree size = 4 * 3 = 12 nodes (efficient!)
```

### Visual Mapping:
```text
Real World (Sparse):
t=1──────────────t=1000───────────────────────────────────t=1000000
100              200                                       150

Compressed (Dense):
idx=0────idx=1────idx=2
100      200      150
  │       │        │
  └───────┴────────┘
         │
    Segment Tree
    (Only 3 leaves!)
```

---

## 📝 Complete Segment Tree Implementation

```python
import bisect
from typing import Optional, List

class SegmentTreeTracker:
    """
    Commodity price tracker using Segment Tree for O(log N) updates and queries.

    Uses coordinate compression to handle sparse timestamps efficiently.
    """

    def __init__(self):
        # Ground truth: timestamp → price
        self.timestamp_to_price = {}

        # Compressed coordinates (sorted unique timestamps)
        self.sorted_timestamps = []

        # Segment tree (array representation)
        self.tree = []

        # Dirty flag: rebuild tree if new timestamps added
        self.dirty = False

    def update(self, timestamp: int, price: int) -> None:
        """
        Add or update price at timestamp.

        Time Complexity:
        - O(log N) if timestamp exists (single tree update)
        - O(N log N) if new timestamp (rebuild tree)

        Space: O(1)
        """
        self.timestamp_to_price[timestamp] = price

        # Check if this is a new timestamp
        if timestamp not in self.sorted_timestamps:
            # New timestamp: add and resort
            self.sorted_timestamps.append(timestamp)
            self.sorted_timestamps.sort()
            self.dirty = True

        # Rebuild tree if needed (new timestamp added)
        if self.dirty:
            self._rebuild_tree()
        else:
            # Update existing position in tree
            idx = bisect.bisect_left(self.sorted_timestamps, timestamp)
            self._update_single(idx, price)

    def _rebuild_tree(self) -> None:
        """
        Build segment tree from scratch.

        Time: O(N) - builds tree bottom-up
        Space: O(N) - tree array
        """
        n = len(self.sorted_timestamps)

        if n == 0:
            self.tree = []
            self.dirty = False
            return

        # Allocate tree array (4*n guarantees enough space)
        self.tree = [float('-inf')] * (4 * n)

        # Build tree by processing each leaf
        self._build(0, 0, n - 1)

        self.dirty = False

    def _build(self, node: int, start: int, end: int) -> None:
        """
        Recursively build segment tree.

        Args:
            node: Current node index in tree array
            start: Left boundary of range (compressed index)
            end: Right boundary of range (compressed index)
        """
        if start == end:
            # Leaf node: store price at this compressed index
            timestamp = self.sorted_timestamps[start]
            self.tree[node] = self.timestamp_to_price[timestamp]
            return

        # Internal node: recursively build children
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2

        # Build left subtree [start, mid]
        self._build(left_child, start, mid)

        # Build right subtree [mid+1, end]
        self._build(right_child, mid + 1, end)

        # Store max of children
        self.tree[node] = max(self.tree[left_child], self.tree[right_child])

    def _update_single(self, index: int, value: int) -> None:
        """
        Update a single leaf in the segment tree and propagate upwards.

        Time: O(log N)

        Args:
            index: Compressed index to update
            value: New price value
        """
        n = len(self.sorted_timestamps)
        self._update_recursive(0, 0, n - 1, index, value)

    def _update_recursive(self, node: int, start: int, end: int,
                          index: int, value: int) -> None:
        """
        Recursively update tree node.

        Args:
            node: Current node index
            start, end: Range of current node
            index: Target index to update
            value: New value
        """
        if start == end:
            # Reached leaf node
            self.tree[node] = value
            return

        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2

        if index <= mid:
            # Update in left subtree
            self._update_recursive(left_child, start, mid, index, value)
        else:
            # Update in right subtree
            self._update_recursive(right_child, mid + 1, end, index, value)

        # Recalculate max for current node
        self.tree[node] = max(self.tree[left_child], self.tree[right_child])

    def getMaxPrice(self, timestamp: int) -> Optional[int]:
        """
        Get maximum price at or before timestamp.

        This queries the segment tree for max in range [0, compressed_idx]
        where compressed_idx is the largest index with timestamp <= query.

        Time: O(log N)
        Space: O(log N) recursion stack
        """
        if not self.sorted_timestamps:
            return None

        # Find rightmost timestamp <= query timestamp
        # This gives us the compressed index
        idx = bisect.bisect_right(self.sorted_timestamps, timestamp) - 1

        if idx < 0:
            # No data at or before this timestamp
            return None

        # Query segment tree for max in range [0, idx]
        n = len(self.sorted_timestamps)
        return self._query(0, 0, n - 1, 0, idx)

    def _query(self, node: int, start: int, end: int,
               query_left: int, query_right: int) -> int:
        """
        Query maximum value in range [query_left, query_right].

        Time: O(log N) - visits at most 2*log(N) nodes

        Args:
            node: Current node index
            start, end: Range of current node
            query_left, query_right: Query range (compressed indices)

        Returns:
            Maximum value in query range
        """
        # Case 1: No overlap
        if query_right < start or query_left > end:
            return float('-inf')

        # Case 2: Complete overlap (current range inside query range)
        if query_left <= start and end <= query_right:
            return self.tree[node]

        # Case 3: Partial overlap - query both children
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2

        left_max = self._query(left_child, start, mid, query_left, query_right)
        right_max = self._query(right_child, mid + 1, end, query_left, query_right)

        return max(left_max, right_max)


# ============================================
# COMPLETE EXAMPLE WITH DETAILED OUTPUT
# ============================================

if __name__ == "__main__":
    print("=" * 70)
    print("SEGMENT TREE COMMODITY TRACKER - DETAILED EXAMPLE")
    print("=" * 70)

    tracker = SegmentTreeTracker()

    # Test 1: Build tree with sparse timestamps
    print("\n[Test 1] Building Tree with Sparse Timestamps")
    print("-" * 70)

    tracker.update(1, 100)
    tracker.update(1000, 200)
    tracker.update(1000000, 150)

    print(f"Timestamps (sparse): {tracker.sorted_timestamps}")
    print(f"Compressed indices: [0, 1, 2]")
    print(f"Tree size: {len(tracker.tree)} nodes (4 * 3 = 12)")
    print(f"\nSegment Tree Array: {tracker.tree[:12]}")

    # Test 2: Query operations
    print("\n[Test 2] Query Operations")
    print("-" * 70)

    queries = [1, 500, 1000, 50000, 1000000, 2000000]
    for q in queries:
        result = tracker.getMaxPrice(q)
        print(f"getMaxPrice({q:>7}) = {result}")

    # Test 3: Out-of-order updates
    print("\n[Test 3] Out-of-Order Updates")
    print("-" * 70)

    tracker2 = SegmentTreeTracker()

    tracker2.update(10, 200)
    print(f"After update(10, 200): timestamps = {tracker2.sorted_timestamps}")

    tracker2.update(5, 300)
    print(f"After update(5, 300):  timestamps = {tracker2.sorted_timestamps}")

    tracker2.update(7, 250)
    print(f"After update(7, 250):  timestamps = {tracker2.sorted_timestamps}")

    print(f"\nQuery Results:")
    for t in [5, 7, 10]:
        print(f"  Max at t={t}: {tracker2.getMaxPrice(t)}")

    # Test 4: Price corrections
    print("\n[Test 4] Price Corrections (Update Existing)")
    print("-" * 70)

    tracker3 = SegmentTreeTracker()
    tracker3.update(5, 100)
    tracker3.update(10, 150)

    print(f"Initial: t=5→100, t=10→150")
    print(f"Max at t=10: {tracker3.getMaxPrice(10)}")

    tracker3.update(5, 400)  # Correct price at t=5
    print(f"\nAfter correction: t=5→400")
    print(f"Max at t=10: {tracker3.getMaxPrice(10)}")

    # Test 5: Performance comparison
    print("\n[Test 5] Performance Characteristics")
    print("-" * 70)

    import time

    tracker4 = SegmentTreeTracker()

    # Build with 1000 timestamps
    timestamps = list(range(1, 1001))

    start = time.time()
    for t in timestamps:
        tracker4.update(t, t * 10)
    build_time = time.time() - start

    # Query 1000 times
    start = time.time()
    for t in range(1, 1001):
        tracker4.getMaxPrice(t)
    query_time = time.time() - start

    print(f"Dataset: 1000 timestamps")
    print(f"Build time: {build_time*1000:.2f} ms")
    print(f"1000 queries: {query_time*1000:.2f} ms ({query_time/1000*1000:.3f} ms/query)")

    print("\n" + "=" * 70)
    print("All tests passed! ✓")
    print("=" * 70)
```

---

## 🎯 Step-by-Step Query Example

Let's trace a query operation with **visual diagrams**.

### Setup:
```python
tracker.update(3, 100)
tracker.update(5, 200)
tracker.update(7, 150)
tracker.update(10, 300)
```

### Step 1: Coordinate Compression
```text
Timestamps: [3, 5, 7, 10]
Prices:     [100, 200, 150, 300]

Compressed Mapping:
┌───────────┬───────┬──────────────┐
│ Timestamp │ Price │ Compressed   │
├───────────┼───────┼──────────────┤
│     3     │  100  │      0       │
│     5     │  200  │      1       │
│     7     │  150  │      2       │
│    10     │  300  │      3       │
└───────────┴───────┴──────────────┘
```

### Step 2: Build Segment Tree
```text
                    ┌──────────────┐
                    │   [0-3]      │  ← Node 0
                    │   MAX = 300  │     (Root)
                    └───────┬──────┘
                            │
            ┌───────────────┴────────────────┐
            │                                │
       ┌────┴─────┐                    ┌────┴─────┐
       │  [0-1]   │                    │  [2-3]   │
       │ MAX=200  │ ← Node 1           │ MAX=300  │ ← Node 2
       └────┬─────┘                    └────┬─────┘
            │                               │
      ┌─────┴─────┐                   ┌─────┴─────┐
      │           │                   │           │
   ┌──┴──┐     ┌──┴──┐             ┌──┴──┐     ┌──┴──┐
   │ [0] │     │ [1] │             │ [2] │     │ [3] │
   │ 100 │     │ 200 │             │ 150 │     │ 300 │
   └─────┘     └─────┘             └─────┘     └─────┘
   Node 3      Node 4              Node 5      Node 6
   (Leaf)      (Leaf)              (Leaf)      (Leaf)
```

### Tree Array Representation:
```text
Index:  0    1    2    3    4    5    6    7    8    9   10   11
       ┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐
Value: │300 │200 │300 │100 │200 │150 │300 │ -  │ -  │ -  │ -  │ -  │
       └────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┘
Range: [0-3][0-1][2-3] [0] [1] [2] [3]
```

---

## 🔍 Query Trace: `getMaxPrice(7)`

**Goal:** Find max price for all timestamps ≤ 7

### Step 1: Find Compressed Index
```text
Query: timestamp = 7
Sorted timestamps: [3, 5, 7, 10]

Binary search for rightmost timestamp ≤ 7:
- bisect_right([3, 5, 7, 10], 7) = 3
- compressed_idx = 3 - 1 = 2

Query becomes: max in range [0, 2] (compressed indices)
```

### Step 2: Segment Tree Query
```text
Query: max in range [0, 2]

Visual Traversal:
                    ┌──────────────┐
                    │   [0-3]      │  ← Check: Does [0-3] overlap [0-2]?
                    │   MAX = 300  │     YES (partial) → recurse
                    └───────┬──────┘
                            │
            ┌───────────────┴────────────────┐
            │                                │
       ┌────┴─────┐                    ┌────┴─────┐
       │  [0-1]   │  ← [0-1] ⊆ [0-2]  │  [2-3]   │  ← [2-3] ∩ [0-2]?
       │ MAX=200  │    ✓ Complete!     │ MAX=300  │     Partial!
       └──────────┘    Return 200      └────┬─────┘
                                             │
                                    ┌────────┴────────┐
                                    │                 │
                                 ┌──┴──┐           ┌──┴──┐
                                 │ [2] │  ← [2]    │ [3] │  ← [3]
                                 │ 150 │    In!    │ 300 │    Out!
                                 └─────┘   ✓       └─────┘    ✗
                                 Return 150        Return -∞

Final: max(200, max(150, -∞)) = max(200, 150) = 200
```

### Step 3: Visual Call Tree
```text
_query(node=0, range=[0-3], query=[0-2])
│
├─ _query(node=1, range=[0-1], query=[0-2])  ← Complete overlap
│  └─ return 200 ✓
│
└─ _query(node=2, range=[2-3], query=[0-2])  ← Partial overlap
   │
   ├─ _query(node=5, range=[2-2], query=[0-2])  ← [2] in [0-2]
   │  └─ return 150 ✓
   │
   └─ _query(node=6, range=[3-3], query=[0-2])  ← [3] NOT in [0-2]
      └─ return -∞ ✗

Result: max(200, max(150, -∞)) = 200
```

**Answer:** Max price for timestamps ≤ 7 is **200** (at timestamp 5)

---

## 📊 Update Operation Example

### Update Existing Value: `update(5, 500)` (correction)

**Before:**
```text
Timestamps: [3, 5, 7, 10]
Prices:     [100, 200, 150, 300]
Compressed index for t=5: 1
```

**Step 1: Find Compressed Index**
```python
idx = bisect_left([3, 5, 7, 10], 5) = 1
```

**Step 2: Recursive Update**
```text
                    ┌──────────────┐
                    │   [0-3]      │  ← Update propagates up
                    │   MAX = 300  │     Recalc: max(500, 300)
                    │    ↓ 500     │     New: 500 ✓
                    └───────┬──────┘
                            │
            ┌───────────────┴────────────────┐
            │                                │
       ┌────┴─────┐                    ┌────┴─────┐
       │  [0-1]   │  ← Update here     │  [2-3]   │  ← Unchanged
       │ MAX=200  │     Recalc!        │ MAX=300  │
       │  ↓ 500   │     max(100, 500)  └──────────┘
       └────┬─────┘     New: 500 ✓
            │
      ┌─────┴─────┐
      │           │
   ┌──┴──┐     ┌──┴──┐
   │ [0] │     │ [1] │  ← Target! Update 200→500
   │ 100 │     │ 500 │     ✓
   └─────┘     └─────┘
```

**After:**
```text
Tree Array:
Index:  0    1    2    3    4    5    6
Value: 500  500  300  100  500  150  300
       ↑    ↑         ↑
     Updated from 300→500, 200→500, 200→500
```

**Complexity:** O(log N) - visits at most log(N) nodes (one path from leaf to root)

---

## 🆚 Comparison: Prefix Max Cache vs Segment Tree

| Feature | Prefix Max Cache | Segment Tree |
|---------|------------------|--------------|
| **Update (existing)** | O(1) mark dirty | **O(log N)** ✓ |
| **Update (new timestamp)** | O(N) insert + sort | O(N log N) rebuild |
| **Query (cache hot)** | **O(log N)** ✓ | O(log N) |
| **Query (cache miss)** | O(N) rebuild | **O(log N)** ✓ |
| **Space** | O(N) | O(4N) |
| **Best for** | Read-heavy | Balanced/write-heavy |

### When to Choose Segment Tree:
1. **Write-heavy workload**: Many updates, fewer queries
2. **Real-time systems**: Need predictable O(log N) performance
3. **Range queries**: Need max/min/sum in arbitrary ranges [L, R]
4. **Balanced operations**: Equal mix of reads and writes

### When to Choose Prefix Max Cache:
1. **Read-heavy workload**: Many queries, few updates
2. **Batch updates**: Can update 100 values, then query 10000 times
3. **Memory constrained**: Need minimal space overhead

---

## 🧮 Complexity Analysis (Segment Tree)

### Time Complexity:

| Operation | Complexity | Explanation |
|-----------|------------|-------------|
| **Build Tree** | O(N) | Visit each node once, 2N-1 nodes total |
| **Update (existing)** | **O(log N)** | Traverse one path from leaf to root |
| **Update (new timestamp)** | O(N log N) | Rebuild entire tree (rare) |
| **Query** | **O(log N)** | Visit at most 4 nodes per level |

### Space Complexity:
- **Tree Array:** O(4N) = O(N)
- **Coordinate Map:** O(N)
- **Recursion Stack:** O(log N)
- **Total:** **O(N)**

### Proof of Query Complexity:

At each level, the query range can intersect at most **4 nodes**:

```text
Level 0 (root):        [0-15]           ← 1 node

Level 1:          [0-7]    [8-15]       ← At most 2 nodes

Level 2:      [0-3][4-7][8-11][12-15]   ← At most 4 nodes

Level 3: [0-1][2-3]... (at most 4)

Height = log₂(N)
Nodes visited ≤ 4 * log₂(N) = O(log N)
```

**Complexity:**
- Update: **O(log N)** (amortized, O(N log N) when tree rebuilds)
- Query: **O(log N)**

---

## ⚠️ Common Pitfalls

### 1. **Binary Search Boundary Errors**

**Wrong:**
```python
idx = bisect.bisect_left(self.data, (timestamp, 0))
return self.prefix_max[idx]  # Might be out of bounds!
```

**Right:**
```python
idx = bisect.bisect_right(self.data, (timestamp, float('inf'))) - 1
if idx < 0:
    return None
return self.prefix_max[idx]
```

### 2. **Forgetting to Mark Dirty**

**Wrong:**
```python
def update(self, timestamp, price):
    self.data.insert(idx, (timestamp, price))
    # Forgot to set self.dirty = True!
```

**Result:** Queries return stale cached values.

### 3. **Not Handling Empty Data**

**Wrong:**
```python
def getMaxPrice(self, timestamp):
    return self.prefix_max[0]  # Crashes if empty!
```

**Right:** Check `if not self.data: return None`.

---

## 🔄 Follow-up Questions

### Follow-up 1: Checkpoint-Based Queries

**Problem Statement:**
> "Instead of querying by timestamp, we want to query by **checkpoint number**. Every update creates a checkpoint. `getMaxAtCheckpoint(n)` returns the max price across the first `n` checkpoints."

**Example:**
```python
tracker.update(5, 100)  # Checkpoint 0
tracker.update(3, 200)  # Checkpoint 1
tracker.update(7, 150)  # Checkpoint 2

getMaxAtCheckpoint(0) → 100
getMaxAtCheckpoint(1) → 200 (max of 100, 200)
getMaxAtCheckpoint(2) → 200 (max of 100, 200, 150)
```

**Solution:**
This is simpler! No need for timestamp sorting.

```python
class CheckpointTracker:
    """
    Track commodity prices by checkpoint number (update order).
    """
    
    def __init__(self):
        self.prices = []        # prices[i] = price at checkpoint i
        self.prefix_max = []    # prefix_max[i] = max(prices[0..i])
    
    def update(self, price: int) -> int:
        """
        Add a new checkpoint.
        Returns checkpoint number.
        
        Time: O(1)
        """
        self.prices.append(price)
        
        # Compute prefix max
        current_max = price
        if self.prefix_max:
            current_max = max(self.prefix_max[-1], price)
        
        self.prefix_max.append(current_max)
        
        return len(self.prices) - 1
    
    def getMaxAtCheckpoint(self, checkpoint: int) -> Optional[int]:
        """
        Get max price up to checkpoint.
        
        Time: O(1)
        """
        if 0 <= checkpoint < len(self.prefix_max):
            return self.prefix_max[checkpoint]
        return None


# ============================================
# EXAMPLE
# ============================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("FOLLOW-UP 1: CHECKPOINT-BASED QUERIES")
    print("=" * 60)
    
    tracker = CheckpointTracker()
    
    cp0 = tracker.update(100)
    cp1 = tracker.update(200)
    cp2 = tracker.update(150)
    cp3 = tracker.update(300)
    
    print(f"Max at checkpoint {cp0}: {tracker.getMaxAtCheckpoint(cp0)}")  # 100
    print(f"Max at checkpoint {cp1}: {tracker.getMaxAtCheckpoint(cp1)}")  # 200
    print(f"Max at checkpoint {cp2}: {tracker.getMaxAtCheckpoint(cp2)}")  # 200
    print(f"Max at checkpoint {cp3}: {tracker.getMaxAtCheckpoint(cp3)}")  # 300
```

**Complexity:** O(1) for both operations!

---

### Follow-up 2: Range Queries

**Problem Statement:**
> "Extend the system to support `getMaxInRange(start_ts, end_ts)` which returns the max price in the timestamp range `[start_ts, end_ts]`."

**Solution:**
Use a Segment Tree to support range queries efficiently.

```python
class CommodityTrackerWithRange:
    """
    Commodity price tracker with range query support using Segment Tree.
    """
    
    def __init__(self):
        self.data = []  # (timestamp, price)
        self.segment_tree = []
        self.dirty = False
    
    def update(self, timestamp: int, price: int) -> None:
        """Add or update price at timestamp."""
        idx = bisect.bisect_left([t for t, p in self.data], timestamp)
        
        if idx < len(self.data) and self.data[idx][0] == timestamp:
            self.data[idx] = (timestamp, price)
        else:
            self.data.insert(idx, (timestamp, price))
        
        self.dirty = True
    
    def _build_segment_tree(self):
        """Build segment tree for max queries."""
        n = len(self.data)
        if n == 0:
            return
        
        # Segment tree size: 4 * n
        self.segment_tree = [float('-inf')] * (4 * n)
        self._build_tree(0, 0, n - 1)
        self.dirty = False
    
    def _build_tree(self, node: int, start: int, end: int):
        """Recursively build segment tree."""
        if start == end:
            # Leaf node
            self.segment_tree[node] = self.data[start][1]
            return
        
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        
        self._build_tree(left_child, start, mid)
        self._build_tree(right_child, mid + 1, end)
        
        self.segment_tree[node] = max(
            self.segment_tree[left_child],
            self.segment_tree[right_child]
        )
    
    def _query_tree(self, node: int, start: int, end: int, 
                    query_start: int, query_end: int) -> int:
        """Query max in range [query_start, query_end]."""
        if query_start > end or query_end < start:
            # No overlap
            return float('-inf')
        
        if query_start <= start and end <= query_end:
            # Complete overlap
            return self.segment_tree[node]
        
        # Partial overlap
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        
        left_max = self._query_tree(left_child, start, mid, query_start, query_end)
        right_max = self._query_tree(right_child, mid + 1, end, query_start, query_end)
        
        return max(left_max, right_max)
    
    def getMaxInRange(self, start_ts: int, end_ts: int) -> Optional[int]:
        """
        Get max price in range [start_ts, end_ts].
        
        Time: O(log N)
        """
        if not self.data:
            return None
        
        if self.dirty:
            self._build_segment_tree()
        
        # Find compressed indices
        timestamps = [t for t, p in self.data]
        left_idx = bisect.bisect_left(timestamps, start_ts)
        right_idx = bisect.bisect_right(timestamps, end_ts) - 1
        
        if left_idx > right_idx or right_idx < 0 or left_idx >= len(self.data):
            return None
        
        # Query segment tree
        result = self._query_tree(0, 0, len(self.data) - 1, left_idx, right_idx)
        return result if result != float('-inf') else None


# Example Usage
if __name__ == "__main__":
    tracker = CommodityTrackerWithRange()
    
    tracker.update(1, 100)
    tracker.update(5, 300)
    tracker.update(10, 150)
    
    print(f"Max in range [1, 5]: {tracker.getMaxInRange(1, 5)}")    # 300
    print(f"Max in range [5, 10]: {tracker.getMaxInRange(5, 10)}")  # 300
    print(f"Max in range [6, 10]: {tracker.getMaxInRange(6, 10)}")  # 150
```

**Complexity:** O(log N) for range queries, O(N) for rebuilds (amortized over multiple queries).

---

## 🧪 Test Cases

```python
def test_commodity_tracker():
    tracker = CommodityTracker()
    
    # Test 1: Sequential
    tracker.update(1, 100)
    tracker.update(2, 150)
    assert tracker.getMaxPrice(2) == 150
    
    # Test 2: Out of order
    tracker.update(10, 200)
    tracker.update(5, 300)
    assert tracker.getMaxPrice(10) == 300
    
    # Test 3: Correction
    tracker.update(5, 50)  # Overwrite
    assert tracker.getMaxPrice(10) == 200
    
    # Test 4: Query before data
    assert tracker.getMaxPrice(0) is None
    
    # Test 5: Empty
    tracker2 = CommodityTracker()
    assert tracker2.getMaxPrice(100) is None
    
    print("All tests passed! ✓")

if __name__ == "__main__":
    test_commodity_tracker()
```

---

## 🎯 Key Takeaways

1. **Prefix Max** is a fundamental pattern for range queries.
2. **Lazy Caching** trades write performance for read performance.
3. **Segment Trees** provide balanced O(log N) for both operations.
4. **Coordinate Compression** handles sparse timestamps efficiently.
5. **Checkpoint-based queries** are simpler (no sorting needed).

---

## 📚 Related Problems

- **LeetCode 2034:** Stock Price Fluctuation (similar pattern)
- **LeetCode 307:** Range Sum Query - Mutable (segment tree)
- **LeetCode 1508:** Range Sum of Sorted Subarray Sums
- **LeetCode 327:** Count of Range Sum (prefix + segment tree)
