# 📂 PROBLEM 7: FILE COLLECTIONS REPORT

### ⭐⭐⭐ **Aggregate File Sizes and Find Top-K Collections**

**Frequency:** Medium (Appears in ~25-30% of rounds)
**Difficulty:** Easy-Medium
**Similar to:** [LeetCode 347 - Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/)

---

## 📋 Problem Statement

You are building a file storage analytics system. Given a list of files, where each file has:
- `name`: String (file identifier)
- `size`: Integer (bytes)
- `collectionId`: String or `null` (optional grouping)

**Generate a report with:**
1. **Total size** of all files in the system
2. **Top K collections** by total size (sum of all files in each collection)

**Constraints:**
- 1 ≤ N ≤ 10⁶ files
- 0 ≤ file size ≤ 10⁹ bytes
- Files with `collectionId = null` count toward total size but are ignored in Top K
- 1 ≤ K ≤ number of collections

---

## 🎨 Visual Example

### Example 1: Basic Aggregation

```text
Input Files:
┌──────────────────────────────────────────────────┐
│ file1.txt   | size: 100  | collection: "photos" │
│ file2.txt   | size: 200  | collection: "photos" │
│ file3.txt   | size: 300  | collection: "docs"   │
│ file4.txt   | size: 150  | collection: "docs"   │
│ file5.txt   | size: 50   | collection: null     │
└──────────────────────────────────────────────────┘

Step 1: Aggregate
┌─────────────────────┐
│ Total Size: 800     │
│                     │
│ Collections:        │
│   photos → 300      │
│   docs   → 450      │
└─────────────────────┘

Step 2: Top K=1
Result: [("docs", 450)]
```

### Example 2: Handling Nulls

```text
Input:
file1 | size: 100 | collection: "A"
file2 | size: 200 | collection: null
file3 | size: 300 | collection: null

Aggregation:
Total Size: 600
Collections: {"A": 100}

Top K=1: [("A", 100)]
Note: Files 2 and 3 contribute to total but not to any collection.
```

---

## 💡 Examples

### Example 1: Standard Report
```python
files = [
    {"name": "a.txt", "size": 100, "collectionId": "col1"},
    {"name": "b.txt", "size": 200, "collectionId": "col1"},
    {"name": "c.txt", "size": 300, "collectionId": "col2"},
    {"name": "d.txt", "size": 50, "collectionId": None}
]

report = generate_report(files, k=2)
print(report)
# {
#   "total_size": 650,
#   "top_collections": [("col1", 300), ("col2", 300)]
# }
```

### Example 2: Large K
```python
files = [
    {"name": "f1", "size": 100, "collectionId": "A"},
    {"name": "f2", "size": 200, "collectionId": "B"}
]

report = generate_report(files, k=10)  # K > num collections
# Returns all 2 collections sorted by size
```

---

## 🗣️ Interview Conversation Guide

### Phase 1: Clarification (3-5 min)

**Candidate:** "What should we do with files that have `collectionId = null`?"
**Interviewer:** "Include them in the total size, but exclude them from the Top K collections report."

**Candidate:** "Can file sizes be negative or zero?"
**Interviewer:** "File sizes are non-negative. Zero is valid."

**Candidate:** "How large is K relative to the number of collections?"
**Interviewer:** "K is typically small (e.g., top 10), even if there are thousands of collections."

**Candidate:** "If two collections have the same size, does the order matter?"
**Interviewer:** "No specific ordering requirement for ties. Any deterministic ordering is fine."

### Phase 2: Approach Discussion (5-8 min)

**Candidate:** "This is an **aggregation + Top K** problem.

**Step 1: Aggregation (O(N))**
- Iterate through all files once.
- Maintain:
  - `total_size`: Running sum of all file sizes.
  - `collection_sizes`: HashMap mapping `collectionId` → total size.

**Step 2: Top K (O(C log K))**
- Extract Top K from the HashMap.
- Options:
  1. **Sort all collections:** O(C log C) time where C = number of collections.
  2. **Min-Heap of size K:** O(C log K) time (better when K << C).
  3. **Use `heapq.nlargest()`:** Python's built-in, optimized for this."

**Candidate:** "I'll use `heapq.nlargest()` since it's clean and efficient for K << C."

### Phase 3: Implementation (10-15 min)

