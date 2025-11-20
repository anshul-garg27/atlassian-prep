# 📁 PROBLEM 4: FILE SYSTEM DESIGN

### ⭐⭐⭐⭐ **Design In-Memory File System with O(1) Size**

**Frequency:** MEDIUM-HIGH at Atlassian
**Difficulty:** Medium-Hard
**Focus:** Tree Structures, Caching, Path Parsing

---

## 📋 Problem Statement

Design an in-memory file system that supports:
- `addFile(path, size)`: Add file at given path
- `getSize(path)`: Get total size of directory in O(1) *(after reaching directory)*
- `listFiles(path)`: List all files/directories at path
- Support wildcard patterns (optional)

**Key Challenge:** Propagate size updates to all parent directories

---

## 🎨 Visual Example

```text
/
├── home/
│   ├── alice/
│   │   ├── docs/
│   │   │   └── file1.txt (100 bytes)
│   │   └── pics/
│   │       └── photo.jpg (500 bytes)
│   └── bob/
│       └── code.py (200 bytes)
└── tmp/
    └── temp.log (50 bytes)

getSize("/home/alice") → 600 bytes
getSize("/home") → 800 bytes
getSize("/") → 850 bytes
```

---

## 💻 Implementation

```java
class FileNode {
    String name;
    boolean isFile;
    long size; // For files: actual size, For dirs: cached total
    Map<String, FileNode> children;
    
    public FileNode(String name, boolean isFile) {
        this.name = name;
        this.isFile = isFile;
        this.size = 0;
        this.children = isFile ? null : new HashMap<>();
    }
}

class FileSystem {
    private FileNode root;
    
    public FileSystem() {
        root = new FileNode("/", false);
    }
    
    public void addFile(String path, long fileSize) {
        String[] parts = path.split("/");
        FileNode current = root;
        List<FileNode> ancestors = new ArrayList<>();
        
        // Navigate to file location
        for (int i = 1; i < parts.length - 1; i++) {
            String dirName = parts[i];
            if (!current.children.containsKey(dirName)) {
                current.children.put(dirName, new FileNode(dirName, false));
            }
            ancestors.add(current);
            current = current.children.get(dirName);
        }
        
        // Add file
        String fileName = parts[parts.length - 1];
        FileNode fileNode = new FileNode(fileName, true);
        fileNode.size = fileSize;
        current.children.put(fileName, fileNode);
        
        // Propagate size to ancestors
        current.size += fileSize;
        for (FileNode ancestor : ancestors) {
            ancestor.size += fileSize;
        }
    }
    
    public long getSize(String path) {
        FileNode node = navigate(path);
        return node != null ? node.size : -1;
    }
    
    public List<String> listFiles(String path) {
        FileNode node = navigate(path);
        if (node == null || node.isFile) {
            return new ArrayList<>();
        }
        return new ArrayList<>(node.children.keySet());
    }
    
    private FileNode navigate(String path) {
        String[] parts = path.split("/");
        FileNode current = root;
        
        for (int i = 1; i < parts.length; i++) {
            if (parts[i].isEmpty()) continue;
            if (!current.children.containsKey(parts[i])) {
                return null;
            }
            current = current.children.get(parts[i]);
        }
        return current;
    }
}
```

---

## 🚀 Follow-ups

**Q: Support file deletion?**
```java
public boolean deleteFile(String path) {
    // Navigate to parent, remove file, propagate negative size
}
```

**Q: Support wildcard matching?**
```java
// Use regex or pattern matching library
public List<String> glob(String pattern) {
    // e.g., "/home/*/*.txt"
}
```

**Q: Thread safety?**
```java
private final ReadWriteLock lock = new ReentrantReadWriteLock();

public void addFile(String path, long size) {
    lock.writeLock().lock();
    try {
        // ... implementation
    } finally {
        lock.writeLock().unlock();
    }
}
```

---

## 📊 Complexity

| Operation | Time | Space |
|-----------|------|-------|
| addFile | O(depth) | O(depth) |
| getSize | O(depth) | O(1) |
| listFiles | O(depth + N) | O(N) |

---

## 💡 Interview Tips

✅ Discuss trade-offs: cached size vs on-demand calculation
✅ Handle edge cases: root path "/", empty paths
✅ Mention thread safety (ReadWriteLock)
✅ Ask about wildcard patterns
✅ Discuss file updates (size changes)

**Related:** LeetCode 588, LeetCode 635
