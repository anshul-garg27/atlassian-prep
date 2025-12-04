# 🌟 PROBLEM 1: RATE LIMITER / TOKEN BUCKET

### ⭐⭐⭐⭐⭐ **Design a Rate Limiting System**

**Frequency:** HIGH FREQUENCY at Atlassian LLD rounds!
**Difficulty:** Medium-Hard
**Time to Solve:** 35-45 minutes
**Focus:** Concurrency, Design Patterns, Algorithm Selection

---

## 📋 Problem Statement

Design a `RateLimiter` library/class that limits the number of requests a user/client can make within a given time window.

**Core Requirements:**
- Track requests per client/user
- Allow/deny requests based on configured limits
- Support multiple rate limiting algorithms
- Thread-safe for concurrent requests
- Efficient memory usage

**Input:** `client_id` (str), `timestamp` (float)
**Output:** `bool` (True = allowed, False = denied)

**Constraints:**
- 1 ≤ Number of clients ≤ 1,000,000
- 1 ≤ Requests per second ≤ 10,000 per client
- Time window: 1 second to 1 hour
- Must handle concurrent requests (multi-threaded)

---

## 🎯 INTERVIEW FLOW: Step-by-Step Guide

### **PHASE 1: Clarify Requirements (2-3 minutes)**

**SAY THIS:**
> "Before I start designing, let me clarify a few requirements:"

**Questions to Ask:**
1. "What's the rate limit format? Requests per second, per minute, or configurable?"
2. "Should different clients have different limits (tiered system)?"
3. "Is this single server or distributed across multiple servers?"
4. "Should we support burst traffic (allow temporary spikes)?"
5. "Do we need to return remaining quota in the response?"

**WRITE DOWN the answers. This shows you're thorough.**

---

### **PHASE 2: Discuss Algorithm Options (3-4 minutes)**

**SAY THIS:**
> "There are several approaches for rate limiting. Let me walk through the main ones and explain why I'll choose Token Bucket."

#### **Option 1: Fixed Window Counter** ⭐⭐⭐
```text
Window: 10 seconds, Limit: 5 requests

|----Window 1----|----Window 2----|
   5 requests        3 requests
```

**Explain:** "Simple counter per time window. Reset when window expires."

**Pros:** O(1) time and space
**Cons:** "The BURST PROBLEM - if 5 requests come at 9.9s and 5 at 10.1s, that's 10 requests in 0.2 seconds!"

---

#### **Option 2: Sliding Window Log** ⭐⭐⭐⭐
```text
Limit: 5 per 10 seconds, Current time: 15s
Queue: [7s, 9s, 12s, 14s, 15s]
        ↑ expired, remove

Clean: [9s, 12s, 14s, 15s] → 4 < 5 → ALLOW
```

**Explain:** "Store timestamp of each request, remove expired ones."

**Pros:** Precise, no burst problem
**Cons:** "O(N) memory where N = max requests. For 1M clients with 1000 req/s each, that's billions of timestamps!"

---

#### **Option 3: Token Bucket** ⭐⭐⭐⭐⭐ (RECOMMENDED)
```text
Bucket capacity: 10 tokens
Refill rate: 1 token/second

Time  Tokens  Action
0s      10    Request → consume 1 → 9 left
1s      10    Refill to max
2s      10    10 requests → 0 left
3s       1    Refilled +1 → can serve 1 request
```

**Explain:** 
> "Token Bucket is the industry standard - used by AWS API Gateway, Stripe, and Google Cloud. It allows controlled bursts while maintaining average rate. Each client has a bucket that refills at a constant rate. Request consumes a token. If no tokens, request is denied."

**Why Token Bucket?**
1. ✅ O(1) time AND space per client
2. ✅ Handles bursts gracefully (up to bucket capacity)
3. ✅ Industry standard - interviewers expect this
4. ✅ Easy to reason about and explain
5. ✅ Maps well to real-world scenarios

---

### **PHASE 3: High-Level Design (2-3 minutes)**

**SAY THIS:**
> "Let me draw the high-level architecture first."

