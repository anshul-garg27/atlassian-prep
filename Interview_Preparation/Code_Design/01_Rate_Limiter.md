# 🌟 PROBLEM 1: RATE LIMITER / TOKEN BUCKET

### ⭐⭐⭐⭐⭐ **Design a Rate Limiting System**

**Frequency:** Appears in **HIGH FREQUENCY** of Atlassian LLD rounds!
**Difficulty:** Medium-Hard
**Focus:** Concurrency, Design Patterns, System Design

---

## 📋 Problem Statement

Design a `RateLimiter` library/class that limits the number of requests a user/client can make within a given time window.

**Core Requirements:**
- Track requests per client/user
- Allow/deny requests based on configured limits
- Support multiple rate limiting algorithms
- Thread-safe for concurrent requests
- Efficient memory usage

**Input:** `clientId` (String), `timestamp` (long)
**Output:** `boolean` (true = allowed, false = denied)

**Constraints:**
- 1 ≤ Number of clients ≤ 1,000,000
- 1 ≤ Requests per second ≤ 10,000 per client
- Time window: 1 second to 1 hour
- Must handle concurrent requests (multi-threaded)

---

## 🎨 Visual Example

```text
Rate Limit: 5 requests per 10 seconds

Timeline (seconds):
0s  1s  2s  3s  4s  5s  6s  7s  8s  9s  10s 11s 12s
│   │   │   │   │   │   │   │   │   │   │   │   │
R1✓ R2✓ R3✓ R4✓ R5✓ R6✗ R7✗ R8✗ R9✗ R10✗ R11✓ R12✓ R13✓
                    (denied - limit reached)

At 10s: R1 expires, so R11 is allowed
At 11s: R2 expires, so R12 is allowed
```

---

## 💡 Algorithm Approaches

### **Approach 1: Fixed Window Counter** ⭐⭐⭐
**Concept:** Divide time into fixed windows, count requests in current window

```text
Window: 10 seconds
Time:   0-10s   10-20s  20-30s
Count:    5       3       7
```

**Pros:**
- Simple to implement
- Memory efficient: O(1) per client
- Fast: O(1) for allow/deny check

**Cons:**
- **Burst problem** at window boundaries
  - Example: 5 req at 9.9s + 5 req at 10.1s = 10 req in 0.2s!
- Not smooth distribution

---

### **Approach 2: Sliding Window Log** ⭐⭐⭐⭐⭐
**Concept:** Store timestamps of all requests, remove expired ones

```text
Limit: 5 requests per 10 seconds
Current time: 15s

Timestamp queue: [7s, 9s, 12s, 14s, 15s]
                  ↑ expired (15-10=5s), remove

Clean queue: [9s, 12s, 14s, 15s] → Count = 4 < 5 → ALLOW
```

**Pros:**
- Precise rate limiting
- No burst problem
- Smooth distribution

**Cons:**
- Memory: O(N) where N = max requests in window
- Cleanup overhead

---

### **Approach 3: Sliding Window Counter** ⭐⭐⭐⭐
**Concept:** Combine Fixed Window + Weighted calculation

```text
Limit: 10 requests per minute
Current time: 00:45 (45 seconds into minute)

Previous window (00:00-01:00): 8 requests
Current window (01:00-02:00): 4 requests

Estimated count = (previous × overlap%) + current
                = (8 × 15/60) + 4
                = 2 + 4 = 6 < 10 → ALLOW
```

**Pros:**
- More accurate than Fixed Window
- Memory efficient: O(1)
- Smooth approximation

**Cons:**
- Not 100% precise
- Approximation can allow slight bursts

---

### **Approach 4: Token Bucket** ⭐⭐⭐⭐⭐ (RECOMMENDED)
**Concept:** Bucket has tokens, refilled at fixed rate

```text
Capacity: 10 tokens
Refill rate: 1 token per second

Time  Tokens  Action
0s      10    Request → consume 1 → 9 left
1s      10    Refilled to 10
2s      10    10 requests → all consumed → 0 left
3s       1    Refilled +1 → 1 available
```

**Pros:**
- Handles bursts gracefully (up to capacity)
- Memory efficient: O(1)
- Industry standard (used by AWS, GCP)
- Smooth rate limiting

