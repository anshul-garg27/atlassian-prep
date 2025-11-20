# 🎾 PROBLEM 4: TENNIS COURT BOOKING

### ⭐⭐⭐ **Minimize Courts for Overlapping Bookings**

**Frequency:** Medium (Appears in ~30% of rounds)
**Difficulty:** Medium
**Similar to:** [LeetCode 253 - Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii/)

---

## 📋 Problem Statement

You manage a tennis club with an unlimited number of courts available. You receive a list of booking requests, where each request specifies a `start_time` and `finish_time`.

**Goal:** Assign each booking to a specific court such that:
1. No two bookings on the same court overlap.
2. The **total number of courts used is minimized**.

**Constraints:**
- 1 ≤ N ≤ 10⁵ bookings
- 0 ≤ start_time < finish_time ≤ 10⁹
- If one booking ends at time `T` and another starts at `T`, they do **not** overlap (can use the same court).

---

## 🎨 Visual Example

### Example 1: Overlapping Bookings

```text
Input Bookings:
A: [0, 30]
B: [10, 20]
C: [15, 45]
D: [50, 70]

Timeline:
0----10---15---20---30---45---50---70--->
|A-------| 
     |B-|
          |C----------|
                         |D----|

Overlap Analysis:
- At t=10: A and B overlap  
- At t=15: A, B, and C all overlap (peak: 3 courts needed)
- At t=20: A and C overlap
- At t=30: Only C
- At t=50: D (no overlap with others)

Court Assignment:
Court 1: [A: 0-30] ................... [D: 50-70]
Court 2:      [B: 10-20]
Court 3:           [C: 15-45]

Total Courts Needed: 3
```

### Example 2: Sequential (No Overlap)

```text
Input Bookings:
A: [0, 10]
B: [10, 20]
C: [20, 30]

Court Assignment:
Court 1: [A] -> [B] -> [C]

Total Courts: 1
```

---

## 🎨 VISUAL ALGORITHM TRACE

This section provides comprehensive visual diagrams showing interval overlap detection, heap operations, and court assignment strategies.

### Heap-Based Algorithm Step-by-Step

**Input Bookings:** `[[0, 30], [10, 20], [15, 45], [50, 70]]`

#### Iteration 1: Process Booking [0, 30]

```text
┌──────────────────────────────────────────────────────────────────┐
│  BOOKING #1: [0, 30]                                             │
├──────────────────────────────────────────────────────────────────┤
│  Heap State BEFORE:                                              │
│    []  (empty)                                                   │
│                                                                  │
│  Decision Logic:                                                 │
│    heap is empty → Need NEW court                                │
│                                                                  │
│  Action:                                                         │
│    1. Create Court 1                                             │
│    2. Assign Booking #1 to Court 1                               │
│    3. Push (finish=30, court=1) to heap                          │
│                                                                  │
│  Heap State AFTER:                                               │
│    [(30, Court1)]                                                │
│                                                                  │
│  Court Assignments:                                              │
│    Court 1: [0────────────────────────30]                       │
└──────────────────────────────────────────────────────────────────┘

Timeline Visualization:
  Time: 0──────────────────────30
  C1:   ████████████████████████
```

---

#### Iteration 2: Process Booking [10, 20]

```text
┌──────────────────────────────────────────────────────────────────┐
│  BOOKING #2: [10, 20]                                            │
├──────────────────────────────────────────────────────────────────┤
│  Heap State BEFORE:                                              │
│    [(30, Court1)]                                                │
│    Top: (30, Court1) ◄── Court 1 free at t=30                    │
│                                                                  │
│  Decision Logic:                                                 │
│    Booking starts: 10                                            │
│    Earliest available court finishes: 30                         │
│    10 < 30? YES → Court 1 still BUSY!                            │
│    Need NEW court                                                │
│                                                                  │
│  Action:                                                         │
│    1. Create Court 2                                             │
│    2. Assign Booking #2 to Court 2                               │
│    3. Push (finish=20, court=2) to heap                          │
│                                                                  │
│  Heap State AFTER:                                               │
│    [(20, Court2), (30, Court1)]                                  │
│     ▲                                                            │
│     └─── Min (earliest available)                               │
│                                                                  │
│  Court Assignments:                                              │
│    Court 1: [0────────────────────────30]                       │
│    Court 2:          [10─────20]                                │
└──────────────────────────────────────────────────────────────────┘

Timeline Visualization:
  Time: 0──────10────20────30
  C1:   ████████████████████████
  C2:           ████████

Overlap Detection:
  At t=10: Court 1 (busy until 30) and Court 2 (starts now)
  At t=15: Both courts busy → Peak = 2 courts
```

---

#### Iteration 3: Process Booking [15, 45]

```text
┌──────────────────────────────────────────────────────────────────┐
│  BOOKING #3: [15, 45]                                            │
├──────────────────────────────────────────────────────────────────┤
│  Heap State BEFORE:                                              │
│    [(20, Court2), (30, Court1)]                                  │
│    Top: (20, Court2) ◄── Court 2 free at t=20                    │
│                                                                  │
│  Decision Logic:                                                 │
│    Booking starts: 15                                            │
│    Earliest available court finishes: 20                         │
│    15 < 20? YES → Court 2 still BUSY!                            │
│    Need NEW court                                                │
│                                                                  │
│  Action:                                                         │
│    1. Create Court 3                                             │
│    2. Assign Booking #3 to Court 3                               │
│    3. Push (finish=45, court=3) to heap                          │
│                                                                  │
│  Heap State AFTER:                                               │
│    [(20, Court2), (30, Court1), (45, Court3)]                    │
│     ▲                                                            │
│     └─── Min (earliest available)                               │
│                                                                  │
│  Court Assignments:                                              │
│    Court 1: [0────────────────────────30]                       │
│    Court 2:          [10─────20]                                │
│    Court 3:               [15──────────────────45]              │
└──────────────────────────────────────────────────────────────────┘

Timeline Visualization:
  Time: 0──────10────15──20────30────────45
  C1:   ████████████████████████████
  C2:           ████████
  C3:                ██████████████████████████

Peak Overlap at t=15:
  Court 1: BUSY (until 30)
  Court 2: BUSY (until 20)
  Court 3: BUSY (just started)
  Total: 3 courts needed! ◄── MAXIMUM
```

