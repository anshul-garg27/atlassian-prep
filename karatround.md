# 1. KARAT SCREENING ROUND

## 📊 Overview
- **Duration:** 60 minutes
- **Platform:** Karat (Third-party screening)
- **Difficulty:** Medium
- **Success Rate:** ~60-70%
- **Availability:** 24/7, nights, weekends
- **Reschedule:** Once within 48 hours (additional reschedules need approval)
- **Redo Opportunity:** Available if you're unhappy with performance

## 🔄 TWO KARAT INTERVIEW FORMATS

### **Format A: System Design + DSA (Common for Senior Roles)**
- **Time Split:** 20-25 min (System Design) + 30-35 min (DSA)
- **Structure:** 5 System Design rapid-fire questions + 2 DSA Problems
- **Focus:** High-level architecture + coding
- **Companies:** Wayfair, Coinbase, PayPal (some roles)

### **Format B: Project Discussion + Knowledge + Coding (Common for Mid-Level)**
- **Time Split:** 15 min (Project) + 10 min (Knowledge) + 35 min (Coding)
- **Structure:** 
  1. **Past Project Discussion** - Explain a project you worked on
  2. **Knowledge Questions** - Algorithms, data structures, time/space complexity
  3. **Multi-Part Coding** - Progressive coding problem with multiple parts
- **Focus:** Practical experience + fundamentals + implementation
- **Companies:** Atlassian, Indeed, some others

## ⚠️ CRITICAL POINTS
- **Time management is EVERYTHING**
- Don't get stuck on one question
- Interviewers provide guidance if stuck too long
- **You may not finish all tasks** - keep moving forward
- Ask clarifying questions early
- Think out loud constantly

## 🖥️ KARAT STUDIO PLATFORM
- **Browser-Based IDE:** No setup needed
- **Supported Browsers:** Chrome or Firefox (recommended)
- **Not Supported:** Tablet devices
- **Features:** Code execution, debugging, print statements
- **Language:** Use your most comfortable language
- **Practice:** Access Karat Studio before interview to familiarize

## ✅ ALLOWED RESOURCES
✅ **Can Use:**
- Google / Stack Overflow
- Documentation (language docs, API references)
- Debugging tools
- Print statements
- Common investigation techniques

❌ **Cannot Use:**
- AI tools (ChatGPT, Copilot, etc.)
- Pre-written code solutions
- Other people's help during interview

## 🔧 TECHNICAL SETUP
- **Good internet connection** (critical)
- **Quiet location**
- **Microphone + Headphones** (for clear audio)
- **Webcam** (video must be on)
- **Monitor/Laptop** (no tablets)
- **Test Karat Studio beforehand**

---

## 💼 FORMAT B: PROJECT DISCUSSION + KNOWLEDGE QUESTIONS

### **Part 1: Past Project Discussion (15 minutes)**

**What They Ask:**
"Tell me about a recent project you worked on that you're proud of."

**How to Structure Your Answer (STAR Method):**

**1. Situation (2 min):**
```
"I worked on [Project Name] at [Company] where we needed to [business problem].
The challenge was [specific technical/business challenge].
This affected [users/revenue/team] by [impact]."
```

**2. Task (1 min):**
```
"My role was [your specific responsibility].
I was responsible for [specific components/features].
The goal was to [measurable objective]."
```

**3. Action (8 min) - MOST IMPORTANT:**
```
"Here's my technical approach:

Architecture:
- Used [technologies/frameworks]
- Designed [system architecture]
- Chose [technology] because [trade-off reasoning]

Implementation:
- Built [feature 1] using [approach]
- Solved [challenge] by [solution]
- Optimized [metric] from X to Y

Collaboration:
- Worked with [team members/stakeholders]
- Made trade-offs between [option A vs B]
- Handled [unexpected issue] by [solution]"
```

**4. Result (2 min):**
```
"Outcomes:
- Reduced [metric] by X%
- Increased [metric] by Y%
- Deployed to [scale]
- Used by [number] users

What I Learned:
- [Technical learning]
- [Process improvement]
- [What I'd do differently]"
```

**Good Project Examples:**
- ✅ E-commerce checkout optimization (reduced latency 40%)
- ✅ Microservices migration (monolith → 15 services)
- ✅ Real-time analytics dashboard (processes 1M events/day)
- ✅ Mobile app feature (increased engagement 25%)

**What NOT to Say:**
- ❌ "We just maintained existing code"
- ❌ Vague: "Made the system better"
- ❌ No metrics: "Users liked it"
- ❌ Only your role: Mention team collaboration

---

### **Part 2: Knowledge Questions (10 minutes)**

**Topic 1: Data Structures**

**Q: What's the difference between Array and LinkedList?**
```
Array:
- Contiguous memory
- O(1) random access by index
- O(n) insertion/deletion (shift elements)
- Fixed size (or resize overhead)
- Cache-friendly

LinkedList:
- Non-contiguous memory (pointers)
- O(n) access (traverse from head)
- O(1) insertion/deletion (just change pointers)
- Dynamic size
- Extra memory for pointers

Use Array: When random access needed, known size
Use LinkedList: When frequent insertions/deletions
```

**Q: Explain HashMap/Dictionary. How does it work internally?**
```
HashMap:
- Key-value pairs
- O(1) average lookup, insert, delete
- Uses hash function: hash(key) → index

Internal:
- Array of buckets
- Hash collision handling:
  1. Chaining: Each bucket → LinkedList
  2. Open Addressing: Find next empty slot
  
- Load factor: 0.75 typical
- When 75% full → resize (double size)
- Rehash all keys into new array

Example:
hash("alice") % 16 = 7 → bucket[7] = {alice: 25}
hash("bob") % 16 = 7 → collision → chain or probe

Time Complexity:
- Best: O(1)
- Worst: O(n) if all keys hash to same bucket
```

**Q: Stack vs Queue - when to use each?**
```
Stack (LIFO - Last In First Out):
- push()/pop() from same end
- O(1) operations
Use cases:
- Function call stack
- Undo/redo
- Expression evaluation
- DFS (Depth-First Search)

Queue (FIFO - First In First Out):
- enqueue() at rear, dequeue() from front
- O(1) operations
Use cases:
- BFS (Breadth-First Search)
- Task scheduling
- Print queue
- Message queues
```

---

**Topic 2: Algorithms**

**Q: What's the difference between BFS and DFS?**
```
BFS (Breadth-First Search):
- Uses Queue
- Level by level
- Finds shortest path
- Space: O(width of tree)
- Use: Shortest path, level-order traversal

DFS (Depth-First Search):
- Uses Stack (or recursion)
- Go deep first
- May not find shortest path
- Space: O(height of tree)
- Use: Detect cycles, topological sort, path finding

Example:
    1
   / \
  2   3
 / \
4   5

BFS: 1 → 2 → 3 → 4 → 5
DFS: 1 → 2 → 4 → 5 → 3 (preorder)
```

**Q: Explain Binary Search. When can you use it?**
```
Binary Search:
- Search in sorted array
- O(log n) time complexity
- Divide and conquer

Algorithm:
1. Check middle element
2. If target < middle: search left half
3. If target > middle: search right half
4. Repeat until found or exhausted

Requirements:
- Array must be sorted
- Random access (array, not linkedlist)

Example:
[1, 3, 5, 7, 9, 11, 13], target=7
Step 1: mid=7 (index 3) → found!

Time: O(log n)
Space: O(1) iterative, O(log n) recursive
```

**Q: What's the difference between O(n) and O(n²)?**
```
O(n) - Linear:
- One loop through n elements
- Example: Find max in array
for i in range(n):
    check arr[i]

O(n²) - Quadratic:
- Nested loops
- Example: Bubble sort, check all pairs
for i in range(n):
    for j in range(n):
        compare arr[i] with arr[j]

Impact:
n = 1,000
- O(n) = 1,000 operations
- O(n²) = 1,000,000 operations (1000x slower)

n = 1,000,000
- O(n) = 1,000,000 operations
- O(n²) = 1,000,000,000,000 operations (impossible)
```

---

**Topic 3: Time & Space Complexity**

**Q: Calculate complexity of this code:**
```python
def example(arr):
    for i in range(len(arr)):        # O(n)
        for j in range(i, len(arr)):  # O(n)
            print(arr[i] + arr[j])
    
    arr.sort()                        # O(n log n)
    
    for i in range(len(arr)):        # O(n)
        if arr[i] == target:
            return i
```

**Answer:**
```
Time Complexity:
- Nested loops: O(n²)
- Sort: O(n log n)
- Linear search: O(n)

Total: O(n²) + O(n log n) + O(n) = O(n²)
Dominant term: n²

Space Complexity:
- No extra data structures
- Sort is in-place (assuming Timsort Python)
- O(1) space
```

**Common Complexities to Know:**
```
O(1)         - Hash lookup, array access
O(log n)     - Binary search, balanced tree
O(n)         - Linear search, iterate array
O(n log n)   - Merge sort, quick sort (average)
O(n²)        - Bubble sort, nested loops
O(2ⁿ)        - Recursive fibonacci (naive)
O(n!)        - Permutations, traveling salesman
```

---

**Topic 4: System Design Basics**

**Q: How would you design a URL shortener?**
```
Requirements:
- Long URL → Short URL
- Redirect short → long
- Scale: 100M URLs

Design:
1. Generate short key (7 chars = 62^7 combinations)
2. Store mapping: {short_key: long_url}
3. Database: Redis or DynamoDB (key-value)

API:
POST /shorten
  Body: {url: "https://..."}
  Return: {short_url: "bit.ly/abc123"}

GET /abc123
  Lookup: db.get("abc123")
  Redirect: 301 to long_url

Key Generation:
- Option 1: Hash(long_url) → collision possible
- Option 2: Counter → convert to base62
- Option 3: Random + check uniqueness

Scale:
- Cache hot URLs (Redis)
- Database sharding by hash(key)
- CDN for redirects
```

---

## 🎯 SYSTEM DESIGN RAPID-FIRE QUESTIONS (FORMAT A)

### Pattern 1: Architecture Concerns/Trade-offs

**Q1: Music Streaming with Consistent Hashing**
```
Given: A music streaming and uploading service with consistent hashing
      Load is equally distributed across all servers
      
Question: Do you see any concerns with this architecture?

Expected Answer:
- Hot spots during peak hours
- Popular content skew (some songs much more popular)
- Need for caching layer
- Bandwidth considerations
- Storage replication for availability
- Handling server failures and rebalancing
```

**Q2: Consistent Hashing for Distributed Cache**
```
Design a distributed cache using consistent hashing

Key Points to Cover:
- Hash function selection
- Virtual nodes for better distribution
- Replication strategy
- Failure detection and recovery
- Client-side vs server-side hashing
```

---

### Pattern 2: Design Trade-off Questions

**Q3: Crossword Puzzle Hints System**
```
Given: Crossword puzzle gaming application with hints

Question: What are advantages/disadvantages of:
          a) Fetching hints from server
          b) Preloading hints on device

Expected Answer:
Server-side:
  Pros: Always fresh, smaller app size, can personalize
  Cons: Network dependency, latency, server load
  
Client-side:
  Pros: Instant access, works offline, less server load
  Cons: Larger app size, outdated hints, update challenges
```

**Q4: Video Streaming Buffer Strategy**
```
Question: Should video be buffered on client or streamed in chunks?

Consider:
- Network bandwidth
- Storage constraints
- User experience (latency)
- Server costs
- Adaptive bitrate streaming
```

---

### Pattern 3: Resource Optimization

**Q5: Large XML File Processing**
```
Given: Large XML file that doesn't fit in RAM
       Service needs to process this file

Question: Approaches to optimize?

Expected Answers:
- Streaming/SAX parser (not DOM)
- Chunk-based processing
- Memory-mapped files
- Distributed processing (split file)
- Compression
- Schema optimization
```

**Q6: Database Query Optimization**
```
Given: Slow database queries on large dataset

Approaches:
- Indexing strategies
- Query optimization
- Caching layer
- Database sharding
- Read replicas
- Denormalization
```

