# 🏷️ PROBLEM 9: TAGGING MANAGEMENT SYSTEM

### ⭐⭐⭐⭐ **Design Atlassian's Tagging System (Jira/Confluence)**

**Frequency:** MEDIUM-HIGH - **Atlassian-specific problem!**
**Difficulty:** Medium
**Time to Solve:** 35-45 minutes
**Focus:** Many-to-Many Relationships, Bidirectional Lookup, Inverted Index

---

## 📋 Problem Statement

Design a tagging system used across Atlassian products (Jira, Confluence, Trello) where:
- Entities (issues, pages, cards) can have multiple tags
- Tags can be associated with multiple entities
- Support fast lookups in both directions
- Track tag popularity

**Core Requirements:**
- `add_tag(entity_id, tag)`: Add tag to entity - O(1)
- `remove_tag(entity_id, tag)`: Remove tag from entity - O(1)
- `get_tags(entity_id)`: Get all tags for entity - O(T)
- `get_entities(tag)`: Get all entities with tag - O(E)
- `search_by_tag(partial)`: Search entities by partial tag name
- `get_popular_tags(limit)`: Get most used tags

**Constraints:**
- Tags are case-insensitive
- Entities can have up to 100 tags
- System may have millions of entities
- Need efficient lookups in both directions

---

## 🎯 INTERVIEW FLOW: Step-by-Step Guide

### **PHASE 1: Clarify Requirements (2-3 minutes)**

**SAY THIS:**
> "Before I start designing, let me clarify a few requirements:"

**Questions to Ask:**
1. "Case-sensitive or insensitive tags?"
2. "Can tags have metadata (color, description)?"
3. "Maximum tags per entity?"
4. "Need to track tag creation/usage time?"
5. "Scale - how many entities and tags?"
6. "Do we need tag suggestions/autocomplete?"

**WRITE DOWN the answers. This shows you're thorough.**

---

### **PHASE 2: Identify Key Design Insight (2-3 minutes)**

**SAY THIS:**
> "The key insight here is that we need BIDIRECTIONAL MAPPING - this is essentially an Inverted Index pattern, the same technique search engines use!"

#### **The Inverted Index Pattern**

```text
┌─────────────────────────────────────────────────────────────────┐
│                    INVERTED INDEX CONCEPT                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  FORWARD INDEX (Entity → Tags):                                 │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  JIRA-101 → ["bug", "high-priority"]                       │ │
│  │  JIRA-102 → ["feature", "frontend"]                        │ │
│  │  JIRA-103 → ["bug", "backend"]                             │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  INVERTED INDEX (Tag → Entities):                               │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  "bug"           → {JIRA-101, JIRA-103}                    │ │
│  │  "high-priority" → {JIRA-101}                              │ │
│  │  "feature"       → {JIRA-102}                              │ │
│  │  "frontend"      → {JIRA-102}                              │ │
│  │  "backend"       → {JIRA-103}                              │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  WHY INVERTED INDEX?                                            │
│  - "Get all tags for JIRA-101" → Forward index O(1)            │
│  - "Get all entities with bug" → Inverted index O(1)           │
│  - Without inverted: must scan ALL entities O(N)!              │
└─────────────────────────────────────────────────────────────────┘
```

**Real-World Usage:**
> "Google uses inverted indexes: word → [doc1, doc2, doc3]
> Elasticsearch does the same for full-text search.
> Our tagging system is a simplified version of this concept."

---

### **PHASE 3: High-Level Design (3-4 minutes)**

**SAY THIS:**
> "Let me draw the class structure with bidirectional mapping."