**Draw on whiteboard:**
```
┌─────────────────────────────────────────────────────────┐
│                     RateLimiter                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │           buckets: Dict[str, TokenBucket]       │   │
│  │                                                  │   │
│  │  "user1" → [Bucket: 10 tokens, refill 1/s]     │   │
│  │  "user2" → [Bucket: 10 tokens, refill 1/s]     │   │
│  │  "user3" → [Bucket: 10 tokens, refill 1/s]     │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  + allow_request(client_id) → bool                     │
│  + get_remaining_tokens(client_id) → int               │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                     TokenBucket                         │
│                                                         │
│  - capacity: int        (max tokens)                    │
│  - tokens: float        (current available)             │
│  - refill_rate: float   (tokens per second)            │
│  - last_refill: float   (timestamp)                    │
│  - lock: Lock           (thread safety)                │
│                                                         │
│  + try_consume(n) → bool                               │
│  + _refill() → void     (private, called before check) │
└─────────────────────────────────────────────────────────┘
```

**Explain the flow:**
> "When a request comes:
> 1. Look up client's bucket (create if doesn't exist)
> 2. Refill tokens based on elapsed time
> 3. If tokens >= 1, consume and return True
> 4. Otherwise return False"

---

### **PHASE 4: Design Patterns Used (2 minutes)**

**SAY THIS:**
> "I'm using two design patterns here. Let me explain why."

#### **Pattern 1: Strategy Pattern** ⭐⭐⭐⭐⭐

**Why?** "Different rate limiting algorithms (Token Bucket, Sliding Window, Leaky Bucket) can be swapped without changing client code."

```python
from abc import ABC, abstractmethod

class RateLimitStrategy(ABC):
    """Strategy interface - defines the contract"""
    
    @abstractmethod
    def allow_request(self, client_id: str) -> bool:
        """Returns True if request allowed, False if rate limited"""
        pass

class TokenBucketStrategy(RateLimitStrategy):
    """Concrete strategy - Token Bucket implementation"""
    def allow_request(self, client_id: str) -> bool:
        # Implementation here
        pass

class SlidingWindowStrategy(RateLimitStrategy):
    """Concrete strategy - Sliding Window implementation"""
    def allow_request(self, client_id: str) -> bool:
        # Different implementation
        pass

# Usage - easily swap algorithms!
limiter = RateLimiter(strategy=TokenBucketStrategy())
# Later: limiter = RateLimiter(strategy=SlidingWindowStrategy())
```

**Interview Value:** Shows you understand SOLID principles (Open/Closed)

---

#### **Pattern 2: Double-Checked Locking**

**Why?** "For thread-safe lazy initialization of client buckets without blocking all threads."

```python
def _get_or_create_bucket(self, client_id: str) -> TokenBucket:
    # First check - no lock (fast path for existing buckets)
    if client_id not in self._buckets:
        with self._lock:
            # Second check - with lock (prevents race condition)
            if client_id not in self._buckets:
                self._buckets[client_id] = TokenBucket(...)
    return self._buckets[client_id]
```

**Interview Value:** Shows you understand concurrency patterns

---

### **PHASE 5: Data Structures & Why (2 minutes)**

**SAY THIS:**
> "Let me explain my data structure choices."

| Data Structure | Used For | Why This Choice |
|----------------|----------|-----------------|
| `Dict[str, TokenBucket]` | Map client_id → bucket | O(1) lookup, Python dict is hash map |
| `threading.Lock` | Thread safety per bucket | Fine-grained locking, not global |
| `float` for tokens | Allow fractional tokens | Smooth refill (0.5 tokens after 0.5s) |
| `dataclass` | TokenBucket | Clean, immutable-like structure |

**Key Insight:**
> "I use PER-CLIENT locks, not a global lock. This is critical - a global lock would serialize ALL requests across ALL clients. With per-client locks, user1 and user2 can be processed simultaneously."

---

### **PHASE 6: Write the Code (15-20 minutes)**

**SAY THIS:**
> "Now let me implement this. I'll start with the TokenBucket class, then the RateLimiter."

