# 🤖 PROBLEM 8: ROBOT PARTS ASSEMBLY

### ⭐⭐ **Inventory Management**

**Frequency:** Low
**Similar to:** Group Anagrams / Set checking.

**Problem Statement:**
> You are building robots. Each robot requires a specific set of parts to be built.
> You have an inventory of parts.
>
> Given a list of **required parts** for a robot (e.g., `["wheel", "motor", "sensor"]`) and a list of **available parts** in inventory (e.g., `["motor", "wheel", "sensor", "wheel"]`), determine:
> 1.  Can we build the robot?
> 2.  If yes, remove the used parts from inventory and return success.
> 3.  If no, return list of missing parts.

**Visual Example:**
```text
Required: [A, A, B]
Inventory: [A, B, A, C]

1. Count Required: {A: 2, B: 1}
2. Count Inventory: {A: 2, B: 1, C: 1}
3. Compare:
   Inventory has 2 A's? Yes.
   Inventory has 1 B? Yes.
   
Result: Success! Inventory becomes [C].
```

---

### 🗣️ **Interview Conversation Guide**

**Phase 1: Clarification**
- **Candidate:** "Does the order of parts matter?"
- **Interviewer:** "No, `[A, B]` is same as `[B, A]`."
- **Candidate:** "Are there duplicates in requirements?"
- **Interviewer:** "Yes, a robot might need 4 wheels."
- **Candidate:** "Should I optimize for one-time check or multiple checks?"
- **Interviewer:** "Assume we have one big inventory and multiple robot build requests coming in."

**Phase 2: Approach**
- **Candidate:** "Since frequency matters (e.g., needing 2 wheels), a `Set` is not enough. We need a **Frequency Map (HashMap / Counter)**."
- **Candidate:** "We can store the Inventory as a Hash Map: `{'wheel': 10, 'motor': 5}`."
- **Candidate:** "For each request, we create a count of required parts."
- **Candidate:** "Then iterate through requirements and check if Inventory has enough."
- **Candidate:** "If checks pass, decrement inventory."

**Phase 3: Coding**
- Use `collections.Counter` in Python.
- Handle the "Transactional" nature (don't remove parts if you can't complete the full robot).

---

### 📝 **Solution Approach: Frequency Map**

**Data Structure:** `HashMap<PartName, Count>`

**Algorithm:**
1.  Convert Inventory list to Map (if not already).
2.  Count requirements.
3.  **Check Phase**: Iterate requirements. If `inventory[part] < required[part]`, collect missing.
4.  **Update Phase**: If no missing parts, decrement inventory.

**Implementation:**

```python
from collections import Counter
from typing import List, Dict

class RobotBuilder:
    def __init__(self, inventory_list: List[str]):
        # Initialize inventory
        self.inventory = Counter(inventory_list)

    def build_robot(self, required_parts: List[str]):
        # 1. Count requirements
        req_counts = Counter(required_parts)
        missing = []

        # 2. Check availability
        for part, count in req_counts.items():
            if self.inventory[part] < count:
                needed = count - self.inventory[part]
                # Add missing part 'needed' times or just once with count
                missing.append(f"{part} (x{needed})")

        if missing:
            return False, missing

        # 3. Commit transaction (Remove parts)
        for part, count in req_counts.items():
            self.inventory[part] -= count
            # Optional: clean up 0 counts to save space
            if self.inventory[part] == 0:
                del self.inventory[part]

        return True, []

# Usage
initial_parts = ["wheel", "wheel", "motor", "sensor", "cable"]
builder = RobotBuilder(initial_parts)

# Request 1: Success
success, msg = builder.build_robot(["wheel", "motor"])
print(f"Build 1: {success}") # True
# Inventory now: {wheel: 1, sensor: 1, cable: 1}

# Request 2: Fail
success, msg = builder.build_robot(["wheel", "wheel"]) 
print(f"Build 2: {success}, Missing: {msg}") 
# False, Missing wheel (need 2, have 1)
```

---

### 🔄 **Follow-up 1: Thread Safety**

**Problem:**
> Multiple robot arms are taking parts from the same inventory concurrently.

**Solution:**
> Needs a lock around the `Check + Update` block.
> This block must be **Atomic**. You can't check, release lock, then update. The inventory might change in between.

```python
    def build_robot_thread_safe(self, required_parts):
        with self.lock:
            # ... same logic ...
```

---

### 🧪 **Test Cases**

**Basic:**
- Exact match.
- Partial match (Success).
- Missing one item.
- Missing quantity (Need 2, have 1).

**Edge Cases:**
- Empty requirement (Free to build).
- Empty inventory.
- Part names case sensitivity (assume sensitive).
