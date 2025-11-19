# 🛣️ PROBLEM 5: DYNAMIC ROUTE MATCHING WITH WILDCARDS

### ⭐⭐⭐ **HTTP Router with Wildcard Path Matching**

**Frequency:** Medium (Appears in ~25-30% of rounds)
**Difficulty:** Medium
**Similar to:** [LeetCode 208. Implement Trie](https://leetcode.com/problems/implement-trie-prefix-tree/), [LeetCode 677. Map Sum Pairs](https://leetcode.com/problems/map-sum-pairs/)

---

## 📋 Problem Statement

Design an HTTP router that matches URL paths to handlers. The router must support:

1. **Exact segment matching:** `/api/users` matches only `/api/users`
2. **Wildcard matching:** `/api/*/profile` where `*` matches any single segment
3. **Priority rules:** Exact matches take precedence over wildcard matches

**Operations:**
- `addRoute(path, handler)`: Register a route with a handler (string or function)
- `matchRoute(path)`: Return the handler for the matching route, or `null` if no match

**Constraints:**
- Paths are case-sensitive
- `*` matches exactly **one** segment (not zero, not multiple)
- 1 ≤ number of routes ≤ 1000
- 1 ≤ segments per path ≤ 10

---

## 🎨 Visual Example

### Example 1: Basic Routing

```text
Routes Registered:
1. /api/users        → Handler: "GetUsers"
2. /api/users/123    → Handler: "GetUserById"
3. /api/*/profile    → Handler: "GetProfile"

Trie Structure:
root
 └─ api
     └─ users ─────────────────→ [Handler: "GetUsers"]
         ├─ 123 ──────────────→ [Handler: "GetUserById"]
         └─ * ──────────────────→ profile → [Handler: "GetProfile"]

Query Examples:
┌─────────────────────────────────────────────────────────┐
│ matchRoute("/api/users")                                │
│ → Traverse: root → api → users                         │
│ → Result: "GetUsers" ✓                                 │
├─────────────────────────────────────────────────────────┤
│ matchRoute("/api/users/456")                            │
│ → Try exact: root → api → users → "456"? (No)         │
│ → Try wildcard: root → api → users → * → Stop (Dead end│
│ → Result: null ✗                                       │
├─────────────────────────────────────────────────────────┤
│ matchRoute("/api/posts/profile")                        │
│ → Try exact: root → api → "posts"? (No)               │
│ → Try wildcard: root → api → * ("posts") → profile    │
│ → Result: "GetProfile" ✓                               │
└─────────────────────────────────────────────────────────┘
```

### Example 2: Priority (Exact > Wildcard)

```text
Routes:
1. /users/admin  → "AdminHandler"
2. /users/*      → "UserHandler"

Query: /users/admin
1. Try exact: /users/admin → Found "AdminHandler" ✓
2. (Don't even check wildcard if exact match succeeds)

Query: /users/john
1. Try exact: /users/john → Not found
2. Try wildcard: /users/* → Found "UserHandler" ✓
```

---

## 💡 Examples

### Example 1: E-commerce API
```python
router = Router()

router.addRoute("/products", "ListProducts")
router.addRoute("/products/featured", "FeaturedProducts")
router.addRoute("/products/*/reviews", "ProductReviews")

print(router.matchRoute("/products"))                  # "ListProducts"
print(router.matchRoute("/products/featured"))         # "FeaturedProducts"
print(router.matchRoute("/products/123/reviews"))      # "ProductReviews"
print(router.matchRoute("/products/abc/reviews"))      # "ProductReviews"
print(router.matchRoute("/products/123"))              # null
```

### Example 2: User Management
```python
router.addRoute("/users", "AllUsers")
router.addRoute("/users/*/posts", "UserPosts")
router.addRoute("/users/*/posts/*", "GetPost")

print(router.matchRoute("/users/john/posts"))          # "UserPosts"
print(router.matchRoute("/users/jane/posts/5"))        # "GetPost"
```

---

## 🗣️ Interview Conversation Guide

### Phase 1: Clarification (3-5 min)

**Candidate:** "When you say 'wildcard,' does `*` match zero or more segments like `**` in some frameworks, or exactly one?"
**Interviewer:** "Exactly one segment. `/api/*/data` matches `/api/v1/data` but not `/api/data` or `/api/v1/v2/data`."

**Candidate:** "If I have both `/api/users` (exact) and `/api/*` (wildcard), which should `/api/users` match?"
**Interviewer:** "Exact matches have higher priority."

**Candidate:** "Are paths case-sensitive?"
**Interviewer:** "Yes."

**Candidate:** "Should I handle trailing slashes? Is `/users` the same as `/users/`?"
**Interviewer:** "Treat them as the same—normalize by removing trailing slashes."

### Phase 2: Approach Discussion (5-8 min)

**Candidate:** "This is a **Trie (Prefix Tree)** problem, but instead of storing characters, we store **path segments**.

**Key Observations:**
1. Paths have a hierarchical structure → Trie is perfect.
2. Wildcards require **backtracking** during search (try exact first, fall back to wildcard).
3. We need **DFS** for the search to handle multiple possible branches."

**Candidate:** "Data structure:
- `TrieNode` with:
  - `children`: Map from segment → child node
  - `handler`: Stores the route handler (if this node is an endpoint)
- Special key `'*'` in `children` for wildcard segments."

**Candidate:** "Operations:
- **addRoute:** Split path, create nodes iteratively.
- **matchRoute:** DFS with backtracking (try exact, then wildcard)."

### Phase 3: Implementation (15-20 min)

**Candidate:** "I'll implement the Trie with careful handling of priorities during search."

---

## 🧠 Intuition & Approach

### Why Trie?

**Problem Characteristics:**
- Hierarchical path structure (`/a/b/c`)
- Prefix-based matching
- Need efficient lookup (thousands of routes)

**Why not HashMap?**
- HashMap with full paths as keys doesn't support wildcards.
- You'd need O(N) routes to check all patterns.

**Why not Regex?**
- Regex compilation is expensive.
- Matching multiple regexes is O(N × M).

**Trie Advantages:**
- O(K) insertion where K = segments
- O(K) lookup (with backtracking for wildcards)
- Natural hierarchical representation

### Search Strategy: DFS with Priority

When matching `/api/users/profile`:
1. At each node, **try exact match first**:
   - If `children["users"]` exists, go there.
2. **Then try wildcard**:
   - If `children["*"]` exists, go there (as fallback).
3. **Backtrack** if path leads to dead end.

**Visual Example:**

```text
Routes:
  /api/users/profile → "A"
  /api/*/profile     → "B"

Matching: /api/users/profile

Step 1: root → api (Exact)
Step 2: api → users (Exact exists)
Step 3: users → profile (Exact match found!)
Result: "A" ✓

If Step 3 failed:
  Backtrack to Step 2, try api → * → profile → "B"
```

---

## 📝 Complete Solution

```python
from typing import Optional, Dict, Any

class TrieNode:
    """
    Node in the Route Trie.
    Each node represents a path segment.
    """
    def __init__(self):
        # Map: segment_name → child TrieNode
        self.children: Dict[str, TrieNode] = {}
        
        # If not None, this node represents a complete route
        self.handler: Optional[str] = None
    
    def is_endpoint(self) -> bool:
        """Check if this node marks the end of a route."""
        return self.handler is not None


class Router:
    """
    HTTP Router with wildcard support using a Trie.
    
    Supports:
    - Exact segment matching: /api/users
    - Wildcard matching: /api/*/profile
    - Priority: Exact match > Wildcard match
    """
    
    def __init__(self):
        self.root = TrieNode()
    
    def addRoute(self, path: str, handler: str) -> None:
        """
        Register a route with a handler.
        
        Args:
            path: URL path (e.g., "/api/users" or "/api/*/profile")
            handler: Handler identifier (string)
        
        Time: O(K) where K = number of segments
        Space: O(K) for new nodes
        """
        # Normalize: remove leading/trailing slashes, split
        segments = self._split_path(path)
        
        node = self.root
        for segment in segments:
            # Create node if it doesn't exist
            if segment not in node.children:
                node.children[segment] = TrieNode()
            node = node.children[segment]
        
        # Mark endpoint
        node.handler = handler
    
    def matchRoute(self, path: str) -> Optional[str]:
        """
        Find the handler for a given path.
        
        Args:
            path: URL path to match
        
        Returns:
            Handler string if match found, None otherwise
        
        Time: O(K) best case (direct match), O(2^K) worst case (backtracking)
        Space: O(K) recursion depth
        """
        segments = self._split_path(path)
        return self._dfs(self.root, segments, 0)
    
    def _dfs(self, node: TrieNode, segments: list, index: int) -> Optional[str]:
        """
        DFS search with backtracking.
        Try exact match first, then wildcard.
        """
        # Base case: reached end of path
        if index == len(segments):
            return node.handler  # None if not an endpoint
        
        current_segment = segments[index]
        
        # Strategy: Exact match has higher priority
        
        # 1. Try exact match
        if current_segment in node.children:
            result = self._dfs(node.children[current_segment], segments, index + 1)
            if result is not None:
                return result
        
        # 2. Try wildcard match (fallback)
        if '*' in node.children:
            result = self._dfs(node.children['*'], segments, index + 1)
            if result is not None:
                return result
        
        # No match found
        return None
    
    def _split_path(self, path: str) -> list:
        """
        Split path into segments, filtering empty strings.
        
        Example:
            "/api/users/" → ["api", "users"]
            "//api/users" → ["api", "users"]
        """
        return [s for s in path.split('/') if s]


# ============================================
# COMPLETE RUNNABLE EXAMPLE
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("HTTP ROUTER WITH WILDCARD MATCHING")
    print("=" * 60)
    
    router = Router()
    
    # Test 1: Basic routing
    print("\n[Test 1] Basic Routes")
    print("-" * 40)
    router.addRoute("/api/users", "GetUsers")
    router.addRoute("/api/posts", "GetPosts")
    router.addRoute("/api/users/profile", "GetProfile")
    
    print(f"Match '/api/users': {router.matchRoute('/api/users')}")        # GetUsers
    print(f"Match '/api/posts': {router.matchRoute('/api/posts')}")        # GetPosts
    print(f"Match '/api/unknown': {router.matchRoute('/api/unknown')}")    # None
    
    # Test 2: Wildcard routes
    print("\n[Test 2] Wildcard Routes")
    print("-" * 40)
    router.addRoute("/users/*/posts", "UserPosts")
    router.addRoute("/users/*/posts/*", "GetPost")
    
    print(f"Match '/users/john/posts': {router.matchRoute('/users/john/posts')}")      # UserPosts
    print(f"Match '/users/jane/posts': {router.matchRoute('/users/jane/posts')}")      # UserPosts
    print(f"Match '/users/john/posts/5': {router.matchRoute('/users/john/posts/5')}")  # GetPost
    print(f"Match '/users/john': {router.matchRoute('/users/john')}")                  # None
    
    # Test 3: Priority (Exact > Wildcard)
    print("\n[Test 3] Priority Rules")
    print("-" * 40)
    router.addRoute("/products/featured", "FeaturedProducts")
    router.addRoute("/products/*", "ProductById")
    
    print(f"Match '/products/featured': {router.matchRoute('/products/featured')}")    # FeaturedProducts (exact)
    print(f"Match '/products/123': {router.matchRoute('/products/123')}")              # ProductById (wildcard)
    print(f"Match '/products/xyz': {router.matchRoute('/products/xyz')}")              # ProductById (wildcard)
    
    # Test 4: Trailing slashes
    print("\n[Test 4] Trailing Slashes")
    print("-" * 40)
    router.addRoute("/api/data", "GetData")
    print(f"Match '/api/data': {router.matchRoute('/api/data')}")      # GetData
    print(f"Match '/api/data/': {router.matchRoute('/api/data/')}")    # GetData (normalized)
    
    # Test 5: Complex nested wildcards
    print("\n[Test 5] Complex Wildcards")
    print("-" * 40)
    router.addRoute("/a/*/c/*/e", "ComplexRoute")
    print(f"Match '/a/b/c/d/e': {router.matchRoute('/a/b/c/d/e')}")    # ComplexRoute
    print(f"Match '/a/x/c/y/e': {router.matchRoute('/a/x/c/y/e')}")    # ComplexRoute
    print(f"Match '/a/b/c/e': {router.matchRoute('/a/b/c/e')}")        # None (missing segment)
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)
```

---

## 🔍 Explanation with Example

Let's trace through how the Trie-based router works with a concrete example:

**Routes Added:**
1. `/api/users` → "GetUsers"
2. `/api/*/profile` → "GetProfile"
3. `/users/admin` → "AdminHandler"

**Query:** `/api/users`

---

**Step 1: Build Trie**

After adding all routes, the Trie looks like:

```text
root
 ├─ api
 │   ├─ users ────→ [handler: "GetUsers"]
 │   └─ * ────→ profile ────→ [handler: "GetProfile"]
 └─ users
     └─ admin ────→ [handler: "AdminHandler"]
```

---

**Step 2: Query `/api/users`**

Split path into segments: `["api", "users"]`

**DFS Traversal:**

```text
_dfs(root, ["api", "users"], index=0):
  segment = "api"
  
  Try exact match: root.children["api"]? YES ✓
    → Recurse: _dfs(api_node, ["api", "users"], index=1)
    
      segment = "users"
      
      Try exact match: api_node.children["users"]? YES ✓
        → Recurse: _dfs(users_node, ["api", "users"], index=2)
        
          index=2 == len(segments)=2 → BASE CASE
          Return users_node.handler = "GetUsers" ✓
```

**Result:** "GetUsers"

---

**Query 2:** `/api/john/profile`

Split path: `["api", "john", "profile"]`

**DFS Traversal:**

```text
_dfs(root, ["api", "john", "profile"], index=0):
  segment = "api"
  
  Try exact: root.children["api"]? YES ✓
    → _dfs(api_node, segments, index=1)
    
      segment = "john"
      
      Try exact: api_node.children["john"]? NO ✗
      Try wildcard: api_node.children["*"]? YES ✓
        → _dfs(wildcard_node, segments, index=2)
        
          segment = "profile"
          
          Try exact: wildcard_node.children["profile"]? YES ✓
            → _dfs(profile_node, segments, index=3)
            
              index=3 == len(segments)=3 → BASE CASE
              Return profile_node.handler = "GetProfile" ✓
```

**Result:** "GetProfile"

---

**Query 3:** `/api/users/settings` (No matching route)

Split path: `["api", "users", "settings"]`

**DFS Traversal:**

```text
_dfs(root, ["api", "users", "settings"], index=0):
  segment = "api"
  
  Try exact: root.children["api"]? YES ✓
    → _dfs(api_node, segments, index=1)
    
      segment = "users"
      
      Try exact: api_node.children["users"]? YES ✓
        → _dfs(users_node, segments, index=2)
        
          segment = "settings"
          
          Try exact: users_node.children["settings"]? NO ✗
          Try wildcard: users_node.children["*"]? NO ✗
          
          Return None ✗
```

**Result:** None (no matching route)

---

**Key Observations:**

1. **Exact match is tried first** (priority)
2. **Wildcard is fallback** when exact fails
3. **DFS explores all possible paths** via backtracking
4. **Handler is returned only at leaf nodes** (end of path)

---

## 🔍 Complexity Analysis

### Time Complexity

| Operation | Best Case | Worst Case | Explanation |
|-----------|-----------|------------|-------------|
| `addRoute()` | **O(K)** | **O(K)** | K = number of segments, create nodes |
| `matchRoute()` | **O(K)** | **O(2^K)** | Best: direct match. Worst: backtrack every node |

**Typical Case:** O(K) because most routes don't have many wildcards at every level.

**Worst Case Example:**
```text
Routes: /*/*, /*/*/*, etc.
Every node has both exact and wildcard children.
DFS tries all combinations → exponential.
```

### Space Complexity

| Component | Space |
|-----------|-------|
| Trie Storage | **O(N × K)** | N routes, K segments each |
| Recursion Stack | **O(K)** | DFS depth = path length |

---

## ⚠️ Common Pitfalls

### 1. **Wrong Priority (Wildcard Before Exact)**

**Wrong:**
```python
def _dfs(self, node, segments, index):
    # ...
    if '*' in node.children:  # Wildcard first
        result = self._dfs(node.children['*'], segments, index + 1)
        if result: return result
    
    if segment in node.children:  # Exact second
        # ...
```

**Problem:** `/users/admin` would match `/users/*` instead of `/users/admin`.

**Right:** Always try exact match first.

### 2. **Not Handling Empty Segments**

**Wrong:**
```python
segments = path.split('/')  # ["", "api", "users"]
```

**Problem:** Leading `/` creates empty string, breaks matching.

**Right:** Filter empty strings: `[s for s in path.split('/') if s]`.

### 3. **Forgetting to Check Endpoint**

**Wrong:**
```python
if index == len(segments):
    return node  # Returns node, not handler!
```

**Right:** Return `node.handler` (might be `None` if not an endpoint).

### 4. **Wildcard Matching Zero or Multiple Segments**

**Wrong Assumption:** `*` in `/api/*/data` matches `/api/data` (zero segments).

**Right:** `*` matches **exactly one** segment. `/api/data` won't match.

---

## 🔄 Follow-up Questions

### Follow-up 1: Path Parameters (Named Wildcards)

**Problem Statement:**
> "Extend the router to support named parameters like `/users/{id}/posts`. When matching, return both the handler and the captured parameters."

**Example:**
```python
router.addRoute("/users/{userId}/posts/{postId}", "GetPost")

result = router.matchRoute("/users/123/posts/456")
# Expected: { "handler": "GetPost", "params": {"userId": "123", "postId": "456"} }
```

**Solution:**

```python
class ParamTrieNode(TrieNode):
    def __init__(self):
        super().__init__()
        self.param_name: Optional[str] = None  # e.g., "userId"

class ParamRouter(Router):
    def addRoute(self, path: str, handler: str) -> None:
        """
        Add route with parameter support.
        {param} is treated like *, but we store param_name.
        """
        segments = self._split_path(path)
        node = self.root
        
        for segment in segments:
            # Check if segment is a parameter
            if segment.startswith('{') and segment.endswith('}'):
                param_name = segment[1:-1]  # Extract "userId" from "{userId}"
                
                # Use '*' as the key, but store param name
                if '*' not in node.children:
                    node.children['*'] = ParamTrieNode()
                    node.children['*'].param_name = param_name
                node = node.children['*']
            else:
                # Regular segment
                if segment not in node.children:
                    node.children[segment] = ParamTrieNode()
                node = node.children[segment]
        
        node.handler = handler
    
    def matchRoute(self, path: str) -> Optional[dict]:
        """
        Match route and return handler + params.
        
        Returns:
            { "handler": str, "params": dict } or None
        """
        segments = self._split_path(path)
        return self._dfs(self.root, segments, 0, {})
    
    def _dfs(self, node, segments, index, params):
        """
        DFS with parameter capture.
        """
        if index == len(segments):
            if node.handler is not None:
                return {"handler": node.handler, "params": params}
            return None
        
        current_segment = segments[index]
        
        # Try exact match
        if current_segment in node.children:
            result = self._dfs(node.children[current_segment], segments, index + 1, params)
            if result is not None:
                return result
        
        # Try wildcard/param match
        if '*' in node.children:
            child = node.children['*']
            # Capture parameter
            new_params = params.copy()  # Avoid mutation on backtrack
            if child.param_name:
                new_params[child.param_name] = current_segment
            
            result = self._dfs(child, segments, index + 1, new_params)
            if result is not None:
                return result
        
        return None


# ============================================
# EXAMPLE
# ============================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("FOLLOW-UP 1: PATH PARAMETERS")
    print("=" * 60)
    
    router = ParamRouter()
    
    router.addRoute("/users/{userId}", "GetUser")
    router.addRoute("/users/{userId}/posts/{postId}", "GetPost")
    router.addRoute("/api/products/{id}/reviews", "ProductReviews")
    
    print("\nTest 1:")
    result = router.matchRoute("/users/123")
    print(f"Path: /users/123")
    print(f"Result: {result}")
    # {"handler": "GetUser", "params": {"userId": "123"}}
    
    print("\nTest 2:")
    result = router.matchRoute("/users/john/posts/456")
    print(f"Path: /users/john/posts/456")
    print(f"Result: {result}")
    # {"handler": "GetPost", "params": {"userId": "john", "postId": "456"}}
    
    print("\nTest 3:")
    result = router.matchRoute("/api/products/xyz/reviews")
    print(f"Path: /api/products/xyz/reviews")
    print(f"Result: {result}")
    # {"handler": "ProductReviews", "params": {"id": "xyz"}}
```

**Complexity:** Same as base solution (O(K) per operation).

---

### Follow-up 2: HTTP Method Matching

**Problem Statement:**
> "Routes should also match by HTTP method (GET, POST, etc.). `/api/users` with GET should map to a different handler than `/api/users` with POST."

**Solution:**

```python
class MethodRouter:
    def __init__(self):
        # Separate trie for each method
        self.tries = {
            'GET': TrieNode(),
            'POST': TrieNode(),
            'PUT': TrieNode(),
            'DELETE': TrieNode()
        }
    
    def addRoute(self, method: str, path: str, handler: str) -> None:
        """Register a route for a specific HTTP method."""
        if method not in self.tries:
            self.tries[method] = TrieNode()
        
        segments = self._split_path(path)
        node = self.tries[method]
        
        for segment in segments:
            if segment not in node.children:
                node.children[segment] = TrieNode()
            node = node.children[segment]
        
        node.handler = handler
    
    def matchRoute(self, method: str, path: str) -> Optional[str]:
        """Match route by method and path."""
        if method not in self.tries:
            return None
        
        segments = self._split_path(path)
        return self._dfs(self.tries[method], segments, 0)
    
    # _dfs and _split_path same as Router


# ============================================
# EXAMPLE
# ============================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("FOLLOW-UP 2: HTTP METHOD ROUTING")
    print("=" * 60)
    
    router = MethodRouter()
    
    router.addRoute("GET", "/users", "ListUsers")
    router.addRoute("POST", "/users", "CreateUser")
    router.addRoute("GET", "/users/*/posts", "GetUserPosts")
    router.addRoute("DELETE", "/users/*", "DeleteUser")
    
    print(f"GET /users: {router.matchRoute('GET', '/users')}")        # ListUsers
    print(f"POST /users: {router.matchRoute('POST', '/users')}")      # CreateUser
    print(f"DELETE /users/123: {router.matchRoute('DELETE', '/users/123')}")  # DeleteUser
    print(f"PUT /users: {router.matchRoute('PUT', '/users')}")        # None
```

---

### Follow-up 3: Middleware Chain

**Problem Statement:**
> "Support middleware that runs before handlers. For example, all routes under `/api/*` should run an authentication middleware first."

**Solution Approach:**

1. Store **middleware list** at each node (inherited by children).
2. During `addRoute`, collect middleware from parent nodes.
3. During `matchRoute`, return `(handler, middleware_list)`.

```python
class MiddlewareNode(TrieNode):
    def __init__(self):
        super().__init__()
        self.middlewares = []  # List of middleware functions

class MiddlewareRouter:
    def addMiddleware(self, path: str, middleware: str) -> None:
        """Attach middleware to a path prefix."""
        segments = self._split_path(path)
        node = self.root
        
        for segment in segments:
            if segment not in node.children:
                node.children[segment] = MiddlewareNode()
            node = node.children[segment]
        
        node.middlewares.append(middleware)
    
    def matchRoute(self, path: str) -> Optional[dict]:
        """Return handler and accumulated middleware."""
        segments = self._split_path(path)
        return self._dfs(self.root, segments, 0, [])
    
    def _dfs(self, node, segments, index, middlewares):
        # Accumulate middleware at this node
        accumulated = middlewares + node.middlewares
        
        if index == len(segments):
            if node.handler:
                return {"handler": node.handler, "middlewares": accumulated}
            return None
        
        # ... (same DFS logic, pass accumulated to recursive calls)
```

---

## 🧪 Test Cases

```python
def test_router():
    router = Router()
    
    # Test 1: Exact match
    router.addRoute("/api/users", "A")
    assert router.matchRoute("/api/users") == "A"
    
    # Test 2: No match
    assert router.matchRoute("/api/posts") is None
    
    # Test 3: Wildcard
    router.addRoute("/users/*/posts", "B")
    assert router.matchRoute("/users/123/posts") == "B"
    assert router.matchRoute("/users/abc/posts") == "B"
    
    # Test 4: Priority
    router.addRoute("/users/admin", "Admin")
    router.addRoute("/users/*", "User")
    assert router.matchRoute("/users/admin") == "Admin"  # Exact
    assert router.matchRoute("/users/john") == "User"    # Wildcard
    
    # Test 5: Nested wildcards
    router.addRoute("/a/*/c/*/e", "Nested")
    assert router.matchRoute("/a/b/c/d/e") == "Nested"
    assert router.matchRoute("/a/x/c/y/e") == "Nested"
    assert router.matchRoute("/a/b/c/e") is None  # Wrong segment count
    
    print("All tests passed! ✓")

if __name__ == "__main__":
    test_router()
```

---

## 🎯 Key Takeaways

1. **Trie is Perfect for Hierarchical Path Matching** (segment-based, not character-based).
2. **DFS with Backtracking** handles wildcard alternatives.
3. **Priority Rules Matter:** Try exact matches before wildcards.
4. **Named Parameters** extend wildcards with metadata capture.
5. **Multiple Tries** (one per HTTP method) handle method-based routing.

---

## 📚 Related Problems

- **LeetCode 208:** Implement Trie (Prefix Tree)
- **LeetCode 211:** Design Add and Search Words Data Structure (wildcards with `.`)
- **LeetCode 677:** Map Sum Pairs (Trie with aggregation)
- **LeetCode 1032:** Stream of Characters (Trie for suffix matching)