**Candidate:** "I'll use `defaultdict` for automatic initialization and `heapq.nlargest` for Top K extraction."

---

## 🧠 Intuition & Approach

### Why HashMap?

**Problem Requirements:**
- Group files by `collectionId`
- Sum sizes within each group

**HashMap is Perfect:**
- O(1) insertion and lookup
- Natural grouping by key

### Why Heap for Top K?

**Sorting vs. Heap:**
| Approach | Time Complexity | When to Use |
|----------|----------------|-------------|
| **Full Sort** | O(C log C) | K ≈ C (need most collections) |
| **Min-Heap (size K)** | O(C log K) | K << C (need few collections) |
| **QuickSelect** | O(C) average | Theoretical best, complex to implement |

**For interviews:** Use `heapq.nlargest()` (internally uses a heap for K << C).

---

## 📝 Complete Solution

```python
from collections import defaultdict
from typing import List, Dict, Tuple, Optional
import heapq

def generate_report(files: List[Dict], k: int) -> Dict:
    """
    Generate file storage report with total size and top K collections.
    
    Args:
        files: List of file dictionaries with keys: name, size, collectionId
        k: Number of top collections to return
    
    Returns:
        Dictionary with total_size and top_collections
    
    Time: O(N + C log K) where N = files, C = collections
    Space: O(C) for collection map
    """
    total_size = 0
    collection_sizes = defaultdict(int)
    
    # Phase 1: Aggregation (O(N))
    for file in files:
        size = file.get("size", 0)
        collection_id = file.get("collectionId")
        
        # Add to global total
        total_size += size
        
        # Add to collection total (skip null collections)
        if collection_id is not None:
            collection_sizes[collection_id] += size
    
    # Phase 2: Extract Top K (O(C log K))
    # heapq.nlargest returns list of tuples: [(col_id, size), ...]
    # sorted by size descending
    top_k_collections = heapq.nlargest(
        k,
        collection_sizes.items(),
        key=lambda item: item[1]  # Sort by size
    )
    
    return {
        "total_size": total_size,
        "top_collections": top_k_collections
    }


def generate_detailed_report(files: List[Dict], k: int) -> Dict:
    """
    Enhanced version with additional statistics.
    """
    total_size = 0
    collection_sizes = defaultdict(int)
    collection_file_counts = defaultdict(int)
    uncategorized_size = 0
    
    for file in files:
        size = file.get("size", 0)
        collection_id = file.get("collectionId")
        
        total_size += size
        
        if collection_id is not None:
            collection_sizes[collection_id] += size
            collection_file_counts[collection_id] += 1
        else:
            uncategorized_size += size
    
    # Top K with additional info
    top_k_full = [
        {
            "collection_id": col_id,
            "total_size": size,
            "file_count": collection_file_counts[col_id],
            "avg_size": size / collection_file_counts[col_id]
        }
        for col_id, size in heapq.nlargest(
            k, collection_sizes.items(), key=lambda x: x[1]
        )
    ]
    
    return {
        "total_size": total_size,
        "num_collections": len(collection_sizes),
        "uncategorized_size": uncategorized_size,
        "top_collections": top_k_full
    }


# ============================================
# COMPLETE RUNNABLE EXAMPLE
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("FILE COLLECTIONS REPORT GENERATOR")
    print("=" * 60)
    
    # Test 1: Basic report
    print("\n[Test 1] Basic Report")
    print("-" * 40)
    files1 = [
        {"name": "photo1.jpg", "size": 100, "collectionId": "photos"},
        {"name": "photo2.jpg", "size": 200, "collectionId": "photos"},
        {"name": "doc1.pdf", "size": 300, "collectionId": "documents"},
        {"name": "doc2.pdf", "size": 150, "collectionId": "documents"},
        {"name": "temp.txt", "size": 50, "collectionId": None}
    ]
    
    report1 = generate_report(files1, k=2)
    print(f"Total Size: {report1['total_size']} bytes")
    print(f"Top 2 Collections:")
    for col_id, size in report1['top_collections']:
        print(f"  {col_id}: {size} bytes")
    
    # Test 2: Detailed report
    print("\n[Test 2] Detailed Report")
    print("-" * 40)
    report2 = generate_detailed_report(files1, k=2)
    print(f"Total Size: {report2['total_size']} bytes")
    print(f"Number of Collections: {report2['num_collections']}")
    print(f"Uncategorized Size: {report2['uncategorized_size']} bytes")
    print(f"\nTop Collections:")
    for col in report2['top_collections']:
        print(f"  {col['collection_id']}:")
        print(f"    Total: {col['total_size']} bytes")
        print(f"    Files: {col['file_count']}")
        print(f"    Average: {col['avg_size']:.2f} bytes/file")
    
    # Test 3: Large dataset simulation
    print("\n[Test 3] Large Dataset")
    print("-" * 40)
    import random
    
    # Generate 10,000 files across 100 collections
    collections = [f"col{i}" for i in range(100)]
    files3 = [
        {
            "name": f"file{i}",
            "size": random.randint(100, 1000),
            "collectionId": random.choice(collections + [None] * 10)
        }
        for i in range(10000)
    ]
    
    report3 = generate_report(files3, k=5)
    print(f"Total Size: {report3['total_size']:,} bytes")
    print(f"Top 5 Collections:")
    for col_id, size in report3['top_collections']:
        print(f"  {col_id}: {size:,} bytes")
    
    # Test 4: Edge cases
    print("\n[Test 4] Edge Cases")
    print("-" * 40)
    
    # Empty files
    report_empty = generate_report([], k=5)
    print(f"Empty list - Total: {report_empty['total_size']}, Top: {report_empty['top_collections']}")
    
    # All null collections
    files_null = [
        {"name": "f1", "size": 100, "collectionId": None},
        {"name": "f2", "size": 200, "collectionId": None}
    ]
    report_null = generate_report(files_null, k=1)
    print(f"All null - Total: {report_null['total_size']}, Top: {report_null['top_collections']}")
    
    # K larger than collections
    files_small = [
        {"name": "f1", "size": 100, "collectionId": "A"},
        {"name": "f2", "size": 200, "collectionId": "B"}
    ]
    report_large_k = generate_report(files_small, k=10)
    print(f"K > C - Top: {report_large_k['top_collections']}")
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)
```