**Cons:**
- Slightly complex implementation
- Requires timestamp tracking for refills

---

## 🔧 Implementation: Token Bucket (Best Approach)

### **Java Implementation**

```java
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.locks.ReentrantLock;

/**
 * Token Bucket Rate Limiter
 * Thread-safe implementation using ConcurrentHashMap + ReentrantLock per client
 */
public class RateLimiter {

    private final ConcurrentHashMap<String, TokenBucket> buckets;
    private final int maxTokens;
    private final double refillRate; // tokens per second

    public RateLimiter(int maxTokens, double refillRate) {
        this.buckets = new ConcurrentHashMap<>();
        this.maxTokens = maxTokens;
        this.refillRate = refillRate;
    }

    public boolean allowRequest(String clientId) {
        TokenBucket bucket = buckets.computeIfAbsent(
            clientId,
            k -> new TokenBucket(maxTokens, refillRate)
        );
        return bucket.tryConsume();
    }

    private static class TokenBucket {
        private final ReentrantLock lock = new ReentrantLock();
        private final int capacity;
        private final double refillRate;
        private double tokens;
        private long lastRefillTimestamp;

        public TokenBucket(int capacity, double refillRate) {
            this.capacity = capacity;
            this.refillRate = refillRate;
            this.tokens = capacity;
            this.lastRefillTimestamp = System.currentTimeMillis();
        }

        public boolean tryConsume() {
            lock.lock();
            try {
                refill();

                if (tokens >= 1) {
                    tokens -= 1;
                    return true; // Request allowed
                }
                return false; // Request denied
            } finally {
                lock.unlock();
            }
        }

        private void refill() {
            long now = System.currentTimeMillis();
            double elapsed = (now - lastRefillTimestamp) / 1000.0; // seconds
            double tokensToAdd = elapsed * refillRate;

            tokens = Math.min(capacity, tokens + tokensToAdd);
            lastRefillTimestamp = now;
        }
    }
}
```

**Usage Example:**
```java
// 5 requests per second per client
RateLimiter limiter = new RateLimiter(5, 5.0);

// Client "user123" makes requests
boolean allowed1 = limiter.allowRequest("user123"); // true
boolean allowed2 = limiter.allowRequest("user123"); // true
// ... 3 more requests ...
boolean allowed6 = limiter.allowRequest("user123"); // false (rate limit exceeded)

Thread.sleep(1000); // Wait 1 second (5 tokens refilled)
boolean allowed7 = limiter.allowRequest("user123"); // true
```

---

### **Python Implementation**

```python
import threading
import time
from collections import defaultdict

class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.refill_rate = refill_rate  # tokens per second
        self.tokens = capacity
        self.last_refill = time.time()
        self.lock = threading.Lock()

    def try_consume(self):
        with self.lock:
            self._refill()

            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False

    def _refill(self):
        now = time.time()
        elapsed = now - self.last_refill
        tokens_to_add = elapsed * self.refill_rate

        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now


class RateLimiter:
    def __init__(self, max_tokens, refill_rate):
        self.buckets = {}
        self.max_tokens = max_tokens
        self.refill_rate = refill_rate
        self.lock = threading.Lock()

    def allow_request(self, client_id):
        if client_id not in self.buckets:
            with self.lock:
                if client_id not in self.buckets:
                    self.buckets[client_id] = TokenBucket(
                        self.max_tokens,
                        self.refill_rate
                    )

        return self.buckets[client_id].try_consume()


# Usage
limiter = RateLimiter(max_tokens=5, refill_rate=5.0)

for i in range(10):
    allowed = limiter.allow_request("user123")
    print(f"Request {i+1}: {'✓ Allowed' if allowed else '✗ Denied'}")
```

---

## 🚨 Alternative Approach: Sliding Window Log

