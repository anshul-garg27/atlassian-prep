# 🏷️ PROBLEM 9: TAGGING MANAGEMENT SYSTEM

### ⭐⭐⭐⭐ **Design Atlassian's Tagging System (Jira/Confluence)**

**Frequency:** Appears in **MEDIUM-HIGH FREQUENCY** - Atlassian-specific!
**Difficulty:** Medium
**Focus:** Many-to-Many Relationships, Bidirectional Lookup, Search

---

## 📋 Problem Statement

Design a tagging system used across Atlassian products (Jira, Confluence, Trello) where:
- Entities (issues, pages, cards) can have multiple tags
- Tags can be associated with multiple entities
- Support fast lookups in both directions

**Core Requirements:**
- `addTag(entityId, tag)`: Add tag to entity
- `removeTag(entityId, tag)`: Remove tag from entity
- `getTags(entityId)`: Get all tags for entity
- `getEntities(tag)`: Get all entities with tag
- `searchByTag(tagName)`: Search entities by tag name
- `getPopularTags(limit)`: Get most used tags

**Input:** Entity IDs (strings), Tag names (strings)
**Output:** Fast bidirectional queries

**Constraints:**
- 1 ≤ Number of entities ≤ 1,000,000
- 1 ≤ Number of tags ≤ 100,000
- 1 ≤ Tags per entity ≤ 50
- Case-insensitive tag matching

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

Tag → Entities mapping:
┌─────────────────────────────────────────────┐
│ "bug" → [JIRA-101, JIRA-103]                │
│ "high-priority" → [JIRA-101]                │
│ "feature" → [JIRA-102]                      │
│ "frontend" → [JIRA-102]                     │
│ "backend" → [JIRA-103]                      │
│ "documentation" → [PAGE-201, PAGE-202]      │
│ "api" → [PAGE-201]                          │
└─────────────────────────────────────────────┘

Operations:
getTags("JIRA-101") → ["bug", "high-priority"]
getEntities("bug") → ["JIRA-101", "JIRA-103"]
searchByTag("doc") → ["PAGE-201", "PAGE-202"]
getPopularTags(3) → ["documentation" (2), "bug" (2), "feature" (1)]
```

---

## 💻 Implementation

### **Java Implementation**

```java
import java.util.*;
import java.util.stream.Collectors;

/**
 * Tag class representing a single tag
 */
class Tag {
    private String name;
    private long createdAt;

    public Tag(String name) {
        this.name = name.toLowerCase(); // Case-insensitive
        this.createdAt = System.currentTimeMillis();
    }

    public String getName() {
        return name;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Tag)) return false;
        Tag tag = (Tag) o;
        return name.equals(tag.name);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name);
    }

    @Override
    public String toString() {
        return name;
    }
}

/**
 * Entity class (Jira issue, Confluence page, etc.)
 */
class Entity {
    private String id;
    private String type; // "ISSUE", "PAGE", "CARD"

    public Entity(String id, String type) {
        this.id = id;
        this.type = type;
    }

    public String getId() {
        return id;
    }

    public String getType() {
        return type;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Entity)) return false;
        Entity entity = (Entity) o;
        return id.equals(entity.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}

/**
 * Tagging Management System
 * Maintains bidirectional mapping for fast lookups
 */
class TaggingSystem {
    // Entity -> Set of Tags
    private Map<String, Set<Tag>> entityToTags;

    // Tag -> Set of Entity IDs
    private Map<Tag, Set<String>> tagToEntities;

    // Tag usage count for popularity tracking
    private Map<Tag, Integer> tagUsageCount;

    // Store entities for retrieval
    private Map<String, Entity> entities;

    public TaggingSystem() {
        this.entityToTags = new HashMap<>();
        this.tagToEntities = new HashMap<>();
        this.tagUsageCount = new HashMap<>();
        this.entities = new HashMap<>();
    }

    /**
     * Register an entity in the system
     */
    public void registerEntity(Entity entity) {
        entities.put(entity.getId(), entity);
        entityToTags.putIfAbsent(entity.getId(), new HashSet<>());
    }

    /**
     * Add tag to entity
     * Time: O(1)
     */
    public void addTag(String entityId, String tagName) {
        // Validate entity exists
        if (!entities.containsKey(entityId)) {
            throw new IllegalArgumentException("Entity not found: " + entityId);
        }

        Tag tag = new Tag(tagName);

        // Add to entity->tags mapping
        entityToTags.computeIfAbsent(entityId, k -> new HashSet<>())
                    .add(tag);

        // Add to tag->entities mapping
        tagToEntities.computeIfAbsent(tag, k -> new HashSet<>())
                     .add(entityId);

        // Update usage count
        tagUsageCount.put(tag, tagUsageCount.getOrDefault(tag, 0) + 1);
    }