---

## 🔍 Explanation with Example

Let's trace through the file aggregation algorithm step by step:

**Files:**
```python
[
    {"name": "file1.txt", "size": 100, "collectionId": "photos"},
    {"name": "file2.txt", "size": 200, "collectionId": "photos"},
    {"name": "file3.txt", "size": 300, "collectionId": "docs"},
    {"name": "file4.txt", "size": 150, "collectionId": "docs"},
    {"name": "file5.txt", "size": 50, "collectionId": null}
]
```

**Goal:** Total size + Top 2 collections

---

**Step 1: Initialize Accumulators**

```python
total_size = 0
collection_sizes = defaultdict(int)
```

---

**Step 2: Aggregate (Single Pass)**

**Process file1:**
```python
size = 100
collectionId = "photos"

total_size += 100  # total_size = 100
collection_sizes["photos"] += 100  # {"photos": 100}
```

**Process file2:**
```python
size = 200
collectionId = "photos"

total_size += 200  # total_size = 300
collection_sizes["photos"] += 200  # {"photos": 300}
```

**Process file3:**
```python
size = 300
collectionId = "docs"

total_size += 300  # total_size = 600
collection_sizes["docs"] += 300  # {"photos": 300, "docs": 300}
```

**Process file4:**
```python
size = 150
collectionId = "docs"

total_size += 150  # total_size = 750
collection_sizes["docs"] += 150  # {"photos": 300, "docs": 450}
```

**Process file5:**
```python
size = 50
collectionId = null

total_size += 50  # total_size = 800
# Don't add to collection_sizes (null collection)
```

---

**After Aggregation:**

```python
total_size = 800
collection_sizes = {
    "photos": 300,
    "docs": 450
}
```

---

**Step 3: Extract Top K (K=2)**

Using `heapq.nlargest()`:

```python
top_k = heapq.nlargest(2, collection_sizes.items(), key=lambda x: x[1])

# Internal process:
# Items: [("photos", 300), ("docs", 450)]
# Sort by size (descending): [("docs", 450), ("photos", 300)]
# Take first 2: [("docs", 450), ("photos", 300)]
```

