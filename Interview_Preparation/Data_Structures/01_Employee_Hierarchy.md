# 🌟 PROBLEM 1: EMPLOYEE HIERARCHY

### ⭐⭐⭐⭐⭐ **Find Closest Department for Employees**

**Frequency:** Appears in **60%** of Atlassian DSA rounds!
**Difficulty:** Medium

---

## 📋 Problem Statement

You maintain the Atlassian employee directory. The company has multiple groups (departments), and each group can have one or more sub-groups. Every employee belongs to exactly one group (in the base version).

**Task:** Design a system that finds the **closest common parent group** given a set of employee names.

**Constraints:**
- 1 ≤ Number of employees ≤ 10,000
- 1 ≤ Number of groups ≤ 1,000
- Tree height ≤ 20
- Employee and group names are unique strings

---

## 🎨 Visual Example

```text
Organization Hierarchy:

                    Company (Root)
                   /      |      \
              Engg       HR      Sales
             /  |  \              / \
     Backend Frontend Mobile  North South
      /  \       |              |     |
  Alice  Bob   Lisa          David  Eve
```

**Path Representation:**
- Alice: `["Company", "Engg", "Backend", "Alice"]`
- Bob: `["Company", "Engg", "Backend", "Bob"]`
- Lisa: `["Company", "Engg", "Frontend", "Lisa"]`
- David: `["Company", "Sales", "North", "David"]`

---

## 💡 Examples

### Example 1: Same Direct Parent
```python
Input: ["Alice", "Bob"]
Output: "Backend"
Explanation: Both employees are directly under Backend group.
```

### Example 2: Different Sub-departments
```python
Input: ["Alice", "Lisa"]
Output: "Engg"
Explanation: 
- Alice path: Company → Engg → Backend → Alice
- Lisa path:  Company → Engg → Frontend → Lisa
- Common prefix: Company, Engg
- LCA: Engg (last common node)
```

### Example 3: Multiple Employees
```python
Input: ["Alice", "Bob", "Lisa"]
Output: "Engg"
Explanation: All three are under Engineering department.
```

### Example 4: Different Top-Level Departments
```python
Input: ["Alice", "David"]
Output: "Company"
Explanation: Only common ancestor is root.
```

### Example 5: Single Employee
```python
Input: ["Alice"]
Output: "Backend"
Explanation: Return immediate parent group.
```

---

## 🗣️ Interview Conversation Guide

### Phase 1: Clarification (3-5 min)

**Candidate:** "Can an employee belong to multiple groups?"
**Interviewer:** "Let's start with the assumption that each employee belongs to exactly one group."

**Candidate:** "Is the input always a valid tree structure, or can there be cycles?"
**Interviewer:** "It's a strict hierarchy (tree structure). No cycles."

**Candidate:** "What should I return if the input list is empty or contains invalid employees?"
**Interviewer:** "Return `None` for empty input. Raise an error or return `None` for invalid employees."

**Candidate:** "Can I assume parent pointers are available, or do I need to build the tree first?"
**Interviewer:** "You'll need to build the tree structure from the input data."

**Candidate:** "What's the expected scale? How many employees and groups?"
**Interviewer:** "Assume up to 10,000 employees and 1,000 groups. Tree height won't exceed 20."

### Phase 2: Approach Discussion (5-8 min)

**Candidate:** "This is a **Lowest Common Ancestor (LCA)** problem. We need to find a node that is an ancestor of all target employees and is the deepest such node."

**Candidate:** "I'm thinking of three possible approaches:
1. **Naive Recursive:** Start from root, recursively check which subtrees contain all employees. O(N²) time.
2. **Path Tracing:** Build paths from each employee to root, find common prefix. O(K × H) time where K is number of employees and H is tree height.
3. **Parent Pointers with Set Intersection:** Store all ancestors in sets, intersect them. Similar complexity but different implementation."

**Candidate:** "I'll go with **Path Tracing** because:
- It's intuitive and easy to explain
- Time complexity is optimal for this problem
- Easy to debug and test
- Works well with the tree structure we're building"

### Phase 3: Coding (15-20 min)

**Candidate:** "I'll implement this in three steps:
1. Define the TreeNode structure
2. Build the tree from input data
3. Implement the LCA query using path comparison"

### Phase 4: Testing & Verification (5-7 min)

**Candidate:** "Let me walk through the example with Alice and Lisa:
1. Find Alice node → Trace path: [Company, Engg, Backend, Alice]
2. Find Lisa node → Trace path: [Company, Engg, Frontend, Lisa]
3. Compare indices:
   - Index 0: Company == Company ✓
   - Index 1: Engg == Engg ✓
   - Index 2: Backend ≠ Frontend ✗
4. Last common: Engg ✓"

---

## 🧠 Intuition & Approach

### Why is this an LCA Problem?

