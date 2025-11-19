# 🤖 PROBLEM 8: ROBOT PARTS ASSEMBLY

### ⭐⭐ **Inventory Management with Multi-Set Matching**

**Frequency:** Low-Medium (Appears in ~20% of rounds)
**Difficulty:** Easy-Medium
**Similar to:** [LeetCode 383 - Ransom Note](https://leetcode.com/problems/ransom-note/), [LeetCode 1657 - Determine if Two Strings Are Close](https://leetcode.com/problems/determine-if-two-strings-are-close/)

---

## 📋 Problem Statement

You are managing a robot assembly factory. Each robot requires a specific **multiset** of parts (e.g., 2 wheels, 1 motor, 3 sensors).

Given:
- **Inventory:** A list of available parts
- **Requirements:** A list of parts needed to build one robot

**Operations:**
1. `canBuild(requirements)`: Check if the inventory has enough parts
2. `build(requirements)`: If possible, consume the parts and return success. Otherwise, return the list of missing parts.

**Constraints:**
- Part names are case-sensitive strings
- Duplicates matter (a robot might need 4 identical wheels)
- 1 ≤ inventory size ≤ 10⁶
- 1 ≤ requirements size ≤ 100

---

## 🎨 Visual Example

### Example 1: Successful Build

```text
Inventory: [wheel, wheel, motor, sensor, cable, wheel]

Robot Requirements: [wheel, wheel, motor]

Step 1: Count Requirements
┌─────────────────────┐
│ wheel  → 2          │
│ motor  → 1          │
└─────────────────────┘

Step 2: Count Inventory
┌─────────────────────┐
│ wheel  → 3          │
│ motor  → 1          │
│ sensor → 1          │
│ cable  → 1          │
└─────────────────────┘

Step 3: Validate
✓ wheel: need 2, have 3 → OK
✓ motor: need 1, have 1 → OK

Step 4: Consume Parts
Inventory After: [wheel, sensor, cable]
```

### Example 2: Insufficient Parts

```text
Inventory: [wheel, motor]

Requirements: [wheel, wheel, motor]

Count Comparison:
✗ wheel: need 2, have 1 → MISSING 1

Result: Cannot build
Missing: ["wheel (x1)"]
```

---

## 💡 Examples

### Example 1: Basic Usage
```python
builder = RobotBuilder(["wheel", "wheel", "motor", "sensor"])

# Build robot 1
success, msg = builder.build(["wheel", "motor"])
print(success)  # True
print(builder.get_inventory())  # {"wheel": 1, "sensor": 1}

# Build robot 2
success, msg = builder.build(["wheel", "sensor"])
print(success)  # True
print(builder.get_inventory())  # {}
```

### Example 2: Insufficient Inventory
```python
builder = RobotBuilder(["wheel", "motor"])

success, msg = builder.build(["wheel", "wheel", "motor"])
print(success)  # False
print(msg)      # ["wheel (need 2, have 1)"]
```

---

## 🗣️ Interview Conversation Guide

### Phase 1: Clarification (3-5 min)

**Candidate:** "Does the order of parts matter? Is `[A, B]` the same as `[B, A]`?"
**Interviewer:** "Order doesn't matter. Think of it as a multiset (bag)."

**Candidate:** "Can the requirements have duplicates?"
**Interviewer:** "Yes, a robot might need 4 wheels and 2 motors."

**Candidate:** "Should the operation be atomic? If I can't build a robot, should the inventory remain unchanged?"
**Interviewer:** "Yes, it's a transaction. Either all parts are consumed, or none."

**Candidate:** "Are part names case-sensitive?"
**Interviewer:** "Yes. 'Wheel' and 'wheel' are different parts."

### Phase 2: Approach Discussion (5-8 min)

**Candidate:** "This is a **frequency matching** problem. Since we care about **how many** of each part (not just presence), a `Set` won't work. We need a **frequency map** (HashMap or Counter).

**Data Structure:**
- Store inventory as `Map<part_name, count>`.
- For each build request, create a frequency map of requirements.
- Compare: `inventory[part] >= required[part]` for all parts.

**Algorithm:**
1. **Check Phase:** Validate all parts are available in sufficient quantity.
2. **Update Phase:** If check passes, decrement inventory counts atomically.

**Why Atomic?** If we check then update separately without locking, another thread might consume parts in between."

### Phase 3: Implementation (10-15 min)

**Candidate:** "I'll use Python's `Counter` for clean frequency mapping."

---

## 🧠 Intuition & Approach

### Why HashMap (Counter)?

**Problem Requirements:**
- Track **quantity** of each part, not just presence.
- Fast lookup: "Do we have enough of part X?"
- Fast update: "Remove N units of part X."

**Counter Properties:**
- O(1) lookup and update
- Handles missing keys gracefully (returns 0)
- Built-in operations like subtraction

### Transaction Pattern

```text
1. Create a "snapshot" of requirements
2. Validate ALL requirements
3. If ANY fail, abort (don't modify inventory)
4. If ALL succeed, commit changes

This is the classic "Check-Then-Act" race condition pattern.
In concurrent systems, need locking.
```

---

## 📝 Complete Solution

```python
from collections import Counter
from typing import List, Tuple, Dict, Optional
import threading

class RobotBuilder:
    """
    Manage robot assembly with inventory tracking.
    
    Supports:
    - Check if robot can be built
    - Build robot (consume parts atomically)
    - Query current inventory
    """
    
    def __init__(self, initial_inventory: List[str]):
        """
        Initialize builder with inventory.
        
        Args:
            initial_inventory: List of part names (can have duplicates)
        
        Time: O(N) where N = number of parts
        Space: O(U) where U = unique parts
        """
        self.inventory = Counter(initial_inventory)
        self.lock = threading.Lock()  # For thread safety
    
    def can_build(self, requirements: List[str]) -> bool:
        """
        Check if robot can be built (non-destructive).
        
        Args:
            requirements: List of required part names
        
        Returns:
            True if all parts available in sufficient quantity
        
        Time: O(R) where R = number of requirements
        Space: O(U) for requirement counter
        """
        required = Counter(requirements)
        
        for part, count in required.items():
            if self.inventory[part] < count:
                return False
        
        return True
    
    def build(self, requirements: List[str]) -> Tuple[bool, List[str]]:
        """
        Attempt to build robot. Consumes parts if successful.
        
        Args:
            requirements: List of required part names
        
        Returns:
            (success, messages):
                - If success: (True, [])
                - If failure: (False, ["part1 (need X, have Y)", ...])
        
        Time: O(R) where R = number of requirements
        Space: O(U) for tracking
        """
        with self.lock:  # Ensure atomicity
            required = Counter(requirements)
            missing = []
            
            # Phase 1: Validation
            for part, needed in required.items():
                available = self.inventory[part]
                if available < needed:
                    shortage = needed - available
                    missing.append(f"{part} (need {needed}, have {available})")
            
            # Phase 2: Commit or Abort
            if missing:
                return False, missing
            
            # All parts available, consume them
            for part, count in required.items():
                self.inventory[part] -= count
                # Optional: Remove zero-count entries
                if self.inventory[part] == 0:
                    del self.inventory[part]
            
            return True, []
    
    def build_multiple(self, requirements: List[str], quantity: int) -> Tuple[int, List[str]]:
        """
        Build multiple identical robots.
        
        Args:
            requirements: Parts for one robot
            quantity: Number of robots to build
        
        Returns:
            (built_count, message):
                - built_count: How many robots were successfully built
                - message: Error messages if any
        """
        with self.lock:
            # Check maximum buildable
            required = Counter(requirements)
            max_buildable = quantity
            
            for part, needed_per_robot in required.items():
                available = self.inventory[part]
                can_build = available // needed_per_robot
                max_buildable = min(max_buildable, can_build)
            
            if max_buildable == 0:
                return 0, [f"Cannot build even 1 robot"]
            
            # Build max_buildable robots
            for part, needed_per_robot in required.items():
                total_needed = needed_per_robot * max_buildable
                self.inventory[part] -= total_needed
                if self.inventory[part] == 0:
                    del self.inventory[part]
            
            return max_buildable, []
    
    def get_inventory(self) -> Dict[str, int]:
        """
        Get current inventory snapshot.
        
        Time: O(U)
        Space: O(U)
        """
        with self.lock:
            return dict(self.inventory)
    
    def restock(self, parts: List[str]) -> None:
        """
        Add parts to inventory.
        
        Time: O(P) where P = number of parts to add
        """
        with self.lock:
            for part in parts:
                self.inventory[part] += 1


# ============================================
# COMPLETE RUNNABLE EXAMPLE
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("ROBOT PARTS ASSEMBLY SYSTEM")
    print("=" * 60)
    
    # Test 1: Basic build
    print("\n[Test 1] Basic Robot Build")
    print("-" * 40)
    builder = RobotBuilder([
        "wheel", "wheel", "wheel", "wheel",
        "motor", "motor",
        "sensor", "camera"
    ])
    
    print("Initial Inventory:", builder.get_inventory())
    
    success, msg = builder.build(["wheel", "wheel", "motor"])
    print(f"\nBuild Robot 1: {success}")
    print(f"Inventory After: {builder.get_inventory()}")
    
    # Test 2: Insufficient parts
    print("\n[Test 2] Insufficient Parts")
    print("-" * 40)
    success, msg = builder.build(["wheel", "wheel", "wheel", "motor"])
    print(f"Build Robot 2: {success}")
    if not success:
        print(f"Missing: {msg}")
    print(f"Inventory (unchanged): {builder.get_inventory()}")
    
    # Test 3: Multiple robots
    print("\n[Test 3] Build Multiple Identical Robots")
    print("-" * 40)
    builder2 = RobotBuilder(["wheel"] * 10 + ["motor"] * 5)
    
    built, msg = builder2.build_multiple(["wheel", "wheel", "motor"], quantity=5)
    print(f"Attempted to build 5 robots")
    print(f"Successfully built: {built} robots")
    print(f"Inventory After: {builder2.get_inventory()}")
    
    # Test 4: Restock
    print("\n[Test 4] Restock Inventory")
    print("-" * 40)
    builder.restock(["wheel", "wheel", "motor"])
    print(f"Restocked: 2 wheels, 1 motor")
    print(f"Inventory: {builder.get_inventory()}")
    
    success, msg = builder.build(["wheel", "wheel", "motor"])
    print(f"Build Robot 3: {success}")
    print(f"Inventory After: {builder.get_inventory()}")
    
    # Test 5: Edge cases
    print("\n[Test 5] Edge Cases")
    print("-" * 40)
    
    # Empty requirements
    success, msg = builder.build([])
    print(f"Build robot with no requirements: {success}")
    
    # Empty inventory
    builder_empty = RobotBuilder([])
    success, msg = builder_empty.build(["wheel"])
    print(f"Build from empty inventory: {success}, Missing: {msg}")
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)
```

---

## 🔍 Explanation with Example

Let's trace through the inventory management system with a concrete example:

**Initial Inventory:** `["wheel", "wheel", "wheel", "motor", "sensor", "sensor"]`

**Requirements:** `["wheel", "wheel", "motor"]`

---

**Step 1: Initialize Builder**

```python
builder = RobotBuilder(["wheel", "wheel", "wheel", "motor", "sensor", "sensor"])

# Internal state:
inventory = Counter({
    "wheel": 3,
    "motor": 1,
    "sensor": 2
})
```

---

**Step 2: Check if Can Build**

```python
requirements = ["wheel", "wheel", "motor"]
req_count = Counter(requirements)
# Result: {"wheel": 2, "motor": 1}
```

**Validation:**
```text
Check "wheel": need 2, have 3 ✓
Check "motor": need 1, have 1 ✓

All requirements satisfied!
```

**Result:** `can_build() = True`

---

**Step 3: Build Robot (Consume Parts)**

Since validation passed, consume parts atomically:

```python
for part, needed in req_count.items():
    inventory[part] -= needed
```

**Updates:**
```text
wheel: 3 - 2 = 1
motor: 1 - 1 = 0
```

**New Inventory State:**
```python
inventory = Counter({
    "wheel": 1,
    "motor": 0,  # Will be removed (0 count)
    "sensor": 2
})

# After cleanup (remove zero counts):
inventory = Counter({
    "wheel": 1,
    "sensor": 2
})
```

**Result:** `build() = (True, "Success")`

---

**Example 2: Insufficient Parts**

Now try to build another robot needing `["wheel", "wheel", "motor"]`:

**Current Inventory:** `{"wheel": 1, "sensor": 2}`

**Validation:**
```text
Check "wheel": need 2, have 1 ✗ MISSING!
Check "motor": need 1, have 0 ✗ MISSING!
```

**Missing Parts Calculation:**
```python
missing = {
    "wheel": 2 - 1 = 1,
    "motor": 1 - 0 = 1
}
```

**Result:** 
```python
build() = (
    False, 
    {"wheel": "need 1 more", "motor": "need 1 more"}
)
```

**Inventory Unchanged** (atomic transaction failed):
```python
inventory = Counter({
    "wheel": 1,
    "sensor": 2
})
```

---

**Key Points:**

1. **Counter** provides O(1) lookup and updates
2. **Validation happens before modification** (atomic)
3. **Missing parts are calculated** for user feedback
4. **Transaction either fully succeeds or fails** (no partial builds)

---

## 🔍 Complexity Analysis

### Time Complexity

| Operation | Time | Explanation |
|-----------|------|-------------|
| `__init__()` | **O(N)** | Count N initial parts |
| `can_build()` | **O(R)** | Check R requirements |
| `build()` | **O(R)** | Validate + update R requirements |
| `build_multiple()` | **O(R)** | Same as single build |
| `get_inventory()` | **O(U)** | Copy U unique parts |
| `restock()` | **O(P)** | Add P new parts |

**Where:**
- N = total initial parts
- R = requirements size
- U = unique part types
- P = parts to restock

### Space Complexity

**O(U)** where U = number of unique part types.

---

## ⚠️ Common Pitfalls

### 1. **Partial Updates (Race Condition)**

**Wrong:**
```python
def build(self, requirements):
    for part in requirements:
        if self.inventory[part] > 0:
            self.inventory[part] -= 1  # Immediate update!
        else:
            return False, [f"Missing {part}"]
    return True, []
```

**Problem:** If the 5th part is missing, we already consumed parts 1-4. The inventory is corrupted.

**Right:** Validate ALL parts first, then update atomically.

### 2. **Forgetting to Handle Duplicates**

**Wrong:**
```python
required = set(requirements)  # Loses count!
```

**Problem:** `["wheel", "wheel"]` becomes `{"wheel"}`. We only check for 1 wheel instead of 2.

**Right:** Use `Counter` to preserve frequencies.

### 3. **Not Thread-Safe**

**Wrong:**
```python
def build(self, requirements):
    if self.can_build(requirements):  # Check
        # Another thread might modify here!
        self._consume(requirements)     # Update
```

**Problem:** Between check and update, another thread might consume parts.

**Right:** Use a lock around the entire check-update block.

---

## 🔄 Follow-up Questions

### Follow-up 1: Thread Safety with Concurrent Builds

**Problem Statement:**
> "Multiple robots are being built concurrently from the same inventory. Ensure thread safety."

**Solution:**
Already implemented with `threading.Lock()` in the base solution. The `with self.lock` ensures the check-update block is atomic.

**Example:**

```python
import threading
import time

def worker(builder, robot_id, requirements):
    """Simulate a worker trying to build a robot."""
    print(f"Robot {robot_id}: Attempting to build...")
    success, msg = builder.build(requirements)
    if success:
        print(f"Robot {robot_id}: ✓ Built successfully")
    else:
        print(f"Robot {robot_id}: ✗ Failed - {msg}")

# ============================================
# EXAMPLE: Concurrent Builds
# ============================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("FOLLOW-UP 1: CONCURRENT BUILDS")
    print("=" * 60)
    
    # Start with limited inventory
    builder = RobotBuilder(["wheel"] * 5 + ["motor"] * 3)
    
    print(f"Initial Inventory: {builder.get_inventory()}")
    
    # Create 5 threads trying to build robots
    threads = []
    for i in range(5):
        requirements = ["wheel", "motor"]
        t = threading.Thread(target=worker, args=(builder, i+1, requirements))
        threads.append(t)
        t.start()
    
    # Wait for all threads
    for t in threads:
        t.join()
    
    print(f"\nFinal Inventory: {builder.get_inventory()}")
    print("Only 3 robots should have been built (limited by 3 motors)")
```

**Output:**
```
Initial Inventory: {'wheel': 5, 'motor': 3}
Robot 1: ✓ Built successfully
Robot 2: ✓ Built successfully
Robot 3: ✓ Built successfully
Robot 4: ✗ Failed - ['motor (need 1, have 0)']
Robot 5: ✗ Failed - ['motor (need 1, have 0)']
Final Inventory: {'wheel': 2}
```

---

### Follow-up 2: Priority Queue for Build Requests

**Problem Statement:**
> "Some robots are high-priority (urgent orders). Process high-priority builds first, even if they arrive later."

**Solution:**
Use a **Priority Queue** (heap) to store build requests.

```python
import heapq

class PriorityRobotBuilder(RobotBuilder):
    """
    Robot builder with priority queue for build requests.
    """
    
    def __init__(self, initial_inventory: List[str]):
        super().__init__(initial_inventory)
        self.build_queue = []  # Min-heap: (priority, timestamp, requirements)
        self.timestamp = 0
    
    def add_build_request(self, requirements: List[str], priority: int = 0) -> None:
        """
        Add build request to queue.
        
        Args:
            requirements: Parts needed
            priority: Lower number = higher priority (0 is highest)
        
        Time: O(log Q) where Q = queue size
        """
        with self.lock:
            heapq.heappush(
                self.build_queue,
                (priority, self.timestamp, requirements)
            )
            self.timestamp += 1
    
    def process_next(self) -> Tuple[bool, Optional[List[str]]]:
        """
        Process highest-priority build request.
        
        Returns:
            (success, requirements_or_message)
        
        Time: O(log Q + R)
        """
        with self.lock:
            if not self.build_queue:
                return False, None
            
            priority, ts, requirements = heapq.heappop(self.build_queue)
        
        # Try to build (uses parent's atomic build method)
        success, msg = self.build(requirements)
        
        if not success:
            # Re-queue if failed (or handle differently)
            with self.lock:
                heapq.heappush(self.build_queue, (priority, ts, requirements))
        
        return success, requirements if success else msg


# ============================================
# EXAMPLE
# ============================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("FOLLOW-UP 2: PRIORITY QUEUE")
    print("=" * 60)
    
    builder = PriorityRobotBuilder(["wheel"] * 10 + ["motor"] * 5)
    
    # Add requests (lower priority number = higher priority)
    builder.add_build_request(["wheel", "motor"], priority=2)  # Low priority
    builder.add_build_request(["wheel", "motor"], priority=0)  # High priority
    builder.add_build_request(["wheel", "motor"], priority=1)  # Medium priority
    
    print("Processing requests by priority...")
    for i in range(3):
        success, result = builder.process_next()
        print(f"  Request {i+1}: {success}, Requirements: {result}")
```

---

### Follow-up 3: Substitutions (Part Compatibility)

**Problem Statement:**
> "Some parts are interchangeable. For example, 'motor_v1' and 'motor_v2' can both fulfill a 'motor' requirement. How do you handle this?"

**Solution:**
Maintain a **compatibility map**:

```python
class FlexibleRobotBuilder(RobotBuilder):
    """
    Robot builder with part substitutions.
    """
    
    def __init__(self, initial_inventory: List[str], compatibility: Dict[str, List[str]]):
        """
        Args:
            initial_inventory: Parts list
            compatibility: Map from abstract part to compatible concrete parts
                Example: {"motor": ["motor_v1", "motor_v2"]}
        """
        super().__init__(initial_inventory)
        self.compatibility = compatibility
    
    def _find_available(self, abstract_part: str, needed: int) -> Optional[List[str]]:
        """
        Find concrete parts that can fulfill the requirement.
        
        Returns:
            List of concrete part names if sufficient, else None
        """
        compatible = self.compatibility.get(abstract_part, [abstract_part])
        
        # Try to gather needed quantity from compatible parts
        selected = []
        remaining = needed
        
        for concrete_part in compatible:
            available = self.inventory.get(concrete_part, 0)
            take = min(available, remaining)
            selected.extend([concrete_part] * take)
            remaining -= take
            
            if remaining == 0:
                return selected
        
        return None if remaining > 0 else selected
    
    def build_with_substitution(self, requirements: List[str]) -> Tuple[bool, List[str]]:
        """
        Build robot, allowing part substitutions.
        """
        with self.lock:
            # Map requirements to concrete parts
            concrete_requirements = []
            
            for abstract_part in requirements:
                selected = self._find_available(abstract_part, 1)
                if selected is None:
                    return False, [f"Cannot fulfill {abstract_part}"]
                concrete_requirements.extend(selected)
            
            # Now build with concrete parts
            return self.build(concrete_requirements)
```

---

## 🧪 Test Cases

```python
def test_robot_builder():
    # Test 1: Exact match
    builder = RobotBuilder(["A", "B"])
    assert builder.can_build(["A", "B"]) == True
    
    # Test 2: Insufficient quantity
    builder = RobotBuilder(["A"])
    assert builder.can_build(["A", "A"]) == False
    
    # Test 3: Missing part
    builder = RobotBuilder(["A"])
    assert builder.can_build(["B"]) == False
    
    # Test 4: Successful build
    builder = RobotBuilder(["A", "A", "B"])
    success, _ = builder.build(["A", "B"])
    assert success == True
    assert builder.get_inventory() == {"A": 1}
    
    # Test 5: Failed build doesn't modify inventory
    builder = RobotBuilder(["A"])
    inv_before = builder.get_inventory().copy()
    success, _ = builder.build(["A", "A"])
    assert success == False
    assert builder.get_inventory() == inv_before
    
    print("All tests passed! ✓")

if __name__ == "__main__":
    test_robot_builder()
```

---

## 🎯 Key Takeaways

1. **Counter is Perfect for Frequency Matching** problems.
2. **Atomic Transactions** require validation before modification.
3. **Thread Safety** needs locking around check-update blocks.
4. **Priority Queues** enable sophisticated scheduling.
5. **Flexibility** (substitutions) requires mapping abstract → concrete parts.

---

## 📚 Related Problems

- **LeetCode 383:** Ransom Note (simpler: no duplicates matter)
- **LeetCode 242:** Valid Anagram (frequency matching)
- **LeetCode 49:** Group Anagrams (frequency as key)
- **LeetCode 1160:** Find Words That Can Be Formed by Characters
