# 🗳️ PROBLEM 9: VOTE COUNTING & LEADERBOARD

### ⭐⭐⭐ **Election Winner with Tie-Breaking**

**Frequency:** Medium (Appears in ~25% of rounds)
**Difficulty:** Easy-Medium
**Similar to:** [LeetCode 347 - Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/), Sorting with Custom Comparators

---

## 📋 Problem Statement

You are implementing a voting system for an election. Given a list of votes (candidate names), determine:

1. **Part 1 (Basic):** Who is the winner? (Most votes)
2. **Part 2 (Tie-Breaking):** If multiple candidates have the same highest vote count, choose based on a **tie-breaking rule** (e.g., alphabetically last name).
3. **Part 3 (Leaderboard):** Return the **Top K** candidates in order.
4. **Part 4 (Weighted Voting):** Each vote has a weight (points). Calculate scores.

**Constraints:**
- 1 ≤ number of votes ≤ 10⁶
- Candidate names are non-empty strings
- Tie-breaking rule varies by problem variant

---

## 🎨 Visual Example

### Example 1: Simple Majority

```text
Votes: [Alice, Bob, Alice, Charlie, Bob, Bob]

Step 1: Count
┌──────────────┐
│ Alice   → 2  │
│ Bob     → 3  │
│ Charlie → 1  │
└──────────────┘

Step 2: Sort by Count (Descending)
1. Bob     (3)
2. Alice   (2)
3. Charlie (1)

Winner: Bob
```

### Example 2: Tie with Alphabetical Rule

```text
Votes: [Alice, Bob, Alice, Bob]

Count:
Alice → 2
Bob   → 2

Tie-Breaking Rule: "Alphabetically Last Wins"
Compare: "Bob" > "Alice" alphabetically

Winner: Bob
```

### Example 3: Weighted Voting

```text
Votes (with weights):
(Alice, 3)  ← First choice (3 points)
(Bob, 2)    ← Second choice (2 points)
(Alice, 1)  ← Third choice (1 point)

Scores:
Alice: 3 + 1 = 4
Bob: 2

Winner: Alice
```

---

## 💡 Examples

### Example 1: Basic Winner
```python
votes = ["Alice", "Bob", "Alice", "Charlie", "Bob", "Bob"]
winner = find_winner(votes)
print(winner)  # "Bob"
```

### Example 2: Tie-Breaking
```python
votes = ["Alice", "Bob"]  # Tie: both have 1 vote
winner = find_winner(votes, tie_rule="alphabetical_last")
print(winner)  # "Bob" (B > A)
```

### Example 3: Top K Leaderboard
```python
votes = ["A", "B", "A", "C", "B", "B", "D"]
leaderboard = get_top_k(votes, k=3)
print(leaderboard)  # ["B" (3), "A" (2), "C" (1)]
```

---

## 🗣️ Interview Conversation Guide

### Phase 1: Clarification (3-5 min)

**Candidate:** "Are votes given as an array or a stream?"
**Interviewer:** "Start with an array. We can discuss streaming as a follow-up."

**Candidate:** "How should ties be broken? Alphabetically first or last?"
**Interviewer:** "Let's say alphabetically **last** (e.g., 'Bob' wins over 'Alice')."

**Candidate:** "Should the output be just the winner's name, or name + count?"
**Interviewer:** "Just the name for basic version, but include counts for the leaderboard."

**Candidate:** "Are votes case-sensitive?"
**Interviewer:** "Yes, 'Alice' and 'alice' are different candidates."

### Phase 2: Approach Discussion (5-8 min)

**Candidate:** "This is a **frequency counting + sorting** problem.

**Algorithm:**
1. **Count Phase:** Use a HashMap (`Counter`) to count votes → O(N).
2. **Sort Phase:** Convert to list and sort by:
   - Primary key: Vote count (descending)
   - Secondary key: Name (descending for 'last' rule)
   - Time: O(C log C) where C = unique candidates (usually C << N).
3. **Extract:** Return top 1 (winner) or top K (leaderboard).

**Total Complexity:** O(N + C log C) ≈ O(N) when C << N."

### Phase 3: Implementation (10-15 min)

**Candidate:** "I'll use Python's `Counter` for clean counting and custom sort keys for tie-breaking."

---

## 🧠 Intuition & Approach

### Why HashMap (Counter)?

**Direct Counting:**
- One pass through votes
- O(1) increment per vote
- Handles arbitrary candidate names

