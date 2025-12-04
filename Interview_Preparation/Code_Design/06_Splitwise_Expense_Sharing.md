# 💰 PROBLEM 6: SPLITWISE / EXPENSE SHARING

### ⭐⭐⭐ **Design Expense Splitting System**

**Frequency:** MEDIUM at Atlassian
**Difficulty:** Medium-Hard
**Time to Solve:** 40-50 minutes
**Focus:** Graph Algorithms, Debt Simplification, Strategy Pattern

---

## 📋 Problem Statement

Design a system like Splitwise where users can:
- Add expenses with different split types
- Track who owes whom
- Simplify debts (minimize transactions)
- Settle debts between users

**Core Requirements:**
- `add_expense(payer, amount, participants, split_type)`: Add an expense
- `get_balance(user)`: Get user's balance (owes/owed)
- `simplify_debts()`: Minimize number of transactions
- `settle_debt(from_user, to_user, amount)`: Record payment

**Constraints:**
- Split types: Equal, Exact amounts, Percentages
- Handle floating point precision
- Support groups of any size
- Minimize transactions in debt simplification

---

## 🎯 INTERVIEW FLOW: Step-by-Step Guide

### **PHASE 1: Clarify Requirements (2-3 minutes)**

**SAY THIS:**
> "Before I start designing, let me clarify a few requirements:"

**Questions to Ask:**
1. "What split types do we need? Equal, exact amounts, percentages?"
2. "Do we need groups (like trip groups)?"
3. "Should we track expense history?"
4. "How to handle floating point precision for currency?"
5. "Should we support recurring expenses?"
6. "Do we need multi-currency support?"

**WRITE DOWN the answers. This shows you're thorough.**

---

### **PHASE 2: Discuss Key Design Decisions (3-4 minutes)**

**SAY THIS:**
> "Let me discuss the key design challenges and my approach."

#### **Challenge 1: Different Split Types**

```text
Equal Split:
  $120 among 3 people → each owes $40

Exact Split:
  $100 split as {Alice: $30, Bob: $50, Charlie: $20}

Percentage Split:
  $100 split as {Alice: 30%, Bob: 50%, Charlie: 20%}
```

**Solution:** Strategy Pattern
> "I'll use the Strategy Pattern - each split type is a separate strategy class.
> This makes it easy to add new split types without modifying existing code."

---

#### **Challenge 2: Debt Simplification**

```text
Before Simplification:
  Alice → Bob: $20
  Bob → Charlie: $30
  Charlie → Alice: $10

After Simplification (Net balances):
  Alice: +$10 (net creditor)
  Bob: -$10 (net debtor)
  Charlie: $0 (neutral)
  
  Result: Bob pays Alice $10 (1 transaction instead of 3!)
```

**Solution:** Greedy Algorithm
> "Calculate NET balance for each user.
> Separate into debtors (owe money) and creditors (owed money).
> Greedily match debtors with creditors."

---

### **PHASE 3: High-Level Design (2-3 minutes)**

**SAY THIS:**
> "Let me draw the class structure."

**Draw on whiteboard:**
```
┌─────────────────────────────────────────────────────────┐
│                   ExpenseManager                        │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Main facade - tracks all balances              │   │
│  │                                                  │   │
│  │  - balances: Dict[user, Dict[user, amount]]     │   │
│  │  - expenses: List[Expense]                      │   │
│  │  - users: Dict[id, User]                        │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  + add_expense(expense) → void                         │
│  + get_balance(user_id) → Dict[user, amount]           │
│  + simplify_debts() → List[Transaction]                │
│  + settle_debt(from, to, amount) → bool                │
└─────────────────────────────────────────────────────────┘

┌─────────────────────┐     ┌─────────────────────┐
│   SplitStrategy     │     │      Expense        │
│     (Abstract)      │     ├─────────────────────┤
├─────────────────────┤     │ - id                │
│ + calculate_splits()│     │ - description       │
│ + validate()        │     │ - amount            │
└─────────────────────┘     │ - paid_by           │
         △                  │ - splits            │
         │                  │ - split_type        │
    ┌────┴────┐             └─────────────────────┘
    │    │    │
Equal  Exact  Percent
```