```python
"""
Rate Limiter using Token Bucket Algorithm
=========================================
Thread-safe implementation suitable for production use.

Design Patterns:
- Double-Checked Locking: Thread-safe bucket creation
- Strategy Pattern (Conceptual): This class implements the Token Bucket strategy. 
  (See Phase 4 for how to abstract this into an interface)

Time Complexity: O(1) per request
Space Complexity: O(N) where N = unique clients

Author: Candidate
"""

import threading
import time
from typing import Dict, Optional
from dataclasses import dataclass, field


@dataclass
class TokenBucket:
    """
    Token Bucket for a single client.
    
    Algorithm:
    1. Bucket holds tokens up to 'capacity'
    2. Tokens refill at 'refill_rate' per second
    3. Each request consumes 1 token
    4. If no tokens available, request is denied
    
    Thread Safety:
    - Uses per-bucket lock (not global)
    - Lock acquired only during token check/consume
    """
    capacity: int
    refill_rate: float
    tokens: float = field(init=False)
    last_refill: float = field(init=False)
    lock: threading.Lock = field(default_factory=threading.Lock)
    
    def __post_init__(self):
        """Initialize bucket to full capacity."""
        self.tokens = float(self.capacity)
        self.last_refill = time.time()
    
    def try_consume(self, tokens_needed: int = 1) -> bool:
        """
        Attempt to consume tokens from bucket.
        
        Args:
            tokens_needed: Number of tokens to consume (default: 1)
        
        Returns:
            True if tokens consumed (request allowed)
            False if insufficient tokens (request denied)
        
        Thread Safety:
            Uses lock to ensure atomic read-modify-write
        """
        with self.lock:
            # Step 1: Refill based on elapsed time
            self._refill()

            # Step 2: Check and consume
            if self.tokens >= tokens_needed:
                self.tokens -= tokens_needed
                return True
            return False

    def _refill(self) -> None:
        """
        Refill tokens based on time elapsed since last refill.
        
        Key insight: We don't need a background thread!
        Tokens are calculated lazily when needed.
        
        Handles clock drift (time going backward).
        """
        now = time.time()
        
        # Handle clock drift (NTP sync, VM migration, etc.)
        if now < self.last_refill:
            self.last_refill = now
            return
        
        # Calculate tokens to add
        elapsed = now - self.last_refill
        tokens_to_add = elapsed * self.refill_rate

        # Update state
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now
    
    def get_available_tokens(self) -> float:
        """
        Get current token count (for monitoring/headers).
        
        Note: Also triggers refill for accuracy.
        """
        with self.lock:
            self._refill()
            return self.tokens


class RateLimiter:
    """
    Thread-safe Rate Limiter using Token Bucket algorithm.
    
    Usage:
        # 5 requests per second, can burst up to 10
        limiter = RateLimiter(max_tokens=10, refill_rate=5.0)
        
        if limiter.allow_request("user123"):
            process_request()
        else:
            return "429 Too Many Requests"
    
    Production Considerations:
        - For distributed systems, use Redis instead of in-memory dict
        - Consider cleanup of inactive clients to prevent memory leaks
        - Add metrics/logging for monitoring
    """
    
    def __init__(self, max_tokens: int, refill_rate: float):
        """
        Initialize rate limiter.
        
        Args:
            max_tokens: Maximum tokens (burst capacity)
            refill_rate: Tokens added per second (sustained rate)
        
        Example:
            max_tokens=10, refill_rate=5.0
            → Can burst 10 requests instantly
            → Sustained rate is 5 requests/second
        
        Raises:
            ValueError: If parameters are invalid
        """
        # Input validation
        if max_tokens <= 0:
            raise ValueError("max_tokens must be positive")
        if refill_rate <= 0:
            raise ValueError("refill_rate must be positive")
        
        self._buckets: Dict[str, TokenBucket] = {}
        self._max_tokens = max_tokens
        self._refill_rate = refill_rate
        self._buckets_lock = threading.Lock()  # Only for bucket creation
    
    def allow_request(self, client_id: str) -> bool:
        """
        Check if request from client should be allowed.
        
        Args:
            client_id: Unique identifier (user_id, IP, API key, etc.)
        
        Returns:
            True: Request allowed, token consumed
            False: Rate limited, request should be rejected
        
        Raises:
            ValueError: If client_id is None or empty
        
        Thread Safety:
            Safe to call from multiple threads simultaneously.
        """
        # Input validation
        if not client_id:
            raise ValueError("client_id cannot be None or empty")
        
        # Get or create bucket (thread-safe)
        bucket = self._get_or_create_bucket(client_id)
        
        # Try to consume token
        return bucket.try_consume()
    
    def _get_or_create_bucket(self, client_id: str) -> TokenBucket:
        """
        Get existing bucket or create new one.
        
        Uses Double-Checked Locking pattern:
        1. Check without lock (fast path)
        2. If not found, acquire lock and check again
        3. Create only if still not found
        
        This prevents:
        - Blocking all requests during bucket creation
        - Race condition creating duplicate buckets
        """
        # Fast path - bucket exists
        if client_id in self._buckets:
            return self._buckets[client_id]
        
        # Slow path - need to create
        with self._buckets_lock:
            # Double-check after acquiring lock
            if client_id not in self._buckets:
                self._buckets[client_id] = TokenBucket(
                    capacity=self._max_tokens,
                    refill_rate=self._refill_rate
                )
        
        return self._buckets[client_id]
    
    def get_remaining_tokens(self, client_id: str) -> float:
        """
        Get remaining tokens for client (for HTTP headers).
        
        Returns:
            Current token count, or max_tokens if client has no bucket
        """
        if client_id in self._buckets:
            return self._buckets[client_id].get_available_tokens()
        return float(self._max_tokens)
    
    def get_rate_limit_headers(self, client_id: str) -> Dict[str, str]:
        """
        Get rate limit headers for HTTP response.
        
        Standard headers used by AWS, Stripe, etc.
        """
        return {
            "X-RateLimit-Limit": str(self._max_tokens),
            "X-RateLimit-Remaining": str(int(self.get_remaining_tokens(client_id))),
            "X-RateLimit-Reset": str(int(time.time() + 1)),
        }


# ============ Alternative: Sliding Window Log ============

from collections import deque

class SlidingWindowRateLimiter:
    """
    Alternative implementation using Sliding Window Log.
    
    Trade-offs vs Token Bucket:
    + More precise (no burst at all)
    - O(N) memory per client where N = max_requests
    - O(N) time to clean expired timestamps
    
    Use when:
    - Strict rate limiting needed (no bursts allowed)
    - Memory is not a constraint
    """
    
    def __init__(self, max_requests: int, window_seconds: float):
        self._max_requests = max_requests
        self._window_seconds = window_seconds
        self._timestamps: Dict[str, deque] = {}
        self._lock = threading.Lock()
    
    def allow_request(self, client_id: str) -> bool:
        now = time.time()
        
        # Get or create timestamp queue
        if client_id not in self._timestamps:
            with self._lock:
                if client_id not in self._timestamps:
                    self._timestamps[client_id] = deque()
        
        queue = self._timestamps[client_id]
        
        # Remove expired timestamps
        cutoff = now - self._window_seconds
        while queue and queue[0] < cutoff:
            queue.popleft()
        
        # Check and add
        if len(queue) < self._max_requests:
            queue.append(now)
            return True
        
        return False


# ============ Demo ============

def main():
    """Demonstrate rate limiter functionality."""
    
    print("=" * 60)
    print("RATE LIMITER DEMO - Token Bucket Algorithm")
    print("=" * 60)
    
    # Create limiter: 5 requests allowed, refills at 5/second
    limiter = RateLimiter(max_tokens=5, refill_rate=5.0)
    
    print("\n📋 Configuration:")
    print(f"   Max tokens (burst): 5")
    print(f"   Refill rate: 5 tokens/second")
    
    # Test 1: Basic rate limiting
    print("\n" + "-" * 40)
    print("TEST 1: Basic Rate Limiting")
    print("-" * 40)
    print("Sending 10 requests rapidly for 'user123':\n")
    
    for i in range(10):
        allowed = limiter.allow_request("user123")
        remaining = limiter.get_remaining_tokens("user123")
        status = "✓ ALLOWED" if allowed else "✗ DENIED"
        print(f"   Request {i+1:2d}: {status} (remaining: {remaining:.1f})")
    
    # Test 2: Token refill
    print("\n" + "-" * 40)
    print("TEST 2: Token Refill")
    print("-" * 40)
    print("Waiting 1 second for tokens to refill...\n")
    
    time.sleep(1)
    
    for i in range(3):
        allowed = limiter.allow_request("user123")
        status = "✓ ALLOWED" if allowed else "✗ DENIED"
        print(f"   Request {i+1}: {status}")
    
    # Test 3: Multiple clients
    print("\n" + "-" * 40)
    print("TEST 3: Multiple Clients (Separate Buckets)")
    print("-" * 40)
    
    for client in ["alice", "bob", "charlie"]:
        allowed = limiter.allow_request(client)
        print(f"   {client}: {'✓ ALLOWED' if allowed else '✗ DENIED'}")
    
    # Test 4: HTTP headers
    print("\n" + "-" * 40)
    print("TEST 4: HTTP Response Headers")
    print("-" * 40)
    
    headers = limiter.get_rate_limit_headers("user123")
    for key, value in headers.items():
        print(f"   {key}: {value}")
    
    print("\n" + "=" * 60)
    print("Demo completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
```

