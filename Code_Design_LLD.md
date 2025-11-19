
# Code Design / Low-Level Design (LLD) - Atlassian Interview Questions

This document focuses on the Code Design rounds, which emphasize clean, modular, and testable code. Candidates are often expected to implement a working solution in an IDE, handle edge cases, and write unit tests.

---

## Common Machine Coding Problems at Atlassian

Based on multiple interview experiences, these are the most frequently asked machine coding/LLD problems:

### High Frequency (Asked Very Often)
1.  **Rate Limiter / Token Bucket** ⭐⭐⭐⭐⭐
2.  **Snake Game** ⭐⭐⭐⭐⭐
3.  **Trello / Kanban Board** ⭐⭐⭐⭐
4.  **File System Design** ⭐⭐⭐⭐

### Medium Frequency
5.  **Parking Lot System** ⭐⭐⭐
6.  **Splitwise / Expense Sharing** ⭐⭐⭐
7.  **Tic Tac Toe** ⭐⭐⭐

### Lower Frequency
8.  **Snake and Ladder** ⭐⭐
9.  **Bowling Alley** ⭐⭐

**Note:** Focus on the high-frequency problems first. Practice implementing them end-to-end with tests.

---

## 1. Rate Limiter
**Frequency:** High
**Core Concept:** Concurrency, Design Patterns

### Problem Description
Implement a `RateLimiter` library/class that limits the number of requests a user/client can make within a given time window.
*   **Input:** `customerId`, `requestTime`
*   **Output:** `boolean` (Allowed/Denied)

### Variations & Follow-ups
1.  **Algorithms:**
    *   **Fixed Window:** Simple counters, resets every X seconds.
    *   **Sliding Window:** More accurate, stores timestamps.
    *   **Token Bucket:** Concept of "credits".
2.  **Concurrency:** The system must be thread-safe.
3.  **Scale:** How to handle this in a distributed system? (Usually moves to HLD discussion).
4.  **Granularity:** Limit by IP, User ID, or API Key.
5.  **Credit System:** Unused requests carry over to next window.

### Analysis & Tips
*   **Interface:** Define a clean interface `isAllowed(clientId)`.
*   **Thread Safety:** Use `synchronized` blocks, `ReentrantLock`, or `ConcurrentHashMap`.
    *   **Key Discussion Points:**
        *   Why `ConcurrentHashMap` over `HashMap`? (Thread-safe put/get operations without locking the entire map)
        *   When to use `synchronized` keyword? (Protecting critical sections like cleanup operations)
        *   Use `Lock` (explicit) for better control over locking mechanism
*   **Efficiency:** Cleaning up old timestamps in Sliding Window (lazy cleanup vs background thread).
*   **Design Pattern:** Strategy Pattern to support multiple algorithms (Fixed Window, Sliding Window, Token Bucket).
*   **Implementation Structure:**
    *   `IRateLimiting` interface with `isRequestAllowed()` method
    *   Separate classes: `FixedWindow`, `MovingWindow`, `TokenBucket` implementing the interface
    *   `RateLimiter` class (Singleton) that manages instances per client/key
    *   `RateLimitAlgoProvider` to get the right algorithm class

---

## 2. Snake Game (LLD Focus)
**Frequency:** Very High
**Core Concept:** Object-Oriented Programming (OOP), Game Loop

### Problem Description
(See DSA section for logic). In the LLD round, the focus is on **Structure** and **Extensibility**.

### Expectations
*   **Classes:**
    *   `Snake`: Manages body (`Deque`), `grow()`, `move()`.
    *   `Board`: Manages grid size.
    *   `Game`: Manages state (`isGameOver`), game loop.
    *   `Direction`: Enum.
    *   `Position`: Helper class for coordinates.
*   **Extensibility:** How easy is it to add new features (e.g., obstacles, different food types)?
*   **Testing:** Write JUnit/Test cases for movement, growth, and collision.