---

### **PHASE 4: Design Patterns & Principles (2 minutes)**

**SAY THIS:**
> "I'm using several design patterns here."

#### **1. Strategy Pattern** ⭐⭐⭐⭐⭐

```python
from abc import ABC, abstractmethod

class SplitStrategy(ABC):
    """Strategy interface for different split types."""
    
    @abstractmethod
    def calculate_splits(self, amount: float, participants: List[User], 
                        split_data: Optional[Dict] = None) -> List[Split]:
        pass
    
    @abstractmethod
    def validate(self, amount: float, split_data: Optional[Dict]) -> bool:
        pass

class EqualSplitStrategy(SplitStrategy):
    def calculate_splits(self, amount, participants, split_data=None):
        share = amount / len(participants)
        return [Split(user=p, amount=share) for p in participants]

class ExactSplitStrategy(SplitStrategy):
    def calculate_splits(self, amount, participants, split_data):
        return [Split(user=p, amount=split_data[p.id]) for p in participants]
```

**Why Strategy Pattern?**
> "We can add new split types (weighted, percentage) without modifying ExpenseManager.
> Each strategy encapsulates its own validation logic.
> Open/Closed Principle - open for extension, closed for modification."

---

#### **2. Factory Pattern** ⭐⭐

```python
class SplitStrategyFactory:
    _strategies = {
        SplitType.EQUAL: EqualSplitStrategy,
        SplitType.EXACT: ExactSplitStrategy,
        SplitType.PERCENT: PercentSplitStrategy,
    }
    
    @classmethod
    def get_strategy(cls, split_type: SplitType) -> SplitStrategy:
        return cls._strategies[split_type]()
```

---

### **PHASE 5: Data Structures & Why (2 minutes)**

**SAY THIS:**
> "Let me explain my data structure choices."

| Data Structure | Used For | Why This Choice |
|----------------|----------|-----------------|
| `Dict[str, Dict[str, float]]` | Balance matrix | O(1) lookup for any user pair |
| `defaultdict(lambda: defaultdict(float))` | Auto-initialize | No null checks needed |
| `List[Expense]` | Expense history | Ordered, append O(1) |
| `Enum` | Split types | Type safety, fixed set of values |
| `dataclass` | User, Expense, Split | Clean initialization |

**Key Insight - Balance Matrix:**
> "The balance matrix stores: `balances[A][B] = amount A owes B`
> If A owes B $20, then `balances[A][B] = 20` and `balances[B][A] = -20`
> This makes net balance calculation easy: just sum the row."

---

### **PHASE 6: Write the Code (15-20 minutes)**

**SAY THIS:**
> "Now let me implement this. I'll start with the Strategy classes, then ExpenseManager."