---

### **PHASE 7: Walk Through Edge Cases (3-4 minutes)**

**SAY THIS:**
> "Let me discuss the edge cases I've handled and how."

| Edge Case | How Handled | Code Location |
|-----------|-------------|---------------|
| **Null/Empty client_id** | Raise `ValueError` | `allow_request()` validation |
| **Negative config values** | Raise `ValueError` | `__init__()` validation |
| **Clock drift (time backward)** | Reset last_refill to now | `_refill()` method |
| **Concurrent bucket creation** | Double-checked locking | `_get_or_create_bucket()` |
| **Token overflow** | Cap at capacity | `min(capacity, tokens + added)` |

**Clock drift explanation:**
> "In distributed systems, NTP can adjust time backward. If we don't handle this, elapsed time becomes negative, and we'd subtract tokens instead of adding!"

---

### **PHASE 8: Testing Strategy (2-3 minutes)**

**SAY THIS:**
> "Here's how I would test this."

```python
import pytest
import threading
from concurrent.futures import ThreadPoolExecutor

class TestRateLimiter:
    """Comprehensive test suite for Rate Limiter."""
    
    def test_basic_rate_limiting(self):
        """First N requests pass, N+1 fails."""
        limiter = RateLimiter(max_tokens=3, refill_rate=3.0)
        
        assert limiter.allow_request("user1") == True  # 1
        assert limiter.allow_request("user1") == True  # 2
        assert limiter.allow_request("user1") == True  # 3
        assert limiter.allow_request("user1") == False # 4 - denied
    
    def test_token_refill(self):
        """Tokens refill over time."""
        limiter = RateLimiter(max_tokens=2, refill_rate=2.0)
        
        # Exhaust tokens
        limiter.allow_request("user1")
        limiter.allow_request("user1")
        assert limiter.allow_request("user1") == False
        
        # Wait for refill
        time.sleep(1.1)
        
        # Should have tokens now
        assert limiter.allow_request("user1") == True
    
    def test_separate_client_buckets(self):
        """Each client has independent bucket."""
        limiter = RateLimiter(max_tokens=1, refill_rate=1.0)
        
        # user1 exhausts their bucket
        assert limiter.allow_request("user1") == True
        assert limiter.allow_request("user1") == False
        
        # user2 should still have full bucket
        assert limiter.allow_request("user2") == True
    
    def test_thread_safety(self):
        """Rate limiter works under concurrent load."""
        limiter = RateLimiter(max_tokens=100, refill_rate=100.0)
        results = {"allowed": 0, "denied": 0}
        lock = threading.Lock()
        
        def make_request():
            if limiter.allow_request("user1"):
                with lock:
                    results["allowed"] += 1
            else:
                with lock:
                    results["denied"] += 1
        
        # 200 concurrent requests
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(make_request) for _ in range(200)]
            for f in futures:
                f.result()
        
        # Exactly 100 should be allowed
        assert results["allowed"] == 100
        assert results["denied"] == 100
    
    def test_invalid_inputs(self):
        """Invalid inputs raise appropriate errors."""
        limiter = RateLimiter(max_tokens=5, refill_rate=5.0)
        
        with pytest.raises(ValueError):
            limiter.allow_request("")
        
        with pytest.raises(ValueError):
            limiter.allow_request(None)
    
    def test_invalid_configuration(self):
        """Invalid config raises errors."""
        with pytest.raises(ValueError):
            RateLimiter(max_tokens=0, refill_rate=5.0)
        
        with pytest.raises(ValueError):
            RateLimiter(max_tokens=5, refill_rate=-1.0)
```

