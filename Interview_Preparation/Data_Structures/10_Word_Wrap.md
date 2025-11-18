# 📝 PROBLEM 10: WORD WRAP / TEXT JUSTIFICATION

### ⭐⭐⭐⭐ **Text Formatting**

**Frequency:** Medium-High
**Similar to:** [LeetCode 68. Text Justification](https://leetcode.com/problems/text-justification/)

**Problem Statement:**
> Given a list of words and a `maxWidth`, format the text such that each line has exactly `maxWidth` characters.
>
> **Rules:**
> 1.  Pack as many words as you can in each line.
> 2.  Pad extra spaces `' '` evenly between words.
> 3.  If spaces don't divide evenly, place more spaces on the left slots.
> 4.  **Last Line** should be left-justified (no extra padding between words).

**Visual Example:**
```text
Words: ["This", "is", "an", "example", "of", "text", "justification."]
Width: 16

Line 1: "This    is    an"  (3 words, 8 letters. 8 spaces needed. 4, 4)
Line 2: "example  of text"  (3 words, 13 letters. 3 spaces. 2, 1)
Line 3: "justification.  "  (Last line, left justified, pad end)
```

---

### 🗣️ **Interview Conversation Guide**

**Phase 1: Clarification**
- **Candidate:** "How do we handle a single word that is longer than `maxWidth`?"
- **Interviewer:** "Assume guaranteed that every word fits within `maxWidth`."
- **Candidate:** "For the last line, just single space between words and pad right?"
- **Interviewer:** "Correct."

**Phase 2: Approach**
- **Candidate:** "This is a Greedy approach line by line."
- **Candidate:** "1. Identify the range of words `[i, j]` that fit in current line."
- **Candidate:** "2. Calculate total spaces needed = `maxWidth - total_letters`."
- **Candidate:** "3. Distribute spaces."
- **Candidate:** "   - If it's the last line or only 1 word: Left justify (pad right)."
- **Candidate:** "   - Otherwise: Round Robin distribution of spaces."

**Phase 3: Coding**
- Carefully manage indices `i` and `j`.
- Write a helper `create_line(words, maxWidth, is_last)`.

---

### 📝 **Solution Approach: Greedy with Space Distribution**

```python
from typing import List

def fullJustify(words: List[str], maxWidth: int) -> List[str]:
    res = []
    i = 0
    n = len(words)
    
    while i < n:
        # 1. Find words that fit in this line
        line_words = []
        line_len = 0
        j = i
        
        while j < n:
            # Length if we add this word: 
            # current_len + len(new_word) + (1 space if not first word)
            added_len = len(words[j])
            if line_len + added_len + (1 if line_words else 0) > maxWidth:
                break
            
            if line_words:
                line_len += 1 # standard space
            line_len += added_len
            line_words.append(words[j])
            j += 1
            
        # Now line_words contains words for this line
        # Range is words[i:j]
        
        # 2. Format the line
        remaining_slots = maxWidth - sum(len(w) for w in line_words)
        
        # Case A: Last line or Single word -> Left Justified
        if j == n or len(line_words) == 1:
            joined = " ".join(line_words)
            res.append(joined + " " * (maxWidth - len(joined)))
            
        # Case B: Fully Justified
        else:
            # Gaps between words
            gaps = len(line_words) - 1
            spaces_per_gap = remaining_slots // gaps
            extra_spaces = remaining_slots % gaps
            
            line_str = ""
            for k, w in enumerate(line_words):
                line_str += w
                if k < gaps:
                    # Add calculated spaces
                    # First 'extra_spaces' gaps get +1 space
                    spaces = spaces_per_gap + (1 if k < extra_spaces else 0)
                    line_str += " " * spaces
            res.append(line_str)
            
        i = j # Move to next batch
        
    return res

# Test
text = ["This", "is", "an", "example", "of", "text", "justification."]
for line in fullJustify(text, 16):
    print(f"|{line}|")
```

---

### 🔄 **Follow-up: DP Variant (Minimize raggedness)**

**Problem:**
> Instead of greedy packing, choose line breaks such that the sum of squares of empty spaces on each line is minimized. (Like LaTeX/TeX).

**Solution:**
> This is a standard **Dynamic Programming** problem (Word Wrap).
> `DP[i]` = Min cost to format words `i...n`.
> Cost of a line = `(spaces_remaining)^2`.
> `DP[i] = min(Cost(i, j) + DP[j+1])` for all valid `j`.

---

### 🧪 **Test Cases**

**Basic:**
- Words fit exactly (0 extra spaces).
- Words need uneven spacing (4 spaces, 3 gaps -> 2, 1, 1).

**Edge:**
- Single word in input.
- Single word per line (long words).
- Last line has exact width (no padding).
