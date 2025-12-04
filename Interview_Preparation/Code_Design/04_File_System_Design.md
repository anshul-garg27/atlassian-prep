# 📁 PROBLEM 4: FILE SYSTEM DESIGN

### ⭐⭐⭐⭐ **Design In-Memory File System with O(1) Size Lookup**

**Frequency:** MEDIUM-HIGH at Atlassian
**Difficulty:** Medium-Hard
**Focus:** Tree Structures, Size Caching, Path Parsing

---

## 📋 Problem Statement

Design an in-memory file system that supports:
- `add_file(path, size)`: Add file at given path
- `get_size(path)`: Get total size of directory in O(1) *(after reaching directory)*
- `list_contents(path)`: List all files/directories at path
- Optional: Support wildcard patterns (`*.txt`, `/home/*/*.py`)

**Key Challenge:** Propagate size updates to all parent directories for O(1) size lookups.

**Constraints:**
- Path format: `/home/user/file.txt`
- File sizes: positive integers
- Directory sizes: sum of all descendant files
- Support nested directories of any depth

---

## 🎤 How to Explain in Interview

### **Opening Statement (30 seconds)**
> "I'll design an in-memory file system using a **tree structure** where each node is either a file or directory. For O(1) size lookups, I'll **cache sizes** at each directory and **propagate updates** to ancestors when files are added."

### **Key Points to Mention:**
1. "Using **tree data structure** - natural for hierarchical file systems"
2. "**Caching directory sizes** for O(1) lookup (trade-off: O(depth) on add)"
3. "**Path parsing** splits `/home/user/file.txt` into components"
4. "**Composite Pattern** - files and directories share common interface"

---

## 🎨 Visual Example

```text
/
├── home/                      (size: 800)
│   ├── alice/                 (size: 600)
│   │   ├── docs/              (size: 100)
│   │   │   └── file1.txt      (100 bytes)
│   │   └── pics/              (size: 500)
│   │       └── photo.jpg      (500 bytes)
│   └── bob/                   (size: 200)
│       └── code.py            (200 bytes)
└── tmp/                       (size: 50)
    └── temp.log               (50 bytes)

Operations:
get_size("/home/alice") → 600 bytes   # O(depth) to reach, O(1) to return
get_size("/home") → 800 bytes
get_size("/") → 850 bytes
list_contents("/home") → ["alice", "bob"]
```

---

## 🎯 Design Patterns Used

### **1. Composite Pattern** ⭐⭐⭐
Files and directories share common interface for uniform treatment.

```python
from abc import ABC, abstractmethod

class FileSystemNode(ABC):
    """Abstract base for files and directories."""
    
    @abstractmethod
    def get_size(self) -> int:
        pass
    
    @abstractmethod
    def is_file(self) -> bool:
        pass

class File(FileSystemNode):
    def get_size(self) -> int:
        return self.size
    
    def is_file(self) -> bool:
        return True

class Directory(FileSystemNode):
    def get_size(self) -> int:
        return self._cached_size  # O(1)
    
    def is_file(self) -> bool:
        return False
```

### **2. Tree Structure**
Natural representation for hierarchical data.

```text
Node
├── name: str
├── is_file: bool
├── size: int (cached for directories)
└── children: Dict[str, Node]  (only for directories)
```

---

## 🏗️ Class Design

```text
┌─────────────────────────┐
│      FileSystem         │  ← Main facade
├─────────────────────────┤
│ - root: FileNode        │
├─────────────────────────┤
│ + add_file(path, size)  │
│ + get_size(path)        │
│ + list_contents(path)   │
│ + delete_file(path)     │
│ + move_file(src, dest)  │
└─────────────────────────┘
            │
            │ contains
            ▼
┌─────────────────────────┐
│       FileNode          │
├─────────────────────────┤
│ - name: str             │
│ - is_file: bool         │
│ - size: int             │
│ - children: Dict        │
│ - parent: FileNode      │  ← For size propagation
└─────────────────────────┘
```

---

## 💻 Python Implementation (Production-Ready)

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
- list_contents: O(depth) for traversal

Space Complexity: O(total_nodes)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from pathlib import PurePosixPath
import fnmatch


