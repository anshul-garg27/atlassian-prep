# 🔌 PROBLEM 7: DATABASE CONNECTION POOL

### ⭐⭐⭐ **Design Thread-Safe Connection Pool**

**Frequency:** MEDIUM at Atlassian
**Difficulty:** Medium-Hard
**Time to Solve:** 40-50 minutes
**Focus:** Concurrency, Resource Management, Object Pool Pattern

---

## 📋 Problem Statement

Design a database connection pool that:
- Maintains a pool of reusable connections
- Thread-safe borrowing/returning
- Blocks when pool is empty (with timeout)
- Lazy creation up to max size
- Connection validation and cleanup

**Core Requirements:**
- `get_connection(timeout)`: Borrow a connection (blocks if empty)
- `release_connection(conn)`: Return connection to pool
- `shutdown()`: Close all connections
- Support min/max pool size
- Handle stale connections

**Constraints:**
- Thread-safe for concurrent access
- Configurable min/max size
- Timeout support for blocking
- Connection validation before use

---

## 🎯 INTERVIEW FLOW: Step-by-Step Guide

### **PHASE 1: Clarify Requirements (2-3 minutes)**

**SAY THIS:**
> "Before I start designing, let me clarify a few requirements:"

**Questions to Ask:**
1. "What's the connection type? Database, HTTP, or generic?"
2. "Should we validate connections before returning to user?"
3. "How to handle connection leaks (borrowed but never returned)?"
4. "Should we support dynamic pool sizing?"
5. "Do we need health checks for idle connections?"
6. "What happens if connection creation fails?"

**WRITE DOWN the answers. This shows you're thorough.**

---

### **PHASE 2: Identify the Design Pattern (2-3 minutes)**

**SAY THIS:**
> "This is the classic Object Pool Pattern."

```text
Object Pool Pattern:
┌─────────────────────────────────────────────────────┐
│                                                     │
│   Client ──get()──► Pool ──create()──► Factory     │
│            ◄──conn──     ◄──conn──                 │
│                                                     │
│   Client ──release()──► Pool                        │
│                         (returns to pool)           │
│                                                     │
└─────────────────────────────────────────────────────┘

Why Object Pool?
- Connections are EXPENSIVE to create (TCP handshake, auth)
- Reusing existing connections is much faster
- Limits concurrent connections to database
- Prevents resource exhaustion
```

**Real-world examples:**
> "HikariCP (Java), psycopg2.pool (Python), and all major ORMs use this pattern.
> Database servers also limit connections, so pooling prevents 'too many connections' errors."

---

### **PHASE 3: High-Level Design (2-3 minutes)**

**SAY THIS:**
> "Let me draw the class structure."

**Draw on whiteboard:**
```
┌─────────────────────────────────────────────────────────┐
│                   ConnectionPool                        │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Thread-safe pool with blocking semantics       │   │
│  │                                                  │   │
│  │  - factory: ConnectionFactory                   │   │
│  │  - config: PoolConfig                           │   │
│  │  - pool: Queue[Connection]  ← Available conns  │   │
│  │  - all_connections: Set     ← All conns        │   │
│  │  - lock: Lock               ← For size tracking│   │
│  │  - condition: Condition     ← For blocking     │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  + get_connection(timeout) → Connection                │
│  + release_connection(conn) → void                     │
│  + shutdown() → void                                   │
└─────────────────────────────────────────────────────────┘

┌─────────────────────┐     ┌─────────────────────┐
│ ConnectionFactory   │     │    Connection       │
│    (Abstract)       │     │    (Abstract)       │
├─────────────────────┤     ├─────────────────────┤
│ + create()          │     │ + is_valid()        │
└─────────────────────┘     │ + close()           │
         │                  │ + execute()         │
         ▼                  └─────────────────────┘
  DatabaseFactory
```

---

### **PHASE 4: Thread Safety Design (3-4 minutes)**

**SAY THIS:**
> "Thread safety is the core challenge. Let me explain my synchronization strategy."

#### **What Needs Synchronization?**

| Resource | Problem | Solution |
|----------|---------|----------|
| Pool (Queue) | Multiple threads grab same conn | Queue is thread-safe |
| Size counter | Race condition on increment | Lock |
| Blocking | Threads wait for available conn | Condition variable |
| Shutdown flag | Read/write race | Volatile or lock |