```text
┌─────────────────────────────────────────────────────────────────┐
│                      TaggingSystem                              │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  Main facade - manages bidirectional mappings              │ │
│  │                                                             │ │
│  │  FORWARD INDEX:                                            │ │
│  │  entity_to_tags: Dict[str, Set[Tag]]                       │ │
│  │    "JIRA-101" → {Tag("bug"), Tag("high-priority")}        │ │
│  │                                                             │ │
│  │  INVERTED INDEX:                                           │ │
│  │  tag_to_entities: Dict[Tag, Set[str]]                      │ │
│  │    Tag("bug") → {"JIRA-101", "JIRA-103"}                  │ │
│  │                                                             │ │
│  │  USAGE TRACKING:                                           │ │
│  │  tag_usage: Dict[str, int]                                 │ │
│  │    "bug" → 2, "feature" → 1                               │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                  │
│  + add_tag(entity_id, tag_name) → bool                         │
│  + remove_tag(entity_id, tag_name) → bool                      │
│  + get_tags(entity_id) → Set[str]                              │
│  + get_entities(tag_name) → Set[str]                           │
│  + get_popular_tags(limit) → List[(name, count)]               │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────┐     ┌─────────────────────┐
│        Tag          │     │       Entity        │
├─────────────────────┤     ├─────────────────────┤
│ - name: str         │     │ - id: str           │
│ - color: str        │     │ - entity_type: str  │
│ - description: str  │     │ - title: str        │
│ - created_at: date  │     └─────────────────────┘
├─────────────────────┤
│ + __hash__()        │  ← Case-insensitive hash
│ + __eq__()          │  ← Case-insensitive equality
└─────────────────────┘
```

**Key Synchronization Point:**
> "CRITICAL: Both mappings must be updated atomically!
> If we add a tag to entity_to_tags but forget tag_to_entities,
> lookups will return inconsistent results."

---

### **PHASE 4: Design Patterns & WHY We Use Them (3-4 minutes)**

**SAY THIS:**
> "Let me explain the design patterns I'm using and WHY each is appropriate."

#### **Pattern 1: Inverted Index Pattern** ⭐⭐⭐⭐⭐

```python
# The core insight - bidirectional mapping
entity_to_tags: Dict[str, Set[Tag]] = {}      # Forward index
tag_to_entities: Dict[Tag, Set[str]] = {}     # Inverted index
```

**WHY Inverted Index?**

| Without Inverted Index | With Inverted Index |
|------------------------|---------------------|
| `get_entities("bug")` = O(N) | `get_entities("bug")` = O(1) |
| Scan ALL entities, check each for tag | Direct dictionary lookup |
| 1M entities × 10 tags = 10M checks | 1 lookup + iterate results |

> "Inverted Index trades SPACE for TIME.
> We store data twice (forward + inverted) but get O(1) lookups in both directions.
> This is the fundamental trade-off in search systems."

---

#### **Pattern 2: Facade Pattern** ⭐⭐⭐

```python
class TaggingSystem:
    """Facade - hides complexity of bidirectional sync."""
    
    def add_tag(self, entity_id: str, tag_name: str) -> bool:
        # Client doesn't need to know about:
        # - Normalizing tag names
        # - Updating forward index
        # - Updating inverted index
        # - Updating usage counts
        # - Handling duplicates
        pass
```

**WHY Facade?**
> "The client just calls `add_tag()`. They don't care about:
> - Maintaining two separate data structures in sync
> - Case normalization
> - Usage tracking
> 
> Facade hides this complexity behind a simple interface."

---

#### **Pattern 3: Flyweight Pattern (for Tags)** ⭐⭐

```python
# Store each unique tag ONCE, reference it multiple times
_tags: Dict[str, Tag] = {}  # Tag name → Tag object (single instance)

def _get_or_create_tag(self, name: str) -> Tag:
    """Flyweight - reuse existing Tag objects."""
    normalized = name.lower().strip()
    if normalized not in self._tags:
        self._tags[normalized] = Tag(name=normalized)
    return self._tags[normalized]
```

**WHY Flyweight?**
> "If 1000 entities have tag 'bug', we don't create 1000 Tag objects.
> We create ONE Tag('bug') and reference it 1000 times.
> This saves memory and ensures consistency (same color/description everywhere)."

---

### **PHASE 5: Data Structures & Why (2 minutes)**

| Data Structure | Used For | Why This Choice |
|----------------|----------|-----------------|
| `Dict[str, Set[Tag]]` | Forward index | O(1) lookup, Set prevents duplicates |
| `Dict[Tag, Set[str]]` | Inverted index | O(1) lookup, Set for unique entities |
| `defaultdict(set)` | Auto-initialize | No null checks needed |
| `defaultdict(int)` | Usage counts | Auto-initializes to 0 |
| `heapq.nlargest` | Top K popular | O(N log K) instead of O(N log N) |

**Why Set instead of List?**
> "Sets give us:
> - O(1) add/remove/contains
> - Automatic duplicate prevention
> - Set operations (intersection, union) for advanced queries"

---

### **PHASE 6: Write the Code (15-20 minutes)**

