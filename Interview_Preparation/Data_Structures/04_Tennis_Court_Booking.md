# 🎾 PROBLEM 4: TENNIS COURT BOOKING

### ⭐⭐⭐ **Expanding Tennis Club**

**Frequency:** Medium (Appears in ~30% of rounds)
**Similar to:** [LeetCode 253 - Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii/)

**Problem Statement:**
> You manage a tennis club. You have a list of court booking requests. Each request has a `start` time and an `end` time.
>
> You want to accept **all** bookings.
>
> **Task:** Assign each booking to a specific court (Court 1, Court 2, etc.) such that no two bookings on the same court overlap. Minimize the total number of courts needed.

**Visual Example:**
```text
Bookings:
A: [0, 30]
B: [10, 20]
C: [15, 45]
D: [50, 70]

Timeline:
0----10----15----20----30----45----50----70-->

Court 1: [A: 0-30] ................. [D: 50-70]
Court 2: .. [B: 10-20]
Court 3: ....... [C: 15-45]

Total Courts: 3
Note: B ends at 20, but C starts at 15, so C cannot use Court 2.
```

**Example Input/Output:**
```python
bookings = [
    BookingRecord(id=1, start=0, finish=30),
    BookingRecord(id=2, start=15, finish=45),
    BookingRecord(id=3, start=10, finish=20),
    BookingRecord(id=4, start=50, finish=70)
]

# Possible Output
# Court 1: Booking 1, Booking 4
# Court 2: Booking 3
# Court 3: Booking 2
```

---

### 🗣️ **Interview Conversation Guide**

**Phase 1: Clarification**
- **Candidate:** "Do we just need the *count* of courts, or the actual assignment?"
- **Interviewer:** "Let's say we need the actual assignment."
- **Candidate:** "What if `end_time` of one meeting equals `start_time` of another? Do they overlap?"
- **Interviewer:** "No, [10, 20] and [20, 30] do NOT overlap."
- **Candidate:** "Is the input sorted?"
- **Interviewer:** "No, assume unsorted."

**Phase 2: Approach**
- **Candidate:** "This is a classic Interval scheduling problem. We can think of it greedily."
- **Candidate:** "If we sort meetings by start time, we can process them one by one."
- **Candidate:** "For each meeting, we check if any existing court is free. If yes, reuse it. If no, create a new court."
- **Candidate:** "To efficiently find a free court (specifically the one that finishes earliest), we can use a **Min-Heap** storing end times."

**Phase 3: Coding**
- Define `BookingRecord` and `Court` classes.
- Sort bookings.
- Use `heapq` to manage court availability.

---

### 📝 **Solution Approach: Greedy with Min-Heap**

We want to fit a new booking into an *existing* court if possible.
Which court is the best candidate? Any court that becomes free **before** the new booking starts.
Ideally, the court that becomes free *closest* to the start time to minimize gaps, but for minimizing *total courts*, just picking *any* free court works.

**Algorithm:**
1.  **Sort** bookings by `start_time`.
2.  Use a **Min-Heap** to track active courts.
    *   Heap stores: `(end_time, court_index)`.
    *   The top of the heap tells us the **earliest** time a court becomes free.
3.  For each booking:
    *   Check if `heap.min_end_time <= booking.start_time`.
    *   **If Yes:** We can reuse that court. Pop from heap, update end time, push back.
    *   **If No:** All courts are busy. Allocate a new court. Push new court to heap.

**Implementation:**