---

#### **Synchronization Primitives**

```python
from queue import Queue  # Thread-safe!
import threading

class ConnectionPool:
    def __init__(self):
        self._pool = Queue(maxsize=max_size)  # Thread-safe by default
        self._lock = threading.Lock()          # For size tracking
        self._condition = threading.Condition(self._lock)  # For blocking
```

**Key Insight:**
> "Python's `Queue` is already thread-safe, so we don't need to lock for get/put.
> We only need explicit locks for:
> 1. Tracking total connection count (create new vs wait)
> 2. Condition variable for blocking when pool is exhausted"

---

### **PHASE 5: Data Structures & Why (2 minutes)**

**SAY THIS:**
> "Let me explain my data structure choices."

| Data Structure | Used For | Why This Choice |
|----------------|----------|-----------------|
| `Queue` | Available connections | Thread-safe, FIFO order, blocking support |
| `Set` | All connections | O(1) membership check, track for cleanup |
| `Lock` | Size tracking | Protect concurrent increment |
| `Condition` | Blocking | Wait/notify when pool exhausted |
| `dataclass` | Config | Clean configuration object |

**Why Queue instead of List?**
> "Queue provides `get_nowait()`, `put_nowait()`, and blocking `get(timeout)` out of the box.
> It's thread-safe without additional locking.
> List would require manual locking for every operation."

---

### **PHASE 6: Write the Code (15-20 minutes)**

**SAY THIS:**
> "Now let me implement this. I'll start with the Connection interface, then the Pool."

