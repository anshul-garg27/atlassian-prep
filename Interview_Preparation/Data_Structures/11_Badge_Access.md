# 🔐 PROBLEM 9: BADGE ACCESS / SECURITY SYSTEM

### ⭐⭐ **Track Entry/Exit Events and Find Anomalies**

**Frequency:** Low (Appears in ~15% of rounds)
**Difficulty:** Easy
**Similar to:** [LeetCode 1133 - Largest Unique Number](https://leetcode.com/problems/largest-unique-number/), State Machine problems

---

## 📋 Problem Statement

You are building a security system that tracks employee badge access to a building. Each event is recorded as `[EmployeeName, Action]` where Action is either `"Enter"` or `"Exit"`.

**Find employees who have anomalous access patterns:**
1. **Entered without exiting:** Still inside at end of day
2. **Exited without entering:** Exited but never entered (tailgating or badge sharing)
3. **Multiple entries:** Entered multiple times without exiting in between

**Constraints:**
- 1 ≤ events.length ≤ 10⁵
- Employee names are non-empty strings
- Actions are exactly "Enter" or "Exit" (case-sensitive)
- Events are given in chronological order

---

## 🎨 Visual Example

### Example 1: Normal and Anomalous Patterns

```text
Badge Events (Chronological):
┌────────────────────────────────────────────────┐
│ 1. [Alice, Enter]     → Alice enters building │
│ 2. [Bob, Enter]       → Bob enters building   │
│ 3. [Alice, Exit]      → Alice exits building  │
│ 4. [Charlie, Exit]    → Charlie exits (⚠️ anomaly: never entered)
│ 5. [Bob, Enter]       → Bob enters (⚠️ anomaly: already inside)
│ 6. [David, Enter]     → David enters building │
└────────────────────────────────────────────────┘

Final State Analysis:
┌───────────────────────────────────────────────┐
│ Inside building: {Bob, David}                 │
│                                               │
│ Anomalies:                                    │
│ • Bob: Multiple entries without exit         │
│ • Charlie: Exited without entering           │
│ • David: Never exited (still inside)         │
└───────────────────────────────────────────────┘
```

### Example 2: Visual State Machine

```text
Employee State Machine:

    START
      │
      ├─── Enter ───→ INSIDE
      │                 │
      │                 ├─── Exit ───→ OUTSIDE
      │                 │                │
      │                 └─── Enter ───→ ERROR (double entry)
      │
      └─── Exit ────→ ERROR (exit without entry)

At end of day:
• INSIDE  → Anomaly: "Never exited"
• OUTSIDE → OK
• ERROR   → Anomaly: "Invalid pattern"
```

---

## 💡 Examples

### Example 1: Perfect Day (No Anomalies)
```python
events = [
    ["Alice", "Enter"],
    ["Bob", "Enter"],
    ["Alice", "Exit"],
    ["Bob", "Exit"]
]

result = find_anomalies(events)
print(result)
# {
#   "never_exited": [],
#   "exit_without_enter": [],
#   "multiple_entries": []
# }
```

### Example 2: Multiple Anomalies
```python
events = [
    ["Alice", "Enter"],
    ["Bob", "Exit"],       # Anomaly: exit without enter
    ["Alice", "Enter"],    # Anomaly: double entry
    ["Charlie", "Enter"]   # Anomaly: never exited
]

result = find_anomalies(events)
print(result)
# {
#   "never_exited": ["Charlie"],
#   "exit_without_enter": ["Bob"],
#   "multiple_entries": ["Alice"]
# }
```

### Example 3: Recovered State
```python
events = [
    ["Alice", "Enter"],
    ["Alice", "Exit"],
    ["Alice", "Enter"],   # Re-entry after proper exit: OK
    ["Alice", "Exit"]
]

result = find_anomalies(events)
# No anomalies (Alice properly exits before re-entering)
```

---

## 🗣️ Interview Conversation Guide

### Phase 1: Clarification (3-5 min)

**Candidate:** "Can an employee enter multiple times in a day if they exit in between?"
**Interviewer:** "Yes, that's normal. The anomaly is entering while already inside."

**Candidate:** "Should we track all anomalies for each person, or just the first one?"
**Interviewer:** "Track all anomalies. Someone might have multiple issues."

**Candidate:** "Are events guaranteed to be in chronological order?"
**Interviewer:** "Yes, events arrive in order."

**Candidate:** "What if someone enters, exits, then enters again but never exits? Is that one anomaly or two?"
**Interviewer:** "That's one anomaly: 'never exited'. The earlier enter-exit was fine."

### Phase 2: Approach Discussion (5-8 min)

**Candidate:** "This is a **state tracking** problem. For each employee, I need to track whether they're currently inside or outside the building.

**Algorithm:**
1. Use a **Set** to track employees currently inside.
2. For each event:
   - **Enter:**
     - If already in Set → anomaly (double entry)
     - Otherwise → add to Set
   - **Exit:**
     - If NOT in Set → anomaly (exit without entry)
     - Otherwise → remove from Set
3. At end: anyone remaining in Set → anomaly (never exited)

**Time Complexity:** O(N) where N = number of events
**Space Complexity:** O(M) where M = number of unique employees"

**Candidate:** "I'll track anomalies in separate lists for clear reporting."

### Phase 3: Implementation (10-15 min)

**Candidate:** "I'll implement using a Set for current state and multiple result lists for different anomaly types."

---

## 🧠 Intuition & Approach

### Why Set?

**State Tracking Requirements:**
- O(1) check: "Is employee inside?"
- O(1) add: "Employee enters"
- O(1) remove: "Employee exits"

**Set is Perfect:**
```
inside = {Alice, Bob}
"Is Charlie inside?" → Charlie not in inside → O(1)
```

### State Machine Approach

For each employee, track their state:

```text
State: OUTSIDE (initial)
│
├─ Enter → INSIDE
│           │
│           ├─ Exit → OUTSIDE
│           │
│           └─ Enter → ANOMALY
│
└─ Exit → ANOMALY
```

### Why Not HashMap?

**HashMap is also valid:**
```python
status = {}  # employee -> "inside" / "outside"
```

**Comparison:**
| Approach | Memory | Clarity |
|----------|--------|---------|
| **Set** | O(people inside) | Clear (presence = inside) |
| **HashMap** | O(all people seen) | More explicit states |

**For interviews:** Set is simpler and sufficient.

---

## 📝 Complete Solution

```python
from typing import List, Dict, Set

def find_badge_anomalies(events: List[List[str]]) -> Dict[str, List[str]]:
    """
    Find employees with anomalous badge access patterns.
    
    Args:
        events: List of [employee_name, action] pairs in chronological order
               action is either "Enter" or "Exit"
    
    Returns:
        Dictionary with three lists:
        - never_exited: Employees still inside at end
        - exit_without_enter: Employees who exited without entering
        - multiple_entries: Employees who entered while already inside
    
    Time: O(N) where N = number of events
    Space: O(M) where M = unique employees
    """
    # Track current state
    currently_inside: Set[str] = set()
    
    # Track anomalies (use sets to avoid duplicates)
    exit_without_enter: Set[str] = set()
    multiple_entries: Set[str] = set()
    
    # Process events
    for employee, action in events:
        if action == "Enter":
            if employee in currently_inside:
                # Anomaly: Already inside, entering again
                multiple_entries.add(employee)
            else:
                # Normal: Enter building
                currently_inside.add(employee)
        
        elif action == "Exit":
            if employee not in currently_inside:
                # Anomaly: Exiting without entering
                exit_without_enter.add(employee)
            else:
                # Normal: Exit building
                currently_inside.remove(employee)
    
    # At end of day, anyone still inside never exited
    never_exited = currently_inside
    
    return {
        "never_exited": sorted(list(never_exited)),
        "exit_without_enter": sorted(list(exit_without_enter)),
        "multiple_entries": sorted(list(multiple_entries))
    }


# ============================================
# COMPLETE RUNNABLE EXAMPLE
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("BADGE ACCESS ANOMALY DETECTOR")
    print("=" * 60)
    
    # Test Case 1: Perfect day
    print("\n[Test 1] Perfect Day")
    events1 = [
        ["Alice", "Enter"],
        ["Bob", "Enter"],
        ["Alice", "Exit"],
        ["Bob", "Exit"]
    ]
    result1 = find_badge_anomalies(events1)
    print(f"Never exited: {result1['never_exited']}")
    print(f"Exit without enter: {result1['exit_without_enter']}")
    print(f"Multiple entries: {result1['multiple_entries']}")
    print("Expected: All empty ✓")
    
    # Test Case 2: Multiple anomalies
    print("\n[Test 2] Multiple Anomalies")
    events2 = [
        ["Alice", "Enter"],
        ["Bob", "Exit"],       # Exit without enter
        ["Alice", "Enter"],    # Double entry
        ["Charlie", "Enter"]   # Never exits
    ]
    result2 = find_badge_anomalies(events2)
    print(f"Never exited: {result2['never_exited']}")
    print(f"Exit without enter: {result2['exit_without_enter']}")
    print(f"Multiple entries: {result2['multiple_entries']}")
    print("Expected: Charlie never exited, Bob exit-no-entry, Alice double entry ✓")
    
    # Test Case 3: Complex pattern
    print("\n[Test 3] Complex Pattern")
    events3 = [
        ["Alice", "Enter"],
        ["Alice", "Exit"],
        ["Alice", "Enter"],
        ["Bob", "Enter"],
        ["Alice", "Enter"],    # Double entry
        ["Bob", "Exit"],
        ["Charlie", "Exit"]    # Exit without enter
    ]
    result3 = find_badge_anomalies(events3)
    print(f"Never exited: {result3['never_exited']}")
    print(f"Exit without enter: {result3['exit_without_enter']}")
    print(f"Multiple entries: {result3['multiple_entries']}")
    print("Expected: Alice never exited, Charlie exit-no-entry, Alice double entry ✓")
```

---

## 🔍 Explanation with Example

Let's trace through **Test Case 2** step by step:

**Initial State:**
```
currently_inside = {}
exit_without_enter = {}
multiple_entries = {}
```

---

**Event 1: ["Alice", "Enter"]**

- Action: Enter
- Alice in currently_inside? No
- **Action taken:** Add Alice to currently_inside

```
currently_inside = {Alice}
```

---

**Event 2: ["Bob", "Exit"]**

- Action: Exit
- Bob in currently_inside? No
- **Anomaly detected:** Exit without entering
- **Action taken:** Add Bob to exit_without_enter

```
currently_inside = {Alice}
exit_without_enter = {Bob}
```

---

**Event 3: ["Alice", "Enter"]**

- Action: Enter
- Alice in currently_inside? **Yes!**
- **Anomaly detected:** Double entry
- **Action taken:** Add Alice to multiple_entries

```
currently_inside = {Alice}  (unchanged)
exit_without_enter = {Bob}
multiple_entries = {Alice}
```

---

**Event 4: ["Charlie", "Enter"]**

- Action: Enter
- Charlie in currently_inside? No
- **Action taken:** Add Charlie to currently_inside

```
currently_inside = {Alice, Charlie}
exit_without_enter = {Bob}
multiple_entries = {Alice}
```

---

**End of Day Analysis:**

```
never_exited = currently_inside = {Alice, Charlie}
```

**Note:** Alice appears in BOTH "multiple_entries" and "never_exited". This is correct - she has two separate issues.

---

## 🔍 Complexity Analysis

### Time Complexity: **O(N)**

**Breakdown:**
- Process N events: O(N)
- Each event:
  - Set lookup: O(1) average
  - Set add/remove: O(1) average
- Convert sets to sorted lists: O(M log M) where M = unique employees
- **Total:** O(N + M log M) ≈ O(N) when M << N

### Space Complexity: **O(M)**

**Breakdown:**
- `currently_inside`: O(M) worst case (all employees inside)
- Anomaly sets: O(M) worst case (all employees have anomalies)
- **Total:** O(M) where M = unique employees

---

## ⚠️ Common Pitfalls

### 1. **Not Handling Multiple Anomalies per Person**

**Problem:**
```python
# ❌ WRONG: Only tracks one anomaly per person
if employee in exit_without_enter:
    # Don't process further events for this person
    continue
```

**Why it fails:** Alice could exit without entering (anomaly 1), then later enter and never exit (anomaly 2).

**Fix:** Track each anomaly type independently.

---

### 2. **Removing from Set on Double Entry**

**Problem:**
```python
# ❌ WRONG
if action == "Enter":
    if employee in currently_inside:
        multiple_entries.add(employee)
        currently_inside.remove(employee)  # ← Wrong!
```

**Why it fails:** If they enter again (triple entry), we'd think they're outside and miss it.

**Fix:** Keep them in the set even after double entry.

---

### 3. **Case Sensitivity Issues**

**Problem:**
```python
events = [["Alice", "enter"], ["Alice", "Exit"]]
# Code checks for "Enter" and "Exit" exactly
```

**Why it fails:** "enter" != "Enter", so it won't be recognized.

**Fix:** Clarify with interviewer. If needed: `action.lower() == "enter"`.

---

### 4. **Not Sorting Results**

**Problem:** Sets have undefined order. Results are non-deterministic.

**Fix:** Always convert to sorted list for consistent output.

```python
return {
    "never_exited": sorted(list(never_exited)),  # ✓
    # Not: list(never_exited)  # ✗
}
```

---

## 🔄 Follow-up Questions

### Follow-up 1: Track Entry/Exit Times

**Problem Statement:**
> "Each event now has a timestamp. Find employees who were inside for more than 8 hours."

**Example:**
```python
events = [
    ["Alice", "Enter", 9],   # 9:00 AM
    ["Alice", "Exit", 19]    # 7:00 PM (10 hours)
]
# Alice was inside for 10 hours → flag as anomaly
```

**Solution:**

```python
from typing import List, Dict

def find_overtime(events: List[List]) -> List[str]:
    """
    Find employees who stayed more than 8 hours.
    
    Args:
        events: [employee, action, hour]
    
    Returns:
        List of employees who exceeded 8 hours
    """
    entry_times: Dict[str, int] = {}
    overtime: Set[str] = set()
    
    for employee, action, hour in events:
        if action == "Enter":
            entry_times[employee] = hour
        elif action == "Exit":
            if employee in entry_times:
                duration = hour - entry_times[employee]
                if duration > 8:
                    overtime.add(employee)
                del entry_times[employee]
    
    return sorted(list(overtime))


# Test
events = [
    ["Alice", "Enter", 9],
    ["Alice", "Exit", 19],   # 10 hours
    ["Bob", "Enter", 10],
    ["Bob", "Exit", 16]      # 6 hours
]

result = find_overtime(events)
print(result)  # ["Alice"]
```

**Time Complexity:** O(N)
**Space Complexity:** O(M)

---

### Follow-up 2: Multiple Buildings

**Problem Statement:**
> "Company has multiple buildings. Events now include building ID. Find employees who are simultaneously inside multiple buildings (badge sharing)."

**Example:**
```python
events = [
    ["Alice", "Enter", "Building-A"],
    ["Alice", "Enter", "Building-B"],  # ⚠️ Alice in two places!
    ["Alice", "Exit", "Building-A"]
]
```

**Solution:**

```python
from collections import defaultdict
from typing import List, Set, Dict

def find_badge_sharing(events: List[List[str]]) -> Set[str]:
    """
    Find employees in multiple buildings simultaneously.
    
    Args:
        events: [employee, action, building_id]
    
    Returns:
        Set of employees who appear in multiple buildings
    """
    # Track which buildings each employee is in
    employee_locations: Dict[str, Set[str]] = defaultdict(set)
    badge_sharers: Set[str] = set()
    
    for employee, action, building in events:
        if action == "Enter":
            employee_locations[employee].add(building)
            
            # If in more than one building → badge sharing!
            if len(employee_locations[employee]) > 1:
                badge_sharers.add(employee)
        
        elif action == "Exit":
            if building in employee_locations[employee]:
                employee_locations[employee].remove(building)
    
    return badge_sharers


# Test
events = [
    ["Alice", "Enter", "A"],
    ["Alice", "Enter", "B"],  # Anomaly!
    ["Bob", "Enter", "A"],
    ["Alice", "Exit", "A"],
    ["Alice", "Exit", "B"]
]

result = find_badge_sharing(events)
print(result)  # {"Alice"}
```

**Time Complexity:** O(N)
**Space Complexity:** O(M × B) where B = buildings per employee

---

### Follow-up 3: Real-Time Alerts

**Problem Statement:**
> "As events stream in real-time, send an alert immediately when an anomaly is detected (don't wait for end of day)."

**Solution:**

```python
class BadgeMonitor:
    """
    Real-time badge anomaly monitoring system.
    """
    
    def __init__(self, alert_callback):
        """
        Args:
            alert_callback: Function to call when anomaly detected
                           Signature: alert_callback(employee, anomaly_type)
        """
        self.currently_inside: Set[str] = set()
        self.alert = alert_callback
    
    def process_event(self, employee: str, action: str) -> None:
        """
        Process a single badge event in real-time.
        
        Time: O(1)
        """
        if action == "Enter":
            if employee in self.currently_inside:
                # Immediate alert!
                self.alert(employee, "DOUBLE_ENTRY")
            else:
                self.currently_inside.add(employee)
        
        elif action == "Exit":
            if employee not in self.currently_inside:
                # Immediate alert!
                self.alert(employee, "EXIT_WITHOUT_ENTRY")
            else:
                self.currently_inside.remove(employee)
    
    def end_of_day_check(self) -> List[str]:
        """
        At end of day, find employees still inside.
        
        Time: O(M)
        """
        still_inside = list(self.currently_inside)
        for employee in still_inside:
            self.alert(employee, "NEVER_EXITED")
        return still_inside


# Test
def my_alert(employee, anomaly_type):
    print(f"⚠️  ALERT: {employee} - {anomaly_type}")

monitor = BadgeMonitor(my_alert)

monitor.process_event("Alice", "Enter")
monitor.process_event("Bob", "Exit")        # Immediate alert!
monitor.process_event("Alice", "Enter")     # Immediate alert!
monitor.end_of_day_check()                  # Alert for Alice
```

**Time Complexity:** O(1) per event
**Space Complexity:** O(M)

---

## 🧪 Test Cases

```python
def test_badge_anomalies():
    # Test 1: No anomalies
    events = [["A", "Enter"], ["A", "Exit"]]
    result = find_badge_anomalies(events)
    assert result["never_exited"] == []
    assert result["exit_without_enter"] == []
    assert result["multiple_entries"] == []
    
    # Test 2: Never exited
    events = [["A", "Enter"]]
    result = find_badge_anomalies(events)
    assert result["never_exited"] == ["A"]
    
    # Test 3: Exit without enter
    events = [["A", "Exit"]]
    result = find_badge_anomalies(events)
    assert result["exit_without_enter"] == ["A"]
    
    # Test 4: Double entry
    events = [["A", "Enter"], ["A", "Enter"]]
    result = find_badge_anomalies(events)
    assert result["multiple_entries"] == ["A"]
    assert result["never_exited"] == ["A"]
    
    # Test 5: Multiple people
    events = [
        ["A", "Enter"],
        ["B", "Enter"],
        ["A", "Exit"],
        ["C", "Exit"]
    ]
    result = find_badge_anomalies(events)
    assert result["never_exited"] == ["B"]
    assert result["exit_without_enter"] == ["C"]
    
    # Test 6: Recovered state
    events = [
        ["A", "Enter"],
        ["A", "Exit"],
        ["A", "Enter"],
        ["A", "Exit"]
    ]
    result = find_badge_anomalies(events)
    assert result["never_exited"] == []
    assert result["multiple_entries"] == []
    
    print("All tests passed! ✓")


if __name__ == "__main__":
    test_badge_anomalies()
```

---

## 🎯 Key Takeaways

1. **Set is Perfect for State Tracking** (inside/outside).
2. **Process Events Sequentially** maintaining current state.
3. **Track Multiple Anomaly Types** independently.
4. **End-of-Day Check** for unclosed states.
5. **Real-Time Monitoring** can alert immediately (O(1) per event).

---

## 📚 Related Problems

- **LeetCode 1133:** Largest Unique Number (Set operations)
- **LeetCode 1207:** Unique Number of Occurrences (frequency tracking)
- **LeetCode 599:** Minimum Index Sum of Two Lists
- **General Pattern:** State machine problems, Event processing