### Analysis & Tips
*   **Single Responsibility Principle:** Don't put movement logic in the `Board` class. The `Snake` should know how to move itself.
*   **Configuration:** Pass board size and initial snake size as constructor parameters.

---

## 3. Tagging Management System (LLD Component)
**Frequency:** Medium
**Core Concept:** Many-to-Many Relationships

### Problem Description
Design the classes and interfaces for a Tagging System used across products (Jira, Confluence).
*   `addTag(entityId, tag)`
*   `removeTag(entityId, tag)`
*   `getTags(entityId)`
*   `getEntities(tag)`

### Variations & Follow-ups
1.  **Search:** get entities by tag name (or partial name).
2.  **Popularity:** Get top used tags.

### Analysis & Tips
*   **Data Model:** `Tag`, `Entity`, `TagService`.
*   **In-Memory Storage:** Two HashMaps: `Entity -> List<Tag>` and `Tag -> List<Entity>` for fast bidirectional lookups.

---

## 4. Router / Middleware (LLD Focus)
**Frequency:** Medium
**Core Concept:** Tree Structure, API Design

### Problem Description
(See DSA section for logic). LLD focus is on the API usability.
*   **Fluent Interface:** `router.path("/api").get(handler)`.
*   **Middleware:** Executing chain of functions before the final handler.

---

## 5. Voting System (LLD Focus)
**Frequency:** Medium
**Core Concept:** Strategy Pattern

### Problem Description
Design a voting system where rules can change.
*   **Rule 1:** Simple majority wins.
*   **Rule 2:** Weighted votes (1st choice = 3pts, 2nd = 2pts).

### Analysis & Tips
*   **Strategy Pattern:** Define a `WinningStrategy` interface. Implement different logic (Weighted, Majority) as classes. This allows switching rules at runtime without changing core logic.

---

## 6. Payment / Cost Explorer
**Frequency:** Low-Medium
**Core Concept:** Billing Logic, Date/Time Handling

### Problem Description
Calculate the cost for a customer's subscription plan over a year.
*   Plans: Basic ($9.99), Standard ($49.99), Premium ($249.99).
*   Users can upgrade/downgrade mid-month.
*   **Goal:** Generate monthly and yearly cost reports.

### Variations & Follow-ups
1.  **Prorated Billing:** If user upgrades on 15th, charge 50% of old plan and 50% of new plan.
2.  **Trial Periods:** Handle free trials.

### Analysis & Tips
*   **Edge Cases:** Leap years, 30 vs 31 day months.
*   **Design:** `Subscription`, `Plan`, `BillingService`.
*   **Money Pattern:** Never use `float/double` for currency. Use `BigDecimal` (Java) or integer cents.

---

## 7. Customer Satisfaction / Agent Rating
**Frequency:** Low
**Core Concept:** Aggregation, Sorting

### Problem Description
A customer support system where agents get rated (1-5 stars).
*   `rateAgent(agentId, rating)`
*   `getAverageRating(agentId)`
*   `getTopAgents()`

### Analysis & Tips
*   **Storage:** `Map<AgentId, List<Rating>>` or `Map<AgentId, RunningAverage>`.
*   **Optimization:** Maintain a running sum and count to calculate average in $O(1)$ instead of iterating through all ratings every time.

---

## 8. Connection Pool
**Frequency:** Low
**Core Concept:** Resource Management, Concurrency

### Problem Description
Design a thread-safe Database Connection Pool.
*   `borrowConnection()`: Get an available connection (wait if none available).
*   `borrowConnection(timeout)`: Get a connection with timeout.
*   `surrenderConnection(conn)`: Return a connection to the pool.

### Key Requirements
1.  **Initial Pool Size:** Pre-create N connections on startup.
2.  **Max Pool Size:** Never exceed M total connections.
3.  **Thread Safety:** Multiple threads can borrow/return connections concurrently.
4.  **Blocking Behavior:** If all connections are in use, block until one is available.
5.  **Dynamic Growth:** If pool is empty and `currentSize < maxSize`, create a new connection.