```python
"""
Thread-Safe Database Connection Pool
====================================
Object Pool Pattern with thread-safe implementation.

Design Patterns:
- Object Pool: Reuse expensive connections
- Factory: Create connections

Thread Safety:
- Queue: Thread-safe pool storage
- Lock: Protect size counter
- Condition: Block when exhausted

Features:
- Lazy creation up to max size
- Timeout support
- Connection validation
- Context manager for safe usage
"""

import threading
import time
from queue import Queue, Empty, Full
from typing import Optional, Set
from dataclasses import dataclass
from contextlib import contextmanager
from abc import ABC, abstractmethod
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============ Connection Interface ============

class ConnectionState(Enum):
    """Connection lifecycle states."""
    IDLE = "idle"
    IN_USE = "in_use"
    CLOSED = "closed"


class Connection(ABC):
    """Abstract connection interface."""
    
    @abstractmethod
    def is_valid(self) -> bool:
        """Check if connection is still valid (not stale)."""
        pass
    
    @abstractmethod
    def close(self) -> None:
        """Close the connection."""
        pass
    
    @abstractmethod
    def execute(self, query: str) -> any:
        """Execute a query."""
        pass


class MockDatabaseConnection(Connection):
    """
    Mock database connection for demonstration.
    
    In production, this would be:
    - psycopg2 connection (PostgreSQL)
    - mysql.connector (MySQL)
    - pyodbc connection (SQL Server)
    """
    
    _id_counter = 0
    _lock = threading.Lock()
    
    def __init__(self, host: str, port: int, database: str):
        with MockDatabaseConnection._lock:
            MockDatabaseConnection._id_counter += 1
            self.id = MockDatabaseConnection._id_counter
        
        self.host = host
        self.port = port
        self.database = database
        self.state = ConnectionState.IDLE
        self.created_at = time.time()
        self.last_used_at = time.time()
        self._closed = False
        
        # Simulate connection establishment (expensive!)
        time.sleep(0.01)
        logger.info(f"Connection {self.id} created")
    
    def is_valid(self) -> bool:
        """Check if connection is still valid."""
        if self._closed:
            return False
        # In real implementation: execute "SELECT 1" or ping
        return True
    
    def close(self) -> None:
        """Close connection."""
        if not self._closed:
            self._closed = True
            self.state = ConnectionState.CLOSED
            logger.info(f"Connection {self.id} closed")
    
    def execute(self, query: str) -> str:
        """Execute a query."""
        if self._closed:
            raise RuntimeError("Connection is closed")
        
        self.last_used_at = time.time()
        return f"Result from connection {self.id}: {query}"
    
    def __repr__(self):
        return f"Connection(id={self.id}, state={self.state.value})"


# ============ Connection Factory ============

class ConnectionFactory(ABC):
    """Factory interface for creating connections."""
    
    @abstractmethod
    def create(self) -> Connection:
        """Create a new connection."""
        pass


class DatabaseConnectionFactory(ConnectionFactory):
    """Factory for database connections."""
    
    def __init__(self, host: str, port: int, database: str):
        self.host = host
        self.port = port
        self.database = database
    
    def create(self) -> Connection:
        return MockDatabaseConnection(self.host, self.port, self.database)


# ============ Pool Configuration ============

@dataclass
class PoolConfig:
    """Configuration for connection pool."""
    min_size: int = 2              # Minimum connections to maintain
    max_size: int = 10             # Maximum connections allowed
    connection_timeout: float = 30.0  # Timeout waiting for connection
    idle_timeout: float = 300.0       # Close connections idle > 5 min
    validation_interval: float = 60.0  # Validate connections every 1 min


# ============ Connection Pool ============

class ConnectionPool:
    """
    Thread-safe connection pool implementation.
    
    Thread Safety Strategy:
    1. Queue for pool - inherently thread-safe
    2. Lock for size counter - prevent race on create
    3. Condition for blocking - wait when exhausted
    
    Connection Lifecycle:
    1. Created lazily (up to max_size)
    2. Validated before returning to client
    3. Returned to pool after use
    4. Closed on shutdown or when stale
    
    Example:
        >>> pool = ConnectionPool(factory, config)
        >>> with pool.connection() as conn:
        ...     conn.execute("SELECT * FROM users")
    """
    
    def __init__(self, factory: ConnectionFactory, config: PoolConfig = None):
        self.factory = factory
        self.config = config or PoolConfig()
        
        # Thread-safe pool using Queue
        self._pool: Queue[Connection] = Queue(maxsize=self.config.max_size)
        
        # Track all connections for cleanup
        self._all_connections: Set[Connection] = set()
        self._lock = threading.Lock()
        
        # Size tracking (need lock because Queue.qsize() is not reliable)
        self._current_size = 0
        self._size_lock = threading.Lock()
        
        # Condition for blocking when pool empty and at max size
        self._available = threading.Condition(self._lock)
        
        # Shutdown flag
        self._shutdown = False
        
        # Initialize minimum connections
        self._initialize_pool()
    
    def _initialize_pool(self) -> None:
        """Create initial connections (min_size)."""
        for _ in range(self.config.min_size):
            conn = self._create_connection()
            if conn:
                self._pool.put_nowait(conn)
    
    def _create_connection(self) -> Optional[Connection]:
        """
        Create a new connection if under max size.
        
        Thread-safe: Uses lock to check and increment size atomically.
        """
        with self._size_lock:
            if self._current_size >= self.config.max_size:
                return None
            self._current_size += 1
        
        try:
            conn = self.factory.create()
            with self._lock:
                self._all_connections.add(conn)
            return conn
        except Exception as e:
            # Failed to create - decrement counter
            with self._size_lock:
                self._current_size -= 1
            logger.error(f"Failed to create connection: {e}")
            raise
    
    def get_connection(self, timeout: float = None) -> Connection:
        """
        Get a connection from the pool.
        
        Algorithm:
        1. Try to get from pool immediately (non-blocking)
        2. If empty, try to create new connection (if under max)
        3. If at max, block until connection returned or timeout
        
        Thread Safety:
        - Queue.get_nowait() is thread-safe
        - Create uses size_lock
        - Wait uses condition variable
        
        Args:
            timeout: Max seconds to wait (None = use config default)
        
        Returns:
            Connection object ready for use
        
        Raises:
            TimeoutError: If timeout exceeded
            RuntimeError: If pool is shutdown
        """
        if self._shutdown:
            raise RuntimeError("Pool is shutdown")
        
        timeout = timeout if timeout is not None else self.config.connection_timeout
        deadline = time.time() + timeout
        
        while True:
            # Step 1: Try to get from pool (non-blocking)
            try:
                conn = self._pool.get_nowait()
                
                # Validate connection before returning
                if not conn.is_valid():
                    logger.warning(f"Connection {conn} invalid, creating new")
                    self._remove_connection(conn)
                    continue  # Try again
                
                conn.state = ConnectionState.IN_USE
                return conn
                
            except Empty:
                pass  # Pool is empty
            
            # Step 2: Try to create new connection (if under max)
            with self._size_lock:
                can_create = self._current_size < self.config.max_size
            
            if can_create:
                conn = self._create_connection()
                if conn:
                    conn.state = ConnectionState.IN_USE
                    return conn
            
            # Step 3: Wait for connection to be returned
            remaining = deadline - time.time()
            if remaining <= 0:
                raise TimeoutError(
                    f"Timeout waiting for connection after {timeout}s"
                )
            
            with self._available:
                self._available.wait(timeout=min(remaining, 1.0))
            
            if self._shutdown:
                raise RuntimeError("Pool shutdown while waiting")
    
    def release_connection(self, conn: Connection) -> None:
        """
        Return a connection to the pool.
        
        Thread Safety:
        - Queue.put_nowait() is thread-safe
        - Notifies waiting threads via condition
        """
        if self._shutdown:
            conn.close()
            return
        
        if conn not in self._all_connections:
            logger.warning(f"Connection {conn} not from this pool")
            return
        
        conn.state = ConnectionState.IDLE
        
        try:
            self._pool.put_nowait(conn)
            
            # Notify waiting threads
            with self._available:
                self._available.notify()
                
        except Full:
            # Pool is full (shouldn't happen with proper usage)
            self._remove_connection(conn)
    
    def _remove_connection(self, conn: Connection) -> None:
        """Remove and close a connection."""
        with self._lock:
            self._all_connections.discard(conn)
        
        with self._size_lock:
            self._current_size -= 1
        
        try:
            conn.close()
        except Exception as e:
            logger.error(f"Error closing connection: {e}")
    
    @contextmanager
    def connection(self, timeout: float = None):
        """
        Context manager for safe connection usage.
        
        ALWAYS use this! Guarantees connection is returned even if exception.
        
        Usage:
            with pool.connection() as conn:
                result = conn.execute("SELECT * FROM users")
        """
        conn = self.get_connection(timeout)
        try:
            yield conn
        finally:
            self.release_connection(conn)
    
    def shutdown(self) -> None:
        """
        Shutdown the pool and close all connections.
        
        Should be called when application exits.
        """
        self._shutdown = True
        
        # Wake up all waiting threads
        with self._available:
            self._available.notify_all()
        
        # Close all connections
        with self._lock:
            for conn in list(self._all_connections):
                try:
                    conn.close()
                except Exception as e:
                    logger.error(f"Error during shutdown: {e}")
            
            self._all_connections.clear()
        
        with self._size_lock:
            self._current_size = 0
        
        logger.info("Connection pool shutdown complete")
    
    @property
    def available_count(self) -> int:
        """Number of available connections in pool."""
        return self._pool.qsize()
    
    @property
    def total_count(self) -> int:
        """Total connections (available + in use)."""
        with self._size_lock:
            return self._current_size
    
    @property
    def in_use_count(self) -> int:
        """Number of connections currently in use."""
        return self.total_count - self.available_count
    
    def get_stats(self) -> dict:
        """Get pool statistics."""
        return {
            "total": self.total_count,
            "available": self.available_count,
            "in_use": self.in_use_count,
            "max_size": self.config.max_size,
            "min_size": self.config.min_size,
        }


# ============ Demo ============
def main():
    """Demonstrate connection pool functionality."""
    print("=" * 60)
    print("CONNECTION POOL DEMO")
    print("=" * 60)
    
    # Create connection factory
    factory = DatabaseConnectionFactory(
        host="localhost",
        port=5432,
        database="mydb"
    )
    
    # Create pool with config
    config = PoolConfig(min_size=2, max_size=5, connection_timeout=5.0)
    pool = ConnectionPool(factory, config)
    
    print("\n📊 Initial Pool State:")
    print(f"   {pool.get_stats()}")
    
    # Single connection usage
    print("\n" + "-" * 50)
    print("TEST 1: Single Connection (Context Manager)")
    print("-" * 50)
    
    with pool.connection() as conn:
        result = conn.execute("SELECT * FROM users")
        print(f"   Result: {result}")
    
    print(f"   After release: {pool.get_stats()}")
    
    # Multiple connections
    print("\n" + "-" * 50)
    print("TEST 2: Multiple Connections")
    print("-" * 50)
    
    conn1 = pool.get_connection()
    conn2 = pool.get_connection()
    conn3 = pool.get_connection()
    
    print(f"   Got 3 connections: {conn1}, {conn2}, {conn3}")
    print(f"   Stats: {pool.get_stats()}")
    
    # Release connections
    pool.release_connection(conn1)
    pool.release_connection(conn2)
    pool.release_connection(conn3)
    
    print(f"   After release all: {pool.get_stats()}")
    
    # Concurrent usage
    print("\n" + "-" * 50)
    print("TEST 3: Concurrent Usage (8 threads, max 5 connections)")
    print("-" * 50)
    
    results = {"success": 0, "timeout": 0}
    results_lock = threading.Lock()
    
    def worker(worker_id: int):
        try:
            with pool.connection(timeout=2.0) as conn:
                print(f"   Worker {worker_id} got {conn}")
                time.sleep(0.3)  # Simulate work
                conn.execute(f"Query from worker {worker_id}")
                with results_lock:
                    results["success"] += 1
        except TimeoutError:
            print(f"   Worker {worker_id}: Timeout!")
            with results_lock:
                results["timeout"] += 1
    
    threads = []
    for i in range(8):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print(f"\n   Results: {results}")
    print(f"   Final stats: {pool.get_stats()}")
    
    # Cleanup
    print("\n" + "-" * 50)
    print("SHUTDOWN")
    print("-" * 50)
    pool.shutdown()


if __name__ == "__main__":
    main()
```

