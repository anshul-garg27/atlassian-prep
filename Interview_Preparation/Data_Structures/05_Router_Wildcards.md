# 🛣️ PROBLEM 5: DYNAMIC ROUTE MATCHING WITH WILDCARDS

### ⭐⭐⭐ **Middleware Router**

**Frequency:** Low-Medium (Appears in ~25% of rounds)
**Similar to:** [LeetCode 208. Implement Trie (Prefix Tree)](https://leetcode.com/problems/implement-trie-prefix-tree/) (but for path segments)

**Problem Statement:**
> Implement a router that matches URL paths.
> - Paths consist of segments separated by `/` (e.g., `/foo/bar`).
> - Support **wildcards** (`*`) which match exactly one segment.
> - Support adding routes and calling routes.

**Visual Example:**
```text
Routes Added:
1. /foo/bar      -> Result: "A"
2. /foo/*/baz    -> Result: "B"

Trie Structure:
root
 └─ "foo"
     ├─ "bar" -> (Result "A")
     └─ "*"   -> "baz" -> (Result "B")

Query: /foo/xyz/baz
Path: root -> "foo" -> "xyz"? (No) -> "*" (Yes, matches "xyz") -> "baz" (Yes) -> Result "B"
```

**Example Usage:**
```python
router = Router()

router.addRoute("/foo", "foo")
router.addRoute("/bar/*/baz", "bar")

print(router.callRoute("/bar/anything/baz"))  # "bar"
print(router.callRoute("/bar/xyz/baz"))       # "bar"
print(router.callRoute("/foo"))                # "foo"
print(router.callRoute("/unknown"))            # None
```

---

### 🗣️ **Interview Conversation Guide**

**Phase 1: Clarification**
- **Candidate:** "Does `*` match multiple segments (like `/**` in some frameworks) or just one?"
- **Interviewer:** "Just one segment."
- **Candidate:** "If we have `/foo/bar` and `/foo/*`, which one takes precedence?"
- **Interviewer:** "Exact matches should have higher priority than wildcards."
- **Candidate:** "Are paths case sensitive?"
- **Interviewer:** "Yes."

**Phase 2: Approach**
- **Candidate:** "Since we are matching prefixes and segments, a **Trie (Prefix Tree)** is the perfect data structure."
- **Candidate:** "Instead of characters, each Trie Node will store a path segment (string)."
- **Candidate:** "When adding a route, we split by `/` and insert nodes."
- **Candidate:** "When searching, we traverse. If an exact match is not found, we check if a `*` child exists."

**Phase 3: Coding**
- Define `TrieNode`.
- Implement `addRoute` (iterative).
- Implement `callRoute` (recursive/DFS to handle backtracking if needed, though iterative often works if priority is simple).

---

### 📝 **Solution Approach: Trie (Prefix Tree)**

Instead of storing characters (like a standard Dictionary Trie), we store **path segments** as nodes.

**Data Structure:**
*   `TrieNode`:
    *   `children`: Map `segment_string` -> `TrieNode`
    *   `is_wildcard`: Boolean (or store `*` in children)
    *   `result`: Value to return if this node is a valid endpoint.

**Algorithm:**
*   **Add Route**: Split path by `/`. Traverse/Create nodes.
*   **Call Route**: Split path. Recursive Search (DFS).
    *   If exact match found in `children`, go there.
    *   If `*` exists in `children`, also try that (backtracking might be needed if we want to find *any* match, or specific priority).

**Implementation:**

```python
class TrieNode:
    def __init__(self):
        self.children = {}  # segment -> TrieNode
        self.result = None  # Not None means this is an endpoint

class Router:
    def __init__(self):
        self.root = TrieNode()

    def addRoute(self, path: str, result: str) -> None:
        # Split path, filtering empty strings (caused by leading /)
        segments = [s for s in path.split('/') if s]
        
        node = self.root
        for segment in segments:
            if segment == '*':
                if '*' not in node.children:
                    node.children['*'] = TrieNode()
                node = node.children['*']
            else:
                if segment not in node.children:
                    node.children[segment] = TrieNode()
                node = node.children[segment]
        
        node.result = result

    def callRoute(self, path: str) -> str:
        segments = [s for s in path.split('/') if s]
        return self._search(self.root, segments, 0)

    def _search(self, node: TrieNode, segments: list, index: int) -> str:
        # Base Case: End of path
        if index == len(segments):
            return node.result

        segment = segments[index]

        # Strategy: Try Exact Match FIRST, then Wildcard
        
        # 1. Try Exact Match
        if segment in node.children:
            res = self._search(node.children[segment], segments, index + 1)
            if res is not None:
                return res

        # 2. Try Wildcard Match
        if '*' in node.children:
            res = self._search(node.children['*'], segments, index + 1)
            if res is not None:
                return res

        return None

# Time Complexity:
# addRoute: O(K), K = number of segments
# callRoute: O(K) in best case (direct match), O(2^K) worst case if every node has both exact and wildcard and we backtrack (rare in URLs).
```

---

### 🔄 **Follow-up 1: Priority Rules**

**Problem:**
> What if both `/foo/bar` and `/foo/*` exist? Which one should `/foo/bar` match?
> **Rule:** Exact match > Wildcard match.

**Solution:**
> The DFS order naturally handles this.
> We check `if segment in node.children` (Exact) **before** checking `*`.
> If the Exact path leads to a dead end (no result), we backtrack and try Wildcard.

---

### 🔄 **Follow-up 2: Path Parameters**

**Problem:**
> Support routes like `/users/{id}/posts` where `{id}` captures any value, and we need to return the captured params.

**Solution:**
> 1.  Modify `addRoute` to detect `{...}` segments. Treat them like wildcards but store the param name.
> 2.  Modify `callRoute` to return `(result, params_dict)`.
> 3.  During DFS, if we take a parameter/wildcard edge, add `param_name: current_segment` to the collected params.

```python
class ParamRouter:
    # ... (TrieNode has self.param_name = None) ...

    def addRoute(self, path, result):
        # ... inside loop ...
        if segment.startswith('{') and segment.endswith('}'):
            param_name = segment[1:-1]
            if '*' not in node.children:
                node.children['*'] = TrieNode()
                node.children['*'].param_name = param_name
            node = node.children['*']
        # ...

    def callRoute(self, path):
        return self._dfs(self.root, segments, 0, {})

    def _dfs(self, node, segments, index, params):
        if index == len(segments):
            return (node.result, params) if node.result else None

        current_seg = segments[index]

        # 1. Try Exact
        if current_seg in node.children:
            res = self._dfs(node.children[current_seg], segments, index+1, params)
            if res: return res

        # 2. Try Param/Wildcard
        if '*' in node.children:
            child = node.children['*']
            # Copy params to avoid polluting other branches if backtracking
            new_params = params.copy()
            if child.param_name:
                new_params[child.param_name] = current_seg
            
            res = self._dfs(child, segments, index+1, new_params)
            if res: return res
            
        return None
```

---

### 🧪 **Test Cases**

**Basic:**
- Add `/a/b`, Call `/a/b` -> Found.
- Call `/a/c` -> None.

**Wildcard:**
- Add `/a/*/c`. Call `/a/b/c` -> Found.
- Call `/a/b/d` -> None.

**Priority:**
- Add `/a/b` (Exact) and `/a/*` (Wildcard).
- Call `/a/b` -> Should return Exact match result.
- Call `/a/z` -> Should return Wildcard match result.

**Edge Cases:**
- Root path `/`.
- Path with trailing slash (handle by splitting logic).
- Empty segments `//` (handle by filtering).