```python
"""
Tagging Management System - Atlassian Style
============================================
Bidirectional mapping with inverted index for efficient lookups.

Design Patterns:
- Inverted Index: O(1) lookups in both directions
- Facade: Hide synchronization complexity
- Flyweight: Reuse Tag objects

Real-World Usage:
- Jira issue labels
- Confluence page tags
- Trello card labels
- GitHub issue tags

Time Complexity:
- add_tag: O(1)
- remove_tag: O(1)
- get_tags: O(T) where T = tags per entity
- get_entities: O(E) where E = entities per tag
- get_popular_tags: O(N log K)
"""

from collections import defaultdict
from typing import Set, List, Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime
import heapq


@dataclass
class Tag:
    """
    Tag entity with case-insensitive matching.
    
    Design Decision: Tags are normalized to lowercase.
    This ensures "Bug", "BUG", "bug" are treated as the same tag.
    
    __hash__ and __eq__ are overridden for case-insensitive
    Set/Dict operations.
    """
    name: str
    color: str = "#808080"  # Default gray
    description: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Normalize tag name on creation."""
        self.name = self.name.lower().strip()

    def __eq__(self, other):
        """Case-insensitive equality."""
        if isinstance(other, Tag):
            return self.name == other.name
        return self.name == str(other).lower()

    def __hash__(self):
        """Case-insensitive hash for use in Sets/Dicts."""
        return hash(self.name)

    def __repr__(self):
        return f"Tag({self.name})"


@dataclass
class Entity:
    """
    Entity that can be tagged.
    Examples: Jira Issue, Confluence Page, Trello Card
    """
    id: str
    entity_type: str  # "ISSUE", "PAGE", "CARD"
    title: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        if isinstance(other, Entity):
            return self.id == other.id
        return self.id == str(other)


class TaggingSystem:
    """
    Tagging system with bidirectional O(1) lookups.
    
    Architecture:
    ┌────────────────────────────────────────────────────┐
    │                    TaggingSystem                   │
    │                                                    │
    │  ┌──────────────────┐    ┌──────────────────┐    │
    │  │  Forward Index   │    │  Inverted Index  │    │
    │  │                  │    │                  │    │
    │  │ entity → {tags}  │    │  tag → {entities}│    │
    │  │                  │    │                  │    │
    │  │ JIRA-1 → {bug}   │←──→│ bug → {JIRA-1}   │    │
    │  └──────────────────┘    └──────────────────┘    │
    │                                                    │
    │         ↕ MUST STAY IN SYNC ↕                     │
    └────────────────────────────────────────────────────┘
    
    Key Invariant:
    - If tag T is in entity_to_tags[E], then E is in tag_to_entities[T]
    - If E is in tag_to_entities[T], then T is in entity_to_tags[E]
    
    Thread Safety:
    - Not thread-safe as-is
    - For production: use threading.Lock or concurrent collections
    """
    
    def __init__(self):
        # FORWARD INDEX: Entity ID → Set of Tags
        self._entity_to_tags: Dict[str, Set[Tag]] = defaultdict(set)
        
        # INVERTED INDEX: Tag → Set of Entity IDs
        self._tag_to_entities: Dict[Tag, Set[str]] = defaultdict(set)
        
        # Tag metadata storage (Flyweight - one Tag object per unique tag)
        self._tags: Dict[str, Tag] = {}
        
        # Usage count for popularity (avoid O(N) count on every query)
        self._tag_usage: Dict[str, int] = defaultdict(int)
        
        # Entity storage
        self._entities: Dict[str, Entity] = {}
    
    # ============ Entity Management ============
    
    def register_entity(self, entity: Entity) -> None:
        """Register an entity in the system."""
        self._entities[entity.id] = entity
    
    def get_entity(self, entity_id: str) -> Optional[Entity]:
        """Get entity by ID."""
        return self._entities.get(entity_id)
    
    # ============ Tag Operations ============
    
    def add_tag(self, entity_id: str, tag_name: str, 
                color: str = None, description: str = None) -> bool:
        """
        Add a tag to an entity.
        
        Time: O(1)
        
        Steps:
        1. Validate entity exists
        2. Get or create Tag object (Flyweight)
        3. Update forward index (entity → tags)
        4. Update inverted index (tag → entities)
        5. Update usage count
        
        Returns: True if tag was added, False if already exists
        """
        if entity_id not in self._entities:
            raise ValueError(f"Entity not found: {entity_id}")

        # Get or create tag (Flyweight pattern)
        tag = self._get_or_create_tag(tag_name, color, description)
        
        # Check if already tagged (O(1) set lookup)
        if tag in self._entity_to_tags[entity_id]:
            return False  # Already tagged
        
        # ★ CRITICAL: Update BOTH indexes atomically ★
        self._entity_to_tags[entity_id].add(tag)      # Forward index
        self._tag_to_entities[tag].add(entity_id)     # Inverted index
        
        # Update usage count
        self._tag_usage[tag.name] += 1
        
        return True
    
    def _get_or_create_tag(self, name: str, color: str = None, 
                          description: str = None) -> Tag:
        """
        Flyweight Pattern: Get existing tag or create new one.
        
        Ensures only ONE Tag object exists per unique tag name.
        """
        normalized = name.lower().strip()
        
        if normalized in self._tags:
            return self._tags[normalized]
        
        tag = Tag(
            name=normalized,
            color=color or "#808080",
            description=description or ""
        )
        self._tags[normalized] = tag
        return tag

    def remove_tag(self, entity_id: str, tag_name: str) -> bool:
        """
        Remove a tag from an entity.
        
        Time: O(1)
        
        Returns: True if removed, False if not found
        """
        normalized = tag_name.lower().strip()
        tag = self._tags.get(normalized)
        
        if not tag:
            return False
        
        if entity_id not in self._entity_to_tags:
            return False

        if tag not in self._entity_to_tags[entity_id]:
            return False

        # ★ CRITICAL: Update BOTH indexes atomically ★
        self._entity_to_tags[entity_id].discard(tag)  # Forward index
        self._tag_to_entities[tag].discard(entity_id)  # Inverted index
        
        # Update usage count
        self._tag_usage[tag.name] -= 1
        
        # ★ Cleanup empty mappings to prevent memory leaks ★
        if not self._entity_to_tags[entity_id]:
            del self._entity_to_tags[entity_id]
        
        if not self._tag_to_entities[tag]:
            del self._tag_to_entities[tag]
            del self._tags[tag.name]
            del self._tag_usage[tag.name]

        return True

    # ============ Query Operations ============
    
    def get_tags(self, entity_id: str) -> Set[str]:
        """
        Get all tags for an entity (forward index lookup).
        
        Time: O(1) lookup + O(T) to build result set
        """
        tags = self._entity_to_tags.get(entity_id, set())
        return {tag.name for tag in tags}

    def get_tag_objects(self, entity_id: str) -> Set[Tag]:
        """Get full Tag objects with metadata."""
        return set(self._entity_to_tags.get(entity_id, set()))
    
    def get_entities(self, tag_name: str) -> Set[str]:
        """
        Get all entity IDs with a tag (inverted index lookup).
        
        Time: O(1) lookup + O(E) to copy result
        
        This is the KEY operation that inverted index optimizes!
        Without inverted index: O(N) to scan all entities
        With inverted index: O(1) lookup
        """
        normalized = tag_name.lower().strip()
        tag = self._tags.get(normalized)
        
        if not tag:
            return set()
        
        return set(self._tag_to_entities.get(tag, set()))
    
    def search_by_tag(self, partial_name: str) -> Set[str]:
        """
        Search entities by partial tag name (prefix/contains).
        
        Time: O(T) where T = total unique tags
        
        Note: For production with millions of tags, use a Trie
        for O(P + K) prefix search where P = prefix length, K = results.
        """
        search_term = partial_name.lower().strip()
        result = set()

        for tag, entity_ids in self._tag_to_entities.items():
            if search_term in tag.name:
                result.update(entity_ids)

        return result

    def get_popular_tags(self, limit: int) -> List[tuple]:
        """
        Get top N most popular tags.
        
        Time: O(T log K) using heap where T = total tags, K = limit
        
        Why heapq.nlargest instead of sorting?
        - Full sort: O(T log T)
        - Heap nlargest: O(T log K)
        - For K=10 and T=1M, that's 10x faster!
        """
        if not self._tag_usage:
            return []
        
        return heapq.nlargest(
            limit,
            self._tag_usage.items(),
            key=lambda x: x[1]
        )
    
    # ============ Advanced Queries ============

    def get_entities_with_all_tags(self, tag_names: List[str]) -> Set[str]:
        """
        Get entities having ALL specified tags (intersection).
        
        Time: O(K × E) where K = tags, E = min entities per tag
        
        Optimization: Start with smallest set for faster intersection.
        """
        if not tag_names:
            return set()

        # Get entity sets for each tag
        sets = [self.get_entities(name) for name in tag_names]
        
        # Remove empty sets (tag doesn't exist)
        sets = [s for s in sets if s]
        
        if not sets:
            return set()
        
        # Optimization: Start with smallest set
        sets.sort(key=len)
        
        result = sets[0]
        for s in sets[1:]:
            result &= s
            if not result:  # Early exit
                return set()

        return result

    def get_entities_with_any_tag(self, tag_names: List[str]) -> Set[str]:
        """
        Get entities having ANY of specified tags (union).
        
        Time: O(K × E) where K = tags, E = entities per tag
        """
        result = set()

        for tag_name in tag_names:
            result |= self.get_entities(tag_name)

        return result

    def get_related_tags(self, tag_name: str, limit: int = 5) -> List[str]:
        """
        Get tags that frequently co-occur with the given tag.
        
        Useful for tag suggestions!
        
        Time: O(E × T) where E = entities with tag, T = avg tags per entity
        """
        entities = self.get_entities(tag_name)
        tag_counts = defaultdict(int)
        
        for entity_id in entities:
            for tag in self._entity_to_tags.get(entity_id, set()):
                if tag.name != tag_name.lower():
                    tag_counts[tag.name] += 1
        
        return [
            tag for tag, _ in 
            heapq.nlargest(limit, tag_counts.items(), key=lambda x: x[1])
        ]
    
    # ============ Statistics ============
    
    def get_statistics(self) -> Dict:
        """Get system statistics."""
        total_taggings = sum(self._tag_usage.values())
        
        return {
            "total_entities": len(self._entities),
            "total_unique_tags": len(self._tags),
            "total_taggings": total_taggings,
            "avg_tags_per_entity": (
                total_taggings / len(self._entities) 
                if self._entities else 0
            ),
        }


# ============ Demo ============
def main():
    """Demonstrate tagging system functionality."""
    print("=" * 60)
    print("TAGGING MANAGEMENT SYSTEM DEMO")
    print("=" * 60)
    
    system = TaggingSystem()

    # Register entities
    entities = [
        Entity("JIRA-101", "ISSUE", "Login bug"),
        Entity("JIRA-102", "ISSUE", "New dashboard"),
        Entity("JIRA-103", "ISSUE", "API performance"),
        Entity("PAGE-201", "PAGE", "API Documentation"),
        Entity("PAGE-202", "PAGE", "User Guide"),
    ]
    
    for entity in entities:
        system.register_entity(entity)
    print(f"\n✓ Registered {len(entities)} entities")

    # Add tags
    system.add_tag("JIRA-101", "bug", color="#FF0000")
    system.add_tag("JIRA-101", "high-priority", color="#FF6600")
    system.add_tag("JIRA-102", "feature", color="#00FF00")
    system.add_tag("JIRA-102", "frontend")
    system.add_tag("JIRA-103", "bug", color="#FF0000")
    system.add_tag("JIRA-103", "backend")
    system.add_tag("PAGE-201", "documentation", color="#0066FF")
    system.add_tag("PAGE-201", "api")
    system.add_tag("PAGE-202", "documentation", color="#0066FF")
    print("✓ Added tags to entities")

    # Forward index lookup
    print("\n" + "=" * 60)
    print("FORWARD INDEX: Entity → Tags")
    print("=" * 60)
    print(f"Tags for JIRA-101: {system.get_tags('JIRA-101')}")
    print(f"Tags for JIRA-103: {system.get_tags('JIRA-103')}")

    # Inverted index lookup
    print("\n" + "=" * 60)
    print("INVERTED INDEX: Tag → Entities")
    print("=" * 60)
    print(f"Entities with 'bug': {system.get_entities('bug')}")
    print(f"Entities with 'documentation': {system.get_entities('documentation')}")

    # Advanced queries
    print("\n" + "=" * 60)
    print("ADVANCED QUERIES")
    print("=" * 60)
    print(f"Search 'doc': {system.search_by_tag('doc')}")
    print(f"Top 3 tags: {system.get_popular_tags(3)}")
    print(f"Entities with ALL [bug, backend]: {system.get_entities_with_all_tags(['bug', 'backend'])}")
    print(f"Entities with ANY [feature, documentation]: {system.get_entities_with_any_tag(['feature', 'documentation'])}")
    print(f"Tags related to 'bug': {system.get_related_tags('bug')}")

    # Statistics
    print("\n" + "=" * 60)
    print("STATISTICS")
    print("=" * 60)
    print(system.get_statistics())


if __name__ == "__main__":
    main()
```