```python
"""
Splitwise / Expense Sharing System
==================================
Design with Strategy Pattern for flexible split types.

Design Patterns:
- Strategy Pattern: Different split algorithms
- Factory Pattern: Create appropriate strategy

Key Features:
- Multiple split types (equal, exact, percentage)
- Debt simplification (greedy algorithm)
- Floating point precision handling

Time Complexity:
- add_expense: O(P) where P = participants
- simplify_debts: O(U log U) where U = users
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional
from abc import ABC, abstractmethod
from collections import defaultdict
import uuid
from datetime import datetime


class SplitType(Enum):
    """Types of expense splits."""
    EQUAL = "equal"
    EXACT = "exact"
    PERCENT = "percent"


@dataclass
class User:
    """User entity."""
    id: str
    name: str
    email: str = ""
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return isinstance(other, User) and self.id == other.id


@dataclass
class Split:
    """Represents how much a user owes for an expense."""
    user: User
    amount: float


@dataclass
class Transaction:
    """Represents a simplified payment transaction."""
    from_user: str
    to_user: str
    amount: float
    
    def __str__(self):
        return f"{self.from_user} pays {self.to_user}: ${self.amount:.2f}"


# ============ Strategy Pattern: Split Types ============

class SplitStrategy(ABC):
    """
    Abstract base class for split strategies.
    
    Each concrete strategy:
    1. Validates the split data
    2. Calculates individual shares
    """
    
    @abstractmethod
    def calculate_splits(self, amount: float, participants: List[User], 
                        split_data: Optional[Dict] = None) -> List[Split]:
        """Calculate how much each participant owes."""
        pass
    
    @abstractmethod
    def validate(self, amount: float, split_data: Optional[Dict]) -> bool:
        """Validate the split is valid."""
        pass


class EqualSplitStrategy(SplitStrategy):
    """Split expense equally among all participants."""
    
    def calculate_splits(self, amount: float, participants: List[User],
                        split_data: Optional[Dict] = None) -> List[Split]:
        if not participants:
            return []
        
        split_amount = amount / len(participants)
        return [Split(user=p, amount=split_amount) for p in participants]
    
    def validate(self, amount: float, split_data: Optional[Dict]) -> bool:
        return amount > 0


class ExactSplitStrategy(SplitStrategy):
    """Split expense by exact amounts specified per user."""
    
    def calculate_splits(self, amount: float, participants: List[User],
                        split_data: Optional[Dict] = None) -> List[Split]:
        if not split_data:
            raise ValueError("Exact split requires split_data with amounts")
        
        splits = []
        for user in participants:
            user_amount = split_data.get(user.id, 0)
            splits.append(Split(user=user, amount=user_amount))
        
        return splits
    
    def validate(self, amount: float, split_data: Optional[Dict]) -> bool:
        if not split_data:
            return False
        
        total = sum(split_data.values())
        # Use epsilon for floating point comparison
        return abs(total - amount) < 0.01


class PercentSplitStrategy(SplitStrategy):
    """Split expense by percentages."""
    
    def calculate_splits(self, amount: float, participants: List[User],
                        split_data: Optional[Dict] = None) -> List[Split]:
        if not split_data:
            raise ValueError("Percent split requires split_data with percentages")
        
        splits = []
        for user in participants:
            percentage = split_data.get(user.id, 0)
            user_amount = amount * percentage / 100
            splits.append(Split(user=user, amount=user_amount))
        
        return splits
    
    def validate(self, amount: float, split_data: Optional[Dict]) -> bool:
        if not split_data:
            return False
        
        total_percent = sum(split_data.values())
        return abs(total_percent - 100) < 0.01


# ============ Factory Pattern ============

class SplitStrategyFactory:
    """Factory to create appropriate split strategy."""
    
    _strategies = {
        SplitType.EQUAL: EqualSplitStrategy,
        SplitType.EXACT: ExactSplitStrategy,
        SplitType.PERCENT: PercentSplitStrategy,
    }
    
    @classmethod
    def get_strategy(cls, split_type: SplitType) -> SplitStrategy:
        strategy_class = cls._strategies.get(split_type)
        if not strategy_class:
            raise ValueError(f"Unknown split type: {split_type}")
        return strategy_class()


# ============ Expense ============

@dataclass
class Expense:
    """Represents an expense."""
    id: str
    description: str
    amount: float
    paid_by: User
    participants: List[User]
    splits: List[Split]
    split_type: SplitType
    created_at: datetime = field(default_factory=datetime.now)
    
    @classmethod
    def create(cls, description: str, amount: float, paid_by: User,
               participants: List[User], split_type: SplitType,
               split_data: Optional[Dict] = None) -> 'Expense':
        """
        Factory method to create expense with proper splits.
        
        Uses Strategy Pattern to calculate splits based on type.
        """
        strategy = SplitStrategyFactory.get_strategy(split_type)
        
        if not strategy.validate(amount, split_data):
            raise ValueError(f"Invalid split data for {split_type}")
        
        splits = strategy.calculate_splits(amount, participants, split_data)
        
        return cls(
            id=str(uuid.uuid4())[:8],
            description=description,
            amount=amount,
            paid_by=paid_by,
            participants=participants,
            splits=splits,
            split_type=split_type
        )


# ============ Expense Manager ============

class ExpenseManager:
    """
    Main class managing expenses and balances.
    
    Key Design Decisions:
    1. Balance matrix: balances[A][B] = amount A owes B
       - Positive = A owes B
       - Negative = B owes A (maintained automatically)
    
    2. Floating point tolerance (EPSILON = 0.01)
       - Currency amounts rounded to cents
       - Comparisons use epsilon
    
    3. Greedy debt simplification
       - Calculate net balance per user
       - Match debtors with creditors
       - Minimizes transactions from O(n²) to O(n)
    """
    
    EPSILON = 0.01  # Floating point tolerance (1 cent)
    
    def __init__(self):
        # balances[debtor_id][creditor_id] = amount owed
        self._balances: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
        self._expenses: List[Expense] = []
        self._users: Dict[str, User] = {}
    
    def add_user(self, user: User) -> None:
        """Register a user in the system."""
        self._users[user.id] = user
    
    def add_expense(self, expense: Expense) -> None:
        """
        Add an expense and update balances.
        
        Time: O(P) where P = number of participants
        """
        self._expenses.append(expense)
        
        payer = expense.paid_by
        
        for split in expense.splits:
            if split.user.id != payer.id:
                # split.user owes payer the split amount
                self._update_balance(split.user.id, payer.id, split.amount)
    
    def _update_balance(self, debtor_id: str, creditor_id: str, amount: float) -> None:
        """
        Update balance between two users.
        
        Maintains symmetric relationship:
        - balances[A][B] = X means A owes B $X
        - balances[B][A] = -X (automatically maintained)
        """
        self._balances[debtor_id][creditor_id] += amount
        self._balances[creditor_id][debtor_id] -= amount
    
    def get_balance(self, user_id: str) -> Dict[str, float]:
        """
        Get balance for a user.
        
        Returns: {other_user_id: amount}
        - Positive = you owe them
        - Negative = they owe you
        
        Time: O(U) where U = users this person has transactions with
        """
        result = {}
        for other_id, amount in self._balances[user_id].items():
            if abs(amount) > self.EPSILON:
                result[other_id] = round(amount, 2)
        return result
    
    def get_net_balance(self, user_id: str) -> float:
        """
        Get net balance (total owed - total to receive).
        
        Positive = net debtor (owes money)
        Negative = net creditor (owed money)
        """
        return sum(self._balances[user_id].values())
    
    def simplify_debts(self) -> List[Transaction]:
        """
        Minimize number of transactions using greedy algorithm.
        
        Algorithm:
        1. Calculate NET balance for each user
        2. Separate into debtors (positive balance) and creditors (negative)
        3. Greedily match: largest debtor pays largest creditor
        
        Why this works:
        - Net balances must sum to zero (closed system)
        - Any valid settlement achieves same net result
        - Greedy minimizes transaction count
        
        Time: O(U log U) for sorting
        Space: O(U) for balance lists
        """
        # Step 1: Calculate net balances
        net_balances: Dict[str, float] = {}
        
        all_users = set(self._balances.keys())
        for user_id in all_users:
            net = sum(self._balances[user_id].values())
            if abs(net) > self.EPSILON:
                net_balances[user_id] = net
        
        # Step 2: Separate debtors and creditors
        debtors = []   # [(user_id, amount_owed)] - positive amounts
        creditors = [] # [(user_id, amount_owed)] - positive amounts (originally negative)
        
        for user_id, net in net_balances.items():
            if net > self.EPSILON:
                debtors.append([user_id, net])
            elif net < -self.EPSILON:
                creditors.append([user_id, -net])  # Convert to positive
        
        # Step 3: Greedy matching
        transactions = []
        i, j = 0, 0
        
        while i < len(debtors) and j < len(creditors):
            debtor_id, debt = debtors[i]
            creditor_id, credit = creditors[j]
            
            # Settle minimum of debt and credit
            settled = min(debt, credit)
            
            transactions.append(Transaction(
                from_user=debtor_id,
                to_user=creditor_id,
                amount=round(settled, 2)
            ))
            
            # Update remaining amounts
            debtors[i][1] -= settled
            creditors[j][1] -= settled
            
            # Move pointers
            if debtors[i][1] < self.EPSILON:
                i += 1
            if creditors[j][1] < self.EPSILON:
                j += 1
        
        return transactions
    
    def settle_debt(self, from_user_id: str, to_user_id: str, amount: float) -> bool:
        """
        Record a payment from one user to another.
        
        Returns: True if successful, False if amount > debt
        """
        current_debt = self._balances[from_user_id].get(to_user_id, 0)
        
        if current_debt < amount - self.EPSILON:
            return False  # Can't pay more than owed
        
        # Payment reduces debt
        self._update_balance(from_user_id, to_user_id, -amount)
        return True
    
    def get_expense_history(self, user_id: str) -> List[Expense]:
        """Get all expenses involving a user."""
        return [
            exp for exp in self._expenses
            if exp.paid_by.id == user_id or 
               any(s.user.id == user_id for s in exp.splits)
        ]
    
    def print_balances(self) -> None:
        """Print all non-zero balances."""
        print("\n" + "=" * 50)
        print("CURRENT BALANCES")
        print("=" * 50)
        
        for user_id in self._users:
            balance = self.get_balance(user_id)
            if balance:
                user = self._users[user_id]
                net = self.get_net_balance(user_id)
                status = "owes" if net > 0 else "owed"
                print(f"\n{user.name} (net {status} ${abs(net):.2f}):")
                for other_id, amount in balance.items():
                    other = self._users.get(other_id, User(other_id, other_id))
                    if amount > 0:
                        print(f"  → owes {other.name}: ${amount:.2f}")
                    else:
                        print(f"  ← owed by {other.name}: ${-amount:.2f}")


# ============ Demo ============
def main():
    """Demonstrate expense sharing system."""
    print("=" * 60)
    print("SPLITWISE / EXPENSE SHARING DEMO")
    print("=" * 60)
    
    manager = ExpenseManager()
    
    # Create users
    alice = User(id="1", name="Alice")
    bob = User(id="2", name="Bob")
    charlie = User(id="3", name="Charlie")
    
    manager.add_user(alice)
    manager.add_user(bob)
    manager.add_user(charlie)
    print(f"\n✓ Created users: {alice.name}, {bob.name}, {charlie.name}")
    
    # Expense 1: Alice paid $120 for dinner, split equally
    print("\n" + "-" * 50)
    print("EXPENSE 1: Dinner ($120, Alice paid, equal split)")
    print("-" * 50)
    
    dinner = Expense.create(
        description="Dinner",
        amount=120.0,
        paid_by=alice,
        participants=[alice, bob, charlie],
        split_type=SplitType.EQUAL
    )
    manager.add_expense(dinner)
    
    print(f"Each person's share: $40.00")
    print(f"Bob owes Alice: $40.00")
    print(f"Charlie owes Alice: $40.00")
    
    # Expense 2: Bob paid $60 for movie, split equally
    print("\n" + "-" * 50)
    print("EXPENSE 2: Movie ($60, Bob paid, equal split)")
    print("-" * 50)
    
    movie = Expense.create(
        description="Movie",
        amount=60.0,
        paid_by=bob,
        participants=[alice, bob, charlie],
        split_type=SplitType.EQUAL
    )
    manager.add_expense(movie)
    
    print(f"Each person's share: $20.00")
    print(f"Alice owes Bob: $20.00")
    print(f"Charlie owes Bob: $20.00")
    
    # Expense 3: Exact split example
    print("\n" + "-" * 50)
    print("EXPENSE 3: Groceries ($100, Charlie paid, exact split)")
    print("-" * 50)
    
    groceries = Expense.create(
        description="Groceries",
        amount=100.0,
        paid_by=charlie,
        participants=[alice, bob, charlie],
        split_type=SplitType.EXACT,
        split_data={"1": 30.0, "2": 50.0, "3": 20.0}
    )
    manager.add_expense(groceries)
    
    print(f"Alice owes: $30.00")
    print(f"Bob owes: $50.00")
    print(f"Charlie owes: $20.00 (paid $100, gets $80 back)")
    
    # Print current balances
    manager.print_balances()
    
    # Simplify debts
    print("\n" + "=" * 50)
    print("SIMPLIFIED TRANSACTIONS")
    print("=" * 50)
    
    transactions = manager.simplify_debts()
    print(f"\nMinimized to {len(transactions)} transaction(s):")
    for t in transactions:
        from_name = manager._users[t.from_user].name
        to_name = manager._users[t.to_user].name
        print(f"  → {from_name} pays {to_name}: ${t.amount:.2f}")


if __name__ == "__main__":
    main()
```

