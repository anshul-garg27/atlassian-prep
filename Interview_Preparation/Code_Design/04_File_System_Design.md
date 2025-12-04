# 📁 PROBLEM 4: FILE SYSTEM DESIGN

### ⭐⭐⭐⭐ **Design In-Memory File System with O(1) Size Lookup**

**Frequency:** MEDIUM-HIGH at Atlassian
**Difficulty:** Medium-Hard
**Time to Solve:** 35-45 minutes
**Focus:** Tree Structures, Size Caching, Path Parsing

---

## 📋 Problem Statement

Design an in-memory file system that supports:
- `add_file(path, size)`: Add file at given path
- `get_size(path)`: Get total size of directory **in O(1)** after traversal
- `list_contents(path)`: List all files/directories at path
- Optional: Support wildcard patterns (`*.txt`, `/home/*/*.py`)

**Key Challenge:** Propagate size updates to all parent directories for O(1) size lookups.

**Constraints:**
- Path format: `/home/user/file.txt`
- File sizes: positive integers
- Directory sizes: sum of all descendant files
- Support nested directories of any depth

---

## 🎯 INTERVIEW FLOW: Step-by-Step Guide

### **PHASE 1: Clarify Requirements (2-3 minutes)**

**SAY THIS:**
> "Before I start designing, let me clarify a few requirements:"

**Questions to Ask:**
1. "Should directory size include all descendants or just direct children?"
2. "Do we need to support file updates (change size)?"
3. "Should paths be case-sensitive?"
4. "Do we need to support symlinks?"
5. "Should we support recursive delete?"
6. "Do we need thread safety?"

**WRITE DOWN the answers. This shows you're thorough.**

---

### **PHASE 2: Discuss Key Design Decisions (3-4 minutes)**

**SAY THIS:**
> "There's a key trade-off for the O(1) size requirement. Let me explain my approach."

#### **Size Calculation: On-Demand vs Cached**

```text
Approach 1: On-Demand (Naive)
- get_size() recursively sums all descendants
- Time: O(N) where N = number of descendant files
- Space: O(1) - no extra storage

Approach 2: Cached with Propagation (Optimal) ✓
- Each directory stores cached total size
- add_file() propagates size to ALL ancestors
- Time: get_size = O(1), add_file = O(depth)
- Space: O(1) per directory for cached size
```

**Explain:**
> "I'll cache directory sizes and propagate updates to ancestors.
> This makes get_size O(1) after reaching the node, at the cost of O(depth) on add_file.
> This is the right trade-off because reads are typically more frequent than writes."

---

#### **Data Structure: Tree**

```text
Why Tree?
- Natural representation for hierarchical data
- Each node has: name, is_file, size, children, parent
- Parent pointer enables upward size propagation
```

---

### **PHASE 3: High-Level Design (2-3 minutes)**

**SAY THIS:**
> "Let me draw the tree structure and explain the size propagation."

**Draw on whiteboard:**
```
                    /  (root)
                    │  size: 850 (cached total)
                    │
        ┌───────────┴───────────┐
        │                       │
      home/                   tmp/
      size: 800               size: 50
        │                       │
    ┌───┴───┐                 temp.log
    │       │                  (50 bytes)
  alice/   bob/
  600      200
    │       │
  ┌─┴─┐   code.py
  │   │   (200 bytes)
docs/ pics/
100   500

When add_file("/home/alice/docs/new.txt", 100):
1. Create file node (100 bytes)
2. Update docs/ → 200 bytes
3. Update alice/ → 700 bytes
4. Update home/ → 900 bytes
5. Update / → 950 bytes
```

**Explain:**
> "The key insight is **upward propagation**:
> When a file is added, we update the size of EVERY ancestor directory.
> This makes `get_size()` O(1) because the answer is already computed."

---

### **PHASE 4: Design Patterns & Principles (2 minutes)**

**SAY THIS:**
> "I'm using the Composite Pattern here."

#### **Composite Pattern** ⭐⭐⭐

```python
from abc import ABC, abstractmethod

class FileSystemNode(ABC):
    """Abstract base - both files and directories share this interface."""
    
    @abstractmethod
    def get_size(self) -> int:
        pass
    
    @abstractmethod
    def is_file(self) -> bool:
        pass

class File(FileSystemNode):
    def get_size(self) -> int:
        return self._size  # Direct size
    
    def is_file(self) -> bool:
        return True

class Directory(FileSystemNode):
    def get_size(self) -> int:
        return self._cached_size  # O(1) - cached!
    
    def is_file(self) -> bool:
        return False
```