```java
import java.util.*;
import java.util.concurrent.*;

public class SlidingWindowRateLimiter {

    private final ConcurrentHashMap<String, Deque<Long>> requestTimestamps;
    private final int maxRequests;
    private final long windowMs;

    public SlidingWindowRateLimiter(int maxRequests, long windowMs) {
        this.requestTimestamps = new ConcurrentHashMap<>();
        this.maxRequests = maxRequests;
        this.windowMs = windowMs;
    }

    public synchronized boolean allowRequest(String clientId) {
        long now = System.currentTimeMillis();
        Deque<Long> timestamps = requestTimestamps.computeIfAbsent(
            clientId,
            k -> new LinkedList<>()
        );

        // Remove expired timestamps
        while (!timestamps.isEmpty() && now - timestamps.peekFirst() > windowMs) {
            timestamps.pollFirst();
        }

        // Check if limit exceeded
        if (timestamps.size() < maxRequests) {
            timestamps.addLast(now);
            return true;
        }

        return false;
    }
}
```

---

## 🎯 Design Patterns Used

### **1. Strategy Pattern**
Support multiple rate limiting algorithms

```java
public interface RateLimitStrategy {
    boolean allowRequest(String clientId, long timestamp);
}

public class TokenBucketStrategy implements RateLimitStrategy { }
public class SlidingWindowStrategy implements RateLimitStrategy { }
public class FixedWindowStrategy implements RateLimitStrategy { }

public class RateLimiter {
    private RateLimitStrategy strategy;

    public RateLimiter(RateLimitStrategy strategy) {
        this.strategy = strategy;
    }

    public boolean allowRequest(String clientId) {
        return strategy.allowRequest(clientId, System.currentTimeMillis());
    }
}
```

### **2. Singleton Pattern**
Single global rate limiter instance

```java
public class RateLimiter {
    private static volatile RateLimiter instance;

    private RateLimiter() {}

    public static RateLimiter getInstance() {
        if (instance == null) {
            synchronized (RateLimiter.class) {
                if (instance == null) {
                    instance = new RateLimiter(100, 10.0);
                }
            }
        }
        return instance;
    }
}
```

---

## 🧪 Testing Strategy

### **Unit Tests**

```java
@Test
public void testBasicRateLimit() {
    RateLimiter limiter = new RateLimiter(3, 3.0); // 3 req/sec

    // First 3 should pass
    assertTrue(limiter.allowRequest("user1"));
    assertTrue(limiter.allowRequest("user1"));
    assertTrue(limiter.allowRequest("user1"));

    // 4th should fail
    assertFalse(limiter.allowRequest("user1"));
}

@Test
public void testRefill() throws InterruptedException {
    RateLimiter limiter = new RateLimiter(2, 2.0);

    // Consume all tokens
    assertTrue(limiter.allowRequest("user1"));
    assertTrue(limiter.allowRequest("user1"));
    assertFalse(limiter.allowRequest("user1"));

    // Wait 1 second (2 tokens refilled)
    Thread.sleep(1000);
    assertTrue(limiter.allowRequest("user1"));
}

@Test
public void testMultipleClients() {
    RateLimiter limiter = new RateLimiter(2, 2.0);

    // Different clients have separate buckets
    assertTrue(limiter.allowRequest("user1"));
    assertTrue(limiter.allowRequest("user2"));
    assertTrue(limiter.allowRequest("user1"));
    assertTrue(limiter.allowRequest("user2"));
}

@Test
public void testConcurrency() throws InterruptedException {
    RateLimiter limiter = new RateLimiter(100, 100.0);
    ExecutorService executor = Executors.newFixedThreadPool(10);
    AtomicInteger allowed = new AtomicInteger(0);
    AtomicInteger denied = new AtomicInteger(0);

    for (int i = 0; i < 200; i++) {
        executor.submit(() -> {
            if (limiter.allowRequest("user1")) {
                allowed.incrementAndGet();
            } else {
                denied.incrementAndGet();
            }
        });
    }

    executor.shutdown();
    executor.awaitTermination(5, TimeUnit.SECONDS);

    assertEquals(100, allowed.get());
    assertEquals(100, denied.get());
}
```

---

## ⚠️ Edge Cases & Error Handling

### **1. Negative/Zero Configuration**
```java
public RateLimiter(int maxTokens, double refillRate) {
    if (maxTokens <= 0) {
        throw new IllegalArgumentException("Max tokens must be positive");
    }
    if (refillRate <= 0) {
        throw new IllegalArgumentException("Refill rate must be positive");
    }
    // ...
}
```

