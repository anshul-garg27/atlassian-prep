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

---

## 📊 Overall Architecture Diagram

```text
┌─────────────────────────────────────────────────────────────────┐
│                    POPULARITY TRACKER                           │
│                                                                 │
│  HashMap: key_to_node                                          │
│  ┌──────────────────────────────────────────────────┐          │
│  │  "A" → Node(count=2)  ──────────┐                │          │
│  │  "B" → Node(count=2)  ──────┐   │                │          │
│  │  "C" → Node(count=1)  ────┐ │   │                │          │
│  └───────────────────────────┼─┼───┼────────────────┘          │
│                              │ │   │                            │
│  Doubly-Linked List (Sorted by Count):                         │
│                              ↓ ↓   ↓                            │
│  ┌──────┐     ┌─────────────────┐     ┌─────────────────┐     ┌──────┐
│  │ Head │◄───►│  Bucket: count=1│◄───►│  Bucket: count=2│◄───►│ Tail │
│  │ (-∞) │     │   keys: {C}     │     │   keys: {A, B}  │     │ (∞)  │
│  └──────┘     └─────────────────┘     └─────────────────┘     └──────┘
│                       ↑                         ↑                       │
│                       └─────────────────────────┘                       │
│                     prev/next pointers (bidirectional)                 │
└─────────────────────────────────────────────────────────────────┘
```

**Key Components:**
1. **HashMap (`key_to_node`)**: O(1) lookup of any content item
2. **Doubly-Linked List**: Maintains sorted order of popularity counts
3. **Bucket Nodes**: Each holds items with the same count
4. **Sentinel Nodes**: Head and Tail simplify edge case handling

---

## 🔍 Detailed Node Structure

```text
┌───────────────────────────────────┐
│        Bucket Node                │
├───────────────────────────────────┤
│  count: int (popularity level)    │
│  keys: Set[str] (content items)   │
│  prev: Node* (previous bucket)    │
│  next: Node* (next bucket)        │
└───────────────────────────────────┘

Example:
┌───────────────────────────────────┐
│  count: 3                         │
│  keys: {"post1", "video5"}        │
│  prev: ───► [Node with count=2]   │
│  next: ───► [Node with count=4]   │
└───────────────────────────────────┘
```