**Why Composite?**
> "Files and directories can be treated uniformly through the same interface.
> Client code can call `get_size()` without knowing if it's a file or directory."

---

### **PHASE 5: Data Structures & Why (2 minutes)**

**SAY THIS:**
> "Let me explain my data structure choices."

| Data Structure | Used For | Why This Choice |
|----------------|----------|-----------------|
| `Dict[str, FileNode]` | Directory children | O(1) lookup by name |
| `FileNode.parent` | Parent reference | O(1) upward propagation |
| `int size` | Cached size | O(1) size retrieval |
| `dataclass` | FileNode | Clean initialization |
| `split("/")` | Path parsing | Standard path handling |

**Key Insight:**
> "The parent pointer is crucial. Without it, we'd need to:
> 1. Parse the path again, or
> 2. Keep track of ancestors during traversal
> 
> With parent pointer, size propagation is just a while loop: `while node: update; node = node.parent`"

---

### **PHASE 6: Write the Code (15-20 minutes)**

**SAY THIS:**
> "Now let me implement this. I'll start with FileNode, then FileSystem."

```python
"""
In-Memory File System Design
============================
Tree-based file system with O(1) directory size lookups.

Design Patterns:
- Composite Pattern: Files and directories share interface
- Tree Structure: Natural hierarchical representation

Key Feature: Cached directory sizes with ancestor propagation

Time Complexity:
- add_file: O(depth) - path traversal + size propagation
- get_size: O(depth) for traversal, O(1) for size
- list_contents: O(depth) + O(children)

Space Complexity: O(total_nodes)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import fnmatch


@dataclass
class FileNode:
    """
    Node in the file system tree.
    
    Represents either a file or directory.
    Directories cache their total size for O(1) lookup.
    
    Key Design Decisions:
    1. is_file flag distinguishes files from directories
    2. size field: actual size for files, cached total for directories
    3. parent pointer enables upward size propagation
    4. children dict for O(1) child lookup
    """
    name: str
    is_file: bool = False
    size: int = 0
    children: Dict[str, 'FileNode'] = field(default_factory=dict)
    parent: Optional['FileNode'] = None
    
    def __str__(self):
        node_type = "File" if self.is_file else "Dir"
        return f"{node_type}({self.name}, size={self.size})"


class FileSystem:
    """
    In-Memory File System with O(1) Directory Size Lookup.
    
    The key optimization is caching directory sizes:
    - Each directory stores the total size of ALL descendants
    - When a file is added/deleted, we update ALL ancestor directories
    - This makes get_size() O(1) after reaching the directory
    
    Trade-off:
    - Read (get_size): O(depth) traversal + O(1) lookup
    - Write (add_file): O(depth) traversal + O(depth) propagation
    - Good trade-off because reads >> writes in most file systems
    
    Example:
        >>> fs = FileSystem()
        >>> fs.add_file("/home/user/doc.txt", 100)
        >>> fs.get_size("/home/user")  # 100 (O(1) after reaching node)
        >>> fs.get_size("/home")  # 100 (propagated up)
    """
    
    def __init__(self):
        """Initialize file system with root directory."""
        self.root = FileNode(name="/", is_file=False)
    
    def add_file(self, path: str, file_size: int) -> bool:
        """
        Add a file at the given path.
        Creates intermediate directories if they don't exist.
        
        Args:
            path: Absolute path (e.g., "/home/user/file.txt")
            file_size: Size of the file in bytes
            
        Returns:
            True if file added successfully
            
        Time: O(depth) for traversal + O(depth) for propagation
        """
        if not path or not path.startswith("/"):
            raise ValueError("Path must be absolute (start with /)")
        if file_size < 0:
            raise ValueError("File size must be non-negative")
        
        parts = self._parse_path(path)
        if not parts:
            raise ValueError("Cannot add file at root path")
        
        # Navigate to parent directory, creating dirs as needed
        current = self.root
        ancestors = [current]  # Track ancestors for size propagation
        
        for dir_name in parts[:-1]:  # All but last (filename)
            if dir_name not in current.children:
                # Create intermediate directory
                new_dir = FileNode(name=dir_name, is_file=False, parent=current)
                current.children[dir_name] = new_dir
            
            current = current.children[dir_name]
            
            if current.is_file:
                raise ValueError(f"Cannot create directory: {dir_name} is a file")
            
            ancestors.append(current)
        
        # Add the file
        file_name = parts[-1]
        
        # Handle file overwrite - calculate size difference
        old_size = 0
        if file_name in current.children:
            existing = current.children[file_name]
            if not existing.is_file:
                raise ValueError(f"Cannot overwrite directory with file: {file_name}")
            old_size = existing.size
        
        # Create/update file node
        file_node = FileNode(
            name=file_name, 
            is_file=True, 
            size=file_size, 
            parent=current
        )
        current.children[file_name] = file_node
        
        # ★ KEY: Propagate size change to ALL ancestors
        size_delta = file_size - old_size
        for ancestor in ancestors:
            ancestor.size += size_delta
        
        return True
    
    def get_size(self, path: str) -> int:
        """
        Get total size of file or directory.
        
        For directories: Returns cached total (O(1) after traversal)
        For files: Returns file size
        
        Time: O(depth) for traversal, O(1) for actual size lookup
        """
        node = self._navigate(path)
        if node is None:
            raise FileNotFoundError(f"Path not found: {path}")
        return node.size  # O(1) - it's cached!
    
    def list_contents(self, path: str) -> List[str]:
        """
        List contents of a directory.
        
        Returns sorted list of child names.
        """
        node = self._navigate(path)
        
        if node is None:
            raise FileNotFoundError(f"Path not found: {path}")
        if node.is_file:
            raise NotADirectoryError(f"Not a directory: {path}")
        
        return sorted(node.children.keys())
    
    def delete_file(self, path: str) -> bool:
        """
        Delete a file (not directory).
        
        Updates ancestor sizes after deletion.
        """
        parts = self._parse_path(path)
        if not parts:
            raise ValueError("Cannot delete root")
        
        # Navigate to parent
        parent_path = "/" + "/".join(parts[:-1]) if len(parts) > 1 else "/"
        parent = self._navigate(parent_path)
        if parent is None:
            raise FileNotFoundError("Parent directory not found")
        
        file_name = parts[-1]
        if file_name not in parent.children:
            raise FileNotFoundError(f"File not found: {path}")
        
        file_node = parent.children[file_name]
        if not file_node.is_file:
            raise IsADirectoryError(f"Cannot delete directory with delete_file: {path}")
        
        # ★ Propagate size decrease to ALL ancestors
        size_to_remove = file_node.size
        current = parent
        while current is not None:
            current.size -= size_to_remove
            current = current.parent
        
        del parent.children[file_name]
        return True
    
    def exists(self, path: str) -> bool:
        """Check if path exists."""
        return self._navigate(path) is not None
    
    def is_file(self, path: str) -> bool:
        """Check if path is a file."""
        node = self._navigate(path)
        return node is not None and node.is_file
    
    def is_directory(self, path: str) -> bool:
        """Check if path is a directory."""
        node = self._navigate(path)
        return node is not None and not node.is_file
    
    def glob(self, pattern: str) -> List[str]:
        """
        Find files matching a pattern.
        Supports wildcards: * matches any characters
        
        Example: "/home/*/*.txt" matches all .txt files in subdirs of /home
        """
        results = []
        self._glob_recursive(self.root, "", pattern, results)
        return sorted(results)
    
    def _glob_recursive(self, node: FileNode, current_path: str, 
                        pattern: str, results: List[str]) -> None:
        """Recursive helper for glob matching."""
        for name, child in node.children.items():
            child_path = f"{current_path}/{name}"
            
            if fnmatch.fnmatch(child_path, pattern):
                results.append(child_path)
            
            if not child.is_file:
                self._glob_recursive(child, child_path, pattern, results)
    
    def _parse_path(self, path: str) -> List[str]:
        """
        Parse path into components.
        
        "/home/user/file.txt" → ["home", "user", "file.txt"]
        "/" → []
        """
        if path == "/":
            return []
        return [p for p in path.split("/") if p]
    
    def _navigate(self, path: str) -> Optional[FileNode]:
        """
        Navigate to node at given path.
        
        Time: O(depth)
        """
        if path == "/":
            return self.root
        
        parts = self._parse_path(path)
        current = self.root
        
        for part in parts:
            if current.is_file or part not in current.children:
                return None
            current = current.children[part]
        
        return current
    
    def print_tree(self, path: str = "/", indent: int = 0) -> None:
        """Print visual representation of file system tree."""
        node = self._navigate(path)
        if node is None:
            print(f"Path not found: {path}")
            return
        
        prefix = "  " * indent
        
        if node == self.root:
            print(f"{prefix}/ (size: {node.size})")
        
        for name in sorted(node.children.keys()):
            child = node.children[name]
            if child.is_file:
                print(f"{prefix}├── {name} ({child.size} bytes)")
            else:
                print(f"{prefix}├── {name}/ (size: {child.size})")
                self.print_tree(f"{path.rstrip('/')}/{name}", indent + 1)


# ============ Demo ============
def main():
    """Demonstrate file system functionality."""
    print("=" * 60)
    print("IN-MEMORY FILE SYSTEM DEMO")
    print("=" * 60)
    
    fs = FileSystem()
    
    # Add files
    print("\n📁 Adding files...")
    fs.add_file("/home/alice/docs/file1.txt", 100)
    fs.add_file("/home/alice/pics/photo.jpg", 500)
    fs.add_file("/home/bob/code.py", 200)
    fs.add_file("/tmp/temp.log", 50)
    
    print("\nFile System Structure:")
    fs.print_tree()
    
    print("\n" + "=" * 60)
    print("SIZE QUERIES (O(1) after reaching node)")
    print("=" * 60)
    print(f"get_size('/home/alice') = {fs.get_size('/home/alice')} bytes")
    print(f"get_size('/home') = {fs.get_size('/home')} bytes")
    print(f"get_size('/') = {fs.get_size('/')} bytes")
    
    print("\n" + "=" * 60)
    print("LIST CONTENTS")
    print("=" * 60)
    print(f"list_contents('/home') = {fs.list_contents('/home')}")
    print(f"list_contents('/home/alice') = {fs.list_contents('/home/alice')}")
    
    print("\n" + "=" * 60)
    print("GLOB PATTERNS")
    print("=" * 60)
    print(f"glob('*.txt') = {fs.glob('*.txt')}")
    print(f"glob('/home/*') = {fs.glob('/home/*')}")
    
    print("\n" + "=" * 60)
    print("DELETE FILE - Size Propagation")
    print("=" * 60)
    print(f"Size before delete: {fs.get_size('/home/alice')}")
    fs.delete_file("/home/alice/docs/file1.txt")
    print(f"Size after delete:  {fs.get_size('/home/alice')}")
    print(f"Root size:          {fs.get_size('/')}")


if __name__ == "__main__":
    main()
```