@dataclass
class FileNode:
    """
    Node in the file system tree.
    
    Represents either a file or directory.
    Directories cache their total size for O(1) lookup.
    
    Attributes:
        name: File/directory name
        is_file: True if file, False if directory
        size: File size (for files) or cached total size (for directories)
        children: Child nodes (only for directories)
        parent: Parent node (for size propagation)
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
    
    Example:
        >>> fs = FileSystem()
        >>> fs.add_file("/home/user/doc.txt", 100)
        >>> fs.get_size("/home/user")  # 100
        >>> fs.get_size("/home")  # 100
        >>> fs.list_contents("/home")  # ["user"]
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
            
        Raises:
            ValueError: If path is invalid or file_size is negative
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
        
        # If file already exists, calculate size difference
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
        
        # Propagate size change to all ancestors
        size_delta = file_size - old_size
        for ancestor in ancestors:
            ancestor.size += size_delta
        
        return True
    
    def get_size(self, path: str) -> int:
        """
        Get total size of file or directory.
        
        Args:
            path: Absolute path
            
        Returns:
            Size in bytes (cached for directories - O(1) after traversal)
            
        Raises:
            FileNotFoundError: If path doesn't exist
        """
        node = self._navigate(path)
        if node is None:
            raise FileNotFoundError(f"Path not found: {path}")
        return node.size
    
    def list_contents(self, path: str) -> List[str]:
        """
        List contents of a directory.
        
        Args:
            path: Absolute path to directory
            
        Returns:
            List of file/directory names
            
        Raises:
            FileNotFoundError: If path doesn't exist
            NotADirectoryError: If path is a file
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
        
        Args:
            path: Absolute path to file
            
        Returns:
            True if deleted successfully
        """
        parts = self._parse_path(path)
        if not parts:
            raise ValueError("Cannot delete root")
        
        # Navigate to parent
        parent = self._navigate("/".join([""] + parts[:-1]) or "/")
        if parent is None:
            raise FileNotFoundError(f"Parent directory not found")
        
        file_name = parts[-1]
        if file_name not in parent.children:
            raise FileNotFoundError(f"File not found: {path}")
        
        file_node = parent.children[file_name]
        if not file_node.is_file:
            raise IsADirectoryError(f"Cannot delete directory with delete_file: {path}")
        
        # Propagate size decrease to ancestors
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
        Supports wildcards: * matches any characters, ? matches single char.
        
        Args:
            pattern: Pattern like "/home/*/*.txt"
            
        Returns:
            List of matching paths
        """
        results = []
        self._glob_recursive(self.root, "", pattern, results)
        return sorted(results)
    
    def _glob_recursive(self, node: FileNode, current_path: str, 
                        pattern: str, results: List[str]) -> None:
        """Recursive helper for glob matching."""
        for name, child in node.children.items():
            child_path = f"{current_path}/{name}"
            
            if child.is_file:
                if fnmatch.fnmatch(child_path, pattern):
                    results.append(child_path)
            else:
                # Check if pattern could match in this subtree
                if fnmatch.fnmatch(child_path, pattern):
                    results.append(child_path)
                # Continue searching
                self._glob_recursive(child, child_path, pattern, results)
    
    def _parse_path(self, path: str) -> List[str]:
        """
        Parse path into components.
        "/home/user/file.txt" → ["home", "user", "file.txt"]
        """
        if path == "/":
            return []
        return [p for p in path.split("/") if p]
    
    def _navigate(self, path: str) -> Optional[FileNode]:
        """
        Navigate to node at given path.
        
        Args:
            path: Absolute path
            
        Returns:
            FileNode at path, or None if not found
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


# ============ Demo / Usage ============
if __name__ == "__main__":
    print("=== In-Memory File System Demo ===\n")
    
    fs = FileSystem()
    
    # Add files
    fs.add_file("/home/alice/docs/file1.txt", 100)
    fs.add_file("/home/alice/pics/photo.jpg", 500)
    fs.add_file("/home/bob/code.py", 200)
    fs.add_file("/tmp/temp.log", 50)
    
    print("File System Structure:")
    fs.print_tree()
    
    print("\n" + "=" * 50)
    print("SIZE QUERIES (O(1) after reaching node)")
    print("=" * 50)
    print(f"get_size('/home/alice') = {fs.get_size('/home/alice')} bytes")
    print(f"get_size('/home') = {fs.get_size('/home')} bytes")
    print(f"get_size('/') = {fs.get_size('/')} bytes")
    
    print("\n" + "=" * 50)
    print("LIST CONTENTS")
    print("=" * 50)
    print(f"list_contents('/home') = {fs.list_contents('/home')}")
    print(f"list_contents('/home/alice') = {fs.list_contents('/home/alice')}")
    
    print("\n" + "=" * 50)
    print("GLOB PATTERNS")
    print("=" * 50)
    print(f"glob('*.txt') = {fs.glob('*.txt')}")
    print(f"glob('/home/*/*.py') = {fs.glob('/home/*/*.py')}")
    
    print("\n" + "=" * 50)
    print("DELETE FILE")
    print("=" * 50)
    print(f"Size before delete: {fs.get_size('/home/alice')}")
    fs.delete_file("/home/alice/docs/file1.txt")
    print(f"Size after delete: {fs.get_size('/home/alice')}")
```

---

## 🚀 Extensions & Follow-ups

### **Extension 1: Thread Safety**
```python
import threading
from contextlib import contextmanager

class ThreadSafeFileSystem(FileSystem):
    """Thread-safe file system using ReadWriteLock."""
    
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

### **Extension 2: Move/Rename Operations**
```python
def move(self, src_path: str, dest_path: str) -> bool:
    """Move file or directory to new location."""
    # Get source node
    src_node = self._navigate(src_path)
    if src_node is None:
        raise FileNotFoundError(f"Source not found: {src_path}")
    
    # Remove from old parent, update sizes
    # Add to new parent, update sizes
    # ... implementation
```

### **Extension 3: File Content Storage**
```python
@dataclass
class FileNode:
    content: bytes = field(default=b"")  # Actual file content
    
    def read(self) -> bytes:
        return self.content
    
    def write(self, data: bytes) -> int:
        self.content = data
        self.size = len(data)
        return self.size
```

---

## 🧪 Testing Strategy

```python
import pytest

class TestFileSystem:
    
    def test_add_file_basic(self):
        """File added with correct size."""
        fs = FileSystem()
        fs.add_file("/file.txt", 100)
        
        assert fs.get_size("/file.txt") == 100
        assert fs.get_size("/") == 100
    
    def test_add_file_nested(self):
        """Nested directories created automatically."""
        fs = FileSystem()
        fs.add_file("/a/b/c/file.txt", 50)
        
        assert fs.exists("/a")
        assert fs.exists("/a/b")
        assert fs.exists("/a/b/c")
        assert fs.get_size("/a/b/c/file.txt") == 50
    
    def test_size_propagation(self):
        """Directory sizes include all descendants."""
        fs = FileSystem()
        fs.add_file("/home/user/file1.txt", 100)
        fs.add_file("/home/user/file2.txt", 200)
        fs.add_file("/home/other/file3.txt", 50)
        
        assert fs.get_size("/home/user") == 300
        assert fs.get_size("/home") == 350
        assert fs.get_size("/") == 350
    
    def test_list_contents(self):
        """List returns direct children only."""
        fs = FileSystem()
        fs.add_file("/home/user1/file.txt", 100)
        fs.add_file("/home/user2/file.txt", 100)
        
        contents = fs.list_contents("/home")
        
        assert contents == ["user1", "user2"]
    
    def test_delete_updates_size(self):
        """Deleting file updates ancestor sizes."""
        fs = FileSystem()
        fs.add_file("/home/file.txt", 100)
        
        assert fs.get_size("/") == 100
        
        fs.delete_file("/home/file.txt")
        
        assert fs.get_size("/") == 0
    
    def test_invalid_path(self):
        """Invalid paths raise errors."""
        fs = FileSystem()
        
        with pytest.raises(ValueError):
            fs.add_file("relative/path.txt", 100)  # Not absolute
        
        with pytest.raises(FileNotFoundError):
            fs.get_size("/nonexistent")
```

---

## 📊 Complexity Analysis

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| `add_file` | O(D) | O(D) | D = path depth |
| `get_size` | O(D) | O(1) | Traversal + O(1) cached lookup |
| `list_contents` | O(D + N) | O(N) | N = num children |
| `delete_file` | O(D) | O(1) | Traversal + size propagation |
| `glob` | O(N) | O(M) | N = total nodes, M = matches |

**Space Complexity:** O(total_files + total_directories)

---

## ⚠️ Edge Cases

| Edge Case | How to Handle |
|-----------|---------------|
| **Root path "/"** | Special handling - cannot add file at root |
| **Empty path** | Raise `ValueError` |
| **Relative path** | Raise `ValueError` - require absolute |
| **File overwrite** | Update size, propagate difference |
| **Directory as file** | Raise error if trying to treat dir as file |
| **Delete non-empty dir** | Either refuse or implement recursive delete |

---

## 💯 Interview Checklist

Before finishing, ensure you've mentioned:
- [ ] ✅ **Tree structure** - natural for hierarchical data
- [ ] ✅ **Cached directory sizes** - O(1) lookup
- [ ] ✅ **Size propagation** - update ancestors on add/delete
- [ ] ✅ **Path parsing** - split into components
- [ ] ✅ **Composite Pattern** - files and dirs share interface
- [ ] ✅ **Thread safety** mention (locks)
- [ ] ✅ **Wildcard support** (glob patterns)
- [ ] ✅ **Testing strategy**

---

**Related LeetCode Problems:**
- LeetCode 588: Design In-Memory File System
- LeetCode 635: Design Log Storage System