---

### **PHASE 7: Walk Through Edge Cases (3-4 minutes)**

**SAY THIS:**
> "Let me discuss the edge cases I've handled."

| Edge Case | How Handled | Code Location |
|-----------|-------------|---------------|
| **Floating point precision** | Use EPSILON (0.01) for comparisons | Throughout code |
| **Split doesn't sum to total** | Validation in strategy | `validate()` method |
| **Empty participants list** | Return empty splits | `calculate_splits()` |
| **Self-payment (payer in split)** | Skip in balance update | `add_expense()` check |
| **Pay more than owed** | Return False | `settle_debt()` check |
| **Zero amount expense** | Validation fails | `validate()` method |
| **Percentage doesn't sum to 100** | Validation fails | `PercentSplitStrategy` |

**Floating Point Handling:**
> "Currency is tricky! $0.10 + $0.20 might not equal $0.30 in floating point.
> I use EPSILON = 0.01 (one cent) for all comparisons.
> All output amounts are rounded to 2 decimal places."

---

### **PHASE 8: Testing Strategy (2-3 minutes)**

```python
import pytest

class TestExpenseSharing:
    
    def test_equal_split(self):
        """Equal split divides evenly."""
        manager = ExpenseManager()
        alice = User("1", "Alice")
        bob = User("2", "Bob")
        manager.add_user(alice)
        manager.add_user(bob)
        
        expense = Expense.create(
            description="Test",
            amount=100.0,
            paid_by=alice,
            participants=[alice, bob],
            split_type=SplitType.EQUAL
        )
        manager.add_expense(expense)
        
        bob_balance = manager.get_balance("2")
        assert abs(bob_balance["1"] - 50.0) < 0.01  # Bob owes Alice $50
    
    def test_exact_split_validation(self):
        """Exact split must sum to total."""
        alice = User("1", "Alice")
        bob = User("2", "Bob")
        
        # Should fail - amounts don't sum to 100
        with pytest.raises(ValueError):
            Expense.create(
                description="Test",
                amount=100.0,
                paid_by=alice,
                participants=[alice, bob],
                split_type=SplitType.EXACT,
                split_data={"1": 30.0, "2": 40.0}  # Only 70!
            )
    
    def test_percent_split(self):
        """Percentage split calculates correctly."""
        alice = User("1", "Alice")
        bob = User("2", "Bob")
        
        expense = Expense.create(
            description="Test",
            amount=100.0,
            paid_by=alice,
            participants=[alice, bob],
            split_type=SplitType.PERCENT,
            split_data={"1": 30.0, "2": 70.0}
        )
        
        # Bob's share should be $70
        bob_split = next(s for s in expense.splits if s.user.id == "2")
        assert abs(bob_split.amount - 70.0) < 0.01
    
    def test_simplify_debts_reduces_transactions(self):
        """Debt simplification minimizes transactions."""
        manager = ExpenseManager()
        alice = User("1", "Alice")
        bob = User("2", "Bob")
        charlie = User("3", "Charlie")
        
        for u in [alice, bob, charlie]:
            manager.add_user(u)
        
        # Create circular debt
        # Alice pays for Bob
        e1 = Expense.create("E1", 30.0, alice, [bob], SplitType.EQUAL)
        manager.add_expense(e1)
        
        # Bob pays for Charlie
        e2 = Expense.create("E2", 30.0, bob, [charlie], SplitType.EQUAL)
        manager.add_expense(e2)
        
        # Charlie pays for Alice
        e3 = Expense.create("E3", 30.0, charlie, [alice], SplitType.EQUAL)
        manager.add_expense(e3)
        
        # After simplification: should be zero transactions (circular!)
        transactions = manager.simplify_debts()
        assert len(transactions) == 0  # Everyone's net balance is 0
    
    def test_settle_debt(self):
        """Settling debt reduces balance."""
        manager = ExpenseManager()
        alice = User("1", "Alice")
        bob = User("2", "Bob")
        manager.add_user(alice)
        manager.add_user(bob)
        
        expense = Expense.create("Test", 100.0, alice, [alice, bob], SplitType.EQUAL)
        manager.add_expense(expense)
        
        # Bob owes Alice $50
        assert manager.settle_debt("2", "1", 30.0) == True
        
        # Now Bob owes Alice $20
        bob_balance = manager.get_balance("2")
        assert abs(bob_balance["1"] - 20.0) < 0.01
    
    def test_cannot_overpay(self):
        """Cannot pay more than owed."""
        manager = ExpenseManager()
        alice = User("1", "Alice")
        bob = User("2", "Bob")
        manager.add_user(alice)
        manager.add_user(bob)
        
        expense = Expense.create("Test", 100.0, alice, [alice, bob], SplitType.EQUAL)
        manager.add_expense(expense)
        
        # Bob owes Alice $50, try to pay $100
        result = manager.settle_debt("2", "1", 100.0)
        assert result == False
```

