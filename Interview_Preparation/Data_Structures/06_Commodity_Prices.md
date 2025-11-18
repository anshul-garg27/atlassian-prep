# 🎲 PROBLEM 6: COMMODITY PRICES WITH CHECKPOINTS

### ⭐⭐ **Commodity Price Tracker**

**Frequency:** Low
**Similar to:** Range Maximum Query (RMQ) problems.

**Problem Statement:**
> You receive a stream of commodity price updates: `(timestamp, price)`.
> The stream is not sorted. You might get updates for past timestamps.
>
> Implement:
> - `update(timestamp, price)`: Record/Update price.
> - `getMaxPrice(timestamp)`: Return the maximum price recorded at any time `t <= timestamp`.

**Visual Example:**
```text
Events:
1. (t=1, p=100)
2. (t=3, p=150)
3. (t=2, p=120)  <-- Out of order

Data: {1: 100, 2: 120, 3: 150}

Queries:
getMaxPrice(1) -> 100
getMaxPrice(2) -> 120 (Max of prices at 1, 2)
getMaxPrice(3) -> 150 (Max of prices at 1, 2, 3)
```

---

### 🗣️ **Interview Conversation Guide**

**Phase 1: Clarification**
- **Candidate:** "Is `timestamp` always increasing in `update`?"
- **Interviewer:** "No, it can be out of order (corrections)."
- **Candidate:** "Is `timestamp` continuous or sparse?"
- **Interviewer:** "Sparse (e.g., 1, 5, 1000)."
- **Candidate:** "Is read or write more frequent?"
- **Interviewer:** "Assume relatively balanced, or slightly more reads."

**Phase 2: Approach**
- **Candidate:** "We need to store prices by timestamp. A Hash Map works for storage."
- **Candidate:** "However, `getMaxPrice(t)` asks for max in range `[0, t]`. Hash Map doesn't support range queries efficiently."
- **Candidate:** "We could use a **Sorted List** of `(timestamp, price)`."
- **Candidate:** "For `getMaxPrice(t)`, we find all entries $\le t$. But scanning them is $O(N)$."
- **Candidate:** "We can cache the **Prefix Max**. `prefix_max[i] = max(data[0]...data[i])`. Then binary search is $O(\log N)$."
- **Candidate:** "Challenge: An update to a past timestamp invalidates all subsequent prefix maxes ($O(N)$ update)."

**Phase 3: Coding**
- Implement the pragmatic `SortedList` + `Lazy Prefix Max` approach (good for interviews unless Segment Tree is explicitly asked).

---

### 📝 **Solution Approach 1: SortedDict + Prefix Max Cache**

If we assume read-heavy workload, we can maintain a cached "Prefix Max".
However, updates are expensive (O(N)) if we change a past value, as it invalidates all subsequent prefix maxes.

**Better for Interview (Balanced):**
Use a **Segment Tree** (Coordinate Compression if timestamps are large) OR a **SortedDict** combined with smart caching.

Since implementation of a Segment Tree is heavy, here is a pragmatic approach using **SortedDict** (bisect in Python) for data storage and a simple **Memoization** or **Heap** strategy if specific constraints are given.

**If simply "Max price ever":** O(1) variable.
**If "Max price in range [0, t]":** This is a Prefix Max problem.

**Python Solution (Bisect + Lazy Prefix Max)**
*Note: Efficient dynamic RMQ is hard without a Segment Tree. This solution assumes we might recompute or the data is relatively sparse.*

```python
import bisect

class CommodityTracker:
    def __init__(self):
        # List of [timestamp, price] sorted by timestamp
        self.data = [] 
        # Cache for prefix max: index -> max_price_in_data[:index+1]
        self.prefix_max = []
        self.is_dirty = False

    def update(self, timestamp: int, price: int) -> None:
        # O(N) insertion to keep sorted
        # In interview, can discuss using Balanced BST (O(log N))
        
        # Check if exists
        idx = bisect.bisect_left(self.data, [timestamp, -1])
        
        if idx < len(self.data) and self.data[idx][0] == timestamp:
            self.data[idx][1] = price
        else:
            bisect.insort(self.data, [timestamp, price])
            
        self.is_dirty = True

    def _rebuild_prefix_max(self):
        # O(N) - acceptable if reads >> writes
        if not self.data:
            return
            
        self.prefix_max = [0] * len(self.data)
        curr_max = float('-inf')
        
        for i, (ts, price) in enumerate(self.data):
            curr_max = max(curr_max, price)
            self.prefix_max[i] = curr_max
            
        self.is_dirty = False

    def getMaxPrice(self, timestamp: int) -> int:
        if self.is_dirty:
            self._rebuild_prefix_max()
            
        if not self.data:
            return None
            
        # Find rightmost index <= timestamp
        # bisect_right searches based on the first element of list comparison
        # We use a dummy [timestamp, INF] to find the upper bound
        idx = bisect.bisect_right(self.data, [timestamp, float('inf')])
        
        if idx == 0:
            return None
            
        return self.prefix_max[idx - 1]

# Time: Update O(N), Query O(log N) + O(N) rebuild if dirty.
```

---

### 🚀 **Optimal Solution: Segment Tree**

If `update` and `query` must both be **O(log N)**, you must use a **Segment Tree**.

1.  **Coordinate Compression**: If timestamps are large (e.g., unix timestamps), map them to indices 0..N based on sorted unique timestamps seen.
2.  **Segment Tree**: Stores max in range.

```python
class SegmentTree:
    def __init__(self, size):
        self.n = size
        self.tree = [0] * (2 * size)

    def update(self, i, val):
        i += self.n
        self.tree[i] = val
        while i > 1:
            i //= 2
            self.tree[i] = max(self.tree[2*i], self.tree[2*i+1])

    def query(self, l, r):
        # Max in range [l, r)
        l += self.n
        r += self.n
        res = 0
        while l < r:
            if l % 2 == 1:
                res = max(res, self.tree[l])
                l += 1
            if r % 2 == 1:
                r -= 1
                res = max(res, self.tree[r])
            l //= 2
            r //= 2
        return res
```

---

### 🔖 **Follow-up: Checkpoints**

**Problem:**
> Every `k` updates, we drop a "checkpoint". We want to find the max price *relative to* checkpoint numbers, not timestamps.

**Solution:**
> This simplifies to an array problem.
> Store checkpoints in a list: `[(ts1, p1), (ts2, p2), ...]`.
> Maintain a `max_so_far` array aligned with this list.
> Querying by "checkpoint number" is just array indexing `O(1)`.

```python
class CheckpointTracker:
    def __init__(self):
        self.checkpoints = [] # Stores (timestamp, price)
        self.max_history = [] # Stores max price up to index i

    def update(self, timestamp, price):
        self.checkpoints.append((timestamp, price))
        
        current_max = price
        if self.max_history:
            current_max = max(self.max_history[-1], price)
        
        self.max_history.append(current_max)

    def getMaxAtCheckpoint(self, checkpoint_idx):
        if 0 <= checkpoint_idx < len(self.max_history):
            return self.max_history[checkpoint_idx]
        return None
```

---

### 🧪 **Test Cases**

**Basic:**
- Add (1, 100), (2, 200). Max(2) -> 200.
- Add (3, 50). Max(3) -> 200.

**Out of Order:**
- Add (1, 100), (3, 100).
- Add (2, 200). Max(2) -> 200. Max(3) -> 200.

**Sparse:**
- Timestamps 1, 1000, 1000000.
- `getMaxPrice(500)` -> Should return max at timestamp 1.