---

### **PHASE 9: Complexity Analysis (1 minute)**

**SAY THIS:**
> "Let me summarize the complexity."

| Operation | Time | Space |
|-----------|------|-------|
| `allow_request()` | O(1) | O(1) |
| `get_remaining_tokens()` | O(1) | O(1) |
| Overall per client | O(1) | O(1) |
| Overall system | O(1) | O(N) where N = unique clients |

**Why O(1)?**
- Dict lookup: O(1)
- Token calculation: O(1) - just math
- Lock acquire: O(1) average

---

### **PHASE 10: Extensions & Follow-ups (5+ minutes)**

**These are common follow-up questions. Prepare answers!**

#### **Q1: "How would you make this distributed?"**

**SAY THIS:**
> "For distributed systems, I'd use Redis with Lua scripts for atomicity."

```python
# Redis Lua script for atomic token bucket
RATE_LIMIT_LUA = """
local key = KEYS[1]
local capacity = tonumber(ARGV[1])
local refill_rate = tonumber(ARGV[2])
local now = tonumber(ARGV[3])

-- Get current state
local bucket = redis.call('HMGET', key, 'tokens', 'last_refill')
local tokens = tonumber(bucket[1]) or capacity
local last_refill = tonumber(bucket[2]) or now

-- Refill tokens
local elapsed = now - last_refill
local new_tokens = math.min(capacity, tokens + elapsed * refill_rate)

-- Try to consume
if new_tokens >= 1 then
    redis.call('HMSET', key, 'tokens', new_tokens - 1, 'last_refill', now)
    redis.call('EXPIRE', key, 3600)  -- Auto cleanup after 1 hour
    return 1  -- Allowed
else
    return 0  -- Denied
end
"""

class DistributedRateLimiter:
    def __init__(self, redis_client, max_tokens, refill_rate):
        self.redis = redis_client
        self.max_tokens = max_tokens
        self.refill_rate = refill_rate
        self.script = self.redis.register_script(RATE_LIMIT_LUA)
    
    def allow_request(self, client_id: str) -> bool:
        key = f"rate_limit:{client_id}"
        result = self.script(
            keys=[key],
            args=[self.max_tokens, self.refill_rate, time.time()]
        )
        return result == 1
```

