# 📋 PROBLEM 3: TRELLO / KANBAN BOARD SYSTEM

### ⭐⭐⭐⭐ **Design a Task Management System (Trello/Jira-like)**

**Frequency:** MEDIUM-HIGH at Atlassian LLD rounds!
**Difficulty:** Medium
**Time to Solve:** 35-45 minutes
**Focus:** OOP Design, Entity Relationships, State Management

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

## 🎯 INTERVIEW FLOW: Step-by-Step Guide

### **PHASE 1: Clarify Requirements (2-3 minutes)**

**SAY THIS:**
> "Before I start designing, let me clarify a few requirements:"

**Questions to Ask:**
1. "What entities do we need? (User, Board, List, Card, Labels?)"
2. "Can a card belong to multiple lists? Or is it 1:1?"
3. "Do we need permissions? (Owner, Admin, Member, Viewer)"
4. "Should we track card history/activity?"
5. "Do we need due dates, priorities, labels?"
6. "Is this single-user or multi-user with shared boards?"

**WRITE DOWN the answers. This shows you're thorough.**

---

### **PHASE 2: Identify Entity Relationships (3-4 minutes)**

**SAY THIS:**
> "Let me identify the key entities and their relationships."

**Draw on whiteboard:**
```
┌──────────┐     1:N      ┌──────────┐     1:N      ┌──────────┐
│   User   │─────────────▶│  Board   │─────────────▶│   List   │
└──────────┘  owns/member └──────────┘   contains   └──────────┘
                                                          │
                                                          │ 1:N
                                                          ▼
                                                    ┌──────────┐
                                                    │   Card   │
                                                    └──────────┘
                                                          │
                                              ┌───────────┼───────────┐
                                              │           │           │
                                           Labels     Assignee    Comments
```

**Explain:**
> "The hierarchy is: User → Board → List → Card
> 
> Key relationships:
> - User can own multiple Boards (1:N)
> - Board can have multiple members (N:N)
> - Board contains multiple Lists (1:N, Composition)
> - List contains multiple Cards (1:N, Composition)
> - Card can have one assignee (N:1 to User)
> - Card can have multiple Labels (N:N)"

---

### **PHASE 3: High-Level Design (2-3 minutes)**

**SAY THIS:**
> "Let me draw the class structure using Composition pattern."

```
┌─────────────────────────────────────────────────────────┐
│                    TrelloService                        │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Facade - Entry point for all operations        │   │
│  │                                                  │   │
│  │  - users: Dict[str, User]                       │   │
│  │  - boards: Dict[str, Board]                     │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  + create_user(name, email) → User                     │
│  + create_board(name, owner) → Board                   │
│  + get_boards_for_user(user) → List[Board]             │
└─────────────────────────────────────────────────────────┘

┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│    Board     │   │   TaskList   │   │     Card     │
├──────────────┤   ├──────────────┤   ├──────────────┤
│ - name       │   │ - name       │   │ - title      │
│ - owner      │   │ - position   │   │ - description│
│ - members    │   │ - cards      │   │ - assignee   │
│ - lists      │   └──────────────┘   │ - due_date   │
└──────────────┘                      │ - labels     │
      │                               │ - priority   │
      │ contains (composition)        └──────────────┘
      ▼
┌──────────────┐   ┌──────────────┐
│   Label      │   │   Priority   │
├──────────────┤   ├──────────────┤
│ - name       │   │ LOW          │
│ - color      │   │ MEDIUM       │
└──────────────┘   │ HIGH         │
                   │ CRITICAL     │
                   └──────────────┘
```

**Explain the hierarchy:**
> "I'm using **Composition** - Board HAS Lists, Lists HAS Cards.
> This means when a Board is deleted, its Lists and Cards are also deleted.
> The TrelloService acts as a **Facade** for the entire system."

---

### **PHASE 4: Design Patterns & Principles (2 minutes)**

**SAY THIS:**
> "I'm using several design patterns here."

#### **1. Composition Pattern** ⭐⭐⭐