### Analysis & Tips
*   **BlockingQueue:** Use a `BlockingQueue` (e.g., `LinkedBlockingQueue`) to store available connections.
    *   `take()`: Blocks until a connection is available.
    *   `offer()`: Adds connection back without exceeding capacity.
*   **Synchronization:** 
    *   Synchronized method for `openAndPoolConnection()` to prevent creating more than `maxPoolSize` connections.
    *   Use `currentPoolSize` counter to track total connections created.
*   **Timeout:** 
    *   `borrowConnection(timeout)` uses `queue.poll(timeout, TimeUnit)` to wait with timeout.
*   **Connection Validation:** In production, validate connections before returning them (check if still alive).
*   **Lazy Creation:** Create new connections on-demand if pool is empty and below max size.

### Implementation Considerations
**Good Practices:**
1.  **Parameter Validation:**
    ```java
    if (initialPoolSize > maxPoolSize || initialPoolSize < 1 || maxPoolSize < 1) {
        throw new IllegalArgumentException("Invalid pool size parameters");
    }
    ```
2.  **Thread-Safe Counter:**
    ```java
    private synchronized void openAndPoolConnection() throws SQLException {
        if (currentPoolSize == maxPoolSize) return; // Guard clause
        Connection conn = DriverManager.getConnection(dbUrl, dbUser, dbPassword);
        pool.offer(conn);
        currentPoolSize++;
    }
    ```
3.  **Lazy Creation in borrowConnection:**
    ```java
    public Connection borrowConnection() throws SQLException, InterruptedException {
        if (pool.peek() == null && currentPoolSize < maxPoolSize) {
            openAndPoolConnection(); // Create new connection if needed
        }
        return pool.take(); // Block until available
    }
    ```

**Potential Issues to Discuss:**
1.  **Connection Leaks:** What if a thread never calls `surrenderConnection()`?
    *   **Solution:** Implement timeout tracking; close stale connections.
2.  **Connection Validity:** Connections might become stale (network issues, DB restarts).
    *   **Solution:** Validate with `connection.isValid(timeout)` before returning.
3.  **Shutdown:** How to gracefully close all connections?
    *   **Solution:** Implement `shutdown()` method that closes all connections in the queue.
4.  **Fairness:** Should waiting threads get connections in FIFO order?
    *   **Solution:** `LinkedBlockingQueue` is FIFO by default.

### Example Code Structure
```java
public class ConnectionPool {
    private BlockingQueue<Connection> pool;
    private int maxPoolSize;
    private int initialPoolSize;
    private int currentPoolSize = 0;
    private String dbUrl, dbUser, dbPassword;

    public ConnectionPool(int maxPoolSize, int initialPoolSize, 
                          String url, String user, String password, 
                          String driverClassName) throws ClassNotFoundException, SQLException {
        // Validation
        if (initialPoolSize > maxPoolSize || initialPoolSize < 1 || maxPoolSize < 1) {
            throw new IllegalArgumentException("Invalid pool size");
        }
        
        this.maxPoolSize = maxPoolSize;
        this.initialPoolSize = initialPoolSize;
        this.dbUrl = url;
        this.dbUser = user;
        this.dbPassword = password;
        
        this.pool = new LinkedBlockingQueue<>(maxPoolSize);
        
        // Load driver and pre-create connections
        Class.forName(driverClassName);
        for (int i = 0; i < initialPoolSize; i++) {
            openAndPoolConnection();
        }
    }

    private synchronized void openAndPoolConnection() throws SQLException {
        if (currentPoolSize >= maxPoolSize) return;
        Connection conn = DriverManager.getConnection(dbUrl, dbUser, dbPassword);
        pool.offer(conn);
        currentPoolSize++;
    }

    public Connection borrowConnection() throws SQLException, InterruptedException {
        if (pool.peek() == null && currentPoolSize < maxPoolSize) {
            openAndPoolConnection();
        }
        return pool.take(); // Blocks until available
    }

    public Connection borrowConnection(long timeoutMillis) 
            throws SQLException, InterruptedException {
        if (pool.peek() == null && currentPoolSize < maxPoolSize) {
            openAndPoolConnection();
        }
        Connection conn = pool.poll(timeoutMillis, TimeUnit.MILLISECONDS);
        if (conn == null) {
            throw new SQLException("Timeout waiting for connection");
        }
        return conn;
    }

    public void surrenderConnection(Connection conn) {
        if (conn != null) {
            pool.offer(conn); // Won't exceed capacity
        }
    }

    public void shutdown() throws SQLException {
        for (Connection conn : pool) {
            conn.close();
        }
        pool.clear();
    }
}
```

