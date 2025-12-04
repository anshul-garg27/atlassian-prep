# 📋 PROBLEM 3: TRELLO / KANBAN BOARD SYSTEM

### ⭐⭐⭐⭐ **Design a Task Management System (Trello/Jira-like)**

**Frequency:** Appears in **MEDIUM-HIGH FREQUENCY** of Atlassian LLD rounds!
**Difficulty:** Medium
**Focus:** OOP Design, Relationships, State Management

---

## 📋 Problem Statement

Design a simplified Trello/Kanban board system where users can create boards, lists, and cards.

**Core Requirements:**
- **Board**: Contains multiple lists
- **List**: Contains multiple cards (e.g., "To Do", "In Progress", "Done")
- **Card**: Represents a task with title, description, assignee, due date
- Support operations: create, move, assign, delete
- Track card history (optional)

**Input:** User actions (create_board, add_list, add_card, move_card, etc.)
**Output:** Working system with proper data structures and relationships

**Constraints:**
- 1 ≤ Number of boards ≤ 1000 per user
- 1 ≤ Number of lists per board ≤ 50
- 1 ≤ Number of cards per list ≤ 1000
- Card title length ≤ 500 characters

---

## 🎤 How to Explain in Interview

### **Opening Statement (30 seconds)**
> "I'll design a Trello-like board using Python's `dataclasses` for clean entity modeling. The hierarchy is Board → List → Card, using composition. I'll use UUIDs for unique identifiers and follow the Single Responsibility Principle."

### **Key Points to Mention:**
1. "Using **dataclasses** for cleaner entity definitions"
2. "**Composition over inheritance** - Board HAS lists, List HAS cards"
3. "**UUID** for unique identifiers instead of auto-increment"
4. "Following **SRP** - separate classes for User, Board, List, Card"
5. "Easy to extend with **history tracking, permissions, checklists**"

---

## 🎨 Visual Example

```text
Board: "Sprint 2024"
├── List: "To Do"
│   ├── Card: "Implement Rate Limiter" (assigned: Alice, HIGH)
│   └── Card: "Write Tests" (assigned: Bob)
├── List: "In Progress"
│   └── Card: "Review PR #123" (assigned: Alice)
└── List: "Done"
    └── Card: "Deploy to Staging" (assigned: Charlie)

Operations:
1. move_card(card1, "To Do" → "In Progress")
2. assign_card(card2, Bob)
3. delete_card(card3)
4. add_label(card1, "Backend")
```

---

## 🎯 Design Patterns Used

### **1. Composition Pattern** ⭐
Board contains Lists, Lists contain Cards (HAS-A relationships).

```python
@dataclass
class Board:
    lists: List[TaskList] = field(default_factory=list)
    # Board HAS lists (composition, not inheritance)
```

### **2. Factory Pattern** (Optional)
Create entities through service methods for validation.

```python
class TrelloService:
    def create_board(self, name: str, owner: User) -> Board:
        # Validation, logging, etc.
        board = Board(name=name, owner=owner)
        self.boards[board.id] = board
        return board
```

### **3. Observer Pattern** (For Extensions)
Notify listeners when cards move or update.

```python
class Card:
    def move_to(self, new_list):
        old_list = self.current_list
        # ... move logic
        self._notify_observers("moved", old_list, new_list)
```

---

## 🏗️ Class Design

```text
┌────────────┐
│    User    │
├────────────┤
│ - id: str  │
│ - name: str│
│ - email    │
└────────────┘
      │ 1:N (owns/member)
      │
      ▼
┌────────────────┐
│     Board      │
├────────────────┤
│ - id: str      │
│ - name: str    │
│ - owner: User  │
│ - members: Set │
│ - lists: List  │◀────────┐
└────────────────┘         │ contains
                    ┌──────┴─────────┐
                    │   TaskList     │
                    ├────────────────┤
                    │ - id: str      │
                    │ - name: str    │
                    │ - position: int│
                    │ - cards: List  │◀────────┐
                    └────────────────┘         │ contains
                                        ┌──────┴────────┐
                                        │     Card      │
                                        ├───────────────┤
                                        │ - id: str     │
                                        │ - title: str  │
                                        │ - desc: str   │
                                        │ - assignee    │
                                        │ - due_date    │
                                        │ - labels: Set │
                                        │ - priority    │
                                        └───────────────┘
```