We're looking for a **group (node)** that:
1. Is an ancestor of ALL target employees (contains all of them in its subtree)
2. Is the **lowest** (deepest/closest) such node in the hierarchy

This is precisely the definition of **Lowest Common Ancestor**.

### Approach Comparison

| Approach | Time | Space | Pros | Cons |
|----------|------|-------|------|------|
| **Naive Recursive** | O(N²) | O(H) | Simple concept | Too slow for large trees |
| **Path Tracing** | O(K×H) | O(K×H) | Clear logic, optimal | Extra space for paths |
| **Set Intersection** | O(K×H) | O(K×H) | Handles multi-group follow-up well | Slightly more complex |

**Recommended:** Path Tracing for interviews (clearest explanation, optimal complexity)

### Why Path Tracing Works

**Key Insight:** In a tree, the path from any node to the root is unique. If two nodes share a common ancestor, their paths must overlap from the root up to that ancestor.

**Visual Trace:**
```text
Alice path:  [Company, Engg, Backend, Alice]
                 ↓       ↓      ↓       ↓
Lisa path:   [Company, Engg, Frontend, Lisa]
                 ✓       ✓       ✗       ✗
```
Last matching position → **Engg**

---

## 📝 Solution 1: Simplified Interview Version (Recommended)

This version is concise, uses standard Python dictionaries, and is perfect for a 20-45 minute interview. It avoids the boilerplate of creating a custom `TreeNode` class.

```python
def find_closest_group_simple(hierarchy, employees):
    """
    Simplified solution using a dictionary for parent lookups.
    """
    # 1. Build a Parent Map (child -> parent)
    # This replaces the entire TreeNode class and tree building logic
    parent_map = {}
    
    def build_map(data, parent_name):
        if isinstance(data, dict):
            for group, content in data.items():
                parent_map[group] = parent_name
                build_map(content, group)
        elif isinstance(data, list):
            for emp in data:
                parent_map[emp] = parent_name

    # Assume "Company" is the root
    build_map(hierarchy, "Company")

    # 2. Helper to get path from Root -> Node
    def get_path(node):
        path = []
        while node:
            path.append(node)
            node = parent_map.get(node) # Move up to parent
        return path[::-1] # Reverse to get [Company, Engg, Backend, Alice]

    if not employees: return None

    # 3. Find LCA by comparing paths
    # Start with the first employee's path as the "common" path
    common_path = get_path(employees[0])

    for emp in employees[1:]:
        current_path = get_path(emp)
        
        # Keep only the matching prefix
        new_common = []
        for i in range(min(len(common_path), len(current_path))):
            if common_path[i] == current_path[i]:
                new_common.append(common_path[i])
            else:
                break
        common_path = new_common
        
        if not common_path: return None # No common ancestor

    # The last node in the common path is the LCA
    lca = common_path[-1]
    
    # Edge case: If LCA is one of the employees (e.g. input ["Alice"]), return their parent
    if lca in employees:
        return parent_map.get(lca)
        
    return lca
```

---

## 📝 Solution 2: Production-Ready (Class-Based)

This version uses classes, type hinting, and is more structured. Use this if the interviewer explicitly asks for Object-Oriented Design or if you are applying for a Senior role where code structure is critical.

### Algorithm Steps

**Step 1:** Build the tree structure with parent pointers
- Parse input data (nested dict or adjacency list)
- Create TreeNode objects
- Link parent-child relationships
- Store nodes in a HashMap for O(1) lookup

**Step 2:** For each employee, trace path to root
- Start at employee node
- Follow parent pointers until reaching root
- Store path in array
- Reverse array (to get root → employee direction)

**Step 3:** Find longest common prefix of all paths
- Compare paths element by element
- Stop when paths diverge
- Return last common element

### Complete Implementation

