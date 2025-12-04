# 💰 PROBLEM 6: SPLITWISE / EXPENSE SHARING

### ⭐⭐⭐ **Design Expense Splitting System**

**Frequency:** MEDIUM at Atlassian
**Difficulty:** Medium-Hard
**Focus:** Graph Algorithms, Debt Simplification, Strategy Pattern

---

## 📋 Problem Statement

Design a system like Splitwise where users can:
- Add expenses
- Split expenses (equally, by percentage, exact amounts)
- Track who owes whom
- Simplify debts (minimize transactions)

**Core Requirements:**
- `add_expense(payer, amount, participants, split_type)`: Add an expense
- `get_balance(user)`: Get user's balance (owes/owed)
- `simplify_debts()`: Minimize number of transactions
- `settle_debt(from_user, to_user, amount)`: Record payment

---

## 🎯 Interview Approach

### Step 1: Clarify Requirements (2 min)
```
"Let me clarify the requirements:
1. What split types? Equal, exact amounts, percentages?
2. Do we need groups (like trip groups)?
3. Should we track expense history?
4. How to handle floating point precision?"
```

### Step 2: Design Classes (3 min)
```
"I'll use these core classes:
- User: Represents a participant
- Expense: Abstract class for different split types (Strategy Pattern)
- ExpenseManager: Manages balances and debt simplification
- Transaction: Represents simplified payment"
```

---

## 🎨 Visual Example

```text
Trip to Restaurant:
┌─────────────────────────────────────────┐
│ Total: $120, Paid by: Alice             │
│ Split: Equal among Alice, Bob, Charlie  │
│ Each share: $40                         │
└─────────────────────────────────────────┘

Resulting Debts:
┌──────────────────────────────────────┐
│ Bob → Alice: $40                     │
│ Charlie → Alice: $40                 │
└──────────────────────────────────────┘

After Movie ($60, paid by Bob, equal split):
┌──────────────────────────────────────┐
│ Alice → Bob: $20                     │
│ Charlie → Bob: $20                   │
└──────────────────────────────────────┘

Net Balances:
┌──────────────────────────────────────┐
│ Alice: +$20 (owed by others)         │
│ Bob: +$20 (owed by others)           │
│ Charlie: -$40 (owes to others)       │
└──────────────────────────────────────┘

Simplified: Charlie pays Alice $20, Charlie pays Bob $20
```

---

## 💻 Python Implementation

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Set, Optional
from abc import ABC, abstractmethod
from collections import defaultdict
import uuid
from datetime import datetime

class SplitType(Enum):
    """Types of expense splits"""
    EQUAL = "equal"
    EXACT = "exact"
    PERCENT = "percent"

@dataclass
class User:
    """Represents a user in the system"""
    id: str
    name: str
    email: str = ""
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return isinstance(other, User) and self.id == other.id

@dataclass
class Split:
    """Represents how much a user owes for an expense"""
    user: User
    amount: float

@dataclass
class Transaction:
    """Represents a simplified payment transaction"""
    from_user: str
    to_user: str
    amount: float
    
    def __str__(self):
        return f"{self.from_user} pays {self.to_user}: ${self.amount:.2f}"

# ============ Strategy Pattern for Split Types ============

class SplitStrategy(ABC):
    """Abstract base class for split strategies"""
    
    @abstractmethod
    def calculate_splits(self, amount: float, participants: List[User], 
                        split_data: Optional[Dict] = None) -> List[Split]:
        pass
    
    @abstractmethod
    def validate(self, amount: float, split_data: Optional[Dict]) -> bool:
        pass

class EqualSplitStrategy(SplitStrategy):
    """Split expense equally among participants"""
    
    def calculate_splits(self, amount: float, participants: List[User],
                        split_data: Optional[Dict] = None) -> List[Split]:
        if not participants:
            return []
        
        split_amount = amount / len(participants)
        return [Split(user=p, amount=split_amount) for p in participants]
    
    def validate(self, amount: float, split_data: Optional[Dict]) -> bool:
        return amount > 0

class ExactSplitStrategy(SplitStrategy):
    """Split expense by exact amounts"""
    
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
        return abs(total - amount) < 0.01  # Floating point tolerance

class PercentSplitStrategy(SplitStrategy):
    """Split expense by percentages"""
    
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

# ============ Factory for Split Strategies ============

class SplitStrategyFactory:
    """Factory to create appropriate split strategy"""
    
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

