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

**Input:** User actions (createBoard, addList, addCard, moveCard, etc.)
**Output:** Working system with proper data structures and relationships

**Constraints:**
- 1 ≤ Number of boards ≤ 1000 per user
- 1 ≤ Number of lists per board ≤ 50
- 1 ≤ Number of cards per list ≤ 1000
- Card title length ≤ 500 characters

---

## 🎨 Visual Example

```text
Board: "Sprint 2024"
├── List: "To Do"
│   ├── Card: "Implement Rate Limiter" (assigned: Alice)
│   └── Card: "Write Tests" (assigned: Bob)
├── List: "In Progress"
│   └── Card: "Review PR #123" (assigned: Alice)
└── List: "Done"
    └── Card: "Deploy to Staging" (assigned: Charlie)

Operations:
1. moveCard(card1, "To Do" → "In Progress")
2. assignCard(card2, Bob)
3. deleteCard(card3)
4. archiveList("Done")
```

---

## 🏗️ Class Design

```text
┌────────────┐
│    User    │
├────────────┤
│ - id       │
│ - name     │
│ - email    │
└────────────┘
      │ 1
      │
      │ *
┌────────────┐
│   Board    │ ◆───────┐
├────────────┤         │
│ - id       │         │ contains
│ - name     │         │
│ - owner    │         │ *
│ - lists    │◀────────┤
└────────────┘    ┌────────────┐
                  │    List    │ ◆───────┐
                  ├────────────┤         │
                  │ - id       │         │ contains
                  │ - name     │         │
                  │ - position │         │ *
                  │ - cards    │◀────────┤
                  └────────────┘    ┌────────────┐
                                    │    Card    │
                                    ├────────────┤
                                    │ - id       │
                                    │ - title    │
                                    │ - desc     │
                                    │ - assignee │
                                    │ - dueDate  │
                                    │ - labels   │
                                    └────────────┘
```

---

## 💻 Implementation

### **Java Implementation**