---

### **PHASE 7: Walk Through Edge Cases (3-4 minutes)**

**SAY THIS:**
> "Let me discuss the edge cases I've handled."

| Edge Case | How Handled | Code Location |
|-----------|-------------|---------------|
| **Pool exhausted** | Block with timeout | `get_connection()` wait loop |
| **Connection invalid** | Validate, remove, retry | `get_connection()` validation |
| **Timeout exceeded** | Raise TimeoutError | `get_connection()` deadline check |
| **Connection not from pool** | Log warning, ignore | `release_connection()` check |
| **Shutdown while waiting** | Wake threads, raise | `_available.notify_all()` |
| **Create fails** | Decrement counter, raise | `_create_connection()` try/except |
| **Double release** | Queue handles gracefully | `put_nowait()` |

**Critical Thread Safety Point:**
> "When creating a new connection, I FIRST increment the counter under lock,
> THEN create the connection outside the lock. If creation fails, I decrement.
> This prevents race conditions where two threads both think they can create."

---

### **PHASE 8: Testing Strategy (2-3 minutes)**

```python
import pytest
import threading
import time

class TestConnectionPool:
    
    def test_get_and_release(self):
        """Basic get and release works."""
        factory = DatabaseConnectionFactory("localhost", 5432, "test")
        pool = ConnectionPool(factory, PoolConfig(min_size=1, max_size=3))
        
        conn = pool.get_connection()
        assert conn is not None
        assert pool.in_use_count == 1
        
        pool.release_connection(conn)
        assert pool.in_use_count == 0
        assert pool.available_count >= 1
        
        pool.shutdown()
    
    def test_context_manager_releases(self):
        """Context manager always releases, even on exception."""
        factory = DatabaseConnectionFactory("localhost", 5432, "test")
        pool = ConnectionPool(factory, PoolConfig(min_size=1, max_size=2))
        
        try:
            with pool.connection() as conn:
                raise ValueError("Test error")
        except ValueError:
            pass
        
        # Connection should be released despite exception
        assert pool.in_use_count == 0
        pool.shutdown()
    
    def test_timeout_when_exhausted(self):
        """Timeout raised when pool exhausted."""
        factory = DatabaseConnectionFactory("localhost", 5432, "test")
        config = PoolConfig(min_size=1, max_size=1, connection_timeout=0.5)
        pool = ConnectionPool(factory, config)
        
        # Exhaust pool
        conn1 = pool.get_connection()
        
        # Should timeout
        with pytest.raises(TimeoutError):
            pool.get_connection(timeout=0.5)
        
        pool.release_connection(conn1)
        pool.shutdown()
    
    def test_concurrent_access(self):
        """Multiple threads can use pool safely."""
        factory = DatabaseConnectionFactory("localhost", 5432, "test")
        config = PoolConfig(min_size=2, max_size=5)
        pool = ConnectionPool(factory, config)
        
        results = {"count": 0}
        lock = threading.Lock()
        
        def worker():
            with pool.connection() as conn:
                conn.execute("test")
                with lock:
                    results["count"] += 1
        
        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert results["count"] == 10
        pool.shutdown()
    
    def test_shutdown_closes_all(self):
        """Shutdown closes all connections."""
        factory = DatabaseConnectionFactory("localhost", 5432, "test")
        pool = ConnectionPool(factory, PoolConfig(min_size=3, max_size=5))
        
        assert pool.total_count == 3
        
        pool.shutdown()
        
        assert pool.total_count == 0
    
    def test_invalid_connection_removed(self):
        """Invalid connections are removed and new ones created."""
        factory = DatabaseConnectionFactory("localhost", 5432, "test")
        pool = ConnectionPool(factory, PoolConfig(min_size=1, max_size=2))
        
        # Get a connection and manually invalidate it
        conn = pool.get_connection()
        pool.release_connection(conn)
        
        # Force invalidation
        conn._closed = True
        
        # Getting connection should create new one (old is invalid)
        conn2 = pool.get_connection()
        assert conn2 is not conn  # Different connection
        
        pool.release_connection(conn2)
        pool.shutdown()
```

