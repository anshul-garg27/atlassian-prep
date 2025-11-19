# 🔤 PROBLEM 12: WORD SEARCH / ANAGRAM SEARCH

### ⭐⭐ **Grid DFS and Anagram Matching**

**Frequency:** Low (Appears in ~10-15% of rounds)
**Difficulty:** Easy-Medium
**Similar to:** [LeetCode 79 - Word Search](https://leetcode.com/problems/word-search/), [LeetCode 242 - Valid Anagram](https://leetcode.com/problems/valid-anagram/)

---

## 📋 Problem Statement

This problem has **two common variations**:

### Variation 1: Grid Word Search
Given an `m × n` grid of characters and a target word, determine if the word exists in the grid.

**Rules:**
- The word can be constructed from letters of sequentially adjacent cells
- Adjacent cells are horizontally or vertically neighboring (not diagonal)
- The same letter cell cannot be used more than once in a single word

### Variation 2: Anagram Search
Given a main word and a list of candidate words, find which candidates are anagrams of (or can be formed from) the main word.

**Constraints:**
- **Grid:** 1 ≤ m, n ≤ 6 (small grids typical)
- **Word:** 1 ≤ word.length ≤ 15
- Grid consists of uppercase or lowercase English letters

---

## 🎨 Visual Example

### Variation 1: Grid Word Search

```text
Grid:
  A B C E
  S F C S
  A D E E

Search for "ABCCED":

Step-by-step path:
A(0,0) → B(0,1) → C(0,2) → C(1,2) → E(1,3) → D(2,3)

Visual:
  [A][B][C] E      Start at (0,0)
   S  F [C] S      Move right, right, down
   A  D  E [D]     Continue down, right

Result: TRUE ✓
```

```text
Search for "ABCB":

  [A][B][C] E      Start at (0,0)
   S  F  C  S      Move right, right
   A  D  E  E      Need to go back to B at (0,1)
                   But (0,1) was already used!

Result: FALSE ✗ (Cannot reuse cells)
```

### Variation 2: Anagram Search

```text
Main word: "listen"

Candidates:
1. "silent" → Anagram? Check frequency:
   l:1, i:1, s:1, t:1, e:1, n:1
   s:1, i:1, l:1, e:1, n:1, t:1
   Match! → TRUE ✓

2. "enlist" → Anagram? Same letters → TRUE ✓

3. "google" → Anagram?
   l:1, i:1, s:1, t:1, e:1, n:1
   g:2, o:2, l:1, e:1
   Different letters → FALSE ✗

4. "inlets" → Anagram? Same letters → TRUE ✓
```

---

## 💡 Examples

### Example 1: Grid Word Search
```python
board = [
    ['A', 'B', 'C', 'E'],
    ['S', 'F', 'C', 'S'],
    ['A', 'D', 'E', 'E']
]

print(word_exists(board, "ABCCED"))  # True
print(word_exists(board, "SEE"))     # True
print(word_exists(board, "ABCB"))    # False
```

### Example 2: Anagram Search
```python
main_word = "listen"
candidates = ["silent", "enlist", "google", "inlets"]

result = find_anagrams(main_word, candidates)
print(result)  # ["silent", "enlist", "inlets"]
```

---

## 🗣️ Interview Conversation Guide

### Phase 1: Clarification (3-5 min)

**Candidate:** "Which variation are we solving—grid search or anagram matching?"
**Interviewer:** "Let's start with grid search. We can discuss anagrams as a follow-up."

**Candidate:** "Can we move diagonally in the grid?"
**Interviewer:** "No, only horizontal and vertical movements."

**Candidate:** "Can we reuse the same cell for multiple letters in one word?"
**Interviewer:** "No, each cell can be used at most once per word search."

**Candidate:** "Should the search be case-sensitive?"
**Interviewer:** "Yes, treat uppercase and lowercase as different letters."

### Phase 2: Approach Discussion (5-8 min)

**Candidate:** "For grid word search, this is a **DFS/Backtracking** problem.

**Algorithm:**
1. **Find Starting Points:** Scan grid for cells matching the first letter.
2. **DFS from Each Start:** Recursively try to match remaining letters.
3. **Backtracking:** Mark cells as visited, explore, then unmark (backtrack).
4. **Base Cases:**
   - If we match all letters → return True
   - If out of bounds or wrong letter → return False

**Time Complexity:** O(M × N × 4^L) where:
- M × N = grid size
- L = word length
- 4^L = worst case branches (up/down/left/right at each step)

For **anagram search**, it's simpler:
- Use **frequency counting** (HashMap or array)
- O(N) time per word where N = word length"

### Phase 3: Implementation (15-20 min)

**Candidate:** "I'll implement DFS with a visited set for grid search, and Counter for anagrams."

---

## 🧠 Intuition & Approach

### Why DFS/Backtracking for Grid Search?

**Problem Characteristics:**
- Explore multiple paths from each starting point
- Need to "undo" visits (backtrack) to try alternative paths
- Decision tree: at each cell, we have up to 4 choices

**Why not BFS?**
BFS explores all neighbors at each level, but we need a specific **sequential path** matching the word. DFS naturally follows one path at a time.

### Backtracking Pattern

```text
DFS(row, col, index):
  │
  ├─ Base Case: index == len(word) → Found!
  │
  ├─ Validation: out of bounds, wrong letter, visited → Fail
  │
  ├─ Mark as visited
  │
  ├─ Try all 4 directions:
  │   ├─ DFS(row+1, col, index+1)  ← Down
  │   ├─ DFS(row-1, col, index+1)  ← Up
  │   ├─ DFS(row, col+1, index+1)  ← Right
  │   └─ DFS(row, col-1, index+1)  ← Left
  │
  └─ Unmark (backtrack)
```

---

## 📝 Solution 1: Grid Word Search (DFS)

```python
from typing import List

def word_exists(board: List[List[str]], word: str) -> bool:
    """
    Determine if word exists in the grid using DFS.
    
    Args:
        board: m x n grid of characters
        word: Target word to search
    
    Returns:
        True if word exists, False otherwise
    
    Time: O(M × N × 4^L) where L = word length
    Space: O(L) for recursion stack
    """
    if not board or not board[0] or not word:
        return False
    
    m, n = len(board), len(board[0])
    
    def dfs(row: int, col: int, index: int) -> bool:
        """
        DFS to match word[index:] starting from (row, col).
        """
        # Base case: matched all letters
        if index == len(word):
            return True
        
        # Boundary checks
        if row < 0 or row >= m or col < 0 or col >= n:
            return False
        
        # Letter mismatch or already visited
        if board[row][col] != word[index] or board[row][col] == '#':
            return False
        
        # Mark as visited (in-place modification)
        temp = board[row][col]
        board[row][col] = '#'
        
        # Explore all 4 directions
        found = (
            dfs(row + 1, col, index + 1) or  # Down
            dfs(row - 1, col, index + 1) or  # Up
            dfs(row, col + 1, index + 1) or  # Right
            dfs(row, col - 1, index + 1)     # Left
        )
        
        # Backtrack: restore original value
        board[row][col] = temp
        
        return found
    
    # Try starting from each cell
    for i in range(m):
        for j in range(n):
            if board[i][j] == word[0]:  # Optimization: check first letter
                if dfs(i, j, 0):
                    return True
    
    return False


# ============================================
# COMPLETE RUNNABLE EXAMPLE
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("GRID WORD SEARCH (DFS)")
    print("=" * 60)
    
    board = [
        ['A', 'B', 'C', 'E'],
        ['S', 'F', 'C', 'S'],
        ['A', 'D', 'E', 'E']
    ]
    
    # Test cases
    test_words = [
        ("ABCCED", True),
        ("SEE", True),
        ("ABCB", False),
        ("SFCS", True),
        ("ASADB", False)
    ]
    
    for word, expected in test_words:
        result = word_exists(board, word)
        status = "✓" if result == expected else "✗"
        print(f"{status} word_exists(board, '{word}') = {result} (expected {expected})")
```

---

## 📝 Solution 2: Anagram Search (Frequency Counting)

```python
from collections import Counter
from typing import List

def find_anagrams(main_word: str, candidates: List[str]) -> List[str]:
    """
    Find all candidates that are anagrams of main_word.
    
    Args:
        main_word: Reference word
        candidates: List of candidate words
    
    Returns:
        List of anagrams
    
    Time: O(M + N × K) where:
        M = len(main_word)
        N = number of candidates
        K = avg length of candidate
    Space: O(1) for frequency array (fixed size 26)
    """
    # Count frequency of main_word
    main_freq = Counter(main_word)
    
    anagrams = []
    
    for candidate in candidates:
        # Quick length check
        if len(candidate) != len(main_word):
            continue
        
        # Compare frequencies
        if Counter(candidate) == main_freq:
            anagrams.append(candidate)
    
    return anagrams


def can_form_from(main_word: str, candidate: str) -> bool:
    """
    Check if candidate can be formed from letters in main_word.
    (Letters in main_word can be used at most once)
    
    Example: main="listen", candidate="sit" → True
             main="listen", candidate="google" → False
    
    Time: O(M + K)
    Space: O(1)
    """
    main_freq = Counter(main_word)
    cand_freq = Counter(candidate)
    
    # Check if candidate uses only available letters
    for letter, count in cand_freq.items():
        if main_freq[letter] < count:
            return False
    
    return True


# ============================================
# COMPLETE RUNNABLE EXAMPLE
# ============================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("ANAGRAM SEARCH")
    print("=" * 60)
    
    main = "listen"
    candidates = ["silent", "enlist", "google", "inlets", "tin"]
    
    print(f"\nMain word: '{main}'")
    print(f"Candidates: {candidates}")
    
    # Test 1: Find exact anagrams
    anagrams = find_anagrams(main, candidates)
    print(f"\nExact anagrams: {anagrams}")
    
    # Test 2: Check if can be formed
    print(f"\nCan form from '{main}':")
    for word in candidates:
        result = can_form_from(main, word)
        print(f"  '{word}': {result}")
```

---

## 🔍 Explanation with Example

### Grid Word Search: "ABCCED"

**Grid:**
```
  0   1   2   3
0 A   B   C   E
1 S   F   C   S
2 A   D   E   E
```

**Step-by-Step DFS:**

```text
Start: Find 'A' at (0,0)

dfs(0, 0, index=0):  # Match 'A'
  Mark (0,0) as visited
  
  Try Down (1,0): 'S' ≠ 'B' → Fail
  Try Up (-1,0): Out of bounds → Fail
  Try Right (0,1): 'B' = 'B' ✓
  
    dfs(0, 1, index=1):  # Match 'B'
      Mark (0,1) as visited
      
      Try Right (0,2): 'C' = 'C' ✓
      
        dfs(0, 2, index=2):  # Match 'C'
          Mark (0,2) as visited
          
          Try Down (1,2): 'C' = 'C' ✓
          
            dfs(1, 2, index=3):  # Match 'C'
              Mark (1,2) as visited
              
              Try Right (1,3): 'S' ≠ 'E' → Fail
              Try Down (2,2): 'E' = 'E' ✓
              
                dfs(2, 2, index=4):  # Match 'E'
                  Mark (2,2) as visited
                  
                  Try Right (2,3): 'E' ≠ 'D' → Fail
                  Try Down (3,2): Out of bounds → Fail
                  Try Left (2,1): 'D' = 'D' ✓
                  
                    dfs(2, 1, index=5):  # Match 'D'
                      index == len(word) → FOUND! ✓
                      
                      Return True
```

---

## 🔍 Complexity Analysis

### Grid Word Search

**Time Complexity: O(M × N × 4^L)**
- Try starting from each cell: O(M × N)
- At each cell, branch into 4 directions: O(4^L)
- L = word length

**Optimizations:**
- Early termination if first letter matches
- Pruning: stop if remaining letters > remaining grid cells

**Space Complexity: O(L)**
- Recursion stack depth = word length

### Anagram Search

**Time Complexity: O(M + N × K)**
- Count main word: O(M)
- For each of N candidates:
  - Count candidate: O(K)
  - Compare: O(1) with Counter

**Space Complexity: O(1)**
- Fixed-size frequency map (26 letters)

---

## ⚠️ Common Pitfalls

### 1. **Not Backtracking (Grid Search)**

**Problem:**
```python
# ❌ WRONG: Never restore original value
board[row][col] = '#'  # Mark visited
result = dfs(...)
# Missing: board[row][col] = temp
```

**Why it fails:** Grid remains modified, affecting other search paths.

**Fix:** Always restore the cell after exploring.

---

### 2. **Using External Visited Set (Grid Search)**

**Problem:**
```python
# ❌ Less efficient
visited = set()
visited.add((row, col))
# ...
visited.remove((row, col))
```

**Why it's suboptimal:** Extra space O(L) for the set.

**Better:** Mark in-place with special character like `'#'`.

---

### 3. **Wrong Anagram Check**

**Problem:**
```python
# ❌ WRONG: Just sorts and compares
def is_anagram(w1, w2):
    return sorted(w1) == sorted(w2)
```

**Why it's suboptimal:** O(N log N) sorting when O(N) counting works.

**Fix:** Use frequency counting (Counter).

---

### 4. **Case Sensitivity Issues**

**Problem:** Grid has lowercase 'a' but searching for uppercase 'A'.

**Fix:** Normalize case if needed:
```python
word = word.lower()
board[i][j] = board[i][j].lower()
```

---

## 🔄 Follow-up Questions

### Follow-up 1: Find All Words in Grid

**Problem Statement:**
> "Given a grid and a list of words, find which words exist in the grid."

**Example:**
```python
board = [['A','B'],['C','D']]
words = ["AB", "CD", "ABCD", "XY"]
# Result: ["AB", "CD", "ABCD"]
```

**Solution:**

```python
def find_words(board: List[List[str]], words: List[str]) -> List[str]:
    """
    Find all words that exist in the grid.
    
    Time: O(M × N × W × 4^L) where W = number of words
    """
    result = []
    
    for word in words:
        if word_exists(board, word):
            result.append(word)
    
    return result
```

**Optimization with Trie:**
Search multiple words simultaneously using a Trie (LeetCode 212 - Word Search II).

---

### Follow-up 2: Count Anagrams

**Problem Statement:**
> "Given a string and a list of words, count how many words are anagrams of any substring of the string."

**Example:**
```python
s = "cbaebabacd"
words = ["abc", "bca", "cab"]
# All 3 words are anagrams of "abc", which appears in s
# Result: 3
```

**Solution:**

```python
from collections import Counter

def count_anagram_matches(s: str, words: List[str]) -> int:
    """
    Count words that are anagrams of any substring in s.
    
    Time: O(N × K + W × K) where:
        N = len(s)
        W = number of words
        K = word length (assume all same length)
    """
    if not words:
        return 0
    
    word_len = len(words[0])
    count = 0
    
    # Create frequency map for each word
    word_freqs = [Counter(word) for word in words]
    
    # Sliding window over s
    for i in range(len(s) - word_len + 1):
        substring = s[i:i + word_len]
        sub_freq = Counter(substring)
        
        # Check against all words
        for word_freq in word_freqs:
            if sub_freq == word_freq:
                count += 1
                break  # Count each window only once
    
    return count
```

**Time Complexity:** O(N × K + W × K)

---

### Follow-up 3: Word Search with Wild Cards

**Problem Statement:**
> "In the grid word search, '.' can match any letter. Find if a word with wildcards exists."

**Example:**
```python
board = [['A','B'],['C','D']]
word = "A.D"  # Should match 'A' then any letter then 'D'
# Result: True (path: A → B → D or A → C → D)
```

**Solution:**

```python
def word_exists_wildcard(board: List[List[str]], word: str) -> bool:
    """
    Word search with wildcard '.' matching any letter.
    
    Time: O(M × N × 4^L)
    """
    m, n = len(board), len(board[0])
    
    def dfs(row: int, col: int, index: int) -> bool:
        if index == len(word):
            return True
        
        if row < 0 or row >= m or col < 0 or col >= n:
            return False
        
        if board[row][col] == '#':  # Already visited
            return False
        
        # Check match: exact letter or wildcard
        if word[index] != '.' and board[row][col] != word[index]:
            return False
        
        temp = board[row][col]
        board[row][col] = '#'
        
        found = (
            dfs(row + 1, col, index + 1) or
            dfs(row - 1, col, index + 1) or
            dfs(row, col + 1, index + 1) or
            dfs(row, col - 1, index + 1)
        )
        
        board[row][col] = temp
        return found
    
    for i in range(m):
        for j in range(n):
            if dfs(i, j, 0):
                return True
    
    return False
```

---

## 🧪 Test Cases

```python
def test_word_search():
    board = [
        ['A', 'B', 'C', 'E'],
        ['S', 'F', 'C', 'S'],
        ['A', 'D', 'E', 'E']
    ]
    
    # Test 1: Word exists
    assert word_exists(board, "ABCCED") == True
    
    # Test 2: Word exists (different path)
    assert word_exists(board, "SEE") == True
    
    # Test 3: Word doesn't exist (reuse issue)
    assert word_exists(board, "ABCB") == False
    
    # Test 4: Single letter
    assert word_exists(board, "A") == True
    
    # Test 5: Word longer than grid
    assert word_exists(board, "ABCDEFGHIJKLMN") == False
    
    print("Grid search tests passed! ✓")


def test_anagram_search():
    # Test 1: Exact anagrams
    anagrams = find_anagrams("listen", ["silent", "enlist", "google"])
    assert set(anagrams) == {"silent", "enlist"}
    
    # Test 2: Can form from
    assert can_form_from("listen", "sit") == True
    assert can_form_from("listen", "google") == False
    
    # Test 3: Empty
    assert find_anagrams("", []) == []
    
    print("Anagram search tests passed! ✓")


if __name__ == "__main__":
    test_word_search()
    test_anagram_search()
```

---

## 🎯 Key Takeaways

1. **DFS + Backtracking** is the standard for grid path problems.
2. **In-Place Marking** (using '#') saves space vs. visited set.
3. **Frequency Counting** (Counter) is optimal for anagram detection.
4. **Early Termination** improves performance (check first letter, length).
5. **Backtracking is Critical** - always restore state after exploring.

---

## 📚 Related Problems

- **LeetCode 79:** Word Search (grid DFS)
- **LeetCode 212:** Word Search II (Trie + DFS)
- **LeetCode 242:** Valid Anagram (frequency counting)
- **LeetCode 438:** Find All Anagrams in a String (sliding window)
- **LeetCode 49:** Group Anagrams (frequency as key)