# ============ Expense Classes ============

@dataclass
class Expense:
    """Represents an expense"""
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
        """Factory method to create expense with proper splits"""
        
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
    Manages expenses and balances.
    
    Key Design Decisions:
    - Uses adjacency map for O(1) balance lookups
    - Greedy algorithm for debt simplification
    - Floating point tolerance for currency comparisons
    """
    
    EPSILON = 0.01  # Floating point tolerance
    
    def __init__(self):
        # user_id -> {other_user_id -> amount_owed}
        # Positive = you owe them, Negative = they owe you
        self._balances: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
        self._expenses: List[Expense] = []
        self._users: Dict[str, User] = {}
    
    def add_user(self, user: User) -> None:
        """Register a user"""
        self._users[user.id] = user
    
    def add_expense(self, expense: Expense) -> None:
        """
        Add an expense and update balances.
        Time: O(P) where P = participants
        """
        self._expenses.append(expense)
        
        payer = expense.paid_by
        
        for split in expense.splits:
            if split.user.id != payer.id:
                # split.user owes payer
                self._update_balance(split.user.id, payer.id, split.amount)
    
    def _update_balance(self, debtor_id: str, creditor_id: str, amount: float) -> None:
        """
        Update balance between two users.
        Maintains net balance to avoid duplicate entries.
        """
        # debtor owes creditor 'amount'
        self._balances[debtor_id][creditor_id] += amount
        self._balances[creditor_id][debtor_id] -= amount
    
    def get_balance(self, user_id: str) -> Dict[str, float]:
        """
        Get balance for a user.
        Returns: {other_user_id: amount} where positive = you owe, negative = they owe you
        Time: O(U) where U = users
        """
        result = {}
        for other_id, amount in self._balances[user_id].items():
            if abs(amount) > self.EPSILON:
                result[other_id] = round(amount, 2)
        return result
    
    def get_net_balance(self, user_id: str) -> float:
        """
        Get net balance (total owed - total to receive).
        Negative = net creditor, Positive = net debtor
        """
        return sum(self._balances[user_id].values())
    
    def simplify_debts(self) -> List[Transaction]:
        """
        Minimize number of transactions using greedy algorithm.
        
        Algorithm:
        1. Calculate net balance for each user
        2. Separate into debtors (owe money) and creditors (owed money)
        3. Match debtors with creditors greedily
        
        Time: O(U log U) for sorting
        Space: O(U) for net balances
        """
        # Step 1: Calculate net balances
        net_balances: Dict[str, float] = {}
        
        all_users = set(self._balances.keys())
        for user_id in all_users:
            net = sum(self._balances[user_id].values())
            if abs(net) > self.EPSILON:
                net_balances[user_id] = net
        
        # Step 2: Separate debtors and creditors
        debtors = []   # (user_id, amount_owed) - positive amounts
        creditors = [] # (user_id, amount_owed) - positive amounts
        
        for user_id, net in net_balances.items():
            if net > self.EPSILON:
                debtors.append([user_id, net])
            elif net < -self.EPSILON:
                creditors.append([user_id, -net])
        
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
        Returns True if successful.
        """
        current_debt = self._balances[from_user_id].get(to_user_id, 0)
        
        if current_debt < amount - self.EPSILON:
            return False  # Can't pay more than owed
        
        self._update_balance(from_user_id, to_user_id, -amount)
        return True
    
    def get_expense_history(self, user_id: str) -> List[Expense]:
        """Get all expenses involving a user"""
        return [
            exp for exp in self._expenses
            if exp.paid_by.id == user_id or 
               any(s.user.id == user_id for s in exp.splits)
        ]

# ============ Demo ============

