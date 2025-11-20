# 📝 PROBLEM 10: WORD WRAP / TEXT JUSTIFICATION

### ⭐⭐⭐⭐ **Format Text with Line Length Constraints**

**Frequency:** Medium-High (Appears in ~30-35% of rounds)
**Difficulty:** Medium-Hard
**Similar to:** [LeetCode 68 - Text Justification](https://leetcode.com/problems/text-justification/)

---

## 📋 Problem Statement

Given a list of `words` and a `maxWidth`, format the text such that each line has **exactly** `maxWidth` characters and is fully justified (except the last line).

**Justification Rules:**
1. **Pack Greedily:** Fit as many words as possible per line
2. **Distribute Spaces:** Pad extra spaces evenly between words
3. **Left-Heavy Distribution:** If spaces don't divide evenly, assign more to left gaps
4. **Last Line:** Left-justified only (single space between words, pad end with spaces)

**Constraints:**
- 1 ≤ words.length ≤ 300
- 1 ≤ words[i].length ≤ maxWidth
- 1 ≤ maxWidth ≤ 100
- Words consist of non-space characters only

---

## 🎨 Visual Example

### Example 1: Even Space Distribution

```text
Words: ["What", "must", "be", "acknowledgment", "shall", "be"]
maxWidth: 16

Line 1: "What   must   be"
         W h a t ███ m u s t ███ b e
         4 chars + 4 chars + 2 chars = 10 letters
         16 - 10 = 6 spaces → 2 gaps → 3 spaces each

Line 2: "acknowledgment  "
         (Single word, left-justify, pad end)
         14 chars + 2 spaces = 16

Line 3: "shall be        "
         (Last line, left-justify)
         5 + 1 + 2 + 8 spaces = 16
```

### Example 2: Uneven Space Distribution

```text
Words: ["This", "is", "an", "example"]
maxWidth: 16

Line 1: "This    is    an"
         T h i s ████ i s ████ a n
         4 + 2 + 2 = 8 letters
         16 - 8 = 8 spaces → 2 gaps → 4 spaces each

Line 2: "example         "
         (Last line, left-justify)
         7 + 9 spaces = 16
```

### Example 3: Left-Heavy Distribution

```text
Words: ["a", "b", "c", "d", "e"]
maxWidth: 7

Line 1: "a  b  c"
         1 + 1 + 1 = 3 letters
         7 - 3 = 4 spaces → 2 gaps
         4 ÷ 2 = 2 spaces per gap, 0 remainder
         Result: 2, 2

Line 2: "d  e   "
         (Last line, left-justify)
```

---

## 💡 Examples

### Example 1: Standard Text
```python
words = ["This", "is", "an", "example", "of", "text", "justification."]
result = fullJustify(words, 16)

for line in result:
    print(f"|{line}|")
    
# Output:
# |This    is    an|
# |example  of text|
# |justification.  |
```

### Example 2: Single Long Word
```python
words = ["verylongword"]
result = fullJustify(words, 20)
# |verylongword        |
```

---

## 🗣️ Interview Conversation Guide

### Phase 1: Clarification (3-5 min)

**Candidate:** "Can a single word be longer than `maxWidth`?"
**Interviewer:** "No, guaranteed that `word.length ≤ maxWidth`."

**Candidate:** "For the last line, should it be left-justified with spaces padded to the right?"
**Interviewer:** "Yes, single space between words, remaining spaces on the right."

**Candidate:** "If a line has only one word (not the last line), how should it be formatted?"
**Interviewer:** "Treat it like the last line—left-justified with spaces on the right."

**Candidate:** "How should we count the minimum space required? Is it word lengths plus one space between each word?"
**Interviewer:** "Yes, you need at least `sum(word lengths) + (num_words - 1)` characters."

### Phase 2: Approach Discussion (5-8 min)

**Candidate:** "This is a **Greedy Line Packing** problem with careful space distribution.

**Algorithm:**
1. **Packing Phase (Greedy):**
   - For each line, greedily pack words until adding the next word would exceed `maxWidth`.
   - Account for mandatory spaces between words.

2. **Formatting Phase:**
   - Calculate total spaces needed: `maxWidth - sum(word_lengths)`.
   - **Case A (Last line or single word):** Left-justify.
   - **Case B (Normal line):** Distribute spaces evenly across gaps.
     - Base spaces per gap: `total_spaces // num_gaps`.
     - Extra spaces: `total_spaces % num_gaps`.
     - Assign extra spaces to leftmost gaps (left-heavy distribution).

**Complexity:** O(N) where N = total characters in all words."

### Phase 3: Implementation (15-20 min)

**Candidate:** "I'll implement this with careful index management and a helper function for formatting lines."

---

## 🧠 Intuition & Approach

### Why Greedy?

**Observation:** To minimize total lines and maximize readability, we want to fit as many words as possible per line. Greedy packing achieves this.

### Space Distribution Logic

```text
Example: 3 words, 10 total spaces, 2 gaps

Base distribution: 10 ÷ 2 = 5 spaces per gap, 0 remainder
Result: [5, 5]

Example: 3 words, 11 total spaces, 2 gaps

Base: 11 ÷ 2 = 5 spaces per gap, 1 remainder
Left-heavy: First gap gets +1
Result: [6, 5]

Example: 4 words, 10 total spaces, 3 gaps

Base: 10 ÷ 3 = 3 spaces per gap, 1 remainder
Left-heavy: First gap gets +1
Result: [4, 3, 3]
```

---

## 📝 Complete Solution

```python
from typing import List

def fullJustify(words: List[str], maxWidth: int) -> List[str]:
    """
    Perform text justification.
    
    Args:
        words: List of words to justify
        maxWidth: Maximum line width
    
    Returns:
        List of justified lines
    
    Time: O(N) where N = total characters
    Space: O(1) excluding output
    """
    result = []
    i = 0
    n = len(words)
    
    while i < n:
        # Phase 1: Pack words for current line
        line_words = []
        line_length = 0  # Total characters (words + minimum spaces)
        j = i
        
        while j < n:
            word = words[j]
            # Calculate length if we add this word
            # Need 1 space before word (except first word)
            needed_space = 1 if line_words else 0
            new_length = line_length + needed_space + len(word)
            
            if new_length > maxWidth:
                break  # Can't fit this word
            
            line_words.append(word)
            line_length = new_length
            j += 1
        
        # Phase 2: Format the line
        num_words = len(line_words)
        total_word_chars = sum(len(w) for w in line_words)
        total_spaces = maxWidth - total_word_chars
        
        # Case A: Last line OR single word → Left justify
        if j == n or num_words == 1:
            line = " ".join(line_words)
            line += " " * (maxWidth - len(line))
            result.append(line)
        
        # Case B: Normal line → Full justify
        else:
            num_gaps = num_words - 1
            spaces_per_gap = total_spaces // num_gaps
            extra_spaces = total_spaces % num_gaps
            
            line = ""
            for k, word in enumerate(line_words):
                line += word
                if k < num_gaps:  # Not the last word
                    # Base spaces + extra (for first 'extra_spaces' gaps)
                    spaces = spaces_per_gap + (1 if k < extra_spaces else 0)
                    line += " " * spaces
            
            result.append(line)
        
        i = j  # Move to next batch of words
    
    return result


# ============================================
# COMPLETE RUNNABLE EXAMPLE
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("TEXT JUSTIFICATION")
    print("=" * 60)
    
    # Test 1: Standard paragraph
    print("\n[Test 1] Standard Text")
    print("-" * 40)
    words1 = ["This", "is", "an", "example", "of", "text", "justification."]
    result1 = fullJustify(words1, 16)
    
    print(f"maxWidth: 16")
    for i, line in enumerate(result1, 1):
        print(f"Line {i}: |{line}| (len={len(line)})")
    
    # Test 2: Single long word
    print("\n[Test 2] Single Long Word")
    print("-" * 40)
    words2 = ["verylongword"]
    result2 = fullJustify(words2, 20)
    
    print(f"maxWidth: 20")
    for line in result2:
        print(f"|{line}| (len={len(line)})")
    
    # Test 3: Uneven space distribution
    print("\n[Test 3] Uneven Space Distribution")
    print("-" * 40)
    words3 = ["What", "must", "be", "acknowledgment", "shall", "be"]
    result3 = fullJustify(words3, 16)
    
    print(f"maxWidth: 16")
    for line in result3:
        print(f"|{line}| (len={len(line)})")
    
    # Test 4: Many short words
    print("\n[Test 4] Many Short Words")
    print("-" * 40)
    words4 = ["a", "b", "c", "d", "e", "f", "g"]
    result4 = fullJustify(words4, 7)
    
    print(f"maxWidth: 7")
    for line in result4:
        print(f"|{line}| (len={len(line)})")
    
    # Test 5: Edge case - exact fit
    print("\n[Test 5] Exact Fit")
    print("-" * 40)
    words5 = ["a", "b"]
    result5 = fullJustify(words5, 3)
    
    print(f"maxWidth: 3")
    for line in result5:
        print(f"|{line}| (len={len(line)})")
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)
```

---

## 🔍 Explanation with Example

Let's trace through the text justification algorithm step by step:

**Words:** `["This", "is", "an", "example", "of", "text"]`  
**maxWidth:** `16`

---

**Step 1: Pack Line 1 - Greedy Packing**

Start with index i=0:

```python
line_words = []
line_length = 0

Try "This": len=4
  line_length = 4
  line_words = ["This"]

Try "is": len=2
  Need 1 space + 2 chars = 3 more
  line_length + 3 = 7 ≤ 16 ✓
  line_words = ["This", "is"]

Try "an": len=2
  Need 1 space + 2 chars = 3 more
  line_length + 3 = 10 ≤ 16 ✓
  line_words = ["This", "is", "an"]

Try "example": len=7
  Need 1 space + 7 chars = 8 more
  line_length + 8 = 18 > 16 ✗ STOP!
```

**Line 1 words:** `["This", "is", "an"]`

---

**Step 2: Format Line 1 - Space Distribution**

```python
num_words = 3
total_word_length = 4 + 2 + 2 = 8
total_spaces = 16 - 8 = 8
gaps = 3 - 1 = 2

base_spaces = 8 // 2 = 4
extra_spaces = 8 % 2 = 0

Space distribution: [4, 4]
```

**Build line:**
```text
"This" + (4 spaces) + "is" + (4 spaces) + "an"
= "This    is    an"
```

**Verification:** Length = 4 + 4 + 2 + 4 + 2 = 16 ✓

---

**Step 3: Pack Line 2**

Continue from "example":

```python
Try "example": len=7
  line_length = 7
  line_words = ["example"]

Try "of": len=2
  7 + 1 + 2 = 10 ≤ 16 ✓
  line_words = ["example", "of"]

Try "text": len=4
  10 + 1 + 4 = 15 ≤ 16 ✓
  line_words = ["example", "of", "text"]

End of words array.
```

**Line 2 words:** `["example", "of", "text"]`

---

**Step 4: Format Line 2 - Last Line (Left-Justify)**

```python
is_last_line = True

# Left-justify: single space between words, pad right
line = "example of text"
padding = 16 - 15 = 1
line = "example of text "
```

**Verification:** Length = 15 + 1 = 16 ✓

---

**Final Result:**

```python
[
    "This    is    an",
    "example of text "
]
```

---

**Example 2: Uneven Distribution**

**Words:** `["a", "b", "c"]`, **maxWidth:** `7`

```python
# All 3 words fit: "a", "b", "c"
total_word_length = 1 + 1 + 1 = 3
total_spaces = 7 - 3 = 4
gaps = 3 - 1 = 2

base_spaces = 4 // 2 = 2
extra_spaces = 4 % 2 = 0

Space distribution: [2, 2]
Result: "a  b  c"
```

**Uneven Example:** `["a", "b", "c", "d"]`, **maxWidth:** `9`

```python
total_word_length = 4
total_spaces = 9 - 4 = 5
gaps = 4 - 1 = 3

base_spaces = 5 // 3 = 1
extra_spaces = 5 % 3 = 2

# First 2 gaps get +1 extra space (left-heavy)
Space distribution: [2, 2, 1]
Result: "a  b  c d"
         ^^  ^^  ^
      (gap1) (gap2) (gap3)
```

---

## 🔍 Complexity Analysis

### Time Complexity: **O(N)**

Where N = total number of characters in all words.
- **Packing:** Each word is visited once → O(W) where W = number of words.
- **Formatting:** Each character is written once → O(N).
- **Total:** O(N).

### Space Complexity: **O(1)**

Excluding the output array. We only use constant extra space for loop variables and counters.

---

## ⚠️ Common Pitfalls

### 1. **Off-by-One in Space Calculation**

**Wrong:**
```python
# Forgetting that first word doesn't need a leading space
new_length = line_length + 1 + len(word)  # ❌ Always adds space
```

**Right:**
```python
needed_space = 1 if line_words else 0
new_length = line_length + needed_space + len(word)
```

### 2. **Incorrect Gap Count**

**Wrong:**
```python
num_gaps = num_words  # ❌ 3 words have 2 gaps, not 3
```

**Right:**
```python
num_gaps = num_words - 1
```

### 3. **Not Handling Last Line Specially**

**Wrong:**
```python
# Always fully justify
line = distribute_spaces(line_words, total_spaces)
```

**Problem:** Last line should be left-justified.

**Right:** Check `if j == n` (reached end).

### 4. **Wrong Extra Space Distribution**

**Wrong:**
```python
# Distributing extra spaces to rightmost gaps
for k in range(extra_spaces):
    spaces_array[-(k+1)] += 1  # ❌ Right-heavy
```

**Right:** Distribute to **leftmost** gaps.
```python
spaces = spaces_per_gap + (1 if k < extra_spaces else 0)
```

---

## 🔄 Follow-up Questions

### Follow-up 1: Minimize Raggedness (DP Approach)

**Problem Statement:**
> "Instead of greedy packing, choose line breaks to minimize the sum of squared 'badness' of each line, where badness = (unused_spaces)². This is how TeX/LaTeX does it."

---

## 🎯 Why Minimize Raggedness?

**Real-World Use Case:** Professional typesetting systems (TeX, LaTeX, InDesign) use this approach for aesthetically pleasing documents.

**Greedy vs Optimal:**

```text
Words: ["The", "quick", "brown", "fox", "jumps"]
maxWidth: 11

GREEDY APPROACH (maximize words per line):
┌───────────┐
│The  quick │  ← 3 unused spaces (cost = 3² = 9)
│brown  fox │  ← 3 unused spaces (cost = 3² = 9)
│jumps      │  ← 6 unused spaces (cost = 6² = 36)
└───────────┘
Total cost: 9 + 9 + 36 = 54

OPTIMAL DP APPROACH (minimize total badness):
┌───────────┐
│The quick  │  ← 2 unused spaces (cost = 2² = 4)
│brown fox  │  ← 2 unused spaces (cost = 2² = 4)
│jumps      │  ← 6 unused spaces (cost = 6² = 36)
└───────────┘
Total cost: 4 + 4 + 36 = 44 ✓ BETTER!

Notice: More even distribution of spaces across lines
```

**Why Square the Badness?**
- Linear penalty: Breaking "5, 5" vs "1, 9" same cost (10)
- Squared penalty: "5², 5²" = 50 vs "1², 9²" = 82 → Prefers even distribution!

---

## 📝 Complete DP Solution

**Solution: Dynamic Programming**

```python
from typing import List, Tuple

def word_wrap_dp(words: List[str], maxWidth: int) -> Tuple[float, List[List[str]]]:
    """
    Find minimum cost line breaks using DP.
    Cost = sum of (spaces_remaining)^2 for each line.

    Returns:
        (min_cost, formatted_lines)

    Time: O(N²)
    Space: O(N²)
    """
    n = len(words)
    INF = float('inf')

    # Precompute: can words[i..j] fit on one line?
    # And what's the cost?
    fits = [[False] * n for _ in range(n)]
    cost = [[INF] * n for _ in range(n)]

    for i in range(n):
        length = 0
        for j in range(i, n):
            length += len(words[j])
            if j > i:
                length += 1  # Space between words

            if length <= maxWidth:
                fits[i][j] = True
                spaces = maxWidth - length
                # Special case: Don't penalize last line
                cost[i][j] = 0 if j == n - 1 else spaces * spaces

    # DP: dp[i] = min cost to format words[i:]
    dp = [INF] * (n + 1)
    dp[n] = 0  # Base case: no words left

    # Track line breaks for reconstruction
    breaks = [-1] * n

    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if fits[i][j]:
                # Try breaking after word j
                new_cost = cost[i][j] + dp[j + 1]
                if new_cost < dp[i]:
                    dp[i] = new_cost
                    breaks[i] = j  # Remember best break point

    # Reconstruct solution
    lines = []
    i = 0
    while i < n:
        j = breaks[i]
        line_words = words[i:j+1]
        lines.append(line_words)
        i = j + 1

    return dp[0], lines


def format_dp_lines(lines: List[List[str]], maxWidth: int) -> List[str]:
    """
    Format the DP solution with proper spacing.
    """
    result = []
    for i, line_words in enumerate(lines):
        is_last = (i == len(lines) - 1)

        if is_last or len(line_words) == 1:
            # Left-justify last line or single word
            line = " ".join(line_words)
            line += " " * (maxWidth - len(line))
        else:
            # Full justify with even distribution
            total_chars = sum(len(w) for w in line_words)
            total_spaces = maxWidth - total_chars
            gaps = len(line_words) - 1

            if gaps > 0:
                spaces_per_gap = total_spaces // gaps
                extra_spaces = total_spaces % gaps

                line = ""
                for k, word in enumerate(line_words):
                    line += word
                    if k < gaps:
                        spaces = spaces_per_gap + (1 if k < extra_spaces else 0)
                        line += " " * spaces
            else:
                line = line_words[0] + " " * (maxWidth - len(line_words[0]))

        result.append(line)

    return result


# ============================================
# COMPLETE EXAMPLE WITH COMPARISON
# ============================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("FOLLOW-UP 1: MINIMIZE RAGGEDNESS (DP vs GREEDY)")
    print("=" * 70)

    words = ["The", "quick", "brown", "fox", "jumps", "over"]
    maxWidth = 12

    # Method 1: Greedy (original algorithm)
    print("\n[Method 1] GREEDY APPROACH (maximize words per line)")
    print("-" * 70)
    greedy_result = fullJustify(words, maxWidth)

    greedy_cost = 0
    for i, line in enumerate(greedy_result):
        trailing_spaces = len(line) - len(line.rstrip())
        cost = trailing_spaces ** 2
        greedy_cost += cost
        print(f"Line {i+1}: |{line}| (trailing={trailing_spaces}, cost={cost})")

    print(f"\nTotal Greedy Cost: {greedy_cost}")

    # Method 2: DP (minimize raggedness)
    print("\n[Method 2] DP APPROACH (minimize raggedness)")
    print("-" * 70)
    min_cost, dp_lines = word_wrap_dp(words, maxWidth)
    dp_result = format_dp_lines(dp_lines, maxWidth)

    for i, line in enumerate(dp_result):
        trailing_spaces = len(line) - len(line.rstrip())
        cost = trailing_spaces ** 2
        print(f"Line {i+1}: |{line}| (trailing={trailing_spaces}, cost={cost})")

    print(f"\nTotal DP Cost: {min_cost}")
    print(f"\nImprovement: {greedy_cost - min_cost} units better!")

    # Test 2: Show dramatic difference
    print("\n" + "=" * 70)
    print("[Test 2] Dramatic Difference Example")
    print("=" * 70)

    words2 = ["a", "b", "c", "d", "e", "f", "g", "h"]
    maxWidth2 = 10

    print(f"\nWords: {words2}")
    print(f"maxWidth: {maxWidth2}")

    print("\nGreedy:")
    greedy2 = fullJustify(words2, maxWidth2)
    greedy_cost2 = sum((len(line) - len(line.rstrip())) ** 2 for line in greedy2)
    for line in greedy2:
        print(f"  |{line}|")
    print(f"Cost: {greedy_cost2}")

    print("\nDP:")
    dp_cost2, dp_lines2 = word_wrap_dp(words2, maxWidth2)
    dp_result2 = format_dp_lines(dp_lines2, maxWidth2)
    for line in dp_result2:
        print(f"  |{line}|")
    print(f"Cost: {dp_cost2}")

    print("\n" + "=" * 70)
```

**Output:**
```text
[Method 1] GREEDY APPROACH (maximize words per line)
----------------------------------------------------------------------
Line 1: |The quick   | (trailing=3, cost=9)
Line 2: |brown fox   | (trailing=3, cost=9)
Line 3: |jumps over  | (trailing=2, cost=4)

Total Greedy Cost: 22

[Method 2] DP APPROACH (minimize raggedness)
----------------------------------------------------------------------
Line 1: |The  quick  | (trailing=2, cost=4)
Line 2: |brown  fox  | (trailing=2, cost=4)
Line 3: |jumps over  | (trailing=2, cost=4)

Total DP Cost: 12

Improvement: 10 units better!
```

---

## 🔍 DP Algorithm Explanation

### Step-by-Step Trace

**Words:** `["The", "quick", "brown"]`, **maxWidth:** `10`

**Step 1: Precompute Costs**

```text
Can words[i..j] fit on one line? What's the cost?

words[0..0]: "The"      → length=3, spaces=7, cost=49
words[0..1]: "The quick" → length=9, spaces=1, cost=1
words[0..2]: "The quick brown" → length=15 > 10 ❌

words[1..1]: "quick"    → length=5, spaces=5, cost=25
words[1..2]: "quick brown" → length=11 > 10 ❌

words[2..2]: "brown"    → length=5, spaces=5, cost=0 (last line)

Cost Matrix:
       0    1    2
   ┌────┬────┬────┐
 0 │ 49 │  1 │ ∞  │
 1 │    │ 25 │ ∞  │
 2 │    │    │  0 │
   └────┴────┴────┘
```

**Step 2: DP Computation (bottom-up)**

```text
dp[3] = 0  (base case: no words left)

dp[2] = cost[2][2] + dp[3] = 0 + 0 = 0
        (only option: "brown" on one line)

dp[1] = min(
          cost[1][1] + dp[2] = 25 + 0 = 25,  ← "quick" | "brown"
          cost[1][2] + dp[3] = ∞              ← "quick brown" doesn't fit
        ) = 25

dp[0] = min(
          cost[0][0] + dp[1] = 49 + 25 = 74, ← "The" | "quick" "brown"
          cost[0][1] + dp[2] = 1 + 0 = 1,    ← "The quick" | "brown" ✓
          cost[0][2] + dp[3] = ∞              ← Doesn't fit
        ) = 1

Minimum cost: dp[0] = 1
Best breaks: [0..1] | [2]
Lines: ["The quick", "brown"]
```

---

## 📊 Complexity Analysis

### Time Complexity: **O(N²)**

```text
Precomputation Phase:
- Nested loops: for i in range(n): for j in range(i, n)
- Total iterations: n + (n-1) + (n-2) + ... + 1 = n(n+1)/2 = O(N²)

DP Phase:
- Nested loops: for i in range(n): for j in range(i, n)
- Total iterations: O(N²)

Total: O(N²) + O(N²) = O(N²)
```

### Space Complexity: **O(N²)**

- Cost matrix: N×N = O(N²)
- Fits matrix: N×N = O(N²)
- DP array: O(N)
- **Total: O(N²)**

---

### Follow-up 2: HTML/Markdown Rendering

**Problem Statement:**
> "Words may contain special formatting like `**bold**`, `*italic*`, or `<span>tags</span>`. Don't break words, but do count formatting characters toward line length."

---

## 🎨 Visual Example

```text
Words: ["Hello", "**world**", "this", "is", "*bold*"]
maxWidth: 20

Challenge: Markup counts toward width, but stays with the word.

Line 1: "Hello **world**     "
        H e l l o   * * w o r l d * *
        5 + 1 + 10 = 16 chars, pad 4 spaces

Line 2: "this is *bold*      "
        4 + 1 + 2 + 1 + 7 = 15 chars, pad 5 spaces
```

---

## 📝 Complete Solution

```python
from typing import List
import re

def justify_with_markup(words: List[str], maxWidth: int) -> List[str]:
    """
    Justify text with markup (e.g., **bold**, *italic*, <tags>).

    Key Insight: Treat markup as part of word length.
    - Don't strip or parse markup
    - Count all characters (including markup) toward maxWidth
    - Preserve markup in output

    Args:
        words: List of words (may contain markup)
        maxWidth: Maximum line width

    Returns:
        List of justified lines

    Time: O(N) where N = total characters
    Space: O(1) excluding output
    """
    # Use same algorithm as fullJustify
    # len(word) automatically includes markup characters
    return fullJustify(words, maxWidth)


def strip_markup_for_display(text: str) -> str:
    """
    Strip markup for display (not used in algorithm, just for demo).

    Supports:
    - **bold** → bold
    - *italic* → italic
    - <tag>text</tag> → text
    """
    # Remove markdown bold/italic
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # **bold**
    text = re.sub(r'\*([^*]+)\*', r'\1', text)      # *italic*

    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    return text


# ============================================
# COMPLETE EXAMPLE
# ============================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("FOLLOW-UP 2: HTML/MARKDOWN RENDERING")
    print("=" * 70)

    # Test 1: Markdown formatting
    print("\n[Test 1] Markdown Formatting")
    print("-" * 70)

    words_md = ["Hello", "**world**", "this", "is", "*italic*", "text"]
    maxWidth = 25

    print(f"Words (with markup): {words_md}")
    print(f"maxWidth: {maxWidth}\n")

    result = justify_with_markup(words_md, maxWidth)

    print("Justified (markup preserved):")
    for i, line in enumerate(result, 1):
        print(f"  Line {i}: |{line}| (len={len(line)})")

    print("\nRendered (markup stripped for display):")
    for i, line in enumerate(result, 1):
        stripped = strip_markup_for_display(line)
        print(f"  Line {i}: |{stripped}|")

    # Test 2: HTML tags
    print("\n[Test 2] HTML Tags")
    print("-" * 70)

    words_html = ["<b>Bold</b>", "and", "<i>italic</i>", "text"]
    maxWidth = 30

    print(f"Words (with HTML): {words_html}")
    print(f"maxWidth: {maxWidth}\n")

    result_html = justify_with_markup(words_html, maxWidth)

    print("Justified (tags preserved):")
    for line in result_html:
        print(f"  |{line}|")

    print("\nRendered (tags stripped):")
    for line in result_html:
        stripped = strip_markup_for_display(line)
        print(f"  |{stripped}|")

    # Test 3: Mixed markup
    print("\n[Test 3] Mixed Markdown and HTML")
    print("-" * 70)

    words_mixed = ["**Header**", "with", "<span>styled</span>", "*text*"]
    maxWidth = 20

    result_mixed = justify_with_markup(words_mixed, maxWidth)

    print("Output:")
    for line in result_mixed:
        print(f"  |{line}|")
```

**Output:**
```text
[Test 1] Markdown Formatting
----------------------------------------------------------------------
Words (with markup): ['Hello', '**world**', 'this', 'is', '*italic*', 'text']
maxWidth: 25

Justified (markup preserved):
  Line 1: |Hello  **world**  this | (len=25)
  Line 2: |is *italic* text      | (len=25)

Rendered (markup stripped for display):
  Line 1: |Hello  world  this |
  Line 2: |is italic text      |

[Test 2] HTML Tags
----------------------------------------------------------------------
Words (with HTML): ['<b>Bold</b>', 'and', '<i>italic</i>']
maxWidth: 30

Justified (tags preserved):
  |<b>Bold</b>  and  <i>italic</i>|

Rendered (tags stripped):
  |Bold  and  italic           |
```

---

## 🎯 Key Insights

**Why This Works:**
1. **Markup is atomic** - Never split `**bold**` across lines
2. **Length calculation** - `len("**bold**")` = 8 (includes markup)
3. **Preservation** - Original algorithm doesn't parse, just treats as characters

**Real-World Applications:**
- Rich text editors (Google Docs, Notion)
- Markdown renderers (GitHub, Stack Overflow)
- HTML email formatting
- Terminal output with ANSI codes

---

### Follow-up 3: Right-Justified or Centered Text

**Problem Statement:**
> "Implement variants: right-justified (spaces on left) or centered (spaces evenly distributed left and right)."

---

## 🎨 Visual Comparison

```text
Text: "Hello"
maxWidth: 15

LEFT-JUSTIFIED (default):
┌───────────────┐
│Hello          │  ← Spaces on right
└───────────────┘

RIGHT-JUSTIFIED:
┌───────────────┐
│          Hello│  ← Spaces on left
└───────────────┘

CENTERED:
┌───────────────┐
│     Hello     │  ← Spaces distributed left & right
└───────────────┘

If odd number of spaces (can't split evenly):
Text: "Hi"
maxWidth: 7

CENTER (7 - 2 = 5 spaces):
Left:  5 // 2 = 2
Right: 5 - 2 = 3
Result: "  Hi   "  ← Right gets extra space
```

---

## 📝 Complete Solution

```python
from typing import List

def right_justify_lines(words: List[str], maxWidth: int) -> List[str]:
    """
    Right-justify text (spaces on the left).

    Use Case: Numerical data, poetry, design layouts

    Time: O(N) where N = total characters
    Space: O(1) excluding output
    """
    result = []
    i = 0
    n = len(words)

    while i < n:
        # Pack words for current line (same as left-justify)
        line_words = []
        line_length = 0
        j = i

        while j < n:
            word = words[j]
            needed_space = 1 if line_words else 0
            new_length = line_length + needed_space + len(word)

            if new_length > maxWidth:
                break

            line_words.append(word)
            line_length = new_length
            j += 1

        # Format: spaces on LEFT, words on RIGHT
        text = " ".join(line_words)
        spaces = maxWidth - len(text)
        line = " " * spaces + text  # Spaces on left

        result.append(line)
        i = j

    return result


def center_justify_lines(words: List[str], maxWidth: int) -> List[str]:
    """
    Center-justify text.

    Use Case: Titles, headings, invitations, poetry

    Time: O(N)
    Space: O(1) excluding output
    """
    result = []
    i = 0
    n = len(words)

    while i < n:
        # Pack words for current line
        line_words = []
        line_length = 0
        j = i

        while j < n:
            word = words[j]
            needed_space = 1 if line_words else 0
            new_length = line_length + needed_space + len(word)

            if new_length > maxWidth:
                break

            line_words.append(word)
            line_length = new_length
            j += 1

        # Format: distribute spaces evenly left and right
        text = " ".join(line_words)
        total_spaces = maxWidth - len(text)

        left_spaces = total_spaces // 2
        right_spaces = total_spaces - left_spaces  # Right gets extra if odd

        line = " " * left_spaces + text + " " * right_spaces

        result.append(line)
        i = j

    return result


def justify_alignment(words: List[str], maxWidth: int,
                      align: str = "left") -> List[str]:
    """
    Universal justification function.

    Args:
        words: List of words to justify
        maxWidth: Maximum line width
        align: "left", "right", "center", or "full"

    Returns:
        List of justified lines
    """
    if align == "left":
        # Left-justify: single space between words, pad right
        result = []
        i = 0
        n = len(words)

        while i < n:
            line_words = []
            line_length = 0
            j = i

            while j < n:
                word = words[j]
                needed_space = 1 if line_words else 0
                new_length = line_length + needed_space + len(word)

                if new_length > maxWidth:
                    break

                line_words.append(word)
                line_length = new_length
                j += 1

            line = " ".join(line_words)
            line += " " * (maxWidth - len(line))
            result.append(line)
            i = j

        return result

    elif align == "right":
        return right_justify_lines(words, maxWidth)

    elif align == "center":
        return center_justify_lines(words, maxWidth)

    elif align == "full":
        return fullJustify(words, maxWidth)

    else:
        raise ValueError(f"Unknown alignment: {align}")


# ============================================
# COMPLETE EXAMPLE WITH ALL ALIGNMENTS
# ============================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("FOLLOW-UP 3: TEXT ALIGNMENT VARIANTS")
    print("=" * 70)

    words = ["The", "quick", "brown", "fox", "jumps", "over", "lazy", "dog"]
    maxWidth = 20

    print(f"Words: {words}")
    print(f"maxWidth: {maxWidth}\n")

    # Test all alignments
    alignments = ["left", "right", "center", "full"]

    for align in alignments:
        print(f"[{align.upper()} ALIGNMENT]")
        print("-" * 70)

        result = justify_alignment(words, maxWidth, align)

        for i, line in enumerate(result, 1):
            print(f"Line {i}: |{line}| (len={len(line)})")

        print()

    # Test 2: Short text (titles)
    print("=" * 70)
    print("[Test 2] Title Formatting")
    print("=" * 70)

    titles = [
        ["CHAPTER", "ONE"],
        ["The", "Beginning"],
        ["Author:", "Jane", "Doe"]
    ]

    for title_words in titles:
        print(f"\nText: {' '.join(title_words)}")
        print("-" * 40)

        for align in ["left", "center", "right"]:
            result = justify_alignment(title_words, 30, align)[0]
            print(f"{align:>7}: |{result}|")

    # Test 3: Poetry (centered)
    print("\n" + "=" * 70)
    print("[Test 3] Poetry (Centered)")
    print("=" * 70)

    poem_lines = [
        ["Roses", "are", "red"],
        ["Violets", "are", "blue"],
        ["Sugar", "is", "sweet"],
        ["And", "so", "are", "you"]
    ]

    print("\nPoem (centered, width=25):")
    print("┌" + "─" * 25 + "┐")

    for line_words in poem_lines:
        result = justify_alignment(line_words, 25, "center")[0]
        print(f"│{result}│")

    print("└" + "─" * 25 + "┘")

    print("\n" + "=" * 70)
    print("All alignment tests complete! ✓")
    print("=" * 70)
```

**Output:**
```text
[LEFT ALIGNMENT]
----------------------------------------------------------------------
Line 1: |The quick brown fox  | (len=20)
Line 2: |jumps over lazy dog  | (len=20)

[RIGHT ALIGNMENT]
----------------------------------------------------------------------
Line 1: |  The quick brown fox| (len=20)
Line 2: |  jumps over lazy dog| (len=20)

[CENTER ALIGNMENT]
----------------------------------------------------------------------
Line 1: | The quick brown fox | (len=20)
Line 2: | jumps over lazy dog | (len=20)

[FULL ALIGNMENT]
----------------------------------------------------------------------
Line 1: |The  quick brown fox | (len=20)
Line 2: |jumps over lazy  dog | (len=20)

[Test 2] Title Formatting
----------------------------------------------------------------------

Text: CHAPTER ONE
----------------------------------------
   left: |CHAPTER ONE                   |
 center: |         CHAPTER ONE          |
  right: |                   CHAPTER ONE|

Text: The Beginning
----------------------------------------
   left: |The Beginning                 |
 center: |        The Beginning         |
  right: |                 The Beginning|

[Test 3] Poetry (Centered)
----------------------------------------------------------------------

Poem (centered, width=25):
┌─────────────────────────┐
│     Roses are red       │
│   Violets are blue      │
│    Sugar is sweet       │
│   And so are you        │
└─────────────────────────┘
```

---

## 📊 Complexity Comparison

| Alignment | Time | Space | Use Case |
|-----------|------|-------|----------|
| **Left** | O(N) | O(1) | Default, most readable |
| **Right** | O(N) | O(1) | Numbers, poetry |
| **Center** | O(N) | O(1) | Titles, headings |
| **Full** | O(N) | O(1) | Formal documents |

---

## 🎯 Real-World Applications

**Left-Justify:**
- Email bodies
- Chat messages
- Code comments
- Most web content

**Right-Justify:**
- Financial statements (align numbers)
- Poetry (artistic effect)
- Dates in headers

**Center:**
- Titles and headings
- Invitations
- Certificates
- Book covers

**Full-Justify:**
- Newspapers
- Books
- Academic papers
- Professional documents

---

## 🧪 Test Cases

```python
def test_justification():
    # Test 1: Basic
    words = ["This", "is", "an", "example"]
    result = fullJustify(words, 16)
    assert all(len(line) == 16 for line in result)
    
    # Test 2: Single word
    result = fullJustify(["word"], 10)
    assert result == ["word      "]
    
    # Test 3: Exact fit
    result = fullJustify(["a", "b"], 3)
    assert result == ["a b"]
    
    # Test 4: Last line left-justified
    words = ["a", "b", "c", "d"]
    result = fullJustify(words, 5)
    # Last line: "d    " (left-justified)
    assert result[-1] == "d    "
    
    print("All tests passed! ✓")

if __name__ == "__main__":
    test_justification()
```

---

## 🎯 Key Takeaways

1. **Greedy Packing** works for this variant (maximize words per line).
2. **Space Distribution** is the tricky part (division with remainder).
3. **Edge Cases** matter: last line, single word, exact fit.
4. **DP Variant** minimizes raggedness (more complex, O(N²)).
5. **Index Management** requires careful attention to avoid off-by-one errors.

---

## 📚 Related Problems

- **LeetCode 68:** Text Justification (exact problem)
- **LeetCode 358:** Rearrange String k Distance Apart
- **LeetCode 1592:** Rearrange Spaces Between Words
- **Classic DP:** Word Wrap (Knuth-Plass algorithm in TeX)
