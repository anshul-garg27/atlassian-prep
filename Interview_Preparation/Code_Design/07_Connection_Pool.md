# 🔌 PROBLEM 7: DATABASE CONNECTION POOL

### ⭐⭐⭐ **Design Thread-Safe Connection Pool**

**Frequency:** MEDIUM at Atlassian
**Difficulty:** Medium-Hard  
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

---

## 🎯 Interview Approach

### Step 1: Clarify Requirements (2 min)
```
"Let me clarify:
1. What's the connection type? (Database, HTTP, custom?)
2. Should we validate connections before returning?
3. How to handle connection leaks (borrowed but never returned)?
4. Should we support dynamic pool sizing?"
```

### Step 2: Identify Design Pattern (1 min)
```
"This is the Object Pool Pattern:
- Reuse expensive-to-create objects
- Thread-safe access with locks
- Bounded pool with blocking semantics"
```

---

## 🎨 Visual Example

```text
Connection Pool (max=5, min=2):

Initial State:
┌─────────────────────────────────────┐
│ Pool: [Conn1, Conn2] (2 available)  │
│ In Use: []                          │
│ Size: 2/5                           │
└─────────────────────────────────────┘

After get_connection() x3:
┌─────────────────────────────────────┐
│ Pool: [] (0 available)              │
│ In Use: [Conn1, Conn2, Conn3]       │
│ Size: 3/5                           │
└─────────────────────────────────────┘

Thread 4 calls get_connection():
→ Pool empty, creates Conn4 (lazy creation)
→ Size: 4/5

Thread 5, 6 call get_connection():
→ Conn5 created (now at max)
→ Thread 6 BLOCKS until connection returned
```

---

## 💻 Python Implementation

