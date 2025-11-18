# 🏗️ SYSTEM DESIGN / HLD ROUND - Complete Guide

**Duration:** 60 minutes
**Format:** High-Level Architecture Design
**Difficulty:** Hard
**Pass Rate:** ~65%

---

## 📋 Round Structure

```
┌──────────────────────────────────────────────────┐
│ Requirements Gathering (5-10 minutes)            │
│ ├─ Functional requirements                       │
│ ├─ Non-functional requirements                   │
│ └─ Constraints & assumptions                     │
├──────────────────────────────────────────────────┤
│ API Design (10 minutes)                          │
│ ├─ REST/GraphQL endpoints                        │
│ └─ Request/Response formats                      │
├──────────────────────────────────────────────────┤
│ Database Schema (10 minutes)                     │
│ ├─ Tables/Collections design                     │
│ ├─ Indexes & relationships                       │
│ └─ SQL vs NoSQL decision                         │
├──────────────────────────────────────────────────┤
│ Architecture & Scalability (20-25 minutes)       │
│ ├─ Component diagram                             │
│ ├─ Data flow                                     │
│ ├─ Caching strategy                              │
│ ├─ Load balancing                                │
│ └─ Sharding/Partitioning                         │
├──────────────────────────────────────────────────┤
│ Deep Dives (10-15 minutes)                       │
│ ├─ Bottlenecks & optimizations                   │
│ └─ Trade-off discussions                         │
└──────────────────────────────────────────────────┘
```

---

## 🏷️ PROBLEM 1: TAGGING MANAGEMENT SYSTEM (Most Popular!)

### ⭐⭐⭐⭐⭐ **Product-Agnostic Tagging System**

**Frequency:** Appears in **60%** of HLD rounds!

**Problem Statement:**
> Design a scalable tagging system for Atlassian products (Jira, Confluence, Bitbucket). Users should be able to:
> - Add/remove/update tags on content
> - Search content by tags
> - View popular/trending tags
> - Get autocomplete suggestions

**Products:**
- Jira → Issues
- Confluence → Pages
- Bitbucket → Pull Requests

---

### 📝 **Step 1: Requirements Clarification**

**Functional Requirements:**
1. Add tag to content
2. Remove tag from content
3. Update tag name
4. Get all content with specific tag
5. Get all tags for specific content
6. Search/autocomplete tags
7. Get trending/popular tags

**Non-Functional Requirements:**
1. **Scale:** 
   - 100M users
   - 1B pieces of content
   - 10M unique tags
   - 10B tag-content mappings
2. **Performance:**
   - Tag search: < 50ms
   - Autocomplete: < 20ms
   - Add/remove tag: < 100ms
3. **Availability:** 99.9%
4. **Consistency:** Eventual consistency OK for tag counts

**Out of Scope (Clarify!):**
- Tag permissions/access control
- Tag hierarchies (nested tags)
- User-specific tags (private tags)

---

### 🌐 **Step 2: API Design**

```javascript
// RESTful API Design

// 1. Add tag to content
POST /api/v1/content/{contentId}/tags
{
  "tagName": "frontend",
  "productType": "jira"
}
Response: 201 Created

// 2. Remove tag from content
DELETE /api/v1/content/{contentId}/tags/{tagId}
Response: 204 No Content

// 3. Get all tags for content
GET /api/v1/content/{contentId}/tags
Response: {
  "contentId": "123",
  "tags": [
    {"id": "1", "name": "frontend", "count": 500},
    {"id": "2", "name": "react", "count": 300}
  ]
}

// 4. Get content by tag
GET /api/v1/tags/{tagName}/content?product=jira&page=1&limit=20
Response: {
  "tagName": "frontend",
  "totalCount": 1500,
  "content": [
    {"contentId": "123", "title": "...", "type": "issue"},
    // ...
  ]
}

// 5. Search/Autocomplete tags
GET /api/v1/tags/search?q=fron&limit=10
Response: {
  "suggestions": [
    {"id": "1", "name": "frontend", "count": 5000},
    {"id": "2", "name": "front-end", "count": 200}
  ]
}

// 6. Get trending tags
GET /api/v1/tags/trending?product=jira&timeWindow=7d&limit=10
Response: {
  "trends": [
    {"name": "frontend", "count": 500, "growth": "+25%"},
    // ...
  ]
}
```

---

### 🗄️ **Step 3: Database Schema**

#### **Option 1: Relational (PostgreSQL)**