---

### **PHASE 7: Walk Through Edge Cases (3-4 minutes)**

**SAY THIS:**
> "Let me discuss the edge cases I've handled."

| Edge Case | How Handled | Code Location |
|-----------|-------------|---------------|
| **Root path "/"** | Special handling - cannot add file | `add_file()` validation |
| **Relative path** | Reject - require absolute | `add_file()` validation |
| **Create file where dir exists** | Raise error | `add_file()` check |
| **File overwrite** | Update size, propagate difference | `add_file()` old_size |
| **Delete non-empty dir** | Use separate method (recursive delete) | `delete_file()` |
| **Path doesn't exist** | Raise FileNotFoundError | `_navigate()` returns None |
| **Intermediate dirs don't exist** | Create automatically | `add_file()` loop |

**Size Propagation Edge Case:**
> "When overwriting a file, I calculate the SIZE DIFFERENCE, not the new size.
> If old file was 100 bytes and new is 150 bytes, I propagate +50, not +150."

---

### **PHASE 8: Testing Strategy (2-3 minutes)**

```python
import pytest

class TestFileSystem:
    
    def test_add_file_basic(self):
        """File added with correct size."""
        fs = FileSystem()
        fs.add_file("/file.txt", 100)
        
        assert fs.get_size("/file.txt") == 100
        assert fs.get_size("/") == 100
    
    def test_add_file_nested_creates_dirs(self):
        """Nested directories created automatically."""
        fs = FileSystem()
        fs.add_file("/a/b/c/file.txt", 50)
        
        assert fs.exists("/a")
        assert fs.exists("/a/b")
        assert fs.exists("/a/b/c")
        assert fs.is_directory("/a")
        assert fs.is_file("/a/b/c/file.txt")
    
    def test_size_propagation(self):
        """Directory sizes include all descendants."""
        fs = FileSystem()
        fs.add_file("/home/user/file1.txt", 100)
        fs.add_file("/home/user/file2.txt", 200)
        fs.add_file("/home/other/file3.txt", 50)
        
        assert fs.get_size("/home/user") == 300
        assert fs.get_size("/home") == 350
        assert fs.get_size("/") == 350
    
    def test_file_overwrite_size_update(self):
        """Overwriting file updates sizes correctly."""
        fs = FileSystem()
        fs.add_file("/file.txt", 100)
        assert fs.get_size("/") == 100
        
        fs.add_file("/file.txt", 250)  # Overwrite
        assert fs.get_size("/") == 250  # Not 350!
    
    def test_delete_updates_ancestor_sizes(self):
        """Deleting file updates all ancestor sizes."""
        fs = FileSystem()
        fs.add_file("/home/file.txt", 100)
        
        assert fs.get_size("/") == 100
        
        fs.delete_file("/home/file.txt")
        
        assert fs.get_size("/") == 0
        assert fs.get_size("/home") == 0
    
    def test_list_contents_sorted(self):
        """List returns sorted children."""
        fs = FileSystem()
        fs.add_file("/home/zebra.txt", 10)
        fs.add_file("/home/alpha.txt", 10)
        fs.add_file("/home/beta.txt", 10)
        
        contents = fs.list_contents("/home")
        
        assert contents == ["alpha.txt", "beta.txt", "zebra.txt"]
    
    def test_invalid_path_raises(self):
        """Invalid paths raise errors."""
        fs = FileSystem()
        
        with pytest.raises(ValueError):
            fs.add_file("relative/path.txt", 100)  # Not absolute
        
        with pytest.raises(FileNotFoundError):
            fs.get_size("/nonexistent")
    
    def test_cannot_overwrite_dir_with_file(self):
        """Cannot replace directory with file."""
        fs = FileSystem()
        fs.add_file("/home/user/file.txt", 100)  # Creates /home/user
        
        with pytest.raises(ValueError):
            fs.add_file("/home/user", 100)  # user is a dir!
```