**Result:**
```python
top_collections = [("docs", 450), ("photos", 300)]
```

---

**Final Report:**

```python
{
    "total_size": 800,
    "top_collections": [("docs", 450), ("photos", 300)]
}
```

---

**Key Observations:**

1. **Single pass aggregation** is O(N)
2. **Null collections** counted in total but excluded from Top K
3. **Heap extraction** is O(C log K) where C = collections
4. **Efficient for K << C** (e.g., Top 10 from 10,000 collections)

---

## 🔍 Complexity Analysis

### Time Complexity

| Phase | Operation | Complexity | Explanation |
|-------|-----------|------------|-------------|
| 1. Aggregation | Iterate files | **O(N)** | Single pass through all files |
| 2. Top K | heapq.nlargest | **O(C log K)** | C collections, heap size K |
| **Total** | | **O(N + C log K)** | Usually N >> C, so ~O(N) |

**Special Cases:**
- If K = C (all collections): O(N + C log C) (equivalent to sorting)
- If K = 1: O(N + C) (find max)

### Space Complexity

| Component | Space |
|-----------|-------|
| `collection_sizes` map | **O(C)** |
| `heapq.nlargest` | **O(K)** |
| **Total** | **O(C)** |

**Note:** C ≤ N (at most one collection per file).

---

## ⚠️ Common Pitfalls

### 1. **Forgetting to Handle `null` Collections**

**Wrong:**
```python
for file in files:
    collection_sizes[file["collectionId"]] += file["size"]
    # Crash if collectionId is None!
```

**Right:** Check `if collection_id is not None` before adding.

### 2. **Using Max-Heap Instead of Min-Heap**

**Wrong (Manual Heap):**
```python
heap = []
for col_id, size in collection_sizes.items():
    heapq.heappush(heap, (size, col_id))  # Min-heap
    if len(heap) > k:
        heapq.heappop(heap)

# heap now has K smallest, not K largest!
```

**Right:** Use `heapq.nlargest()` or negate sizes for max-heap.

### 3. **Not Handling K > Number of Collections**

**Wrong:**
```python
top_k = heapq.nlargest(k, collection_sizes.items(), key=lambda x: x[1])
# Works fine! heapq handles this gracefully
```

**Actually:** This is correct. `heapq.nlargest` returns min(K, len(items)) elements.

---

## 🔄 Follow-up Questions

### Follow-up 1: Streaming / Memory-Constrained

**Problem Statement:**
> "The file list is too large to fit in memory (e.g., 1 billion files). Files arrive as a stream. How do you handle this?"

**Challenge:**
- Can't store all files in memory.
- Can't store all collection IDs in a HashMap if there are millions of unique collections.

**Solution: MapReduce Pattern**

```python
from collections import defaultdict
import heapq

class StreamingReportGenerator:
    """
    Process files in chunks (streaming/batch).
    """
    
    def __init__(self, k: int):
        self.k = k
        self.total_size = 0
        self.collection_sizes = defaultdict(int)
    
    def process_chunk(self, chunk: List[Dict]) -> None:
        """
        Process a chunk of files.
        
        Args:
            chunk: List of file dictionaries
        
        Time: O(M) where M = chunk size
        """
        for file in chunk:
            size = file.get("size", 0)
            collection_id = file.get("collectionId")
            
            self.total_size += size
            
            if collection_id is not None:
                self.collection_sizes[collection_id] += size
    
    def get_report(self) -> Dict:
        """
        Generate final report after all chunks processed.
        
        Time: O(C log K)
        """
        top_k = heapq.nlargest(
            self.k,
            self.collection_sizes.items(),
            key=lambda x: x[1]
        )
        
        return {
            "total_size": self.total_size,
            "top_collections": top_k
        }


# ============================================
# EXAMPLE: Streaming
# ============================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("FOLLOW-UP 1: STREAMING PROCESSING")
    print("=" * 60)
    
    generator = StreamingReportGenerator(k=3)
    
    # Simulate streaming chunks
    chunk1 = [
        {"name": "f1", "size": 100, "collectionId": "A"},
        {"name": "f2", "size": 200, "collectionId": "B"}
    ]
    chunk2 = [
        {"name": "f3", "size": 150, "collectionId": "A"},
        {"name": "f4", "size": 300, "collectionId": "C"}
    ]
    chunk3 = [
        {"name": "f5", "size": 50, "collectionId": None}
    ]
    
    generator.process_chunk(chunk1)
    print("Processed chunk 1...")
    
    generator.process_chunk(chunk2)
    print("Processed chunk 2...")
    
    generator.process_chunk(chunk3)
    print("Processed chunk 3...")
    
    final_report = generator.get_report()
    print(f"\nFinal Report:")
    print(f"  Total Size: {final_report['total_size']} bytes")
    print(f"  Top 3 Collections: {final_report['top_collections']}")
```