```sql
-- Tags table
CREATE TABLE tags (
    tag_id BIGSERIAL PRIMARY KEY,
    tag_name VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    usage_count BIGINT DEFAULT 0
);

CREATE INDEX idx_tag_name ON tags(tag_name);
CREATE INDEX idx_usage_count ON tags(usage_count DESC);

-- Content table (simplified)
CREATE TABLE content (
    content_id BIGSERIAL PRIMARY KEY,
    product_type VARCHAR(50),  -- 'jira', 'confluence', 'bitbucket'
    title VARCHAR(500),
    created_by BIGINT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_content_product ON content(product_type);

-- Tag-Content mapping (many-to-many)
CREATE TABLE content_tags (
    id BIGSERIAL PRIMARY KEY,
    content_id BIGINT NOT NULL,
    tag_id BIGINT NOT NULL,
    tagged_at TIMESTAMP DEFAULT NOW(),
    tagged_by BIGINT,
    
    FOREIGN KEY (content_id) REFERENCES content(content_id),
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id),
    
    UNIQUE(content_id, tag_id)  -- Prevent duplicate tags
);

-- Composite indexes for common queries
CREATE INDEX idx_content_tags_content ON content_tags(content_id);
CREATE INDEX idx_content_tags_tag ON content_tags(tag_id);
CREATE INDEX idx_content_tags_time ON content_tags(tagged_at DESC);

-- For trending tags (time-series data)
CREATE TABLE tag_usage_stats (
    id BIGSERIAL PRIMARY KEY,
    tag_id BIGINT NOT NULL,
    date DATE NOT NULL,
    usage_count INT DEFAULT 0,
    
    UNIQUE(tag_id, date)
);

CREATE INDEX idx_tag_stats_date ON tag_usage_stats(date DESC);
```

**Queries:**
```sql
-- Add tag to content
INSERT INTO content_tags (content_id, tag_id, tagged_by) 
VALUES (123, 45, 1001);

-- Get all tags for content
SELECT t.tag_id, t.tag_name, t.usage_count
FROM tags t
JOIN content_tags ct ON t.tag_id = ct.tag_id
WHERE ct.content_id = 123;

-- Get content by tag (paginated)
SELECT c.content_id, c.title, c.product_type
FROM content c
JOIN content_tags ct ON c.content_id = ct.content_id
WHERE ct.tag_id = 45
ORDER BY ct.tagged_at DESC
LIMIT 20 OFFSET 0;

-- Autocomplete tags
SELECT tag_id, tag_name, usage_count
FROM tags
WHERE tag_name LIKE 'fron%'
ORDER BY usage_count DESC
LIMIT 10;

-- Trending tags (last 7 days)
SELECT t.tag_name, SUM(tus.usage_count) as total_uses
FROM tags t
JOIN tag_usage_stats tus ON t.tag_id = tus.tag_id
WHERE tus.date >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY t.tag_id, t.tag_name
ORDER BY total_uses DESC
LIMIT 10;
```

#### **Option 2: NoSQL (DynamoDB)**

```
// Tags Table
Table: tags
Partition Key: tag_id
Sort Key: -
Attributes: {
  tag_id: string,
  tag_name: string,
  usage_count: number,
  created_at: timestamp
}
GSI: tag_name-index (for lookup by name)

// Content Tags Table (mappings)
Table: content_tags
Partition Key: content_id
Sort Key: tag_id
Attributes: {
  content_id: string,
  tag_id: string,
  tagged_at: timestamp,
  tagged_by: string
}
GSI: tag_id-tagged_at-index (for reverse lookup: tag -> contents)

// Tag to Content (reverse index)
Table: tag_contents
Partition Key: tag_id
Sort Key: content_id#timestamp
Attributes: {
  tag_id: string,
  content_id: string,
  product_type: string,
  timestamp: number
}
```

**Why SQL over NoSQL for this use case?**
- ✅ Complex queries (JOIN, aggregations)
- ✅ ACID transactions for consistency
- ✅ Mature indexing capabilities
- ✅ Tag analytics (counts, trends)
- ❌ NoSQL: Hard to model many-to-many relationships efficiently

---

### 🏛️ **Step 4: High-Level Architecture**

