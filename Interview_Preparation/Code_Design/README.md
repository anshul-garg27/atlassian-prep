# 🛠️ CODE DESIGN / LOW-LEVEL DESIGN PROBLEMS

**Complete collection of Atlassian's most frequently asked Code Design (LLD) / Machine Coding round questions**

---

## 📚 Problem Index

### **High Frequency** ⭐⭐⭐⭐⭐
These appear in **40-60%** of Atlassian Code Design rounds:

| # | Problem | Difficulty | Key Concepts | File |
|---|---------|------------|--------------|------|
| 1 | **Rate Limiter / Token Bucket** | Medium-Hard | Concurrency, Design Patterns | [View](./01_Rate_Limiter.md) |
| 2 | **Snake Game** | Medium | OOP, Game Loop, Data Structures | [View](./02_Snake_Game.md) |

### **Medium Frequency** ⭐⭐⭐⭐
These appear in **20-40%** of rounds:

| # | Problem | Difficulty | Key Concepts | File |
|---|---------|------------|--------------|------|
| 3 | **Trello / Kanban Board** | Medium | OOP, Relationships, State Mgmt | [View](./03_Trello_Kanban_Board.md) |
| 4 | **File System Design** | Medium-Hard | Tree, Caching, Path Parsing | [View](./04_File_System_Design.md) |
| 5 | **Parking Lot System** | Medium | Strategy Pattern, Resource Allocation | [View](./05_Parking_Lot_System.md) |

### **Lower Frequency** ⭐⭐⭐
These appear in **10-20%** of rounds:

| # | Problem | Difficulty | Key Concepts | File |
|---|---------|------------|--------------|------|
| 6 | **Splitwise / Expense Sharing** | Medium-Hard | Graph Algorithms, Debt Simplification | [View](./06_Splitwise_Expense_Sharing.md) |
| 7 | **Connection Pool** | Medium-Hard | Concurrency, Blocking, Resource Mgmt | [View](./07_Connection_Pool.md) |
| 8 | **Tic Tac Toe** | Easy-Medium | Game Logic, Win Detection | [View](./08_Tic_Tac_Toe.md) |

---

## 🎯 What This Round Tests

Atlassian's Code Design round evaluates:

### **1. Object-Oriented Design (40%)**
- **Classes & Responsibilities:** Each class has one clear purpose
- **Relationships:** Proper use of composition, inheritance, interfaces
- **Encapsulation:** Private fields, public methods, getters/setters
- **SOLID Principles:** Especially SRP and OCP

### **2. Code Quality (30%)**
- **Clean Code:** Readable, maintainable, well-structured
- **Naming:** Meaningful variable/method/class names
- **Modularity:** Breaking down complex logic into methods
- **Error Handling:** Try-catch, input validation, edge cases

### **3. Design Patterns (15%)**
- **Strategy Pattern:** Multiple algorithm implementations
- **Factory Pattern:** Object creation
- **Singleton Pattern:** Single global instance
- **Observer Pattern:** Event listeners

### **4. Testing Mindset (15%)**
- **Unit Tests:** Writing or describing test cases
- **Edge Cases:** Null, empty, boundary conditions
- **Concurrency Tests:** Multi-threaded scenarios
- **Integration Tests:** End-to-end workflows

---

## 💡 Common Interview Expectations

### **What Gets You Hired** ✅

1. **Ask Clarifying Questions First**
   - "What's the expected scale?"
   - "Single-threaded or multi-threaded?"
   - "Need to persist data?"
   - "Any specific constraints?"

2. **Start with High-Level Design**
   - Draw class diagram
   - Identify relationships
   - Discuss data structures
   - Get interviewer agreement

3. **Implement Core Functionality First**
   - Basic CRUD operations
   - Happy path scenarios
   - Clean, working code

4. **Then Add Robustness**
   - Edge case handling
   - Input validation
   - Error messages
   - Thread safety (if needed)

5. **Discuss Extensions**
   - "We could add..."
   - "If we need X, we'd..."
   - Shows forward thinking

6. **Mention Testing**
   - "I'd write tests for..."
   - Describe test scenarios
   - Edge cases to cover

### **Common Rejection Reasons** ❌

1. **"Complex code to understand and debug"**
   - Over-engineered solutions
   - Premature optimization
   - Too many abstractions

2. **"Did not justify approach"**
   - Silent coding
   - No explanation of design choices
   - Didn't discuss trade-offs

3. **"Missing logs/locks/error handling"**
   - No exception handling
   - No input validation
   - Missing thread safety

4. **"Did not write/mention tests"**
   - Ignored testing completely
   - No edge case discussion

5. **"Messy code structure"**
   - Everything in one class
   - Poor naming (x1, x2, temp)
   - No separation of concerns

---

## 🎨 Design Pattern Quick Reference

### **Strategy Pattern**
When you need multiple implementations of the same interface:
```java
interface RateLimitStrategy {
    boolean allowRequest(String clientId);
}

class TokenBucketStrategy implements RateLimitStrategy { }
class FixedWindowStrategy implements RateLimitStrategy { }
```

**Use Cases:** Rate limiters, payment methods, pricing strategies

### **Factory Pattern**
When object creation is complex:
```java
class VehicleFactory {
    public static Vehicle create(VehicleType type) {
        switch(type) {
            case CAR: return new Car();
            case BIKE: return new Bike();
        }
    }
}
```

**Use Cases:** Creating game objects, database connections