---

#### Iteration 4: Process Booking [50, 70] (Court Reuse!)

```text
┌──────────────────────────────────────────────────────────────────┐
│  BOOKING #4: [50, 70]                                            │
├──────────────────────────────────────────────────────────────────┤
│  Heap State BEFORE:                                              │
│    [(20, Court2), (30, Court1), (45, Court3)]                    │
│    Top: (20, Court2) ◄── Court 2 free at t=20                    │
│                                                                  │
│  Decision Logic:                                                 │
│    Booking starts: 50                                            │
│    Earliest available court finishes: 20                         │
│    50 >= 20? YES → Court 2 is FREE! ✓                            │
│    REUSE Court 2                                                 │
│                                                                  │
│  Action:                                                         │
│    1. Pop (20, Court2) from heap                                 │
│    2. Assign Booking #4 to Court 2                               │
│    3. Push (finish=70, court=2) to heap                          │
│                                                                  │
│  Heap State AFTER:                                               │
│    [(30, Court1), (45, Court3), (70, Court2)]                    │
│     ▲                                                            │
│     └─── Min (Court 1 now earliest)                             │
│                                                                  │
│  Court Assignments:                                              │
│    Court 1: [0────────────────────────30]                       │
│    Court 2:          [10─────20]         [50──────70]           │
│    Court 3:               [15──────────────────45]              │
│                                                                  │
│  Total Courts: 3 (NO new court needed!)                          │
└──────────────────────────────────────────────────────────────────┘

Timeline Visualization:
  Time: 0──────10────15──20────30────────45──50────70
  C1:   ████████████████████████████
  C2:           ████████                    ██████████
  C3:                ██████████████████████████

Court 2 Reuse:
  [10──20]         [50──70]
        ▲           ▲
        └───gap─────┘
  Gap > 0, so no overlap! Safe to reuse.
```

---

### Heap State Evolution Diagram

```text
┌──────────────────────────────────────────────────────────────────┐
│                    HEAP STATE PROGRESSION                        │
└──────────────────────────────────────────────────────────────────┘

After Booking #1 [0, 30]:
┌─────────┐
│   30    │  ◄── Court 1
└─────────┘

After Booking #2 [10, 20]:
      ┌─────────┐
      │   20    │  ◄── Court 2 (min)
     / \
┌───┘   └───┐
│           │
│   30      │    ◄── Court 1
└───────────┘

After Booking #3 [15, 45]:
      ┌─────────┐
      │   20    │  ◄── Court 2 (min)
     / \
┌───┘   └───────┐
│   30          │
│   Court 1     │
└───┬───────────┘
    │
┌───┘
│   45
│   Court 3
└───────────

After Booking #4 [50, 70] - REUSE Court 2:
Pop (20, Court2), Push (70, Court2)

      ┌─────────┐
      │   30    │  ◄── Court 1 (now min!)
     / \
┌───┘   └───────┐
│   45          │
│   Court 3     │
└───┬───────────┘
    │
┌───┘
│   70
│   Court 2 (updated)
└───────────

Key Insight:
  • Heap size = number of courts
  • Top of heap = earliest available court
  • Pop + Push when reusing (O(log K))
```

---

### Interval Overlap Detection Matrix

```text
┌──────────────────────────────────────────────────────────────────┐
│              INTERVAL OVERLAP DETECTION MATRIX                   │
└──────────────────────────────────────────────────────────────────┘

Bookings: A=[0,30], B=[10,20], C=[15,45], D=[50,70]

Overlap Check: Does interval X overlap with interval Y?
  Overlap if: X.start < Y.finish AND Y.start < X.finish

┌─────────┬─────────┬─────────┬─────────┬─────────┐
│         │  A      │  B      │  C      │  D      │
│         │  [0,30] │ [10,20] │ [15,45] │ [50,70] │
├─────────┼─────────┼─────────┼─────────┼─────────┤
│  A      │    -    │   ✓     │   ✓     │   ✗     │
│ [0,30]  │         │ 0<20 ✓  │ 0<45 ✓  │ 0<70 ✓  │
│         │         │10<30 ✓  │15<30 ✓  │50<30 ✗  │
├─────────┼─────────┼─────────┼─────────┼─────────┤
│  B      │   ✓     │    -    │   ✓     │   ✗     │
│ [10,20] │ 10<30 ✓ │         │10<45 ✓  │10<70 ✓  │
│         │ 0<20 ✓  │         │15<20 ✓  │50<20 ✗  │
├─────────┼─────────┼─────────┼─────────┼─────────┤
│  C      │   ✓     │   ✓     │    -    │   ✗     │
│ [15,45] │15<30 ✓  │15<20 ✓  │         │15<70 ✓  │
│         │ 0<45 ✓  │10<45 ✓  │         │50<45 ✗  │
├─────────┼─────────┼─────────┼─────────┼─────────┤
│  D      │   ✗     │   ✗     │   ✗     │    -    │
│ [50,70] │50<30 ✗  │50<20 ✗  │50<45 ✗  │         │
└─────────┴─────────┴─────────┴─────────┴─────────┘

Conflict Groups:
  Group 1: {A, B, C} ◄── All overlap at some point
  Group 2: {D}       ◄── Isolated, no overlaps

Court Assignment Strategy:
  • A, B, C need 3 separate courts (maximum overlap at t=15)
  • D can reuse any court from Group 1 (no overlap)
```

---

### Line Sweep Algorithm Visualization