```python
import threading
import time
from queue import Queue, Empty, Full
from typing import Optional, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from contextlib import contextmanager
from abc import ABC, abstractmethod
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============ Connection Interface ============

class ConnectionState(Enum):
    """Connection states"""
    IDLE = "idle"
    IN_USE = "in_use"
    CLOSED = "closed"

class Connection(ABC):
    """Abstract connection interface"""
    
    @abstractmethod
    def is_valid(self) -> bool:
        """Check if connection is still valid"""
        pass
    
    @abstractmethod
    def close(self) -> None:
        """Close the connection"""
        pass
    
    @abstractmethod
    def execute(self, query: str) -> any:
        """Execute a query"""
        pass

# ============ Mock Database Connection ============

class MockDatabaseConnection(Connection):
    """Simulated database connection for demonstration"""
    
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
        
        # Simulate connection establishment
        time.sleep(0.01)  # Expensive operation
        logger.info(f"Connection {self.id} created")
    
    def is_valid(self) -> bool:
        """Check connection validity"""
        if self._closed:
            return False
        
        # Simulate connection check (e.g., ping)
        # In real implementation: execute "SELECT 1"
        return True
    
    def close(self) -> None:
        """Close connection"""
        if not self._closed:
            self._closed = True
            self.state = ConnectionState.CLOSED
            logger.info(f"Connection {self.id} closed")
    
    def execute(self, query: str) -> str:
        """Execute query"""
        if self._closed:
            raise RuntimeError("Connection is closed")
        
        self.last_used_at = time.time()
        return f"Result from connection {self.id}: {query}"
    
    def __repr__(self):
        return f"Connection(id={self.id}, state={self.state.value})"

# ============ Connection Factory ============

class ConnectionFactory(ABC):
    """Factory for creating connections"""
    
    @abstractmethod
    def create(self) -> Connection:
        """Create a new connection"""
        pass

class DatabaseConnectionFactory(ConnectionFactory):
    """Factory for database connections"""
    
    def __init__(self, host: str, port: int, database: str, 
                 username: str = "", password: str = ""):
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
    
    def create(self) -> Connection:
        return MockDatabaseConnection(self.host, self.port, self.database)

# ============ Connection Pool ============

@dataclass
class PoolConfig:
    """Configuration for connection pool"""
    min_size: int = 2
    max_size: int = 10
    connection_timeout: float = 30.0  # seconds
    idle_timeout: float = 300.0  # 5 minutes
    validation_interval: float = 60.0  # 1 minute

class ConnectionPool:
    """
    Thread-safe connection pool implementation.
    
    Design Pattern: Object Pool
    
    Key Features:
    - Thread-safe with locks
    - Blocking with timeout
    - Lazy creation up to max_size
    - Connection validation
    - Automatic cleanup of stale connections
    
    Thread Safety:
    - Uses Queue for thread-safe pool
    - Lock for size tracking
    - Condition variable for blocking
    """
    
    def __init__(self, factory: ConnectionFactory, config: PoolConfig = None):
        self.factory = factory
        self.config = config or PoolConfig()
        
        # Thread-safe pool using Queue
        self._pool: Queue[Connection] = Queue(maxsize=self.config.max_size)
        
        # Track all connections (for cleanup)
        self._all_connections: set = set()
        self._lock = threading.Lock()
        
        # Size tracking
        self._current_size = 0
        self._size_lock = threading.Lock()
        
        # Condition for blocking when pool is empty and at max size
        self._available = threading.Condition(self._lock)
        
        # Shutdown flag
        self._shutdown = False
        
        # Initialize minimum connections
        self._initialize_pool()
    
    def _initialize_pool(self) -> None:
        """Create initial connections"""
        for _ in range(self.config.min_size):
            self._create_and_add_connection()
    
    def _create_and_add_connection(self) -> Optional[Connection]:
        """Create a new connection and add to pool"""
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
            with self._size_lock:
                self._current_size -= 1
            logger.error(f"Failed to create connection: {e}")
            raise
    
    def get_connection(self, timeout: float = None) -> Connection:
        """
        Get a connection from the pool.
        
        Behavior:
        1. Try to get from pool immediately
        2. If empty, try to create new (if under max)
        3. If at max, block until available or timeout
        
        Time: O(1) average case
        
        Args:
            timeout: Max seconds to wait (None = use config default)
        
        Returns:
            Connection object
        
        Raises:
            TimeoutError: If timeout exceeded
            RuntimeError: If pool is shutdown
        """
        if self._shutdown:
            raise RuntimeError("Pool is shutdown")
        
        timeout = timeout if timeout is not None else self.config.connection_timeout
        deadline = time.time() + timeout
        
        while True:
            # Try to get from pool
            try:
                conn = self._pool.get_nowait()
                
                # Validate connection
                if not conn.is_valid():
                    logger.warning(f"Connection {conn} invalid, creating new")
                    self._remove_connection(conn)
                    continue
                
                conn.state = ConnectionState.IN_USE
                return conn
                
            except Empty:
                pass
            
            # Try to create new connection
            with self._size_lock:
                can_create = self._current_size < self.config.max_size
            
            if can_create:
                conn = self._create_and_add_connection()
                if conn:
                    conn.state = ConnectionState.IN_USE
                    return conn
            
            # Wait for connection to be returned
            remaining = deadline - time.time()
            if remaining <= 0:
                raise TimeoutError(
                    f"Timeout waiting for connection after {timeout}s"
                )
            
            with self._available:
                # Wait with timeout
                self._available.wait(timeout=min(remaining, 1.0))
            
            if self._shutdown:
                raise RuntimeError("Pool shutdown while waiting")
    
    def release_connection(self, conn: Connection) -> None:
        """
        Return a connection to the pool.
        
        Time: O(1)
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
        """Remove and close a connection"""
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
        Context manager for automatic connection handling.
        
        Usage:
            with pool.connection() as conn:
                result = conn.execute("SELECT * FROM users")
        
        Guarantees connection is returned even if exception occurs.
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
        """Number of available connections"""
        return self._pool.qsize()
    
    @property
    def total_count(self) -> int:
        """Total connections (available + in use)"""
        with self._size_lock:
            return self._current_size
    
    @property
    def in_use_count(self) -> int:
        """Number of connections currently in use"""
        return self.total_count - self.available_count
    
    def get_stats(self) -> dict:
        """Get pool statistics"""
        return {
            "total": self.total_count,
            "available": self.available_count,
            "in_use": self.in_use_count,
            "max_size": self.config.max_size,
            "min_size": self.config.min_size,
        }

# ============ Connection Pool with Health Check ============

class HealthCheckPool(ConnectionPool):
    """Extended pool with periodic health checks"""
    
    def __init__(self, factory: ConnectionFactory, config: PoolConfig = None):
        super().__init__(factory, config)
        self._health_check_thread = None
        self._start_health_check()
    
    def _start_health_check(self):
        """Start background health check thread"""
        def health_check_loop():
            while not self._shutdown:
                time.sleep(self.config.validation_interval)
                self._validate_connections()
        
        self._health_check_thread = threading.Thread(
            target=health_check_loop, 
            daemon=True
        )
        self._health_check_thread.start()
    
    def _validate_connections(self):
        """Validate all idle connections"""
        # Get all connections from pool temporarily
        connections = []
        while True:
            try:
                conn = self._pool.get_nowait()
                connections.append(conn)
            except Empty:
                break
        
        # Validate and return
        for conn in connections:
            if conn.is_valid():
                self._pool.put_nowait(conn)
            else:
                logger.warning(f"Removing invalid connection {conn}")
                self._remove_connection(conn)
        
        # Ensure minimum connections
        while self.total_count < self.config.min_size:
            try:
                conn = self._create_and_add_connection()
                if conn:
                    self._pool.put_nowait(conn)
            except Exception:
                break

# ============ Demo ============

def main():
    # Create connection factory
    factory = DatabaseConnectionFactory(
        host="localhost",
        port=5432,
        database="mydb"
    )
    
    # Create pool with config
    config = PoolConfig(min_size=2, max_size=5, connection_timeout=5.0)
    pool = ConnectionPool(factory, config)
    
    print("=== Initial Pool State ===")
    print(pool.get_stats())
    
    # Single connection usage
    print("\n=== Single Connection ===")
    with pool.connection() as conn:
        result = conn.execute("SELECT * FROM users")
        print(result)
    
    print(f"After release: {pool.get_stats()}")
    
    # Concurrent usage demo
    print("\n=== Concurrent Usage ===")
    
    def worker(worker_id: int):
        try:
            with pool.connection(timeout=2.0) as conn:
                print(f"Worker {worker_id} got {conn}")
                time.sleep(0.5)  # Simulate work
                result = conn.execute(f"Query from worker {worker_id}")
                print(f"Worker {worker_id}: {result}")
        except TimeoutError:
            print(f"Worker {worker_id}: Timeout!")
    
    threads = []
    for i in range(8):  # More workers than max pool size
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print(f"\nFinal stats: {pool.get_stats()}")
    
    # Cleanup
    pool.shutdown()

if __name__ == "__main__":
    main()
```