### Interview Discussion Points
1.  **Why BlockingQueue over Semaphore?**
    *   BlockingQueue stores actual connections; Semaphore just counts permits.
    *   BlockingQueue handles FIFO ordering naturally.
2.  **Why synchronized on openAndPoolConnection()?**
    *   Prevent race condition where multiple threads try to create connections simultaneously.
    *   Without sync, `currentPoolSize` could exceed `maxPoolSize`.
3.  **Why not create all maxPoolSize connections upfront?**
    *   Resource efficiency: only create connections as needed.
    *   Database might not support thousands of idle connections.
4.  **How to test this?**
    *   Unit test: Create pool with size 2, borrow 3 (one should block).
    *   Stress test: 100 threads borrowing/returning concurrently.

---

## 9. File System with O(1) Directory Size
**Frequency:** Low
**Core Concept:** Tree Structure, Caching, Propagation

### Problem Description
Design a file system that supports:
*   `addFile(path, size)`: Add a file to a directory
*   `getSize(path)`: Get the total size of a directory in O(1) time (ignoring traversal from root to directory)

**Challenge:** When a file is added to a directory, all parent directories' sizes must be updated.

### Variations & Follow-ups
1.  **File Updates:** What happens when a file size changes?
2.  **File Deletion:** How to handle `deleteFile(path)`?
3.  **Move Operations:** Moving files/directories between folders.
4.  **Concurrency:** Thread-safe operations for multi-user access.
5.  **Wildcard Pattern Matching (LeetCode 588 variation):**
    *   **Problem:** Support wildcard `*` in path creation and retrieval.
    *   **Example:** 
        *   `createPath("/a/*/b", 100)` 
        *   `get("/a/x/y/b")` should return `100` (because `*` matches `/x/y`)
    *   **Solution:** Use pattern matching libraries (e.g., regex) or implement Trie with wildcard nodes.
    *   **Expectation:** Handle wildcard matching in `createPath` method by storing patterns, then match during `get` operations.

### Analysis & Tips
*   **Data Structure:**
    *   `Directory` class with:
        *   `Map<String, Directory> subDirectories`
        *   `Map<String, Long> files` (fileName -> size)
        *   `long totalSize` (cached size of this directory and all subdirectories)
*   **O(1) Size Query:** Maintain a cached `totalSize` field in each directory.
*   **Size Update Propagation:** When adding a file:
    1.  Parse the path to find the target directory (this traversal cost is "ignored" as per problem statement).
    2.  Add the file to the directory.
    3.  **Propagate size update:** Traverse back up to the root, adding `fileSize` to each parent's `totalSize`.
*   **Time Complexity:**
    *   `addFile`: O(depth) for traversal + O(depth) for propagation = O(depth)
    *   `getSize`: O(depth) for traversal + O(1) for size retrieval = O(depth) (but the O(1) part is the "getting size", not the traversal)
*   **Space Complexity:** O(N) where N is the number of files and directories.
*   **Alternative Approach (without O(1) size):** Calculate size on-demand using DFS with memoization.