---

### **PHASE 7: Walk Through Edge Cases (3-4 minutes)**

| Edge Case | How Handled | Code Location |
|-----------|-------------|---------------|
| **Case-insensitive tags** | Normalize to lowercase | `Tag.__post_init__()` |
| **Add same tag twice** | Return False, no duplicate | `add_tag()` set check |
| **Remove non-existent tag** | Return False | `remove_tag()` checks |
| **Tag on non-existent entity** | Raise ValueError | `add_tag()` validation |
| **Empty tag name** | Stripped, empty string fails | `strip()` in normalize |
| **Memory leak from empty mappings** | Delete empty entries | `remove_tag()` cleanup |
| **Tag metadata consistency** | Flyweight pattern | `_get_or_create_tag()` |

**Memory Cleanup Explanation:**
> "When the last entity removes a tag, we must clean up:
> 1. Empty set in entity_to_tags
> 2. Empty set in tag_to_entities
> 3. Tag object from _tags
> 4. Usage count from _tag_usage
> 
> Without this, we'd have a memory leak!"

---

### **PHASE 8: Testing Strategy (2-3 minutes)**

```python
import pytest

class TestTaggingSystem:
    
    def test_add_tag_basic(self):
        """Tag is added to entity."""
        system = TaggingSystem()
        entity = Entity("E1", "ISSUE", "Test")
        system.register_entity(entity)
        
        result = system.add_tag("E1", "bug")
        
        assert result == True
        assert "bug" in system.get_tags("E1")
        assert "E1" in system.get_entities("bug")
    
    def test_add_tag_case_insensitive(self):
        """Tags are case-insensitive."""
        system = TaggingSystem()
        system.register_entity(Entity("E1", "ISSUE"))
        
        system.add_tag("E1", "Bug")
        result = system.add_tag("E1", "BUG")  # Same tag
        
        assert result == False  # Already exists
        assert len(system.get_tags("E1")) == 1
    
    def test_add_tag_duplicate_returns_false(self):
        """Adding same tag twice returns False."""
        system = TaggingSystem()
        system.register_entity(Entity("E1", "ISSUE"))
        
        assert system.add_tag("E1", "bug") == True
        assert system.add_tag("E1", "bug") == False
    
    def test_bidirectional_consistency(self):
        """Forward and inverted indexes stay in sync."""
        system = TaggingSystem()
        system.register_entity(Entity("E1", "ISSUE"))
        system.register_entity(Entity("E2", "ISSUE"))
        
        system.add_tag("E1", "bug")
        system.add_tag("E2", "bug")
        
        # Check both directions
        assert system.get_entities("bug") == {"E1", "E2"}
        assert "bug" in system.get_tags("E1")
        assert "bug" in system.get_tags("E2")
        
        # Remove from one entity
        system.remove_tag("E1", "bug")
        
        assert system.get_entities("bug") == {"E2"}
        assert "bug" not in system.get_tags("E1")
    
    def test_remove_tag_cleanup(self):
        """Removing last usage cleans up tag."""
        system = TaggingSystem()
        system.register_entity(Entity("E1", "ISSUE"))
        
        system.add_tag("E1", "temp")
        system.remove_tag("E1", "temp")
        
        # Tag should be completely removed
        assert system.get_entities("temp") == set()
        assert system._tag_usage.get("temp") is None
    
    def test_get_entities_with_all_tags(self):
        """Intersection query works."""
        system = TaggingSystem()
        system.register_entity(Entity("E1", "ISSUE"))
        system.register_entity(Entity("E2", "ISSUE"))
        
        system.add_tag("E1", "bug")
        system.add_tag("E1", "critical")
        system.add_tag("E2", "bug")
        
        result = system.get_entities_with_all_tags(["bug", "critical"])
        
        assert result == {"E1"}  # Only E1 has both
    
    def test_popular_tags(self):
        """Popular tags returns correct order."""
        system = TaggingSystem()
        for i in range(3):
            system.register_entity(Entity(f"E{i}", "ISSUE"))
        
        system.add_tag("E0", "common")
        system.add_tag("E1", "common")
        system.add_tag("E2", "common")
        system.add_tag("E0", "rare")
        
        popular = system.get_popular_tags(2)
        
        assert popular[0] == ("common", 3)
        assert popular[1] == ("rare", 1)
```