---

### **PHASE 9: Complexity Analysis (1 minute)**

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| `add_file` | O(D) | O(D) | D = path depth, propagation |
| `get_size` | O(D) | O(1) | Traversal + O(1) cached lookup |
| `list_contents` | O(D + C) | O(C) | C = num children |
| `delete_file` | O(D) | O(1) | Traversal + propagation |
| `glob` | O(N) | O(M) | N = total nodes, M = matches |

**Why O(1) for size lookup?**
> "After we traverse to the node (O(depth)), the size is already cached.
> No recursion needed. This is the key optimization."

---

### **PHASE 10: Extensions & Follow-ups (5+ minutes)**

#### **Q1: "How would you add thread safety?"**

```python
import threading
from contextlib import contextmanager

class ThreadSafeFileSystem(FileSystem):
    """Thread-safe file system using read-write lock."""
    
    def __init__(self):
        super().__init__()
        self._lock = threading.RLock()
    
    @contextmanager
    def _write_lock(self):
        self._lock.acquire()
        try:
            yield
        finally:
            self._lock.release()
    
    def add_file(self, path: str, size: int) -> bool:
        with self._write_lock():
            return super().add_file(path, size)
    
    def get_size(self, path: str) -> int:
        with self._write_lock():  # Could use read lock
            return super().get_size(path)
```