### **2. Clock Drift / Time Going Backwards**
```java
private void refill() {
    long now = System.currentTimeMillis();

    // Handle clock going backwards
    if (now < lastRefillTimestamp) {
        lastRefillTimestamp = now;
        return;
    }

    // ... refill logic
}
```

### **3. Memory Cleanup (for Sliding Window)**
```java
// Periodic cleanup of inactive clients
ScheduledExecutorService cleanup = Executors.newSingleThreadScheduledExecutor();
cleanup.scheduleAtFixedRate(() -> {
    long now = System.currentTimeMillis();
    buckets.entrySet().removeIf(entry -> {
        return now - entry.getValue().lastRefillTimestamp > 3600000; // 1 hour
    });
}, 1, 1, TimeUnit.HOURS);
```

### **4. Null Client ID**
```java
public boolean allowRequest(String clientId) {
    if (clientId == null || clientId.isEmpty()) {
        throw new IllegalArgumentException("Client ID cannot be null or empty");
    }
    // ...
}
```

---

## 🔥 Common Interview Follow-ups

### **Q1: How would you handle distributed systems?**
**Answer:**
- Use **Redis** with `INCR` + `EXPIRE` for Fixed Window
- Use **Redis Sorted Sets** for Sliding Window (timestamps as scores)
- Token Bucket: Store `(tokens, last_refill)` in Redis with Lua script for atomic operations

```lua
-- Redis Lua script for Token Bucket
local key = KEYS[1]
local capacity = tonumber(ARGV[1])
local refill_rate = tonumber(ARGV[2])
local now = tonumber(ARGV[3])

local bucket = redis.call('HMGET', key, 'tokens', 'last_refill')
local tokens = tonumber(bucket[1]) or capacity
local last_refill = tonumber(bucket[2]) or now

-- Refill
local elapsed = now - last_refill
local new_tokens = math.min(capacity, tokens + elapsed * refill_rate)

-- Try consume
if new_tokens >= 1 then
    redis.call('HMSET', key, 'tokens', new_tokens - 1, 'last_refill', now)
    return 1
else
    return 0
end
```

### **Q2: How to handle VIP users with higher limits?**
**Answer:**
```java
public class TieredRateLimiter {
    private Map<String, Integer> userTiers; // userId -> tier
    private Map<Integer, RateLimiter> tierLimiters; // tier -> limiter

    public boolean allowRequest(String userId) {
        int tier = userTiers.getOrDefault(userId, 1); // Default tier 1
        RateLimiter limiter = tierLimiters.get(tier);
        return limiter.allowRequest(userId);
    }
}
```

### **Q3: How to implement rate limiting per API endpoint?**
**Answer:**
```java
public boolean allowRequest(String userId, String endpoint) {
    String key = userId + ":" + endpoint;
    return buckets.computeIfAbsent(key, k -> new TokenBucket(...)).tryConsume();
}
```

### **Q4: What about credit system (unused requests carry over)?**
**Answer:**
- Token Bucket naturally supports this!
- Tokens accumulate up to capacity
- If user makes 3 requests in 10 seconds (limit is 10), they have 7 tokens available immediately

---

## ❌ Common Mistakes & Anti-Patterns

### **MISTAKE 1: Using Semaphore for Rate Limiting** ❌
```java
// WRONG APPROACH - Don't do this!
Semaphore semaphore = new Semaphore(5);
ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(1);

scheduler.scheduleAtFixedRate(() -> {
    semaphore.release(5 - semaphore.availablePermits());
}, 0, 1, TimeUnit.SECONDS);

public boolean allowRequest() {
    return semaphore.tryAcquire();
}
```

**Why it's wrong:**
1. **Thundering herd:** All 5 requests allowed at 0.001s, then blocked for 0.999s
2. **Not atomic:** `availablePermits()` and `release()` are separate operations
3. **Resource leak:** ScheduledExecutorService never shutdown
4. **Wrong mental model:** Semaphores are for resource pooling, not rate limiting

