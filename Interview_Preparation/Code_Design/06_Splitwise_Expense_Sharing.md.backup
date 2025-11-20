# 💰 PROBLEM 6: SPLITWISE / EXPENSE SHARING

### ⭐⭐⭐ **Design Expense Splitting System**

**Frequency:** MEDIUM at Atlassian
**Difficulty:** Medium-Hard
**Focus:** Graph Algorithms, Debt Simplification

---

## 📋 Problem Statement

Design a system like Splitwise where users can:
- Add expenses
- Split expenses (equally, by percentage, exact amounts)
- Track who owes whom
- Simplify debts (minimize transactions)

---

## 🎨 Visual Example

```text
Trip to Restaurant:
- Total: $120
- Paid by: Alice
- Split among: Alice, Bob, Charlie (equally)
- Each owes: $40

Result:
Bob owes Alice $40
Charlie owes Alice $40

After simplification with other expenses:
Bob owes Alice $20 (net)
Charlie owes Bob $10
Alice owes Charlie $5
```

---

## 💻 Implementation

```java
enum SplitType {
    EQUAL, EXACT, PERCENT
}

class User {
    String id;
    String name;
    
    public User(String id, String name) {
        this.id = id;
        this.name = name;
    }
}

class Split {
    User user;
    double amount;
    
    public Split(User user, double amount) {
        this.user = user;
        this.amount = amount;
    }
}

abstract class Expense {
    String id;
    double amount;
    User paidBy;
    List<Split> splits;
    String description;
    LocalDate date;
    
    public Expense(double amount, User paidBy, String description) {
        this.id = UUID.randomUUID().toString();
        this.amount = amount;
        this.paidBy = paidBy;
        this.description = description;
        this.date = LocalDate.now();
        this.splits = new ArrayList<>();
    }
    
    abstract void calculateSplits(List<User> users);
    
    boolean validate() {
        double totalSplit = splits.stream()
                .mapToDouble(s -> s.amount)
                .sum();
        return Math.abs(totalSplit - amount) < 0.01; // Floating point tolerance
    }
}

class EqualExpense extends Expense {
    public EqualExpense(double amount, User paidBy, String description) {
        super(amount, paidBy, description);
    }
    
    @Override
    void calculateSplits(List<User> users) {
        double splitAmount = amount / users.size();
        for (User user : users) {
            splits.add(new Split(user, splitAmount));
        }
    }
}

class ExactExpense extends Expense {
    public ExactExpense(double amount, User paidBy, String description, 
                        Map<User, Double> exactSplits) {
        super(amount, paidBy, description);
        for (Map.Entry<User, Double> entry : exactSplits.entrySet()) {
            splits.add(new Split(entry.getKey(), entry.getValue()));
        }
    }
    
    @Override
    void calculateSplits(List<User> users) {
        // Already calculated in constructor
    }
}

class PercentExpense extends Expense {
    public PercentExpense(double amount, User paidBy, String description,
                          Map<User, Double> percentSplits) {
        super(amount, paidBy, description);
        for (Map.Entry<User, Double> entry : percentSplits.entrySet()) {
            double splitAmount = amount * entry.getValue() / 100.0;
            splits.add(new Split(entry.getKey(), splitAmount));
        }
    }
    
    @Override
    void calculateSplits(List<User> users) {
        // Already calculated in constructor
    }
}

class ExpenseManager {
    // userId -> userId -> amount (A owes B)
    private Map<String, Map<String, Double>> balances;
    private List<Expense> expenses;
    
    public ExpenseManager() {
        this.balances = new HashMap<>();
        this.expenses = new ArrayList<>();
    }
    
    public void addExpense(Expense expense) {
        if (!expense.validate()) {
            throw new IllegalArgumentException("Expense splits don't add up!");
        }
        
        expenses.add(expense);
        
        // Update balances
        for (Split split : expense.splits) {
            if (!split.user.equals(expense.paidBy)) {
                updateBalance(split.user, expense.paidBy, split.amount);
            }
        }
    }
    
    private void updateBalance(User debtor, User creditor, double amount) {
        balances.putIfAbsent(debtor.id, new HashMap<>());
        Map<String, Double> debtorBalances = balances.get(debtor.id);
        
        debtorBalances.put(creditor.id,
                debtorBalances.getOrDefault(creditor.id, 0.0) + amount);
    }
    
    public Map<String, Double> getBalancesForUser(User user) {
        Map<String, Double> result = new HashMap<>();
        
        // What user owes to others
        if (balances.containsKey(user.id)) {
            for (Map.Entry<String, Double> entry : balances.get(user.id).entrySet()) {
                result.put(entry.getKey(), entry.getValue());
            }
        }
        
        // What others owe to user (negative values)
        for (Map.Entry<String, Map<String, Double>> entry : balances.entrySet()) {
            if (entry.getValue().containsKey(user.id)) {
                result.put(entry.getKey(),
                        result.getOrDefault(entry.getKey(), 0.0) - entry.getValue().get(user.id));
            }
        }
        
        return result;
    }
    
    public List<Transaction> simplifyDebts() {
        // Calculate net balance for each user
        Map<String, Double> netBalance = new HashMap<>();
        
        for (Map.Entry<String, Map<String, Double>> entry : balances.entrySet()) {
            String userId = entry.getKey();
            double totalOwed = entry.getValue().values().stream()
                    .mapToDouble(Double::doubleValue).sum();
            netBalance.put(userId, netBalance.getOrDefault(userId, 0.0) - totalOwed);
        }
        
        for (Map.Entry<String, Map<String, Double>> entry : balances.entrySet()) {
            for (Map.Entry<String, Double> debt : entry.getValue().entrySet()) {
                String creditorId = debt.getKey();
                netBalance.put(creditorId,
                        netBalance.getOrDefault(creditorId, 0.0) + debt.getValue());
            }
        }
        
        // Separate debtors and creditors
        List<Map.Entry<String, Double>> debtors = new ArrayList<>();
        List<Map.Entry<String, Double>> creditors = new ArrayList<>();
        
        for (Map.Entry<String, Double> entry : netBalance.entrySet()) {
            if (entry.getValue() < -0.01) {
                debtors.add(entry);
            } else if (entry.getValue() > 0.01) {
                creditors.add(entry);
            }
        }
        
        // Greedy matching
        List<Transaction> transactions = new ArrayList<>();
        int i = 0, j = 0;
        
        while (i < debtors.size() && j < creditors.size()) {
            double debt = -debtors.get(i).getValue();
            double credit = creditors.get(j).getValue();
            double settled = Math.min(debt, credit);
            
            transactions.add(new Transaction(
                    debtors.get(i).getKey(),
                    creditors.get(j).getKey(),
                    settled
            ));
            
            debtors.get(i).setValue(debtors.get(i).getValue() + settled);
            creditors.get(j).setValue(creditors.get(j).getValue() - settled);
            
            if (Math.abs(debtors.get(i).getValue()) < 0.01) i++;
            if (Math.abs(creditors.get(j).getValue()) < 0.01) j++;
        }
        
        return transactions;
    }
}

class Transaction {
    String fromUserId;
    String toUserId;
    double amount;
    
    public Transaction(String from, String to, double amount) {
        this.fromUserId = from;
        this.toUserId = to;
        this.amount = amount;
    }
    
    @Override
    public String toString() {
        return String.format("%s pays %s: $%.2f", fromUserId, toUserId, amount);
    }
}

// Demo
public class Main {
    public static void main(String[] args) {
        ExpenseManager manager = new ExpenseManager();
        
        User alice = new User("1", "Alice");
        User bob = new User("2", "Bob");
        User charlie = new User("3", "Charlie");
        
        // Alice paid $120, split equally
        EqualExpense dinner = new EqualExpense(120.0, alice, "Dinner");
        dinner.calculateSplits(Arrays.asList(alice, bob, charlie));
        manager.addExpense(dinner);
        
        // Bob paid $60, split equally
        EqualExpense movie = new EqualExpense(60.0, bob, "Movie");
        movie.calculateSplits(Arrays.asList(alice, bob, charlie));
        manager.addExpense(movie);
        
        System.out.println("=== Simplified Debts ===");
        List<Transaction> simplified = manager.simplifyDebts();
        for (Transaction t : simplified) {
            System.out.println(t);
        }
    }
}
```

---

## 🚀 Extensions

### **1. Groups**
```java
class Group {
    String id;
    String name;
    Set<User> members;
    List<Expense> expenses;
}
```

### **2. Categories**
```java
enum Category {
    FOOD, TRANSPORT, ENTERTAINMENT, UTILITIES
}
```

### **3. Settlements**
```java
class Settlement {
    User from;
    User to;
    double amount;
    LocalDateTime settledAt;
}
```

---

## 📊 Complexity

| Operation | Time | Space |
|-----------|------|-------|
| addExpense | O(N) | O(N) |
| getBalances | O(U²) | O(U) |
| simplifyDebts | O(U log U) | O(U) |

**Where:** N = users in expense, U = total users

---

## 💡 Interview Tips

✅ Use **abstract class** for expense types
✅ Validate splits sum to total
✅ **Greedy algorithm** for debt simplification
✅ Handle floating point precision
✅ Discuss graph algorithms (debt network)

**Related:** Graph cycle detection, Min-cost max-flow