### **Singleton Pattern**
When you need exactly one instance:
```java
class RateLimiter {
    private static volatile RateLimiter instance;

    public static RateLimiter getInstance() {
        if (instance == null) {
            synchronized (RateLimiter.class) {
                if (instance == null) {
                    instance = new RateLimiter();
                }
            }
        }
        return instance;
    }
}
```

**Use Cases:** Configuration, connection pools, loggers

### **Observer Pattern**
When objects need to be notified of changes:
```java
interface GameListener {
    void onGameOver(int score);
    void onScoreChanged(int newScore);
}

class Game {
    List<GameListener> listeners = new ArrayList<>();

    void notifyGameOver() {
        for (GameListener l : listeners) {
            l.onGameOver(score);
        }
    }
}
```

**Use Cases:** Event systems, UI updates, notifications

---

## 🧪 Testing Strategies

### **Unit Test Template**
```java
@Test
public void testNormalCase() {
    // Arrange
    SnakeGame game = new SnakeGame(10, 10, new Position(5, 5));

    // Act
    boolean success = game.move(Direction.UP);

    // Assert
    assertTrue(success);
    assertFalse(game.isGameOver());
}

@Test(expected = IllegalArgumentException.class)
public void testInvalidInput() {
    new Board(-1, 10); // Should throw
}

@Test
public void testEdgeCase() {
    SnakeGame game = new SnakeGame(10, 10, new Position(0, 0));
    assertFalse(game.move(Direction.UP)); // Hit wall
    assertTrue(game.isGameOver());
}
```

### **Concurrency Test Template**
```java
@Test
public void testThreadSafety() throws InterruptedException {
    RateLimiter limiter = new RateLimiter(100, 100.0);
    ExecutorService executor = Executors.newFixedThreadPool(10);
    AtomicInteger allowed = new AtomicInteger(0);

    for (int i = 0; i < 200; i++) {
        executor.submit(() -> {
            if (limiter.allowRequest("user1")) {
                allowed.incrementAndGet();
            }
        });
    }

    executor.shutdown();
    executor.awaitTermination(5, TimeUnit.SECONDS);

    assertEquals(100, allowed.get());
}
```

---

## 📊 Complexity Analysis Guide

Always discuss time/space complexity:

| Data Structure | Operation | Time | When to Use |
|----------------|-----------|------|-------------|
| **HashMap** | get/put | O(1) | Fast lookups |
| **TreeMap** | get/put | O(log N) | Sorted order needed |
| **LinkedList** | addFirst/Last | O(1) | Deque operations |
| **ArrayList** | get | O(1) | Random access |
| **PriorityQueue** | add/poll | O(log N) | Top K elements |
| **HashSet** | contains | O(1) | Uniqueness check |

---

## 🎤 Interview Flow Template

### **Phase 1: Understanding (5 mins)**
1. Ask clarifying questions
2. Confirm requirements
3. Discuss scale/constraints

### **Phase 2: Design (10 mins)**
1. Draw class diagram
2. Identify key classes
3. Define relationships
4. Choose data structures

### **Phase 3: Implementation (35 mins)**
1. Start with main class
2. Implement core methods
3. Add helper classes
4. Handle edge cases

### **Phase 4: Testing & Extensions (10 mins)**
1. Walk through test cases
2. Discuss edge cases
3. Propose extensions
4. Discuss improvements

---

## 🏆 Best Practices Checklist

Before submitting your solution, ensure:

- [ ] **Classes have clear responsibilities** (SRP)
- [ ] **Proper encapsulation** (private fields, public methods)
- [ ] **Meaningful names** (no x1, x2, temp)
- [ ] **Input validation** (null checks, bounds)
- [ ] **Error handling** (try-catch, exceptions)
- [ ] **Edge cases handled** (empty, null, boundary)
- [ ] **Thread safety** (if concurrent)
- [ ] **Complexity analyzed** (time/space)
- [ ] **Tests mentioned** (unit, integration)
- [ ] **Extensibility discussed** (future features)

---

## 🔥 Pro Tips

1. **Simplicity > Optimization**
   - Start simple, optimize only if asked
   - "Premature optimization is the root of all evil"

2. **Communication is Key**
   - Think out loud
   - Explain your reasoning
   - Discuss trade-offs

3. **Use Standard Libraries**
   - `HashMap`, `ArrayList`, `Deque`
   - Don't reinvent the wheel

4. **Design Patterns Show Maturity**
   - But don't force them
   - Use when natural fit

5. **Testing Shows Production Mindset**
   - Always mention testing
   - Even if not writing code

6. **Ask About Requirements**
   - "Do we need persistence?"
   - "Expected QPS?"
   - "Single server or distributed?"

---

## 📝 Preparation Plan

### **Week 1-2: High Frequency Problems**
Focus on:
- Rate Limiter (all 4 approaches)
- Snake Game (complete implementation)
- Practice both Java and Python

### **Week 3: Medium Frequency Problems**
Focus on:
- Trello/Kanban Board
- File System
- Parking Lot

### **Week 4: Design Patterns & Testing**
- Implement each pattern 3 times
- Write unit tests for all solutions
- Practice explaining design choices

---

## 🌟 Summary

**Key Takeaways:**
- ✅ **Clean, simple code** beats complex optimizations
- ✅ **Communication** is as important as code
- ✅ **Design patterns** show maturity
- ✅ **Testing mindset** is crucial
- ✅ **Extensibility** shows forward thinking
- ✅ **Edge cases** prevent bugs

**Remember:** Atlassian values **clean, maintainable code** over clever tricks. Show you can write code that your team would want to review and maintain!

---

**Good luck with your Atlassian Code Design round! 🚀**

For more details on each problem, click the links in the problem index above.