```
                          ┌─────────────────┐
                          │   CDN / Edge    │
                          │  (Static Assets)│
                          └────────┬────────┘
                                   │
                          ┌────────▼────────┐
                          │  Load Balancer  │
                          └────────┬────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                    │
     ┌────────▼────────┐  ┌────────▼────────┐  ┌──────▼──────┐
     │  API Gateway    │  │  API Gateway    │  │  API Gateway│
     │   (Node.js)     │  │   (Node.js)     │  │  (Node.js)  │
     └────────┬────────┘  └────────┬────────┘  └──────┬──────┘
              │                    │                    │
              └────────────────────┼────────────────────┘
                                   │
        ┌──────────────────────────┼──────────────────────────┐
        │                          │                          │
┌───────▼───────┐       ┌──────────▼──────────┐     ┌────────▼────────┐
│ Tagging       │       │  Search Service     │     │  Analytics      │
│ Service       │       │  (Elasticsearch)    │     │  Service        │
│ (Java/Go)     │       │  - Autocomplete     │     │  (Spark)        │
└───────┬───────┘       │  - Fuzzy search     │     └────────┬────────┘
        │               └──────────┬──────────┘              │
        │                          │                         │
        │                  ┌───────▼────────┐                │
        │                  │  Redis Cache   │                │
        │                  │  - Tag counts  │                │
        │                  │  - Hot tags    │                │
        │                  └───────┬────────┘                │
        │                          │                         │
┌───────▼──────────────────────────▼─────────────────────────▼─────┐
│                    PostgreSQL (Primary)                           │
│  - Tags table                                                     │
│  - Content table                                                  │
│  - Content_tags mapping                                           │
│                                                                   │
│  Sharding Strategy: By tag_id hash                               │
│  Read Replicas: 3-5 for read-heavy workload                      │
└───────────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────┐
│  Kafka / SQS    │
│  Event Stream   │
│  - Tag added    │
│  - Tag removed  │
└─────────┬───────┘
          │
   ┌──────▼───────┐
   │  Trend       │
   │  Calculator  │
   │  (Batch)     │
   └──────────────┘
```

---

### ⚡ **Step 5: Scalability & Optimizations**

#### **Caching Strategy**

```python
# Redis Cache Structure

# 1. Tag metadata cache (frequently accessed tags)
Key: "tag:{tag_id}"
Value: {
  "name": "frontend",
  "count": 50000
}
TTL: 1 hour

# 2. Content tags cache
Key: "content:{content_id}:tags"
Value: ["tag1", "tag2", "tag3"]
TTL: 5 minutes

# 3. Tag search results cache
Key: "tag:search:{query}"
Value: [
  {"id": 1, "name": "frontend", "count": 5000},
  {"id": 2, "name": "front-end", "count": 200}
]
TTL: 10 minutes

# 4. Trending tags cache
Key: "tags:trending:{product}:{timeWindow}"
Value: [{"name": "frontend", "count": 500}, ...]
TTL: 30 minutes (or update via cron)
```

#### **Database Sharding**

**Shard by tag_id:**
```
Shard 1: tag_id % 10 == 0,1
Shard 2: tag_id % 10 == 2,3
Shard 3: tag_id % 10 == 4,5
...
```

**Challenge:** How to get "all tags for content"?
- Need to query all shards (fan-out query)
- Solution: Maintain reverse index in separate table
  - Table: content_to_tags (sharded by content_id)
  - Stores all tags for a content_id

#### **Elasticsearch for Search**

```json
// Index: tags
{
  "mappings": {
    "properties": {
      "tag_id": {"type": "keyword"},
      "tag_name": {
        "type": "text",
        "analyzer": "standard",
        "fields": {
          "keyword": {"type": "keyword"},
          "ngram": {
            "type": "text",
            "analyzer": "ngram_analyzer"
          }
        }
      },
      "usage_count": {"type": "integer"},
      "product_type": {"type": "keyword"}
    }
  }
}

// Autocomplete query
GET /tags/_search
{
  "query": {
    "match": {
      "tag_name.ngram": "fron"
    }
  },
  "sort": [
    {"usage_count": "desc"}
  ],
  "size": 10
}
```

#### **Rate Limiting**

```
Per user:
- Add/remove tag: 100 requests/min
- Search tags: 1000 requests/min
- Get content by tag: 500 requests/min

Implementation: Redis with sliding window
```

---

### 🔥 **Step 6: Deep Dive Topics**

#### **How to Handle Trending Tags?**

**Approach: Time-windowed aggregation**

