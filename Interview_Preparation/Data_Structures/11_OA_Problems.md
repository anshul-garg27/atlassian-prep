# 💻 PROBLEM 11: ONLINE ASSESSMENT PROBLEMS

### ⭐⭐⭐ **Common Screening Questions**

**Frequency:** High (Karat / Hackerrank)

This section covers smaller, logic-heavy problems often seen in the initial screening (OA) round.

---

### 1️⃣ **The MEX Problem (Minimum Excluded)**

**Problem:**
> Given an array of integers, find the **Minimum Excluded** positive integer (MEX).
> That is, the smallest positive integer `> 0` that is NOT present in the array.

**Example:**
```text
[1, 2, 3] -> 4
[3, 2, 1] -> 4
[4, 5, 6] -> 1 (Since 1 is missing)
[0, 2, 3] -> 1 (0 is not positive/or ignored depending on spec)
[-5, 1, 3] -> 2
```

**Approach:**
1.  **Set approach (O(N)):** Put all numbers in a Set. Iterate 1, 2, 3... until not found.
2.  **In-place Swap (O(N) Time, O(1) Space):**
    - Try to put value `x` at index `x-1`. (Put 1 at index 0, 2 at index 1...).
    - Ignore values $\le 0$ or $> N$.
    - After arranging, scan array. The first index `i` where `arr[i] != i+1` is the answer.

```python
def first_missing_positive(nums):
    n = len(nums)
    for i in range(n):
        # While nums[i] is in valid range [1, n] AND not in correct spot
        while 1 <= nums[i] <= n and nums[nums[i]-1] != nums[i]:
            # Swap to correct spot
            correct_idx = nums[i] - 1
            nums[i], nums[correct_idx] = nums[correct_idx], nums[i]
            
    for i in range(n):
        if nums[i] != i + 1:
            return i + 1
            
    return n + 1
```

---

### 2️⃣ **Perfect Break (Advertising/Breaks)**

**Problem:**
> You have a video of length `L` minutes.
> You want to insert an ad break.
> Users have watched intervals `[start, end]`.
> Find a time `t` to insert the ad such that it does NOT interrupt any user's active session? Or minimizes interruptions?
>
> (Variation: Find the "Perfect Break" where 0 users are watching).

**Approach:**
> This is **Interval Merging** or **Line Sweep**.
> If looking for 0 interruptions: Merge all user intervals. The gaps between merged intervals are the "Perfect Breaks".

**Example:**
```text
Users: [0, 5], [10, 15], [4, 8]
Merged: [0, 8], [10, 15]
Gap: (8, 10). Any time t in 8 < t < 10 is perfect.
```

```python
def find_perfect_breaks(intervals, video_length):
    if not intervals:
        return [(0, video_length)]

    # 1. Sort by start time
    intervals.sort()
    
    # 2. Merge
    merged = []
    for start, end in intervals:
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
            
    # 3. Find Gaps
    gaps = []
    curr_time = 0
    for start, end in merged:
        if start > curr_time:
            gaps.append((curr_time, start))
        curr_time = max(curr_time, end)
        
    if curr_time < video_length:
        gaps.append((curr_time, video_length))
        
    return gaps
```

---

### 🧪 **Test Cases**

**MEX:**
- `[1, 2, 0]` -> 3.
- `[]` -> 1.
- `[7, 8, 9]` -> 1.

**Breaks:**
- No users: Full video is a gap.
- Full coverage `[0, 100]`: No gap.
- Disjoint `[0, 10], [20, 30]`: Gap `(10, 20)` and `(30, End)`.
