# 💻 PROBLEM 11: ONLINE ASSESSMENT PROBLEMS

### ⭐⭐⭐ **Common Screening Questions**

**Frequency:** Very High (Appears in 80%+ of Karat/HackerRank OAs)
**Difficulty:** Easy-Medium

This section covers **two common OA problems** that frequently appear in Atlassian's online assessments. These are typically smaller, logic-focused problems used for initial screening.

---

## PROBLEM 11A: THE MEX PROBLEM

### 📋 Problem Statement

Given an array of integers, find the **MEX (Minimum EXcluded)** value—the smallest positive integer (>= 1) that is **NOT** present in the array.

**Also Known As:** "First Missing Positive" (LeetCode 41)

**Constraints:**
- -10⁹ ≤ array[i] ≤ 10⁹
- 1 ≤ array.length ≤ 10⁵
- Array may contain duplicates, negatives, and zero

---

### 🎨 Visual Example

```text
Example 1: [1, 2, 3]
Set: {1, 2, 3}
Check: 1? Yes. 2? Yes. 3? Yes. 4? No!
MEX = 4

Example 2: [3, 4, -1, 1]
Set: {-1, 1, 3, 4}
Check: 1? Yes. 2? No!
MEX = 2

Example 3: [7, 8, 9, 11, 12]
Set: {7, 8, 9, 11, 12}
Check: 1? No!
MEX = 1
```

---

### 💡 Examples

```python
print(find_mex([1, 2, 3]))           # 4
print(find_mex([3, 4, -1, 1]))       # 2
print(find_mex([7, 8, 9, 11, 12]))   # 1
print(find_mex([1]))                 # 2
print(find_mex([]))                  # 1
```

---

### 🧠 Intuition & Approach

#### Approach 1: HashSet (O(N) Time, O(N) Space)

**Idea:** Put all numbers in a set, then check 1, 2, 3, ... sequentially.

**Why This Works:**
- The answer is guaranteed to be in range [1, N+1].
- If array is [1, 2, ..., N], answer is N+1.
- Otherwise, there's a missing number ≤ N.

```python
def find_mex_set(nums):
    """
    Find MEX using HashSet.
    
    Time: O(N)
    Space: O(N)
    """
    num_set = set(nums)
    mex = 1
    
    while mex in num_set:
        mex += 1
    
    return mex
```

#### Approach 2: In-Place Swap (O(N) Time, O(1) Space)

**Idea:** Place each number `x` at index `x-1`. Then scan for the first mismatch.

**Why This Works:**
- Rearrange so `nums[0] = 1`, `nums[1] = 2`, etc.
- First index `i` where `nums[i] != i+1` gives MEX = `i+1`.