    /**
     * Remove tag from entity
     * Time: O(1)
     */
    public boolean removeTag(String entityId, String tagName) {
        Tag tag = new Tag(tagName);

        // Remove from entity->tags
        Set<Tag> tags = entityToTags.get(entityId);
        if (tags == null || !tags.remove(tag)) {
            return false; // Tag not found
        }

        // Remove from tag->entities
        Set<String> entityIds = tagToEntities.get(tag);
        if (entityIds != null) {
            entityIds.remove(entityId);

            // Clean up empty sets
            if (entityIds.isEmpty()) {
                tagToEntities.remove(tag);
                tagUsageCount.remove(tag);
            } else {
                tagUsageCount.put(tag, tagUsageCount.get(tag) - 1);
            }
        }

        return true;
    }

    /**
     * Get all tags for an entity
     * Time: O(1) to access, O(T) to copy where T = tags per entity
     */
    public Set<String> getTags(String entityId) {
        Set<Tag> tags = entityToTags.get(entityId);
        if (tags == null) {
            return Collections.emptySet();
        }

        return tags.stream()
                   .map(Tag::getName)
                   .collect(Collectors.toSet());
    }

    /**
     * Get all entities with a specific tag
     * Time: O(1) to access, O(E) to copy where E = entities with tag
     */
    public Set<String> getEntities(String tagName) {
        Tag tag = new Tag(tagName);
        Set<String> entityIds = tagToEntities.get(tag);

        if (entityIds == null) {
            return Collections.emptySet();
        }

        return new HashSet<>(entityIds);
    }

    /**
     * Search entities by partial tag name (case-insensitive)
     * Time: O(T) where T = total unique tags
     */
    public Set<String> searchByTag(String partialTagName) {
        String searchTerm = partialTagName.toLowerCase();
        Set<String> result = new HashSet<>();

        for (Map.Entry<Tag, Set<String>> entry : tagToEntities.entrySet()) {
            if (entry.getKey().getName().contains(searchTerm)) {
                result.addAll(entry.getValue());
            }
        }

        return result;
    }

    /**
     * Get top N most popular tags
     * Time: O(T log T) where T = total unique tags
     */
    public List<String> getPopularTags(int limit) {
        return tagUsageCount.entrySet().stream()
                .sorted(Map.Entry.<Tag, Integer>comparingByValue().reversed())
                .limit(limit)
                .map(entry -> entry.getKey().getName())
                .collect(Collectors.toList());
    }

    /**
     * Get entities with ALL specified tags (intersection)
     * Time: O(N * E) where N = number of tags, E = entities per tag
     */
    public Set<String> getEntitiesWithAllTags(List<String> tagNames) {
        if (tagNames.isEmpty()) {
            return Collections.emptySet();
        }

        // Start with entities of first tag
        Set<String> result = getEntities(tagNames.get(0));

        // Intersect with entities of other tags
        for (int i = 1; i < tagNames.size(); i++) {
            result.retainAll(getEntities(tagNames.get(i)));
        }

        return result;
    }

    /**
     * Get entities with ANY of specified tags (union)
     * Time: O(N * E) where N = number of tags, E = entities per tag
     */
    public Set<String> getEntitiesWithAnyTag(List<String> tagNames) {
        Set<String> result = new HashSet<>();

        for (String tagName : tagNames) {
            result.addAll(getEntities(tagName));
        }

        return result;
    }

    /**
     * Get tag statistics
     */
    public Map<String, Object> getStatistics() {
        Map<String, Object> stats = new HashMap<>();
        stats.put("totalEntities", entities.size());
        stats.put("totalTags", tagToEntities.size());
        stats.put("totalTaggings", tagUsageCount.values().stream()
                                                 .mapToInt(Integer::intValue).sum());
        return stats;
    }
}

// ============ Demo ============
public class Main {
    public static void main(String[] args) {
        TaggingSystem system = new TaggingSystem();

        // Register entities
        system.registerEntity(new Entity("JIRA-101", "ISSUE"));
        system.registerEntity(new Entity("JIRA-102", "ISSUE"));
        system.registerEntity(new Entity("JIRA-103", "ISSUE"));
        system.registerEntity(new Entity("PAGE-201", "PAGE"));
        system.registerEntity(new Entity("PAGE-202", "PAGE"));

        // Add tags
        system.addTag("JIRA-101", "bug");
        system.addTag("JIRA-101", "high-priority");
        system.addTag("JIRA-102", "feature");
        system.addTag("JIRA-102", "frontend");
        system.addTag("JIRA-103", "bug");
        system.addTag("JIRA-103", "backend");
        system.addTag("PAGE-201", "documentation");
        system.addTag("PAGE-201", "api");
        system.addTag("PAGE-202", "documentation");

        // Queries
        System.out.println("=== Tags for JIRA-101 ===");
        System.out.println(system.getTags("JIRA-101"));

        System.out.println("\n=== Entities with 'bug' tag ===");
        System.out.println(system.getEntities("bug"));

        System.out.println("\n=== Search for 'doc' ===");
        System.out.println(system.searchByTag("doc"));

        System.out.println("\n=== Top 3 popular tags ===");
        System.out.println(system.getPopularTags(3));

        System.out.println("\n=== Entities with ALL tags: [bug, backend] ===");
        System.out.println(system.getEntitiesWithAllTags(
                Arrays.asList("bug", "backend")));

        System.out.println("\n=== Statistics ===");
        System.out.println(system.getStatistics());

        // Remove tag
        system.removeTag("JIRA-101", "high-priority");
        System.out.println("\n=== After removing 'high-priority' from JIRA-101 ===");
        System.out.println(system.getTags("JIRA-101"));
    }
}
```

---

### **Python Implementation**

```python
from collections import defaultdict
from typing import Set, List, Dict
from dataclasses import dataclass