---

## 🎯 Interview Explanation Flow

### 1. Identify the Pattern (30 sec)
```
"This is the Object Pool Pattern - we reuse expensive 
objects instead of creating/destroying them repeatedly.
It's critical for database connections which are expensive to create."
```

### 2. Explain Thread Safety (1 min)
```
"For thread safety, I use:
1. Queue - inherently thread-safe for connection storage
2. Lock - for tracking total connections
3. Condition variable - for blocking when pool is exhausted

The key insight is separating:
- Pool access (Queue handles this)
- Size tracking (needs explicit lock)
- Blocking semantics (Condition variable)"
```

### 3. Key Design Decisions (1 min)
```
"Important decisions:
1. Lazy creation - don't create until needed (up to max)
2. Connection validation - check before returning to user
3. Context manager - ensures connections are always returned
4. Timeout support - prevent indefinite blocking"
```

---

## 📊 Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| get_connection | O(1) avg | O(1) |
| release_connection | O(1) | O(1) |
| shutdown | O(N) | O(1) |

**Where:** N = total connections

---

## 🚀 Extensions

### 1. Connection Wrapper (Prevent Accidental Close)
```python
class PooledConnection:
    """Wrapper that returns to pool instead of closing"""
    
    def __init__(self, real_conn: Connection, pool: ConnectionPool):
        self._conn = real_conn
        self._pool = pool
    
    def close(self):
        # Don't close, return to pool
        self._pool.release_connection(self._conn)
    
    def __getattr__(self, name):
        return getattr(self._conn, name)
```

### 2. Connection Leak Detection
```python
class LeakDetectionPool(ConnectionPool):
    def __init__(self, *args, leak_timeout: float = 60.0, **kwargs):
        super().__init__(*args, **kwargs)
        self._borrowed: Dict[Connection, float] = {}
        self._leak_timeout = leak_timeout
    
    def get_connection(self, timeout=None):
        conn = super().get_connection(timeout)
        self._borrowed[conn] = time.time()
        return conn
    
    def _check_leaks(self):
        now = time.time()
        for conn, borrow_time in list(self._borrowed.items()):
            if now - borrow_time > self._leak_timeout:
                logger.warning(f"Potential leak: {conn}")
```

### 3. Pool Metrics
```python
@dataclass
class PoolMetrics:
    total_borrows: int = 0
    total_returns: int = 0
    total_timeouts: int = 0
    total_created: int = 0
    avg_wait_time: float = 0.0
```

---

## 💡 Interview Tips

### What Interviewers Look For:
✅ **Thread safety** with proper synchronization
✅ **Object Pool Pattern** understanding
✅ **Blocking with timeout** semantics
✅ **Resource cleanup** on shutdown
✅ **Context manager** for safe usage

### Common Mistakes:
❌ Not handling connection validation
❌ Forgetting to notify waiting threads
❌ No timeout support (infinite blocking)
❌ Memory leaks (connections never returned)
❌ Race conditions in size tracking

### Questions to Ask:
- "Should we support connection priorities?"
- "How to handle partial failures during shutdown?"
- "Do we need metrics/monitoring?"
- "Should connections be refreshed after N uses?"

---

## 🔗 Related Concepts

- **Object Pool Pattern**: Core design pattern
- **Semaphore**: Alternative for limiting concurrent access
- **Producer-Consumer**: Pool is a bounded buffer
- **Resource Management**: RAII pattern in Python (context managers)

**Production Libraries:** 
- Python: `sqlalchemy.pool`, `psycopg2.pool`
- Java: HikariCP, C3P0

