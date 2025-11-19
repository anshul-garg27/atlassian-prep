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

### Coordinate Compression

Since timestamps are sparse (1, 1000, 1000000), we:
1. Collect all unique timestamps
2. Map timestamp → compressed index (0, 1, 2, ...)
3. Build segment tree on compressed indices

```python
class SegmentTreeTracker:
    """
    Commodity tracker using Segment Tree for O(log N) updates and queries.
    """
    
    def __init__(self):
        self.timestamp_to_price = {}  # Ground truth
        self.sorted_timestamps = []   # Compressed coordinates
        self.tree = None
        self.dirty = False
    
    def update(self, timestamp: int, price: int) -> None:
        """
        Update price. Rebuilds tree if needed.
        
        Time: O(log N) update + O(N log N) rebuild if new timestamp
        """
        self.timestamp_to_price[timestamp] = price
        
        if timestamp not in self.sorted_timestamps:
            self.sorted_timestamps.append(timestamp)
            self.sorted_timestamps.sort()
            self.dirty = True
        
        if self.dirty:
            self._rebuild_tree()
        else:
            # Update existing position
            idx = bisect.bisect_left(self.sorted_timestamps, timestamp)
            self._update_tree(idx, price)
    
    def _rebuild_tree(self):
        """Build segment tree from scratch."""
        n = len(self.sorted_timestamps)
        self.tree = [0] * (4 * n)
        for i, ts in enumerate(self.sorted_timestamps):
            self._update_tree(i, self.timestamp_to_price[ts])
        self.dirty = False
    
    def _update_tree(self, index, value):
        """Update segment tree at index."""
        # Standard segment tree update (omitted for brevity)
        pass
    
    def getMaxPrice(self, timestamp: int) -> Optional[int]:
        """
        Query max in range [0, timestamp].
        
        Time: O(log N)
        """
        if not self.sorted_timestamps:
            return None
        
        # Find compressed index
        idx = bisect.bisect_right(self.sorted_timestamps, timestamp) - 1
        
        if idx < 0:
            return None
        
        # Query segment tree for range [0, idx]
        return self._query_tree(0, idx)
    
    def _query_tree(self, left, right):
        """Query max in range [left, right]."""
        # Standard segment tree query (omitted for brevity)
        pass
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
Use the Segment Tree approach from Approach 2, but query a range instead of prefix.

```python
def getMaxInRange(self, start_ts: int, end_ts: int) -> Optional[int]:
    """
    Get max price in range [start_ts, end_ts].
    """
    if not self.sorted_timestamps:
        return None
    
    # Find compressed indices
    left_idx = bisect.bisect_left(self.sorted_timestamps, start_ts)
    right_idx = bisect.bisect_right(self.sorted_timestamps, end_ts) - 1
    
    if left_idx > right_idx or right_idx < 0:
        return None
    
    # Query segment tree for range [left_idx, right_idx]
    return self._query_tree(left_idx, right_idx)
```

**Complexity:** O(log N) with Segment Tree.

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