### Example Code Structure
```java
class Directory {
    String name;
    Map<String, Directory> subDirectories;
    Map<String, Long> files;
    long totalSize;
    
    void addFile(String fileName, long size) {
        files.put(fileName, size);
        totalSize += size;
    }
    
    long getSize() {
        return totalSize; // O(1)
    }
}

class FileSystem {
    Directory root;
    
    void addFile(String path, long size) {
        String[] parts = path.split("/");
        Directory current = root;
        List<Directory> pathTrace = new ArrayList<>();
        
        // Traverse to target directory
        for (int i = 0; i < parts.length - 1; i++) {
            pathTrace.add(current);
            current = current.subDirectories.computeIfAbsent(parts[i], k -> new Directory(parts[i]));
        }
        
        // Add file
        String fileName = parts[parts.length - 1];
        current.addFile(fileName, size);
        
        // Propagate size update to all parents
        for (Directory dir : pathTrace) {
            dir.totalSize += size;
        }
    }
}
```

---

## Common Interview Feedback & Pitfalls

### What Interviewers Look For
1.  **Code Clarity:**
    *   Simple, readable code is preferred over complex optimizations
    *   Avoid overly clever solutions that are hard to understand and debug
2.  **Testing:**
    *   Offer to write unit tests even if time is running out
    *   Show test-driven thinking (edge cases, null checks, boundary conditions)
3.  **Design Patterns:**
    *   Strategy Pattern for multiple implementations
    *   Singleton for global instances (Rate Limiter, Connection Pool)
    *   Factory Pattern for object creation
4.  **Communication:**
    *   Clarifying questions are essential
    *   Explain your approach before coding
    *   Justify design decisions (e.g., "I'm using HashMap here because...")

### Common Rejection Reasons (From Candidate Feedback)
1.  **"Complex code to understand and debug"**
    *   Even if solution is correct, if it's too complex, it's a red flag
    *   Simplicity > Optimization (unless optimization is explicitly asked)
2.  **"Did not justify approach"**
    *   Don't just code silently; explain your thought process
    *   Discuss tradeoffs (time vs space complexity)
3.  **"Missing logs/locks/error handling"**
    *   For production-level code, mention logging and exception handling
    *   For concurrent systems, explicitly discuss locking mechanisms
4.  **"Did not write tests"**
    *   Always offer to write tests; it shows maturity
5.  **Confusing Problem Statement:**
    *   If the problem is unclear, ask clarifying questions immediately
    *   Don't assume input/output formats; verify with examples

### "STRONG NO HIRE" Despite Working Code - Why?

**Real Case Study:** A candidate received "STRONG NO HIRE" for both Rate Limiter and Voting problems despite submitting working code.

#### Rate Limiter Issues (Using Semaphore Approach)
**What the candidate did:**
*   Used `Semaphore` with `ScheduledExecutorService` to release permits after time window.
*   Code compiled and ran correctly.

**Why it failed:**
1.  **Semaphore Pattern Mismatch:**
    *   Semaphores are designed for resource pooling (e.g., connection pools), not time-based rate limiting.
    *   Releasing all permits at once every X seconds creates a "thundering herd" - all requests are allowed in the first millisecond of each window.
    *   **Example:** 5 requests per second. At 0.001s, all 5 slots are used. For the next 0.999s, all requests are blocked. This is **not** smooth rate limiting.
2.  **Fixed Window Problem:**
    *   The scheduled release creates a fixed window, which has known issues (burst at window boundaries).
    *   Better: Sliding window or token bucket with gradual replenishment.
3.  **Resource Leak:**
    *   `ScheduledExecutorService` is created per customer but never shut down.
    *   For millions of customers, this creates millions of threads → memory leak.