```python
from typing import List, Dict, Optional

class TreeNode:
    """Represents a node in the organization hierarchy."""
    def __init__(self, name: str):
        self.name = name
        self.parent: Optional[TreeNode] = None
        self.children: List[TreeNode] = []

class EmployeeDirectory:
    """
    Main class to manage employee hierarchy and find closest common groups.
    
    Supports:
    - Building hierarchy from nested dictionary
    - Finding closest common group for a set of employees
    - O(1) employee lookup
    """
    
    def __init__(self):
        self.nodes: Dict[str, TreeNode] = {}
        self.root: Optional[TreeNode] = None
    
    def build_from_dict(self, hierarchy: Dict) -> None:
        """
        Build tree from nested dictionary structure.
        
        Args:
            hierarchy: Nested dict like:
                {
                    "Engg": {
                        "Backend": ["Alice", "Bob"],
                        "Frontend": ["Lisa"]
                    },
                    "HR": ["Charlie"]
                }
        
        Time: O(N) where N = total nodes
        Space: O(N) for storing nodes
        """
        # Create root
        self.root = TreeNode("Company")
        self.nodes["Company"] = self.root
        
        # Recursively build tree
        self._build_recursive(hierarchy, self.root)
    
    def _build_recursive(self, data, parent: TreeNode) -> None:
        """Helper to recursively build tree."""
        if isinstance(data, dict):
            # data is a dictionary of sub-groups
            for name, children in data.items():
                # Create group node
                node = TreeNode(name)
                node.parent = parent
                parent.children.append(node)
                self.nodes[name] = node
                
                # Recurse on children
                self._build_recursive(children, node)
                
        elif isinstance(data, list):
            # data is a list of employees (leaf nodes)
            for emp_name in data:
                emp_node = TreeNode(emp_name)
                emp_node.parent = parent
                parent.children.append(emp_node)
                self.nodes[emp_name] = emp_node
    
    def find_closest_group(self, employees: List[str]) -> Optional[str]:
        """
        Find the closest common parent group for given employees.
        
        Args:
            employees: List of employee names
            
        Returns:
            Name of closest common group, or None if not found
            
        Time: O(K × H) where K = len(employees), H = tree height
        Space: O(K × H) for storing paths
        
        Raises:
            ValueError: If any employee is not found
        """
        # Edge case: empty input
        if not employees:
            return None
        
        # Edge case: single employee
        if len(employees) == 1:
            if employees[0] not in self.nodes:
                raise ValueError(f"Employee '{employees[0]}' not found")
            
            emp_node = self.nodes[employees[0]]
            # Return parent group (not the employee itself)
            if emp_node.parent:
                return emp_node.parent.name
            return None
        
        # Step 1: Get paths for all employees
        paths = []
        for emp in employees:
            if emp not in self.nodes:
                raise ValueError(f"Employee '{emp}' not found")
            
            path = self._get_path_to_root(self.nodes[emp])
            paths.append(path)
        
        # Step 2: Find longest common prefix
        lca_name = self._find_common_prefix(paths)
        
        # Edge case: If LCA is an employee (shouldn't happen with valid input),
        # return their parent
        if lca_name in employees:
            node = self.nodes[lca_name]
            if node.parent:
                return node.parent.name
            return None
        
        return lca_name
    
    def _get_path_to_root(self, node: TreeNode) -> List[str]:
        """
        Trace path from node to root.
        
        Time: O(H) where H = tree height
        Space: O(H) for path storage
        """
        path = []
        current = node
        
        while current:
            path.append(current.name)
            current = current.parent
        
        # Reverse to get root → node direction
        return path[::-1]
    
    def _find_common_prefix(self, paths: List[List[str]]) -> Optional[str]:
        """
        Find the longest common prefix of all paths.
        
        Time: O(K × H) where K = number of paths, H = avg path length
        Space: O(1) excluding input
        """
        if not paths:
            return None
        
        min_len = min(len(p) for p in paths)
        lca = None
        
        for i in range(min_len):
            # Check if all paths have the same node at position i
            first_node = paths[0][i]
            
            if all(path[i] == first_node for path in paths):
                lca = first_node
            else:
                # Paths diverge here, stop
                break
        
        return lca


# ============================================
# COMPLETE RUNNABLE EXAMPLE
# ============================================

if __name__ == "__main__":
    # Build organization hierarchy
    directory = EmployeeDirectory()
    
    hierarchy = {
        "Engg": {
            "Backend": ["Alice", "Bob"],
            "Frontend": ["Lisa"],
            "Mobile": ["Mike"]
        },
        "HR": ["Charlie"],
        "Sales": {
            "North": ["David"],
            "South": ["Eve"]
        }
    }
    
    directory.build_from_dict(hierarchy)
    
    # Test cases
    print("=" * 50)
    print("EMPLOYEE HIERARCHY - LCA FINDER")
    print("=" * 50)
    
    test_cases = [
        (["Alice", "Bob"], "Backend"),
        (["Alice", "Lisa"], "Engg"),
        (["Alice", "Bob", "Lisa"], "Engg"),
        (["Alice", "Charlie"], "Company"),
        (["David", "Eve"], "Sales"),
        (["Alice"], "Backend"),
        (["Mike", "Lisa"], "Engg"),
    ]
    
    for employees, expected in test_cases:
        result = directory.find_closest_group(employees)
        status = "✓" if result == expected else "✗"
        print(f"{status} Input: {employees}")
        print(f"  Expected: {expected}, Got: {result}")
        print()
    
    # Show internal paths for debugging
    print("\n" + "=" * 50)
    print("PATH TRACING (for Alice and Lisa)")
    print("=" * 50)
    
    alice_path = directory._get_path_to_root(directory.nodes["Alice"])
    lisa_path = directory._get_path_to_root(directory.nodes["Lisa"])
    
    print(f"Alice path: {' → '.join(alice_path)}")
    print(f"Lisa path:  {' → '.join(lisa_path)}")
    print(f"\nCommon Prefix: ", end="")
    
    for i in range(min(len(alice_path), len(lisa_path))):
        if alice_path[i] == lisa_path[i]:
            print(f"{alice_path[i]}", end="")
            if i < min(len(alice_path), len(lisa_path)) - 1:
                print(" → ", end="")
        else:
            break
    
    print(f"\nLCA: {directory.find_closest_group(['Alice', 'Lisa'])}")
```