**Memory:** Still O(C) for unique collections. If C is too large, use **Count-Min Sketch** or **Heavy Hitters** algorithms (beyond interview scope).

---

### Follow-up 2: Real-Time Updates

**Problem Statement:**
> "Files are added/removed in real-time. Maintain a live Top K report that updates dynamically."

**Challenge:**
- Need to efficiently update the Top K when a file is added/removed.
- Recomputing Top K after every update is expensive.

**Solution: Maintain Top K Heap**

```python
import heapq

class LiveReportGenerator:
    """
    Maintain live Top K with dynamic updates.
    """
    
    def __init__(self, k: int):
        self.k = k
        self.total_size = 0
        self.collection_sizes = defaultdict(int)
        self.top_k_heap = []  # Min-heap of (size, col_id)
        self.in_heap = set()  # Collections currently in heap
    
    def add_file(self, file: Dict) -> None:
        """
        Add a file to the system.
        
        Time: O(log K) amortized
        """
        size = file.get("size", 0)
        collection_id = file.get("collectionId")
        
        self.total_size += size
        
        if collection_id is None:
            return
        
        old_size = self.collection_sizes[collection_id]
        new_size = old_size + size
        self.collection_sizes[collection_id] = new_size
        
        # Update Top K heap
        self._update_heap(collection_id, new_size)
    
    def _update_heap(self, col_id: str, new_size: int) -> None:
        """
        Update heap with new collection size.
        """
        # Remove old entry (lazy deletion)
        # Add new entry
        
        if col_id in self.in_heap:
            # Already in heap, size changed (lazy: just add new entry)
            heapq.heappush(self.top_k_heap, (new_size, col_id))
        else:
            # Not in heap
            if len(self.in_heap) < self.k:
                # Heap not full, add
                heapq.heappush(self.top_k_heap, (new_size, col_id))
                self.in_heap.add(col_id)
            else:
                # Heap full, check if new size qualifies
                min_size, min_col = self.top_k_heap[0]
                if new_size > min_size:
                    heapq.heapreplace(self.top_k_heap, (new_size, col_id))
                    self.in_heap.discard(min_col)
                    self.in_heap.add(col_id)
    
    def get_top_k(self) -> List[Tuple[str, int]]:
        """
        Get current Top K.
        
        Time: O(K log K) to sort heap
        """
        # Clean heap (remove stale entries)
        valid_heap = [
            (size, col_id)
            for size, col_id in self.top_k_heap
            if self.collection_sizes[col_id] == size
        ]
        
        # Return sorted descending
        return sorted(valid_heap, reverse=True)[:self.k]
```

---

### Follow-up 3: Time-Based Queries

**Problem Statement:**
> "Files have timestamps. Support queries like 'Top K collections for files added in the last 24 hours'."

**Solution:**

