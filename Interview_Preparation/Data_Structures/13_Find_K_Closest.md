# 🎯 PROBLEM 13: FIND K CLOSEST ELEMENTS

### ⭐⭐⭐ **Binary Search + Two Pointers**

**Frequency:** Low-Medium (Appears in ~15-20% of rounds)
**Difficulty:** Medium
**Similar to:** [LeetCode 658 - Find K Closest Elements](https://leetcode.com/problems/find-k-closest-elements/)

---

## 📋 Problem Statement

Given a **sorted** integer array `arr`, two integers `k` and `x`, return the `k` closest integers to `x` in the array. The result should also be sorted in **ascending order**.

**Closeness Definition:**
- An integer `a` is closer to `x` than `b` if:
  - `|a - x| < |b - x|`, OR
  - `|a - x| == |b - x|` and `a < b` (prefer smaller element in ties)

**Constraints:**
- 1 ≤ k ≤ arr.length
- 1 ≤ arr.length ≤ 10⁴
- arr is **sorted in ascending order**
- -10⁴ ≤ arr[i], x ≤ 10⁴

---

## 🎨 Visual Example

### Example 1: Basic Case

```text
arr = [1, 2, 3, 4, 5]
k = 4
x = 3

Distance from x=3:
Index: 0   1   2   3   4
Value: 1   2   3   4   5
Dist:  2   1   0   1   2

Step 1: Find 4 closest elements
- Distance 0: [3]           (1 element)
- Distance 1: [2, 4]        (3 elements)
- Distance 2: [1, 5]        (5 elements)

Step 2: Take first 4
Closest 4: [1, 2, 3, 4]

Step 3: Sort (already sorted)
Result: [1, 2, 3, 4]
```

### Example 2: Target Not in Array

```text
arr = [1, 2, 3, 4, 5]
k = 4
x = -1

Distance from x=-1:
Index: 0   1   2   3   4
Value: 1   2   3   4   5
Dist:  2   3   4   5   6

Closest 4: [1, 2, 3, 4]
```

### Example 3: Tie-Breaking

```text
arr = [1, 1, 1, 10, 10, 10]
k = 1
x = 9

Distance from x=9:
Value: 1   1   1   10  10  10
Dist:  8   8   8    1   1   1

Closest with distance 1: [10, 10, 10]
But we need k=1, so take first: [10]
```

---

## 💡 Examples

### Example 1: Standard Case
```python
arr = [1, 2, 3, 4, 5]
result = findClosestElements(arr, k=4, x=3)
print(result)  # [1, 2, 3, 4]
```

### Example 2: Target Outside Range
```python
arr = [1, 2, 3, 4, 5]
result = findClosestElements(arr, k=4, x=-1)
print(result)  # [1, 2, 3, 4]
```

### Example 3: Target Far Right
```python
arr = [1, 2, 3, 4, 5]
result = findClosestElements(arr, k=4, x=10)
print(result)  # [2, 3, 4, 5]
```

---

## 🗣️ Interview Conversation Guide

### Phase 1: Clarification (3-5 min)

**Candidate:** "Is the array always sorted?"
**Interviewer:** "Yes, it's sorted in ascending order."

**Candidate:** "How should ties be handled? If two elements are equidistant from x?"
**Interviewer:** "Choose the smaller element."

**Candidate:** "Should the result be sorted?"
**Interviewer:** "Yes, return them in ascending order."

**Candidate:** "Can k be larger than the array length?"
**Interviewer:** "No, guaranteed that 1 ≤ k ≤ arr.length."

### Phase 2: Approach Discussion (5-8 min)

**Candidate:** "I can think of a few approaches:

**Approach 1: Sort by Distance (Naive)**
- Create pairs of (value, distance)
- Sort by distance, then by value
- Take first k elements, sort them
- Time: O(N log N), Space: O(N)

**Approach 2: Binary Search + Two Pointers (Optimal)**
- Use binary search to find the closest starting position
- Expand window using two pointers to collect k elements
- Time: O(log N + k), Space: O(1)

**Approach 3: Binary Search for Window Start (Most Elegant)**
- Binary search directly for the left boundary of k-element window
- Time: O(log(N - k) + k), Space: O(1)

I'll use **Approach 2** because it's intuitive and efficient."

### Phase 3: Implementation (15-20 min)

**Candidate:** "I'll find the closest element using binary search, then expand left and right to collect k elements."

---

## 🧠 Intuition & Approach

### Why Binary Search?

**Key Observation:** The array is sorted. We can use binary search to quickly find a starting point close to `x`, then expand outward.

**Why Not Just Sort Everything?**
- We already have a sorted array!
- Binary search gives us O(log N) to find starting point
- Two pointers give us O(k) to collect k elements
- Total: O(log N + k) << O(N log N)

### Two-Pointer Expansion Strategy

Once we have a starting point (closest element), we expand a "window" of size k:

```text
arr = [1, 2, 3, 4, 5, 6, 7, 8]
x = 5
k = 3

Step 1: Binary search finds 5 at index 4
        1  2  3  4  5  6  7  8
        0  1  2  3  4  5  6  7
                      ↑
                   start

Step 2: Expand window using two pointers
        left = 4, right = 4

Step 3: Compare distances
- arr[left-1] = 4, distance = |4-5| = 1
- arr[right+1] = 6, distance = |6-5| = 1
- Tie! Choose smaller → extend left
- Window: [4, 5]

Step 4: Continue
- arr[left-1] = 3, distance = |3-5| = 2
- arr[right+1] = 6, distance = |6-5| = 1
- 6 is closer → extend right
- Window: [4, 5, 6]

Result: [4, 5, 6]
```

---

## 📝 Solution 1: Binary Search + Two Pointers (Recommended)

```python
from typing import List
import bisect

def findClosestElements(arr: List[int], k: int, x: int) -> List[int]:
    """
    Find k closest elements to x using binary search + two pointers.
    
    Args:
        arr: Sorted array of integers
        k: Number of closest elements to find
        x: Target value
    
    Returns:
        k closest elements in ascending order
    
    Time: O(log N + k)
    Space: O(1) excluding output
    """
    n = len(arr)
    
    # Edge case: k equals array length
    if k == n:
        return arr
    
    # Binary search to find insertion point for x
    # bisect_left gives us the leftmost position where x could be inserted
    idx = bisect.bisect_left(arr, x)
    
    # Initialize two pointers around insertion point
    # left points to element just before x (or -1)
    # right points to element at or after x (or n)
    left = idx - 1
    right = idx
    
    # Expand window to collect k elements
    while k > 0:
        # If left pointer is exhausted
        if left < 0:
            right += 1
            k -= 1
            continue
        
        # If right pointer is exhausted
        if right >= n:
            left -= 1
            k -= 1
            continue
        
        # Both pointers valid: compare distances
        dist_left = abs(arr[left] - x)
        dist_right = abs(arr[right] - x)
        
        if dist_left <= dist_right:
            # Left is closer or equal (prefer smaller element)
            left -= 1
        else:
            # Right is closer
            right += 1
        
        k -= 1
    
    # Extract window [left+1, right)
    return arr[left + 1:right]


# ============================================
# COMPLETE RUNNABLE EXAMPLE
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("FIND K CLOSEST ELEMENTS")
    print("=" * 60)
    
    test_cases = [
        ([1, 2, 3, 4, 5], 4, 3, [1, 2, 3, 4]),
        ([1, 2, 3, 4, 5], 4, -1, [1, 2, 3, 4]),
        ([1, 2, 3, 4, 5], 4, 10, [2, 3, 4, 5]),
        ([1, 1, 1, 10, 10, 10], 1, 9, [10]),
        ([0, 1, 2, 2, 2, 3, 6, 8, 8, 9], 5, 9, [3, 6, 8, 8, 9]),
        ([1], 1, 1, [1]),
    ]
    
    for arr, k, x, expected in test_cases:
        result = findClosestElements(arr, k, x)
        status = "✓" if result == expected else "✗"
        print(f"{status} findClosestElements({arr}, k={k}, x={x})")
        print(f"   Result: {result}")
        if result != expected:
            print(f"   Expected: {expected}")
```

---

## 📝 Solution 2: Binary Search for Window Start (Most Elegant)

This approach directly binary searches for the **left boundary** of the k-element window.

```python
def findClosestElements_window(arr: List[int], k: int, x: int) -> List[int]:
    """
    Find k closest elements by binary searching for window start.
    
    Key Insight: The k-element window starts at some index i ∈ [0, n-k].
    We binary search for the optimal i.
    
    Time: O(log(N - k) + k)
    Space: O(1)
    """
    n = len(arr)
    left, right = 0, n - k
    
    # Binary search for the start of k-element window
    while left < right:
        mid = (left + right) // 2
        
        # Compare distances of window boundaries
        # Window: arr[mid : mid + k]
        # Left boundary: arr[mid]
        # Right boundary: arr[mid + k]
        
        # If arr[mid] is farther from x than arr[mid + k],
        # then we should move window to the right
        if x - arr[mid] > arr[mid + k] - x:
            left = mid + 1
        else:
            right = mid
    
    # left now points to optimal window start
    return arr[left:left + k]


# Test
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("SOLUTION 2: BINARY SEARCH FOR WINDOW")
    print("=" * 60)
    
    arr = [1, 2, 3, 4, 5]
    result = findClosestElements_window(arr, k=4, x=3)
    print(f"Result: {result}")  # [1, 2, 3, 4]
```

**Why This Works:**

Consider window starting at index `mid`:
- Left boundary: `arr[mid]`
- Right boundary: `arr[mid + k]`

If `x - arr[mid] > arr[mid + k] - x`:
- Left element is farther from x than right element
- We should shift window to the right

Otherwise:
- Left element is closer or equal → keep this window or search left

---

## 🔍 Explanation with Example

**Example:** `arr = [1, 2, 3, 4, 5]`, `k = 4`, `x = 3`

### Using Binary Search + Two Pointers

**Step 1: Binary search for insertion point**
```
arr = [1, 2, 3, 4, 5]
x = 3

bisect_left(arr, 3) = 2
(3 would be inserted at index 2)
```

**Step 2: Initialize pointers**
```
left = 2 - 1 = 1  (points to 2)
right = 2         (points to 3)

  1   2   3   4   5
  0   1   2   3   4
      ↑   ↑
    left right
```

**Step 3: Expand window (k = 4)**

```
Iteration 1:
- dist_left = |2 - 3| = 1
- dist_right = |3 - 3| = 0
- 0 < 1 → extend right
- Window: [2, 3]
- left = 1, right = 3

Iteration 2:
- dist_left = |2 - 3| = 1
- dist_right = |4 - 3| = 1
- Tie! 1 <= 1 → extend left (prefer smaller)
- Window: [2, 3, 4] → Actually [left+1, right) = [1, 3, 4]
Wait, let me recalculate...

Actually:
After extending right in iteration 1:
left = 1, right = 3, k = 3

Iteration 2:
- dist_left = |arr[1] - 3| = |2 - 3| = 1
- dist_right = |arr[3] - 3| = |4 - 3| = 1
- Tie: extend left
- left = 0, right = 3, k = 2

Iteration 3:
- dist_left = |arr[0] - 3| = |1 - 3| = 2
- dist_right = |arr[3] - 3| = |4 - 3| = 1
- 1 < 2 → extend right
- left = 0, right = 4, k = 1

Iteration 4:
- dist_left = |arr[0] - 3| = |1 - 3| = 2
- dist_right = |arr[4] - 3| = |5 - 3| = 2
- Tie: extend left
- left = -1, right = 4, k = 0

Window: arr[0:4] = [1, 2, 3, 4] ✓
```

---

## 🔍 Complexity Analysis

### Solution 1: Binary Search + Two Pointers

**Time Complexity: O(log N + k)**
- Binary search: O(log N)
- Two-pointer expansion: O(k)
- Extracting subarray: O(k)
- **Total:** O(log N + k)

**Space Complexity: O(1)**
- Excluding output array
- Only constant extra variables

### Solution 2: Binary Search for Window

**Time Complexity: O(log(N - k) + k)**
- Binary search range: [0, N - k] → O(log(N - k))
- Extracting subarray: O(k)
- **Total:** O(log(N - k) + k)

**Space Complexity: O(1)**

### Comparison

| Approach | Time | Space | Pros | Cons |
|----------|------|-------|------|------|
| **Sort by distance** | O(N log N) | O(N) | Simple logic | Wastes sorted array |
| **Binary Search + Two Pointers** | O(log N + k) | O(1) | Intuitive | More code |
| **Window Binary Search** | O(log(N-k) + k) | O(1) | Elegant, minimal code | Less intuitive |

---

## ⚠️ Common Pitfalls

### 1. **Forgetting Tie-Breaking Rule**

**Problem:**
```python
# ❌ WRONG: Doesn't prefer smaller element in ties
if dist_left < dist_right:  # Should be <=
    left -= 1
```

**Fix:** Use `<=` to prefer the left (smaller) element.

---

### 2. **Off-by-One in Window Extraction**

**Problem:**
```python
# ❌ WRONG: arr[left:right] might be wrong
return arr[left:right]
```

**Why it fails:** After loop, `left` is one position before window start.

**Fix:** `return arr[left + 1:right]` or track window correctly.

---

### 3. **Not Handling Edge Cases**

**Edge Cases to Test:**
- `k == n` (return entire array)
- `x < arr[0]` (all elements on right)
- `x > arr[n-1]` (all elements on left)
- `x` exactly in array vs. not in array

---

## 🔄 Follow-up Questions

### Follow-up 1: Unsorted Array

**Problem Statement:**
> "What if the array is not sorted? How would you adapt the solution?"

**Solution:**

```python
def findClosestElements_unsorted(arr: List[int], k: int, x: int) -> List[int]:
    """
    Find k closest elements in unsorted array.
    
    Time: O(N log k) using max-heap
    Space: O(k)
    """
    import heapq
    
    # Max-heap of (-distance, -value, value)
    # Negative for max-heap behavior
    heap = []
    
    for num in arr:
        dist = abs(num - x)
        
        # Python's heapq is min-heap, so negate for max-heap
        heapq.heappush(heap, (-dist, -num, num))
        
        if len(heap) > k:
            heapq.heappop(heap)
    
    # Extract values and sort
    result = [num for _, _, num in heap]
    result.sort()
    
    return result
```

**Time Complexity:** O(N log k)
**Space Complexity:** O(k)

---

### Follow-up 2: Stream of Elements

**Problem Statement:**
> "Elements arrive one at a time. Maintain k closest elements to x dynamically."

**Solution:**

```python
import heapq
from typing import List

class ClosestTracker:
    """
    Maintain k closest elements to x in a stream.
    """
    
    def __init__(self, k: int, x: int):
        self.k = k
        self.x = x
        # Max-heap: (-distance, -value)
        self.heap = []
    
    def add(self, num: int) -> None:
        """
        Add new element to stream.
        
        Time: O(log k)
        """
        dist = abs(num - self.x)
        
        if len(self.heap) < self.k:
            heapq.heappush(self.heap, (-dist, -num))
        else:
            # Compare with max (top of heap)
            if -self.heap[0][0] > dist:
                heapq.heapreplace(self.heap, (-dist, -num))
    
    def get_closest(self) -> List[int]:
        """
        Get current k closest elements.
        
        Time: O(k log k) for sorting
        """
        result = [-val for _, val in self.heap]
        result.sort()
        return result


# Test
tracker = ClosestTracker(k=3, x=5)
for num in [1, 4, 6, 8, 2]:
    tracker.add(num)
    print(f"After adding {num}: {tracker.get_closest()}")
```

---

### Follow-up 3: 2D Closest Points

**Problem Statement:**
> "Given points in 2D space, find k closest points to origin (0, 0)."

This is **LeetCode 973 - K Closest Points to Origin**.

**Solution:**

```python
import heapq
from typing import List

def kClosest(points: List[List[int]], k: int) -> List[List[int]]:
    """
    Find k closest points to origin.
    
    Time: O(N log k)
    Space: O(k)
    """
    # Max-heap of (-distance, point)
    heap = []
    
    for x, y in points:
        dist = x * x + y * y  # Squared distance (no sqrt needed)
        
        heapq.heappush(heap, (-dist, [x, y]))
        
        if len(heap) > k:
            heapq.heappop(heap)
    
    return [point for _, point in heap]


# Test
points = [[1, 3], [-2, 2], [5, 8], [0, 1]]
result = kClosest(points, k=2)
print(result)  # [[0, 1], [-2, 2]] or [[-2, 2], [0, 1]]
```

---

## 🧪 Test Cases

```python
def test_find_closest():
    # Test 1: Standard case
    assert findClosestElements([1, 2, 3, 4, 5], 4, 3) == [1, 2, 3, 4]
    
    # Test 2: Target left of array
    assert findClosestElements([1, 2, 3, 4, 5], 4, -1) == [1, 2, 3, 4]
    
    # Test 3: Target right of array
    assert findClosestElements([1, 2, 3, 4, 5], 4, 10) == [2, 3, 4, 5]
    
    # Test 4: k equals array length
    assert findClosestElements([1, 2, 3], 3, 2) == [1, 2, 3]
    
    # Test 5: Single element
    assert findClosestElements([1], 1, 2) == [1]
    
    # Test 6: Duplicate elements
    assert findClosestElements([1, 1, 2, 2, 2, 3], 3, 2) == [1, 2, 2]
    
    # Test 7: Tie-breaking
    assert findClosestElements([1, 2, 3, 4, 5], 2, 3) == [2, 3]
    
    print("All tests passed! ✓")


if __name__ == "__main__":
    test_find_closest()
```

---

## 🎯 Key Takeaways

1. **Binary Search on Sorted Arrays** is powerful for O(log N) operations.
2. **Two Pointers** work well for expanding/shrinking windows.
3. **Heap (Priority Queue)** is the go-to for unsorted data.
4. **Tie-Breaking Rules** matter—always clarify with interviewer.
5. **Edge Cases:** Test boundaries (k=n, x outside range, duplicates).

---

## 📚 Related Problems

- **LeetCode 658:** Find K Closest Elements (exact problem)
- **LeetCode 973:** K Closest Points to Origin (2D variant)
- **LeetCode 347:** Top K Frequent Elements (heap pattern)
- **LeetCode 215:** Kth Largest Element (QuickSelect)
- **LeetCode 378:** Kth Smallest Element in Sorted Matrix