```python
@dataclass
class Board:
    name: str
    owner: User
    lists: List[TaskList] = field(default_factory=list)  # Board HAS Lists
    
@dataclass
class TaskList:
    name: str
    cards: List[Card] = field(default_factory=list)  # List HAS Cards
```

**Why Composition over Inheritance?**
> "A Board IS-NOT-A List. A Board HAS Lists. This is the classic HAS-A vs IS-A decision."

---

#### **2. Facade Pattern** ⭐⭐

```python
class TrelloService:
    """Facade - Single entry point for the system."""
    
    def create_board(self, name: str, owner: User) -> Board:
        # Validation, logging, event publishing, etc.
        board = Board(name=name, owner=owner)
        self.boards[board.id] = board
        return board
```

**Why Facade?**
> "Instead of clients directly creating entities, they go through TrelloService.
> This allows us to add validation, logging, events without changing entity classes."

---

#### **3. Factory Pattern** (Optional) ⭐

```python
class CardFactory:
    """Factory for creating cards with validation."""
    
    @staticmethod
    def create(title: str, board: Board) -> Card:
        if len(title) > 500:
            raise ValueError("Title too long")
        if not board.is_member(current_user):
            raise PermissionError("Not a board member")
        return Card(title=title)
```

---

### **PHASE 5: Data Structures & Why (2 minutes)**

**SAY THIS:**
> "Let me explain my data structure choices."

| Data Structure | Used For | Why This Choice |
|----------------|----------|-----------------|
| `Dict[str, Board]` | Board storage | O(1) lookup by ID |
| `List[TaskList]` | Lists in board | Ordered, supports reordering |
| `List[Card]` | Cards in list | Ordered, supports reordering |
| `Set[User]` | Board members | O(1) membership check, no duplicates |
| `Set[Label]` | Card labels | O(1) add/remove, no duplicates |
| `dataclass` | All entities | Clean initialization, less boilerplate |
| `Enum` | Priority | Type safety, defined set of values |
| `UUID` | Entity IDs | Globally unique, no collision |

**Key Insight:**
> "I use UUIDs instead of auto-increment IDs because:
> 1. No need for central ID generator
> 2. IDs can be generated client-side
> 3. Works in distributed systems"

---

### **PHASE 6: Write the Code (15-20 minutes)**

**SAY THIS:**
> "Now let me implement this. I'll start with enums and small classes, then build up to Board and TrelloService."