---

## 💻 Python Implementation (Production-Ready)

```python
"""
Trello / Kanban Board System - Low-Level Design
================================================
Clean OOP implementation using Python's dataclasses.

Design Patterns:
- Composition: Board → Lists → Cards
- Factory Pattern: TrelloService creates entities
- Single Responsibility: Each class has one purpose

Features:
- Board management (create, delete)
- List management (create, reorder)
- Card management (create, move, assign, labels)
- Member management (add/remove)
"""

from dataclasses import dataclass, field
from typing import List, Set, Dict, Optional
from datetime import date, datetime
from enum import Enum
import uuid


def generate_id(prefix: str = "") -> str:
    """Generate unique ID with optional prefix."""
    return f"{prefix}{uuid.uuid4().hex[:8]}"


class Priority(Enum):
    """Card priority levels."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

    def __str__(self):
        return self.name


@dataclass
class User:
    """
    User entity.
    
    Attributes:
        name: Display name
        email: User email (unique identifier in real system)
        id: Unique identifier
    """
    name: str
    email: str
    id: str = field(default_factory=lambda: generate_id("USER_"))
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.id == other.id


@dataclass
class Label:
    """
    Card label for categorization.
    
    Attributes:
        name: Label text (e.g., "Backend", "Bug")
        color: Hex color code (e.g., "#FF5733")
    """
    name: str
    color: str = "#3B82F6"  # Default blue
    
    def __hash__(self):
        return hash(self.name)
    
    def __eq__(self, other):
        if not isinstance(other, Label):
            return False
        return self.name == other.name


@dataclass
class Card:
    """
    Card/Task entity.
    
    Attributes:
        title: Card title (required)
        description: Detailed description
        assignee: User assigned to the card
        due_date: Due date for the task
        priority: Priority level
        labels: Set of labels
        created_at: Creation timestamp
        comments: List of comments
    """
    title: str
    description: str = ""
    id: str = field(default_factory=lambda: generate_id("CARD_"))
    assignee: Optional[User] = None
    due_date: Optional[date] = None
    priority: Optional[Priority] = None
    labels: Set[Label] = field(default_factory=set)
    created_at: datetime = field(default_factory=datetime.now)
    comments: List[str] = field(default_factory=list)

    def assign(self, user: User) -> None:
        """Assign card to user."""
        self.assignee = user

    def unassign(self) -> None:
        """Remove assignee from card."""
        self.assignee = None
    
    def set_due_date(self, due: date) -> None:
        """Set due date."""
        self.due_date = due
    
    def set_priority(self, priority: Priority) -> None:
        """Set priority level."""
        self.priority = priority
    
    def add_label(self, label: Label) -> None:
        """Add label to card."""
        self.labels.add(label)

    def remove_label(self, label: Label) -> None:
        """Remove label from card."""
        self.labels.discard(label)
    
    def add_comment(self, comment: str) -> None:
        """Add comment to card."""
        self.comments.append(comment)

    def is_overdue(self) -> bool:
        """Check if card is past due date."""
        if self.due_date is None:
            return False
        return date.today() > self.due_date
    
    def __str__(self):
        assignee_name = self.assignee.name if self.assignee else "Unassigned"
        due = self.due_date or "No due date"
        priority = self.priority or "No priority"
        return f"Card[{self.id}]: {self.title} | {assignee_name} | Due: {due} | {priority}"


@dataclass
class TaskList:
    """
    List/Column in a board (e.g., "To Do", "In Progress", "Done").
    
    Attributes:
        name: List name
        position: Order position in board
        cards: Cards in this list
    """
    name: str
    position: int = 0
    id: str = field(default_factory=lambda: generate_id("LIST_"))
    cards: List[Card] = field(default_factory=list)

    def add_card(self, card: Card) -> None:
        """Add card to end of list."""
        self.cards.append(card)

    def remove_card(self, card: Card) -> bool:
        """Remove card from list. Returns True if found and removed."""
        if card in self.cards:
            self.cards.remove(card)
            return True
        return False

    def get_card(self, card_id: str) -> Optional[Card]:
        """Find card by ID."""
        for card in self.cards:
            if card.id == card_id:
                return card
        return None

    def move_card_to_position(self, card: Card, position: int) -> None:
        """Move card to specific position within list."""
        if card in self.cards:
            self.cards.remove(card)
            self.cards.insert(min(position, len(self.cards)), card)
    
    def __str__(self):
        return f"List[{self.id}]: {self.name} ({len(self.cards)} cards)"


@dataclass
class Board:
    """
    Kanban Board containing lists and managing members.
    
    Attributes:
        name: Board name
        owner: User who created the board
        members: Set of users with access
        lists: Ordered lists in the board
    """
    name: str
    owner: User
    id: str = field(default_factory=lambda: generate_id("BOARD_"))
    members: Set[User] = field(default_factory=set)
    lists: List[TaskList] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Add owner to members automatically."""
        self.members.add(self.owner)

    # ========== List Operations ==========
    
    def create_list(self, name: str) -> TaskList:
        """Create new list at end of board."""
        task_list = TaskList(name=name, position=len(self.lists))
        self.lists.append(task_list)
        return task_list

    def get_list(self, list_id: str) -> Optional[TaskList]:
        """Find list by ID."""
        for lst in self.lists:
            if lst.id == list_id:
                return lst
        return None

    def get_list_by_name(self, name: str) -> Optional[TaskList]:
        """Find list by name."""
        for lst in self.lists:
            if lst.name == name:
                return lst
        return None
    
    def delete_list(self, list_id: str) -> bool:
        """Delete list by ID. Returns True if found and deleted."""
        for i, lst in enumerate(self.lists):
            if lst.id == list_id:
                self.lists.pop(i)
                return True
        return False
    
    def reorder_lists(self, list_ids: List[str]) -> None:
        """Reorder lists based on provided ID order."""
        id_to_list = {lst.id: lst for lst in self.lists}
        self.lists = [id_to_list[lid] for lid in list_ids if lid in id_to_list]
        for i, lst in enumerate(self.lists):
            lst.position = i
    
    # ========== Card Operations ==========
    
    def create_card(self, list_id: str, title: str, 
                    description: str = "") -> Card:
        """Create card in specified list."""
        task_list = self.get_list(list_id)
        if not task_list:
            raise ValueError(f"List not found: {list_id}")

        card = Card(title=title, description=description)
        task_list.add_card(card)
        return card

    def move_card(self, card_id: str, from_list_id: str, 
                  to_list_id: str) -> bool:
        """Move card between lists."""
        from_list = self.get_list(from_list_id)
        to_list = self.get_list(to_list_id)

        if not from_list or not to_list:
            raise ValueError("List not found")

        card = from_list.get_card(card_id)
        if not card:
            raise ValueError(f"Card not found: {card_id}")

        from_list.remove_card(card)
        to_list.add_card(card)
        return True
    
    def delete_card(self, card_id: str) -> bool:
        """Delete card from any list. Returns True if found."""
        for lst in self.lists:
            card = lst.get_card(card_id)
            if card:
                lst.remove_card(card)
                return True
        return False
    
    def find_card(self, card_id: str) -> Optional[Card]:
        """Find card in any list."""
        for lst in self.lists:
            card = lst.get_card(card_id)
            if card:
                return card
        return None
    
    # ========== Member Operations ==========
    
    def add_member(self, user: User) -> None:
        """Add member to board."""
        self.members.add(user)

    def remove_member(self, user: User) -> bool:
        """Remove member (cannot remove owner)."""
        if user == self.owner:
            return False
        self.members.discard(user)
        return True
    
    def is_member(self, user: User) -> bool:
        """Check if user is a member."""
        return user in self.members
    
    # ========== Query Operations ==========
    
    def get_all_cards(self) -> List[Card]:
        """Get all cards across all lists."""
        return [card for lst in self.lists for card in lst.cards]
    
    def get_cards_by_assignee(self, user: User) -> List[Card]:
        """Get all cards assigned to a user."""
        return [card for card in self.get_all_cards() 
                if card.assignee == user]
    
    def get_overdue_cards(self) -> List[Card]:
        """Get all overdue cards."""
        return [card for card in self.get_all_cards() 
                if card.is_overdue()]
    
    def get_cards_by_label(self, label: Label) -> List[Card]:
        """Get all cards with a specific label."""
        return [card for card in self.get_all_cards() 
                if label in card.labels]
    
    def __str__(self):
        return f"Board[{self.id}]: {self.name} | Owner: {self.owner.name} | {len(self.lists)} lists"


class TrelloService:
    """
    Service layer for managing boards and users.
    Acts as a facade for the system.
    """
    
    def __init__(self):
        self.boards: Dict[str, Board] = {}
        self.users: Dict[str, User] = {}

    def create_user(self, name: str, email: str) -> User:
        """Create and register a new user."""
        user = User(name=name, email=email)
        self.users[user.id] = user
        return user

    def create_board(self, name: str, owner: User) -> Board:
        """Create and register a new board."""
        board = Board(name=name, owner=owner)
        self.boards[board.id] = board
        return board

    def get_board(self, board_id: str) -> Optional[Board]:
        """Get board by ID."""
        return self.boards.get(board_id)

    def delete_board(self, board_id: str) -> bool:
        """Delete board. Returns True if found."""
        if board_id in self.boards:
            del self.boards[board_id]
            return True
        return False
    
    def get_boards_for_user(self, user: User) -> List[Board]:
        """Get all boards where user is a member."""
        return [board for board in self.boards.values()
                if board.is_member(user)]


# ============ Demo / Usage ============
if __name__ == "__main__":
    print("=== Trello Board System Demo ===\n")
    
    # Create service
    trello = TrelloService()

    # Create users
    alice = trello.create_user("Alice", "alice@example.com")
    bob = trello.create_user("Bob", "bob@example.com")
    print(f"Created users: {alice.name}, {bob.name}")

    # Create board
    board = trello.create_board("Sprint 2024", alice)
    board.add_member(bob)
    print(f"\nCreated board: {board}")

    # Create lists
    todo_list = board.create_list("To Do")
    progress_list = board.create_list("In Progress")
    done_list = board.create_list("Done")
    print(f"\nCreated lists: {[l.name for l in board.lists]}")

    # Create cards
    card1 = board.create_card(todo_list.id, "Implement Rate Limiter",
                              "Use token bucket algorithm")
    card1.assign(alice)
    card1.set_priority(Priority.HIGH)
    card1.add_label(Label("Backend", "#10B981"))

    card2 = board.create_card(todo_list.id, "Write Tests",
                              "Unit tests for all components")
    card2.assign(bob)
    card2.set_due_date(date.today())
    
    card3 = board.create_card(progress_list.id, "Review PR #123",
                              "Security review needed")
    card3.assign(alice)
    
    # Print board state
    print("\n" + "=" * 50)
    print("BOARD STATE")
    print("=" * 50)
    print(board)
    print("-" * 50)
    for lst in board.lists:
        print(f"\n📋 {lst.name}")
        for card in lst.cards:
            print(f"   └─ {card}")

    # Move card
    print("\n" + "=" * 50)
    print("AFTER MOVING CARD")
    print("=" * 50)
    board.move_card(card1.id, todo_list.id, progress_list.id)

    for lst in board.lists:
        print(f"\n📋 {lst.name}")
        for card in lst.cards:
            print(f"   └─ {card}")
    
    # Query operations
    print("\n" + "=" * 50)
    print("QUERIES")
    print("=" * 50)
    print(f"\nAlice's cards: {len(board.get_cards_by_assignee(alice))}")
    print(f"Overdue cards: {len(board.get_overdue_cards())}")
```