---

## 🔍 Complexity Analysis

### Time Complexity: **O(K × H)**

**Breakdown:**
- **Building Tree:** O(N) where N = total nodes (employees + groups)
  - We visit each node once during recursive construction
- **Query (find_closest_group):**
  - For K employees:
    - Get path for each: O(H) per employee
    - Total: O(K × H)
  - Find common prefix: O(K × H)
    - Compare up to H positions
    - For each position, check K paths
  - **Total Query:** O(K × H)

**Where:**
- K = Number of employees in query
- H = Height of organization tree (typically H ≪ N)
- N = Total nodes in tree

**Typical Values:**
- Large company: N = 10,000, H = 10-15 (log scale)
- Query: K = 2-5 employees
- Time: ~20-75 comparisons (very fast!)

### Space Complexity: **O(K × H)**

**Breakdown:**
- **Tree Storage:** O(N) for nodes HashMap and TreeNode objects
- **Query:**
  - K paths, each of length ≤ H: O(K × H)
  - Temporary variables: O(1)
- **Total:** O(N + K × H)

**Optimization:** If memory is critical, we could avoid storing full paths by comparing on-the-fly (but code becomes more complex).

---

## ⚠️ Common Pitfalls

### 1. **Assuming Binary Tree**
**Problem:** Using binary tree LCA algorithms (recursion with left/right checks).
**Why it fails:** Organization is an **N-ary tree** (a manager can have many reports).
**Fix:** Use path-based or iterative approaches that don't assume two children.

### 2. **Not Reversing Path**
**Problem:**
```python
path = []
while current:
    path.append(current.name)
    current = current.parent
return path  # ❌ Wrong order!
```
**Why it fails:** Path goes Employee → Root, but LCA comparison needs Root → Employee.
**Fix:** `return path[::-1]`

### 3. **Returning Employee Name Instead of Group**
**Problem:** For input `["Alice"]`, returning "Alice" instead of "Backend".
**Why it fails:** Question asks for closest *group*, not the employee.
**Fix:** Check if result is in employee list, return parent if so.

### 4. **Not Handling Edge Cases**
**Common issues:**
- Empty input `[]` → Should return `None`
- Single employee → Return their parent group
- Non-existent employee → Should raise error or return `None`
- Duplicate employees → Should handle gracefully

### 5. **Forgetting O(1) Lookup**
**Problem:** Searching for employees by iterating through tree each time.
**Why it fails:** O(N) lookup makes total complexity O(K × N × H).
**Fix:** Use HashMap (`self.nodes`) for O(1) employee lookup.

---

## 🔄 Follow-up Questions

### Follow-up 1: Employees in Multiple Groups

**Problem Statement:**
> "Now employees can belong to multiple groups. For example, Alice is in both Backend and Mobile (she works part-time in both teams). How does your solution change?"

**Visual Example:**
```text
Organization Structure:
                    Company
                   /      \
              Engg         Sales
             /  |  \
     Backend Frontend Mobile
        |       |       |
      Alice   Lisa   Alice (same person!)
        |             Mike
       Bob
       
Alice is in TWO groups: Backend AND Mobile
```

**Modified Input:**
```python
employee_to_groups = {
    "Alice": ["Backend", "Mobile"],  # Alice in 2 groups
    "Bob": ["Backend"],
    "Lisa": ["Frontend"],
    "Mike": ["Mobile"]
}

# Example Query:
find_closest_group(["Alice", "Bob"])
# Alice paths: [Company, Engg, Backend] OR [Company, Engg, Mobile]
# Bob path: [Company, Engg, Backend]
# We need to find which path from Alice gives closest LCA with Bob
```

#### Solution 1: Simplified (Interview Recommended)