```java
import java.time.LocalDate;
import java.util.*;
import java.util.concurrent.atomic.AtomicLong;

// ============ ID Generator ============
class IdGenerator {
    private static AtomicLong counter = new AtomicLong(0);

    public static String generate(String prefix) {
        return prefix + counter.incrementAndGet();
    }
}

// ============ User Class ============
class User {
    private String id;
    private String name;
    private String email;

    public User(String name, String email) {
        this.id = IdGenerator.generate("USER_");
        this.name = name;
        this.email = email;
    }

    // Getters
    public String getId() { return id; }
    public String getName() { return name; }
    public String getEmail() { return email; }
}

// ============ Label/Tag Class ============
enum Priority {
    LOW, MEDIUM, HIGH, CRITICAL
}

class Label {
    private String name;
    private String color; // Hex color

    public Label(String name, String color) {
        this.name = name;
        this.color = color;
    }

    public String getName() { return name; }
    public String getColor() { return color; }
}

// ============ Card Class ============
class Card {
    private String id;
    private String title;
    private String description;
    private User assignee;
    private LocalDate dueDate;
    private LocalDate createdDate;
    private Priority priority;
    private Set<Label> labels;
    private List<String> comments;

    public Card(String title, String description) {
        this.id = IdGenerator.generate("CARD_");
        this.title = title;
        this.description = description;
        this.createdDate = LocalDate.now();
        this.labels = new HashSet<>();
        this.comments = new ArrayList<>();
    }

    // Setters
    public void assign(User user) {
        this.assignee = user;
    }

    public void setDueDate(LocalDate dueDate) {
        this.dueDate = dueDate;
    }

    public void setPriority(Priority priority) {
        this.priority = priority;
    }

    public void addLabel(Label label) {
        labels.add(label);
    }

    public void addComment(String comment) {
        comments.add(comment);
    }

    // Getters
    public String getId() { return id; }
    public String getTitle() { return title; }
    public String getDescription() { return description; }
    public User getAssignee() { return assignee; }
    public LocalDate getDueDate() { return dueDate; }
    public Priority getPriority() { return priority; }

    @Override
    public String toString() {
        return String.format("Card[%s]: %s (Assignee: %s, Due: %s)",
                id, title,
                assignee != null ? assignee.getName() : "Unassigned",
                dueDate != null ? dueDate : "No due date");
    }
}

// ============ List Class ============
class TaskList {
    private String id;
    private String name;
    private int position; // For ordering lists
    private List<Card> cards;

    public TaskList(String name, int position) {
        this.id = IdGenerator.generate("LIST_");
        this.name = name;
        this.position = position;
        this.cards = new ArrayList<>();
    }

    public void addCard(Card card) {
        cards.add(card);
    }

    public void removeCard(Card card) {
        cards.remove(card);
    }

    public void moveCard(Card card, int newPosition) {
        if (cards.contains(card)) {
            cards.remove(card);
            cards.add(Math.min(newPosition, cards.size()), card);
        }
    }

    public List<Card> getCards() {
        return new ArrayList<>(cards);
    }

    public Card getCard(String cardId) {
        return cards.stream()
                .filter(c -> c.getId().equals(cardId))
                .findFirst()
                .orElse(null);
    }

    // Getters
    public String getId() { return id; }
    public String getName() { return name; }
    public int getPosition() { return position; }

    @Override
    public String toString() {
        return String.format("List[%s]: %s (%d cards)", id, name, cards.size());
    }
}

// ============ Board Class ============
class Board {
    private String id;
    private String name;
    private User owner;
    private List<TaskList> lists;
    private Set<User> members;

    public Board(String name, User owner) {
        this.id = IdGenerator.generate("BOARD_");
        this.name = name;
        this.owner = owner;
        this.lists = new ArrayList<>();
        this.members = new HashSet<>();
        this.members.add(owner);
    }

    // List operations
    public TaskList createList(String name) {
        TaskList list = new TaskList(name, lists.size());
        lists.add(list);
        return list;
    }

    public void deleteList(String listId) {
        lists.removeIf(list -> list.getId().equals(listId));
    }

    public TaskList getList(String listId) {
        return lists.stream()
                .filter(list -> list.getId().equals(listId))
                .findFirst()
                .orElse(null);
    }

    // Card operations
    public Card createCard(String listId, String title, String description) {
        TaskList list = getList(listId);
        if (list == null) {
            throw new IllegalArgumentException("List not found: " + listId);
        }

        Card card = new Card(title, description);
        list.addCard(card);
        return card;
    }

    public void moveCard(String cardId, String fromListId, String toListId) {
        TaskList fromList = getList(fromListId);
        TaskList toList = getList(toListId);

        if (fromList == null || toList == null) {
            throw new IllegalArgumentException("List not found");
        }

        Card card = fromList.getCard(cardId);
        if (card == null) {
            throw new IllegalArgumentException("Card not found: " + cardId);
        }

        fromList.removeCard(card);
        toList.addCard(card);
    }

    // Member operations
    public void addMember(User user) {
        members.add(user);
    }

    public void removeMember(User user) {
        if (!user.equals(owner)) {
            members.remove(user);
        }
    }

    // Getters
    public String getId() { return id; }
    public String getName() { return name; }
    public List<TaskList> getLists() { return new ArrayList<>(lists); }
    public Set<User> getMembers() { return new HashSet<>(members); }

    @Override
    public String toString() {
        return String.format("Board[%s]: %s (Owner: %s, %d lists)",
                id, name, owner.getName(), lists.size());
    }
}

// ============ Trello Service ============
class TrelloService {
    private Map<String, Board> boards;
    private Map<String, User> users;

    public TrelloService() {
        this.boards = new HashMap<>();
        this.users = new HashMap<>();
    }

    // User management
    public User createUser(String name, String email) {
        User user = new User(name, email);
        users.put(user.getId(), user);
        return user;
    }

    // Board management
    public Board createBoard(String name, User owner) {
        Board board = new Board(name, owner);
        boards.put(board.getId(), board);
        return board;
    }

    public Board getBoard(String boardId) {
        return boards.get(boardId);
    }

    public void deleteBoard(String boardId) {
        boards.remove(boardId);
    }

    // Get all boards for a user
    public List<Board> getBoardsForUser(User user) {
        List<Board> userBoards = new ArrayList<>();
        for (Board board : boards.values()) {
            if (board.getMembers().contains(user)) {
                userBoards.add(board);
            }
        }
        return userBoards;
    }
}

// ============ Main / Demo ============
public class Main {
    public static void main(String[] args) {
        TrelloService trello = new TrelloService();

        // Create users
        User alice = trello.createUser("Alice", "alice@example.com");
        User bob = trello.createUser("Bob", "bob@example.com");

        // Create board
        Board board = trello.createBoard("Sprint 2024", alice);
        board.addMember(bob);

        // Create lists
        TaskList todoList = board.createList("To Do");
        TaskList inProgressList = board.createList("In Progress");
        TaskList doneList = board.createList("Done");

        // Create cards
        Card card1 = board.createCard(todoList.getId(),
                "Implement Rate Limiter",
                "Use token bucket algorithm");
        card1.assign(alice);
        card1.setPriority(Priority.HIGH);

        Card card2 = board.createCard(todoList.getId(),
                "Write Tests",
                "Unit tests for all components");
        card2.assign(bob);
        card2.setDueDate(LocalDate.now().plusDays(7));

        // Move card
        System.out.println("=== Initial State ===");
        printBoard(board);

        board.moveCard(card1.getId(), todoList.getId(), inProgressList.getId());

        System.out.println("\n=== After Moving Card ===");
        printBoard(board);
    }

    private static void printBoard(Board board) {
        System.out.println(board);
        for (TaskList list : board.getLists()) {
            System.out.println("  " + list);
            for (Card card : list.getCards()) {
                System.out.println("    - " + card);
            }
        }
    }
}
```