---

### **PHASE 9: Complexity Analysis (1 minute)**

| Operation | Time | Space |
|-----------|------|-------|
| `add_tag` | **O(1)** | O(1) |
| `remove_tag` | **O(1)** | O(1) |
| `get_tags` | O(T) | O(T) |
| `get_entities` | O(E) | O(E) |
| `search_by_tag` | O(N) | O(E) |
| `get_popular_tags` | O(N log K) | O(K) |
| `get_entities_with_all_tags` | O(K × E) | O(E) |
| `get_related_tags` | O(E × T) | O(N) |

**Where:** T = tags per entity, E = entities per tag, N = total tags, K = limit

---

### **PHASE 10: Extensions & Follow-ups (5+ minutes)**

#### **Q1: "How would you add tag hierarchies?"**

```python
class HierarchicalTaggingSystem(TaggingSystem):
    """
    Hierarchical tags: programming/java, programming/python
    
    Querying "programming" returns all entities with programming/*
    """
    
    def __init__(self):
        super().__init__()
        self._parent_map: Dict[str, str] = {}  # child → parent
    
    def add_tag_hierarchy(self, child: str, parent: str) -> None:
        """Set parent-child relationship."""
        self._parent_map[child.lower()] = parent.lower()
    
    def get_entities_with_hierarchy(self, tag_name: str) -> Set[str]:
        """Get entities with tag or any descendant tags."""
        result = self.get_entities(tag_name)
        
        # Find all children recursively
        normalized = tag_name.lower()
        for child, parent in self._parent_map.items():
            if parent == normalized:
                result |= self.get_entities_with_hierarchy(child)
        
        return result
```