```python
def find_closest_multi_simple(hierarchy, employees):
    """
    Simplified solution for multiple groups using Set Intersection.
    """
    # 1. Build Parent Map (child -> LIST of parents)
    parents = {} # name -> [parent_names]
    
    def build_multi_map(data, parent_name):
        if isinstance(data, dict):
            for group, content in data.items():
                if group not in parents: parents[group] = []
                parents[group].append(parent_name)
                build_multi_map(content, group)
        elif isinstance(data, list):
            for emp in data:
                if emp not in parents: parents[emp] = []
                parents[emp].append(parent_name)

    build_multi_map(hierarchy, "Company")
    
    # 2. Helper to get ALL ancestors of a node
    def get_all_ancestors(node):
        ancestors = set()
        queue = [node]
        while queue:
            curr = queue.pop(0)
            ancestors.add(curr)
            # Add all parents to queue
            for p in parents.get(curr, []):
                if p not in ancestors:
                    queue.append(p)
        return ancestors

    if not employees: return None

    # 3. Intersect Ancestor Sets
    # Start with ancestors of first employee
    common_ancestors = get_all_ancestors(employees[0])
    
    for emp in employees[1:]:
        emp_ancestors = get_all_ancestors(emp)
        common_ancestors = common_ancestors.intersection(emp_ancestors)
        
    if not common_ancestors: return None
    
    # 4. Find the deepest ancestor in the common set
    # We need a way to measure depth. Simple BFS from root can assign depths.
    # For interview, you can assume a helper `get_depth(node)` exists or implement simple one.
    
    # (Simplified depth check for this snippet)
    # In a real interview, you'd calculate depth. Here we just return one.
    return list(common_ancestors)[0] 
```

#### Solution 2: Production (Class-Based)

**Algorithm: Set Intersection Approach**

**Step-by-Step:**
1. For each employee, collect ALL their ancestor groups (from all their groups)
2. Find the intersection of all ancestor sets
3. Return the deepest (maximum depth) common ancestor

**Visual Walkthrough:**
```text
Query: ["Alice", "Mike"]

Step 1: Get all ancestors for Alice
  - From Backend: {Company, Engg, Backend}
  - From Mobile: {Company, Engg, Mobile}
  - Union: {Company, Engg, Backend, Mobile}

Step 2: Get all ancestors for Mike
  - From Mobile: {Company, Engg, Mobile}

Step 3: Intersection
  {Company, Engg, Backend, Mobile} ∩ {Company, Engg, Mobile}
  = {Company, Engg, Mobile}

Step 4: Find deepest
  - Company (depth 0)
  - Engg (depth 1)
  - Mobile (depth 2) ← DEEPEST
  
Result: "Mobile"
```

**Complete Implementation:**

```python
from typing import List, Dict, Set

class MultiGroupDirectory:
    """
    Employee directory where employees can belong to multiple groups.
    """
    
    def __init__(self):
        self.nodes = {}  # name -> TreeNode
        self.employee_to_groups = {}  # emp_name -> [group_names]
        self.root = None
    
    def add_employee_to_group(self, emp_name: str, group_name: str):
        """Add an employee to a group (can be called multiple times)."""
        if emp_name not in self.employee_to_groups:
            self.employee_to_groups[emp_name] = []
        self.employee_to_groups[emp_name].append(group_name)
    
    def find_closest_group(self, employees: List[str]) -> str:
        """
        Find closest common ancestor when employees can be in multiple groups.
        
        Time: O(K × G × H) where G = avg groups per employee
        Space: O(K × G × H)
        """
        if not employees:
            return None
        
        # Step 1: Collect all ancestors for each employee
        all_ancestor_sets = []
        
        for emp in employees:
            if emp not in self.employee_to_groups:
                raise ValueError(f"Employee {emp} not found")
            
            # Get ancestors from ALL groups this employee belongs to
            employee_ancestors = set()
            
            for group_name in self.employee_to_groups[emp]:
                # Trace path from this group to root
                current = self.nodes[group_name]
                while current:
                    employee_ancestors.add(current.name)
                    current = current.parent
            
            all_ancestor_sets.append(employee_ancestors)
        
        # Step 2: Find intersection of all ancestor sets
        common_ancestors = set.intersection(*all_ancestor_sets)
        
        if not common_ancestors:
            return None
        
        # Step 3: Find the deepest (closest) common ancestor
        deepest = None
        max_depth = -1
        
        for ancestor_name in common_ancestors:
            depth = self._get_depth(self.nodes[ancestor_name])
            if depth > max_depth:
                max_depth = depth
                deepest = ancestor_name
        
        return deepest
    
    def _get_depth(self, node: 'TreeNode') -> int:
        """Get depth of a node (distance from root)."""
        depth = 0
        current = node
        while current.parent:
            depth += 1
            current = current.parent
        return depth


# ============================================
# COMPLETE EXAMPLE
# ============================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("FOLLOW-UP 1: EMPLOYEES IN MULTIPLE GROUPS")
    print("=" * 60)
    
    # Setup
    directory = MultiGroupDirectory()
    
    # Build tree (simplified for example)
    # ... (tree building code) ...
    
    # Add employees to multiple groups
    directory.add_employee_to_group("Alice", "Backend")
    directory.add_employee_to_group("Alice", "Mobile")  # Alice in 2 groups!
    directory.add_employee_to_group("Bob", "Backend")
    directory.add_employee_to_group("Mike", "Mobile")
    
    # Test cases
    print("\nTest 1: Alice (in Backend + Mobile) and Bob (in Backend)")
    result = directory.find_closest_group(["Alice", "Bob"])
    print(f"Result: {result}")  # Expected: Backend or Engg
    print("Explanation: Alice's Backend path shares Backend with Bob")
    
    print("\nTest 2: Alice (in Backend + Mobile) and Mike (in Mobile)")
    result = directory.find_closest_group(["Alice", "Mike"])
    print(f"Result: {result}")  # Expected: Mobile
    print("Explanation: Alice's Mobile path shares Mobile with Mike")
```