---

#### **Q2: "How would you add move/rename?"**

```python
def move(self, src_path: str, dest_path: str) -> bool:
    """Move file or directory to new location."""
    src_node = self._navigate(src_path)
    if src_node is None:
        raise FileNotFoundError(f"Source not found: {src_path}")
    
    # Remove from old parent, update old ancestor sizes
    old_parent = src_node.parent
    del old_parent.children[src_node.name]
    
    # Propagate size decrease up old path
    size = src_node.size
    current = old_parent
    while current:
        current.size -= size
        current = current.parent
    
    # Add to new parent, update new ancestor sizes
    # ... similar logic for adding
```

---

#### **Q3: "How would you store actual file content?"**

```python
@dataclass
class FileNode:
    content: bytes = field(default=b"")  # Actual file content
    
    def read(self) -> bytes:
        if not self.is_file:
            raise IsADirectoryError()
        return self.content
    
    def write(self, data: bytes) -> int:
        if not self.is_file:
            raise IsADirectoryError()
        old_size = self.size
        self.content = data
        self.size = len(data)
        # Propagate size change to ancestors
        return self.size - old_size
```

---

## ❌ Common Mistakes (What NOT to Do)

### **MISTAKE 1: O(N) Size Calculation** ❌

```python
# WRONG - Recalculates every time!
def get_size(self, path):
    node = self._navigate(path)
    if node.is_file:
        return node.size
    # O(N) recursive sum every call!
    return sum(self.get_size(child) for child in node.children)

# CORRECT - Cached size
def get_size(self, path):
    node = self._navigate(path)
    return node.size  # Already calculated!
```