---

### **PHASE 9: Complexity Analysis (1 minute)**

| Operation | Time | Space |
|-----------|------|-------|
| `add_expense` | O(P) | O(1) |
| `get_balance` | O(U) | O(U) |
| `simplify_debts` | O(U log U) | O(U) |
| `settle_debt` | O(1) | O(1) |

**Where:** P = participants per expense, U = total users

**Why O(U log U) for simplify?**
> "We could sort debtors and creditors for optimal matching.
> In my implementation, I use simple iteration which is O(U).
> The sorting optimization helps with very large user bases."

---

### **PHASE 10: Extensions & Follow-ups (5+ minutes)**

#### **Q1: "How would you add groups (trip groups)?"**

```python
@dataclass
class Group:
    id: str
    name: str
    members: Set[User]
    expenses: List[Expense] = field(default_factory=list)
    
    def add_expense(self, expense: Expense):
        """Validate all participants are members."""
        for split in expense.splits:
            if split.user not in self.members:
                raise ValueError(f"{split.user.name} not in group")
        self.expenses.append(expense)
    
    def get_group_balances(self) -> Dict[str, Dict[str, float]]:
        """Get balances within this group only."""
        # Calculate balances from group expenses only
        pass
```

---

#### **Q2: "How would you handle recurring expenses?"**