---

### **Python Implementation**

```python
from dataclasses import dataclass, field
from typing import List, Set, Optional
from datetime import date, datetime
from enum import Enum
import uuid

# ============ Enums ============
class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

# ============ User Class ============
@dataclass
class User:
    name: str
    email: str
    id: str = field(default_factory=lambda: f"USER_{uuid.uuid4().hex[:8]}")

# ============ Label Class ============
@dataclass
class Label:
    name: str
    color: str

# ============ Card Class ============
@dataclass
class Card:
    title: str
    description: str
    id: str = field(default_factory=lambda: f"CARD_{uuid.uuid4().hex[:8]}")
    assignee: Optional[User] = None
    due_date: Optional[date] = None
    created_date: date = field(default_factory=date.today)
    priority: Optional[Priority] = None
    labels: Set[Label] = field(default_factory=set)
    comments: List[str] = field(default_factory=list)

    def assign(self, user: User):
        self.assignee = user

    def add_label(self, label: Label):
        self.labels.add(label)

    def add_comment(self, comment: str):
        self.comments.append(comment)

    def __str__(self):
        assignee_name = self.assignee.name if self.assignee else "Unassigned"
        due = self.due_date if self.due_date else "No due date"
        return f"Card[{self.id}]: {self.title} (Assignee: {assignee_name}, Due: {due})"

# ============ TaskList Class ============
@dataclass
class TaskList:
    name: str
    position: int
    id: str = field(default_factory=lambda: f"LIST_{uuid.uuid4().hex[:8]}")
    cards: List[Card] = field(default_factory=list)

    def add_card(self, card: Card):
        self.cards.append(card)

    def remove_card(self, card: Card):
        if card in self.cards:
            self.cards.remove(card)

    def get_card(self, card_id: str) -> Optional[Card]:
        for card in self.cards:
            if card.id == card_id:
                return card
        return None

    def __str__(self):
        return f"List[{self.id}]: {self.name} ({len(self.cards)} cards)"

# ============ Board Class ============
@dataclass
class Board:
    name: str
    owner: User
    id: str = field(default_factory=lambda: f"BOARD_{uuid.uuid4().hex[:8]}")
    lists: List[TaskList] = field(default_factory=list)
    members: Set[User] = field(default_factory=set)

    def __post_init__(self):
        self.members.add(self.owner)

    def create_list(self, name: str) -> TaskList:
        task_list = TaskList(name, len(self.lists))
        self.lists.append(task_list)
        return task_list

    def get_list(self, list_id: str) -> Optional[TaskList]:
        for lst in self.lists:
            if lst.id == list_id:
                return lst
        return None

    def create_card(self, list_id: str, title: str, description: str) -> Card:
        task_list = self.get_list(list_id)
        if not task_list:
            raise ValueError(f"List not found: {list_id}")

        card = Card(title, description)
        task_list.add_card(card)
        return card

    def move_card(self, card_id: str, from_list_id: str, to_list_id: str):
        from_list = self.get_list(from_list_id)
        to_list = self.get_list(to_list_id)

        if not from_list or not to_list:
            raise ValueError("List not found")

        card = from_list.get_card(card_id)
        if not card:
            raise ValueError(f"Card not found: {card_id}")

        from_list.remove_card(card)
        to_list.add_card(card)

    def add_member(self, user: User):
        self.members.add(user)

    def __str__(self):
        return f"Board[{self.id}]: {self.name} (Owner: {self.owner.name}, {len(self.lists)} lists)"

# ============ Trello Service ============
class TrelloService:
    def __init__(self):
        self.boards = {}
        self.users = {}

    def create_user(self, name: str, email: str) -> User:
        user = User(name, email)
        self.users[user.id] = user
        return user

    def create_board(self, name: str, owner: User) -> Board:
        board = Board(name, owner)
        self.boards[board.id] = board
        return board

    def get_board(self, board_id: str) -> Optional[Board]:
        return self.boards.get(board_id)

    def get_boards_for_user(self, user: User) -> List[Board]:
        return [board for board in self.boards.values()
                if user in board.members]

# ============ Demo ============
if __name__ == "__main__":
    trello = TrelloService()

    # Create users
    alice = trello.create_user("Alice", "alice@example.com")
    bob = trello.create_user("Bob", "bob@example.com")

    # Create board
    board = trello.create_board("Sprint 2024", alice)
    board.add_member(bob)

    # Create lists
    todo_list = board.create_list("To Do")
    in_progress_list = board.create_list("In Progress")
    done_list = board.create_list("Done")

    # Create cards
    card1 = board.create_card(todo_list.id, "Implement Rate Limiter",
                              "Use token bucket algorithm")
    card1.assign(alice)
    card1.priority = Priority.HIGH

    card2 = board.create_card(todo_list.id, "Write Tests",
                              "Unit tests for all components")
    card2.assign(bob)

    # Print initial state
    print("=== Initial State ===")
    print(board)
    for lst in board.lists:
        print(f"  {lst}")
        for card in lst.cards:
            print(f"    - {card}")

    # Move card
    board.move_card(card1.id, todo_list.id, in_progress_list.id)

    print("\n=== After Moving Card ===")
    print(board)
    for lst in board.lists:
        print(f"  {lst}")
        for card in lst.cards:
            print(f"    - {card}")
```

