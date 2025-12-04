# 🏷️ PROBLEM 9: TAGGING MANAGEMENT SYSTEM

### ⭐⭐⭐⭐ **Design Atlassian's Tagging System (Jira/Confluence)**

**Frequency:** MEDIUM-HIGH - **Atlassian-specific problem!**
**Difficulty:** Medium
**Focus:** Many-to-Many Relationships, Bidirectional Lookup, Inverted Index

---

## 📋 Problem Statement

Design a tagging system used across Atlassian products (Jira, Confluence, Trello) where:
- Entities (issues, pages, cards) can have multiple tags
- Tags can be associated with multiple entities
- Support fast lookups in both directions

**Core Requirements:**
- `add_tag(entity_id, tag)`: Add tag to entity - O(1)
- `remove_tag(entity_id, tag)`: Remove tag from entity - O(1)
- `get_tags(entity_id)`: Get all tags for entity - O(T)
- `get_entities(tag)`: Get all entities with tag - O(E)
- `search_by_tag(partial)`: Search entities by partial tag name
- `get_popular_tags(limit)`: Get most used tags

---

## 🎯 Interview Approach

### Step 1: Clarify Requirements (2 min)
```
"Let me clarify the requirements:
1. Case-sensitive or insensitive tags?
2. Can tags have metadata (color, description)?
3. Maximum tags per entity?
4. Need to track tag creation/usage time?
5. Scale - how many entities and tags?"
```

### Step 2: Identify Key Insight (1 min)
```
"The key insight is bidirectional mapping:
- entity → tags (for 'get all tags of entity')
- tag → entities (for 'get all entities with tag')

This is essentially an inverted index, similar to how 
search engines work!"
```

---

## 🎨 Visual Example

```text
Entities and their tags:
┌──────────────────────────────────────┐
│ JIRA-101 → ["bug", "high-priority"]  │
│ JIRA-102 → ["feature", "frontend"]   │
│ JIRA-103 → ["bug", "backend"]        │
│ PAGE-201 → ["documentation", "api"]  │
│ PAGE-202 → ["documentation"]         │
└──────────────────────────────────────┘

Inverted Index (Tag → Entities):
┌─────────────────────────────────────────────┐
│ "bug" → {JIRA-101, JIRA-103}                │
│ "high-priority" → {JIRA-101}                │
│ "feature" → {JIRA-102}                      │
│ "frontend" → {JIRA-102}                     │
│ "backend" → {JIRA-103}                      │
│ "documentation" → {PAGE-201, PAGE-202}      │
│ "api" → {PAGE-201}                          │
└─────────────────────────────────────────────┘

Operations:
get_tags("JIRA-101") → ["bug", "high-priority"]
get_entities("bug") → ["JIRA-101", "JIRA-103"]
search_by_tag("doc") → ["PAGE-201", "PAGE-202"]
get_popular_tags(3) → ["documentation"(2), "bug"(2), "feature"(1)]
```

---

## 💻 Python Implementation