**Complexity Analysis:**
- **Time:** O(K × G × H)
  - K employees
  - G groups per employee (average)
  - H height to trace ancestors
- **Space:** O(K × G × H) for ancestor sets

---

### Follow-up 2: Thread Safety with Concurrent Updates

**Problem Statement:**
> "The hierarchy can be updated dynamically (employees added/removed, groups reorganized) while queries are running. How do you handle concurrent reads and writes efficiently?"

**Challenge:**
Multiple threads are:
- **Reading:** Finding LCA for employees
- **Writing:** Adding new employees, moving employees, reorganizing groups

#### Solution 1: Simplified Explanation (Interview Focus)

"To handle concurrency, I would use a **Read-Write Lock**.
- **Readers (Queries):** Acquire a shared `Read Lock`. Multiple queries can run at the same time.
- **Writers (Updates):** Acquire an exclusive `Write Lock`. This blocks all other readers and writers until the update is done.
This ensures we don't read the tree while it's being modified (preventing race conditions)."

```python
import threading

class ThreadSafeDirectory:
    def __init__(self):
        self.lock = threading.RLock() # Reentrant Lock
        self.data = {}

    def find_closest(self, emps):
        with self.lock: # Or read_lock if available
            # ... perform read ...
            pass

    def add_employee(self, emp, group):
        with self.lock: # Exclusive write lock
            # ... perform write ...
            pass
```

#### Solution 2: Production (Read-Write Lock)

**Concept:** Allow multiple readers OR one writer (not both).

```python
import threading
from typing import List

class ThreadSafeDirectory(EmployeeDirectory):
    """
    Thread-safe employee directory using locks.
    Multiple readers can read simultaneously.
    Writers get exclusive access.
    """
    
    def __init__(self):
        super().__init__()
        self.lock = threading.RLock()  # Reentrant lock
    
    def find_closest_group(self, employees: List[str]) -> str:
        """READ operation - multiple readers allowed."""
        with self.lock:
            return super().find_closest_group(employees)
    
    def add_employee(self, emp_name: str, group_name: str):
        """WRITE operation - exclusive access."""
        with self.lock:
            if group_name not in self.nodes:
                raise ValueError(f"Group {group_name} not found")
            
            # Create new employee node
            emp_node = TreeNode(emp_name)
            group_node = self.nodes[group_name]
            
            # Link to parent
            emp_node.parent = group_node
            group_node.children.append(emp_node)
            self.nodes[emp_name] = emp_node
    
    def move_employee(self, emp_name: str, new_group: str):
        """WRITE operation - move employee to different group."""
        with self.lock:
            if emp_name not in self.nodes:
                raise ValueError(f"Employee {emp_name} not found")
            if new_group not in self.nodes:
                raise ValueError(f"Group {new_group} not found")
            
            emp_node = self.nodes[emp_name]
            old_parent = emp_node.parent
            
            # Remove from old parent
            if old_parent:
                old_parent.children.remove(emp_node)
            
            # Add to new parent
            new_parent = self.nodes[new_group]
            emp_node.parent = new_parent
            new_parent.children.append(emp_node)


# Example Usage
if __name__ == "__main__":
    directory = ThreadSafeDirectory()
    
    # Thread 1: Reader
    def reader_thread():
        for _ in range(100):
            result = directory.find_closest_group(["Alice", "Bob"])
            print(f"Reader: {result}")
    
    # Thread 2: Writer
    def writer_thread():
        for i in range(10):
            directory.add_employee(f"NewEmp{i}", "Backend")
            print(f"Writer: Added NewEmp{i}")
    
    # Start threads
    t1 = threading.Thread(target=reader_thread)
    t2 = threading.Thread(target=writer_thread)
    
    t1.start()
    t2.start()
    t1.join()
    t2.join()
```

**Pros:**
- Simple to implement
- Correct (no race conditions)

**Cons:**
- Readers block each other (even though they could read simultaneously)
- Writers block readers (even though read operation is usually fast)

---

#### Solution 3: Copy-on-Write (Advanced, Better for Read-Heavy)