---

### **PHASE 9: Complexity Analysis (1 minute)**

| Operation | Time | Space |
|-----------|------|-------|
| `get_connection` (available) | O(1) | O(1) |
| `get_connection` (create) | O(1) + creation time | O(1) |
| `get_connection` (wait) | O(timeout) | O(1) |
| `release_connection` | O(1) | O(1) |
| `shutdown` | O(N) | O(1) |

**Where:** N = total connections

**Why O(1) for get/release?**
> "Queue operations are O(1). Lock acquisition is O(1) average.
> The only variable is connection creation time (network I/O) and wait time."

---

### **PHASE 10: Extensions & Follow-ups (5+ minutes)**

#### **Q1: "How would you handle connection leaks?"**

**SAY THIS:**
> "Track borrow time and periodically check for leaks."

```python
class LeakDetectionPool(ConnectionPool):
    """Pool with leak detection."""
    
    def __init__(self, *args, leak_timeout: float = 60.0, **kwargs):
        super().__init__(*args, **kwargs)
        self._borrowed: Dict[Connection, float] = {}
        self._leak_timeout = leak_timeout
        self._start_leak_checker()
    
    def get_connection(self, timeout=None):
        conn = super().get_connection(timeout)
        self._borrowed[conn] = time.time()
        return conn
    
    def release_connection(self, conn):
        self._borrowed.pop(conn, None)
        super().release_connection(conn)
    
    def _check_leaks(self):
        now = time.time()
        for conn, borrow_time in list(self._borrowed.items()):
            if now - borrow_time > self._leak_timeout:
                logger.warning(f"LEAK DETECTED: {conn} borrowed {now - borrow_time}s ago")
                # Optionally: force close and remove
```

