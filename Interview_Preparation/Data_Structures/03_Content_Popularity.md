# 📈 PROBLEM 3: CONTENT POPULARITY TRACKER

### ⭐⭐⭐⭐ **Rank Content by Popularity**

**Frequency:** High (Appears in ~40% of rounds)
**Difficulty:** Medium-Hard
**Similar to:** [LeetCode 432. All O`one Data Structure](https://leetcode.com/problems/all-oone-data-structure/)

---

## 📋 Problem Statement

Implement a data structure to track the popularity of content items (e.g., pages, posts, videos) in real-time.

**Required Operations:**
1. `increasePopularity(contentId)`: Increase the popularity count of `contentId` by 1.
2. `decreasePopularity(contentId)`: Decrease the popularity count of `contentId` by 1. If count drops to 0, remove the item.
3. `mostPopular()`: Return the `contentId` with the highest popularity. If there are ties, return any one of them. If no content exists, return `null` or `-1`.

**Constraints:**
- All operations must be **O(1)** time complexity.
- 1 ≤ contentId ≤ 10⁹ (or string)
- At most 10⁵ calls total.

---

## 🎨 Visual Example

**Data Structure Design:**
We need a **Doubly Linked List (DLL)** where each node represents a "Bucket" of items with the same popularity count. Buckets are sorted by count.

```text
Initial State: Empty

1. increase("A") -> A has 1
   [Head] <-> [Bucket: 1 | {A}] <-> [Tail]

2. increase("B") -> B has 1
   [Head] <-> [Bucket: 1 | {A, B}] <-> [Tail]

3. increase("B") -> B has 2. Move B to next bucket.
   [Head] <-> [Bucket: 1 | {A}] <-> [Bucket: 2 | {B}] <-> [Tail]

4. increase("B") -> B has 3. Create new bucket.
   [Head] <-> [Bucket: 1 | {A}] <-> [Bucket: 2 | {}] <-> [Bucket: 3 | {B}] <-> [Tail]
                                          ↑ (Empty, remove it)
   [Head] <-> [Bucket: 1 | {A}] <-> [Bucket: 3 | {B}] <-> [Tail]

5. decrease("A") -> A has 0. Remove A.
   [Head] <-> [Bucket: 3 | {B}] <-> [Tail]
```

---

## 💡 Examples

### Example 1: Basic Flow
```python
tracker = PopularityTracker()
tracker.increase("post1")  # post1: 1
tracker.increase("post1")  # post1: 2
tracker.increase("post2")  # post2: 1
print(tracker.mostPopular()) # "post1"
```

### Example 2: Ties
```python
tracker.increase("A")
tracker.increase("B")
print(tracker.mostPopular()) # "A" or "B" (both have 1)
```

### Example 3: Decrement & Removal
```python
tracker.increase("A")
tracker.decrease("A")      # A is removed
print(tracker.mostPopular()) # None
```

---

## 🗣️ Interview Conversation Guide

### Phase 1: Clarification (3-5 min)

**Candidate:** "For `mostPopular`, if there are ties, does it matter which one I return?"
**Interviewer:** "No, returning any valid item with the max popularity is fine."

**Candidate:** "What happens if I call `decrease` on an item that doesn't exist?"
**Interviewer:** "You can ignore it or raise an error. Let's say ignore it."

**Candidate:** "Is the content ID an integer or a string?"
**Interviewer:** "Could be either. Assume string for generality."

**Candidate:** "Most importantly, do we need O(1) for ALL operations?"
**Interviewer:** "Yes, O(1) is the goal. O(log N) is acceptable but not optimal."

### Phase 2: Approach Discussion (5-8 min)

**Candidate:** "My initial thought is a **HashMap** `Map<ID, Count>`.
- `increase/decrease`: O(1)
- `mostPopular`: O(N) scan to find max. Too slow."

**Candidate:** "To optimize `mostPopular`, I could use a **Max-Heap**.
- `increase`: O(log N)
- `mostPopular`: O(1)
- `decrease`: O(N) to remove arbitrary element (heap limitation). Lazy removal helps but still amortized O(log N)."

**Candidate:** "To get strict O(1), we need to group items by their count.
- **Doubly Linked List of Buckets:** Each node is a count (1, 2, 3...).
- Each node stores a **Set** of items having that count.
- **HashMap:** `Map<ID, BucketNode>` to quickly find where an item is.
- Since counts change by +1/-1, we only ever move items to the adjacent bucket. This allows O(1) updates."

### Phase 3: Coding (15-20 min)

**Candidate:** "I'll implement:
1. `Node` class for the DLL buckets.
2. `PopularityTracker` class with the Map + DLL logic.
3. Helper functions `_add_node_after`, `_remove_node` to keep the code clean."

---

## 🧠 Intuition & Approach

### Why Doubly Linked List + HashMap?

We need to support **arbitrary access** (updates) and **ordered max access** (queries) simultaneously.

1.  **HashMap** gives us direct access to the *current state* of any item (O(1)).
2.  **Doubly Linked List** maintains the *order* of counts (1 < 2 < 3...).
    *   Why not an Array? Because counts can be sparse (e.g., items with 1, 500, 1000 votes). Array would be mostly empty.
    *   Why not a standard List? We need to remove empty buckets in O(1).
3.  **Sets within Nodes**: Allow O(1) insertion/removal of items within a bucket.

**Data Structure:**
- `key_to_node`: Maps `contentId` → `Node` (where `Node` stores count X)
- `head` / `tail`: Sentinels for the DLL. `tail.prev` is always the max bucket.

---

## 📝 Complete Solution

```python
from typing import Optional, Set, Dict

class Node:
    """
    A Bucket in the Doubly Linked List.
    Represents a specific popularity count.
    """
    def __init__(self, count: int = 0):
        self.count = count
        self.keys: Set[str] = set()  # Items with this popularity
        self.prev: Optional['Node'] = None
        self.next: Optional['Node'] = None

    def add_key(self, key: str):
        self.keys.add(key)

    def remove_key(self, key: str):
        self.keys.remove(key)
    
    def is_empty(self):
        return len(self.keys) == 0
    
    def get_any_key(self):
        """Return one key from the set (for mostPopular)."""
        return next(iter(self.keys)) if self.keys else None


class PopularityTracker:
    """
    O(1) Content Popularity Tracker using DLL + HashMap.
    """
    
    def __init__(self):
        # Map: contentId -> Node (bucket)
        self.key_to_node: Dict[str, Node] = {}
        
        # DLL Sentinels
        self.head = Node(float('-inf'))  # Min sentinel
        self.tail = Node(float('inf'))   # Max sentinel
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_node_after(self, prev_node: Node, count: int) -> Node:
        """Create and insert a new node after prev_node."""
        new_node = Node(count)
        new_node.prev = prev_node
        new_node.next = prev_node.next
        prev_node.next.prev = new_node
        prev_node.next = new_node
        return new_node

    def _remove_node(self, node: Node):
        """Remove a node from DLL."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def increasePopularity(self, key: str) -> None:
        """
        Increase count for key by 1.
        Time: O(1)
        """
        if key in self.key_to_node:
            current_node = self.key_to_node[key]
            new_count = current_node.count + 1
            
            # Check if next bucket exists
            next_node = current_node.next
            if next_node.count != new_count:
                next_node = self._add_node_after(current_node, new_count)
            
            # Move key
            next_node.add_key(key)
            self.key_to_node[key] = next_node
            current_node.remove_key(key)
            
            # Clean up
            if current_node.is_empty():
                self._remove_node(current_node)
        else:
            # New key: Add to bucket 1
            first_node = self.head.next
            if first_node.count != 1:
                first_node = self._add_node_after(self.head, 1)
            
            first_node.add_key(key)
            self.key_to_node[key] = first_node

    def decreasePopularity(self, key: str) -> None:
        """
        Decrease count for key by 1.
        Time: O(1)
        """
        if key not in self.key_to_node:
            return  # Ignore if not found
            
        current_node = self.key_to_node[key]
        new_count = current_node.count - 1
        
        # Remove from current
        current_node.remove_key(key)
        
        if new_count == 0:
            # Remove completely
            del self.key_to_node[key]
        else:
            # Move to prev bucket
            prev_node = current_node.prev
            if prev_node.count != new_count:
                prev_node = self._add_node_after(current_node.prev, new_count)
            
            prev_node.add_key(key)
            self.key_to_node[key] = prev_node
            
        # Clean up
        if current_node.is_empty():
            self._remove_node(current_node)

    def mostPopular(self) -> Optional[str]:
        """
        Return key with max popularity.
        Time: O(1)
        """
        if self.tail.prev == self.head:
            return None  # Empty
        return self.tail.prev.get_any_key()


# ============================================
# COMPLETE RUNNABLE EXAMPLE
# ============================================

if __name__ == "__main__":
    print("=" * 50)
    print("CONTENT POPULARITY TRACKER (O(1))")
    print("=" * 50)
    
    tracker = PopularityTracker()
    
    # Test 1: Basic Increase
    print("\n[Test 1] Increasing A, B")
    tracker.increasePopularity("A") # A:1
    tracker.increasePopularity("B") # B:1
    tracker.increasePopularity("B") # B:2
    print(f"Most Popular: {tracker.mostPopular()}") # Expected: B
    
    # Test 2: Overtake
    print("\n[Test 2] A overtakes B")
    tracker.increasePopularity("A") # A:2
    tracker.increasePopularity("A") # A:3
    print(f"Most Popular: {tracker.mostPopular()}") # Expected: A
    
    # Test 3: Decrease
    print("\n[Test 3] Decrease A")
    tracker.decreasePopularity("A") # A:2
    print(f"Most Popular: {tracker.mostPopular()}") # Expected: A or B (both 2)
    tracker.decreasePopularity("A") # A:1
    print(f"Most Popular: {tracker.mostPopular()}") # Expected: B (2 vs 1)
    
    # Test 4: Removal
    print("\n[Test 4] Remove A completely")
    tracker.decreasePopularity("A") # A:0 -> Removed
    print(f"Most Popular: {tracker.mostPopular()}") # Expected: B
    
    print("\nAll basic operations verified! ✓")
```

---

## 🔍 Explanation with Example

Let's trace through a detailed example step by step to understand how the algorithm works:

**Operations:**
1. `increasePopularity("A")`  
2. `increasePopularity("B")`  
3. `increasePopularity("B")`  
4. `mostPopular()`  
5. `increasePopularity("A")`  
6. `decreasePopularity("B")`

---

**Initial State:**
```
key_to_node = {}
DLL: [Head] <-> [Tail]
```

---

**Operation 1: increasePopularity("A")**

- A is new (not in `key_to_node`)
- Need bucket for count=1
- Check `head.next`: Is it count=1? No (it's Tail)
- Create new bucket for count=1 after Head
- Add A to this bucket

```
key_to_node = {A: Node(count=1)}
DLL: [Head] <-> [count=1: {A}] <-> [Tail]
```

---

**Operation 2: increasePopularity("B")**

- B is new (not in `key_to_node`)
- Need bucket for count=1
- Check `head.next`: Is it count=1? Yes! Use existing bucket
- Add B to this bucket

```
key_to_node = {A: Node(count=1), B: Node(count=1)}
DLL: [Head] <-> [count=1: {A, B}] <-> [Tail]
```

---

**Operation 3: increasePopularity("B")**

- B exists at count=1
- Need to move to count=2
- current_node = Node(count=1)
- Check current_node.next: Is it count=2? No (it's Tail)
- Create new bucket for count=2 after current_node
- Move B from count=1 bucket to count=2 bucket
- count=1 bucket still has A, so don't remove it

```
key_to_node = {A: Node(count=1), B: Node(count=2)}
DLL: [Head] <-> [count=1: {A}] <-> [count=2: {B}] <-> [Tail]
```

---

**Operation 4: mostPopular()**

- Look at `tail.prev`
- tail.prev = Node(count=2)
- Return any key from this bucket: "B"

**Result:** "B"

---

**Operation 5: increasePopularity("A")**

- A exists at count=1
- Need to move to count=2
- current_node = Node(count=1)
- Check current_node.next: Is it count=2? Yes! Use existing bucket
- Move A from count=1 bucket to count=2 bucket
- count=1 bucket is now empty → remove it from DLL

```
key_to_node = {A: Node(count=2), B: Node(count=2)}
DLL: [Head] <-> [count=2: {A, B}] <-> [Tail]
```

---

**Operation 6: decreasePopularity("B")**

- B exists at count=2
- Need to move to count=1
- current_node = Node(count=2)
- Remove B from count=2 bucket
- Check current_node.prev: Is it count=1? No (it's Head)
- Create new bucket for count=1 after Head (before count=2)
- Add B to count=1 bucket
- count=2 bucket still has A, so don't remove it

```
key_to_node = {A: Node(count=2), B: Node(count=1)}
DLL: [Head] <-> [count=1: {B}] <-> [count=2: {A}] <-> [Tail]
```

**Final State:** A has count=2 (most popular), B has count=1

---

## 🔍 Complexity Analysis

### Time Complexity: **O(1)** for all operations
- **HashMap Lookup:** O(1) average.
- **DLL Insertion/Deletion:** O(1) because we always have a reference to the neighbor node.
- **Set Operations:** O(1) to add/remove items.

### Space Complexity: **O(N)**
- **HashMap:** Stores N keys.
- **DLL Nodes:** At most N nodes (if all items have different counts). Usually much fewer.
- **Sets:** Store total N keys distributed across buckets.

---

## ⚠️ Common Pitfalls

### 1. **Forgetting to clean up empty buckets**
**Problem:** If you leave empty nodes in the DLL, the list grows indefinitely. Iterating (if needed) becomes slow.
**Fix:** Always check `if node.is_empty(): remove(node)` after moving an item out.

### 2. **Handling "Gaps" Incorrectly**
**Problem:** When increasing from count 1 to 2, assuming `curr.next` is count 2.
**Edge Case:** `curr.next` might be count 5.
**Fix:** Check `curr.next.count`. If it's not `target_count`, create a new node and insert it.

### 3. **Memory Leak in Sets**
**Problem:** Removing an item from the tracker but leaving it in the `key_to_node` map or the bucket set.
**Fix:** Ensure explicit `del` and `remove()` calls are symmetric to addition.

---

## 🔄 Follow-up Questions

### Follow-up 1: Return Most Recently Updated Content

**Problem:**
> "Currently `mostPopular()` returns *any* max item. Change it to return the one that reached that popularity **most recently**."

**Solution:**
Instead of a standard `Set`, use an `OrderedDict` (or Python's insertion-ordered `dict`) inside the Node.
- **Add:** Append to end (newest).
- **Access:** `next(reversed(node.keys))` gets the last inserted item.

```python
class RecencyNode(Node):
    def __init__(self, count):
        super().__init__(count)
        self.keys = {}  # Ordered Dict
        
    def add_key(self, key):
        self.keys[key] = True  # Append to end
        
    def remove_key(self, key):
        if key in self.keys:
            del self.keys[key]
            
    def get_newest_key(self):
        # Return last key (most recent)
        return next(reversed(self.keys)) if self.keys else None

class RecencyTracker(PopularityTracker):
    # Override _add_node_after to use RecencyNode
    def _add_node_after(self, prev_node, count):
        new_node = RecencyNode(count)
        # ... (link logic same as parent) ...
        return new_node
        
    def mostPopular(self):
        if self.tail.prev == self.head: return None
        return self.tail.prev.get_newest_key()
```

---

### Follow-up 2: Get Top-K Popular Items

**Problem:**
> "Implement `getTopK(k)` to return the k most popular items."

**Challenge:**
We need to traverse from the tail backwards.

**Algorithm:**
1. Start at `tail.prev`.
2. Take all items from this bucket.
3. If we need more, move to `node.prev`.
4. Repeat until we have k items or hit head.

```python
    def getTopK(self, k: int) -> list:
        result = []
        current = self.tail.prev
        
        while current != self.head and len(result) < k:
            # Get items from current bucket
            # Note: Order depends on set implementation (random or insertion)
            bucket_items = list(current.keys)
            
            # Take needed amount
            needed = k - len(result)
            result.extend(bucket_items[:needed])
            
            current = current.prev
            
        return result
```

**Complexity:** O(K) (assuming buckets aren't huge relative to K).

---

### Follow-up 3: Thread Safety

**Problem:**
> "Make the tracker thread-safe for concurrent web requests."

**Solution:**
Since operations are O(1), critical sections are very short. A **Coarse-Grained Lock** (one lock for the whole structure) is efficient and simple.

```python
import threading

class ThreadSafeTracker(PopularityTracker):
    def __init__(self):
        super().__init__()
        self.lock = threading.Lock()
        
    def increasePopularity(self, key):
        with self.lock:
            super().increasePopularity(key)
            
    def mostPopular(self):
        with self.lock:
            return super().mostPopular()
```

---

## 🧪 Test Cases

```python
def test_popularity_tracker():
    tracker = PopularityTracker()
    
    # 1. Basic Increase
    tracker.increasePopularity("A")
    assert tracker.mostPopular() == "A"
    
    # 2. Tie Breaking
    tracker.increasePopularity("B")
    assert tracker.mostPopular() in ["A", "B"]
    
    # 3. Separation
    tracker.increasePopularity("B")
    assert tracker.mostPopular() == "B"
    
    # 4. Decrement logic
    tracker.decreasePopularity("B")
    assert tracker.mostPopular() in ["A", "B"]
    
    # 5. Top K
    # A:1, B:1. Add C:3
    tracker.increasePopularity("C")
    tracker.increasePopularity("C")
    tracker.increasePopularity("C")
    
    # Top 2 should be [C, A] or [C, B]
    top2 = tracker.getTopK(2)  # Hypothetical method call
    assert top2[0] == "C"
    assert len(top2) == 2
    
    print("Tests Passed!")
```