---

## 🚀 Extensions & Follow-ups

### **Extension 1: Activity/History Log**
```python
from datetime import datetime

@dataclass
class Activity:
    """Activity log entry."""
    user: User
    action: str  # "created", "moved", "assigned", "commented"
    timestamp: datetime
    details: str

@dataclass
class Card:
    history: List[Activity] = field(default_factory=list)
    
    def log_activity(self, user: User, action: str, details: str = ""):
        self.history.append(Activity(user, action, datetime.now(), details))
    
    def assign(self, user: User, assigned_by: User):
        self.assignee = user
        self.log_activity(assigned_by, "assigned", f"Assigned to {user.name}")
```

### **Extension 2: Checklist**
```python
@dataclass
class ChecklistItem:
    text: str
    completed: bool = False

@dataclass
class Card:
    checklist: List[ChecklistItem] = field(default_factory=list)
    
    def add_checklist_item(self, text: str):
        self.checklist.append(ChecklistItem(text))
    
    def toggle_checklist_item(self, index: int):
        if 0 <= index < len(self.checklist):
            self.checklist[index].completed = not self.checklist[index].completed
    
    @property
    def checklist_progress(self) -> float:
        if not self.checklist:
            return 0.0
        completed = sum(1 for item in self.checklist if item.completed)
        return completed / len(self.checklist) * 100
```