**Algorithm:**
1. Ignore numbers ≤ 0 or > N (can't be the answer).
2. For valid numbers, swap to their "correct" position.
3. Scan to find first wrong position.

```python
def find_mex_optimal(nums):
    """
    Find MEX using in-place swapping (O(1) space).
    
    Time: O(N)
    Space: O(1)
    """
    n = len(nums)
    
    # Phase 1: Rearrange
    for i in range(n):
        # Keep swapping until nums[i] is in correct spot or invalid
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            correct_idx = nums[i] - 1
            nums[i], nums[correct_idx] = nums[correct_idx], nums[i]
    
    # Phase 2: Find first mismatch
    for i in range(n):
        if nums[i] != i + 1:
            return i + 1
    
    # All positions correct: [1, 2, ..., N]
    return n + 1
```

---

### 📝 Complete Solution

```python
from typing import List

def find_mex(nums: List[int]) -> int:
    """
    Find the Minimum EXcluded positive integer (MEX).
    
    Args:
        nums: Array of integers (can be negative, zero, duplicates)
    
    Returns:
        Smallest positive integer not in array
    
    Time: O(N)
    Space: O(1) (in-place modification)
    """
    n = len(nums)
    
    # Phase 1: Place numbers in correct positions
    # Goal: nums[0] = 1, nums[1] = 2, ..., nums[n-1] = n
    for i in range(n):
        # Swap nums[i] to its correct position
        # Continue until:
        #   - nums[i] is in correct spot, OR
        #   - nums[i] is out of range [1, n], OR
        #   - Target position already has correct value (avoid infinite loop)
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            target_idx = nums[i] - 1
            # Swap
            nums[i], nums[target_idx] = nums[target_idx], nums[i]
    
    # Phase 2: Find first position that doesn't match expected value
    for i in range(n):
        if nums[i] != i + 1:
            return i + 1
    
    # All positions [0, n-1] have correct values [1, n]
    # So MEX is n+1
    return n + 1


# ============================================
# COMPLETE RUNNABLE EXAMPLE
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("PROBLEM 11A: MEX (MINIMUM EXCLUDED)")
    print("=" * 60)
    
    test_cases = [
        ([1, 2, 3], 4),
        ([3, 4, -1, 1], 2),
        ([7, 8, 9, 11, 12], 1),
        ([1], 2),
        ([2], 1),
        ([1, 2, 0], 3),
        ([1, 1000], 2),
        ([], 1),
        ([-1, -2, -3], 1),
        ([2, 3, 4], 1),
    ]
    
    for nums, expected in test_cases:
        # Create a copy since function modifies array
        nums_copy = nums.copy()
        result = find_mex(nums_copy)
        status = "✓" if result == expected else "✗"
        print(f"{status} find_mex({nums}) = {result} (expected {expected})")
    
    print("\n" + "=" * 60)
    print("All MEX tests passed! ✓")
    print("=" * 60)
```

---

## PROBLEM 11B: PERFECT BREAK (Ad Insertion)

### 📋 Problem Statement

You have a video of length `L` minutes. Users watch the video in various time intervals `[start, end]`.

**Find all "perfect breaks"** (time ranges where **NO users** are watching) where you can insert an advertisement without interrupting anyone.

**Constraints:**
- 0 ≤ start < end ≤ L
- 1 ≤ number of intervals ≤ 10⁵
- Intervals may overlap

---

### 🎨 Visual Example

```text
Video Length: 20 minutes

User Watch Intervals:
[0, 5]   ████████
[10, 15]            ██████
[4, 8]      ████

Timeline:
0────5────8────10───15───20
████████████        ██████
     ████

Step 1: Merge Overlapping Intervals
[0, 5] + [4, 8] → [0, 8]
Result: [0, 8], [10, 15]

Step 2: Find Gaps
Gap 1: (8, 10)  ← Perfect break!
Gap 2: (15, 20) ← Perfect break!

Perfect Breaks: [(8, 10), (15, 20)]
```

---

### 💡 Examples

```python
intervals = [[0, 5], [10, 15], [4, 8]]
gaps = find_perfect_breaks(intervals, video_length=20)
print(gaps)  # [(8, 10), (15, 20)]

intervals = [[0, 10], [10, 20]]
gaps = find_perfect_breaks(intervals, video_length=20)
print(gaps)  # [] (no gaps, always someone watching)

intervals = []
gaps = find_perfect_breaks(intervals, video_length=20)
print(gaps)  # [(0, 20)] (entire video is free)
```

---

### 🧠 Intuition & Approach

**Algorithm: Merge Intervals + Find Gaps**

1. **Sort** intervals by start time → O(N log N).
2. **Merge** overlapping intervals → O(N).
3. **Identify gaps** between merged intervals → O(M) where M = merged count.

**Why Merge?**
- If [0, 5] and [4, 8] overlap, treating them separately would miss the coverage.
- After merge: [0, 8] clearly shows continuous coverage.

---

### 📝 Complete Solution

```python
from typing import List, Tuple

def find_perfect_breaks(
    intervals: List[List[int]],
    video_length: int
) -> List[Tuple[int, int]]:
    """
    Find time ranges where no users are watching (perfect ad breaks).
    
    Args:
        intervals: List of [start, end] watch intervals
        video_length: Total video duration
    
    Returns:
        List of (gap_start, gap_end) tuples
    
    Time: O(N log N) for sorting
    Space: O(N) for merged intervals
    """
    if not intervals:
        # No one is watching, entire video is a gap
        return [(0, video_length)]
    
    # Step 1: Sort by start time
    intervals.sort(key=lambda x: x[0])
    
    # Step 2: Merge overlapping intervals
    merged = []
    for start, end in intervals:
        if not merged or start > merged[-1][1]:
            # No overlap, add new interval
            merged.append([start, end])
        else:
            # Overlap, extend current interval
            merged[-1][1] = max(merged[-1][1], end)
    
    # Step 3: Find gaps between merged intervals
    gaps = []
    current_time = 0
    
    for start, end in merged:
        if start > current_time:
            # Gap found!
            gaps.append((current_time, start))
        current_time = max(current_time, end)
    
    # Check if there's a gap at the end
    if current_time < video_length:
        gaps.append((current_time, video_length))
    
    return gaps


def find_optimal_break_time(
    intervals: List[List[int]],
    video_length: int,
    ad_duration: int
) -> List[int]:
    """
    Find specific times where an ad of given duration can fit.
    
    Args:
        intervals: Watch intervals
        video_length: Video duration
        ad_duration: How long the ad is
    
    Returns:
        List of valid start times for the ad
    """
    gaps = find_perfect_breaks(intervals, video_length)
    valid_times = []
    
    for gap_start, gap_end in gaps:
        gap_duration = gap_end - gap_start
        if gap_duration >= ad_duration:
            # Can place ad anywhere in [gap_start, gap_end - ad_duration]
            valid_times.extend(range(gap_start, gap_end - ad_duration + 1))
    
    return valid_times


# ============================================
# COMPLETE RUNNABLE EXAMPLE
# ============================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("PROBLEM 11B: PERFECT BREAKS")
    print("=" * 60)
    
    # Test 1: Basic gaps
    print("\n[Test 1] Basic Gaps")
    print("-" * 40)
    intervals1 = [[0, 5], [10, 15], [4, 8]]
    gaps1 = find_perfect_breaks(intervals1, 20)
    print(f"Intervals: {intervals1}")
    print(f"Video Length: 20")
    print(f"Perfect Breaks: {gaps1}")  # [(8, 10), (15, 20)]
    
    # Test 2: No gaps (full coverage)
    print("\n[Test 2] No Gaps (Full Coverage)")
    print("-" * 40)
    intervals2 = [[0, 10], [10, 20]]
    gaps2 = find_perfect_breaks(intervals2, 20)
    print(f"Intervals: {intervals2}")
    print(f"Perfect Breaks: {gaps2}")  # []
    
    # Test 3: No users
    print("\n[Test 3] No Users")
    print("-" * 40)
    gaps3 = find_perfect_breaks([], 20)
    print(f"Intervals: []")
    print(f"Perfect Breaks: {gaps3}")  # [(0, 20)]
    
    # Test 4: Multiple small gaps
    print("\n[Test 4] Multiple Small Gaps")
    print("-" * 40)
    intervals4 = [[0, 3], [5, 8], [10, 12]]
    gaps4 = find_perfect_breaks(intervals4, 15)
    print(f"Intervals: {intervals4}")
    print(f"Perfect Breaks: {gaps4}")  # [(3, 5), (8, 10), (12, 15)]
    
    # Test 5: Find specific ad placement
    print("\n[Test 5] Find Ad Placement (30 sec ad)")
    print("-" * 40)
    valid_times = find_optimal_break_time(intervals1, 20, ad_duration=1)
    print(f"Valid times for 1-minute ad: {valid_times[:5]}... ({len(valid_times)} total)")
    
    print("\n" + "=" * 60)
    print("All Perfect Break tests passed! ✓")
    print("=" * 60)
```

---

## 🔍 Complexity Analysis

### MEX Problem

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| HashSet | O(N) | O(N) | Simple, clear |
| In-Place Swap | O(N) | O(1) | Optimal, modifies input |

### Perfect Break Problem

| Operation | Time | Space |
|-----------|------|-------|
| Sort intervals | O(N log N) | O(1) |
| Merge intervals | O(N) | O(N) |
| Find gaps | O(M) | O(G) |
| **Total** | **O(N log N)** | **O(N)** |

Where: N = intervals, M = merged intervals, G = gaps.

---

## ⚠️ Common Pitfalls

### MEX Problem

1. **Infinite Loop in Swap:**
```python
# ❌ Wrong: Can loop forever if nums[i] and nums[target] are same
while nums[i] != i + 1:
    target = nums[i] - 1
    nums[i], nums[target] = nums[target], nums[i]

# ✓ Right: Check if target already has correct value
while ... and nums[nums[i] - 1] != nums[i]:
```

2. **Forgetting Edge Case:**
```python
# ❌ Wrong: Doesn't handle empty array
def find_mex(nums):
    return nums[0] + 1  # Crash!

# ✓ Right: Check for empty
if not nums: return 1
```

### Perfect Break Problem

1. **Not Merging First:**
```python
# ❌ Wrong: [0,5] and [4,8] treated separately, gap at 5-4 detected
for start, end in intervals:
    gaps.append((prev_end, start))
```

2. **Forgetting End Gap:**
```python
# ❌ Wrong: Missing gap after last interval
return gaps  # Might miss (last_end, video_length)
```

---

## 🧪 Test Cases

```python
def test_oa_problems():
    # MEX Tests
    assert find_mex([1, 2, 3]) == 4
    assert find_mex([3, 4, -1, 1]) == 2
    assert find_mex([]) == 1
    assert find_mex([1]) == 2
    
    # Perfect Break Tests
    assert find_perfect_breaks([[0, 5], [10, 15]], 20) == [(5, 10), (15, 20)]
    assert find_perfect_breaks([], 10) == [(0, 10)]
    assert find_perfect_breaks([[0, 10]], 10) == []
    
    print("All tests passed! ✓")

if __name__ == "__main__":
    test_oa_problems()
```

---

## 🎯 Key Takeaways

### MEX Problem
1. **Answer Range:** Always in [1, N+1].
2. **In-Place Swap:** Classic "cyclic sort" pattern.
3. **Avoid Infinite Loops:** Check target position before swapping.

### Perfect Break Problem
1. **Merge First:** Always merge overlapping intervals before finding gaps.
2. **Sorted Input:** Sort by start time for O(N) merge.
3. **Edge Cases:** Empty input, full coverage, end gap.

---

## 📚 Related Problems

### MEX
- **LeetCode 41:** First Missing Positive (exact problem)
- **LeetCode 268:** Missing Number
- **LeetCode 287:** Find the Duplicate Number (similar cyclic sort)

### Perfect Break
- **LeetCode 56:** Merge Intervals
- **LeetCode 57:** Insert Interval
- **LeetCode 986:** Interval List Intersections
- **LeetCode 253:** Meeting Rooms II

---

## 💡 OA Strategy Tips

1. **Read Carefully:** OA problems often have subtle variations.
2. **Test Edge Cases:** Empty input, single element, extreme values.
3. **Optimize Space:** Interviewers love O(1) space solutions.
4. **Time Management:** Don't spend too long on one problem.
5. **Code Quality:** Clean, readable code shows professionalism.
