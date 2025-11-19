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

**Solution: Dynamic Programming**

```python
def word_wrap_dp(words: List[str], maxWidth: int) -> float:
    """
    Find minimum cost line breaks using DP.
    Cost = sum of (spaces_remaining)^2 for each line.
    
    Returns minimum cost (not the actual formatting).
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
                cost[i][j] = spaces * spaces
    
    # DP: dp[i] = min cost to format words[i:]
    dp = [INF] * (n + 1)
    dp[n] = 0  # Base case: no words left
    
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if fits[i][j]:
                # Try breaking after word j
                dp[i] = min(dp[i], cost[i][j] + dp[j + 1])
    
    return dp[0]


# ============================================
# EXAMPLE
# ============================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("FOLLOW-UP 1: MINIMIZE RAGGEDNESS (DP)")
    print("=" * 60)
    
    words = ["The", "quick", "brown", "fox"]
    maxWidth = 10
    
    min_cost = word_wrap_dp(words, maxWidth)
    print(f"Words: {words}")
    print(f"maxWidth: {maxWidth}")
    print(f"Minimum raggedness cost: {min_cost}")
```

**Complexity:**
- **Time:** O(N²) to compute costs + O(N²) for DP = **O(N²)**.
- **Space:** O(N²) for cost matrix.

---

### Follow-up 2: HTML/Markdown Rendering

**Problem Statement:**
> "Words may contain special formatting like `**bold**`. Don't break words, but do count formatting characters toward line length."

**Solution:**
Treat each word as an atomic unit (don't split). Count full length including markup.

```python
def justify_with_markup(words: List[str], maxWidth: int) -> List[str]:
    """
    Justify text with markup (e.g., **bold**).
    Markup characters count toward maxWidth.
    """
    # Use same algorithm, but len(word) includes markup
    return fullJustify(words, maxWidth)

# Example:
words_with_markup = ["This", "is", "**bold**", "text"]
result = justify_with_markup(words_with_markup, 20)
```

---

### Follow-up 3: Right-Justified or Centered

**Problem Statement:**
> "Implement variants: right-justified (spaces on left) or centered (spaces evenly distributed left and right)."

**Solution:**

```python
def right_justify(words: List[str], maxWidth: int) -> List[str]:
    """
    Right-justify text (spaces on the left).
    """
    result = []
    for word in words:
        spaces = maxWidth - len(word)
        result.append(" " * spaces + word)
    return result

def center_justify(words: List[str], maxWidth: int) -> List[str]:
    """
    Center-justify text.
    """
    result = []
    for word in words:
        spaces = maxWidth - len(word)
        left_spaces = spaces // 2
        right_spaces = spaces - left_spaces
        result.append(" " * left_spaces + word + " " * right_spaces)
    return result
```

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