---

#### **Q2: "How would you support different limits for different users?"**

**SAY THIS:**
> "I'd create a tiered system with different configurations per tier."

```python
class TieredRateLimiter:
    """Different rate limits based on user tier."""
    
    def __init__(self):
        self.tiers = {
            "free": {"max_tokens": 10, "refill_rate": 1.0},
            "premium": {"max_tokens": 100, "refill_rate": 10.0},
            "enterprise": {"max_tokens": 10000, "refill_rate": 1000.0},
        }
        self._limiters: Dict[str, RateLimiter] = {}
        self._user_tiers: Dict[str, str] = {}  # user_id -> tier
    
    def set_user_tier(self, user_id: str, tier: str):
        self._user_tiers[user_id] = tier
    
    def allow_request(self, user_id: str) -> bool:
        tier = self._user_tiers.get(user_id, "free")
        
        if tier not in self._limiters:
            config = self.tiers[tier]
            self._limiters[tier] = RateLimiter(
                max_tokens=config["max_tokens"],
                refill_rate=config["refill_rate"]
            )
        
        return self._limiters[tier].allow_request(user_id)
```

---

#### **Q3: "How would you handle cleanup of inactive clients?"**

**SAY THIS:**
> "I'd add a background cleanup thread or use LRU eviction."