```python
# Real-time pipeline
1. User adds tag -> Event to Kafka
2. Stream processor (Flink/Spark Streaming) aggregates:
   - Count tags added per 5-min window
   - Keep sliding window of last 24 hours
3. Update trending_tags table
4. Cache results in Redis

# Batch pipeline (backup)
1. Daily cron job
2. Query tag_usage_stats table
3. Calculate growth rate: (today - yesterday) / yesterday
4. Update trending cache
```

#### **How to Handle Tag Renames?**

```sql
-- When tag "frontend" renamed to "front-end"
BEGIN TRANSACTION;

-- 1. Update tag name
UPDATE tags SET tag_name = 'front-end' WHERE tag_id = 123;

-- 2. Invalidate caches
DELETE FROM cache WHERE key LIKE '%:123:%';

-- 3. Update Elasticsearch
POST /tags/_update/123 {"doc": {"tag_name": "front-end"}}

COMMIT;
```

#### **How to Prevent Tag Spam?**

1. **Rate limiting** - Max 10 tags per content
2. **Duplicate detection** - Fuzzy matching (Levenshtein distance)
3. **Admin review** - Flag tags with sudden spike in usage
4. **Machine learning** - Detect spam patterns

---

### 📊 **Capacity Estimation**

```
Storage:
- Tags: 10M * 100 bytes = 1 GB
- Content: 1B * 500 bytes = 500 GB
- Mappings: 10B * (8+8+8) bytes = 240 GB
Total: ~750 GB (with indexes: ~2 TB)

QPS:
- Read (get tags, search): 100K QPS (90% of traffic)
- Write (add/remove tags): 10K QPS

Network:
- Read: 100K * 1KB = 100 MB/s = 800 Mbps
- Write: 10K * 1KB = 10 MB/s = 80 Mbps

Caching:
- Hot tags (top 1%): 100K tags * 100 bytes = 10 MB
- Recent searches: 1M queries * 1KB = 1 GB
Total cache: ~2 GB (easily fits in Redis)
```

---

## 🕷️ PROBLEM 2: WEB SCRAPING SYSTEM

**Problem:** Design a scalable web scraper that extracts images from URLs.

**APIs:**
```
POST /jobs -> {jobId}
GET /jobs/{jobId}/status -> {completed: 5, inProgress: 3}
GET /jobs/{jobId}/results -> {url: [images]}
```

**Architecture:**
```
Client -> API Gateway -> Job Service -> SQS Queue
                              ↓
                         Worker Pool (EC2/Lambda)
                              ↓
                      S3 (store results)
                      Redis (job status)
```

**Key Components:**
1. **Job Service:** Create scraping jobs
2. **SQS Queue:** Distributed task queue
3. **Worker Pool:** Scrape URLs in parallel
4. **S3:** Store scraped images/data
5. **Redis:** Track job progress

**Challenges:**
- Rate limiting (robots.txt)
- Duplicate URL detection (Bloom filter)
- Failed scrapes (retry with exponential backoff)
- Nested URLs (BFS traversal with depth limit)

---

## 📄 PROBLEM 3: GOOGLE DOCS CLONE

**Requirements:**
- Real-time collaborative editing
- Conflict resolution
- Version history

**Key Technologies:**
- **WebSockets** for real-time sync
- **Operational Transformation (OT)** or **CRDT** for conflict resolution
- **Event sourcing** for version history

**Architecture:**
```
Client (Editor) <-> WebSocket Server <-> Pub/Sub (Redis)
                         ↓
                    Database (MongoDB)
                    Version Store (S3)
```

---

## 🎯 KEY TAKEAWAYS

**What Interviewers Look For:**
1. ✅ **Requirements gathering** - Ask clarifying questions
2. ✅ **API design first** - Start with APIs before architecture
3. ✅ **Database schema** - Justify SQL vs NoSQL
4. ✅ **Scalability** - Caching, sharding, load balancing
5. ✅ **Trade-offs** - Discuss alternatives and why you chose one
6. ✅ **Bottlenecks** - Identify and solve bottlenecks
7. ✅ **Numbers** - Back-of-envelope calculations

**Common Mistakes:**
1. ❌ Jumping to architecture without requirements
2. ❌ Not designing APIs
3. ❌ Ignoring database design
4. ❌ Over-engineering (adding ML, blockchain unnecessarily)
5. ❌ No numbers/estimates
6. ❌ Not discussing trade-offs

---

**Next:** [05_Values_Behavioral_Round.md](./05_Values_Behavioral_Round.md)
**Back to:** [README.md](./README.md)