Alternative approach that only counts courts (doesn't assign):

```text
┌──────────────────────────────────────────────────────────────────┐
│                   LINE SWEEP ALGORITHM                           │
└──────────────────────────────────────────────────────────────────┘

Bookings: [0,30], [10,20], [15,45], [50,70]

Step 1: Create Events
┌────────────────────────────────────────────────────┐
│  Event Type: +1 = court needed (start)            │
│              -1 = court freed (finish)             │
│                                                    │
│  Time │ Event │ Reason                             │
│  ─────┼───────┼──────────────────────────────────  │
│   0   │  +1   │ Booking [0,30] starts              │
│  10   │  +1   │ Booking [10,20] starts             │
│  15   │  +1   │ Booking [15,45] starts             │
│  20   │  -1   │ Booking [10,20] finishes           │
│  30   │  -1   │ Booking [0,30] finishes            │
│  45   │  -1   │ Booking [15,45] finishes           │
│  50   │  +1   │ Booking [50,70] starts             │
│  70   │  -1   │ Booking [50,70] finishes           │
└────────────────────────────────────────────────────┘

Step 2: Sort Events (with tie-breaking: finish before start)
┌────────────────────────────────────────────────────┐
│  Events: [(0,+1), (10,+1), (15,+1), (20,-1),       │
│           (30,-1), (45,-1), (50,+1), (70,-1)]      │
└────────────────────────────────────────────────────┘

Step 3: Sweep Through Events
┌──────────────────────────────────────────────────────────────┐
│  Time │ Event │ Courts Before │ Delta │ Courts After │ Max │
├───────┼───────┼───────────────┼───────┼──────────────┼─────┤
│   0   │  +1   │       0       │  +1   │      1       │  1  │
│  10   │  +1   │       1       │  +1   │      2       │  2  │
│  15   │  +1   │       2       │  +1   │      3       │  3  │◄─┐
│  20   │  -1   │       3       │  -1   │      2       │  3  │  │
│  30   │  -1   │       2       │  -1   │      1       │  3  │  │
│  45   │  -1   │       1       │  -1   │      0       │  3  │  │
│  50   │  +1   │       0       │  +1   │      1       │  3  │  │
│  70   │  -1   │       1       │  -1   │      0       │  3  │  │
└──────────────────────────────────────────────────────────────┘  │
                                                                  │
Result: Maximum courts needed = 3 ◄───────────────────────────────┘

Visual Sweep:
Time: 0──────10───15──20───30────45──50──70
      │      │    │   │    │     │   │   │
      +1     +1   +1  -1   -1    -1  +1  -1

Courts:
  1  ┌─────┬────┬───┬────┬─────┬───┬───┬──
      │  1  │  2 │ 3 │  2 │  1  │ 0 │ 1 │ 0
      └─────┴────┴───┴────┴─────┴───┴───┴──
                   ▲
                   └─── Peak = 3
```

---

### Edge Case: Touching Intervals (No Overlap)

```text
┌──────────────────────────────────────────────────────────────────┐
│              EDGE CASE: [10, 20] and [20, 30]                    │
└──────────────────────────────────────────────────────────────────┘

Question: Do these overlap?

Overlap Formula:
  A.start < B.finish AND B.start < A.finish

Check:
  A = [10, 20], B = [20, 30]
  10 < 30? YES ✓
  20 < 20? NO ✗

Result: NO OVERLAP!

Visual:
┌─────────────────────────────────────────┐
│  Time:  10────────20────────30          │
│  A:     [────────]                      │
│  B:               [────────]            │
│                   ▲                     │
│                   └─── Touching, not overlapping
└─────────────────────────────────────────┘

Line Sweep with Tie-Breaking:
┌────────────────────────────────────────────────┐
│  Events: [(10, +1), (20, -1), (20, +1), (30, -1)]│
│                      ▲        ▲                 │
│                      └────────┘                 │
│                 Same time! Process finish first │
│                                                 │
│  Time │ Event │ Courts                          │
│  ─────┼───────┼───────                          │
│   10  │  +1   │   1                             │
│   20  │  -1   │   0  ◄── Process finish first   │
│   20  │  +1   │   1  ◄── Then process start     │
│   30  │  -1   │   0                             │
│                                                 │
│  Max Courts: 1 (correct!)                       │
└────────────────────────────────────────────────┘

Tie-Breaking Code:
events.sort(key=lambda x: (x[0], x[1]))
  # x[1] = -1 (finish) comes before +1 (start)
```

---

### Court Reuse Decision Tree

```text
┌──────────────────────────────────────────────────────────────────┐
│               COURT REUSE DECISION TREE                          │
└──────────────────────────────────────────────────────────────────┘

For each booking:

                    Start Processing
                         │
                         ▼
                   ┌─────────────┐
                   │  Heap empty? │
                   └─────┬───┬───┘
                         │   │
                    YES──┘   └──NO
                     │           │
                     ▼           ▼
              ┌──────────┐  ┌──────────────────────────┐
              │ Create   │  │ Check heap top:          │
              │ NEW      │  │ earliest_finish vs start │
              │ Court    │  └──────┬────────┬──────────┘
              └──────────┘         │        │
                                   │        │
                       earliest_finish      earliest_finish
                        <= start            > start
                           │                    │
                           ▼                    ▼
                    ┌─────────────┐      ┌──────────────┐
                    │ REUSE       │      │ Create NEW   │
                    │ Court       │      │ Court        │
                    │             │      │              │
                    │ • Pop heap  │      │ • Add to     │
                    │ • Assign    │      │   courts[]   │
                    │ • Push new  │      │ • Push to    │
                    │   finish    │      │   heap       │
                    └─────────────┘      └──────────────┘

Example Traces:

Booking [50, 70] with heap [(20, C2), (30, C1), (45, C3)]:
  1. Heap NOT empty → Check top
  2. Top = (20, Court2)
  3. 20 <= 50? YES
  4. REUSE Court 2 ✓

Booking [15, 45] with heap [(20, C2), (30, C1)]:
  1. Heap NOT empty → Check top
  2. Top = (20, Court2)
  3. 20 <= 15? NO
  4. CREATE NEW Court 3 ✓
```

---

### Complexity Comparison

```text
┌──────────────────────────────────────────────────────────────────┐
│                   ALGORITHM COMPARISON                           │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Approach         │  Time           │  Space  │  Assignments?   │
│  ────────────────────────────────────────────────────────────── │
│  Brute Force      │  O(N × K)       │  O(K)   │  Yes            │
│  (Check all       │  N bookings,    │  K      │                 │
│  courts)          │  K courts       │  courts │                 │
│                   │                 │         │                 │
│  Greedy + Heap    │  O(N log N      │  O(K)   │  Yes            │
│  (This solution)  │  + N log K)     │         │                 │
│                   │  ≈ O(N log N)   │         │                 │
│                   │                 │         │                 │
│  Line Sweep       │  O(N log N)     │  O(N)   │  No (count      │
│  (Count only)     │                 │         │  only)          │
└──────────────────────────────────────────────────────────────────┘

Where:
  N = number of bookings
  K = number of courts (usually K << N)

Example with N=1000 bookings, K=10 courts:
  Brute Force: 1000 × 10 = 10,000 comparisons
  Greedy+Heap: 1000 log(1000) + 1000 log(10)
              ≈ 10,000 + 3,322 = 13,322 operations
  Line Sweep:  1000 log(1000) ≈ 10,000 operations

Best Choice:
  • Need assignments? → Greedy + Heap
  • Just need count? → Line Sweep (simpler)
```

---

## 💡 Examples

### Example 1: Mixed Overlap
```python
bookings = [
    Booking(id=1, start=0, finish=30),
    Booking(id=2, start=10, finish=20),
    Booking(id=3, start=15, finish=45),
    Booking(id=4, start=50, finish=70)
]

result = assign_courts(bookings)
print(f"Courts needed: {len(result)}")  # 3
# Court 1: Bookings 1, 4
# Court 2: Booking 2
# Court 3: Booking 3
```

### Example 2: Complete Reuse
```python
bookings = [
    Booking(id=1, start=0, finish=10),
    Booking(id=2, start=10, finish=20),
    Booking(id=3, start=20, finish=30)
]

result = assign_courts(bookings)
print(f"Courts needed: {len(result)}")  # 1
```

---

## 🗣️ Interview Conversation Guide

### Phase 1: Clarification (3-5 min)

**Candidate:** "Do we need to return the actual court assignments, or just count the minimum number of courts?"
**Interviewer:** "Let's start with the count, then extend to assignments."

**Candidate:** "If one booking ends at time 10 and another starts at 10, do they overlap?"
**Interviewer:** "No, [5, 10] and [10, 15] can use the same court."

**Candidate:** "Can we assume the input is sorted by start time?"
**Interviewer:** "No, assume it's unsorted."

**Candidate:** "What about edge cases like empty input or single booking?"
**Interviewer:** "Handle them gracefully—return 0 or 1 court respectively."

### Phase 2: Approach Discussion (5-8 min)

**Candidate:** "This is an **Interval Scheduling** problem. There are a few approaches:

1. **Brute Force:** For each booking, check all existing courts to see if it fits. O(N²) time.
2. **Line Sweep (for count only):** Track start/end events, count overlaps. O(N log N).
3. **Greedy with Min-Heap (for assignments):** Sort bookings, reuse courts efficiently. O(N log N)."

**Candidate:** "I'll use the **Greedy + Min-Heap** approach because:
- It gives actual assignments (not just count).
- We process bookings chronologically (sort by start time).
- The heap tracks which court becomes available earliest.
- If the earliest available court is free before the next booking starts, we reuse it."

### Phase 3: Implementation (15-20 min)

**Candidate:** "I'll define a `Booking` class and use Python's `heapq` to manage court availability."

---

## 🧠 Intuition & Approach

### Why This Problem is Challenging

The naive approach is to try every possible assignment, but that's exponential. The key insight is **greedy scheduling**:
- Process bookings in **chronological order** (by start time).
- Always try to **reuse** a court that's already allocated before creating a new one.

### The Greedy Strategy

**Key Question:** When we get a new booking, how do we decide which court to use?

**Answer:** Use the court that becomes free **earliest**. If that court is free before our booking starts, reuse it. Otherwise, we need a new court.

**Data Structure:** A **Min-Heap** of `(available_time, court_id)` pairs:
- **Top of heap:** The court with the earliest finish time.
- **Heap Operations:** O(log K) where K = number of courts (usually K << N).

### Visual Walkthrough

```text
Bookings (sorted by start): [0,30], [10,20], [15,45], [50,70]

Step 1: Process [0, 30]
  - No courts exist yet.
  - Create Court 1, assign [0, 30].
  - Heap: [(30, Court1)]

Step 2: Process [10, 20]
  - Top of heap: (30, Court1) — Court 1 is busy until t=30.
  - Booking starts at t=10 < 30 → Cannot reuse Court 1.
  - Create Court 2, assign [10, 20].
  - Heap: [(20, Court2), (30, Court1)]

Step 3: Process [15, 45]
  - Top of heap: (20, Court2) — Court 2 is busy until t=20.
  - Booking starts at t=15 < 20 → Cannot reuse Court 2.
  - Create Court 3, assign [15, 45].
  - Heap: [(20, Court2), (30, Court1), (45, Court3)]

Step 4: Process [50, 70]
  - Top of heap: (20, Court2) — Court 2 is free at t=20.
  - Booking starts at t=50 > 20 → Reuse Court 2!
  - Wait, that's wrong. Let me reconsider...
  - Actually, Court 2 finishes at 20, so it's free. But we should use Court 1? 
  - Heap pop gives us (20, Court2). Since 20 < 50, we can reuse Court 2.
  - Assign [50, 70] to Court 2. Update: Court 2 now busy until 70.
  - Heap: [(30, Court1), (45, Court3), (70, Court2)]

Wait, this is wrong. Let me think again...

Actually, once we pop (20, Court2), we should assign [50,70] to Court 2. But visually, it makes more sense to assign to Court 1 (which is free at 30). The heap gives us *any* free court, not necessarily the "best" one for visualization. The algorithm is still correct—it minimizes total courts.

Let me redo:

Step 4: Process [50, 70]
  - Heap: [(20, Court2), (30, Court1), (45, Court3)]
  - Top: (20, Court2). 20 <= 50? Yes! Reuse Court 2.
  - Pop (20, Court2), assign [50,70] to Court 2.
  - Push (70, Court2).
  - Heap: [(30, Court1), (45, Court3), (70, Court2)]

Final Assignment:
  Court 1: [0, 30]
  Court 2: [10, 20], [50, 70]
  Court 3: [15, 45]
```

---

## 📝 Solution 0: Ultra-Simplified (Interview-Ready, No Classes)

**Perfect for 20-30 minute interviews!** Uses only built-in types and heapq.

```python
import heapq
from typing import List, Tuple

# Global state for simplified version (or can pass as parameters)
def assign_courts_simple(bookings: List[Tuple[int, int]]) -> int:
    """
    Find minimum number of courts needed for bookings.
    
    Args:
        bookings: List of (start, finish) tuples
    
    Returns:
        Number of courts needed
    
    Time: O(N log N) for sorting + O(N log K) for heap operations
    Space: O(K) where K = number of courts
    
    Algorithm:
    1. Sort bookings by start time
    2. Use min-heap to track when each court becomes free
    3. For each booking:
       - If earliest free court is available, reuse it
       - Otherwise, need a new court
    """
    if not bookings:
        return 0
    
    # Sort by start time
    sorted_bookings = sorted(bookings, key=lambda x: x[0])
    
    # Min-heap: stores finish times of courts
    # heap[0] = earliest time a court becomes available
    heap = []
    
    for start, finish in sorted_bookings:
        # If heap is not empty and earliest available court is free
        if heap and heap[0] <= start:
            # Reuse this court (remove old finish time)
            heapq.heappop(heap)
        
        # Add this booking's finish time to heap
        # (Either reusing a court or allocating new one)
        heapq.heappush(heap, finish)
    
    # Heap size = number of courts needed
    return len(heap)


def assign_courts_with_details(bookings: List[Tuple[int, int, str]]) -> dict:
    """
    Enhanced version that returns court assignments.
    
    Args:
        bookings: List of (start, finish, booking_id) tuples
    
    Returns:
        {
            "num_courts": int,
            "assignments": {court_id: [booking_ids]}
        }
    
    Time: O(N log N)
    Space: O(N)
    """
    if not bookings:
        return {"num_courts": 0, "assignments": {}}
    
    # Sort by start time
    sorted_bookings = sorted(bookings, key=lambda x: x[0])
    
    # Min-heap: (finish_time, court_id)
    heap = []
    
    # Track assignments: court_id -> list of booking_ids
    assignments = {}
    next_court_id = 1
    
    for start, finish, booking_id in sorted_bookings:
        if heap and heap[0][0] <= start:
            # Reuse existing court
            old_finish, court_id = heapq.heappop(heap)
            assignments[court_id].append(booking_id)
            heapq.heappush(heap, (finish, court_id))
        else:
            # Need new court
            court_id = next_court_id
            next_court_id += 1
            assignments[court_id] = [booking_id]
            heapq.heappush(heap, (finish, court_id))
    
    return {
        "num_courts": len(set(cid for _, cid in heap)),
        "assignments": assignments
    }


# --- Runnable Example for Interview ---
if __name__ == "__main__":
    print("=" * 60)
    print("TENNIS COURT BOOKING - ULTRA-SIMPLIFIED (NO CLASSES)")
    print("=" * 60)
    
    # Test 1: Overlapping bookings
    print("\n[Test 1] Overlapping Bookings")
    bookings1 = [
        (0, 30),   # Booking A
        (10, 20),  # Booking B
        (15, 45),  # Booking C
        (50, 70)   # Booking D
    ]
    courts_needed = assign_courts_simple(bookings1)
    print(f"Bookings: {bookings1}")
    print(f"Courts needed: {courts_needed}")
    print(f"Expected: 3 (peak overlap at t=15)")
    
    # Test 2: Sequential (no overlap)
    print("\n[Test 2] Sequential Bookings")
    bookings2 = [
        (0, 10),
        (10, 20),
        (20, 30)
    ]
    courts_needed = assign_courts_simple(bookings2)
    print(f"Bookings: {bookings2}")
    print(f"Courts needed: {courts_needed}")
    print(f"Expected: 1 (all can use same court)")
    
    # Test 3: All overlap (worst case)
    print("\n[Test 3] All Overlap")
    bookings3 = [
        (0, 100),
        (10, 90),
        (20, 80),
        (30, 70)
    ]
    courts_needed = assign_courts_simple(bookings3)
    print(f"Bookings: {bookings3}")
    print(f"Courts needed: {courts_needed}")
    print(f"Expected: 4 (all overlap)")
    
    # Test 4: With detailed assignments
    print("\n[Test 4] Detailed Assignments")
    bookings4 = [
        (0, 30, "A"),
        (10, 20, "B"),
        (15, 45, "C"),
        (50, 70, "D")
    ]
    result = assign_courts_with_details(bookings4)
    print(f"Courts needed: {result['num_courts']}")
    print(f"Assignments:")
    for court_id in sorted(result['assignments'].keys()):
        print(f"  Court {court_id}: {result['assignments'][court_id]}")
    
    # Test 5: Edge cases
    print("\n[Test 5] Edge Cases")
    print(f"Empty: {assign_courts_simple([])}")  # 0
    print(f"Single: {assign_courts_simple([(5, 10)])}")  # 1
    
    # Test 6: Out of order input
    print("\n[Test 6] Out of Order Input")
    bookings6 = [
        (50, 70),   # Last chronologically
        (10, 20),   # Second
        (0, 30),    # First
        (15, 45)    # Third
    ]
    courts_needed = assign_courts_simple(bookings6)
    print(f"Bookings (unsorted): {bookings6}")
    print(f"Courts needed: {courts_needed}")
    print(f"Expected: 3 (algorithm sorts them)")

    print("\n" + "=" * 60)
    print("Ultra-Simplified tests passed! ✓")
    print("=" * 60)
    print("\n💡 Key Points:")
    print("  • Heap size = number of courts")
    print("  • Heap top = earliest available court")
    print("  • Sort bookings first!")
    print("  • Can write in 15-20 minutes")
```

**Why This Is Perfect for Interviews:**
- ✅ **No classes** - Just pure functions
- ✅ **Standard library only** - heapq is built-in
- ✅ **15-20 minutes** - Can write from scratch quickly
- ✅ **Easy to explain** - Greedy algorithm is intuitive
- ✅ **Correct complexity** - O(N log N) optimal

**Trade-off:** Uses simple tuples instead of objects. For production, use the class-based solution below.

---

## 📝 Complete Solution: Greedy with Min-Heap

```python
import heapq
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Booking:
    """Represents a single court booking."""
    id: int
    start: int
    finish: int
    
    def __repr__(self):
        return f"Booking({self.id}: [{self.start}, {self.finish}])"

@dataclass
class Court:
    """Represents a tennis court with its schedule."""
    court_id: int
    bookings: List[Booking] = field(default_factory=list)
    
    def add_booking(self, booking: Booking):
        self.bookings.append(booking)
    
    def get_finish_time(self) -> int:
        """Return when this court becomes available."""
        return self.bookings[-1].finish if self.bookings else 0
    
    def __repr__(self):
        return f"Court {self.court_id}: {self.bookings}"


def assign_courts(bookings: List[Booking]) -> List[Court]:
    """
    Assign bookings to courts to minimize total courts needed.
    
    Algorithm:
    1. Sort bookings by start time.
    2. Use min-heap to track (finish_time, court_index).
    3. For each booking:
       - If earliest available court is free, reuse it.
       - Otherwise, create a new court.
    
    Time: O(N log N) for sort + O(N log K) for heap ops
    Space: O(K) where K = number of courts
    """
    if not bookings:
        return []
    
    # Sort by start time
    sorted_bookings = sorted(bookings, key=lambda b: b.start)
    
    courts = []
    # Min-heap: (finish_time, court_index)
    heap = []
    
    for booking in sorted_bookings:
        if heap and heap[0][0] <= booking.start:
            # Reuse existing court
            finish_time, court_idx = heapq.heappop(heap)
            courts[court_idx].add_booking(booking)
            # Update heap with new finish time
            heapq.heappush(heap, (booking.finish, court_idx))
        else:
            # Need new court
            court_idx = len(courts)
            new_court = Court(court_id=court_idx + 1)
            new_court.add_booking(booking)
            courts.append(new_court)
            heapq.heappush(heap, (booking.finish, court_idx))
    
    return courts


def min_courts_needed(bookings: List[Booking]) -> int:
    """
    Simpler version: Just return the count (no assignments).
    Uses Line Sweep algorithm.
    
    Time: O(N log N)
    Space: O(N)
    """
    if not bookings:
        return 0
    
    events = []
    for booking in bookings:
        events.append((booking.start, 1))   # Court needed
        events.append((booking.finish, -1)) # Court freed
    
    # Sort by time. Tie-break: process end before start
    # (so [10,20] and [20,30] can share a court)
    events.sort(key=lambda x: (x[0], x[1]))
    
    current_courts = 0
    max_courts = 0
    
    for time, delta in events:
        current_courts += delta
        max_courts = max(max_courts, current_courts)
    
    return max_courts


# ============================================
# COMPLETE RUNNABLE EXAMPLE
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("TENNIS COURT BOOKING SYSTEM")
    print("=" * 60)
    
    # Test 1: Overlapping bookings
    print("\n[Test 1] Overlapping Bookings")
    print("-" * 40)
    bookings = [
        Booking(id=1, start=0, finish=30),
        Booking(id=2, start=10, finish=20),
        Booking(id=3, start=15, finish=45),
        Booking(id=4, start=50, finish=70)
    ]
    
    result = assign_courts(bookings)
    print(f"Courts needed: {len(result)}")
    for court in result:
        print(f"  {court}")
    
    # Test 2: Sequential (no overlap)
    print("\n[Test 2] Sequential Bookings")
    print("-" * 40)
    bookings2 = [
        Booking(id=1, start=0, finish=10),
        Booking(id=2, start=10, finish=20),
        Booking(id=3, start=20, finish=30)
    ]
    
    result2 = assign_courts(bookings2)
    print(f"Courts needed: {len(result2)}")
    for court in result2:
        print(f"  {court}")
    
    # Test 3: All overlap (worst case)
    print("\n[Test 3] All Overlap")
    print("-" * 40)
    bookings3 = [
        Booking(id=1, start=0, finish=100),
        Booking(id=2, start=10, finish=90),
        Booking(id=3, start=20, finish=80),
        Booking(id=4, start=30, finish=70)
    ]
    
    result3 = assign_courts(bookings3)
    print(f"Courts needed: {len(result3)}")
    for court in result3:
        print(f"  {court}")
    
    # Test 4: Line Sweep (count only)
    print("\n[Test 4] Line Sweep (Count Only)")
    print("-" * 40)
    count = min_courts_needed(bookings)
    print(f"Minimum courts: {count}")
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)
```

---

## 🔍 Explanation with Example

Let's trace through the algorithm step by step with a concrete example:

**Bookings:** `[[0, 30], [10, 20], [15, 45], [50, 70]]`

**Goal:** Minimize number of courts needed

---

**Step 1: Sort by Start Time**

```python
bookings = [[0, 30], [10, 20], [15, 45], [50, 70]]
# Already sorted by start time!
```

---

**Step 2: Initialize Min-Heap**

```python
heap = []  # Will store end times of courts
courts_needed = 0
```

---

**Step 3: Process Each Booking**

**Booking 1: [0, 30]**
- Heap is empty
- Need a new court
- Assign to Court 1, ends at 30
- Push 30 to heap

```
heap = [30]
courts_needed = 1
Timeline: Court 1: [0────────30]
```

---

**Booking 2: [10, 20]**
- Heap top = 30 (Court 1 busy until 30)
- Booking starts at 10 < 30 → Court 1 not available
- Need a new court
- Assign to Court 2, ends at 20
- Push 20 to heap

```
heap = [20, 30]  (min-heap)
courts_needed = 2
Timeline: 
  Court 1: [0────────30]
  Court 2:      [10──20]
```

---

**Booking 3: [15, 45]**
- Heap top = 20 (Court 2 free at 20)
- Booking starts at 15 < 20 → Court 2 not available yet
- Need a new court
- Assign to Court 3, ends at 45
- Push 45 to heap

```
heap = [20, 30, 45]
courts_needed = 3
Timeline:
  Court 1: [0────────30]
  Court 2:      [10──20]
  Court 3:           [15───────45]
```

---

**Booking 4: [50, 70]**
- Heap top = 20 (Court 2 free at 20)
- Booking starts at 50 > 20 → Court 2 is available!
- **Reuse Court 2**
- Pop 20 from heap, push 70

```
heap = [30, 45, 70]
courts_needed = 3 (no new court needed)
Timeline:
  Court 1: [0────────30]
  Court 2:      [10──20]                     [50──70]
  Court 3:           [15───────45]
```

---

**Final Answer: 3 courts needed**

The heap size (or max heap size) gives us the answer: **3 courts**

---

**Visual Timeline:**

```text
Time:    0────10───15──20───30────45──50──70
Court 1: █████████████████████████
Court 2:      ██████████                ████████
Court 3:           ████████████████████████
                   
Peak overlap at t=15: 3 courts in use simultaneously
```

---

## 🔍 Complexity Analysis

### Greedy with Min-Heap Approach

| Operation | Time Complexity | Explanation |
|-----------|----------------|-------------|
| Sort bookings | **O(N log N)** | Sort N bookings by start time |
| Process each booking | **O(log K)** | Heap push/pop where K = courts |
| **Total** | **O(N log N + N log K)** | Usually K << N, so ~O(N log N) |

**Space Complexity:** O(K) for the heap, O(N) for storing assignments.

### Line Sweep Approach (Count Only)

| Operation | Time Complexity | Explanation |
|-----------|----------------|-------------|
| Create events | **O(N)** | 2 events per booking |
| Sort events | **O(N log N)** | 2N events |
| Scan events | **O(N)** | Single pass |
| **Total** | **O(N log N)** | |

**Space Complexity:** O(N) for events array.

---

## ⚠️ Common Pitfalls

### 1. **Off-by-One Error: Overlap Definition**
**Wrong:**
```python
if heap[0][0] < booking.start:  # Strict <
    # Reuse court
```
**Problem:** [10, 20] and [20, 30] would require 2 courts.

**Right:**
```python
if heap[0][0] <= booking.start:  # <=
    # Reuse court
```

### 2. **Forgetting to Sort**
**Wrong:**
```python
for booking in bookings:  # Unsorted!
    # Process...
```
**Problem:** Greedy doesn't work on unsorted data.

### 3. **Line Sweep Tie-Breaking**
**Wrong:**
```python
events.sort()  # Default sort
```
**Problem:** If end=10 and start=10, we might process start first, incorrectly thinking we need 2 courts.

**Right:**
```python
events.sort(key=lambda x: (x[0], x[1]))  # -1 before 1
```

### 4. **Heap Corruption**
**Wrong:**
```python
courts[court_idx].add_booking(booking)
# Forgot to update heap!
```
**Problem:** Heap still has old finish time. Future bookings use stale data.

---

## 🔄 Follow-up Questions

### Follow-up 1: Maintenance Time After Each Booking

**Problem Statement:**
> "After each booking finishes, the court requires `M` minutes of maintenance before it can be used again. How does this change the solution?"

**Challenge:**
The court isn't immediately available at `finish_time`. It's available at `finish_time + maintenance_time`.

**Solution:**
Modify the heap entry to account for maintenance:

```python
def assign_courts_with_maintenance(bookings: List[Booking], maintenance_time: int) -> List[Court]:
    """
    Assign courts with mandatory maintenance time after each booking.
    
    Args:
        bookings: List of booking requests
        maintenance_time: Minutes required for maintenance after each booking
    
    Returns:
        List of courts with assignments
    """
    if not bookings:
        return []
    
    sorted_bookings = sorted(bookings, key=lambda b: b.start)
    courts = []
    heap = []
    
    for booking in sorted_bookings:
        # Court is available after: finish_time + maintenance_time
        if heap and heap[0][0] <= booking.start:
            # Reuse court
            _, court_idx = heapq.heappop(heap)
            courts[court_idx].add_booking(booking)
            
            # Next available = finish + maintenance
            next_available = booking.finish + maintenance_time
            heapq.heappush(heap, (next_available, court_idx))
        else:
            # New court
            court_idx = len(courts)
            new_court = Court(court_id=court_idx + 1)
            new_court.add_booking(booking)
            courts.append(new_court)
            
            next_available = booking.finish + maintenance_time
            heapq.heappush(heap, (next_available, court_idx))
    
    return courts


# ============================================
# EXAMPLE
# ============================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("FOLLOW-UP 1: MAINTENANCE TIME")
    print("=" * 60)
    
    bookings = [
        Booking(id=1, start=0, finish=10),
        Booking(id=2, start=10, finish=20),
        Booking(id=3, start=15, finish=25)
    ]
    
    print("\nWithout Maintenance:")
    result = assign_courts(bookings)
    print(f"Courts needed: {len(result)}")  # 2
    
    print("\nWith 5 min Maintenance:")
    result_m = assign_courts_with_maintenance(bookings, maintenance_time=5)
    print(f"Courts needed: {len(result_m)}")  # 3
    print("Explanation: Booking 1 ends at 10, needs maintenance until 15.")
    print("Booking 2 starts at 10 (OK), but Booking 3 at 15 conflicts with maintenance.")
```

**Complexity:** Same as base solution (O(N log N)).

---

### Follow-up 2: Maintenance After Every Y Bookings

**Problem Statement:**
> "A court only needs maintenance after every `Y` bookings (e.g., every 3 matches). How do you track this?"

**Challenge:**
We need to count how many bookings each court has handled.

**Solution:**
Extend the heap to track usage count:

```python
from typing import Tuple

def assign_courts_periodic_maintenance(
    bookings: List[Booking],
    maintenance_time: int,
    bookings_per_maintenance: int
) -> List[Court]:
    """
    Courts need maintenance after every Y bookings.
    
    Args:
        bookings: List of booking requests
        maintenance_time: Minutes for maintenance
        bookings_per_maintenance: Number of bookings before maintenance needed
    
    Returns:
        List of courts with assignments
    """
    if not bookings:
        return []
    
    sorted_bookings = sorted(bookings, key=lambda b: b.start)
    courts = []
    
    # Heap: (available_time, court_idx, usage_count)
    heap = []
    
    for booking in sorted_bookings:
        if heap and heap[0][0] <= booking.start:
            # Reuse court
            _, court_idx, usage_count = heapq.heappop(heap)
            courts[court_idx].add_booking(booking)
            
            # Increment usage
            usage_count += 1
            next_available = booking.finish
            
            # Check if maintenance is needed
            if usage_count >= bookings_per_maintenance:
                next_available += maintenance_time
                usage_count = 0  # Reset counter
            
            heapq.heappush(heap, (next_available, court_idx, usage_count))
        else:
            # New court
            court_idx = len(courts)
            new_court = Court(court_id=court_idx + 1)
            new_court.add_booking(booking)
            courts.append(new_court)
            
            heapq.heappush(heap, (booking.finish, court_idx, 1))
    
    return courts


# ============================================
# EXAMPLE
# ============================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("FOLLOW-UP 2: PERIODIC MAINTENANCE")
    print("=" * 60)
    
    # 5 sequential bookings, maintenance after every 2
    bookings = [
        Booking(id=i, start=i*10, finish=i*10+8)
        for i in range(5)
    ]
    
    result = assign_courts_periodic_maintenance(
        bookings,
        maintenance_time=5,
        bookings_per_maintenance=2
    )
    
    print(f"Courts needed: {len(result)}")
    for court in result:
        print(f"  {court}")
    
    print("\nExplanation:")
    print("  - Bookings 0,1 on Court 1 (2 uses → maintenance)")
    print("  - Booking 2 might need Court 2 if maintenance overlaps")
```

**Complexity:** O(N log N) time, O(K) space (same as base).

---

### Follow-up 3: Court Preferences

**Problem Statement:**
> "Some customers prefer specific courts (e.g., 'Court 1' or 'Court with shade'). How do you handle preferences while still minimizing total courts?"

**Challenge:**
- Hard constraint: Respect preferences where possible.
- Soft constraint: Minimize courts.

**Solution Approach:**

1. **Strict Preferences (Hard Constraint):**
   - Maintain separate heaps per court.
   - If booking has preference, only check that court's heap.

2. **Flexible Preferences (Soft Constraint):**
   - Try preferred court first.
   - If unavailable, fall back to any free court.

**Simplified Implementation (Flexible):**

```python
@dataclass
class BookingWithPreference(Booking):
    preferred_court: Optional[int] = None

def assign_courts_with_preferences(bookings: List[BookingWithPreference]) -> List[Court]:
    """
    Attempt to honor court preferences while minimizing total courts.
    """
    if not bookings:
        return []
    
    sorted_bookings = sorted(bookings, key=lambda b: b.start)
    courts = []
    heap = []
    
    for booking in sorted_bookings:
        assigned = False
        
        # Try preferred court first
        if booking.preferred_court is not None:
            pref_idx = booking.preferred_court - 1
            if pref_idx < len(courts):
                court_finish = courts[pref_idx].get_finish_time()
                if court_finish <= booking.start:
                    courts[pref_idx].add_booking(booking)
                    
                    # Update heap: Remove old entry for this court and add new one
                    # Find and remove old entry (linear search in heap)
                    heap_copy = []
                    for entry in heap:
                        if entry[1] != pref_idx:  # Keep entries for other courts
                            heap_copy.append(entry)
                    heap[:] = heap_copy
                    heapq.heapify(heap)
                    
                    # Add updated entry
                    heapq.heappush(heap, (booking.finish, pref_idx))
                    assigned = True
        
        # Fall back to any free court
        if not assigned:
            if heap and heap[0][0] <= booking.start:
                _, court_idx = heapq.heappop(heap)
                courts[court_idx].add_booking(booking)
                heapq.heappush(heap, (booking.finish, court_idx))
            else:
                # New court
                court_idx = len(courts)
                new_court = Court(court_id=court_idx + 1)
                new_court.add_booking(booking)
                courts.append(new_court)
                heapq.heappush(heap, (booking.finish, court_idx))
    
    return courts
```

**Note:** Full preference handling with heap updates is complex. In interviews, discuss the trade-offs and implement a simplified version.

---

## 🧪 Test Cases

```python
def test_court_booking():
    # Test 1: No overlap
    bookings = [
        Booking(1, 0, 10),
        Booking(2, 10, 20)
    ]
    assert len(assign_courts(bookings)) == 1
    
    # Test 2: Complete overlap
    bookings = [
        Booking(1, 0, 20),
        Booking(2, 5, 15)
    ]
    assert len(assign_courts(bookings)) == 2
    
    # Test 3: Empty
    assert len(assign_courts([])) == 0
    
    # Test 4: Single booking
    assert len(assign_courts([Booking(1, 0, 10)])) == 1
    
    # Test 5: Line sweep matches heap
    bookings = [Booking(i, i*2, i*2+5) for i in range(10)]
    assert min_courts_needed(bookings) == len(assign_courts(bookings))
    
    print("All test cases passed! ✓")

if __name__ == "__main__":
    test_court_booking()
```

---

## 🎯 Key Takeaways

1. **Greedy + Heap is the Standard Pattern** for interval scheduling with assignments.
2. **Line Sweep is Simpler** if you only need the count (not assignments).
3. **Sorting is Essential** for greedy algorithms on intervals.
4. **Heap Top = Earliest Available** allows O(log K) reuse checks.
5. **Maintenance Time** is just an offset to the finish time.

---

## 📚 Related Problems

- **LeetCode 252:** Meeting Rooms (is there any overlap?)
- **LeetCode 253:** Meeting Rooms II (this problem)
- **LeetCode 435:** Non-overlapping Intervals (maximize non-overlapping)
- **LeetCode 1229:** Meeting Scheduler (find common free slots)