### **Extension 3: Permissions/Access Control**
```python
class Permission(Enum):
    VIEW = 1
    EDIT = 2
    ADMIN = 3

@dataclass
class Board:
    permissions: Dict[str, Permission] = field(default_factory=dict)
    
    def set_permission(self, user: User, permission: Permission):
        self.permissions[user.id] = permission
    
    def can_edit(self, user: User) -> bool:
        perm = self.permissions.get(user.id, Permission.VIEW)
        return perm in (Permission.EDIT, Permission.ADMIN)
```

---

## 🧪 Testing Strategy

```python
import pytest
from datetime import date, timedelta

class TestTrelloBoard:
    
    def test_create_board(self):
        """Board created with owner as member."""
        alice = User("Alice", "alice@example.com")
        board = Board(name="Test Board", owner=alice)
        
        assert board.name == "Test Board"
        assert board.owner == alice
        assert alice in board.members
    
    def test_create_list(self):
        """Lists created with correct position."""
        board = Board("Board", User("Alice", "alice@example.com"))
        
        list1 = board.create_list("To Do")
        list2 = board.create_list("Done")
        
        assert len(board.lists) == 2
        assert list1.position == 0
        assert list2.position == 1
    
    def test_move_card(self):
        """Card moves between lists correctly."""
        board = Board("Board", User("Alice", "alice@example.com"))
        list1 = board.create_list("List 1")
        list2 = board.create_list("List 2")
        card = board.create_card(list1.id, "Card", "Desc")
        
        assert len(list1.cards) == 1
        assert len(list2.cards) == 0
        
        board.move_card(card.id, list1.id, list2.id)
        
        assert len(list1.cards) == 0
        assert len(list2.cards) == 1
    
    def test_move_card_invalid_list(self):
        """Moving to invalid list raises error."""
        board = Board("Board", User("Alice", "alice@example.com"))
        list1 = board.create_list("List 1")
        card = board.create_card(list1.id, "Card", "Desc")
        
        with pytest.raises(ValueError):
            board.move_card(card.id, list1.id, "INVALID_ID")
    
    def test_card_assignment(self):
        """Cards can be assigned and unassigned."""
        alice = User("Alice", "alice@example.com")
        card = Card("Task")
        
        card.assign(alice)
        assert card.assignee == alice
        
        card.unassign()
        assert card.assignee is None
    
    def test_overdue_cards(self):
        """Overdue cards detected correctly."""
        board = Board("Board", User("Alice", "alice@example.com"))
        lst = board.create_list("List")
        card = board.create_card(lst.id, "Card")
        
        # Set due date in past
        card.set_due_date(date.today() - timedelta(days=1))
        
        overdue = board.get_overdue_cards()
        assert card in overdue
    
    def test_cannot_remove_owner(self):
        """Owner cannot be removed from board."""
        alice = User("Alice", "alice@example.com")
        board = Board("Board", alice)
        
        result = board.remove_member(alice)
        
        assert result == False
        assert alice in board.members
```

---

## 📊 Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| `create_board` | O(1) | O(1) |
| `create_list` | O(1) | O(1) |
| `create_card` | O(1) | O(1) |
| `move_card` | O(L + C) | O(1) |
| `get_all_cards` | O(L × C) | O(L × C) |
| `get_cards_by_assignee` | O(L × C) | O(K) |

**Where:** L = lists, C = cards per list, K = matching cards

---

## 💯 Interview Checklist

Before finishing, ensure you've mentioned:
- [ ] ✅ **Dataclasses** for clean entity modeling
- [ ] ✅ **Composition** (Board HAS Lists HAS Cards)
- [ ] ✅ **UUID** for unique identifiers
- [ ] ✅ **SRP** - separate classes for each entity
- [ ] ✅ **Member management** (owner can't be removed)
- [ ] ✅ **Query methods** (by assignee, overdue, label)
- [ ] ✅ **Extensions** (history, checklist, permissions)
- [ ] ✅ **Testing strategy**

---

**Related Problems:**
- Jira Board Design
- GitHub Projects
- Monday.com
