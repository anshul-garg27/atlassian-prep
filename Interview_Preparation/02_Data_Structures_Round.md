# 🧠 DATA STRUCTURES / ALGO ROUND - Complete Guide

**Duration:** 60 minutes
**Format:** 1-2 DSA problems with multiple follow-ups
**Difficulty:** Medium to Hard
**Pass Rate:** ~60% (hardest technical round)

---

## 📋 Round Structure

```
┌──────────────────────────────────────────────────┐
│ Main Problem (30-35 minutes)                     │
│ ├─ Problem statement + clarifications            │
│ ├─ Approach discussion                           │
│ ├─ Code implementation                           │
│ └─ Test cases + complexity analysis              │
├──────────────────────────────────────────────────┤
│ Follow-ups (20-25 minutes)                       │
│ ├─ Extension 1: Add constraint                   │
│ ├─ Extension 2: Optimize further                 │
│ └─ Extension 3: Handle edge cases / concurrency  │
└──────────────────────────────────────────────────┘
```

---

## 📚 Problem Collection

The questions have been organized into individual files for better readability.

| # | Problem Name | Frequency | Key Concept | Link |
|---|--------------|-----------|-------------|------|
| 1 | **Employee Hierarchy** | ⭐⭐⭐⭐⭐ (60%) | LCA, N-ary Tree | [View Problem](./Data_Structures/01_Employee_Hierarchy.md) |
| 2 | **Stock Price Fluctuation** | ⭐⭐⭐⭐ | SortedList, Heap, Map | [View Problem](./Data_Structures/02_Stock_Price_Fluctuation.md) |
| 3 | **Content Popularity** | ⭐⭐⭐⭐ (40%) | Doubly Linked List + Map | [View Problem](./Data_Structures/03_Content_Popularity.md) |
| 4 | **Tennis Court Booking** | ⭐⭐⭐ (30%) | Greedy, Heap, Intervals | [View Problem](./Data_Structures/04_Tennis_Court_Booking.md) |
| 5 | **Router / Wildcards** | ⭐⭐⭐ (25%) | Trie | [View Problem](./Data_Structures/05_Router_Wildcards.md) |
| 6 | **Commodity Prices** | ⭐⭐ | SortedMap, Segment Tree | [View Problem](./Data_Structures/06_Commodity_Prices.md) |
| 7 | **File Collections** | ⭐⭐ | Heap, HashMap | [View Problem](./Data_Structures/07_File_Collections.md) |
| 8 | **Robot Parts** | ⭐⭐ | Set, HashMap | [View Problem](./Data_Structures/08_Robot_Parts.md) |
| 9 | **Vote Counting** | ⭐⭐ | Sorting, Comparator | [View Problem](./Data_Structures/09_Vote_Counting.md) |
| 10 | **Word Wrap** | ⭐⭐⭐ | Greedy, Strings | [View Problem](./Data_Structures/10_Word_Wrap.md) |
| 11 | **OA Problems** | ⭐ | Math, DP | [View Problem](./Data_Structures/11_OA_Problems.md) |

---

## 📊 SUMMARY & KEY TAKEAWAYS

### 🎯 Most Important Problems (Must Practice)

1. **Employee Hierarchy (60% frequency)** ⭐⭐⭐⭐⭐
   - Master LCA algorithm
   - Practice all follow-ups
   - Know thread-safe implementation

2. **Content Popularity (40% frequency)** ⭐⭐⭐⭐
   - Learn Doubly Linked List + HashMap pattern
   - All O(1) operations
   - Similar to LRU Cache design

3. **Tennis Court Booking (30% frequency)** ⭐⭐⭐
   - Meeting Rooms II pattern
   - Min-heap for greedy assignment

### ✅ Success Checklist

**Before the Interview:**
- [ ] Solve Employee Hierarchy 5+ times
- [ ] Implement Content Popularity from scratch 3 times
- [ ] Practice explaining time/space complexity
- [ ] Review all follow-up variations
- [ ] Review Robot Parts and File Collection problems

**During the Interview:**
- [ ] Ask clarifying questions
- [ ] Discuss approach before coding
- [ ] Write clean, modular code
- [ ] Test with examples
- [ ] Analyze complexity
- [ ] Handle edge cases

### ❌ Common Mistakes to Avoid

1. **Not asking clarifying questions**
   - "Can employees be in multiple groups?"
   - "Is the input sorted?"
   - "What should I return if no solution?"

2. **Jumping to code too quickly**
   - Discuss approach first
   - Confirm with interviewer
   - Then code

3. **Ignoring edge cases**
   - Employee doesn't exist
   - Empty group
   - Circular dependencies

4. **Poor time complexity analysis**
   - Be precise: O(n log n), not just "O(n something)"
   - Explain which operations dominate

5. **Not testing code**
   - Walk through at least 2-3 examples
   - Include edge case

---

**Next:** [03_Code_Design_LLD_Round.md](./03_Code_Design_LLD_Round.md) - Low-Level Design problems

**Back to:** [README.md](./README.md)