---

### **MISTAKE 2: Forgetting Parent Pointer** ❌

```python
# WRONG - Can't propagate sizes upward!
@dataclass
class FileNode:
    name: str
    children: Dict[str, 'FileNode']
    # No parent pointer!

# When adding file, how do we update ancestors?
# Would need to re-traverse from root every time!

# CORRECT - Parent pointer for O(1) upward navigation
@dataclass
class FileNode:
    parent: Optional['FileNode'] = None
```

---

### **MISTAKE 3: Not Handling File Overwrite** ❌

```python
# WRONG - Adds size instead of replacing!
def add_file(self, path, size):
    file_node = FileNode(size=size)
    parent.children[name] = file_node
    # Propagate full size
    self._propagate_size(parent, size)  # Wrong if file existed!

# CORRECT - Calculate difference
old_size = existing_file.size if file_exists else 0
size_delta = new_size - old_size
self._propagate_size(parent, size_delta)
```

---

## 💯 Interview Checklist

- [ ] ✅ **Clarified requirements** (size scope, updates, case sensitivity)
- [ ] ✅ **Explained size caching trade-off** (O(1) read vs O(depth) write)
- [ ] ✅ **Drew tree structure** with size propagation
- [ ] ✅ **Used Composite Pattern** (files/dirs share interface)
- [ ] ✅ **Used parent pointer** for upward propagation
- [ ] ✅ **Handled file overwrite** (size delta, not absolute)
- [ ] ✅ **Implemented path parsing** (split by "/")
- [ ] ✅ **Handled edge cases** (root, relative paths, dir as file)
- [ ] ✅ **Discussed complexity** (O(depth) for operations)
- [ ] ✅ **Mentioned extensions** (thread safety, move, content storage)

---

## 📚 Quick Reference Card

```
┌────────────────────────────────────────────────────────────┐
│                  FILE SYSTEM CHEAT SHEET                   │
├────────────────────────────────────────────────────────────┤
│ KEY INSIGHT:                                              │
│   Cache directory sizes, propagate on add/delete          │
│   Read = O(depth) + O(1), Write = O(depth) + O(depth)    │
│                                                            │
│ DATA STRUCTURE:                                           │
│   FileNode:                                               │
│     - name: str                                           │
│     - is_file: bool                                       │
│     - size: int (CACHED for dirs)                        │
│     - children: Dict[str, FileNode]                      │
│     - parent: FileNode (for upward propagation)          │
│                                                            │
│ DESIGN PATTERN:                                           │
│   Composite: Files and directories share get_size()      │
│                                                            │
│ SIZE PROPAGATION:                                         │
│   add_file: propagate +delta to all ancestors            │
│   delete_file: propagate -size to all ancestors          │
│   overwrite: propagate (new - old) to all ancestors      │
│                                                            │
│ EDGE CASES:                                               │
│   - Require absolute paths (/home/...)                   │
│   - Auto-create intermediate directories                  │
│   - Can't overwrite dir with file                        │
│   - Handle size DIFFERENCE on overwrite                  │
└────────────────────────────────────────────────────────────┘
```

---

**Related LeetCode Problems:**
- LeetCode 588: Design In-Memory File System
- LeetCode 635: Design Log Storage System