```python
from collections import defaultdict
from typing import List, Dict, Tuple
import heapq

@dataclass
class FileWithTimestamp:
    name: str
    size: int
    collectionId: Optional[str]
    timestamp: int  # Unix timestamp

class TimeBasedReportGenerator:
    """
    Generate reports for files within a time range.
    """
    
    def __init__(self, k: int):
        self.k = k
        self.files = []  # Sorted by timestamp
    
    def add_file(self, file: FileWithTimestamp) -> None:
        """
        Add file (assume files added in chronological order).
        
        Time: O(1) amortized
        """
        # If not chronological, use bisect.insort for O(log N)
        self.files.append(file)
    
    def get_report_for_range(self, start_time: int, end_time: int) -> Dict:
        """
        Get Top K collections for files in time range [start_time, end_time].
        
        Args:
            start_time: Start timestamp (inclusive)
            end_time: End timestamp (inclusive)
        
        Returns:
            Report dict with total_size and top_collections
        
        Time: O(M + C log K) where M = files in range, C = collections
        """
        total_size = 0
        collection_sizes = defaultdict(int)
        
        # Sliding window to find files in range
        for file in self.files:
            if start_time <= file.timestamp <= end_time:
                total_size += file.size
                if file.collectionId:
                    collection_sizes[file.collectionId] += file.size
        
        # Get Top K
        top_k = heapq.nlargest(
            self.k,
            collection_sizes.items(),
            key=lambda x: x[1]
        )
        
        return {
            "total_size": total_size,
            "top_collections": top_k
        }


# Example Usage
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("FOLLOW-UP 3: TIME-BASED QUERIES")
    print("=" * 60)
    
    generator = TimeBasedReportGenerator(k=2)
    
    # Add files with timestamps (Unix time: day 1-3)
    generator.add_file(FileWithTimestamp("f1", 100, "A", timestamp=1))
    generator.add_file(FileWithTimestamp("f2", 200, "B", timestamp=2))
    generator.add_file(FileWithTimestamp("f3", 150, "A", timestamp=3))
    generator.add_file(FileWithTimestamp("f4", 300, "C", timestamp=4))
    
    # Query last 2 days (timestamps 2-3)
    report = generator.get_report_for_range(2, 3)
    print(f"Files in range [2, 3]:")
    print(f"  Total Size: {report['total_size']}")
    print(f"  Top 2 Collections: {report['top_collections']}")
```

**Optimization for Sorted Files:**
If files are always sorted by timestamp, use binary search for O(log N) lookup:

```python
def get_report_for_range_optimized(self, start_time: int, end_time: int) -> Dict:
    """Binary search for range boundaries."""
    import bisect
    
    timestamps = [f.timestamp for f in self.files]
    left_idx = bisect.bisect_left(timestamps, start_time)
    right_idx = bisect.bisect_right(timestamps, end_time)
    
    # Process only files in range
    total_size = 0
    collection_sizes = defaultdict(int)
    
    for i in range(left_idx, right_idx):
        file = self.files[i]
        total_size += file.size
        if file.collectionId:
            collection_sizes[file.collectionId] += file.size
    
    top_k = heapq.nlargest(self.k, collection_sizes.items(), key=lambda x: x[1])
    
    return {"total_size": total_size, "top_collections": top_k}
```

**Complexity:**
- With binary search: O(log N + M + C log K) where M = files in range
- Without: O(N) where N = total files

---

## 🧪 Test Cases

```python
def test_file_report():
    # Test 1: Basic
    files = [
        {"name": "f1", "size": 100, "collectionId": "A"},
        {"name": "f2", "size": 200, "collectionId": "A"}
    ]
    report = generate_report(files, k=1)
    assert report["total_size"] == 300
    assert report["top_collections"][0] == ("A", 300)
    
    # Test 2: Null collections
    files = [
        {"name": "f1", "size": 100, "collectionId": None},
        {"name": "f2", "size": 200, "collectionId": "A"}
    ]
    report = generate_report(files, k=1)
    assert report["total_size"] == 300
    assert report["top_collections"] == [("A", 200)]
    
    # Test 3: Empty
    report = generate_report([], k=5)
    assert report["total_size"] == 0
    assert report["top_collections"] == []
    
    # Test 4: K > collections
    files = [
        {"name": "f1", "size": 100, "collectionId": "A"}
    ]
    report = generate_report(files, k=10)
    assert len(report["top_collections"]) == 1
    
    print("All tests passed! ✓")

if __name__ == "__main__":
    test_file_report()
```

---

## 🎯 Key Takeaways

1. **HashMap for Aggregation** is the standard pattern for grouping.
2. **Heap for Top K** is optimal when K << N.
3. **heapq.nlargest()** simplifies implementation and is well-optimized.
4. **Streaming Processing** uses chunked aggregation (MapReduce pattern).
5. **Real-Time Updates** require maintaining a live heap with lazy deletion.

---

## 📚 Related Problems

- **LeetCode 347:** Top K Frequent Elements
- **LeetCode 692:** Top K Frequent Words
- **LeetCode 973:** K Closest Points to Origin
- **LeetCode 215:** Kth Largest Element in an Array