```python
from datetime import timedelta

@dataclass
class RecurringExpense:
    template: Expense
    frequency: timedelta  # weekly, monthly
    next_due: datetime
    
    def generate_next(self) -> Expense:
        """Generate next expense from template."""
        expense = Expense.create(
            description=self.template.description,
            amount=self.template.amount,
            paid_by=self.template.paid_by,
            participants=self.template.participants,
            split_type=self.template.split_type
        )
        self.next_due += self.frequency
        return expense
```

---

#### **Q3: "How would you support multiple currencies?"**

```python
class CurrencyConverter:
    def __init__(self):
        self.rates = {"USD": 1.0, "EUR": 0.85, "GBP": 0.73}
    
    def convert(self, amount: float, from_curr: str, to_curr: str) -> float:
        usd_amount = amount / self.rates[from_curr]
        return usd_amount * self.rates[to_curr]

@dataclass
class Expense:
    amount: float
    currency: str = "USD"
    
    def get_amount_in(self, currency: str, converter: CurrencyConverter) -> float:
        return converter.convert(self.amount, self.currency, currency)
```

---

## ❌ Common Mistakes (What NOT to Do)

### **MISTAKE 1: Direct Floating Point Comparison** ❌

```python
# WRONG - Floating point precision issues!
if balance == 0:  # Might be 0.00000001
    ...

# CORRECT - Use epsilon
EPSILON = 0.01
if abs(balance) < EPSILON:
    ...
```