### Sorting vs. Heap for Top K

| Approach | Time | When to Use |
|----------|------|-------------|
| **Full Sort** | O(C log C) | K ≈ C (need most candidates) or C is small |
| **Heap (Top K)** | O(C log K) | K << C (e.g., K=3, C=1000) |

**For interviews:** Full sort is simpler and sufficient unless C is huge.

---

## 📝 Complete Solution

```python
from collections import Counter
from typing import List, Tuple, Optional

def find_winner(
    votes: List[str],
    tie_rule: str = "alphabetical_last"
) -> Optional[str]:
    """
    Find the election winner.
    
    Args:
        votes: List of candidate names
        tie_rule: How to break ties
            - "alphabetical_last": Choose alphabetically later name
            - "alphabetical_first": Choose alphabetically earlier name
    
    Returns:
        Winner's name, or None if no votes
    
    Time: O(N + C log C)
    Space: O(C)
    """
    if not votes:
        return None
    
    # Count votes
    counts = Counter(votes)
    
    # Find max count
    max_count = max(counts.values())
    
    # Find all candidates with max count
    winners = [name for name, count in counts.items() if count == max_count]
    
    # Tie-breaking
    if tie_rule == "alphabetical_last":
        return max(winners)  # Max alphabetically
    elif tie_rule == "alphabetical_first":
        return min(winners)  # Min alphabetically
    else:
        return winners[0]  # Arbitrary


def get_leaderboard(
    votes: List[str],
    k: int = 3,
    tie_rule: str = "alphabetical_last"
) -> List[Tuple[str, int]]:
    """
    Get top K candidates with their vote counts.
    
    Args:
        votes: List of candidate names
        k: Number of top candidates to return
        tie_rule: Tie-breaking rule
    
    Returns:
        List of (name, count) tuples sorted by rank
    
    Time: O(N + C log C)
    Space: O(C)
    """
    if not votes:
        return []
    
    counts = Counter(votes)
    candidates = list(counts.items())
    
    # Sort by (count desc, name desc) for alphabetical_last
    if tie_rule == "alphabetical_last":
        candidates.sort(key=lambda x: (x[1], x[0]), reverse=True)
    elif tie_rule == "alphabetical_first":
        # Sort by (count desc, name asc)
        candidates.sort(key=lambda x: (-x[1], x[0]))
    else:
        candidates.sort(key=lambda x: x[1], reverse=True)
    
    return candidates[:k]


def weighted_voting(
    votes: List[Tuple[str, int]]
) -> List[Tuple[str, int]]:
    """
    Handle weighted votes (e.g., ranked choice).
    
    Args:
        votes: List of (candidate, points) tuples
    
    Returns:
        Sorted list of (candidate, total_score)
    
    Time: O(N + C log C)
    Space: O(C)
    """
    from collections import defaultdict
    
    scores = defaultdict(int)
    
    for candidate, points in votes:
        scores[candidate] += points
    
    # Sort by score descending
    sorted_scores = sorted(
        scores.items(),
        key=lambda x: (x[1], x[0]),  # By score, then by name
        reverse=True
    )
    
    return sorted_scores


# ============================================
# COMPLETE RUNNABLE EXAMPLE
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("VOTING SYSTEM")
    print("=" * 60)
    
    # Test 1: Basic winner
    print("\n[Test 1] Basic Winner")
    print("-" * 40)
    votes1 = ["Alice", "Bob", "Alice", "Charlie", "Bob", "Bob"]
    winner1 = find_winner(votes1)
    print(f"Votes: {votes1}")
    print(f"Winner: {winner1}")  # Bob (3 votes)
    
    # Test 2: Tie-breaking (alphabetical last)
    print("\n[Test 2] Tie-Breaking (Alphabetical Last)")
    print("-" * 40)
    votes2 = ["Alice", "Bob", "Alice", "Bob"]
    winner2 = find_winner(votes2, tie_rule="alphabetical_last")
    print(f"Votes: {votes2}")
    print(f"Alice: 2, Bob: 2 (tie)")
    print(f"Winner: {winner2}")  # Bob (alphabetically > Alice)
    
    # Test 3: Tie-breaking (alphabetical first)
    print("\n[Test 3] Tie-Breaking (Alphabetical First)")
    print("-" * 40)
    winner3 = find_winner(votes2, tie_rule="alphabetical_first")
    print(f"Winner: {winner3}")  # Alice
    
    # Test 4: Leaderboard (Top K)
    print("\n[Test 4] Leaderboard (Top 3)")
    print("-" * 40)
    votes4 = ["A", "B", "A", "C", "B", "B", "D", "A", "C"]
    leaderboard = get_leaderboard(votes4, k=3)
    print(f"Votes: {votes4}")
    print(f"Top 3:")
    for rank, (name, count) in enumerate(leaderboard, 1):
        print(f"  {rank}. {name}: {count} votes")
    
    # Test 5: Weighted voting (ranked choice)
    print("\n[Test 5] Weighted Voting")
    print("-" * 40)
    # First choice = 3 points, Second = 2, Third = 1
    weighted_votes = [
        ("Alice", 3),   # Someone's 1st choice
        ("Bob", 2),     # Someone's 2nd choice
        ("Alice", 1),   # Someone's 3rd choice
        ("Bob", 3),     # Someone's 1st choice
        ("Charlie", 3)  # Someone's 1st choice
    ]
    
    results = weighted_voting(weighted_votes)
    print("Weighted Results:")
    for rank, (name, score) in enumerate(results, 1):
        print(f"  {rank}. {name}: {score} points")
    
    # Test 6: Edge cases
    print("\n[Test 6] Edge Cases")
    print("-" * 40)
    print(f"Empty votes: {find_winner([])}")  # None
    print(f"Single vote: {find_winner(['Alice'])}")  # Alice
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)
```