```python
from collections import defaultdict
from typing import Set, List, Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime
import heapq

# ============ Data Classes ============

@dataclass
class Tag:
    """
    Represents a tag with metadata.
    
    Design Decision: Tags are normalized to lowercase for
    case-insensitive matching.
    """
    name: str
    color: str = "#808080"  # Default gray
    description: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        # Normalize tag name
        self.name = self.name.lower().strip()

    def __eq__(self, other):
        if isinstance(other, Tag):
            return self.name == other.name
        return self.name == str(other).lower()

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f"Tag({self.name})"

@dataclass
class Entity:
    """
    Represents an entity that can be tagged.
    (Jira Issue, Confluence Page, Trello Card, etc.)
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

# ============ Tagging System ============

class TaggingSystem:
    """
    Tagging system with bidirectional mapping.
    
    Design Pattern: Inverted Index
    
    Key Design Decisions:
    1. Bidirectional maps for O(1) lookups in both directions
    2. Case-insensitive tag matching
    3. Usage count tracking for popularity
    4. Cleanup of empty mappings to prevent memory leaks
    
    Thread Safety Note:
    - Not thread-safe as-is
    - For production: use threading.Lock or concurrent collections
    """
    
    def __init__(self):
        # Entity ID → Set of Tags
        self._entity_to_tags: Dict[str, Set[Tag]] = defaultdict(set)
        
        # Tag → Set of Entity IDs (Inverted Index)
        self._tag_to_entities: Dict[Tag, Set[str]] = defaultdict(set)
        
        # Tag metadata storage
        self._tags: Dict[str, Tag] = {}
        
        # Tag usage count for popularity
        self._tag_usage: Dict[str, int] = defaultdict(int)
        
        # Entity storage
        self._entities: Dict[str, Entity] = {}
    
    # ============ Entity Management ============
    
    def register_entity(self, entity: Entity) -> None:
        """Register an entity in the system"""
        self._entities[entity.id] = entity
    
    def get_entity(self, entity_id: str) -> Optional[Entity]:
        """Get entity by ID"""
        return self._entities.get(entity_id)
    
    # ============ Tag Operations ============
    
    def add_tag(self, entity_id: str, tag_name: str, 
                color: str = None, description: str = None) -> bool:
        """
        Add a tag to an entity.
        
        Time Complexity: O(1)
        Space Complexity: O(1) per tag
        
        Returns: True if tag was added, False if already exists
        """
        if entity_id not in self._entities:
            raise ValueError(f"Entity not found: {entity_id}")

        # Get or create tag
        tag = self._get_or_create_tag(tag_name, color, description)
        
        # Check if already tagged
        if tag in self._entity_to_tags[entity_id]:
            return False
        
        # Add to bidirectional mappings
        self._entity_to_tags[entity_id].add(tag)
        self._tag_to_entities[tag].add(entity_id)
        
        # Update usage count
        self._tag_usage[tag.name] += 1
        
        return True
    
    def _get_or_create_tag(self, name: str, color: str = None, 
                          description: str = None) -> Tag:
        """Get existing tag or create new one"""
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
        
        Time Complexity: O(1)
        
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

        # Remove from bidirectional mappings
        self._entity_to_tags[entity_id].discard(tag)
        self._tag_to_entities[tag].discard(entity_id)
        
        # Update usage count
        self._tag_usage[tag.name] -= 1
        
        # Cleanup empty mappings
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
        Get all tags for an entity.
        
        Time Complexity: O(T) where T = tags per entity
        
        Returns: Set of tag names
        """
        tags = self._entity_to_tags.get(entity_id, set())
        return {tag.name for tag in tags}

    def get_tag_objects(self, entity_id: str) -> Set[Tag]:
        """Get tag objects with metadata"""
        return set(self._entity_to_tags.get(entity_id, set()))
    
    def get_entities(self, tag_name: str) -> Set[str]:
        """
        Get all entity IDs with a specific tag.
        
        Time Complexity: O(E) where E = entities with tag
        
        Returns: Set of entity IDs
        """
        normalized = tag_name.lower().strip()
        tag = self._tags.get(normalized)
        
        if not tag:
            return set()
        
        return set(self._tag_to_entities.get(tag, set()))
    
    def search_by_tag(self, partial_name: str) -> Set[str]:
        """
        Search entities by partial tag name.
        
        Time Complexity: O(N) where N = total unique tags
        
        Returns: Set of entity IDs matching any tag containing the search term
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
        
        Time Complexity: O(N log K) using heap where N = tags, K = limit
        
        Returns: List of (tag_name, count) tuples
        """
        if not self._tag_usage:
            return []
        
        # Use heap for O(N log K) instead of O(N log N) full sort
        return heapq.nlargest(
            limit,
            self._tag_usage.items(),
            key=lambda x: x[1]
        )
    
    # ============ Advanced Queries ============

    def get_entities_with_all_tags(self, tag_names: List[str]) -> Set[str]:
        """
        Get entities having ALL specified tags (intersection).
        
        Time Complexity: O(K × E) where K = tags, E = entities per tag
        """
        if not tag_names:
            return set()

        # Start with entities of first tag
        result = self.get_entities(tag_names[0])

        # Intersect with other tags
        for tag_name in tag_names[1:]:
            result &= self.get_entities(tag_name)
            
            # Early exit if empty
            if not result:
                return set()

        return result

    def get_entities_with_any_tag(self, tag_names: List[str]) -> Set[str]:
        """
        Get entities having ANY of specified tags (union).
        
        Time Complexity: O(K × E) where K = tags, E = entities per tag
        """
        result = set()

        for tag_name in tag_names:
            result |= self.get_entities(tag_name)

        return result

    def get_related_tags(self, tag_name: str, limit: int = 5) -> List[str]:
        """
        Get tags that frequently appear with the given tag.
        
        Useful for tag suggestions!
        
        Time Complexity: O(E × T) where E = entities with tag, T = avg tags per entity
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
        """Get system statistics"""
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

# ============ Extensions ============

class HierarchicalTaggingSystem(TaggingSystem):
    """
    Extended tagging with hierarchical tags.
    
    Example: programming/java, programming/python
    """
    
    def __init__(self):
        super().__init__()
        self._parent_map: Dict[str, str] = {}  # child → parent
    
    def add_tag_hierarchy(self, child: str, parent: str) -> None:
        """Set parent-child relationship"""
        self._parent_map[child.lower()] = parent.lower()
    
    def get_entities_with_hierarchy(self, tag_name: str) -> Set[str]:
        """Get entities with tag or any child tags"""
        result = self.get_entities(tag_name)
        
        # Find all children
        normalized = tag_name.lower()
        for child, parent in self._parent_map.items():
            if parent == normalized:
                result |= self.get_entities_with_hierarchy(child)
        
        return result

class TagAutoComplete:
    """
    Trie-based autocomplete for tags.
    
    Time: O(P + K) where P = prefix length, K = number of results
    """
    
    def __init__(self):
        self._trie = {}
        self._end_marker = "$"
    
    def add_tag(self, tag_name: str) -> None:
        """Add tag to trie"""
        node = self._trie
        for char in tag_name.lower():
            node = node.setdefault(char, {})
        node[self._end_marker] = tag_name
    
    def suggest(self, prefix: str, limit: int = 10) -> List[str]:
        """Get tag suggestions for prefix"""
        node = self._trie
        
        # Navigate to prefix node
        for char in prefix.lower():
            if char not in node:
                return []
            node = node[char]
        
        # Collect all tags under this node
        results = []
        self._collect_tags(node, results, limit)
        return results[:limit]
    
    def _collect_tags(self, node: dict, results: List[str], limit: int) -> None:
        if len(results) >= limit:
            return
        
        if self._end_marker in node:
            results.append(node[self._end_marker])
        
        for char, child_node in node.items():
            if char != self._end_marker:
                self._collect_tags(child_node, results, limit)

# ============ Demo ============

def main():
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

    # Queries
    print("=== Tags for JIRA-101 ===")
    print(system.get_tags("JIRA-101"))

    print("\n=== Entities with 'bug' tag ===")
    print(system.get_entities("bug"))

    print("\n=== Search for 'doc' ===")
    print(system.search_by_tag("doc"))

    print("\n=== Top 3 Popular Tags ===")
    print(system.get_popular_tags(3))

    print("\n=== Entities with ALL tags: [bug, backend] ===")
    print(system.get_entities_with_all_tags(["bug", "backend"]))
    
    print("\n=== Entities with ANY tags: [feature, documentation] ===")
    print(system.get_entities_with_any_tag(["feature", "documentation"]))
    
    print("\n=== Related tags to 'bug' ===")
    print(system.get_related_tags("bug"))

    print("\n=== Statistics ===")
    print(system.get_statistics())
    
    # Remove tag demo
    print("\n=== After removing 'high-priority' from JIRA-101 ===")
    system.remove_tag("JIRA-101", "high-priority")
    print(system.get_tags("JIRA-101"))

if __name__ == "__main__":
    main()
```