```python
import heapq
from dataclasses import dataclass
from typing import List

@dataclass
class BookingRecord:
    id: int
    start_time: int
    finish_time: int

@dataclass
class Court:
    court_id: int
    bookings: List[BookingRecord]
    available_at: int = 0  # When this court becomes free

def assign_courts(booking_records: List[BookingRecord]) -> List[Court]:
    if not booking_records:
        return []

    # 1. Sort by start time
    bookings = sorted(booking_records, key=lambda x: x.start_time)

    courts = []
    
    # Min-heap stores: (available_time, court_index)
    # This allows us to efficiently find a free court
    court_heap = []

    for booking in bookings:
        # Check if the earliest available court is free before this booking starts
        if court_heap and court_heap[0][0] <= booking.start_time:
            # Reuse existing court
            available_time, court_idx = heapq.heappop(court_heap)
            
            # Add booking to this court
            courts[court_idx].bookings.append(booking)
            courts[court_idx].available_at = booking.finish_time

            # Push back with new available time
            heapq.heappush(court_heap, (booking.finish_time, court_idx))
        else:
            # Need new court
            court_idx = len(courts)
            new_court = Court(
                court_id=court_idx + 1,
                bookings=[booking],
                available_at=booking.finish_time
            )
            courts.append(new_court)
            
            # Push to heap
            heapq.heappush(court_heap, (booking.finish_time, court_idx))

    return courts

# Time Complexity: O(N log N) for sorting. O(N log K) for heap ops (K = num courts).
# Space Complexity: O(K) for heap.
```

---

### 📝 **Alternative: Line Sweep (Count Only)**

If the interviewer only asks for the **number** of courts needed (not the schedule), use Line Sweep.

1.  Separate start and end times.
2.  Start time = `+1` court needed.
3.  End time = `-1` court needed.
4.  Sort events. Iterate and track max running sum.

```python
def min_courts_needed(bookings: List[BookingRecord]) -> int:
    events = []
    for b in bookings:
        events.append((b.start_time, 1))   # Start
        events.append((b.finish_time, -1)) # End (court freed)

    # Sort: time ascending.
    # Tie-break: Process END (-1) before START (1) to minimize courts
    # (If one game ends at 10 and another starts at 10, we can reuse).
    events.sort(key=lambda x: (x[0], x[1]))

    current_courts = 0
    max_courts = 0

    for _, change in events:
        current_courts += change
        max_courts = max(max_courts, current_courts)

    return max_courts
```

---

### 🔧 **Follow-up 1: Maintenance Time**

**Problem:**
> After every booking, the court needs `X` minutes of maintenance before it can be used again.

**Solution:**
> Effectively, the booking "occupies" the court until `end_time + maintenance_time`.
> Just modify the heap push:
> `heapq.heappush(court_heap, (booking.finish_time + maintenance_time, court_idx))`

```python
def assign_courts_with_maintenance(bookings, maintenance_time):
    # ... sort ...
    for booking in bookings:
        if court_heap and court_heap[0][0] <= booking.start_time:
            _, court_idx = heapq.heappop(court_heap)
            # ... add booking ...
            
            # Next available time includes maintenance
            heapq.heappush(court_heap, (booking.finish_time + maintenance_time, court_idx))
        # ... else create new ...
```

---

### 🔧 **Follow-up 2: Periodic Maintenance**

**Problem:**
> A court only needs maintenance after every `Y` bookings (e.g., every 3 matches).

**Solution:**
> Track `bookings_count` in the heap or Court object.
> `heap element: (available_time, court_idx, bookings_since_last_maintenance)`

```python
def assign_courts_periodic(bookings, maintenance_time, limit):
    # ...
    # Heap: (available_time, court_idx, usage_count)
    
    for booking in bookings:
        if heap and heap[0][0] <= booking.start_time:
            time, idx, count = heapq.heappop(heap)
            count += 1
            
            next_free = booking.finish_time
            if count >= limit:
                next_free += maintenance_time
                count = 0 # Reset
            
            heapq.heappush(heap, (next_free, idx, count))
        else:
            # New court
            heapq.heappush(heap, (booking.finish_time, len(courts), 1))
```

---

### 🧪 **Test Cases**

**Basic Overlap:**
- Input: `[0, 10], [5, 15]`
- Output: 2 Courts.

**Reuse:**
- Input: `[0, 10], [10, 20]`
- Output: 1 Court (Ends at 10, Starts at 10).

**Nested:**
- Input: `[0, 100], [10, 20], [30, 40]`
- Output: 2 Courts (One holds [0, 100], other holds the rest).

**Empty:**
- Input: `[]`
- Output: `[]` (or 0 courts).