---

## 🚀 Extensions & Follow-ups

### **1. Card History/Activity Log**
```java
class Activity {
    User user;
    String action; // "created", "moved", "assigned", "commented"
    LocalDateTime timestamp;
    String details;
}

class Card {
    List<Activity> history = new ArrayList<>();

    public void addActivity(User user, String action, String details) {
        history.add(new Activity(user, action, LocalDateTime.now(), details));
    }
}
```

### **2. Checklist within Cards**
```java
class ChecklistItem {
    String text;
    boolean completed;
}

class Card {
    List<ChecklistItem> checklist = new ArrayList<>();

    public void addChecklistItem(String text) {
        checklist.add(new ChecklistItem(text, false));
    }

    public int getCompletionPercentage() {
        long completed = checklist.stream().filter(i -> i.completed).count();
        return (int) (completed * 100 / checklist.size());
    }
}
```

### **3. Card Filtering & Search**
```java
class Board {
    public List<Card> filterCards(Predicate<Card> filter) {
        return lists.stream()
                .flatMap(list -> list.getCards().stream())
                .filter(filter)
                .collect(Collectors.toList());
    }

    // Usage examples
    List<Card> aliceCards = board.filterCards(c -> c.getAssignee() == alice);
    List<Card> overdueCards = board.filterCards(c ->
            c.getDueDate() != null && c.getDueDate().isBefore(LocalDate.now()));
    List<Card> highPriorityCards = board.filterCards(c ->
            c.getPriority() == Priority.HIGH || c.getPriority() == Priority.CRITICAL);
}
```

### **4. Permissions/Access Control**
```java
enum Permission {
    VIEW, EDIT, ADMIN
}

class Board {
    Map<User, Permission> permissions = new HashMap<>();

    public void setPermission(User user, Permission permission) {
        permissions.put(user, permission);
    }

    public boolean canEdit(User user) {
        Permission perm = permissions.getOrDefault(user, Permission.VIEW);
        return perm == Permission.EDIT || perm == Permission.ADMIN;
    }
}
```

---

## 🧪 Testing Strategy

```java
@Test
public void testCreateBoard() {
    User alice = new User("Alice", "alice@example.com");
    Board board = new Board("Test Board", alice);

    assertEquals("Test Board", board.getName());
    assertEquals(alice, board.getOwner());
    assertTrue(board.getMembers().contains(alice));
}

@Test
public void testMoveCard() {
    Board board = new Board("Board", owner);
    TaskList list1 = board.createList("List 1");
    TaskList list2 = board.createList("List 2");

    Card card = board.createCard(list1.getId(), "Card", "Desc");

    assertEquals(1, list1.getCards().size());
    assertEquals(0, list2.getCards().size());

    board.moveCard(card.getId(), list1.getId(), list2.getId());

    assertEquals(0, list1.getCards().size());
    assertEquals(1, list2.getCards().size());
}

@Test(expected = IllegalArgumentException.class)
public void testMoveCardToInvalidList() {
    Board board = new Board("Board", owner);
    TaskList list = board.createList("List");
    Card card = board.createCard(list.getId(), "Card", "Desc");

    board.moveCard(card.getId(), list.getId(), "INVALID_LIST");
}
```

---

## 📊 Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| createBoard | O(1) | O(1) |
| createList | O(1) | O(1) |
| createCard | O(1) | O(1) |
| moveCard | O(N) | O(1) |
| filterCards | O(N×M) | O(K) |

**Where:** N = lists, M = cards per list, K = matching cards

---

## 💯 Summary

✅ Clear class hierarchy (Board → List → Card)
✅ Proper encapsulation (private fields, public methods)
✅ ID generation for uniqueness
✅ Support for members, labels, priorities
✅ Easy to extend (activities, checklists, permissions)
✅ Thread-safety considerations (use ConcurrentHashMap in production)
✅ Clean separation of concerns

**Interview Pro Tip:** Start simple, then ask "Should I add labels/checklists/history?" to show extensibility thinking!

---

**Related Problems:**
- Jira board design
- GitHub Projects
- Monday.com