---

### Pattern 4: Capacity Planning

**Q7: Smart Engine Service - Budget Planning**
```
Given: Service that takes URLs and extracts useful data

Question: What to consider for budget planning?

Expected Parameters:
- Number of URLs per day
- Processing time per URL
- Storage requirements
- Bandwidth costs
- Server/compute costs
- Caching strategy
- Peak vs average load
- Geographic distribution
```

**Q8: E-commerce Platform Capacity**
```
Plan capacity for e-commerce platform during sale

Consider:
- Peak concurrent users
- Transactions per second
- Database load
- CDN requirements
- Auto-scaling thresholds
```

---

### Pattern 5: Scaling Questions

**Q9: Social Media App - US to Worldwide**
```
Given: Social media app for college students, successful in US

Question: How to scale it worldwide?

Expected Answer:
- Geographic distribution (multiple regions)
- CDN for static content
- Database replication across regions
- Localization (language, content)
- Latency optimization
- Compliance (GDPR, data residency)
- Cultural adaptations
- Payment gateway integrations
```

**Q10: Real-time Chat Application Scaling**
```
Scale from 10K to 10M users

Cover:
- WebSocket connections
- Message queuing
- Database sharding by user/conversation
- Presence service
- Media storage
- Push notifications
```

---

### Pattern 6: Consistency & Database Questions

**Q11: Strong vs Eventual Consistency**
```
Given: Three scenarios
Question: For each, would you use strong consistency or eventual consistency?

Scenarios:
a) Bank account balance display
b) Social media post likes count
c) E-commerce inventory during checkout

Expected Answer:
a) Strong consistency - Money must be accurate
b) Eventual consistency - Likes can be slightly delayed
c) Strong consistency for checkout, eventual for display
   - At checkout: need accurate stock to prevent overselling
   - On product page: approximate count is acceptable

Key Points:
- Strong consistency: CAP theorem, higher latency, ACID
- Eventual consistency: Better performance, BASE, tolerate stale data
- Trade-off: Consistency vs Availability vs Partition Tolerance
```

**Q12: Database JOIN Performance**
```
Given: Large tables with millions of rows
Question: What are concerns with JOINs? How to optimize?

Expected Answer:
- Performance degrades with table size (O(n*m) for nested loop)
- Index on JOIN columns critical
- LEFT JOIN vs INNER JOIN performance
- Denormalization to avoid JOINs
- Materialized views
- Read replicas for JOIN-heavy queries
- Query optimization: EXPLAIN ANALYZE
```

---

### Pattern 7: Infrastructure & Reliability

**Q13: Multiple Servers Uploading to Shared Storage**
```
Given: Multiple application servers uploading files to shared storage (S3/NFS)
Question: What problems could arise? How to handle?

Expected Answer:
- Filename collisions (use UUID or timestamp)
- Race conditions (two servers writing same file)
- Network failures mid-upload (implement retry + idempotency)
- Storage quotas/limits (monitoring, alerts)
- Uneven distribution (some servers overloaded)
- Data consistency (eventual vs immediate)
- Cost considerations (bandwidth, storage)

Solution:
- Use message queue (SQS/Kafka) for upload jobs
- Implement checksum for verification
- Exponential backoff for retries
- Upload to temp location, then move atomically
```

**Q14: Subtitle Generation Service - Thread Management**
```
Given: Service generates subtitles for videos
       Creates new thread per video (CPU-intensive)
       Currently single process on one machine
       
Question: What problems will occur at scale? How to improve?

Expected Answer:
Current Problems:
- Thread exhaustion (too many threads = context switching overhead)
- Single point of failure
- Limited by single machine CPU/memory
- No load balancing

Solutions:
- Thread pool with fixed size (e.g., 10-20 threads)
- Queue-based system (RabbitMQ/SQS)
- Distribute across multiple machines
- Worker pattern: pull jobs from queue
- Auto-scaling based on queue depth
- Progress tracking & failure recovery
```

**Q15: Load Balancer - Algorithms & Trade-offs**
```
Question: Explain different load balancing algorithms and when to use each

Expected Answer:

1. Round Robin:
   - Pros: Simple, fair distribution
   - Cons: Doesn't consider server load
   - Use: Homogeneous servers, stateless apps

2. Least Connections:
   - Pros: Considers active load
   - Cons: More complex tracking
   - Use: Long-lived connections, WebSockets

3. Weighted Round Robin:
   - Pros: Accounts for different server capacities
   - Cons: Static weights need manual update
   - Use: Mixed hardware specs

4. IP Hash:
   - Pros: Session persistence (same client → same server)
   - Cons: Uneven distribution
   - Use: Stateful applications

5. Least Response Time:
   - Pros: Performance-based routing
   - Cons: Complex monitoring
   - Use: Variable workload complexity

Health Checks: All need heartbeat monitoring
```

---

### Pattern 8: Authentication & Security

**Q16: Basic Authentication Flow - UI to Backend**
```
Given: Login page with username/password textboxes
Question: Explain the complete authentication flow from UI to backend

Expected Answer:

1. Frontend (UI):
   - User enters credentials
   - HTTPS POST to /api/login (never GET - credentials in URL)
   - Hash password client-side? (No - false security)
   
2. Network:
   - TLS/HTTPS encryption in transit
   - Prevents man-in-the-middle attacks
   
3. Backend:
   - Receive credentials
   - Hash password (bcrypt/argon2) + salt
   - Compare with stored hash in database
   - Generate JWT or session token
   - Set secure, httpOnly cookie or return token
   
4. Subsequent Requests:
   - Client sends token in Authorization header
   - Backend validates token (signature + expiry)
   - Extract user identity
   
5. Security Considerations:
   - Rate limiting (prevent brute force)
   - MFA/2FA for sensitive operations
   - Session expiry & refresh tokens
   - Password requirements (length, complexity)
   - Account lockout after failed attempts
```

---

### Pattern 9: Content Delivery & Caching

**Q17: Facebook Friends Query Optimization**
```
Given: Users table (user_id, name)
       Friendships table (user_id, friend_id)
       
Question: Query to find number of friends. How to optimize for billions of users?

Expected Answer:

Query:
SELECT u.user_id, u.name, COUNT(f.friend_id) as friend_count
FROM Users u
LEFT JOIN Friendships f ON u.user_id = f.user_id
GROUP BY u.user_id, u.name

Optimizations:
1. Indexes:
   - Index on Friendships(user_id)
   - Composite index on (user_id, friend_id)

2. Denormalization:
   - Store friend_count in Users table
   - Update via triggers or async job
   - Trade: Storage for query speed

3. Caching:
   - Cache popular users' friend counts (celebrities)
   - Redis with TTL
   - 80/20 rule: 20% users = 80% queries

4. Database Sharding:
   - Shard by user_id
   - Each shard handles subset of users
   
5. Read Replicas:
   - Direct COUNT queries to replicas
   - Keep master for writes only
```

**Q18: API Design for Social Media Feed**
```
Question: Design API endpoints for a social media feed (like Twitter/Facebook)

Expected Answer:

Core Endpoints:

1. GET /feed
   - Returns personalized feed for authenticated user
   - Pagination: ?cursor=xyz&limit=20
   - Response: [{post_id, author, content, timestamp, likes, comments}]
   
2. POST /posts
   - Create new post
   - Body: {content, media_urls, visibility}
   - Returns: post_id
   
3. GET /posts/{post_id}
   - Retrieve specific post
   
4. POST /posts/{post_id}/like
   - Like a post (idempotent)
   
5. GET /posts/{post_id}/comments
   - Get comments for post
   - Nested pagination

Design Considerations:
- Feed Algorithm: chronological vs ranked
- Caching: Redis for hot posts
- Real-time Updates: WebSocket for new posts
- Rate Limiting: Prevent spam
- Cursor-based Pagination: Better than offset for large datasets
- Optimistic Updates: Client shows like immediately

Database:
- Posts table: post_id, user_id, content, created_at
- Likes table: user_id, post_id (composite PK)
- Followers table: follower_id, following_id
- Feed pre-computation for popular users
```

---

### Pattern 10: Communication & Messaging

**Q19: Composition vs Inheritance in OOD**
```
Question: When would you use composition over inheritance? Give examples.

Expected Answer:

Inheritance (IS-A):
- Dog IS-A Animal
- Square IS-A Shape
- Use when: True hierarchical relationship

Composition (HAS-A):
- Car HAS-A Engine
- Person HAS-A Address
- Use when: Behavior reuse without "is-a" relationship

Why Composition Often Better:
1. Flexibility: Change behavior at runtime
2. Less Coupling: Components independent
3. Avoid Fragile Base Class Problem
4. Multiple "has-a" relationships (single inheritance limitation)

Example:
// BAD: Inheritance
class Bird extends Flyer { }
class Penguin extends Bird { } // Problem: Can't fly!

// GOOD: Composition
class Bird {
    FlightBehavior flightBehavior;
    void fly() { flightBehavior.fly(); }
}

Dependency Injection: Form of composition
- Inject dependencies (database, services)
- Makes testing easier (mock injection)
- Loose coupling
```

**Q20: Unit Tests, Mocks, Regression Testing**
```
Question: Explain unit testing best practices and mocking

Expected Answer:

Unit Tests:
- Test single function/method in isolation
- Fast execution (milliseconds)
- No external dependencies (database, network)
- FIRST principles: Fast, Independent, Repeatable, Self-validating, Timely

Mocks vs Stubs:
- Mock: Verify interactions (was method called?)
- Stub: Provide canned responses
- Example: Mock database to verify query was called with correct params

Test Structure (AAA):
1. Arrange: Set up test data
2. Act: Execute function
3. Assert: Verify results

Regression Testing:
- Ensure new changes don't break existing features
- Run full test suite on every commit
- CI/CD integration
- Code coverage tracking (aim for 80%+)

Test Pyramid:
- Many unit tests (70%)
- Some integration tests (20%)
- Few E2E tests (10%)

Example:
def test_calculate_total():
    # Arrange
    mock_db = Mock()
    mock_db.get_price.return_value = 10.0
    cart = ShoppingCart(mock_db)
    
    # Act
    total = cart.calculate_total(item_id=1, quantity=2)
    
    # Assert
    assert total == 20.0
    mock_db.get_price.assert_called_once_with(1)
```

---

## 🎤 INTERVIEW-READY ANSWERS (How to Actually Answer in Interview)

### **Q1: Music Streaming with Consistent Hashing - Concerns?**

**Your Answer (4-5 min):**

"While consistent hashing distributes load evenly in theory, I see several concerns:

**1. Hot Content Problem:** Popular songs create hot spots. Even with even distribution, if 70% of requests are for top 100 songs, those servers get hammered regardless of hashing.

**2. Cache Inefficiency:** With consistent hashing alone, the same song gets cached on multiple servers, wasting memory. We need a dedicated caching layer (Redis/CDN) in front.

**3. Replication Strategy:** For high availability, we need replicas. If a node fails, do we have enough replicas? Consistent hashing helps with rebalancing, but we need 3x replication minimum.

**4. Bandwidth Bottlenecks:** Streaming consumes massive bandwidth. We need CDN integration for edge delivery, not just backend consistent hashing.

**5. Peak Hour Handling:** During evening hours (7-10 PM), load isn't "equal" - it spikes everywhere. We need auto-scaling beyond just distribution.

**6. Write vs Read Imbalance:** Uploads are rare, streams are frequent. Consistent hashing treats them equally, but we should optimize read paths separately with CDN + cache layers."

---

### **Q2: Distributed Cache with Consistent Hashing - Design**

**Your Answer (4-5 min):**

"I'll design this in layers:

**Hash Ring Architecture:**
- Use 150-200 virtual nodes per physical server for smoother distribution
- Hash function: MD5 or MurmurHash3 - fast, good distribution
- Clock-wise lookup on ring to find cache server