---

#### **Q2: "How would you add autocomplete?"**

```python
class TagAutoComplete:
    """
    Trie-based autocomplete for tag suggestions.
    
    Time: O(P + K) where P = prefix length, K = results
    Much faster than O(N) scan for large tag sets!
    """
    
    def __init__(self):
        self._trie = {}
        self._END = "$"
    
    def add_tag(self, tag_name: str) -> None:
        node = self._trie
        for char in tag_name.lower():
            node = node.setdefault(char, {})
        node[self._END] = tag_name
    
    def suggest(self, prefix: str, limit: int = 10) -> List[str]:
        """Get tag suggestions for prefix."""
        node = self._trie
        
        # Navigate to prefix node
        for char in prefix.lower():
            if char not in node:
                return []
            node = node[char]
        
        # Collect all tags under this node
        results = []
        self._collect(node, results, limit)
        return results[:limit]
    
    def _collect(self, node: dict, results: List[str], limit: int):
        if len(results) >= limit:
            return
        if self._END in node:
            results.append(node[self._END])
        for char, child in node.items():
            if char != self._END:
                self._collect(child, results, limit)
```

---

#### **Q3: "How would you make this distributed?"**

```python
class RedisTaggingSystem:
    """
    Distributed tagging using Redis Sets.
    
    Redis provides:
    - SADD: O(1) add to set
    - SMEMBERS: O(N) get all members
    - SINTER: O(N*M) intersection (for ALL tags query)
    - ZINCRBY: O(log N) for sorted set (popularity)
    """
    
    def __init__(self, redis_client):
        self.redis = redis_client
    
    def add_tag(self, entity_id: str, tag: str) -> bool:
        tag = tag.lower()
        pipe = self.redis.pipeline()
        # Forward index
        pipe.sadd(f"entity:{entity_id}:tags", tag)
        # Inverted index
        pipe.sadd(f"tag:{tag}:entities", entity_id)
        # Popularity
        pipe.zincrby("tag:popularity", 1, tag)
        pipe.execute()
        return True
    
    def get_entities(self, tag: str) -> Set[str]:
        return self.redis.smembers(f"tag:{tag.lower()}:entities")
    
    def get_popular_tags(self, limit: int) -> List[tuple]:
        return self.redis.zrevrange("tag:popularity", 0, limit-1, withscores=True)
```

