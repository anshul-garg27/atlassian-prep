# 🔌 PROBLEM 7: DATABASE CONNECTION POOL

### ⭐⭐⭐ **Design Thread-Safe Connection Pool**

**Frequency:** MEDIUM at Atlassian
**Difficulty:** Medium-Hard  
**Focus:** Concurrency, Resource Management, Blocking

---

## 📋 Problem Statement

Design a database connection pool that:
- Maintains N connections
- Thread-safe borrowing/returning
- Blocks when pool is empty
- Lazy creation up to max size
- Timeout support

---

## 💻 Implementation

```java
import java.sql.*;
import java.util.concurrent.*;

public class ConnectionPool {
    private BlockingQueue<Connection> pool;
    private int maxPoolSize;
    private int currentPoolSize;
    private String dbUrl, dbUser, dbPassword;
    
    public ConnectionPool(int maxPoolSize, int initialPoolSize,
                          String url, String user, String password,
                          String driverClassName) throws Exception {
        if (initialPoolSize > maxPoolSize || initialPoolSize < 1) {
            throw new IllegalArgumentException("Invalid pool size");
        }
        
        this.maxPoolSize = maxPoolSize;
        this.currentPoolSize = 0;
        this.dbUrl = url;
        this.dbUser = user;
        this.dbPassword = password;
        this.pool = new LinkedBlockingQueue<>(maxPoolSize);
        
        Class.forName(driverClassName);
        
        // Pre-create connections
        for (int i = 0; i < initialPoolSize; i++) {
            createConnection();
        }
    }
    
    private synchronized void createConnection() throws SQLException {
        if (currentPoolSize >= maxPoolSize) return;
        
        Connection conn = DriverManager.getConnection(dbUrl, dbUser, dbPassword);
        pool.offer(conn);
        currentPoolSize++;
    }
    
    public Connection borrowConnection() throws Exception {
        // Try to create new connection if pool empty
        if (pool.peek() == null && currentPoolSize < maxPoolSize) {
            createConnection();
        }
        
        return pool.take(); // Blocks until available
    }
    
    public Connection borrowConnection(long timeoutMs) throws Exception {
        if (pool.peek() == null && currentPoolSize < maxPoolSize) {
            createConnection();
        }
        
        Connection conn = pool.poll(timeoutMs, TimeUnit.MILLISECONDS);
        if (conn == null) {
            throw new SQLException("Timeout waiting for connection");
        }
        return conn;
    }
    
    public void returnConnection(Connection conn) {
        if (conn != null) {
            pool.offer(conn);
        }
    }
    
    public void shutdown() throws SQLException {
        for (Connection conn : pool) {
            conn.close();
        }
        pool.clear();
    }
    
    public int getAvailableConnections() {
        return pool.size();
    }
}

// Usage
public class Demo {
    public static void main(String[] args) throws Exception {
        ConnectionPool pool = new ConnectionPool(
            10,  // max size
            3,   // initial size
            "jdbc:mysql://localhost:3306/mydb",
            "user",
            "password",
            "com.mysql.cj.jdbc.Driver"
        );
        
        Connection conn = pool.borrowConnection();
        try {
            // Use connection
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("SELECT * FROM users");
            // ...
        } finally {
            pool.returnConnection(conn);
        }
    }
}
```

---

## 🚀 Extensions

### **1. Connection Validation**
```java
public Connection borrowConnection() throws Exception {
    Connection conn = pool.take();
    
    // Validate connection
    if (!conn.isValid(2)) {
        conn.close();
        currentPoolSize--;
        createConnection();
        return borrowConnection();
    }
    
    return conn;
}
```

### **2. Connection Wrapper (Prevent Close)**
```java
class PooledConnection implements Connection {
    private Connection realConnection;
    private ConnectionPool pool;
    
    @Override
    public void close() {
        // Don't actually close, return to pool
        pool.returnConnection(realConnection);
    }
    
    // Delegate all other methods to realConnection
}
```

### **3. Monitoring**
```java
class PoolMetrics {
    AtomicLong totalBorrowed = new AtomicLong();
    AtomicLong totalReturned = new AtomicLong();
    AtomicLong totalTimeout = new AtomicLong();
}
```

---

## 🧪 Testing

```java
@Test
public void testBasicBorrowReturn() throws Exception {
    ConnectionPool pool = new ConnectionPool(5, 2, ...);
    
    Connection conn = pool.borrowConnection();
    assertNotNull(conn);
    assertEquals(1, pool.getAvailableConnections());
    
    pool.returnConnection(conn);
    assertEquals(2, pool.getAvailableConnections());
}

@Test
public void testLazyCreation() throws Exception {
    ConnectionPool pool = new ConnectionPool(5, 0, ...);
    assertEquals(0, pool.getAvailableConnections());
    
    Connection conn = pool.borrowConnection();
    assertNotNull(conn);
}

@Test(timeout = 5000)
public void testBlocking() throws Exception {
    ConnectionPool pool = new ConnectionPool(1, 1, ...);
    Connection conn1 = pool.borrowConnection();
    
    // This should block
    Future<Connection> future = executor.submit(() -> 
        pool.borrowConnection()
    );
    
    Thread.sleep(1000);
    assertFalse(future.isDone());
    
    pool.returnConnection(conn1);
    assertTrue(future.get() != null);
}
```

---

## 📊 Complexity

| Operation | Time | Space |
|-----------|------|-------|
| borrow | O(1) | O(1) |
| return | O(1) | O(1) |
| create | O(1) | O(N) |

---

## 💡 Interview Discussion

**Q: Why BlockingQueue over Semaphore?**
- BlockingQueue stores actual connections
- FIFO ordering built-in
- Simpler API

**Q: Why synchronized on createConnection?**
- Prevent race: multiple threads creating connections
- Ensure currentPoolSize doesn't exceed max

**Q: What about connection leaks?**
- Track borrow time, auto-close stale connections
- Use connection wrapper to prevent manual close

**Q: Distributed systems?**
- Use connection pool library (HikariCP, C3P0)
- Each server has its own pool

✅ Use **BlockingQueue** for waiting
✅ **Lazy creation** for efficiency
✅ **Connection validation** before returning
✅ **Timeout** support for robustness
✅ **Synchronized** on pool size check

**Production:** Use HikariCP (industry standard)