---

## 🎯 Interview Explanation Flow

### 1. Identify Core Pattern (30 sec)
```
"This is fundamentally an Inverted Index problem:
- Forward index: entity → tags
- Inverted index: tag → entities

Same pattern used by search engines for text search!"
```

### 2. Explain Data Structures (1 min)
```
"I use:
- Dict[str, Set[Tag]] for entity → tags (O(1) lookup)
- Dict[Tag, Set[str]] for tag → entities (O(1) lookup)
- Usage counter for popularity (avoid O(N) counting)

The key is maintaining BOTH directions in sync!"
```

### 3. Discuss Trade-offs (1 min)
```
"Trade-offs:
- Space: 2x storage for bidirectional maps
- Time: O(1) for all basic operations
- Consistency: Must update both maps atomically

For production:
- Use Redis Sets for distributed tags
- Consider Elasticsearch for full-text search"
```

---

## 📊 Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| add_tag | O(1) | O(1) |
| remove_tag | O(1) | O(1) |
| get_tags | O(T) | O(T) |
| get_entities | O(E) | O(E) |
| search_by_tag | O(N) | O(E) |
| get_popular_tags | O(N log K) | O(K) |
| get_related_tags | O(E × T) | O(N) |

**Where:** T = tags per entity, E = entities per tag, N = total tags, K = limit

---

## 💡 Interview Tips

### What Interviewers Look For:
✅ **Bidirectional mapping** for O(1) lookups
✅ **Case-insensitive** tag handling
✅ **Memory cleanup** for removed tags
✅ **Efficient popularity** tracking
✅ **Understanding of inverted index** pattern

### Common Mistakes:
❌ Only one-way mapping (missing inverted index)
❌ O(N) popularity calculation on every request
❌ Not cleaning up empty mappings (memory leak)
❌ Case-sensitive matching without discussion
❌ Missing atomic updates for consistency

### Questions to Ask:
- "Case-sensitive or insensitive?"
- "Maximum tags per entity?"
- "Need tag metadata (color, description)?"
- "Scale expectations?"
- "Need tag suggestions/autocomplete?"

---

## 🔗 Real-World Usage

**Atlassian Products:**
- **Jira**: Issue labels
- **Confluence**: Page tags
- **Trello**: Card labels
- **Bitbucket**: PR labels

**Similar Systems:**
- GitHub issue tags
- Stack Overflow question tags
- Gmail labels
- Social media hashtags

---

## 🚀 Production Considerations

### Distributed System:
```python
# Using Redis for distributed tags
class RedisTaggingSystem:
    def add_tag(self, entity_id: str, tag: str):
        # SADD entity:{id}:tags {tag}
        # SADD tag:{tag}:entities {entity_id}
        # ZINCRBY tag:popularity {tag} 1
        pass
```

### Search Integration:
```python
# Using Elasticsearch for full-text search
class ElasticTaggingSystem:
    def search_tags(self, query: str):
        # Use prefix/fuzzy matching
        pass
```