---

## ❌ Common Mistakes (What NOT to Do)

### **MISTAKE 1: Only Forward Index** ❌

```python
# WRONG - No inverted index!
class BadTaggingSystem:
    def __init__(self):
        self.entity_to_tags = {}  # Only forward index
    
    def get_entities(self, tag):
        # O(N) scan ALL entities!
        result = []
        for entity_id, tags in self.entity_to_tags.items():
            if tag in tags:
                result.append(entity_id)
        return result

# CORRECT - Bidirectional mapping
class GoodTaggingSystem:
    def __init__(self):
        self.entity_to_tags = {}   # Forward
        self.tag_to_entities = {}  # Inverted ← THE KEY!
```

---

### **MISTAKE 2: Not Cleaning Up Empty Mappings** ❌

```python
# WRONG - Memory leak!
def remove_tag(self, entity_id, tag):
    self.entity_to_tags[entity_id].discard(tag)
    self.tag_to_entities[tag].discard(entity_id)
    # Empty sets stay in memory forever!

# CORRECT - Clean up
def remove_tag(self, entity_id, tag):
    self.entity_to_tags[entity_id].discard(tag)
    self.tag_to_entities[tag].discard(entity_id)
    
    # Clean up empty entries
    if not self.entity_to_tags[entity_id]:
        del self.entity_to_tags[entity_id]
    if not self.tag_to_entities[tag]:
        del self.tag_to_entities[tag]
```