def main():
    manager = ExpenseManager()
    
    # Create users
    alice = User(id="1", name="Alice")
    bob = User(id="2", name="Bob")
    charlie = User(id="3", name="Charlie")
    
    manager.add_user(alice)
    manager.add_user(bob)
    manager.add_user(charlie)
    
    # Expense 1: Alice paid $120 for dinner, split equally
    dinner = Expense.create(
        description="Dinner",
        amount=120.0,
        paid_by=alice,
        participants=[alice, bob, charlie],
        split_type=SplitType.EQUAL
    )
    manager.add_expense(dinner)
    
    print("=== After Dinner ($120, Alice paid, equal split) ===")
    print(f"Alice balance: {manager.get_balance(alice.id)}")
    print(f"Bob balance: {manager.get_balance(bob.id)}")
    print(f"Charlie balance: {manager.get_balance(charlie.id)}")
    
    # Expense 2: Bob paid $60 for movie, split equally
    movie = Expense.create(
        description="Movie",
        amount=60.0,
        paid_by=bob,
        participants=[alice, bob, charlie],
        split_type=SplitType.EQUAL
    )
    manager.add_expense(movie)
    
    print("\n=== After Movie ($60, Bob paid, equal split) ===")
    print(f"Alice balance: {manager.get_balance(alice.id)}")
    print(f"Bob balance: {manager.get_balance(bob.id)}")
    print(f"Charlie balance: {manager.get_balance(charlie.id)}")
    
    # Expense 3: Exact split example
    groceries = Expense.create(
        description="Groceries",
        amount=100.0,
        paid_by=charlie,
        participants=[alice, bob, charlie],
        split_type=SplitType.EXACT,
        split_data={"1": 30.0, "2": 50.0, "3": 20.0}  # Alice $30, Bob $50, Charlie $20
    )
    manager.add_expense(groceries)
    
    print("\n=== After Groceries ($100, Charlie paid, exact split) ===")
    print(f"Alice balance: {manager.get_balance(alice.id)}")
    print(f"Bob balance: {manager.get_balance(bob.id)}")
    print(f"Charlie balance: {manager.get_balance(charlie.id)}")
    
    # Simplify debts
    print("\n=== Simplified Transactions ===")
    transactions = manager.simplify_debts()
    for t in transactions:
        print(t)

if __name__ == "__main__":
    main()
```

---

## 🎯 Interview Explanation Flow

### 1. Start with Requirements (30 sec)
```
"For Splitwise, I need to handle:
- Multiple split types (Strategy Pattern)
- Efficient balance tracking (O(1) lookups)
- Debt simplification (minimize transactions)
- Floating point precision for currency"
```

### 2. Explain Core Design (1 min)
```
"I'm using:
1. Strategy Pattern for split types - easy to add new strategies
2. Factory Pattern to create appropriate strategy
3. Adjacency map for O(1) balance queries
4. Greedy algorithm for debt simplification"
```

### 3. Walk Through Key Methods (2 min)
```
"Key insight for simplify_debts():
- Calculate NET balance for each user
- A user either owes or is owed (not both after netting)
- Greedily match debtors with creditors
- This minimizes transactions from O(n²) to O(n)"
```

---

## 📊 Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| add_expense | O(P) | O(1) |
| get_balance | O(U) | O(U) |
| simplify_debts | O(U log U) | O(U) |
| settle_debt | O(1) | O(1) |

**Where:** P = participants per expense, U = total users

---

## 🚀 Extensions

### 1. Groups (Trip Groups)
```python
@dataclass
class Group:
    id: str
    name: str
    members: Set[User]
    expenses: List[Expense] = field(default_factory=list)
    
    def add_expense(self, expense: Expense):
        # Validate all participants are members
        for split in expense.splits:
            if split.user not in self.members:
                raise ValueError(f"{split.user.name} not in group")
        self.expenses.append(expense)
```

### 2. Recurring Expenses
```python
@dataclass
class RecurringExpense:
    template: Expense
    frequency: str  # "weekly", "monthly"
    next_due: datetime
```

### 3. Currency Support
```python
class CurrencyConverter:
    def convert(self, amount: float, from_curr: str, to_curr: str) -> float:
        # Use exchange rates
        pass
```

---

## 💡 Interview Tips

### What Interviewers Look For:
✅ **Strategy Pattern** for split types
✅ **Factory Pattern** for creating strategies
✅ **Greedy algorithm** for debt simplification
✅ **Floating point handling** (use EPSILON)
✅ **Clean separation** of concerns

### Common Mistakes:
❌ Not handling floating point precision
❌ O(n²) debt simplification when O(n) is possible
❌ Not validating split totals equal expense amount
❌ Missing edge cases (0 participants, self-payment)

### Questions to Ask:
- "How to handle currency conversion?"
- "Should we support recurring expenses?"
- "Do we need expense categories?"
- "How to handle expense deletion/modification?"

---

## 🔗 Related Concepts

- **Graph Theory**: Debt network is a weighted directed graph
- **Min-Cost Max-Flow**: Optimal debt simplification (advanced)
- **Floating Point Arithmetic**: Always use epsilon comparisons