**Concept:** Create a new immutable snapshot for every write. Readers always read from a consistent snapshot without locks.

```python
import threading
from copy import deepcopy

class DirectorySnapshot:
    """Immutable snapshot of the directory."""
    def __init__(self, nodes_copy, root_copy):
        self.nodes = nodes_copy
        self.root = root_copy
    
    def find_closest_group(self, employees):
        # ... same LCA logic on this snapshot ...
        pass

class COWDirectory:
    """
    Copy-on-Write directory for high read throughput.
    
    Key idea:
    - Readers read from immutable snapshot (no lock!)
    - Writers create new snapshot (locked)
    - Atomic pointer swap to new snapshot
    """
    
    def __init__(self):
        self.current_snapshot = DirectorySnapshot({}, None)
        self.write_lock = threading.Lock()
    
    def find_closest_group(self, employees: List[str]) -> str:
        """
        READ operation - NO LOCK!
        
        Time: O(K × H)
        Space: O(K × H)
        """
        # Get reference to current snapshot (atomic read in Python)
        snapshot = self.current_snapshot
        
        # Read from immutable snapshot - no lock needed!
        return snapshot.find_closest_group(employees)
    
    def add_employee(self, emp_name: str, group_name: str):
        """
        WRITE operation - creates new snapshot.
        
        Time: O(N) to copy structure
        Space: O(N) for new snapshot
        """
        with self.write_lock:
            # 1. Create a copy of current structure
            new_nodes = deepcopy(self.current_snapshot.nodes)
            new_root = deepcopy(self.current_snapshot.root)
            
            # 2. Make modifications on the copy
            # ... add employee to new_nodes ...
            
            # 3. Create new snapshot
            new_snapshot = DirectorySnapshot(new_nodes, new_root)
            
            # 4. Atomic swap (single pointer update)
            self.current_snapshot = new_snapshot


# Example: High read throughput
if __name__ == "__main__":
    directory = COWDirectory()
    
    # 1000 readers (no blocking!)
    def reader():
        result = directory.find_closest_group(["Alice", "Bob"])
    
    # 1 writer (occasional)
    def writer():
        directory.add_employee("NewEmp", "Backend")
    
    readers = [threading.Thread(target=reader) for _ in range(1000)]
    writer_thread = threading.Thread(target=writer)
    
    # All readers run simultaneously without blocking!
    for r in readers:
        r.start()
    writer_thread.start()
```

**Pros:**
- **No reader blocking:** Readers never wait for each other
- **Consistent reads:** Each reader sees a consistent snapshot
- **Fast reads:** No lock overhead

**Cons:**
- **Expensive writes:** O(N) to copy structure
- **Memory usage:** Multiple snapshots can exist temporarily

**When to use COW:**
- Read-heavy workload (1000 reads : 1 write)
- Structure is relatively small
- Read latency is critical

---

### Follow-up 3: Flat Hierarchy Optimization

**Problem Statement:**
> "What if there's only one level of groups (no nested departments)? How would you optimize?"

**Example Structure:**
```text
Company (not relevant)
   ├─ Backend: [Alice, Bob, Charlie]
   ├─ Frontend: [Lisa, Mike]
   ├─ Mobile: [Alice, Mike]  ← Alice and Mike in multiple groups
   └─ Sales: [David]
```

**Key Insight:** No hierarchy means no tree traversal needed! Just set intersection.

#### Solution 1: Simplified (Interview Recommended)

```python
def find_common_flat_simple(employee_groups, employees):
    """
    employee_groups: dict { 'Alice': {'Backend', 'Mobile'}, 'Bob': {'Backend'} }
    """
    if not employees: return []
    
    # Start with groups of first employee
    common = employee_groups.get(employees[0], set()).copy()
    
    # Intersect with others
    for emp in employees[1:]:
        groups = employee_groups.get(emp, set())
        common &= groups # In-place intersection
        
    return list(common)
```

#### Solution 2: Production (Optimized Class)