---

### **MISTAKE 2: O(n²) Debt Simplification** ❌

```python
# WRONG - Creates transaction for every pair!
for debtor in debtors:
    for creditor in creditors:
        transactions.append(...)  # O(n²) transactions!

# CORRECT - Net balance approach → O(n) transactions
net_balances = calculate_net_balances()
# Match debtors with creditors
```

---

### **MISTAKE 3: Not Validating Split Totals** ❌

```python
# WRONG - Trust the input
def exact_split(amount, split_data):
    return [Split(user, split_data[user]) for user in users]
    # What if split_data doesn't sum to amount?

# CORRECT - Validate first
if abs(sum(split_data.values()) - amount) > EPSILON:
    raise ValueError("Split doesn't sum to expense amount")
```

---

## 💯 Interview Checklist

- [ ] ✅ **Clarified requirements** (split types, groups, currency)
- [ ] ✅ **Used Strategy Pattern** for split types
- [ ] ✅ **Used Factory Pattern** for creating strategies
- [ ] ✅ **Handled floating point** with EPSILON
- [ ] ✅ **Implemented debt simplification** (greedy algorithm)
- [ ] ✅ **Validated split totals** match expense amount
- [ ] ✅ **Explained balance matrix** representation
- [ ] ✅ **Handled edge cases** (self-payment, overpay)
- [ ] ✅ **Discussed extensions** (groups, recurring, currency)