4.  **Thread Safety Issues:**
    *   `semaphore.release(this.maxLimit - semaphore.availablePermits())` is not atomic.
    *   Between `availablePermits()` and `release()`, permits might be acquired, leading to over-release.
5.  **Wrong Mental Model:**
    *   Interviewer expects Token Bucket or Sliding Window, not Semaphore.
    *   Semaphore approach shows lack of understanding of rate limiting patterns.

**What should have been done:**
*   **Sliding Window:** Store timestamps in a queue, remove old ones, check size.
*   **Token Bucket:** Track tokens, refill rate, last refill time.
*   Use `ConcurrentHashMap` with `ReentrantLock` per user, not Semaphore.

#### Voting Algorithm Issues
**What the candidate did:**
*   Calculated points correctly (3, 2, 1 for positions).
*   Used `LinkedHashMap` to store candidate scores.
*   Sorted by score using streams.

**Why it failed:**
1.  **No Tie-Breaking Logic:**
    *   Code returns `0` in comparator when scores are equal, which doesn't handle ties.
    *   Interviewer expects: "If scores are equal, who wins?" (e.g., lexicographically, or first to reach score).
    *   Candidate didn't ask this clarifying question.
2.  **Inefficient Sorting:**
    *   Using streams to sort the entire map is O(N log N) every time.
    *   For "get top 3 teams," a Min-Heap of size 3 is O(N log 3) = O(N).
3.  **LinkedHashMap Misuse:**
    *   `LinkedHashMap` maintains insertion order, not sorted order.
    *   Using it here doesn't provide any benefit; plain `HashMap` would work.
4.  **No Discussion of Follow-ups:**
    *   Didn't propose how to extend to "most recent vote wins" or "weighted by position."
    *   Didn't discuss real-time updates (what if votes keep coming?).
5.  **Production Readiness:**
    *   No input validation (what if votes list is null? Empty strings?).
    *   No handling of duplicate votes by same voter.
    *   No logging or error messages.

**What should have been done:**
*   Ask about tie-breaking strategy before coding.
*   Use `PriorityQueue` (min-heap) for top K.
*   Discuss extensibility: "If we need to handle streaming votes, we'd use the All O(1) approach with doubly linked list."
*   Add input validation and edge case handling.

### Key Takeaways
1.  **Working Code ≠ Good Code:**
    *   Interviewers assess: Is this production-ready? Maintainable? Scalable?
2.  **Know Design Patterns:**
    *   Don't use Semaphore for rate limiting; use Token Bucket or Sliding Window.
    *   Don't use LinkedHashMap when you need sorting; use TreeMap or PriorityQueue.
3.  **Ask Clarifying Questions:**
    *   Tie-breaking, edge cases, scale requirements.
4.  **Discuss Trade-offs:**
    *   "I'm using approach X because of Y benefit, but it has Z drawback."
5.  **Think Long-Term:**
    *   Resource leaks (threads, connections) are red flags.
    *   Always consider memory and thread management.

### Best Practices
*   Start with a simple, working solution, then optimize
*   Use meaningful variable/method names
*   Separate concerns (business logic vs data access vs presentation)
*   Handle edge cases (null inputs, empty collections, negative numbers)
*   For DSA problems: Test your code with the given examples before submitting

### Additional Expectations (Especially for Intern/Junior Roles)
1.  **Real-Life Problem Mapping:**
    *   Interviewers may give you a real-world scenario (e.g., "restaurant reservation system") and expect you to choose appropriate data structures.
    *   Explain why you chose HashMap over ArrayList, or TreeSet over HashSet.
2.  **Theory Questions:**
    *   Internal working of STL containers (C++) or Collections (Java).
    *   Time complexity of operations: `map.insert()`, `set.find()`, `vector.push_back()`.
    *   Difference between `unordered_map` and `map` (hash table vs balanced BST).
3.  **Dry Run:**
    *   After coding, be prepared to trace through your code with sample inputs.
    *   Explain each step verbally as you execute.

---