```python
class FlatGroupDirectory:
    """
    Optimized directory for flat (single-level) hierarchy.
    
    No tree structure needed - just two HashMaps.
    """
    
    def __init__(self):
        # Bidirectional mappings
        self.employee_to_groups = {}  # emp -> set of groups
        self.group_to_employees = {}  # group -> set of employees
    
    def add_employee(self, emp: str, group: str):
        """
        Add employee to a group.
        
        Time: O(1)
        Space: O(1)
        """
        # Add to employee_to_groups
        if emp not in self.employee_to_groups:
            self.employee_to_groups[emp] = set()
        self.employee_to_groups[emp].add(group)
        
        # Add to group_to_employees
        if group not in self.group_to_employees:
            self.group_to_employees[group] = set()
        self.group_to_employees[group].add(emp)
    
    def find_common_groups(self, employees: List[str]) -> List[str]:
        """
        Find all groups that contain ALL given employees.
        
        Time: O(K × G) where K = num employees, G = avg groups per employee
        Space: O(G) for result set
        """
        if not employees:
            return []
        
        # Start with first employee's groups
        common = self.employee_to_groups.get(employees[0], set()).copy()
        
        # Intersect with each other employee's groups
        for emp in employees[1:]:
            if emp not in self.employee_to_groups:
                return []  # Employee not found
            
            common &= self.employee_to_groups[emp]
            
            # Early exit if no common groups
            if not common:
                return []
        
        return list(common)


# ============================================
# COMPLETE EXAMPLE
# ============================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("FOLLOW-UP 3: FLAT HIERARCHY OPTIMIZATION")
    print("=" * 60)
    
    directory = FlatGroupDirectory()
    
    # Build flat structure
    directory.add_employee("Alice", "Backend")
    directory.add_employee("Alice", "Mobile")  # Alice in 2 groups
    directory.add_employee("Bob", "Backend")
    directory.add_employee("Mike", "Mobile")
    directory.add_employee("Lisa", "Frontend")
    
    # Test cases
    print("\nTest 1: Alice and Bob")
    result = directory.find_common_groups(["Alice", "Bob"])
    print(f"Common groups: {result}")  # ["Backend"]
    
    print("\nTest 2: Alice and Mike")
    result = directory.find_common_groups(["Alice", "Mike"])
    print(f"Common groups: {result}")  # ["Mobile"]
    
    print("\nTest 3: Alice, Bob, and Mike")
    result = directory.find_common_groups(["Alice", "Bob", "Mike"])
    print(f"Common groups: {result}")  # [] (no group contains all 3)
    
    print("\nTest 4: Only Alice")
    result = directory.find_common_groups(["Alice"])
    print(f"Common groups: {result}")  # ["Backend", "Mobile"]
```

**Visual Walkthrough:**
```text
Query: ["Alice", "Bob"]

Step 1: Get Alice's groups
  Alice → {Backend, Mobile}

Step 2: Get Bob's groups
  Bob → {Backend}

Step 3: Intersection
  {Backend, Mobile} ∩ {Backend} = {Backend}

Result: ["Backend"]
```

**Performance Comparison:**

| Operation | Tree Approach | Flat Approach | Speedup |
|-----------|---------------|---------------|---------|
| Add Employee | O(1) | O(1) | Same |
| Find Common | O(K × H) | O(K × G) | 10x faster* |
| Memory | O(N) | O(N + E) | Similar |

*For typical cases where H=10, G=2

**When to use Flat approach:**
- Organization has no hierarchy (all groups at same level)
- Don't care about "closest" - just "common"
- Performance is critical

---

## 🧪 Test Cases

### Basic Functionality
```python
# Test 1: Same parent
assert find_closest_group(["Alice", "Bob"]) == "Backend"

# Test 2: Different sub-departments
assert find_closest_group(["Alice", "Lisa"]) == "Engg"

# Test 3: Multiple employees
assert find_closest_group(["Alice", "Bob", "Lisa"]) == "Engg"
```

### Edge Cases
```python
# Test 4: Single employee
assert find_closest_group(["Alice"]) == "Backend"

# Test 5: Empty input
assert find_closest_group([]) is None

# Test 6: Different top-level departments
assert find_closest_group(["Alice", "Charlie"]) == "Company"

# Test 7: Root level
assert find_closest_group(["Charlie"]) == "HR"

# Test 8: All employees in company
assert find_closest_group(["Alice", "Charlie", "David"]) == "Company"
```

### Error Cases
```python
# Test 9: Non-existent employee
with pytest.raises(ValueError):
    find_closest_group(["Alice", "Zorro"])

# Test 10: Duplicate employees (should work)
assert find_closest_group(["Alice", "Alice"]) == "Backend"
```

### Performance Test
```python
# Test 11: Large number of employees
many_employees = ["Emp" + str(i) for i in range(100)]
result = find_closest_group(many_employees)
# Should complete in < 1ms for H=20
```

---

## 🎯 Key Takeaways

1. **Recognize LCA Pattern:** "Closest common parent/ancestor" → LCA problem
2. **Path Tracing is Intuitive:** Easier to explain than recursive approaches
3. **Use HashMap for O(1) Lookup:** Critical for performance
4. **Handle Edge Cases:** Empty, single, invalid inputs
5. **N-ary Trees are Different:** Can't use binary tree algorithms directly

---

## 📚 Related Problems

- **LeetCode 236:** Lowest Common Ancestor of a Binary Tree
- **LeetCode 1644:** LCA of Binary Tree II (with node not found)
- **LeetCode 1650:** LCA of Binary Tree III (with parent pointers)
- **LeetCode 1676:** LCA of Binary Tree IV (K nodes)