---

#### **Q2: "How would you add connection validation/health checks?"**

```python
class HealthCheckPool(ConnectionPool):
    """Pool with periodic health checks."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._health_thread = threading.Thread(target=self._health_check_loop, daemon=True)
        self._health_thread.start()
    
    def _health_check_loop(self):
        while not self._shutdown:
            time.sleep(self.config.validation_interval)
            self._validate_idle_connections()
    
    def _validate_idle_connections(self):
        """Remove invalid idle connections."""
        connections_to_check = []
        
        # Drain pool temporarily
        while True:
            try:
                conn = self._pool.get_nowait()
                connections_to_check.append(conn)
            except Empty:
                break
        
        # Check and return valid ones
        for conn in connections_to_check:
            if conn.is_valid():
                self._pool.put_nowait(conn)
            else:
                logger.info(f"Removing invalid connection: {conn}")
                self._remove_connection(conn)
```

---

#### **Q3: "How would you add metrics?"**

```python
@dataclass
class PoolMetrics:
    """Connection pool metrics."""
    total_borrows: int = 0
    total_returns: int = 0
    total_timeouts: int = 0
    total_created: int = 0
    total_closed: int = 0
    max_wait_time: float = 0.0
    avg_wait_time: float = 0.0

class MetricsPool(ConnectionPool):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metrics = PoolMetrics()
        self._wait_times = []
    
    def get_connection(self, timeout=None):
        start = time.time()
        try:
            conn = super().get_connection(timeout)
            wait_time = time.time() - start
            self._wait_times.append(wait_time)
            self.metrics.total_borrows += 1
            self.metrics.max_wait_time = max(self.metrics.max_wait_time, wait_time)
            return conn
        except TimeoutError:
            self.metrics.total_timeouts += 1
            raise
```

