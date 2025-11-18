# 📂 PROBLEM 7: FILE COLLECTIONS REPORT

### ⭐⭐⭐ **File Size & Top-K Collections**

**Frequency:** Medium
**Similar to:** Top K Frequent Elements, but with aggregation.

**Problem Statement:**
> You are given a list of files. Each file has a `name`, `size`, and `collection_id` (optional).
>
> You need to generate a report that shows:
> 1.  **Total Size** of files stored in the system.
> 2.  **Top K Collections** by total size of files within them.

**Input Format:**
```python
files = [
    {"file": "file1.txt", "size": 100, "collectionId": "col1"},
    {"file": "file2.txt", "size": 200, "collectionId": "col1"},
    {"file": "file3.txt", "size": 200, "collectionId": "col2"},
    {"file": "file4.txt", "size": 100, "collectionId": None} 
]
```

**Output:**
- Total Size: 600
- Top K (e.g., K=2) Collections: `["col1" (300), "col2" (200)]`

---

### 🗣️ **Interview Conversation Guide**

**Phase 1: Clarification**
- **Candidate:** "What do we do with files that have `collectionId: None`?"
- **Interviewer:** "Include them in 'Total Size', but ignore them for the 'Top K Collections' report."
- **Candidate:** "Can the file size be negative?"
- **Interviewer:** "No."
- **Candidate:** "Is K usually small?"
- **Interviewer:** "Yes, K is much smaller than the number of collections."

**Phase 2: Approach**
- **Candidate:** "This is a standard aggregation problem."
- **Candidate:** "We can iterate through the files once ($O(N)$)."
- **Candidate:** "Maintain a running `total_size`."
- **Candidate:** "Use a Hash Map (`collection_map`) to aggregate size per collection."
- **Candidate:** "After processing all files, we have a map of `{col1: 300, col2: 200}`."
- **Candidate:** "To find Top K, we can sort the map items ($O(C \log C)$ where $C$ is num collections) or use a **Min-Heap** of size K ($O(C \log K)$)."
- **Candidate:** "Since $C$ can be large and $K$ is small, the Heap approach is optimal."

**Phase 3: Coding**
- Define `process_files` function.
- Use `defaultdict` for aggregation.
- Use `heapq.nlargest` or maintain a custom heap.

---

### 📝 **Solution Approach: HashMap + Heap**

**Steps:**
1.  **Aggregate:** Loop through files. Sum global size. Sum per-collection size in a HashMap.
2.  **Top K:** Use `heapq.nlargest` on the items of the HashMap.

**Implementation:**

```python
from collections import defaultdict
import heapq
from typing import List, Dict, Optional

def generate_report(files: List[Dict], k: int):
    total_size = 0
    collection_sizes = defaultdict(int)

    # 1. Aggregation Phase
    for f in files:
        size = f.get("size", 0)
        col_id = f.get("collectionId")

        # Add to global total
        total_size += size

        # Add to collection total if it belongs to one
        if col_id is not None:
            collection_sizes[col_id] += size

    # 2. Top K Phase
    # collection_sizes.items() returns [(col1, 300), (col2, 200), ...]
    # We want to sort by size (item[1]) descending.
    
    top_k_collections = heapq.nlargest(
        k, 
        collection_sizes.items(), 
        key=lambda item: item[1]
    )

    # Formatting output
    return {
        "total_size": total_size,
        "top_collections": top_k_collections
    }

# Usage
data = [
    {"file": "a.txt", "size": 100, "collectionId": "c1"},
    {"file": "b.txt", "size": 200, "collectionId": "c1"},
    {"file": "c.txt", "size": 300, "collectionId": "c2"},
    {"file": "d.txt", "size": 50,  "collectionId": None}
]

report = generate_report(data, k=1)
print(report)
# Output: {'total_size': 650, 'top_collections': [('c2', 300)]}
# c1 total is 300, c2 is 300. Ties broken arbitrarily or by key stability.
```

**Complexity Analysis:**
- **Time:** $O(N + C \log K)$. $N$ to iterate files. $C$ to iterate collections (where $C \le N$). Heap operations take $\log K$.
- **Space:** $O(C)$ to store the map.

---

### 🔄 **Follow-up 1: Streaming / Large Dataset**

**Problem:**
> The file list is too large to fit in memory. It comes as a stream.
> You cannot store all collection IDs in a map if there are millions of unique collections.
> However, you assume **Top K** are significantly larger than the "long tail" of small collections.

**Solution:**
> This becomes a **Heavy Hitters** problem (e.g., Count-Min Sketch or Misra-Gries).
> But generally for interview simplification:
> - If we can't store *all*, can we store *some*? LRU cache approach?
> - Or simply, assume we can store the map (usually fits), but maybe we process files in chunks (MapReduce).
> - **MapReduce**:
>   - Mapper: Reads chunk of files, emits `(col_id, size)`.
>   - Reducer: Sums sizes for `col_id`.
>   - Finalizer: Finds Top K.

---

### 🧪 **Test Cases**

**Basic:**
- 2 collections, K=1. Returns largest.
- Files with `None` collection. Checked `total_size` matches.

**Ties:**
- col1: 100, col2: 100. `heapq` handles ties (usually by key).

**Edge Cases:**
- Empty file list -> Total 0, Top K empty.
- K=0 -> Top K empty.
- K > Number of collections -> Returns all collections sorted.
- File size 0.