```python
"""
Trello / Kanban Board System - Low-Level Design
================================================
Clean OOP implementation using Python's dataclasses.

Design Patterns:
- Composition: Board → Lists → Cards (HAS-A relationships)
- Facade: TrelloService as single entry point
- Factory: Entity creation with validation

Features:
- Board management (create, delete, members)
- List management (create, reorder)
- Card management (create, move, assign, labels)
- Query operations (by assignee, overdue, label)
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
    
    Uses id for equality/hashing so two User objects
    with same id are considered equal.
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
    """Card label for categorization."""
    name: str
    color: str = "#3B82F6"  # Default blue
    
    def __hash__(self):
        return hash(self.name.lower())  # Case-insensitive
    
    def __eq__(self, other):
        if not isinstance(other, Label):
            return False
        return self.name.lower() == other.name.lower()


@dataclass
class Card:
    """
    Card/Task entity - the core unit of work.
    
    Responsibilities:
    - Store task information
    - Manage assignee, labels, priority
    - Track due dates and comments
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
        """Add label to card. O(1)"""
        self.labels.add(label)

    def remove_label(self, label: Label) -> None:
        """Remove label from card. O(1)"""
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
        due = str(self.due_date) if self.due_date else "No due date"
        priority = str(self.priority) if self.priority else "No priority"
        return f"[{self.id}] {self.title} | {assignee_name} | Due: {due} | {priority}"


@dataclass
class TaskList:
    """
    List/Column in a board (e.g., "To Do", "In Progress", "Done").
    
    Contains cards in a specific order.
    """
    name: str
    position: int = 0
    id: str = field(default_factory=lambda: generate_id("LIST_"))
    cards: List[Card] = field(default_factory=list)

    def add_card(self, card: Card) -> None:
        """Add card to end of list. O(1)"""
        self.cards.append(card)

    def remove_card(self, card: Card) -> bool:
        """Remove card from list. Returns True if found. O(N)"""
        if card in self.cards:
            self.cards.remove(card)
            return True
        return False

    def get_card(self, card_id: str) -> Optional[Card]:
        """Find card by ID. O(N)"""
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
        return f"[{self.id}] {self.name} ({len(self.cards)} cards)"


@dataclass
class Board:
    """
    Kanban Board containing lists and managing members.
    
    Main entity that users interact with.
    Implements Composition - owns its Lists and Cards.
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
        """Find list by ID. O(L) where L = number of lists."""
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
        """Delete list by ID."""
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
        """Delete card from any list."""
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
        """Add member to board. O(1)"""
        self.members.add(user)

    def remove_member(self, user: User) -> bool:
        """Remove member (cannot remove owner)."""
        if user == self.owner:
            return False  # Owner cannot be removed
        self.members.discard(user)
        return True
    
    def is_member(self, user: User) -> bool:
        """Check if user is a member. O(1)"""
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
    
    def get_cards_by_priority(self, priority: Priority) -> List[Card]:
        """Get all cards with specific priority."""
        return [card for card in self.get_all_cards() 
                if card.priority == priority]
    
    def __str__(self):
        return f"[{self.id}] {self.name} | Owner: {self.owner.name} | {len(self.lists)} lists"


class TrelloService:
    """
    Service layer / Facade for managing boards and users.
    
    Single entry point for the system.
    Handles validation, cross-cutting concerns.
    """
    
    def __init__(self):
        self.boards: Dict[str, Board] = {}
        self.users: Dict[str, User] = {}

    def create_user(self, name: str, email: str) -> User:
        """Create and register a new user."""
        if not name or not email:
            raise ValueError("Name and email are required")
        
        user = User(name=name, email=email)
        self.users[user.id] = user
        return user

    def create_board(self, name: str, owner: User) -> Board:
        """Create and register a new board."""
        if not name:
            raise ValueError("Board name is required")
        if owner.id not in self.users:
            raise ValueError("Owner must be a registered user")
        
        board = Board(name=name, owner=owner)
        self.boards[board.id] = board
        return board

    def get_board(self, board_id: str) -> Optional[Board]:
        """Get board by ID. O(1)"""
        return self.boards.get(board_id)

    def delete_board(self, board_id: str) -> bool:
        """Delete board."""
        if board_id in self.boards:
            del self.boards[board_id]
            return True
        return False
    
    def get_boards_for_user(self, user: User) -> List[Board]:
        """Get all boards where user is a member."""
        return [board for board in self.boards.values()
                if board.is_member(user)]


# ============ Demo ============
def main():
    """Demonstrate Trello Board functionality."""
    print("=" * 60)
    print("TRELLO BOARD SYSTEM DEMO")
    print("=" * 60)
    
    # Create service
    trello = TrelloService()

    # Create users
    alice = trello.create_user("Alice", "alice@example.com")
    bob = trello.create_user("Bob", "bob@example.com")
    print(f"\n✓ Created users: {alice.name}, {bob.name}")

    # Create board
    board = trello.create_board("Sprint 2024", alice)
    board.add_member(bob)
    print(f"✓ Created board: {board}")

    # Create lists
    todo_list = board.create_list("To Do")
    progress_list = board.create_list("In Progress")
    done_list = board.create_list("Done")
    print(f"✓ Created lists: {[l.name for l in board.lists]}")

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
    print("\n" + "=" * 60)
    print("BOARD STATE")
    print("=" * 60)
    print(board)
    for lst in board.lists:
        print(f"\n📋 {lst.name}")
        for card in lst.cards:
            print(f"   └─ {card}")

    # Move card
    print("\n" + "=" * 60)
    print("MOVE CARD: Rate Limiter → In Progress")
    print("=" * 60)
    board.move_card(card1.id, todo_list.id, progress_list.id)

    for lst in board.lists:
        print(f"\n📋 {lst.name}")
        for card in lst.cards:
            print(f"   └─ {card}")
    
    # Query operations
    print("\n" + "=" * 60)
    print("QUERIES")
    print("=" * 60)
    print(f"Alice's cards: {len(board.get_cards_by_assignee(alice))}")
    print(f"Overdue cards: {len(board.get_overdue_cards())}")
    print(f"High priority: {len(board.get_cards_by_priority(Priority.HIGH))}")


if __name__ == "__main__":
    main()
```