@dataclass
class Entity:
    id: str
    type: str  # "ISSUE", "PAGE", "CARD"

class Tag:
    def __init__(self, name: str):
        self.name = name.lower()  # Case-insensitive

    def __eq__(self, other):
        return isinstance(other, Tag) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return self.name

class TaggingSystem:
    def __init__(self):
        # Entity ID -> Set of Tags
        self.entity_to_tags: Dict[str, Set[Tag]] = defaultdict(set)

        # Tag -> Set of Entity IDs
        self.tag_to_entities: Dict[Tag, Set[str]] = defaultdict(set)

        # Tag usage count
        self.tag_usage_count: Dict[Tag, int] = defaultdict(int)

        # Store entities
        self.entities: Dict[str, Entity] = {}

    def register_entity(self, entity: Entity):
        """Register an entity in the system"""
        self.entities[entity.id] = entity

    def add_tag(self, entity_id: str, tag_name: str):
        """Add tag to entity - O(1)"""
        if entity_id not in self.entities:
            raise ValueError(f"Entity not found: {entity_id}")

        tag = Tag(tag_name)

        # Add to mappings
        self.entity_to_tags[entity_id].add(tag)
        self.tag_to_entities[tag].add(entity_id)

        # Update count
        self.tag_usage_count[tag] += 1

    def remove_tag(self, entity_id: str, tag_name: str) -> bool:
        """Remove tag from entity - O(1)"""
        tag = Tag(tag_name)

        if entity_id not in self.entity_to_tags:
            return False

        # Remove from entity->tags
        if tag not in self.entity_to_tags[entity_id]:
            return False

        self.entity_to_tags[entity_id].remove(tag)

        # Remove from tag->entities
        if tag in self.tag_to_entities:
            self.tag_to_entities[tag].discard(entity_id)

            # Clean up if empty
            if not self.tag_to_entities[tag]:
                del self.tag_to_entities[tag]
                del self.tag_usage_count[tag]
            else:
                self.tag_usage_count[tag] -= 1

        return True

    def get_tags(self, entity_id: str) -> Set[str]:
        """Get all tags for entity - O(1)"""
        tags = self.entity_to_tags.get(entity_id, set())
        return {tag.name for tag in tags}

    def get_entities(self, tag_name: str) -> Set[str]:
        """Get all entities with tag - O(1)"""
        tag = Tag(tag_name)
        return set(self.tag_to_entities.get(tag, set()))

    def search_by_tag(self, partial_tag_name: str) -> Set[str]:
        """Search entities by partial tag name - O(T)"""
        search_term = partial_tag_name.lower()
        result = set()

        for tag, entity_ids in self.tag_to_entities.items():
            if search_term in tag.name:
                result.update(entity_ids)

        return result

    def get_popular_tags(self, limit: int) -> List[str]:
        """Get top N popular tags - O(T log T)"""
        sorted_tags = sorted(
            self.tag_usage_count.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return [tag.name for tag, _ in sorted_tags[:limit]]

    def get_entities_with_all_tags(self, tag_names: List[str]) -> Set[str]:
        """Get entities having ALL specified tags - O(N * E)"""
        if not tag_names:
            return set()

        # Start with first tag's entities
        result = self.get_entities(tag_names[0])

        # Intersect with other tags
        for tag_name in tag_names[1:]:
            result &= self.get_entities(tag_name)

        return result

    def get_entities_with_any_tag(self, tag_names: List[str]) -> Set[str]:
        """Get entities having ANY of specified tags - O(N * E)"""
        result = set()

        for tag_name in tag_names:
            result |= self.get_entities(tag_name)

        return result

    def get_statistics(self) -> Dict:
        """Get system statistics"""
        total_taggings = sum(self.tag_usage_count.values())
        return {
            "total_entities": len(self.entities),
            "total_tags": len(self.tag_to_entities),
            "total_taggings": total_taggings
        }

# Demo
if __name__ == "__main__":
    system = TaggingSystem()

    # Register entities
    system.register_entity(Entity("JIRA-101", "ISSUE"))
    system.register_entity(Entity("JIRA-102", "ISSUE"))
    system.register_entity(Entity("JIRA-103", "ISSUE"))
    system.register_entity(Entity("PAGE-201", "PAGE"))
    system.register_entity(Entity("PAGE-202", "PAGE"))

    # Add tags
    system.add_tag("JIRA-101", "bug")
    system.add_tag("JIRA-101", "high-priority")
    system.add_tag("JIRA-102", "feature")
    system.add_tag("JIRA-102", "frontend")
    system.add_tag("JIRA-103", "bug")
    system.add_tag("JIRA-103", "backend")
    system.add_tag("PAGE-201", "documentation")
    system.add_tag("PAGE-201", "api")
    system.add_tag("PAGE-202", "documentation")

    # Queries
    print("=== Tags for JIRA-101 ===")
    print(system.get_tags("JIRA-101"))

    print("\n=== Entities with 'bug' tag ===")
    print(system.get_entities("bug"))

    print("\n=== Search for 'doc' ===")
    print(system.search_by_tag("doc"))

    print("\n=== Top 3 popular tags ===")
    print(system.get_popular_tags(3))

    print("\n=== Entities with ALL tags: [bug, backend] ===")
    print(system.get_entities_with_all_tags(["bug", "backend"]))

    print("\n=== Statistics ===")
    print(system.get_statistics())
```

---

## 🚀 Extensions & Follow-ups

### **Extension 1: Tag Hierarchies**
```java
class Tag {
    String name;
    Tag parent;  // For hierarchical tags

    // e.g., "java" is child of "programming"
}
```

### **Extension 2: Tag Auto-complete**
```java
class TaggingSystem {
    // Trie for fast prefix matching
    private Trie tagTrie;

    public List<String> suggestTags(String prefix) {
        return tagTrie.findWordsWithPrefix(prefix);
    }
}
```

### **Extension 3: Tag Synonyms**
```java
class TaggingSystem {
    Map<String, Set<String>> synonyms;

    public void addSynonym(String tag1, String tag2) {
        synonyms.computeIfAbsent(tag1, k -> new HashSet<>()).add(tag2);
    }

    public Set<String> getEntitiesWithSynonyms(String tagName) {
        Set<String> result = getEntities(tagName);
        // Add entities with synonyms
        for (String synonym : synonyms.getOrDefault(tagName, Set.of())) {
            result.addAll(getEntities(synonym));
        }
        return result;
    }
}
```

---

## 📊 Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| addTag | O(1) | O(1) |
| removeTag | O(1) | O(1) |
| getTags | O(T) | O(T) |
| getEntities | O(E) | O(E) |
| searchByTag | O(N) | O(E) |
| getPopularTags | O(N log N) | O(N) |

**Where:** T = tags per entity, E = entities per tag, N = total unique tags

**Space:** O(E×T + T×E) = O(E×T) overall

---

## 💡 Interview Discussion Points

### **What Interviewers Look For:**
✅ **Bidirectional mapping** for O(1) lookups
✅ **Case-insensitive** tag matching
✅ **Efficient storage** (avoid duplication)
✅ **Clean separation** (Tag, Entity, System classes)
✅ **Discuss trade-offs** (memory vs speed)

### **Questions to Ask:**
- Case-sensitive or insensitive tags?
- Can entities have duplicate tags?
- Need to track tag creation time?
- Need tag permissions/ownership?
- Scale: millions of entities?

### **Follow-up Discussions:**
1. **How to handle tag renaming?**
   - Update all references atomically
   - Use tag IDs internally, names as display

2. **How to implement tag suggestions?**
   - Trie for prefix matching
   - Cache popular tags

3. **How to scale to distributed system?**
   - Shard by entity ID
   - Use Redis for tag-to-entities mapping
   - Event-driven updates

---

## 💯 Best Practices

✅ **Use bidirectional maps** for fast lookups
✅ **Normalize tag names** (lowercase, trim)
✅ **Use Set for uniqueness** (no duplicate tags)
✅ **Clean up empty mappings** to avoid memory leaks
✅ **Consider Trie** for auto-complete features
✅ **Track usage counts** for popularity
✅ **Support bulk operations** (addTags, removeTags)

**Interview Pro Tip:** This is an **Atlassian-specific problem**! Mention Jira labels, Confluence tags, and how they're used across products!

---

**Related Problems:**
- Inverted Index design
- Search engine autocomplete
- Social media hashtags

**Real-World Usage:**
- Jira issue labels
- Confluence page tags
- Trello card labels
- GitHub issue tags