---

## 📚 Quick Reference Card

```
┌────────────────────────────────────────────────────────────┐
│                  SPLITWISE CHEAT SHEET                     │
├────────────────────────────────────────────────────────────┤
│ DESIGN PATTERNS:                                          │
│   - Strategy Pattern: Split types (Equal, Exact, Percent) │
│   - Factory Pattern: Create appropriate strategy          │
│                                                            │
│ BALANCE MATRIX:                                           │
│   balances[A][B] = amount A owes B                        │
│   Automatically maintain: balances[B][A] = -amount        │
│                                                            │
│ DEBT SIMPLIFICATION:                                      │
│   1. Calculate NET balance per user                       │
│   2. Separate debtors (positive) and creditors (negative)│
│   3. Greedy match: debtor pays creditor                   │
│   Result: O(n) transactions instead of O(n²)              │
│                                                            │
│ FLOATING POINT:                                           │
│   - EPSILON = 0.01 (one cent)                            │
│   - Always use abs(a - b) < EPSILON                      │
│   - Round output to 2 decimal places                      │
│                                                            │
│ COMPLEXITY:                                               │
│   - add_expense: O(P) participants                        │
│   - simplify_debts: O(U log U) users                     │
│   - settle_debt: O(1)                                    │
└────────────────────────────────────────────────────────────┘
```

---

**Related Problems:**
- Optimal Account Balancing (LeetCode 465)
- Graph algorithms (debt network is a graph)
- Min-Cost Max-Flow (optimal simplification)