```python
from collections import OrderedDict
import threading

class RateLimiterWithCleanup(RateLimiter):
    """Rate limiter with LRU cleanup of inactive clients."""
    
    def __init__(self, max_tokens, refill_rate, max_clients=100000):
        super().__init__(max_tokens, refill_rate)
        self._buckets = OrderedDict()  # LRU order
        self._max_clients = max_clients
    
    def _get_or_create_bucket(self, client_id: str) -> TokenBucket:
        if client_id in self._buckets:
            # Move to end (most recently used)
            self._buckets.move_to_end(client_id)
            return self._buckets[client_id]
        
        with self._buckets_lock:
            if client_id not in self._buckets:
                # Evict oldest if at capacity
                while len(self._buckets) >= self._max_clients:
                    self._buckets.popitem(last=False)
                
                self._buckets[client_id] = TokenBucket(
                    capacity=self._max_tokens,
                    refill_rate=self._refill_rate
                )
        
        return self._buckets[client_id]
```

---

## ❌ Common Mistakes (What NOT to Do)

### **MISTAKE 1: Using Semaphore** ❌

```python
# WRONG! This is for resource pooling, not rate limiting
semaphore = threading.Semaphore(5)

def allow_request():
    if semaphore.acquire(blocking=False):
        # Process request
        semaphore.release()  # When to release?!
```

**Problem:** "Semaphore controls CONCURRENT access, not RATE. You can have 5 requests simultaneously, but if they complete fast, you can have 1000/second!"

---

### **MISTAKE 2: Global Lock** ❌

```python
# WRONG! All clients blocked by one lock
global_lock = threading.Lock()

def allow_request(client_id):
    with global_lock:  # user1 blocks user2!
        # Check rate limit
        pass
```

**Problem:** "A global lock serializes ALL requests. If user1 takes 100ms, user2 waits even though they have different buckets!"

---

### **MISTAKE 3: Not Handling Time Drift** ❌

```python
# WRONG! Negative time = negative tokens!
elapsed = now - last_refill  # What if now < last_refill?
tokens += elapsed * rate     # Tokens become negative!
   ```

---

## 💯 Interview Checklist

Before saying "I'm done," make sure you've covered:

- [ ] ✅ **Clarified requirements** (asked questions first)
- [ ] ✅ **Discussed algorithm options** (and why Token Bucket)
- [ ] ✅ **Drew architecture** (visual diagram)
- [ ] ✅ **Mentioned design patterns** (Strategy, Double-checked Locking)
- [ ] ✅ **Explained data structure choices** (why Dict, why Lock)
- [ ] ✅ **Implemented thread safety** (per-client locks)
- [ ] ✅ **Handled edge cases** (null, negative, clock drift)
- [ ] ✅ **Discussed complexity** (O(1) time and space)
- [ ] ✅ **Mentioned testing approach**
- [ ] ✅ **Prepared for extensions** (distributed, tiered, cleanup)

---

## 📚 Quick Reference Card

**Print this and review before interview!**

```
┌────────────────────────────────────────────────────────────┐
│                    RATE LIMITER CHEAT SHEET                │
├────────────────────────────────────────────────────────────┤
│ ALGORITHM: Token Bucket (industry standard)               │
│                                                            │
│ WHY: O(1) time/space, handles bursts, used by AWS/Stripe  │
│                                                            │
│ PATTERNS:                                                  │
│   - Strategy Pattern → swap algorithms                     │
│   - Double-Checked Locking → thread-safe init             │
│                                                            │
│ DATA STRUCTURES:                                          │
│   - Dict[str, TokenBucket] → O(1) client lookup           │
│   - threading.Lock per bucket → fine-grained locking      │
│                                                            │
│ KEY FORMULA:                                               │
│   tokens = min(capacity, current + elapsed * rate)        │
│                                                            │
│ EDGE CASES:                                               │
│   - Clock drift → reset last_refill to now                │
│   - Null client_id → raise ValueError                     │
│   - Concurrent creation → double-checked locking          │
│                                                            │
│ FOLLOW-UPS:                                               │
│   - Distributed? → Redis + Lua script                     │
│   - Tiered limits? → Config per tier                      │
│   - Cleanup? → LRU eviction                               │
└────────────────────────────────────────────────────────────┘
```

---

**Related Problems:**
- LeetCode 359: Logger Rate Limiter
- LeetCode 362: Design Hit Counter