---

## 🔍 Explanation with Example

Let's trace through how the vote counting algorithm works with a concrete example:

**Votes:** `["Alice", "Bob", "Alice", "Charlie", "Bob", "Bob", "Alice"]`

**Goal:** Find the winner with tie-breaking rule = "alphabetically last"

---

**Step 1: Count Votes (O(N))**

Iterate through each vote and build frequency map:

```python
votes = ["Alice", "Bob", "Alice", "Charlie", "Bob", "Bob", "Alice"]

# Using Counter
counts = Counter(votes)
```

**Result:**
```
counts = {
    "Alice": 3,
    "Bob": 3,
    "Charlie": 1
}
```

---

**Step 2: Find Maximum Count (O(C))**

```python
max_count = max(counts.values())  # max(3, 3, 1) = 3
```

**Result:** `max_count = 3`

---

**Step 3: Find All Winners with Max Count**

```python
winners = [name for name, count in counts.items() if count == max_count]
```

**Result:** `winners = ["Alice", "Bob"]` (both have 3 votes)

---

**Step 4: Apply Tie-Breaking Rule**

Since we have a tie, apply the rule "alphabetically last":

```python
if tie_rule == "alphabetical_last":
    winner = max(winners)  # max("Alice", "Bob") = "Bob"
```

**Comparison:** "Bob" > "Alice" alphabetically → **Bob wins!**

---

**Alternative: Top K Leaderboard**

If we want Top 2 candidates:

**Step 1:** Sort all candidates by count (descending), then by name (ascending for ties):

```python
sorted_candidates = sorted(
    counts.items(),
    key=lambda x: (-x[1], x[0])
)

# Result:
# [("Alice", 3), ("Bob", 3), ("Charlie", 1)]
# Both Alice and Bob have 3, but Alice < Bob alphabetically
```

**Step 2:** Take first k:

```python
top_2 = sorted_candidates[:2]
# Result: [("Alice", 3), ("Bob", 3)]
```

---

## 🔍 Complexity Analysis

### Time Complexity

| Operation | Time | Explanation |
|-----------|------|-------------|
| Count votes | **O(N)** | Single pass through votes |
| Find max count | **O(C)** | Scan counter (C = unique candidates) |
| Sort candidates | **O(C log C)** | Sort C candidates |
| **Total** | **O(N + C log C)** | Usually C << N, so ≈ O(N) |

### Space Complexity

**O(C)** for the counter (C = unique candidates).

---

## ⚠️ Common Pitfalls

### 1. **Wrong Tie-Breaking Logic**

**Wrong:**
```python
# Want: Bob > Alice if tied
candidates.sort(key=lambda x: x[1], reverse=True)  # Only sorts by count
# Result: Arbitrary order for ties
```

**Right:** Include secondary sort key.
```python
candidates.sort(key=lambda x: (x[1], x[0]), reverse=True)
```

### 2. **Incorrect Sort Key for "Alphabetical First"**

**Wrong:**
```python
# Want: Alice > Bob if tied (alphabetically first)
candidates.sort(key=lambda x: (x[1], x[0]), reverse=True)
# This gives Bob > Alice (reverse sorts both keys)
```