---

### **PHASE 7: Walk Through Edge Cases (3-4 minutes)**

**SAY THIS:**
> "Let me discuss the edge cases I've handled."

| Edge Case | How Handled | Code Location |
|-----------|-------------|---------------|
| **Remove board owner** | Return False, owner stays | `remove_member()` |
| **Move card to invalid list** | Raise ValueError | `move_card()` |
| **Create card in non-existent list** | Raise ValueError | `create_card()` |
| **Duplicate labels on card** | Set prevents duplicates | `labels: Set[Label]` |
| **Empty board/card name** | Raise ValueError | Service layer validation |
| **User not registered** | Raise ValueError | Service validation |
| **Case-insensitive labels** | Label `__hash__` uses `.lower()` | `Label.__hash__()` |

---

### **PHASE 8: Testing Strategy (2-3 minutes)**

```python
import pytest
from datetime import date, timedelta

class TestTrelloBoard:
    
    def test_create_board_with_owner_as_member(self):
        """Board created with owner automatically as member."""
        alice = User("Alice", "alice@example.com")
        board = Board(name="Test Board", owner=alice)
        
        assert board.name == "Test Board"
        assert board.owner == alice
        assert alice in board.members
    
    def test_create_list_with_position(self):
        """Lists created with correct position."""
        board = Board("Board", User("Alice", "alice@example.com"))
        
        list1 = board.create_list("To Do")
        list2 = board.create_list("Done")
        
        assert len(board.lists) == 2
        assert list1.position == 0
        assert list2.position == 1
    
    def test_move_card_between_lists(self):
        """Card moves correctly between lists."""
        board = Board("Board", User("Alice", "alice@example.com"))
        list1 = board.create_list("List 1")
        list2 = board.create_list("List 2")
        card = board.create_card(list1.id, "Card", "Desc")
        
        assert len(list1.cards) == 1
        assert len(list2.cards) == 0
        
        board.move_card(card.id, list1.id, list2.id)
        
        assert len(list1.cards) == 0
        assert len(list2.cards) == 1
    
    def test_move_card_to_invalid_list_raises(self):
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
    
    def test_overdue_cards_detection(self):
        """Overdue cards detected correctly."""
        board = Board("Board", User("Alice", "alice@example.com"))
        lst = board.create_list("List")
        card = board.create_card(lst.id, "Card")
        
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
    
    def test_label_case_insensitive(self):
        """Labels are case-insensitive."""
        card = Card("Task")
        card.add_label(Label("Backend"))
        card.add_label(Label("BACKEND"))  # Same as above
        
        assert len(card.labels) == 1  # No duplicate
```

---

### **PHASE 9: Complexity Analysis (1 minute)**

| Operation | Time | Space |
|-----------|------|-------|
| `create_board` | O(1) | O(1) |
| `create_list` | O(1) | O(1) |
| `create_card` | O(L) | O(1) |
| `move_card` | O(L + C) | O(1) |
| `get_all_cards` | O(L × C) | O(L × C) |
| `is_member` | O(1) | O(1) |
| `add_label` | O(1) | O(1) |

**Where:** L = lists, C = cards per list

---

### **PHASE 10: Extensions & Follow-ups (5+ minutes)**

#### **Q1: "How would you add activity history?"**

```python
@dataclass
class Activity:
    """Activity log entry."""
    user: User
    action: str  # "created", "moved", "assigned"
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

---

#### **Q2: "How would you add permissions?"**

```python
class Permission(Enum):
    VIEW = 1
    EDIT = 2
    ADMIN = 3