**Replication:**
- Store each key on 3 consecutive nodes on the ring
- Primary node handles writes, replicas for read redundancy
- If primary fails, promote first replica

**Client-Side vs Server-Side:**
- Client-side hashing is better here - less network hops
- Client maintains hash ring map (updated via gossip protocol)
- Direct connection to cache server after hash calculation

**Failure Handling:**
- Heartbeat every 5 seconds to detect failures
- Remove failed node from ring
- Keys automatically route to next node (minimal rebalancing)
- When node recovers, gradually warm up cache

**Eviction:**
- LRU at individual server level
- TTL for all keys (prevents stale data)

**Edge Cases:**
- Add/remove servers: Only K/N keys move (K=total keys, N=servers)
- Network partition: Consistent hashing helps but need quorum reads for consistency"

---

### **Q3: Crossword Hints - Server vs Preload**

**Your Answer (4-5 min):**

"Let me analyze both approaches:

**Server-Side Fetching:**
- **Pros:** 
  - Fresh hints always (can update puzzles without app update)
  - Smaller app size (~10 MB vs ~100 MB)
  - Can personalize hints based on user history
  - A/B testing different hint strategies
  - Analytics on which hints are used
  
- **Cons:**
  - Network dependency (game broken without internet)
  - Latency 200-500ms per hint fetch
  - Server costs scale with DAU
  - Poor experience on bad networks

**Client-Side Preloading:**
- **Pros:**
  - Instant hint display (0ms latency)
  - Works offline completely
  - Zero server load for hints
  - Predictable user experience
  