**Right:**
```python
candidates.sort(key=lambda x: (-x[1], x[0]))  # Count desc, name asc
```

### 3. **Not Handling Empty Votes**

**Wrong:**
```python
def find_winner(votes):
    counts = Counter(votes)
    return max(counts, key=counts.get)  # Crashes on empty Counter
```

**Right:** Check `if not votes: return None`.

---

## 🔄 Follow-up Questions

### Follow-up 1: Streaming Votes

**Problem Statement:**
> "Votes arrive one at a time as a stream. Maintain a live leaderboard that can be queried at any time."

**Solution:**
Maintain a `Counter` and update it incrementally.

```python
class LiveLeaderboard:
    """
    Maintain live voting results.
    """
    
    def __init__(self):
        self.counts = Counter()
    
    def cast_vote(self, candidate: str) -> None:
        """
        Add a vote.
        Time: O(1)
        """
        self.counts[candidate] += 1
    
    def get_leader(self) -> Optional[str]:
        """
        Get current leader.
        Time: O(C)
        """
        if not self.counts:
            return None
        return max(self.counts, key=self.counts.get)
    
    def get_top_k(self, k: int) -> List[Tuple[str, int]]:
        """
        Get current top K.
        Time: O(C log C)
        """
        candidates = sorted(
            self.counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return candidates[:k]
```

---

### Follow-up 2: Ranked Choice Voting (IRV)

**Problem Statement:**
> "Each voter ranks candidates (1st, 2nd, 3rd choice). Implement Instant Runoff Voting: eliminate the candidate with the fewest 1st-choice votes, redistribute their votes to voters' 2nd choices, repeat until someone has a majority."

**Solution:**
This is complex! Key steps:

1. Count 1st-choice votes for each candidate.
2. If someone has >50%, they win.
3. Otherwise, eliminate the candidate with fewest 1st-choice votes.
4. Redistribute their votes to next-choice candidates.
5. Repeat.

```python
def instant_runoff(ballots: List[List[str]]) -> str:
    """
    Implement instant runoff voting.
    
    Args:
        ballots: List of ranked ballots (1st choice first)
    
    Returns:
        Winner's name
    """
    active = set()
    for ballot in ballots:
        active.update(ballot)
    
    while len(active) > 1:
        # Count current top choices
        counts = Counter()
        for ballot in ballots:
            # Find first active candidate on this ballot
            for candidate in ballot:
                if candidate in active:
                    counts[candidate] += 1
                    break
        
        # Check for majority
        total = sum(counts.values())
        for candidate, count in counts.items():
            if count > total / 2:
                return candidate
        
        # Eliminate candidate with fewest votes
        min_count = min(counts.values())
        eliminated = [c for c, count in counts.items() if count == min_count][0]
        active.remove(eliminated)
    
    return list(active)[0]
```

---

## 🧪 Test Cases

```python
def test_voting():
    # Test 1: Clear winner
    assert find_winner(["A", "B", "A"]) == "A"
    
    # Test 2: Tie (alphabetical last)
    assert find_winner(["A", "B"], tie_rule="alphabetical_last") == "B"
    
    # Test 3: Tie (alphabetical first)
    assert find_winner(["A", "B"], tie_rule="alphabetical_first") == "A"
    
    # Test 4: Empty
    assert find_winner([]) is None
    
    # Test 5: Leaderboard order
    leaderboard = get_leaderboard(["A", "B", "A", "C", "B", "B"], k=3)
    assert leaderboard[0][0] == "B"  # Most votes
    assert leaderboard[1][0] == "A"  # Second most
    
    print("All tests passed! ✓")

if __name__ == "__main__":
    test_voting()
```

---

## 🎯 Key Takeaways

1. **Counter is Perfect** for frequency-based problems.
2. **Custom Sort Keys** handle tie-breaking elegantly.
3. **Tuple Sort Keys** `(primary, secondary)` are powerful.
4. **Negative Values** in sort keys reverse order: `(-count, name)`.
5. **Streaming Updates** maintain Counter incrementally (O(1) per vote).

---

## 📚 Related Problems

- **LeetCode 347:** Top K Frequent Elements
- **LeetCode 692:** Top K Frequent Words (with tie-breaking)
- **LeetCode 451:** Sort Characters By Frequency
- **LeetCode 1636:** Sort Array by Increasing Frequency