### **MISTAKE 2: Not Thread-Safe** ❌
```java
// WRONG - Race condition!
Map<String, Integer> counts = new HashMap<>();

public boolean allowRequest(String userId) {
    int count = counts.getOrDefault(userId, 0);
    if (count < 10) {
        counts.put(userId, count + 1); // Race condition!
        return true;
    }
    return false;
}
```

**Fix:** Use `ConcurrentHashMap` + `synchronized` or `ReentrantLock`

### **MISTAKE 3: Memory Leak in Sliding Window** ❌
```java
// WRONG - Timestamps never cleaned up!
Deque<Long> timestamps = new LinkedList<>();

public boolean allowRequest() {
    timestamps.add(System.currentTimeMillis());
    // Missing: Remove old timestamps!
    return timestamps.size() <= 10;
}
```

---

## 📊 Complexity Analysis

| Algorithm | Space per Client | Time per Request | Pros |
|-----------|------------------|------------------|------|
| Fixed Window | O(1) | O(1) | Simple, fast |
| Sliding Window Log | O(N) | O(N) | Accurate |
| Sliding Window Counter | O(1) | O(1) | Balanced |
| Token Bucket | O(1) | O(1) | Industry standard |

**Recommendation:** **Token Bucket** for production systems

---

## 🎤 Interview Discussion Points

**What interviewers look for:**
1. ✅ **Understanding of trade-offs:** Fixed vs Sliding vs Token Bucket
2. ✅ **Thread safety:** Proper use of locks/concurrent data structures
3. ✅ **Edge cases:** Null checks, time going backwards, memory cleanup
4. ✅ **Scalability:** Mention distributed approach (Redis)
5. ✅ **Design patterns:** Strategy pattern for multiple algorithms
6. ✅ **Testing mindset:** Mention unit tests, concurrency tests

**Questions to ask interviewer:**
- What's the expected QPS (queries per second)?
- Single server or distributed?
- Hard limit or soft limit (allow small bursts)?
- Rate limit per user, per IP, or per API key?
- Need to support multiple time windows (1 sec, 1 min, 1 hour)?

---

## 🏆 Production-Ready Enhancements

1. **Monitoring & Metrics:**
   ```java
   AtomicLong totalAllowed = new AtomicLong();
   AtomicLong totalDenied = new AtomicLong();

   public boolean allowRequest(String clientId) {
       boolean allowed = bucket.tryConsume();
       if (allowed) {
           totalAllowed.incrementAndGet();
       } else {
           totalDenied.incrementAndGet();
       }
       return allowed;
   }
   ```

2. **Logging:**
   ```java
   logger.warn("Rate limit exceeded for client: {}", clientId);
   ```

3. **Configuration via Properties:**
   ```java
   @Value("${ratelimit.max.tokens}")
   private int maxTokens;

   @Value("${ratelimit.refill.rate}")
   private double refillRate;
   ```

4. **Response Headers (HTTP):**
   ```java
   response.setHeader("X-RateLimit-Limit", "100");
   response.setHeader("X-RateLimit-Remaining", String.valueOf(tokensLeft));
   response.setHeader("X-RateLimit-Reset", String.valueOf(resetTime));
   ```

---

## 💯 Summary & Best Practices

✅ **Use Token Bucket** for most scenarios (industry standard)
✅ **Thread safety** via `ReentrantLock` per client
✅ **ConcurrentHashMap** for storing client buckets
✅ **Cleanup inactive clients** to prevent memory leaks
✅ **Ask clarifying questions** before implementing
✅ **Mention testing strategy** (unit tests, concurrency tests)
✅ **Discuss distributed approach** (Redis, Lua scripts)
✅ **Handle edge cases** (null, time drift, negative values)

**Interview Pro Tip:** Start with simple Fixed Window, explain limitations, then propose Token Bucket as an improvement. This shows progression of thought and understanding of trade-offs!

---

**Related LeetCode Problems:**
- LeetCode 359: Logger Rate Limiter
- LeetCode 362: Design Hit Counter

**Further Reading:**
- [Cloudflare: Rate Limiting](https://blog.cloudflare.com/counting-things-a-lot-of-different-things/)
- [Stripe API Rate Limits](https://stripe.com/docs/rate-limits)
- [AWS API Gateway Throttling](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html)