---

### **MISTAKE 3: O(N) Popularity Count** ❌

```python
# WRONG - Count on every request!
def get_popular_tags(self, limit):
    counts = {}
    for entity_tags in self.entity_to_tags.values():
        for tag in entity_tags:
            counts[tag] = counts.get(tag, 0) + 1
    return sorted(counts.items(), key=lambda x: -x[1])[:limit]

# CORRECT - Maintain count incrementally
def add_tag(self, entity_id, tag):
    ...
    self._tag_usage[tag] += 1  # O(1) update

def get_popular_tags(self, limit):
    return heapq.nlargest(limit, self._tag_usage.items(), key=lambda x: x[1])
```

---

## 💯 Interview Checklist

- [ ] ✅ **Identified Inverted Index pattern**
- [ ] ✅ **Explained bidirectional mapping** and WHY
- [ ] ✅ **Drew architecture diagram**
- [ ] ✅ **Implemented case-insensitive** tags
- [ ] ✅ **Used Flyweight pattern** for Tag objects
- [ ] ✅ **Tracked usage counts** incrementally
- [ ] ✅ **Cleaned up empty mappings**
- [ ] ✅ **Implemented advanced queries** (intersection, union)
- [ ] ✅ **Discussed extensions** (hierarchy, autocomplete, distributed)

---

## 📚 Quick Reference Card

```
┌────────────────────────────────────────────────────────────┐
│               TAGGING SYSTEM CHEAT SHEET                   │
├────────────────────────────────────────────────────────────┤
│ CORE PATTERN: Inverted Index                              │
│   Forward:  entity_to_tags[entity] → {tags}               │
│   Inverted: tag_to_entities[tag] → {entities}             │
│                                                            │
│ WHY INVERTED INDEX?                                       │
│   Without: get_entities("bug") = O(N) scan all entities   │
│   With: get_entities("bug") = O(1) dictionary lookup      │
│                                                            │
│ KEY INVARIANT:                                            │
│   If tag T in entity_to_tags[E],                         │
│   then E in tag_to_entities[T]                           │
│   ALWAYS KEEP BOTH IN SYNC!                               │
│                                                            │
│ DESIGN PATTERNS:                                          │
│   - Inverted Index: Bidirectional O(1) lookups           │
│   - Facade: Hide sync complexity                          │
│   - Flyweight: Reuse Tag objects                          │
│                                                            │
│ COMPLEXITY:                                               │
│   - add_tag: O(1)                                        │
│   - remove_tag: O(1)                                     │
│   - get_entities: O(1) lookup + O(E) copy                │
│   - get_popular_tags: O(N log K)                         │
│                                                            │
│ GOTCHAS:                                                  │
│   - Case-insensitive (normalize to lowercase)            │
│   - Clean up empty mappings (memory leak!)               │
│   - Track usage incrementally (not O(N) count)           │
└────────────────────────────────────────────────────────────┘
```

---

**Real-World Usage:**
- Jira: Issue labels
- Confluence: Page tags
- Trello: Card labels
- GitHub: Issue/PR labels
- Gmail: Email labels
- Stack Overflow: Question tags

**Related Problems:**
- Design Search Engine (inverted index for text)
- Design Tag Cloud
- Design Bookmark Manager