**Why Sets?**
- O(1) add/remove of items within a bucket
- No duplicates (each content ID appears once)
- Unordered (we don't care about order within same popularity)

---

## 📝 Step-by-Step Operation Trace

### **Initial State: Empty**

```text
HashMap: {}

DLL:
┌──────┐          ┌──────┐
│ Head │◄────────►│ Tail │
│ (-∞) │          │ (∞)  │
└──────┘          └──────┘
```

---

### **Step 1: increase("A") → A has count=1**

**Operation:**
- A is new (not in HashMap)
- Need bucket for count=1
- head.next = Tail (no bucket exists)
- Create new bucket after Head

**Result:**
```text
HashMap: {A → Node(count=1)}

DLL:
┌──────┐     ┌─────────────────┐     ┌──────┐
│ Head │◄───►│  Bucket: 1      │◄───►│ Tail │
│ (-∞) │     │  keys: {A}      │     │ (∞)  │
└──────┘     └─────────────────┘     └──────┘
               ↑
               └─ A points here
```

---

### **Step 2: increase("B") → B has count=1**

**Operation:**
- B is new (not in HashMap)
- Need bucket for count=1
- head.next = Node(count=1) ✓ (reuse existing!)
- Add B to existing bucket

**Result:**
```text
HashMap: {A → Node(count=1), B → Node(count=1)}

DLL:
┌──────┐     ┌─────────────────┐     ┌──────┐
│ Head │◄───►│  Bucket: 1      │◄───►│ Tail │
│ (-∞) │     │  keys: {A, B}   │     │ (∞)  │
└──────┘     └─────────────────┘     └──────┘
               ↑         ↑
               │         └─ B points here
               └─ A points here
```

---

### **Step 3: increase("B") → B has count=2**

**Operation:**
- B exists at count=1
- Need to move to count=2
- current_node.next = Tail (no count=2 bucket)
- Create new bucket after current_node
- Move B from count=1 to count=2
- Bucket count=1 still has A, so keep it

**Result:**
```text
HashMap: {A → Node(count=1), B → Node(count=2)}

DLL:
┌──────┐     ┌─────────────────┐     ┌─────────────────┐     ┌──────┐
│ Head │◄───►│  Bucket: 1      │◄───►│  Bucket: 2      │◄───►│ Tail │
│ (-∞) │     │  keys: {A}      │     │  keys: {B}      │     │ (∞)  │
└──────┘     └─────────────────┘     └─────────────────┘     └──────┘
               ↑                        ↑
               └─ A points here         └─ B points here
```

---

### **Step 4: increase("B") → B has count=3**

**Operation:**
- B exists at count=2
- Need to move to count=3
- current_node.next = Tail (no count=3 bucket)
- Create new bucket after count=2
- Move B from count=2 to count=3
- Bucket count=2 is now EMPTY → **DELETE IT!**

**During:**
```text
┌──────┐     ┌────────┐     ┌────────┐     ┌────────┐     ┌──────┐
│ Head │◄───►│Bucket:1│◄───►│Bucket:2│◄───►│Bucket:3│◄───►│ Tail │
│      │     │ {A}    │     │  {}    │     │ {B}    │     │      │
└──────┘     └────────┘     └────────┘     └────────┘     └──────┘
                              ↑ EMPTY!
                              Remove this
```

**After Cleanup:**
```text
HashMap: {A → Node(count=1), B → Node(count=3)}

DLL:
┌──────┐     ┌─────────────────┐     ┌─────────────────┐     ┌──────┐
│ Head │◄───►│  Bucket: 1      │◄───►│  Bucket: 3      │◄───►│ Tail │
│ (-∞) │     │  keys: {A}      │     │  keys: {B}      │     │ (∞)  │
└──────┘     └─────────────────┘     └─────────────────┘     └──────┘
               ↑                        ↑
               └─ A (count=1)           └─ B (count=3) ← MOST POPULAR
```

---

### **Step 5: decrease("A") → A has count=0 (REMOVE)**

**Operation:**
- A exists at count=1
- New count = 0 → **Delete from tracker**
- Remove A from bucket
- Bucket count=1 is now EMPTY → **DELETE IT!**
- Delete A from HashMap

**Result:**
```text
HashMap: {B → Node(count=3)}

DLL:
┌──────┐     ┌─────────────────┐     ┌──────┐
│ Head │◄───►│  Bucket: 3      │◄───►│ Tail │
│ (-∞) │     │  keys: {B}      │     │ (∞)  │
└──────┘     └─────────────────┘     └──────┘
               ↑
               └─ B (count=3) ← MOST POPULAR
```

---

## 🎯 mostPopular() Query Visualization

**Question:** How do we find the most popular item in O(1)?

**Answer:** It's always in `tail.prev` (the last bucket before the sentinel)!

```text
DLL:
┌──────┐     ┌────────┐     ┌────────┐     ┌────────┐     ┌──────┐
│ Head │◄───►│Bucket:1│◄───►│Bucket:5│◄───►│Bucket:9│◄───►│ Tail │
│      │     │ {C}    │     │ {A}    │     │ {B, D} │     │      │
└──────┘     └────────┘     └────────┘     └────────┘     └──────┘
                                              ↑              ↑
                                              │              │
                                            tail.prev ────────┘

mostPopular() = tail.prev.get_any_key() = "B" or "D"
                                          (either valid)
```

**Time Complexity:** O(1) - direct pointer access!

---

## 🔄 Pointer Manipulation Details

### **Adding a New Bucket Between Two Existing Nodes**

**Scenario:** Insert count=4 bucket between count=3 and count=5

**Before:**
```text
┌────────────┐          ┌────────────┐
│ Bucket: 3  │◄────────►│ Bucket: 5  │
│ {A}        │          │ {B}        │
└────────────┘          └────────────┘
     prev3                   prev5
      next ────────────────► prev
      prev ◄──────────────── next
```

**Step 1: Create new node**
```text
┌────────────┐
│ Bucket: 4  │  (new_node)
│ {C}        │
└────────────┘
  prev = None
  next = None
```

**Step 2: Link new_node**
```text
new_node.prev = prev3  (point to left)
new_node.next = prev5  (point to right)
```

**Step 3: Update neighbors**
```text
prev3.next = new_node  (left neighbor points to new)
prev5.prev = new_node  (right neighbor points to new)
```

**After:**
```text
┌────────────┐     ┌────────────┐     ┌────────────┐
│ Bucket: 3  │◄───►│ Bucket: 4  │◄───►│ Bucket: 5  │
│ {A}        │     │ {C}        │     │ {B}        │
└────────────┘     └────────────┘     └────────────┘
```

---

### **Removing an Empty Bucket**

**Before:**
```text
┌────────────┐     ┌────────────┐     ┌────────────┐
│ Bucket: 2  │◄───►│ Bucket: 3  │◄───►│ Bucket: 4  │
│ {A}        │     │ {}         │     │ {B}        │
└────────────┘     └────────────┘     └────────────┘
                       ↑ EMPTY!
                     to_remove
```

**Operation:**
```python
to_remove.prev.next = to_remove.next  # Skip over node
to_remove.next.prev = to_remove.prev  # Link backwards
```

**After:**
```text
┌────────────┐                    ┌────────────┐
│ Bucket: 2  │◄──────────────────►│ Bucket: 4  │
│ {A}        │                    │ {B}        │
└────────────┘                    └────────────┘

Node(count=3) is now unreachable → garbage collected
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

## 📝 Solution 0: Ultra-Simplified (No Classes - Interview Speed Coding)

**Perfect for 20-30 minute interviews.** Trades some performance for simplicity.

```python
from collections import defaultdict

# Global state (or pass as parameters)
popularity = defaultdict(int)  # contentId -> popularity count

def increase_popularity(content_id):
    """Increase popularity of content by 1."""
    popularity[content_id] += 1

def decrease_popularity(content_id):
    """Decrease popularity of content by 1."""
    if content_id in popularity:
        popularity[content_id] -= 1
        if popularity[content_id] <= 0:
            del popularity[content_id]

def most_popular():
    """Return most popular content (highest count)."""
    if not popularity:
        return None
    
    # Find max count
    max_count = max(popularity.values())
    
    # Find all items with max count (for tie-breaking)
    candidates = [cid for cid, count in popularity.items() if count == max_count]
    
    # Return any one (or implement tie-breaking logic)
    return candidates[0] if candidates else None


# ============================================
# COMPLETE RUNNABLE EXAMPLE
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("CONTENT POPULARITY TRACKER - ULTRA SIMPLIFIED")
    print("=" * 60)
    
    # Test 1: Basic operations
    print("\n[Test 1] Basic Operations")
    print("-" * 40)
    increase_popularity("video1")
    increase_popularity("video2")
    increase_popularity("video1")
    
    print(f"Popularity counts: {dict(popularity)}")
    print(f"Most popular: {most_popular()}")
    
    # Test 2: More increases
    print("\n[Test 2] Multiple Increases")
    print("-" * 40)
    increase_popularity("video3")
    increase_popularity("video3")
    increase_popularity("video3")
    
    print(f"Popularity counts: {dict(popularity)}")
    print(f"Most popular: {most_popular()}")
    
    # Test 3: Decrease
    print("\n[Test 3] Decrease Popularity")
    print("-" * 40)
    decrease_popularity("video3")
    decrease_popularity("video3")
    
    print(f"Popularity counts: {dict(popularity)}")
    print(f"Most popular: {most_popular()}")
    
    # Test 4: Edge cases
    print("\n[Test 4] Edge Cases")
    print("-" * 40)
    decrease_popularity("video1")
    decrease_popularity("video1")  # Goes to 0, should be removed
    
    print(f"Popularity counts: {dict(popularity)}")
    print(f"Most popular: {most_popular()}")
    
    print("\n" + "=" * 60)
    print("✅ All operations completed!")
    print("=" * 60)
    
    print("\n💡 Trade-offs:")
    print("  ✅ Increase/Decrease: O(1)")
    print("  ⚠️  Most Popular: O(N) - scans all items")
    print("  ✅ Simple to code in interview")
    print("\n  For O(1) most_popular(), use DLL + HashMap (see below)")
```

**Complexity:**
- `increase_popularity()`: **O(1)**
- `decrease_popularity()`: **O(1)**  
- `most_popular()`: **O(N)** where N = unique content items

**When to use:** Interview time-pressure, or when `most_popular()` is called rarely.

---

## 📝 Solution 1: Optimal (DLL + HashMap for O(1) Everything)

If interviewer asks for O(1) `most_popular()`, use this:

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

## 🔍 Edge Cases with Detailed Visualizations

### **Edge Case 1: First Item Addition**

```text
Before:
┌──────┐          ┌──────┐
│ Head │◄────────►│ Tail │
└──────┘          └──────┘

Operation: increase("A")

Checks:
1. Is A in HashMap? NO → New item
2. Does head.next have count=1? NO (head.next = Tail)
3. Action: Create new bucket with count=1

After:
┌──────┐     ┌─────────────────┐     ┌──────┐
│ Head │◄───►│  Bucket: 1      │◄───►│ Tail │
│      │     │  keys: {A}      │     │      │
└──────┘     └─────────────────┘     └──────┘

Complexity: O(1) - constant pointer updates
```

---

### **Edge Case 2: Gap in Counts (1 → 5 → 10)**

**Scenario:** Items jump counts, creating gaps

```text
State: Items with counts 1, 5, 10
┌──────┐     ┌────────┐     ┌────────┐     ┌────────┐     ┌──────┐
│ Head │◄───►│Count:1 │◄───►│Count:5 │◄───►│Count:10│◄───►│ Tail │
│      │     │  {A}   │     │  {B}   │     │  {C}   │     │      │
└──────┘     └────────┘     └────────┘     └────────┘     └──────┘

Operation: increase("A")  # A: 1 → 2

Question: Does bucket for count=2 exist?
Answer: NO! (next bucket is count=5)

Action: Create new bucket for count=2 between count=1 and count=5

After:
┌──────┐     ┌────────┐     ┌────────┐     ┌────────┐     ┌──────┐
│ Head │◄───►│Count:2 │◄───►│Count:5 │◄───►│Count:10│◄───►│ Tail │
│      │     │  {A}   │     │  {B}   │     │  {C}   │     │      │
└──────┘     └────────┘     └────────┘     └────────┘     └──────┘
              ↑ NEW!

Note: count=1 bucket removed (was empty)
```

**Why This Works:**
- We only move to adjacent counts (+1 or -1)
- If target bucket doesn't exist, create it
- Maintains sorted order automatically

---

### **Edge Case 3: Mass Deletion (All Items at Same Count)**

```text
Before: 3 items, all with count=5
┌──────┐     ┌─────────────────┐     ┌──────┐
│ Head │◄───►│  Count: 5       │◄───►│ Tail │
│      │     │  {A, B, C}      │     │      │
└──────┘     └─────────────────┘     └──────┘

Operation Sequence:
1. decrease("A")  # A: 5 → 4
2. decrease("B")  # B: 5 → 4
3. decrease("C")  # C: 5 → 4

Step 1: decrease("A")
┌──────┐     ┌────────┐     ┌────────┐     ┌──────┐
│ Head │◄───►│Count:4 │◄───►│Count:5 │◄───►│ Tail │
│      │     │  {A}   │     │ {B, C} │     │      │
└──────┘     └────────┘     └────────┘     └──────┘

Step 2: decrease("B")
┌──────┐     ┌─────────────┐     ┌────────┐     ┌──────┐
│ Head │◄───►│  Count: 4   │◄───►│Count:5 │◄───►│ Tail │
│      │     │   {A, B}    │     │  {C}   │     │      │
└──────┘     └─────────────┘     └────────┘     └──────┘

Step 3: decrease("C")
┌──────┐     ┌─────────────────┐     ┌──────┐
│ Head │◄───►│  Count: 4       │◄───►│ Tail │
│      │     │   {A, B, C}     │     │      │
└──────┘     └─────────────────┘     └──────┘
              ↑
              Count=5 bucket removed (was empty)
```

---

### **Edge Case 4: Decrease to Zero (Complete Removal)**

```text
Before:
┌──────┐     ┌────────┐     ┌────────┐     ┌──────┐
│ Head │◄───►│Count:1 │◄───►│Count:3 │◄───►│ Tail │
│      │     │  {A}   │     │  {B}   │     │      │
└──────┘     └────────┘     └────────┘     └──────┘

Operation: decrease("A")  # A: 1 → 0

Checks:
1. Is A in HashMap? YES
2. Current count = 1
3. New count = 0 → REMOVE COMPLETELY

Actions:
1. Remove A from bucket
2. Delete A from HashMap
3. Check if bucket is empty → YES
4. Remove bucket from DLL

After:
┌──────┐     ┌────────┐     ┌──────┐
│ Head │◄───►│Count:3 │◄───►│ Tail │
│      │     │  {B}   │     │      │
└──────┘     └────────┘     └──────┘

HashMap: {B: Node(count=3)}
```

---

### **Edge Case 5: Single Item Tracker**

**Scenario:** Only one item exists

```text
State: One item with count=7
┌──────┐     ┌────────┐     ┌──────┐
│ Head │◄───►│Count:7 │◄───►│ Tail │
│      │     │  {X}   │     │      │
└──────┘     └────────┘     └──────┘

mostPopular() = "X"  ✓ (tail.prev.get_any_key())

decrease("X") # X: 7 → 6
┌──────┐     ┌────────┐     ┌──────┐
│ Head │◄───►│Count:6 │◄───►│ Tail │
│      │     │  {X}   │     │      │
└──────┘     └────────┘     └──────┘

decrease("X") repeatedly until count=0:
┌──────┐          ┌──────┐
│ Head │◄────────►│ Tail │
└──────┘          └──────┘

mostPopular() = None  ✓ (head.next = tail, empty)
```

---

## 🔄 Complete Operation Trace with All Details

### **Full Example Sequence**

```text
Operations:
1. increase("A")
2. increase("B")
3. increase("B")
4. mostPopular()
5. increase("A")
6. decrease("B")

══════════════════════════════════════════════════════════

[0] Initial State
HashMap: {}
┌──────┐          ┌──────┐
│ Head │◄────────►│ Tail │
└──────┘          └──────┘

══════════════════════════════════════════════════════════

[1] increase("A")
HashMap: {A → Node(count=1)}
┌──────┐     ┌─────────────────┐     ┌──────┐
│ Head │◄───►│  Count: 1       │◄───►│ Tail │
│      │     │  keys: {A}      │     │      │
└──────┘     └─────────────────┘     └──────┘

══════════════════════════════════════════════════════════

[2] increase("B")
HashMap: {A → Node(count=1), B → Node(count=1)}
┌──────┐     ┌─────────────────┐     ┌──────┐
│ Head │◄───►│  Count: 1       │◄───►│ Tail │
│      │     │  keys: {A, B}   │     │      │
└──────┘     └─────────────────┘     └──────┘

══════════════════════════════════════════════════════════

[3] increase("B")  # B: 1 → 2
HashMap: {A → Node(count=1), B → Node(count=2)}
┌──────┐     ┌────────────┐     ┌────────────┐     ┌──────┐
│ Head │◄───►│  Count: 1  │◄───►│  Count: 2  │◄───►│ Tail │
│      │     │  keys: {A} │     │  keys: {B} │     │      │
└──────┘     └────────────┘     └────────────┘     └──────┘

══════════════════════════════════════════════════════════

[4] mostPopular()
Returns: "B" (from tail.prev = Node(count=2))
Time: O(1)

══════════════════════════════════════════════════════════

[5] increase("A")  # A: 1 → 2 (reuses existing bucket)
HashMap: {A → Node(count=2), B → Node(count=2)}
┌──────┐     ┌─────────────────┐     ┌──────┐
│ Head │◄───►│  Count: 2       │◄───►│ Tail │
│      │     │  keys: {A, B}   │     │      │
└──────┘     └─────────────────┘     └──────┘
              ↑ Count=1 bucket removed (was empty)

══════════════════════════════════════════════════════════

[6] decrease("B")  # B: 2 → 1 (creates new bucket)
HashMap: {A → Node(count=2), B → Node(count=1)}
┌──────┐     ┌────────────┐     ┌────────────┐     ┌──────┐
│ Head │◄───►│  Count: 1  │◄───►│  Count: 2  │◄───►│ Tail │
│      │     │  keys: {B} │     │  keys: {A} │     │      │
└──────┘     └────────────┘     └────────────┘     └──────┘

══════════════════════════════════════════════════════════

Final State:
- A has count=2 (most popular)
- B has count=1
- mostPopular() returns "A"
```

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

**Key Insight:**
We need to maintain **insertion order** within each bucket so we can track which item reached the current popularity level most recently.

**Solution Approach:**
Instead of using a standard `Set` (which has no ordering), use Python's `dict` (which maintains insertion order since Python 3.7+) or `OrderedDict` for explicit ordering.

**Data Structure Modification:**
```text
Before: Bucket stores Set {A, B, C} (unordered)
After:  Bucket stores Dict {"A": True, "B": True, "C": True} (insertion-ordered)

When we add a key:
- Append to the end of the dict → "newest" item
- When we query: next(reversed(node.keys)) → gets last inserted
```

**Complete Implementation:**

```python
from typing import Optional, Dict

class RecencyNode:
    """
    Enhanced Node that maintains insertion order of keys.
    Uses dict instead of set to track when items reached this popularity.
    """
    def __init__(self, count: int = 0):
        self.count = count
        self.keys = {}  # Ordered dict: {key: True}
        self.prev: Optional['RecencyNode'] = None
        self.next: Optional['RecencyNode'] = None

    def add_key(self, key: str):
        """Add key to end (most recent)."""
        self.keys[key] = True  # Append to end maintains insertion order

    def remove_key(self, key: str):
        """Remove key if exists."""
        if key in self.keys:
            del self.keys[key]

    def is_empty(self):
        return len(self.keys) == 0

    def get_newest_key(self):
        """Return the most recently added key (LIFO within bucket)."""
        return next(reversed(self.keys)) if self.keys else None


class RecencyTracker:
    """
    O(1) Content Popularity Tracker with recency-based tie-breaking.
    Returns the most recently updated item when multiple items have max popularity.
    """

    def __init__(self):
        # Map: contentId -> Node (bucket)
        self.key_to_node: Dict[str, RecencyNode] = {}

        # DLL Sentinels
        self.head = RecencyNode(float('-inf'))  # Min sentinel
        self.tail = RecencyNode(float('inf'))   # Max sentinel
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_node_after(self, prev_node: RecencyNode, count: int) -> RecencyNode:
        """Create and insert a new node after prev_node."""
        new_node = RecencyNode(count)
        new_node.prev = prev_node
        new_node.next = prev_node.next
        prev_node.next.prev = new_node
        prev_node.next = new_node
        return new_node

    def _remove_node(self, node: RecencyNode):
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
        Return the most recently updated item with max popularity.
        Time: O(1)
        """
        if self.tail.prev == self.head:
            return None  # Empty tracker
        return self.tail.prev.get_newest_key()  # Most recent in max bucket


# ============================================
# USAGE EXAMPLE
# ============================================
if __name__ == "__main__":
    tracker = RecencyTracker()

    # Add items
    tracker.increasePopularity("A")  # A:1
    tracker.increasePopularity("B")  # B:1
    tracker.increasePopularity("A")  # A:2 (moved to bucket 2 first)
    tracker.increasePopularity("B")  # B:2 (moved to bucket 2 second)

    print(tracker.mostPopular())  # Output: "B" (most recently updated)
```

**Example Trace:**

```text
Operations:
1. increase("A")  # A:1
2. increase("B")  # B:1
3. increase("A")  # A:2 (moved to bucket 2)
4. increase("B")  # B:2 (moved to bucket 2 AFTER A)

Bucket State (count=2):
keys = {"A": True, "B": True}
        ↑ added first   ↑ added second (most recent)

mostPopular() returns "B" (most recently updated)
```

**Complexity Analysis:**
- **Time Complexity:**
  - `increase()`: O(1) - dict append is O(1) amortized
  - `decrease()`: O(1) - dict deletion is O(1) average
  - `mostPopular()`: O(1) - `next(reversed())` is O(1)
- **Space Complexity:** O(N) - same as original (dict overhead ~same as set)

**Trade-offs:**
- **Pros:** Deterministic tie-breaking based on recency
- **Cons:** Slightly more memory overhead (dict vs set) and marginally slower operations due to ordering maintenance

---

### Follow-up 2: Get Top-K Popular Items

**Problem:**
> "Implement `getTopK(k)` to return the k most popular items in descending order of popularity."

**Key Insight:**
The DLL is already sorted by popularity (ascending from head to tail). We traverse backwards from `tail.prev` to collect the top-k items.

**Algorithm:**
1. Start at the maximum bucket (`tail.prev`)
2. Collect all items from this bucket
3. If we have fewer than k items, move to previous bucket (`node.prev`)
4. Repeat until we have k items or reach head
5. Return list of top-k items

**Visualization:**

```text
DLL State:
┌──────┐  ┌────────┐  ┌────────┐  ┌────────┐  ┌──────┐
│ Head │◄─│Count:2 │◄─│Count:5 │◄─│Count:8 │◄─│ Tail │
│      │  │ {C, D} │  │ {B}    │  │ {A, E} │  │      │
└──────┘  └────────┘  └────────┘  └────────┘  └──────┘
                                      ↑
                                   Start here (tail.prev)

getTopK(3):
Step 1: current = Count:8, take {A, E} → result = [A, E]
Step 2: Need 1 more, current = Count:5, take {B} → result = [A, E, B]
Return: [A, E, B]  (top 3 by popularity)
```

**Complete Implementation:**

```python
from typing import Optional, Set, Dict, List, Tuple

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
    O(1) Content Popularity Tracker with Top-K support.
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

    def getTopK(self, k: int) -> List[str]:
        """
        Return k most popular items in descending popularity order.

        Args:
            k: Number of top items to return

        Returns:
            List of up to k content IDs with highest popularity

        Time: O(B + K) where B = number of buckets traversed
        Space: O(K) for result list
        """
        if k <= 0:
            return []

        result = []
        current = self.tail.prev

        # Traverse backwards from max bucket
        while current != self.head and len(result) < k:
            # Get all items from current bucket
            bucket_items = list(current.keys)

            # Calculate how many more items we need
            needed = k - len(result)

            # Take up to 'needed' items from this bucket
            result.extend(bucket_items[:needed])

            # Move to next lower popularity bucket
            current = current.prev

        return result

    def getTopKWithCounts(self, k: int) -> List[Tuple[str, int]]:
        """
        Return k most popular items WITH their popularity counts.

        Args:
            k: Number of top items to return

        Returns:
            List of (content_id, count) tuples

        Example: [("A", 10), ("B", 8), ("C", 8)]

        Time: O(B + K) where B = number of buckets traversed
        Space: O(K) for result list
        """
        if k <= 0:
            return []

        result = []
        current = self.tail.prev

        while current != self.head and len(result) < k:
            bucket_items = list(current.keys)
            needed = k - len(result)

            # Add items with their count
            for item in bucket_items[:needed]:
                result.append((item, current.count))

            current = current.prev

        return result


# ============================================
# USAGE EXAMPLE
# ============================================
if __name__ == "__main__":
    tracker = PopularityTracker()

    # Setup: A:5, B:3, C:3, D:1
    for _ in range(5):
        tracker.increasePopularity("A")
    for _ in range(3):
        tracker.increasePopularity("B")
    for _ in range(3):
        tracker.increasePopularity("C")
    tracker.increasePopularity("D")

    print("Top 2:", tracker.getTopK(2))
    # Output: ["A", "B"] or ["A", "C"] (A is always first, B/C are tied)

    print("Top 3 with counts:", tracker.getTopKWithCounts(3))
    # Output: [("A", 5), ("B", 3), ("C", 3)]
```

**Complexity Analysis:**
- **Time Complexity:**
  - **Best Case:** O(1) - if top bucket has ≥ k items
  - **Average Case:** O(B) where B = number of buckets traversed
  - **Worst Case:** O(N) - if each item is in a separate bucket and k = N
  - **Practical:** O(K) when buckets are reasonably populated

- **Space Complexity:** O(K) - result list

**Why Not O(K log K) Sort?**
We leverage the fact that the DLL is *already sorted* by popularity, so we just traverse and collect.

---

### Follow-up 3: Thread Safety

**Problem:**
> "Make the tracker thread-safe for concurrent web requests in a production environment."

**Challenge:**
Multiple threads could:
1. Read/write the HashMap simultaneously
2. Modify DLL pointers concurrently (causing corruption)
3. Race on bucket operations (add/remove keys)

**Solution: Coarse-Grained Locking**

Since all operations are O(1) and very fast, using a single lock for the entire data structure is efficient and prevents deadlocks.

**Complete Implementation (Coarse-Grained Locking):**

```python
import threading
from typing import Optional, Set, Dict, List

class Node:
    """
    A Bucket in the Doubly Linked List.
    Represents a specific popularity count.
    """
    def __init__(self, count: int = 0):
        self.count = count
        self.keys: Set[str] = set()
        self.prev: Optional['Node'] = None
        self.next: Optional['Node'] = None

    def add_key(self, key: str):
        self.keys.add(key)

    def remove_key(self, key: str):
        self.keys.remove(key)

    def is_empty(self):
        return len(self.keys) == 0

    def get_any_key(self):
        return next(iter(self.keys)) if self.keys else None


class ThreadSafeTracker:
    """
    Thread-safe Content Popularity Tracker using coarse-grained locking.
    All operations are O(1) with lock acquisition overhead.
    Suitable for high-concurrency web applications.
    """

    def __init__(self):
        # Map: contentId -> Node (bucket)
        self.key_to_node: Dict[str, Node] = {}

        # DLL Sentinels
        self.head = Node(float('-inf'))
        self.tail = Node(float('inf'))
        self.head.next = self.tail
        self.tail.prev = self.head

        # Single lock for entire data structure
        self.lock = threading.Lock()

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
        """Thread-safe increase operation."""
        with self.lock:
            if key in self.key_to_node:
                current_node = self.key_to_node[key]
                new_count = current_node.count + 1

                next_node = current_node.next
                if next_node.count != new_count:
                    next_node = self._add_node_after(current_node, new_count)

                next_node.add_key(key)
                self.key_to_node[key] = next_node
                current_node.remove_key(key)

                if current_node.is_empty():
                    self._remove_node(current_node)
            else:
                first_node = self.head.next
                if first_node.count != 1:
                    first_node = self._add_node_after(self.head, 1)

                first_node.add_key(key)
                self.key_to_node[key] = first_node

    def decreasePopularity(self, key: str) -> None:
        """Thread-safe decrease operation."""
        with self.lock:
            if key not in self.key_to_node:
                return

            current_node = self.key_to_node[key]
            new_count = current_node.count - 1

            current_node.remove_key(key)

            if new_count == 0:
                del self.key_to_node[key]
            else:
                prev_node = current_node.prev
                if prev_node.count != new_count:
                    prev_node = self._add_node_after(current_node.prev, new_count)

                prev_node.add_key(key)
                self.key_to_node[key] = prev_node

            if current_node.is_empty():
                self._remove_node(current_node)

    def mostPopular(self) -> Optional[str]:
        """Thread-safe query operation."""
        with self.lock:
            if self.tail.prev == self.head:
                return None
            return self.tail.prev.get_any_key()

    def getTopK(self, k: int) -> List[str]:
        """Thread-safe top-k query."""
        with self.lock:
            if k <= 0:
                return []

            result = []
            current = self.tail.prev

            while current != self.head and len(result) < k:
                bucket_items = list(current.keys)
                needed = k - len(result)
                result.extend(bucket_items[:needed])
                current = current.prev

            return result

    def getCount(self, key: str) -> int:
        """
        Get current popularity count for a key.
        Returns 0 if key doesn't exist.
        """
        with self.lock:
            if key not in self.key_to_node:
                return 0
            return self.key_to_node[key].count


# ============================================
# USAGE EXAMPLE
# ============================================
if __name__ == "__main__":
    import concurrent.futures

    tracker = ThreadSafeTracker()

    # Simulate concurrent updates from 10 threads
    def worker(content_id: str, num_increments: int):
        for _ in range(num_increments):
            tracker.increasePopularity(content_id)

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(worker, "video1", 100),
            executor.submit(worker, "video2", 150),
            executor.submit(worker, "video3", 120),
        ]
        concurrent.futures.wait(futures)

    print("Most Popular:", tracker.mostPopular())
    print("Top 3:", tracker.getTopK(3))
```

**Alternative: Fine-Grained Locking (Advanced)**

For extremely high concurrency with read-heavy workloads (90%+ reads), we can use a Read-Write Lock to allow concurrent reads:

```python
import threading
from typing import Optional, Set, Dict, List

class Node:
    """Bucket node for DLL."""
    def __init__(self, count: int = 0):
        self.count = count
        self.keys: Set[str] = set()
        self.prev: Optional['Node'] = None
        self.next: Optional['Node'] = None

    def add_key(self, key: str):
        self.keys.add(key)

    def remove_key(self, key: str):
        self.keys.remove(key)

    def is_empty(self):
        return len(self.keys) == 0

    def get_any_key(self):
        return next(iter(self.keys)) if self.keys else None


class RWLockTracker:
    """
    Read-Write Lock Popularity Tracker.
    Multiple readers can query simultaneously.
    Writers get exclusive access.
    Best for read-heavy workloads (90%+ reads).
    """

    def __init__(self):
        # Map: contentId -> Node
        self.key_to_node: Dict[str, Node] = {}

        # DLL Sentinels
        self.head = Node(float('-inf'))
        self.tail = Node(float('inf'))
        self.head.next = self.tail
        self.tail.prev = self.head

        # RW Lock implementation
        self._read_ready = threading.Condition(threading.Lock())
        self._readers = 0
        self._writer = False

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

    def _acquire_read(self):
        """Acquire read lock (shared)."""
        with self._read_ready:
            while self._writer:
                self._read_ready.wait()
            self._readers += 1

    def _release_read(self):
        """Release read lock."""
        with self._read_ready:
            self._readers -= 1
            if self._readers == 0:
                self._read_ready.notify_all()

    def _acquire_write(self):
        """Acquire write lock (exclusive)."""
        with self._read_ready:
            while self._writer or self._readers > 0:
                self._read_ready.wait()
            self._writer = True

    def _release_write(self):
        """Release write lock."""
        with self._read_ready:
            self._writer = False
            self._read_ready.notify_all()

    def increasePopularity(self, key: str) -> None:
        """Write operation: exclusive lock."""
        self._acquire_write()
        try:
            if key in self.key_to_node:
                current_node = self.key_to_node[key]
                new_count = current_node.count + 1

                next_node = current_node.next
                if next_node.count != new_count:
                    next_node = self._add_node_after(current_node, new_count)

                next_node.add_key(key)
                self.key_to_node[key] = next_node
                current_node.remove_key(key)

                if current_node.is_empty():
                    self._remove_node(current_node)
            else:
                first_node = self.head.next
                if first_node.count != 1:
                    first_node = self._add_node_after(self.head, 1)

                first_node.add_key(key)
                self.key_to_node[key] = first_node
        finally:
            self._release_write()

    def decreasePopularity(self, key: str) -> None:
        """Write operation: exclusive lock."""
        self._acquire_write()
        try:
            if key not in self.key_to_node:
                return

            current_node = self.key_to_node[key]
            new_count = current_node.count - 1

            current_node.remove_key(key)

            if new_count == 0:
                del self.key_to_node[key]
            else:
                prev_node = current_node.prev
                if prev_node.count != new_count:
                    prev_node = self._add_node_after(current_node.prev, new_count)

                prev_node.add_key(key)
                self.key_to_node[key] = prev_node

            if current_node.is_empty():
                self._remove_node(current_node)
        finally:
            self._release_write()

    def mostPopular(self) -> Optional[str]:
        """Read operation: shared lock (concurrent reads allowed)."""
        self._acquire_read()
        try:
            if self.tail.prev == self.head:
                return None
            return self.tail.prev.get_any_key()
        finally:
            self._release_read()

    def getTopK(self, k: int) -> List[str]:
        """Read operation: shared lock (concurrent reads allowed)."""
        self._acquire_read()
        try:
            if k <= 0:
                return []

            result = []
            current = self.tail.prev

            while current != self.head and len(result) < k:
                bucket_items = list(current.keys)
                needed = k - len(result)
                result.extend(bucket_items[:needed])
                current = current.prev

            return result
        finally:
            self._release_read()


# ============================================
# USAGE EXAMPLE
# ============================================
if __name__ == "__main__":
    import concurrent.futures
    import time

    tracker = RWLockTracker()

    # Setup initial data
    for i in range(10):
        tracker.increasePopularity(f"video{i}")

    # Simulate read-heavy workload (95% reads, 5% writes)
    def reader_worker():
        for _ in range(100):
            tracker.mostPopular()
            tracker.getTopK(5)

    def writer_worker():
        for i in range(5):
            tracker.increasePopularity(f"video{i}")

    start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        # 19 readers, 1 writer
        futures = [executor.submit(reader_worker) for _ in range(19)]
        futures.append(executor.submit(writer_worker))
        concurrent.futures.wait(futures)

    print(f"Completed in {time.time() - start:.2f}s")
    print("Most Popular:", tracker.mostPopular())
```

**Complexity Analysis:**

**Coarse-Grained Locking:**
- **Time Complexity:** O(1) + lock acquisition overhead
  - Lock acquisition: O(1) amortized (assuming low contention)
  - Under high contention: threads block, but operations remain O(1) once lock is acquired
- **Space Complexity:** O(N) + O(T) where T = thread overhead (minimal)
- **Throughput:** Serialized access (one operation at a time)

**Read-Write Locking:**
- **Time Complexity:**
  - Reads: O(1) + shared lock overhead (concurrent)
  - Writes: O(1) + exclusive lock overhead (serialized)
- **Throughput:** Better for read-heavy workloads (multiple `mostPopular()` queries)

**Comparison Table:**

| Approach | Reads | Writes | Complexity | Best For |
|----------|-------|--------|------------|----------|
| **No Lock** | Fast | Fast | Simple | Single-threaded |
| **Coarse Lock** | Serialized | Serialized | Simple | Balanced workload |
| **RW Lock** | Concurrent | Serialized | Complex | Read-heavy (90%+ reads) |

**Best Practice:**
- **Start with coarse-grained locking** (simpler, fewer bugs)
- **Profile in production** to identify bottlenecks
- **Upgrade to RW locks** only if lock contention is proven to be a bottleneck

**Deadlock Prevention:**
Our implementation is deadlock-free because:
1. Single lock (no lock ordering issues)
2. No nested locking
3. Locks are always released (context manager `with`)

---

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