---

## ❌ Common Mistakes (What NOT to Do)

### **MISTAKE 1: Not Using Context Manager** ❌

```python
# WRONG - Connection might leak on exception!
conn = pool.get_connection()
result = conn.execute(query)  # If this raises, connection is lost!
pool.release_connection(conn)

# CORRECT - Always use context manager
with pool.connection() as conn:
    result = conn.execute(query)  # Releases even on exception
```

---

### **MISTAKE 2: Global Lock for Everything** ❌

```python
# WRONG - All operations serialized!
def get_connection(self):
    with self._global_lock:
        conn = self._pool.get()
        # All threads blocked while one gets connection!

# CORRECT - Fine-grained locking
def get_connection(self):
    conn = self._pool.get_nowait()  # Queue is thread-safe
    # Lock only for specific operations like size tracking
```

---

### **MISTAKE 3: Not Validating Before Return** ❌

```python
# WRONG - Return potentially broken connection
def get_connection(self):
    return self._pool.get()  # What if connection is stale?

# CORRECT - Validate first
def get_connection(self):
    conn = self._pool.get()
    if not conn.is_valid():
        self._remove_connection(conn)
        return self.get_connection()  # Retry
    return conn
```

---

## 💯 Interview Checklist

- [ ] ✅ **Identified Object Pool Pattern**
- [ ] ✅ **Explained thread safety** (Queue, Lock, Condition)
- [ ] ✅ **Implemented blocking with timeout**
- [ ] ✅ **Used context manager** for safe usage
- [ ] ✅ **Validated connections** before returning
- [ ] ✅ **Handled edge cases** (timeout, shutdown, invalid)
- [ ] ✅ **Lazy creation** up to max size
- [ ] ✅ **Proper shutdown** closing all connections
- [ ] ✅ **Discussed extensions** (leak detection, health checks, metrics)

---

## 📚 Quick Reference Card

```
┌────────────────────────────────────────────────────────────┐
│                CONNECTION POOL CHEAT SHEET                 │
├────────────────────────────────────────────────────────────┤
│ DESIGN PATTERN: Object Pool                               │
│   - Reuse expensive connections                           │
│   - Limit concurrent connections                          │
│   - Thread-safe access                                    │
│                                                            │
│ THREAD SAFETY:                                            │
│   - Queue: Thread-safe pool storage                       │
│   - Lock: Protect size counter                            │
│   - Condition: Block when exhausted                       │
│                                                            │
│ GET CONNECTION ALGORITHM:                                 │
│   1. Try pool (non-blocking)                             │
│   2. Try create (if under max)                           │
│   3. Wait with timeout                                    │
│                                                            │
│ ALWAYS USE CONTEXT MANAGER:                               │
│   with pool.connection() as conn:                         │
│       conn.execute(query)                                 │
│   # Connection ALWAYS released!                           │
│                                                            │
│ COMPLEXITY:                                               │
│   - get/release: O(1)                                    │
│   - shutdown: O(N)                                        │
└────────────────────────────────────────────────────────────┘
```

---

**Production Libraries:**
- Python: `sqlalchemy.pool`, `psycopg2.pool`
- Java: HikariCP, C3P0, Apache DBCP
- Node.js: `generic-pool`

**Related Problems:**
- Design Rate Limiter (resource management)
- Design Thread Pool (similar pattern)
- Producer-Consumer Pattern

