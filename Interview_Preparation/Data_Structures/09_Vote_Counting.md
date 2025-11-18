# 🗳️ PROBLEM 9: VOTE COUNTING / LEADERBOARD

### ⭐⭐⭐ **Ranked Choice Voting / Top Candidates**

**Frequency:** Medium
**Similar to:** Top K, Custom Sorting

**Problem Statement:**
> You have a list of votes. Each vote contains a candidate name.
>
> **Part 1 (Simple):** Return the winner (most votes). If tie, lexicographically last (or first, depending on rule).
>
> **Part 2 (Weighted):** Each vote has a "weight" (e.g., 3 points, 2 points, 1 point).
>
> **Part 3 (Leaderboard):** Return Top 3 candidates.

**Example:**
```python
votes = ["A", "B", "A", "C", "B", "B"]
# A: 2, B: 3, C: 1
# Winner: B
```

---

### 🗣️ **Interview Conversation Guide**

**Phase 1: Clarification**
- **Candidate:** "How are votes received? Array or Stream?"
- **Interviewer:** "Array for now."
- **Candidate:** "How to break ties?"
- **Interviewer:** "If vote counts are equal, choose the one that is alphabetically **last** (e.g., 'Bob' > 'Alice')."

**Phase 2: Approach**
- **Candidate:** "I will use a Hash Map to count votes."
- **Candidate:** "Then, I will convert the map to a list of objects/tuples."
- **Candidate:** "I need to sort this list. Primary key: `count` (descending). Secondary key: `name` (descending for 'last' rule)."

**Phase 3: Coding**
- Use `collections.Counter`.
- Use Python's sort with a tuple key `(-count, name)` (min-heap style) or `(count, name)` with `reverse=True`.

---

### 📝 **Solution Approach: Counting & Sorting**

**Part 1 & 3 Combined (Top K)**

```python
from collections import Counter, defaultdict

def get_leaderboard(votes, k=3):
    # 1. Count
    # If input is just names:
    counts = Counter(votes)
    
    # If input is weighted (Name, Points):
    # counts = defaultdict(int)
    # for name, points in votes:
    #     counts[name] += points

    # 2. Sort
    # We want Max Votes first. If Tie, Max Name (Alphabetically last) first.
    # Python's sort is stable and ascending by default.
    # We can sort by (-count, -name) to get Ascending order equivalent to Descending?
    # No, easier: Sort by (count, name) and take reverse.
    
    candidates = list(counts.items()) # [(Name, Count), ...]
    
    # Sort Key:
    # Primary: x[1] (Count)
    # Secondary: x[0] (Name)
    candidates.sort(key=lambda x: (x[1], x[0]), reverse=True)

    # 3. Return Top K
    # Return just names
    return [name for name, count in candidates[:k]]

# Test
votes = ["Alice", "Bob", "Alice", "Charlie", "Bob", "Bob"]
print(get_leaderboard(votes, k=1)) # ['Bob']
```

**Note on Tie-Breaking:**
- If rule: "Alphabetically First" (Alice > Bob on tie).
- Sort Key: `(-x[1], x[0])` (Count descending, Name ascending).
- `candidates.sort(key=lambda x: (-x[1], x[0]))`.

---

### 🧪 **Test Cases**

**Tie Breaking:**
- A: 2, B: 2.
- Rule: Last name wins -> Returns B.
- Rule: First name wins -> Returns A.

**Single Vote:**
- Works correctly.

**No Votes:**
- Returns empty list.