@dataclass
class BoardMember:
    user: User
    permission: Permission

@dataclass
class Board:
    member_permissions: Dict[str, Permission] = field(default_factory=dict)
    
    def can_edit(self, user: User) -> bool:
        perm = self.member_permissions.get(user.id, Permission.VIEW)
        return perm in (Permission.EDIT, Permission.ADMIN)
```

---

#### **Q3: "How would you add checklists?"**

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
    
    @property
    def checklist_progress(self) -> float:
        if not self.checklist:
            return 0.0
        completed = sum(1 for item in self.checklist if item.completed)
        return completed / len(self.checklist) * 100
```

---

## ❌ Common Mistakes (What NOT to Do)

### **MISTAKE 1: No ID Generation Strategy** ❌

```python
# WRONG - Auto-increment doesn't work in distributed systems
class Card:
    _counter = 0
    def __init__(self):
        Card._counter += 1
        self.id = Card._counter  # Race condition!

# CORRECT - UUID
self.id = uuid.uuid4().hex[:8]
```

---

### **MISTAKE 2: Mutable Default Arguments** ❌

```python
# WRONG - All instances share the same list!
@dataclass
class Board:
    lists: List[TaskList] = []  # Shared across all boards!

# CORRECT - Use default_factory
@dataclass
class Board:
    lists: List[TaskList] = field(default_factory=list)
```

---

### **MISTAKE 3: Not Using Set for Membership** ❌

```python
# WRONG - O(N) membership check
class Board:
    members: List[User] = field(default_factory=list)
    
    def is_member(self, user):
        return user in self.members  # O(N)

# CORRECT - O(1) with Set
class Board:
    members: Set[User] = field(default_factory=set)
    
    def is_member(self, user):
        return user in self.members  # O(1)
```

---

## 💯 Interview Checklist

- [ ] ✅ **Clarified requirements** (asked about entities, permissions)
- [ ] ✅ **Drew entity relationships** (1:N, N:N)
- [ ] ✅ **Used Composition** (Board HAS Lists HAS Cards)
- [ ] ✅ **Used Facade** (TrelloService as entry point)
- [ ] ✅ **Used dataclasses** for clean entities
- [ ] ✅ **Used UUID** for unique identifiers
- [ ] ✅ **Used Set** for members (O(1) lookup)
- [ ] ✅ **Handled edge cases** (owner removal, invalid moves)
- [ ] ✅ **Implemented query methods** (by assignee, overdue)
- [ ] ✅ **Mentioned extensions** (history, permissions, checklist)

---

## 📚 Quick Reference Card

```
┌────────────────────────────────────────────────────────────┐
│                  TRELLO BOARD CHEAT SHEET                  │
├────────────────────────────────────────────────────────────┤
│ ENTITY HIERARCHY:                                         │
│   User → Board → List → Card                              │
│   (1:N)   (1:N)   (1:N)                                   │
│                                                            │
│ DESIGN PATTERNS:                                          │
│   - Composition: Board HAS Lists HAS Cards                │
│   - Facade: TrelloService as entry point                  │
│   - Factory: Validation during creation                   │
│                                                            │
│ DATA STRUCTURES:                                          │
│   - Dict[str, Board] → O(1) board lookup                 │
│   - Set[User] → O(1) membership check                    │
│   - Set[Label] → O(1) label operations                   │
│   - List → Maintains order for lists/cards               │
│                                                            │
│ KEY OPERATIONS:                                           │
│   - create_card: O(L) - find list                        │
│   - move_card: O(L + C) - find and move                  │
│   - is_member: O(1) - set lookup                         │
│                                                            │
│ EDGE CASES:                                               │
│   - Owner cannot be removed                               │
│   - Labels are case-insensitive                          │
│   - Use field(default_factory=list) for mutable defaults │
└────────────────────────────────────────────────────────────┘
```

---

**Related Problems:**
- Jira Board Design
- GitHub Projects
- Asana Task Management