- **Cons:**
  - Large app size (100+ MB for thousands of puzzles)
  - Stale hints (typos can't be fixed until next app update)
  - Can't personalize
  - Apple/Google approval needed for each hint update

**My Recommendation:** Hybrid approach:
- Preload last 50 puzzles and their hints (playable offline)
- Lazy load hints for older puzzles from server
- Cache fetched hints locally
- Background sync when on WiFi
- Best of both worlds - works offline but stays fresh"

---

### **Q4: Video Streaming - Buffer vs Chunk Strategy**

**Your Answer (4-5 min):**

"Modern video streaming uses **adaptive chunking**, not full buffering. Here's why:

**Full Buffering (Bad Approach):**
- Downloads entire video upfront
- Wastes bandwidth if user stops watching (60% of videos abandoned)
- Doesn't adapt to network changes
- High storage requirement on device

**Chunked Streaming (Correct Approach):**
- Break video into 2-10 second segments
- Download 3-4 chunks ahead (buffer ~30 seconds)
- Each chunk available in multiple qualities (360p, 720p, 1080p, 4K)

**Adaptive Bitrate (ABR) Strategy:**
- Monitor network throughput every chunk
- If bandwidth drops, fetch lower quality chunks
- If bandwidth improves, upgrade quality
- Algorithms: Buffer-based (if buffer > 30s, upgrade) or Rate-based (if throughput > 5 Mbps, fetch 1080p)

**Implementation:**
- Use HLS (Apple) or DASH (Google) protocols
- CDN delivers chunks from edge locations
- Client-side player (ExoPlayer, AVPlayer) handles ABR logic
- Preload next chunk while current plays

**Storage:** Only keep 30-60 seconds buffered, discard watched chunks.

This balances UX (no buffering), bandwidth efficiency, and quality adaptation."

---

### **Q5: Large XML Processing - Optimization**

**Your Answer (4-5 min):**

"The key issue is the XML is larger than RAM, so in-memory parsing fails. Here are approaches:

**1. Streaming Parser (SAX/StAX) - Best Approach:**
- Don't load entire XML into memory
- Event-driven: reads one element at a time
- Memory: O(1) - only current element in memory
- Process each element, discard, move to next
- Perfect for sequential processing

**2. Chunked Processing:**
- Split XML file into logical chunks (e.g., by user records)
- Process each chunk independently
- Write intermediate results to disk
- Merge results at end
- Parallelizable across multiple workers

**3. Memory-Mapped Files:**
- OS maps file to virtual memory
- Appears in memory but actually on disk
- Pages loaded on-demand
- Good for random access patterns

**4. Distributed Processing:**
- If file is 100GB+, use Spark/Hadoop
- Distribute chunks across cluster
- Each node processes its portion
- Aggregate results

**5. Schema Optimization:**
- If we control XML format, use attributes instead of nested tags (more compact)
- Compress with gzip (10x reduction typically)

**My Choice:** For single-server: SAX parser + chunked writes. For multi-GB scale: distributed processing with Spark."

---

### **Q6: Database Query Optimization**

**Your Answer (4-5 min):**

"I'll approach this systematically:

**1. Indexing (First Fix):**
- Identify slow queries via query logs (queries > 1s)
- Add indexes on WHERE, JOIN, ORDER BY columns
- Composite indexes for multi-column filters
- But: indexes slow writes, so balance read/write ratio

**2. Query Optimization:**
- Use EXPLAIN ANALYZE to see execution plan
- Avoid SELECT * (fetch only needed columns)
- Limit + pagination instead of fetching all rows
- Rewrite subqueries as JOINs
- Remove unnecessary JOINs

**3. Caching Layer:**
- Add Redis/Memcached in front of DB
- Cache hot queries (e.g., homepage data)
- Invalidate cache on writes
- 95% cache hit rate = 20x load reduction

**4. Database Sharding:**
- If single DB can't handle load, shard by user_id or region
- Each shard handles subset of data
- Application routes queries to correct shard

**5. Read Replicas:**
- Master for writes, replicas for reads
- Route read traffic to replicas (5 replicas = 5x read capacity)
- Async replication (slight lag acceptable)

**6. Denormalization:**
- If JOINs are expensive, duplicate data across tables
- Trade storage for query speed
- Use for read-heavy, rarely-updated data

**Approach:** Start with indexing (easiest win), then caching, then replicas, finally sharding (most complex)."

---

### **Q7: Smart Engine Service - Budget Planning**

**Your Answer (4-5 min):**

"For capacity planning, I need to gather these parameters:

**Traffic Metrics:**
- URLs processed per day (e.g., 10 million)
- Peak vs average (peak might be 5x average)
- Processing time per URL (e.g., 2 seconds)
- Success vs error rate (retries needed?)

**Compute Costs:**
- CPU/memory per request (data extraction is CPU-intensive)
- Server requirements: (10M URLs × 2s) / 86400s = 231 servers running 24/7
- But with peak 5x, need 1,150 servers during peak
- Use auto-scaling: 300 base + scale to 1,200
- Cost: AWS EC2 m5.xlarge ($0.192/hr) × 300 × 730 hr/mo = $42,000/mo base

**Storage Costs:**
- Data extracted per URL (e.g., 100 KB)
- Retention period (7 days? 90 days?)
- 10M × 100 KB × 30 days = 30 TB
- S3 storage: 30 TB × $0.023/GB = $690/mo

**Bandwidth:**
- Fetching URLs: 10M × 500 KB download = 5 TB/day
- Egress: 10M × 100 KB = 1 TB/day
- AWS data transfer: 6 TB/day × 30 × $0.09/GB = $16,200/mo

**Caching:**
- If same URLs repeated, cache results (Redis)
- 30% cache hit rate = 30% cost savings

**Total Monthly Budget:** ~$60,000-70,000 for 10M URLs/day.

**Optimization:** Use spot instances (70% cheaper), aggressive caching, regional optimization."

---

### **Q8: E-commerce Platform - Sale Capacity**

**Your Answer (4-5 min):**

"For a major sale event (Black Friday), here's my capacity plan:

**Load Estimation:**
- Normal: 10K concurrent users
- Sale: 500K concurrent users (50x spike)
- Transactions: Normal 100 TPS → Sale 5,000 TPS

**Frontend/CDN:**
- Static assets (images, CSS, JS) → CloudFront CDN (unlimited scale)
- Homepage/product pages → pre-generate and cache
- CDN handles 90% of traffic, origin servers see only 10%

**Application Servers:**
- Auto-scaling group: min 50, max 500 instances
- Scale up trigger: CPU > 70% or latency > 500ms
- Pre-warm 200 instances 1 hour before sale

**Database:**
- Read replicas: 10 replicas (vs normal 2)
- Write master: scale vertically (largest RDS instance)
- Read/write split: 95% reads to replicas
- Connection pooling: max 1000 connections per server

**Caching:**
- Redis cluster: product inventory, user sessions
- Warm cache 2 hours before sale
- 10K products × 1 KB = 10 MB (easily cached)

**Payment Gateway:**
- Coordinate with payment provider (Stripe/PayPal) - alert them
- Queue-based processing: if payment slow, queue requests

**Monitoring:**
- Set alerts: latency > 1s, error rate > 1%
- Have on-call engineers during sale

**Cost:** 50x spike but only 4 hours = 200x normal for 4 hours ≈ 8x daily cost for one day."

---

### **Q9: Social Media App - US to Worldwide**

**Your Answer (4-5 min):**

"Scaling globally involves more than just adding servers:

**Geographic Distribution:**
- Deploy in multiple AWS regions: US-East, EU-West, Asia-Pacific
- Route users to nearest region (Route 53 geo-routing)
- Reduces latency from 500ms → 50ms

**Data Replication:**
- Multi-region database replication
- Master-master or master-slave per region
- Challenge: consistency across regions (eventual consistency acceptable for social media)
- User data stored in home region, replicated globally

**CDN for Static Content:**
- CloudFront edge locations worldwide
- Profile pictures, videos served from nearest edge
- 200+ edge locations globally

**Localization:**
- UI translation: 10-15 major languages
- Content moderation: local language support
- Currency handling: payments in local currency
- Date/time formats: regional preferences

**Compliance:**
- GDPR (Europe): right to delete, data residency
- User data must stay in EU for EU users
- China: separate deployment, local servers (legal requirement)

**Cultural Adaptation:**
- Features vary by region (e.g., WeChat integration in China)
- Content recommendations: local trends
- Privacy settings: stricter defaults in EU

**Performance:**
- GraphQL API gateway in each region
- Websocket connections terminate regionally
- Cross-region traffic only for user-to-user interactions

**Monitoring:**
- Per-region dashboards
- Detect regional outages quickly

Key challenge: balancing global reach with data sovereignty laws."

---

### **Q10: Real-time Chat - 10K to 10M Users**

**Your Answer (4-5 min):**

"Scaling chat 1000x requires architectural changes:

**WebSocket Connections (Critical Bottleneck):**
- Single server: ~10K connections max
- For 10M users: need 1,000 servers just for connections
- Use WebSocket gateway layer (AWS API Gateway Websockets or custom)
- Stateless: any user can connect to any gateway server

**Message Routing:**
- Can't broadcast to all 10M users
- Use presence service: which users online, which gateway they're connected to
- Redis Pub/Sub for message routing between gateway servers
- User A sends message → Gateway 1 → Redis → Gateway 73 (where User B connected) → User B

**Message Storage:**
- Don't keep all messages in memory
- Store in Cassandra/MongoDB (sharded by conversation_id)
- Only load recent messages (last 50) into cache
- Older messages: lazy load on scroll

**Database Sharding:**
- Shard by conversation_id or user_id
- Each shard handles subset of conversations
- 100 shards × 100K users per shard

**Presence Service:**
- Track who's online (Redis)
- Heartbeat every 30s
- If no heartbeat, mark offline
- At 10M scale: 10M / 30s = 333K updates/sec to presence service

**Media/File Sharing:**
- Don't send media through WebSocket
- Upload to S3, send URL through chat
- Images/videos served via CDN

**Push Notifications:**
- When user offline, send push via FCM/APNS
- Queue-based: if 1M users need notification, queue it

**Scalability Numbers:**
- 10M users × 5 KB connection state = 50 GB memory (Redis cluster)
- 1,000 gateway servers (10K connections each)
- 100 DB shards
- Message throughput: 10M users × 10 messages/day = 100M messages/day = 1,200 writes/sec

**Architecture:** WebSocket Gateways → Redis Pub/Sub → Message Queue → Database Shards → S3 for media."

---

## 🎯 DELIVERY TIPS FOR INTERVIEW

### How to Structure Your Answer (4-5 minutes):
1. **Opening (10 seconds):** Start with core concern or approach
   - "The main issue here is..."
   - "I see several concerns..."
   - "I would approach this in layers..."

2. **Main Points (3-4 minutes):** Cover 4-6 key points
   - Use numbered structure in your mind
   - Give concrete examples/numbers when possible
   - Show trade-offs, not just solutions

3. **Closing (30 seconds):** Summary or recommendation
   - "So my approach would be..."
   - "The key trade-off is..."
   - "For this scale, I'd choose..."

### What Makes a Strong Answer:
✅ **Concrete numbers** (shows depth): "10M users × 5KB = 50GB memory"
✅ **Real technologies** (shows experience): "Redis Pub/Sub", "HLS/DASH protocols"
✅ **Trade-offs** (shows maturity): "Pros: X, Y. Cons: A, B. Therefore..."
✅ **Structured thinking** (shows clarity): "I'll cover 3 areas: Architecture, Data, Scaling"
✅ **Practical concerns** (shows real-world exp): "Peak hours 7-10 PM", "60% videos abandoned"

### What to Avoid:
❌ Being too vague: "We'll use caching" → Instead: "Redis cluster, 30GB memory, 95% hit rate"
❌ Going too deep: Don't code during system design, stay high-level
❌ Ignoring interviewer: If they interrupt/redirect, follow their lead
❌ Taking too long: Watch time - 5 min max per question

### Practice Strategy:
- **Record yourself** answering each question (use phone timer - 5 min limit)
- **Practice transitions:** "Let me cover 3 aspects: A, B, C"
- **Memorize key numbers:** 10K connections/server, 2-10s video chunks, 95% cache hit rate
- **Mock with friend:** Have them ask follow-ups

---

## 📋 ADDITIONAL SYSTEM DESIGN ANSWERS (Q11-Q20)

### **Q11: Strong vs Eventual Consistency**

**Your Answer (3-4 min):**

"Let me analyze each scenario based on consistency requirements:

**Scenario A: Bank Account Balance**
- Need: Strong consistency
- Why: Money must be accurate to the cent
- Implementation: ACID transactions, synchronous replication
- User can't see $100 when they actually have $10
- Trade-off: Accept higher latency for correctness

**Scenario B: Social Media Likes Count**
- Need: Eventual consistency
- Why: Seeing 99 vs 101 likes doesn't matter
- Implementation: Asynchronous updates, cache with TTL
- Optimize for speed over perfect accuracy
- Eventually all counters sync up

**Scenario C: E-commerce Inventory**
- Need: Hybrid approach
- Product page display: Eventual (show approximate stock)
- Checkout: Strong consistency (prevent overselling)
- Implementation: 
  - Display can be cached (5 min TTL)
  - At checkout, lock inventory with distributed lock
  - Use optimistic locking with version numbers

**CAP Theorem Trade-off:**
- Strong consistency: Choose CP (Consistency + Partition tolerance)
- Eventual consistency: Choose AP (Availability + Partition tolerance)
- In distributed systems, partition tolerance is mandatory
- So we trade between Consistency and Availability"

---

### **Q12: Database JOIN Performance**

**Your Answer (3-4 min):**

"JOINs on large tables present several performance challenges:

**Performance Issues:**

1. **Time Complexity:** Nested loop JOIN is O(n×m), millions of rows = very slow
2. **Memory:** Large result sets don't fit in memory
3. **Network:** Transferring massive datasets between DB nodes

**Optimization Strategies:**

**1. Indexing (First Priority):**
- Index JOIN columns: `CREATE INDEX idx_user_id ON orders(user_id)`
- Composite indexes for multi-column JOINs
- Query planner uses index for faster lookups

**2. Query Optimization:**
- Use EXPLAIN ANALYZE to see execution plan
- LEFT JOIN vs INNER JOIN: INNER JOIN faster (smaller result set)
- Limit result set: WHERE clause before JOIN
- Avoid SELECT *, fetch only needed columns

**3. Denormalization:**
- Store commonly joined data together
- Example: Store user name in orders table (duplicate data)
- Trade: Storage space for query speed
- Good for read-heavy, rarely-updated data

**4. Materialized Views:**
- Pre-compute JOIN results
- Refresh periodically (hourly/daily)
- Great for reports and analytics

**5. Read Replicas:**
- Route JOIN-heavy queries to replicas
- Keep master for writes only
- Distribute load across 5-10 replicas

**6. Application-Level JOINs:**
- Fetch from table A, then table B separately
- JOIN in application code
- Better control, can cache intermediate results

For our use case: Start with indexing (easiest), then caching, finally denormalization if still slow."

---

### **Q13: Multiple Servers Upload to Shared Storage**

**Your Answer (4-5 min):**

"Multiple servers uploading to shared storage creates several challenges:

**Problems:**

1. **Filename Collisions:**
   - Two servers upload 'image.jpg' simultaneously
   - One overwrites the other
   - Solution: UUID-based naming `{uuid}-image.jpg`

2. **Race Conditions:**
   - Server A starts uploading file
   - Server B tries to read it before it's complete
   - Solution: Write to temp location, atomic move when done

3. **Network Failures:**
   - Upload fails mid-way (partial file)
   - Need retry mechanism
   - Solution: Implement idempotency (same upload = same result)

4. **Consistency:**
   - S3 has eventual consistency for overwrites
   - Server might see old version briefly
   - Solution: Use object versioning, read-after-write consistency

5. **Load Distribution:**
   - Some servers overloaded, others idle
   - Solution: Queue-based approach

**Better Architecture:**

1. **Message Queue Pattern:**
   - Upload job → SQS/Kafka queue
   - Worker servers pull from queue
   - Natural load balancing

2. **Checksum Verification:**
   - Calculate MD5/SHA256 before upload
   - Verify after upload
   - Retry if mismatch

3. **Multipart Upload:**
   - Split large files into chunks
   - Upload chunks in parallel
   - Combine at end (atomic)

4. **Monitoring:**
   - Track upload success/failure rates
   - Alert on high failure rate
   - Storage quota monitoring

5. **Cost Optimization:**
   - S3 transfer acceleration for far regions
   - Lifecycle policies (move to Glacier after 90 days)
   - Compression before upload

This approach ensures reliability and scalability."

---

### **Q14: Subtitle Generation Service - Thread Management**

**Your Answer (4-5 min):**

"The current architecture has critical scaling issues:

**Current Problems:**

1. **Thread Exhaustion:**
   - Creating unlimited threads → context switching overhead
   - Each thread consumes 1-2 MB stack memory
   - 1000 videos = 1000 threads = 2GB just for stacks
   - CPU thrashing when threads >> cores

2. **Single Point of Failure:**
   - One machine crashes = all subtitle jobs lost
   - No redundancy

3. **Resource Limits:**
   - Single machine's CPU/RAM is ceiling
   - Can't scale beyond vertical limits

**Solutions:**

**1. Thread Pool (Immediate Fix):**
```
ThreadPoolExecutor(max_threads=20)
```
- Fixed pool size = controlled resources
- Queues excess jobs
- Still single machine though

**2. Queue-Based Architecture (Better):**
- Upload video → publish to SQS/RabbitMQ
- Multiple worker machines pull jobs
- Each worker has thread pool (10-20 threads)
- Horizontal scaling: add more workers

**3. Worker Distribution:**
```
CloudWatch alarm: Queue depth > 100
→ Auto-scaling: Launch more EC2 workers
→ Each worker pulls jobs from queue
```

**4. Failure Recovery:**
- Job timeout (if processing > 10 min, retry)
- Dead letter queue for failed jobs
- Store progress in database (resume on failure)

**5. Resource Allocation:**
- Short videos: lightweight workers (2 vCPU)
- Long videos: powerful workers (8 vCPU)
- Route to appropriate worker based on video length

**Architecture:**
```
Video Upload → S3
S3 trigger → SQS Queue
Worker Fleet (10-100 machines)
  ↓
Results → S3
Notification → User via SNS
```

**Scaling Numbers:**
- 1 video = 2 min processing
- 1 worker (20 threads) = 10 videos/min = 600/hour
- Need 10,000 videos/hour? → 17 workers
- Auto-scale based on queue depth

This handles millions of videos with automatic scaling and fault tolerance."

---

### **Q15: Load Balancer Algorithms**

**Your Answer (4-5 min):**

"Different load balancing algorithms suit different use cases:

**1. Round Robin:**
- How: Request 1 → Server A, Request 2 → Server B, Request 3 → Server C, repeat
- Pros: Simple, fair distribution
- Cons: Ignores server load (Server A might be overloaded)
- Best for: Homogeneous servers, stateless applications
- Example: Serving static content

**2. Least Connections:**
- How: Route to server with fewest active connections
- Tracks: Active connection count per server
- Pros: Better for long-lived connections
- Cons: More complex tracking, slight overhead
- Best for: WebSocket servers, database connections
- Example: Chat applications

**3. Weighted Round Robin:**
- How: Assign weights (Server A: 3, Server B: 1)
- Server A gets 3 requests for every 1 to Server B
- Pros: Handles different server capacities
- Cons: Static weights (need manual adjustment)
- Best for: Mixed hardware (some powerful, some weak)
- Example: New server with lower capacity

**4. IP Hash:**
- How: Hash(client_IP) % num_servers → consistent server
- Same client always → same server
- Pros: Session persistence (sticky sessions)
- Cons: Uneven distribution if traffic skewed
- Best for: Stateful applications with local cache
- Example: Shopping cart stored in-memory

**5. Least Response Time:**
- How: Route to server with lowest latency
- Tracks: Active connections + response time
- Pros: Performance-aware routing
- Cons: Complex monitoring overhead
- Best for: Variable workload complexity
- Example: API with some slow endpoints

**6. Random:**
- How: Pick server randomly
- Pros: Simplest implementation, even distribution (statistically)
- Cons: No intelligence
- Best for: Quick prototyping

**Health Checks (Essential for All):**
- Heartbeat every 5-10 seconds
- Remove unhealthy servers from pool
- Graceful shutdown (drain connections)

**Real-World Choice:**
For most web apps: Start with Round Robin + Health Checks
For WebSockets: Least Connections
For stateful: IP Hash
For microservices: Least Response Time (service mesh)"

---

### **Q16: Authentication Flow - UI to Backend**

**Your Answer (5 min):**

"Let me walk through the complete authentication flow:

**1. Frontend (User enters credentials):**
```
User inputs: username='alice', password='secret123'
JavaScript: POST /api/login
Body: {username: 'alice', password: 'secret123'}
```
- Important: HTTPS only (TLS encryption)
- Never GET (credentials in URL logged everywhere)
- Don't hash client-side (false security theater)

**2. Network Layer:**
- TLS 1.3 encryption in transit
- Prevents man-in-the-middle attacks
- Certificate validation

**3. Backend API Server:**
```python
def login(username, password):
    # 1. Rate limiting check
    if too_many_attempts(username):
        return 429  # Too Many Requests
    
    # 2. Fetch user from database
    user = db.query("SELECT * FROM users WHERE username=?", username)
    
    # 3. Hash incoming password
    hashed = bcrypt.hash(password, user.salt)
    
    # 4. Compare with stored hash
    if hashed != user.password_hash:
        increment_failed_attempts(username)
        return 401  # Unauthorized
    
    # 5. Generate JWT token
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.now() + timedelta(hours=24)
    }, SECRET_KEY)
    
    # 6. Return token
    return {'token': token, 'user': user.name}
```

**4. Token Storage (Client):**
- Option A: HttpOnly, Secure cookie (safer from XSS)
- Option B: LocalStorage (vulnerable to XSS)
- Best: Secure, HttpOnly, SameSite cookie

**5. Subsequent Requests:**
```
GET /api/profile
Headers:
  Authorization: Bearer <token>
```

Backend validates:
- JWT signature (tamper-proof)
- Expiry timestamp
- Optional: Check revocation list (logged out users)

**Security Measures:**

1. **Password Storage:**
   - Never store plaintext
   - bcrypt/argon2 with salt (not MD5/SHA1)
   - Salt unique per user

2. **Rate Limiting:**
   - 5 failed attempts → 15 min lockout
   - Prevents brute force

3. **Token Expiry:**
   - Access token: 1 hour
   - Refresh token: 7 days
   - Refresh before expiry

4. **MFA/2FA:**
   - TOTP (time-based one-time password)
   - SMS code (less secure)
   - Required for sensitive operations

5. **Account Lockout:**
   - After 5 failed attempts
   - Email notification
   - Unlock link sent to email

This ensures secure authentication with defense in depth."

---

### **Q17: Facebook Friends Query Optimization**

**Your Answer (4 min):**

"For querying friend counts at Facebook scale:

**Basic Query:**
```sql
SELECT u.user_id, u.name, COUNT(f.friend_id) as friend_count
FROM Users u
LEFT JOIN Friendships f ON u.user_id = f.user_id
GROUP BY u.user_id, u.name
```

**Problem at Scale:**
- 3 billion users
- Average 300 friends each
- Friendships table: 900 billion rows
- This query takes minutes

**Optimization 1: Indexing**
```sql
CREATE INDEX idx_friendship_user ON Friendships(user_id);
CREATE INDEX idx_composite ON Friendships(user_id, friend_id);
```
- Speeds up JOIN from sequential scan to index lookup
- O(n) → O(log n) for lookup

**Optimization 2: Denormalization**
```sql
ALTER TABLE Users ADD COLUMN friend_count INT;
```
- Store count directly in Users table
- Update triggers:
```sql
CREATE TRIGGER update_count 
AFTER INSERT ON Friendships
  UPDATE Users SET friend_count = friend_count + 1 
  WHERE user_id = NEW.user_id
```
- Query becomes: `SELECT user_id, name, friend_count FROM Users`
- No JOIN needed → blazing fast

**Optimization 3: Caching Strategy**
- 80/20 rule: 20% of users (celebrities) = 80% of queries
- Cache top 1 million users in Redis
```
Key: "user:123:friend_count"
Value: 543
TTL: 1 hour
```
- Cache hit rate: 95% → 20x load reduction

**Optimization 4: Database Sharding**
- Shard Users by user_id % 100 = 100 shards
- Each shard: 30 million users
- Parallel query across shards
- Application layer aggregates results

**Optimization 5: Read Replicas**
- Master: writes (new friendships)
- 10 read replicas: COUNT queries
- Async replication (slight lag okay)

**Optimization 6: Approximate Counts**
- For users with >10K friends, show "10K+"
- No need for exact count
- HyperLogLog for approximation

**Final Architecture:**
```
Query → Check Redis cache
  → Cache hit? Return
  → Cache miss? Query read replica
    → Store in cache
    → Return
```

This handles billions of queries per day efficiently."

---

### **Q18: Social Media Feed API Design**

**Your Answer (4-5 min):**

"I'll design a scalable social media feed API:

**Core Endpoints:**

**1. GET /api/v1/feed**
```
Authorization: Bearer <token>
Query params:
  - cursor: string (pagination token)
  - limit: int (default 20, max 100)
  
Response:
{
  "posts": [
    {
      "post_id": "123",
      "author": {"user_id": "456", "name": "Alice", "avatar": "url"},
      "content": "Hello world!",
      "media": ["image_url1", "image_url2"],
      "timestamp": "2025-01-15T10:30:00Z",
      "likes_count": 42,
      "comments_count": 5,
      "has_liked": false
    }
  ],
  "next_cursor": "xyz123"
}
```

**2. POST /api/v1/posts**
```
Body:
{
  "content": "My new post",
  "media_urls": ["s3://..."],
  "visibility": "public" | "friends" | "private"
}

Response:
{
  "post_id": "789",
  "created_at": "2025-01-15T10:35:00Z"
}
```

**3. POST /api/v1/posts/{post_id}/like**
- Idempotent: Multiple calls = same result
- Response: 204 No Content

**4. DELETE /api/v1/posts/{post_id}/like**
- Unlike a post

**5. GET /api/v1/posts/{post_id}/comments**
- Nested pagination (cursor-based)

**Design Decisions:**

**1. Cursor-Based Pagination:**
```
cursor = base64(timestamp + post_id)
```
- Better than offset for large datasets
- Offset skip becomes slow (skip 1 million rows)
- Cursor uses index efficiently

**2. Feed Algorithm:**
- Chronological (simple)
- Ranked (complex): engagement score = likes + comments + recency
- Pre-compute feeds for active users (write-intensive)

**3. Database Schema:**
```sql
Posts: post_id, user_id, content, created_at, media_urls
Likes: user_id, post_id (composite PK)
Follows: follower_id, following_id
Comments: comment_id, post_id, user_id, content
```

**4. Feed Generation:**
```
SELECT p.* FROM Posts p
JOIN Follows f ON p.user_id = f.following_id
WHERE f.follower_id = :user_id
ORDER BY p.created_at DESC
LIMIT 20
```

**5. Caching Strategy:**
- User feed: Cache last 100 posts (Redis)
- Popular posts: Cache for 5 minutes
- Likes/comments count: Eventual consistency

**6. Real-Time Updates:**
- WebSocket for live feed updates
- Server pushes new posts
- Client merges into existing feed

**7. Rate Limiting:**
- POST /posts: 10/hour (prevent spam)
- GET /feed: 100/minute
- Use Redis for tracking

**Scalability:**
- Feed pre-computation for users with >1K followers
- Fanout on write: When celebrity posts, push to all follower feeds
- Fanout on read: When normal user requests feed, pull and merge
- Hybrid: Fanout for friends, pull for follows

This design handles millions of daily active users with good UX."

---

### **Q19: Composition vs Inheritance**

**Your Answer (3-4 min):**

"Composition vs Inheritance is a fundamental OOD decision:

**Inheritance (IS-A Relationship):**
```java
class Animal {
    void eat() { }
}
class Dog extends Animal {
    void bark() { }
}
// Dog IS-A Animal ✓
```
- Use when: True hierarchical relationship
- Tightly coupled: Changes in parent affect children

**Composition (HAS-A Relationship):**
```java
class Engine {
    void start() { }
}
class Car {
    private Engine engine; // HAS-A
    Car(Engine e) { this.engine = e; }
    void drive() { engine.start(); }
}
```
- Use when: Behavior reuse without IS-A
- Loosely coupled: Independent components

**Why Composition Often Better:**

**1. Flexibility:**
```java
// Can change behavior at runtime
car.setEngine(new ElectricEngine()); // Composition
// vs inheritance: fixed at compile time
```

**2. Avoid Fragile Base Class:**
```java
// Problem with inheritance:
class Bird extends Flyer { }
class Penguin extends Bird { } // Oops! Penguins can't fly
```
Solution with composition:
```java
interface FlightBehavior {
    void fly();
}
class Bird {
    FlightBehavior flightBehavior;
    void performFly() { flightBehavior.fly(); }
}
class Penguin extends Bird {
    Penguin() {
        flightBehavior = new NoFlight();
    }
}
```

**3. Multiple Behaviors:**
- Java: Single inheritance only
- Composition: Multiple HAS-A relationships
```java
class Person {
    Address address;
    Phone phone;
    Job job;
}
```

**Dependency Injection (Form of Composition):**
```java
class UserService {
    private Database db; // Injected
    UserService(Database db) { this.db = db; }
}
```
Benefits:
- Testability: Inject mock database
- Loose coupling: Swap implementations
- Configuration: Inject different DB in prod vs dev

**When to Use Each:**
- Inheritance: True IS-A (Rectangle IS-A Shape)
- Composition: Behavior reuse, flexibility, testing

**Rule of Thumb:** Favor composition over inheritance (Gang of Four principle)."

---

### **Q20: Unit Testing, Mocks, Regression**

**Your Answer (4 min):**

"Let me explain unit testing best practices:

**Unit Test Characteristics (FIRST):**
- **F**ast: Milliseconds (no network/DB)
- **I**ndependent: Tests don't depend on each other
- **R**epeatable: Same result every time
- **S**elf-validating: Pass/fail, no manual check
- **T**imely: Write with code, not after

**Example Unit Test:**
```python
def test_calculate_discount():
    # Arrange
    product = Product(price=100)
    
    # Act
    discounted = product.calculate_discount(percent=20)
    
    # Assert
    assert discounted == 80
```

**Mocks vs Stubs:**

**Stub:** Returns canned data
```python
class StubDatabase:
    def get_user(self, user_id):
        return {"id": 1, "name": "Alice"}  # Fake data
```

**Mock:** Verifies interactions
```python
def test_create_order():
    mock_db = Mock()
    mock_db.save.return_value = True
    
    service = OrderService(mock_db)
    service.create_order(item="book")
    
    # Verify save was called with correct data
    mock_db.save.assert_called_once_with(
        {'item': 'book', 'status': 'pending'}
    )
```

**When to Mock:**
- External APIs (network calls)
- Databases
- File system
- Time-dependent code (datetime.now())

**Example with Mock:**
```python
def test_send_email_on_order():
    mock_email_service = Mock()
    order_service = OrderService(mock_email_service)
    
    order_service.place_order(user="alice", item="book")
    
    # Verify email sent
    mock_email_service.send.assert_called_once()
```

**Regression Testing:**
- Ensures new code doesn't break existing features
- Run full test suite on every commit
- CI/CD: GitHub Actions, Jenkins
- Code coverage: Aim for 80%+

**Test Pyramid:**
```
      /\
     /E2E\    (10%) - Few, expensive, slow
    /------\
   /  API  \  (20%) - Some, medium cost
  /--------\
 /  UNIT   \ (70%) - Many, cheap, fast
/----------\
```

**Good Practices:**
1. **One Assert Per Test** (easier to debug)
2. **Descriptive Names:** `test_login_fails_with_wrong_password`
3. **No Logic in Tests:** Tests should be simple
4. **Test Edge Cases:** Empty arrays, null, negative numbers
5. **Mock External Dependencies:** Keep tests fast

**Coverage:**
```bash
pytest --cov=myapp
Coverage: 85%
```
- Aim: 80%+ coverage
- Critical paths: 100% (payment, auth)

**CI/CD Integration:**
```yaml
on: push
  run: pytest
  if tests fail: block merge
```

This ensures code quality and prevents regressions."

---

## 💻 DSA PROBLEMS (2 Problems - 30 Minutes)

### Problem Type 1: String Manipulation ⭐ **VERY COMMON**

**DSA 1: Word Wrap Problem**
```python
"""
Given: List of strings and maxLen
Task: Wrap words into lines separated by '-'
      If line length exceeds maxLen, start new line

Example:
Input: ["Hello", "Sir", "Please", "Upvote", "If", "You", "Like", "My", "Post"]
       maxLen = 10

Output: ["Hello-Sir", "Please", "Upvote-If", "You-Like", "My-Post"]

Explanation:
- "Hello-Sir" = 9 chars (fits in 10)
- "Please" = 6 chars (alone)
- "Upvote-If" = 9 chars
- "You-Like" = 8 chars
- "My-Post" = 7 chars

Constraints:
- Words don't exceed maxLen
- Minimize number of lines
- Use '-' as separator
"""

# Solution approach:
def wordWrap(words, maxLen):
    result = []
    current_line = []
    current_length = 0
    
    for word in words:
        word_len = len(word)
        # +1 for the '-' separator
        needed_length = current_length + (1 if current_line else 0) + word_len
        
        if needed_length <= maxLen:
            current_line.append(word)
            current_length = needed_length
        else:
            # Start new line
            result.append('-'.join(current_line))
            current_line = [word]
            current_length = word_len
    
    if current_line:
        result.append('-'.join(current_line))
    
    return result
```

**DSA 2: Text Justification (Harder Variation)**
```python
"""
Given: List of sentences (words separated by space) and exactLen
Task: Generate lines of EXACT length by distributing spaces evenly
      Last line doesn't need padding

Example:
Input: ["The day began as still as the",
        "night abruptly lighted with",
        "brilliant flame"]
       exactLen = 24

Output: ["The--day--began-as-still",
         "as--the--night--abruptly",
         "lighted--with--brilliant",
         "flame"]

Key Points:
- Extra spaces distributed left to right
- Last line: no extra padding
- Single word on line: no padding
"""

# Solution approach:
def textJustification(sentences, exactLen):
    # 1. Split all sentences into words
    # 2. Group words that fit in exactLen
    # 3. Distribute spaces evenly (extra spaces go left to right)
    # 4. Last line: left-aligned only
    pass
```

---

### Problem Type 2: Array/List Problems

**DSA 3: Find Missing Elements**
```python
"""
Given: Array of friend IDs, some IDs are missing

Task: Find all missing IDs in a range

Example:
Input: [1, 2, 4, 6, 7, 10], range: 1-10
Output: [3, 5, 8, 9]
"""
```

**DSA 4: Meeting Rooms**
```python
"""
Given: List of meeting intervals

Task: Find minimum number of meeting rooms required

Example:
Input: [[0, 30], [5, 10], [15, 20]]
Output: 2
"""
```

---

### Problem Type 3: 2D Array/Grid

**DSA 5: Word Search in 2D Grid**
```python
"""
Given: 2D array and target word
Task: Find coordinates where word appears (DFS)

Example:
Input: grid = [['A', 'B', 'C'],
               ['D', 'E', 'F'],
               ['G', 'H', 'I']]
       target = "BEH"

Output: [(0,1), (1,1), (2,1)]  # One valid path
"""
```

---

## 🗣️ HOW TO EXPLAIN DSA PROBLEMS IN INTERVIEW

### The 5-Step Interview Framework (15 minutes per problem):

```
1. CLARIFY (1-2 min)    → Ask questions, confirm understanding
2. APPROACH (2-3 min)   → Explain your strategy before coding
3. CODE (8-10 min)      → Write solution while narrating
4. TEST (2-3 min)       → Walk through example + edge cases
5. OPTIMIZE (1-2 min)   → Discuss time/space complexity, improvements
```

---

## 📝 PROBLEM-BY-PROBLEM INTERVIEW GUIDE

### **DSA 1: Word Wrap Problem - COMPLETE INTERVIEW WALKTHROUGH**

#### **STEP 1: CLARIFY (1-2 min)**

**What to say:**
```
"Let me make sure I understand the problem:
- I have a list of words and a maxLen
- I need to combine words into lines separated by '-'
- Each line can't exceed maxLen characters
- The dash separator counts as a character, right?

Quick clarification questions:
1. Can a single word ever exceed maxLen? 
   → Assume no (they'll tell you)
2. Should I minimize the number of lines?
   → Yes, fit as many words as possible per line
3. Does trailing space count?
   → No, just the words and dashes between them

Got it, let me work through the example..."
```

**Walk through example out loud:**
```
Input: ["Hello", "Sir", "Please", "Upvote", "If"], maxLen = 10

"Hello" = 5 chars
"Hello-Sir" = 5 + 1 + 3 = 9 chars ✓ (fits in 10)
"Hello-Sir-Please" = 9 + 1 + 6 = 16 chars ✗ (exceeds 10)
So first line: "Hello-Sir"

Start new line with "Please" = 6 chars
"Please-Upvote" = 6 + 1 + 6 = 13 chars ✗ (exceeds 10)
So second line: "Please" alone

And so on...
```

---

#### **STEP 2: APPROACH (2-3 min)**

**What to say:**
```
"Here's my approach - it's a greedy algorithm:

1. I'll maintain a current_line list to track words for this line
2. Keep a running count of current_length (words + dashes)
3. For each word:
   - Calculate needed_length = current_length + dash (if not first word) + word_len
   - If it fits (needed_length <= maxLen): add word to current_line
   - If it doesn't fit: 
     * Join current_line with '-' and add to result
     * Start new line with this word
4. Don't forget to add the last line after the loop

Time Complexity: O(n) where n is number of words
Space Complexity: O(n) for the result

Does this approach make sense?"
```

---

#### **STEP 3: CODE (8-10 min) - Talk While You Code**

**What to narrate:**
```python
def wordWrap(words, maxLen):
    # "First, I'll initialize my result array and tracking variables"
    result = []
    current_line = []
    current_length = 0
    
    # "Now I'll iterate through each word"
    for word in words:
        word_len = len(word)
        
        # "Calculate the length if I add this word"
        # "If current_line is empty, no dash needed, otherwise add 1 for dash"
        needed_length = current_length + (1 if current_line else 0) + word_len
        
        # "Check if it fits in maxLen"
        if needed_length <= maxLen:
            # "It fits, so add to current line and update length"
            current_line.append(word)
            current_length = needed_length
        else:
            # "Doesn't fit, so finish current line and start new one"
            result.append('-'.join(current_line))
            current_line = [word]
            current_length = word_len
    
    # "Don't forget the last line - important edge case"
    if current_line:
        result.append('-'.join(current_line))
    
    return result
```

**Key narration points:**
- Explain the `(1 if current_line else 0)` logic: "This adds 1 for the dash only if there are already words in current_line"
- Explain why you reset: "I reset current_line to [word] and current_length to word_len to start fresh"
- Point out the final check: "This handles the last line that's still in current_line after the loop"

---

#### **STEP 4: TEST (2-3 min)**

**What to say:**
```
"Let me test with the given example:
words = ["Hello", "Sir", "Please", "Upvote", "If", "You", "Like", "My", "Post"]
maxLen = 10

Iteration 1: word = "Hello" (5 chars)
  needed_length = 0 + 0 + 5 = 5 ≤ 10 ✓
  current_line = ["Hello"], current_length = 5

Iteration 2: word = "Sir" (3 chars)
  needed_length = 5 + 1 + 3 = 9 ≤ 10 ✓
  current_line = ["Hello", "Sir"], current_length = 9

Iteration 3: word = "Please" (6 chars)
  needed_length = 9 + 1 + 6 = 16 > 10 ✗
  Add "Hello-Sir" to result
  current_line = ["Please"], current_length = 6

...continuing this way...

Final result: ["Hello-Sir", "Please", "Upvote-If", "You-Like", "My-Post"] ✓

Now edge cases:
1. Empty list: words = [] → return []
2. Single word: words = ["Hello"], maxLen = 10 → ["Hello"]
3. All words fit on one line: words = ["Hi", "Ho"], maxLen = 20 → ["Hi-Ho"]
4. Each word needs own line: words = ["Hello", "World"], maxLen = 5 → ["Hello", "World"]

My solution handles all these correctly."
```

---

#### **STEP 5: OPTIMIZE (1-2 min)**

**What to say:**
```
"Time Complexity: O(n) - single pass through all words
Space Complexity: O(n) - result array stores all words

This is already optimal because we need to look at every word once.

Potential variations they might ask:
- What if words can exceed maxLen? → Need to split words (more complex)
- What if we want to minimize lines differently? → Different greedy strategy
- What if maxLen changes per line? → Similar approach with dynamic maxLen

Any questions on my solution?"
```

---

### **DSA 2: Text Justification - COMPLETE WALKTHROUGH**

#### **STEP 1: CLARIFY (1-2 min)**

**What to say:**
```
"Let me understand this problem:
- I need lines of EXACT length (exactLen)
- Distribute spaces evenly between words
- Extra spaces go left to right
- Last line is left-aligned (no extra padding)

Questions:
1. How do I handle a single word on a line? 
   → Left-aligned, no padding
2. If exactLen is 10 and words total 6 chars, I need 4 spaces?
   → Yes, distribute among gaps
3. What if a sentence has multiple words separated by spaces?
   → Treat each space-separated word as separate

Got it."
```

---

#### **STEP 2: APPROACH (2-3 min)**

**What to say:**
```
"This is more complex than basic word wrap. Here's my strategy:

Phase 1: Parse and Group Words
- Split all sentences by spaces to get individual words
- Group words that fit in exactLen (similar to word wrap)

Phase 2: Justify Each Line (except last)
- Calculate total chars used by words
- Calculate total spaces needed: exactLen - total_word_chars
- Calculate gaps between words: num_words - 1
- Distribute spaces: spaces_per_gap = total_spaces // gaps
- Extra spaces: total_spaces % gaps (distribute left to right)

Phase 3: Build Result String
- For each gap, add spaces_per_gap spaces
- For first (extra_spaces) gaps, add one more space
- Last line: just join with single spaces

Let me code this step by step..."
```

---

#### **STEP 3: CODE (8-10 min)**

**What to narrate:**
```python
def textJustification(sentences, exactLen):
    # "First, split all sentences into individual words"
    words = []
    for sentence in sentences:
        words.extend(sentence.split())
    
    # "Now group words into lines that fit in exactLen"
    lines = []
    current_line = []
    current_length = 0  # Just word lengths, not spaces yet
    
    for word in words:
        # "Calculate length with minimum spaces (one space between words)"
        needed = current_length + len(current_line) + len(word)
        # len(current_line) = number of spaces needed (one per existing word)
        
        if needed <= exactLen:
            current_line.append(word)
            current_length += len(word)
        else:
            lines.append(current_line)
            current_line = [word]
            current_length = len(word)
    
    if current_line:
        lines.append(current_line)
    
    # "Now justify each line"
    result = []
    for i, line in enumerate(lines):
        if i == len(lines) - 1:
            # "Last line: left-aligned, no extra padding"
            result.append(' '.join(line))
        elif len(line) == 1:
            # "Single word: left-aligned, no padding"
            result.append(line[0])
        else:
            # "Justify this line to exactLen"
            result.append(justify_line(line, exactLen))
    
    return result

def justify_line(words, exactLen):
    # "Calculate how to distribute spaces"
    total_word_chars = sum(len(word) for word in words)
    total_spaces = exactLen - total_word_chars
    gaps = len(words) - 1
    
    spaces_per_gap = total_spaces // gaps
    extra_spaces = total_spaces % gaps
    
    # "Build the justified line"
    justified = []
    for i, word in enumerate(words):
        justified.append(word)
        if i < len(words) - 1:  # Not the last word
            # "Add base spaces for this gap"
            justified.append('-' * spaces_per_gap)
            # "Add extra space if this is one of the leftmost gaps"
            if i < extra_spaces:
                justified.append('-')
    
    return ''.join(justified)
```

---

#### **STEP 4: TEST (2-3 min)**

**What to say:**
```
"Let me test with the example:
Input: ["The day began as still as the",
        "night abruptly lighted with",
        "brilliant flame"]
exactLen = 24

After splitting: ["The", "day", "began", "as", "still", "as", "the", "night", ...]

Grouping into lines (with min spaces):
Line 1: ["The", "day", "began", "as", "still"]
  → "The" + "day" + "began" + "as" + "still" = 3+3+5+2+5 = 18 chars
  → With min spaces (4 gaps): 18 + 4 = 22 ≤ 24 ✓

Justifying Line 1:
  - Total word chars: 18
  - Total spaces needed: 24 - 18 = 6
  - Gaps: 4
  - Spaces per gap: 6 // 4 = 1
  - Extra spaces: 6 % 4 = 2
  - Result: "The--day--began-as-still" (first 2 gaps get extra space) ✓

Looks correct!"
```

---

#### **STEP 5: OPTIMIZE (1-2 min)**

**What to say:**
```
"Time Complexity: O(n) where n is total number of words
Space Complexity: O(n) for result

This is optimal for this problem. The justification logic is the tricky part,
but once you understand the space distribution, it's straightforward."
```

---

### **DSA 3: Find Missing Elements - WALKTHROUGH**

#### **STEP 1-2: CLARIFY & APPROACH (2 min)**

**What to say:**
```
"Problem: Find missing IDs in a range.
Input: [1, 2, 4, 6, 7, 10], range: 1-10
Output: [3, 5, 8, 9]

Approach 1 (Simple): Convert to set, iterate range, check if missing
Approach 2 (Optimal): Use set for O(1) lookup

I'll use Approach 2 - it's cleaner."
```

---

#### **STEP 3-4: CODE & TEST (10 min)**

```python
def findMissing(ids, start, end):
    # "Convert to set for O(1) lookup"
    id_set = set(ids)
    
    # "Iterate through range and collect missing"
    missing = []
    for i in range(start, end + 1):
        if i not in id_set:
            missing.append(i)
    
    return missing

# "Test:"
# ids = [1, 2, 4, 6, 7, 10], range 1-10
# id_set = {1, 2, 4, 6, 7, 10}
# Check 1: in set ✗, 2: in set ✗, 3: not in set ✓ → add 3
# Check 4: in set ✗, 5: not in set ✓ → add 5
# Check 6-7: in set ✗, 8: not in set ✓ → add 8
# ...
# Result: [3, 5, 8, 9] ✓
```

**Complexity:**
```
"Time: O(n + m) where n = len(ids), m = range size
Space: O(n) for the set"
```

---

### **DSA 4: Meeting Rooms - WALKTHROUGH**

#### **STEP 1-2: CLARIFY & APPROACH (2 min)**

**What to say:**
```
"Problem: Find minimum meeting rooms needed for overlapping meetings.
Input: [[0, 30], [5, 10], [15, 20]]
Output: 2 (meetings [0,30] and [5,10] overlap)

Approach: Sweep line algorithm
1. Create events: start times (+1 room) and end times (-1 room)
2. Sort events by time
3. Track current rooms needed and max rooms

Alternative: Use a min-heap (but sweep line is simpler)."
```

---

#### **STEP 3-4: CODE & TEST (10 min)**

```python
def minMeetingRooms(intervals):
    # "Create events for start and end times"
    events = []
    for start, end in intervals:
        events.append((start, 1))   # Meeting starts, need +1 room
        events.append((end, -1))     # Meeting ends, free up 1 room
    
    # "Sort by time (if tie, process end before start)"
    events.sort(key=lambda x: (x[0], x[1]))
    
    # "Sweep through events and track rooms"
    current_rooms = 0
    max_rooms = 0
    
    for time, delta in events:
        current_rooms += delta
        max_rooms = max(max_rooms, current_rooms)
    
    return max_rooms

# "Test with [[0, 30], [5, 10], [15, 20]]:"
# Events: [(0, 1), (5, 1), (10, -1), (15, 1), (20, -1), (30, -1)]
# Time 0: current = 1, max = 1
# Time 5: current = 2, max = 2  ← Peak
# Time 10: current = 1, max = 2
# Time 15: current = 2, max = 2
# Time 20: current = 1, max = 2
# Time 30: current = 0, max = 2
# Result: 2 ✓
```

**Complexity:**
```
"Time: O(n log n) for sorting
Space: O(n) for events array"
```

---

### **DSA 5: Word Search in 2D Grid (DFS) - WALKTHROUGH**

#### **STEP 1-2: CLARIFY & APPROACH (2 min)**

**What to say:**
```
"Problem: Find a word in 2D grid (can move up/down/left/right).
Input: grid = [['A', 'B', 'C'],
               ['D', 'E', 'F'],
               ['G', 'H', 'I']]
       target = "BEH"
Output: One valid path (can return coordinates or True/False)

Approach: DFS (backtracking)
1. Find all cells matching first character
2. From each, do DFS to find complete word
3. Mark visited cells (avoid revisiting)
4. Backtrack if path doesn't work

Clarifications:
- Can I revisit cells? → No
- Diagonal moves allowed? → No, only 4 directions
- Return path or just True/False? → I'll return True/False (simpler)"
```

---

#### **STEP 3-4: CODE & TEST (12 min)**

```python
def wordSearch(grid, target):
    if not grid or not target:
        return False
    
    rows, cols = len(grid), len(grid[0])
    
    def dfs(r, c, index, visited):
        # "Base case: found entire word"
        if index == len(target):
            return True
        
        # "Boundary checks"
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False
        
        # "Already visited or wrong character"
        if (r, c) in visited or grid[r][c] != target[index]:
            return False
        
        # "Mark as visited"
        visited.add((r, c))
        
        # "Try all 4 directions"
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in directions:
            if dfs(r + dr, c + dc, index + 1, visited):
                return True
        
        # "Backtrack: unmark for other paths"
        visited.remove((r, c))
        return False
    
    # "Try starting from each cell"
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == target[0]:
                if dfs(r, c, 0, set()):
                    return True
    
    return False

# "Test with grid and target='BEH':"
# Start at B (0,1): B matches target[0]
#   Go down to E (1,1): E matches target[1]
#     Go down to H (2,1): H matches target[2]
#       index = 3 = len(target), return True ✓
```

**Complexity:**
```
"Time: O(rows × cols × 4^L) where L = target length (DFS from each cell)
Space: O(L) for recursion depth"
```

---

## 🎯 GENERAL DSA INTERVIEW TIPS

### Communication is Key:
✅ **Think out loud:** "I'm thinking we need to track..."
✅ **Explain before coding:** "My approach is... Does that make sense?"
✅ **Narrate while coding:** "Now I'll iterate through..."
✅ **Point out edge cases:** "I need to handle empty input..."
✅ **Walk through examples:** "Let me trace through with..."

### Time Management (15 min per problem):
- **2 min:** Clarify and discuss approach
- **10 min:** Code while narrating
- **3 min:** Test and discuss complexity

### If You Get Stuck:
1. **Talk through it:** "I'm thinking about..."
2. **Start with brute force:** "The naive approach would be..."
3. **Ask for hints:** "Would a hashmap help here?"
4. **Move forward:** Don't get stuck on syntax

### Common Mistakes to Avoid:
❌ Silent coding (interviewer doesn't know your thought process)
❌ Jumping to code without explaining approach
❌ Not testing with examples
❌ Ignoring edge cases
❌ Poor variable naming (`x`, `y`, `temp`)

### Strong Signals You're Doing Well:
✅ Clear explanation of approach before coding
✅ Clean, readable code with good naming
✅ Handling edge cases proactively
✅ Testing with examples without being asked
✅ Discussing trade-offs and complexity

---

## 📚 ADDITIONAL REAL KARAT PROBLEMS (From Recent Interviews)

### **Problem 6: Subdomain Visit Count**
```python
"""
Given: List of domain visit counts
Task: Count visits for all subdomains

Example:
Input: ["9001 discuss.leetcode.com", "50 yahoo.com", "1 intel.mail.com"]
Output: {
    "9001 discuss.leetcode.com",
    "9001 leetcode.com",
    "9001 com",
    "50 yahoo.com",
    "50 com",
    "1 intel.mail.com",
    "1 mail.com",
    "1 com"
}

Approach:
- Split each entry into count and domain
- Split domain by '.' to get all subdomains
- Use hashmap to aggregate counts
- For "discuss.leetcode.com", subdomains are: "discuss.leetcode.com", "leetcode.com", "com"

Company: Compass
"""

def subdomainVisits(cpdomains):
    count_map = {}
    
    for cpdomain in cpdomains:
        count, domain = cpdomain.split()
        count = int(count)
        
        # Split domain and process all subdomains
        parts = domain.split('.')
        for i in range(len(parts)):
            subdomain = '.'.join(parts[i:])
            count_map[subdomain] = count_map.get(subdomain, 0) + count
    
    return [f"{count} {domain}" for domain, count in count_map.items()]

# Time: O(n * m) where n = number of entries, m = average domain parts
# Space: O(n * m) for the hashmap
```

---

### **Problem 7: Pattern Matching with Words**
```python
"""
Given: Pattern string and list of words
Task: Find which words can be constructed using characters from pattern (in order)

Example:
Input: pattern = "drctkla", words = ["cat", "dada", "breath", "taking", "doll"]
Output: "cat"

Explanation:
Pattern "drctkla" contains d,r,c,t,k,l,a
"cat" needs c,a,t → all present in order in pattern ✓
"breath" needs b,r,e,a,t,h → 'b' not in pattern ✗

Approach:
- For each word, use two pointers
- Try to match each character of word in pattern
- Pattern pointer only moves forward
- If all word characters matched, word is valid

Company: Walmart, Compass
"""

def findMatchingWord(pattern, words):
    def canMatch(word, pattern):
        word_idx = 0
        pattern_idx = 0
        
        while word_idx < len(word) and pattern_idx < len(pattern):
            if word[word_idx] == pattern[pattern_idx]:
                word_idx += 1
            pattern_idx += 1
        
        return word_idx == len(word)
    
    result = []
    for word in words:
        if canMatch(word, pattern):
            result.append(word)
    
    return result

# Time: O(n * m) where n = number of words, m = pattern length
# Space: O(1) excluding output
```

---

### **Problem 8: Singer Song Range**
```python
"""
Given: Singer's vocal range (lowest and highest notes)
       Songs with their note ranges
Task: Find all songs the singer can perform

A note is represented by:
- A letter from A to G
- An octave number (0-9)
- Example: C4, D5, F#3

Note ordering: C0 < C#0 < D0 < ... < B0 < C1 < C#1 < ...

Example:
Input: 
  singer_range = ["C2", "E4"]
  songs = [
    {"name": "Song1", "notes": ["C2", "D3", "E4"]},
    {"name": "Song2", "notes": ["F4", "G5"]},
    {"name": "Song3", "notes": ["A1", "C2", "D2"]}
  ]
Output: ["Song1"]

Explanation:
- Song1: all notes C2-E4 are within singer's range ✓
- Song2: F4, G5 are above E4 ✗
- Song3: A1 is below C2 ✗

Company: PayPal
"""

def canSingSongs(singer_low, singer_high, songs):
    note_order = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    def note_to_number(note):
        # Parse note like "C4" into comparable number
        if '#' in note:
            note_name = note[:2]
            octave = int(note[2:])
        else:
            note_name = note[0]
            octave = int(note[1:])
        
        note_idx = note_order.index(note_name)
        return octave * 12 + note_idx
    
    singer_low_num = note_to_number(singer_low)
    singer_high_num = note_to_number(singer_high)
    
    singable_songs = []
    
    for song in songs:
        can_sing = True
        for note in song['notes']:
            note_num = note_to_number(note)
            if note_num < singer_low_num or note_num > singer_high_num:
                can_sing = False
                break
        
        if can_sing:
            singable_songs.append(song['name'])
    
    return singable_songs

# Time: O(n * m) where n = songs, m = notes per song
# Space: O(1) excluding output
```

---

### **Problem 9: Robot Factory Parts**
```python
"""
Given: List of available parts in factory bin
       Required parts to build one robot (comma-separated string)
Task: Determine how many complete robots can be built

Example:
Input: 
  parts = ["head", "body", "leg", "leg", "arm", "arm", "head", "body"]
  required = "head,body,leg,leg,arm,arm"
Output: 1

Explanation:
Need: 1 head, 1 body, 2 legs, 2 arms
Have: 2 heads, 2 bodies, 2 legs, 2 arms
Limiting factor: legs (have 2, need 2 per robot) = 1 robot

Company: Atlassian P50
"""

def getRobotsBuilt(parts, required):
    from collections import Counter
    
    # Count available parts
    available = Counter(parts)
    
    # Count required parts per robot
    required_parts = required.split(',')
    required_count = Counter(required_parts)
    
    # Find minimum number of robots we can build
    min_robots = float('inf')
    
    for part, count_needed in required_count.items():
        if part not in available:
            return 0
        
        robots_possible = available[part] // count_needed
        min_robots = min(min_robots, robots_possible)
    
    return min_robots if min_robots != float('inf') else 0

# Time: O(n + m) where n = parts, m = required parts
# Space: O(n + m) for counters
```

---

### **Problem 10: Longest Common Subsequence for Two Users**
```python
"""
Given: Two users' browsing patterns (sequences of page visits)
Task: Find longest common subsequence of pages visited by both

Example:
Input: 
  user1 = ["hi", "bye", "hello", "leetcode", "start", "end"]
  user2 = ["hello", "hi", "bye", "start", "end"]
Output: ["hi", "bye", "start", "end"] (length 4)

Explanation:
Common pages that appear in same relative order

Company: Wayfair
"""

def longestCommonPattern(user1, user2):
    m, n = len(user1), len(user2)
    
    # DP approach: dp[i][j] = length of LCS ending at user1[i], user2[j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if user1[i-1] == user2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    # Backtrack to find the actual sequence
    result = []
    i, j = m, n
    while i > 0 and j > 0:
        if user1[i-1] == user2[j-1]:
            result.append(user1[i-1])
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            i -= 1
        else:
            j -= 1
    
    return result[::-1]

# Time: O(m * n)
# Space: O(m * n)
```

---

### **Problem 11: Basic Calculator (Progressive)**
```python
"""
Implement calculator that evaluates expressions:
Part 1: Addition and subtraction only
Part 2: Add multiplication and division
Part 3: Add parentheses support

Example:
Input: "3 + 5 * 2 - 4"
Output: 9

Company: Roblox
"""

def calculate(s):
    """
    Handles +, -, *, / with correct precedence
    """
    def helper(s, idx):
        stack = []
        num = 0
        operator = '+'
        
        while idx < len(s):
            char = s[idx]
            
            if char.isdigit():
                num = num * 10 + int(char)
            
            if char == '(':
                num, idx = helper(s, idx + 1)
            
            if char in '+-*/)' or idx == len(s) - 1:
                if operator == '+':
                    stack.append(num)
                elif operator == '-':
                    stack.append(-num)
                elif operator == '*':
                    stack.append(stack.pop() * num)
                elif operator == '/':
                    stack.append(int(stack.pop() / num))
                
                if char == ')':
                    return sum(stack), idx
                
                operator = char
                num = 0
            
            idx += 1
        
        return sum(stack), idx
    
    result, _ = helper(s, 0)
    return result

# Time: O(n)
# Space: O(n) for stack
```

---

### **Problem 12: Teleporter Reachability (Graph Problem)**
```python
"""
Given: Board game with teleporters
       Board size and teleporter mappings
Task: Determine if player can reach the end

Example:
Input: 
  board_size = 20
  teleporters = {3: 15, 8: 4, 12: 18, 19: 7}
  (position 3 teleports to 15, etc.)
  
Output: True/False if end is reachable

Approach: BFS/DFS to check reachability

Company: Atlassian P40
"""

def canReachEnd(board_size, teleporters):
    visited = set()
    queue = [1]  # Start at position 1
    visited.add(1)
    
    while queue:
        pos = queue.pop(0)
        
        # Check if we reached the end
        if pos == board_size:
            return True
        
        # Try dice rolls (1-6)
        for dice in range(1, 7):
            next_pos = pos + dice
            
            if next_pos > board_size:
                continue
            
            # Check if there's a teleporter
            if next_pos in teleporters:
                next_pos = teleporters[next_pos]
            
            if next_pos not in visited:
                visited.add(next_pos)
                queue.append(next_pos)
    
    return False

# Time: O(board_size)
# Space: O(board_size)
```

---

## 🎓 REAL INTERVIEW INSIGHTS (From LeetCode Discussions)

### Common Companies Using Karat:
✅ **Atlassian** - Most reported (P30, P40, P50 levels)
✅ **Indeed** - Very common
✅ **PayPal** - Frequent
✅ **Walmart** - Backend/Data Engineering
✅ **Wayfair** - Senior Engineer
✅ **Coinbase** - IC4 level
✅ **Palantir** - SDE roles
✅ **Compass** - Phone screens
✅ **Roblox** - All levels

### Interview Format Consistency:
📋 **Duration:** Exactly 60 minutes
📋 **Intro:** 3-5 minutes (interviewer script + your intro)
📋 **System Design:** 20-25 minutes (5 rapid-fire questions)
📋 **DSA:** 30-35 minutes (2 medium problems)
📋 **Platform:** Karat's custom IDE with live interviewer

### Success Rate Patterns:
- **Pass Rate:** ~60-70% reported
- **Critical Factor:** Time management (most failures due to spending too long on SD or first DSA)
- **Redo Opportunity:** Some companies allow one redo if you feel interview didn't go well

### Red Flags to Avoid:
❌ Taking >5 min on any single system design question
❌ Not completing at least 1 DSA problem fully
❌ Silent coding (not explaining your thought process)
❌ Asking to reschedule more than once
❌ Not testing your code with examples

### Green Flags (What Works):
✅ Answering SD questions in 3-4 minutes each (shows breadth)
✅ Starting DSA with clarifying questions (shows communication)
✅ Thinking out loud constantly
✅ Testing with edge cases without being asked
✅ Clean, readable code with good variable names
✅ Asking for hints if stuck (better than silence)

### Actual Feedback Examples:
**Strong Pass:**
- "Clear communication throughout"
- "Solid system design knowledge"
- "Clean, working code with good testing"
- "Strong problem-solving approach"

**Reject:**
- "Poor time management"
- "Weak system design skills"
- "Code had bugs, didn't test"
- "Struggled with basic concepts"

---

## 🔥 MUST-KNOW PATTERNS FOR KARAT

### String Manipulation (40% of DSA):
1. **Word Wrap / Text Justification** ⭐⭐⭐ (VERY COMMON)
2. **Pattern Matching** (subsequence, substring)
3. **Domain/URL Parsing** (split, aggregate)
4. **Calculator** (expression evaluation)

### Array/List (30% of DSA):
1. **Missing Elements** (set-based)
2. **Interval Problems** (meeting rooms)
3. **Longest Common Subsequence**
4. **Counting/Grouping** (hashmap patterns)

### Graph/Grid (20% of DSA):
1. **Word Search** (DFS/backtracking)
2. **Reachability** (BFS/DFS)
3. **Path Finding**

### Math/Logic (10% of DSA):
1. **Note/Music Range** (custom comparisons)
2. **Resource Allocation** (robot parts)

### System Design Topics (100% Asked):
1. **Caching** (Redis, CDN, strategies)
2. **Consistency** (Strong vs Eventual)
3. **Load Balancing** (algorithms, pros/cons)
4. **Database** (sharding, replication, optimization)
5. **Scaling** (horizontal, vertical, bottlenecks)
6. **Trade-offs** (client vs server, sync vs async)

---

## ✅ PREPARATION STRATEGY FOR KARAT

### System Design Prep (20-25 minutes):
1. **Practice rapid-fire answers** (4-5 min each)
2. **Focus on high-level concepts**, not implementation
3. **Know common patterns:**
   - Caching strategies
   - Load balancing
   - Database optimization
   - Scaling approaches
   - Trade-off analysis

### DSA Prep (30 minutes):
1. **Must Practice:**
   - Word wrap variations (3-4 problems)
   - Text justification
   - String manipulation
   - Array problems (medium level)

2. **Time Management:**
   - 15 min per problem
   - Write clean, working code
   - Test with examples
   - Handle edge cases

### Mock Interview:
- Set timer for 60 minutes
- Do 5 SD questions (25 min) + 2 DSA (35 min)
- Practice explaining thought process
- Get comfortable with time pressure

---
## 📝 FINAL PRE-INTERVIEW CHECKLIST

### 📅 1 Week Before
- [ ] Identify your interview format (A: SD+DSA or B: Project+Knowledge+Coding)
- [ ] Practice Karat Studio interface (request access from recruiter)
- [ ] Prepare 2-3 project stories using STAR method
- [ ] Review data structures & algorithms fundamentals
- [ ] Practice 10-15 LeetCode medium problems

### 📅 2-3 Days Before
- [ ] Mock interview with timer (60 min exactly)
- [ ] Review all knowledge questions (DS, algorithms, complexity)
- [ ] Test your setup: Internet, webcam, microphone, headphones
- [ ] Test Chrome/Firefox browser
- [ ] Find quiet location for interview

### 📅 Day Before
- [ ] Review this entire document (focus on your format)
- [ ] Practice explaining 1-2 projects out loud
- [ ] Quick review: HashMap internals, BFS vs DFS, Big-O
- [ ] Prepare workspace: Clean desk, good lighting, close other apps
- [ ] Charge laptop, test backup internet (phone hotspot)
- [ ] Get good sleep (seriously!)

### 📅 1 Hour Before
- [ ] Review format-specific tips above
- [ ] Close all unnecessary browser tabs
- [ ] Close Slack, email, notifications
- [ ] Test audio/video in Karat Studio
- [ ] Have water nearby
- [ ] Bathroom break
- [ ] Deep breaths, you got this!

### 🎯 During Interview Checklist

**First 2 Minutes:**
- [ ] Greet interviewer warmly
- [ ] Confirm audio/video working
- [ ] Listen to full problem before asking questions

**During Problem Solving:**
- [ ] Ask clarifying questions
- [ ] Explain approach before coding
- [ ] Think out loud constantly
- [ ] Write clean, readable code
- [ ] Use descriptive variable names
- [ ] Test with example
- [ ] Mention edge cases

**If Stuck:**
- [ ] Ask for hint (better than silence)
- [ ] State what you're thinking
- [ ] Try brute force first, then optimize
- [ ] Keep moving forward

**Last 5 Minutes:**
- [ ] Summarize solution
- [ ] State time/space complexity
- [ ] Ask if interviewer has questions
- [ ] Thank them for their time

---

## 🚀 FINAL TIPS FOR SUCCESS

### Communication is 50% of the Score
- Silence = Red flag
- Thinking out loud = Shows problem-solving process
- Asking questions = Shows curiosity and thoroughness

### Technical Skills are the Other 50%
- Working code > Perfect code
- Tested code > Untested code
- Explained code > Unexplained code

### Time Management Strategy

**Format A (SD + DSA):**
```
0-5 min:   Introductions
5-25 min:  System Design (4 min per question × 5)
25-40 min: DSA Problem 1 (15 min)
40-55 min: DSA Problem 2 (15 min)
55-60 min: Questions for interviewer
```

**Format B (Project + Knowledge + Coding):**
```
0-5 min:   Introductions
5-20 min:  Project Discussion (STAR method)
20-30 min: Knowledge Questions (2-3 min each)
30-55 min: Multi-part Coding (start easy, progress harder)
55-60 min: Questions for interviewer
```

### Common Mistakes to Avoid
❌ Starting to code without explaining approach
❌ Coding in silence
❌ Not testing your code
❌ Giving up when stuck
❌ Going over time on one section
❌ Bad variable names (`x`, `temp`, `arr1`)
❌ Not handling edge cases
❌ Forgetting to ask questions

### What Strong Candidates Do
✅ Ask clarifying questions immediately
✅ Explain approach clearly before coding
✅ Think out loud constantly
✅ Write clean, readable code
✅ Test with examples without being asked
✅ Handle edge cases proactively
✅ State time/space complexity
✅ Ask for hints when genuinely stuck
✅ Stay calm and positive throughout

---

## 🎓 REMEMBER

> **Karat interviews are designed to be collaborative, not adversarial.**

The interviewer **wants** you to succeed. They will:
- Answer your questions
- Provide hints if you're stuck
- Guide you if you go off track
- Give you time to think

Your goal:
- Show your problem-solving process
- Communicate clearly
- Write working code
- Stay positive even when stuck

---

## 💪 YOU'VE GOT THIS!

You've prepared:
- ✅ 20 System Design questions with answers
- ✅ 12 DSA problems with walkthroughs
- ✅ Knowledge questions on DS, algorithms, complexity
- ✅ Project discussion STAR template
- ✅ Complete interview framework

**Trust your preparation. Think out loud. Stay calm. You'll do great!**

---

**Last Updated:** 2025
**Format:** Karat Technical Screening Round
**Good luck! 🚀**
