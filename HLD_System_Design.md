
# High-Level Design (HLD) / System Design - Atlassian Interview Questions

This document covers large-scale system design problems. Atlassian focuses heavily on **scalability**, **reliability**, **APIs**, and **data models**.

---

## Karat Screening Round (Rapid Fire System Design)
**Format:** 5 theoretical system design questions + 1-2 coding questions
**Duration:** ~1 hour
**Expected Performance:** Solve 4/5 design questions + 1.5 coding questions (first fully working, second partial with correct approach)

### System Design Questions Format
*   **Time Allocation:** 5 minutes per question
*   **Expected Response:** Provide as many points as possible for each question
*   **Common Topics:**
    *   Concerns with Consistent Hashing for distributed systems
    *   Handling large files that cannot fit on a single machine
    *   Scaling backend from single country to international
    *   Pros/cons of preloading vs loading from server (e.g., game hints - text/image/video)
    *   Latency improvement strategies (caching, CDN, DB indexes, etc.)

### Tips
*   Be prepared with a mental checklist of common system design concepts:
    *   Caching (Redis, Memcached)
    *   CDN for static content
    *   Database indexing
    *   Load balancing
    *   Sharding/Partitioning
    *   Replication
    *   Message Queues
    *   Rate Limiting
*   Answer quickly and concisely; don't go too deep in 5 minutes
*   HR will share a format/template beforehand

---

## 1. Tagging Management Service
**Frequency:** Very High
**Core Concept:** High Read/Write Throughput, Search

### Problem Description
Design a centralized Tagging Service for all Atlassian products (Jira, Confluence, Bitbucket).
*   **Features:**
    *   Add/Remove tags from entities (issues, pages).
    *   Search for entities by tag.
    *   View popular tags (Trending).
*   **Scale:** Billions of entities, high read traffic.

### Key Challenges & Analysis
1.  **Data Model:**
    *   Relational (SQL) vs NoSQL?
    *   Many-to-Many relationship: `(EntityID, TagID)`.
    *   NoSQL (Cassandra/DynamoDB) is often preferred for scale, storing `Tag -> List<EntityID>` and `EntityID -> List<Tag>` (Materialized Views) for fast lookups.
2.  **Search & Autocomplete:**
    *   Use **Elasticsearch** or **Solr** for fuzzy search and autocomplete capabilities.
3.  **Trending Tags:**
    *   Real-time stream processing (Kafka + Flink/Spark) or batch processing to calculate top tags.
    *   Approximate counting (Count-Min Sketch) for "Heavy Hitters".

---

## 2. Content Popularity / "Like" System
**Frequency:** High
**Core Concept:** High Write Throughput, Aggregation

### Problem Description
Design a system to track likes/views/votes for content.
*   **Features:**
    *   User clicks "Like".
    *   Show "Total Likes" count.
    *   Show "Most Liked" content (Leaderboard).

**Common Variations:**
*   **Top Confluence Feed:** Find top feeds based on multiple signals (likes, shares, views).
*   **Combined Score:** Calculate a weighted score: `Score = w1*likes + w2*shares + w3*views`.

### Key Challenges & Analysis
1.  **Write Heavy:** A popular page might get thousands of likes per second.
    *   **Batching/Buffer:** Don't write to DB on every click. Buffer in Redis/Memory and write in batches.
    *   **Sharded Counters:** If one row is a hotspot, split the counter into N rows and sum them up on read.
2.  **Consistency:**
    *   Eventual consistency is usually acceptable for "Like" counts.
3.  **Historical Data / Time-Series:**
    *   **Challenge:** Show "Most Liked Page" for current year vs. previous years without mixing data.
    *   **Solution Options:**
        *   **Cassandra Time-Series:** Store data with timestamp partitioning. Query by date range (e.g., year 2024, year 2023).
        *   **Separate Aggregations:** Daily/Monthly/Yearly rollups. Store `PageID -> LikeCount` per time bucket.
        *   **NoSQL with Composite Keys:** `(PageID, Year/Month) -> Count`.
    *   **Storage Decision:** Whether to maintain individual `viewed_user_ids` or just a count depends on requirements. Storing IDs allows deduplication and detailed analytics but costs more space.
    *   **Interviewer Preference:** For historical queries, Cassandra/DynamoDB with time-based partitioning is often preferred over relational DBs.
4.  **Multi-Signal Ranking (Likes + Shares + Views):**
    *   **Weighted Score:** `Score = w1*likes + w2*shares + w3*views` where weights can be tuned.
    *   **Real-time Leaderboard:** Use Redis Sorted Sets with score as the combined metric.
    *   **Batch Processing:** Periodically recalculate scores using Spark/Flink for more complex ranking algorithms (e.g., time decay, engagement rate).
    *   **Normalization:** Normalize each signal to prevent one metric from dominating (e.g., views are usually 10x more than likes).

---

## 3. Collaborative Editing (Google Docs / Confluence)
**Frequency:** Medium
**Core Concept:** Real-time Synchronization, Conflict Resolution

### Problem Description
Design a system where multiple users edit the same document simultaneously.

### Key Challenges & Analysis
1.  **Conflict Resolution:**
    *   **Operational Transformation (OT):** The classic approach (used by Google Docs).
    *   **CRDTs (Conflict-free Replicated Data Types):** Newer, decentralized approach.
2.  **Communication:**
    *   **WebSockets:** For persistent, low-latency connection.
3.  **Consistency:**
    *   Users must see the same document state eventually.

---

## 4. Rate Limiter (HLD Focus)
**Frequency:** Medium
**Core Concept:** Distributed Systems, Latency

### Problem Description
Design a distributed Rate Limiter service used by all Atlassian APIs.

### Key Challenges & Analysis
1.  **State Sharing:** How do different server nodes know the current count for a user?
    *   **Redis (Centralized):** Fast, but can be a bottleneck/single point of failure.
    *   **Local Memory + Gossip:** approximate limiting.
2.  **Race Conditions:** Handling concurrent requests correctly.
    *   Redis `INCR` + Lua scripts.

---

## 5. HTTP Request Scheduler / Delayed Job Execution
**Frequency:** Medium-High
**Core Concept:** Job Scheduling, Delayed Execution, Reliability

### Problem Description
Design a system that allows users to schedule HTTP requests to be executed at a specified future time.

**Example:** 
*   User schedules `DELETE https://myservice.com/api/items/123` to execute on Sunday at 1:00 AM.
*   System must execute the request exactly at the scheduled time.

### Functional Requirements
1.  **Schedule API:** Provide an interface to schedule HTTP requests with:
    *   HTTP method (GET, POST, DELETE, etc.)
    *   URL
    *   Headers, body (optional)
    *   Execution time (timestamp)
2.  **Execute Requests:** Execute the HTTP request at the specified time.
3.  **Status Tracking:** Allow users to check status of scheduled jobs (pending, executed, failed).

### Non-Functional Requirements
1.  **Scale:** Initially 10 requests/minute, but should scale to thousands/minute.
2.  **Reliability:** System must not lose scheduled jobs even if it crashes.
3.  **Exactly-Once Execution:** Avoid duplicate execution of the same request.
4.  **Availability:** Highly available; no single point of failure.

### High-Level Architecture

**Components:**
1.  **API Gateway:** Receives scheduling requests from users.
2.  **Scheduler Service:** Manages scheduled jobs and triggers execution.
3.  **Executor Workers:** Stateless workers that execute HTTP requests.
4.  **Job Queue:** Persistent queue (e.g., RabbitMQ, AWS SQS) for pending jobs.
5.  **Database:** Stores job metadata (MySQL, PostgreSQL for ACID, or DynamoDB for scale).
6.  **Monitoring Service:** Tracks job status and retries.

**Flow:**
```
User → API Gateway → Scheduler Service → Job Queue → Executor Workers → External HTTP Service
                          ↓
                      Database (Job Status)
```

### API Design

**Schedule a Request:**
```json
POST /schedule
{
  "request": {
    "method": "DELETE",
    "url": "https://myservice.com/api/items/123",
    "headers": {"Authorization": "Bearer token"},
    "body": null
  },
  "scheduled_time": "2024-12-15T01:00:00Z",
  "timezone": "America/New_York"
}

Response:
{
  "job_id": "job-12345",
  "status": "scheduled"
}
```

**Check Job Status:**
```
GET /jobs/:job_id
Response:
{
  "job_id": "job-12345",
  "status": "executed",
  "executed_at": "2024-12-15T01:00:05Z",
  "response_code": 200
}
```

### Database Schema
```sql
CREATE TABLE scheduled_jobs (
    job_id VARCHAR(255) PRIMARY KEY,
    user_id INT,
    http_method VARCHAR(10),
    url TEXT,
    headers JSON,
    body TEXT,
    scheduled_time TIMESTAMP,
    status ENUM('pending', 'in_progress', 'executed', 'failed'),
    retry_count INT DEFAULT 0,
    executed_at TIMESTAMP NULL,
    response_code INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_scheduled_time (scheduled_time, status)
);
```

### Key Design Decisions

#### 1. Timezone Handling
**Challenge:** User in New York schedules a job for "Sunday 1:00 AM" - what timezone?

**Solutions:**
*   **Frontend:** Display timezone selector in GUI. Show user's local timezone (detected via browser).
*   **Backend:** Always store `scheduled_time` in **UTC** in the database.
*   **API:** Accept timezone in request body; convert to UTC before storing.
*   **Execution:** Execute based on UTC; log both UTC and original timezone for debugging.

**Example:**
*   User input: "2024-12-15 01:00:00 America/New_York"
*   Stored in DB: "2024-12-15 06:00:00 UTC"
*   GUI displays: "2024-12-15 01:00:00 EST (06:00:00 UTC)"

#### 2. How Scheduler Works
**Option A: Polling (Simple, works for small scale)**
*   Every minute, a cron job queries the database:
    ```sql
    SELECT * FROM scheduled_jobs 
    WHERE status = 'pending' 
    AND scheduled_time <= NOW() 
    LIMIT 1000;
    ```
*   For each job, push to Job Queue for execution.
*   Mark job status as `in_progress`.

**Option B: Delay Queue (Scalable)**
*   Use a **Delay Queue** (AWS SQS Delay, RabbitMQ Delayed Message Plugin).
*   When user schedules a job, calculate delay: `scheduled_time - now()`.
*   Push message to delay queue with the calculated delay.
*   Workers poll the queue and execute when message becomes visible.

**Option C: Time-Wheel / Priority Queue (Custom)**
*   Use a distributed time-wheel data structure (like Kafka's TimingWheel).
*   Jobs are organized into buckets by execution time.
*   Scheduler advances through buckets and executes jobs.

**Recommendation:** Start with Option A (polling) for MVP, move to Option B for scale.

#### 3. Crash Recovery & Exactly-Once Execution
**Challenge:** What if the system crashes after marking a job as `in_progress` but before executing it?

**Solution: Idempotency & Status Tracking**
1.  **Idempotent Job IDs:** Generate unique `job_id` (UUID). Store in DB before execution.
2.  **Atomic State Transitions:**
    *   Before execution: `UPDATE scheduled_jobs SET status = 'in_progress' WHERE job_id = ? AND status = 'pending'`.
    *   Use database transactions to ensure only one worker picks up the job.
3.  **Heartbeat Mechanism:**
    *   Worker updates `last_heartbeat` field every 10 seconds during execution.
    *   Monitoring service checks for stale jobs (status = 'in_progress' but `last_heartbeat` > 5 minutes ago).
    *   Stale jobs are re-queued with `retry_count++`.
4.  **Retry Logic:**
    *   If HTTP request fails (network error, 5xx response), retry up to 3 times.
    *   Exponential backoff: 1 min, 5 min, 15 min.
5.  **Deduplication:**
    *   Store `job_id` in Redis with TTL = 24 hours after execution.
    *   Before executing, check Redis: `if exists(job_id) then skip`.

#### 4. Handling Duplicate Requests (System Restart)
**Scenario:** System crashes and restarts. Same job is re-queued.

**Prevention:**
*   Use **database transactions** with optimistic locking:
    ```sql
    UPDATE scheduled_jobs 
    SET status = 'in_progress', version = version + 1 
    WHERE job_id = ? AND status = 'pending' AND version = ?;
    ```
*   Only the worker that successfully updates the row executes the job.
*   Other workers see 0 rows affected and skip.

### Scalability Considerations
1.  **Horizontal Scaling:**
    *   Add more Executor Workers (stateless).
    *   Add more Scheduler instances (coordinate via leader election using ZooKeeper/etcd).
2.  **Database Sharding:**
    *   Shard by `scheduled_time` range (e.g., January jobs on DB1, February on DB2).
    *   Or shard by `user_id` if jobs are user-specific.
3.  **Job Queue Partitioning:**
    *   Partition queue by execution time buckets (e.g., next 1 hour, next 24 hours, future).
4.  **Rate Limiting:**
    *   If external service has rate limits, apply rate limiter before execution.

### Monitoring & Observability
1.  **Metrics:**
    *   Number of jobs scheduled per minute.
    *   Average execution delay (how late were jobs executed?).
    *   Failed jobs count.
2.  **Alerting:**
    *   Alert if execution delay > 5 minutes.
    *   Alert if failed jobs > 10% of total.
3.  **Logs:**
    *   Log every job execution with `job_id`, `scheduled_time`, `executed_at`, `response_code`.

### Interviewer Follow-Up Questions (Common)
1.  **How does frontend interact with backend?**
    *   REST API with JSON request/response.
    *   Frontend sends timezone; backend converts to UTC.
2.  **How will users know the GUI timezone?**
    *   Display detected timezone prominently in UI.
    *   Allow users to override if needed.
3.  **How to handle system crash and restart?**
    *   Database transactions + heartbeat mechanism.
    *   Idempotency with `job_id`.
4.  **What if scheduled time is in the past?**
    *   Validate in API: reject if `scheduled_time < now()`.
    *   Or execute immediately if past due by < 5 minutes.
5.  **How to cancel a scheduled job?**
    *   Provide `DELETE /jobs/:job_id` endpoint.
    *   Mark status as `cancelled` in DB.

### Interviewer Tips (Principal/Senior Level)
*   This is a **P5-level question**; expectations are high.
*   Discuss **trade-offs** extensively (polling vs delay queue, SQL vs NoSQL).
*   Mention **failure modes** and how to handle them (worker crashes, DB failures, network partitions).
*   Talk about **observability** (metrics, logging, alerting).
*   Consider **cost optimization** (minimize DB queries, use caching).

---

## 6. Web Scraper
**Frequency:** Medium
**Core Concept:** Job Scheduling, Async Processing

### Problem Description
Design a system that takes a list of URLs, scrapes them, and extracts images/metadata.

### Key Challenges & Analysis
1.  **Architecture:**
    *   **Scheduler:** Manages the crawl frontier (URLs to visit).
    *   **Workers:** Stateless nodes that fetch and parse pages.
    *   **Queue:** Kafka/SQS to distribute URLs to workers.
2.  **Politeness:** Don't DDOS the target sites. (Rate limiting per domain).
3.  **Deduping:** Avoid scraping the same URL multiple times (Bloom Filter / Redis).

---

## 6. File Storage / Google Drive Clone
**Frequency:** Low-Medium
**Core Concept:** Binary Data vs Metadata

### Problem Description
Design a file storage system. Support upload, download, and search.

### Key Challenges & Analysis
1.  **Storage Split:**
    *   **Metadata DB:** (Name, Size, Owner, Folder structure) -> SQL/NoSQL.
    *   **Object Storage:** (Actual file content) -> S3/Blob Store.
2.  **Uploads:**
    *   Chunking large files.
    *   Resumable uploads.

---

## 7. Notification System
**Frequency:** Low
**Core Concept:** Fan-out, Message Queues

### Problem Description
Design a system to send notifications (Email, Push, In-app) to users.

### Key Challenges & Analysis
1.  **Fan-out:** One event (e.g., "Server Down") might trigger 10,000 emails.
2.  **Priority:** OTP SMS > Marketing Email.
3.  **User Preferences:** Don't send if user opted out.

---

## 8. Collaborative Board (Jira / Trello)
**Frequency:** Medium
**Core Concept:** Real-time State Management, Conflict Resolution

### Problem Description
Design a collaborative board system (like Jira or Trello) where users can:
*   Create boards with columns (e.g., "To Do", "In Progress", "Done").
*   Add cards/tasks to columns.
*   Move cards between columns.
*   Multiple users collaborate on the same board in real-time.

**Interview Flow:** Start with single-user workflow, then extend to multi-user collaboration.

### Key Components
1.  **Board Service:** Manages boards, columns, and cards.
2.  **User Service:** Authentication and authorization.
3.  **Real-time Sync Service:** WebSocket server for live updates.
4.  **Notification Service:** Notify users of changes (optional).

### Data Architecture
**Relational Schema:**
```sql
Boards: (board_id, name, owner_id, created_at)
Columns: (column_id, board_id, name, position)
Cards: (card_id, column_id, title, description, assignee_id, position, updated_at)
BoardMembers: (board_id, user_id, role) -- for access control
```

**NoSQL Alternative (Document Store):**
```json
{
  "board_id": "b123",
  "name": "Project X",
  "columns": [
    {
      "column_id": "c1",
      "name": "To Do",
      "cards": [
        {"card_id": "card1", "title": "Task 1", "assignee": "user123", "position": 1}
      ]
    }
  ]
}
```

### Scalability Considerations
1.  **Database:**
    *   Use **indexing** on `board_id`, `column_id`, and `updated_at`.
    *   For high-traffic boards, consider **read replicas** for card fetching.
2.  **Caching:**
    *   Cache board data in **Redis** (TTL-based or invalidate on update).
    *   Cache structure: `board:<board_id> -> JSON of entire board`.
3.  **WebSocket Scaling:**
    *   Use **Redis Pub/Sub** or **message broker (Kafka)** to broadcast updates across multiple WebSocket servers.
    *   When User A moves a card, the backend publishes the event to Redis; all WebSocket servers subscribed to that board's channel push the update to connected clients.
4.  **Sharding:**
    *   Shard boards by `board_id` to distribute load.

### Real-time Collaboration Challenges
1.  **Conflict Resolution:**
    *   **Scenario:** User A moves Card X from Column 1 to Column 2. Simultaneously, User B moves Card X from Column 1 to Column 3.
    *   **Solutions:**
        *   **Last Write Wins (LWW):** Use timestamps; the most recent update wins.
        *   **Operational Transformation (OT):** Transform operations based on the order they occurred.
        *   **CRDTs (Conflict-free Replicated Data Types):** Use data structures that can merge conflicting states.
    *   **Optimistic Locking:** Use versioning (`version` field in Cards table). If `version` doesn't match during update, reject and ask client to retry.
2.  **Ordering of Cards:**
    *   **Problem:** If cards have integer positions (1, 2, 3), moving a card requires updating all subsequent cards.
    *   **Solution: Lexorank (Fractional Indexing):**
        *   Assign each card a string position (e.g., "a", "b", "c").
        *   To insert between "a" and "b", use "a5" (lexicographically between).
        *   This avoids re-indexing the entire column.
3.  **Concurrency Control:**
    *   Use **database transactions** or **distributed locks** (Redis SETNX) to prevent race conditions when updating card positions.

### API Design
```
POST /boards                    -- Create board
GET /boards/:id                 -- Get board with all columns and cards
POST /boards/:id/columns        -- Add column
POST /boards/:id/cards          -- Add card
PATCH /cards/:id/move           -- Move card to different column/position
DELETE /cards/:id               -- Delete card
```

### Evolution: Single-User → Multi-User
1.  **Single-User (MVP):**
    *   Simple CRUD operations for boards, columns, cards.
    *   No real-time sync; user refreshes to see updates.
2.  **Multi-User (Phase 2):**
    *   Add WebSocket connection for real-time updates.
    *   Implement conflict resolution (start with Last Write Wins).
    *   Add access control (BoardMembers table).
3.  **Advanced Features:**
    *   Presence indicators (show who's viewing the board).
    *   Comments and attachments on cards.
    *   Activity log (audit trail).

### Interviewer Tips
*   Start simple (REST API, single user), then gradually add complexity.
*   Discuss trade-offs between SQL (structured, ACID) vs NoSQL (flexible, denormalized).
*   Emphasize **conflict resolution** strategies; this is a key differentiator in collaborative systems.

---

## 9. Color Picker / Favorites System
**Frequency:** Low
**Core Concept:** Social Sharing, Access Control

### Problem Description
Design a system where users can pick favorite colors, save them as lists, and share them with friends (Access Control).

### Key Challenges & Analysis
1.  **Access Control (ACL):** Validating if User A can view User B's list.
2.  **Sharing:** Email integration to share lists.
3.  **Database:** simple relational schema `User -> ColorList -> Colors`.

---

## 10. Dynamic Sprint Dashboard (Frontend System Design)
**Frequency:** Low
**Core Concept:** Reusable UI Components, Component Versioning, State Management

### Problem Description
Design a dynamic sprint dashboard (frontend architecture) where users can:
*   Add/Remove columns (e.g., "Backlog", "Scheduled", "In Progress", "Done").
*   Drag and drop entities (tasks/stories) between columns.
*   Customize the board layout.

### Key Challenges & Analysis
1.  **Reusable Components:**
    *   Tasks, Stories, Issues should all use reusable UI components.
    *   Example: A `Task` component should render the same way regardless of which column it's in.
2.  **Component Versioning:**
    *   Instead of modifying existing components, create new versions (similar to Maven versioning in backend).
    *   Benefits: Backward compatibility, rollback capability, A/B testing.
3.  **State Management:**
    *   Use React Context, Redux, or Zustand for global state (board layout, column data).
    *   Local state for individual card interactions.
4.  **Performance:**
    *   Virtual scrolling for large boards with hundreds of cards.
    *   Optimize re-renders using React.memo, useMemo, useCallback.
5.  **Drag & Drop:**
    *   Use libraries like `react-beautiful-dnd` or `dnd-kit`.
    *   Handle optimistic UI updates (update UI immediately, sync to backend asynchronously).

### Frontend Architecture Tips
*   **Component Hierarchy:** `Board -> Column -> Card`
*   **Props Drilling:** Avoid deep prop drilling; use Context API or state management library.
*   **API Design:** RESTful endpoints like `POST /boards/:id/columns`, `PATCH /cards/:id/move`.

---

## 11. Scorecard System / Performance Metrics Dashboard
**Frequency:** Low
**Core Concept:** Aggregation, Reporting, Time-Series Data

### Problem Description
Design a system to display scorecards or performance metrics for teams/users.
*   **Features:**
    *   Track various metrics (e.g., tasks completed, bugs fixed, story points).
    *   Display aggregated scores over time periods (daily, weekly, monthly).
    *   Compare performance across teams or individuals.
    *   Generate reports.

### Functional Requirements
1.  **Metric Ingestion:** Receive events/metrics from various sources (Jira, GitHub, etc.).
2.  **Aggregation:** Calculate scores based on predefined rules (e.g., `score = tasks_completed * 2 + bugs_fixed * 5`).
3.  **Query API:** Get scorecard for a user/team for a given time range.
4.  **Leaderboard:** Show top performers.

### Non-Functional Requirements
1.  **Scalability:** Handle millions of events per day.
2.  **Low Latency:** Query results within 100-200ms.
3.  **Historical Data:** Store data for at least 1 year.

### High-Level Architecture
1.  **Event Ingestion:**
    *   Use **Kafka** or **AWS Kinesis** to stream events.
    *   Events: `{user_id, metric_type, value, timestamp}`.
2.  **Stream Processing:**
    *   Use **Apache Flink** or **Spark Streaming** to:
        *   Aggregate events in real-time (e.g., sum tasks completed per user per day).
        *   Write aggregated data to a data warehouse.
3.  **Data Storage:**
    *   **Time-Series DB (InfluxDB / TimescaleDB):** For storing metric data with timestamps.
    *   **Schema:** `(user_id, metric_type, timestamp, value)`
    *   Alternatively, use **Cassandra** with time-based partitioning.
4.  **Query Service:**
    *   REST API to fetch scorecards: `GET /scorecards?user_id=123&start_date=2024-01-01&end_date=2024-01-31`
    *   Cache frequently accessed scorecards in **Redis**.
5.  **Reporting:**
    *   Batch jobs (daily/weekly) to generate pre-computed reports and store in S3 or database.

### API Design
```
POST /metrics                           -- Ingest metric event
GET /scorecards/:user_id                -- Get scorecard for user
GET /scorecards/team/:team_id           -- Get team scorecard
GET /leaderboard?period=weekly          -- Get top performers
```

### Database Design
**Time-Series Table:**
```sql
CREATE TABLE metrics (
    user_id INT,
    metric_type VARCHAR(50),
    value INT,
    timestamp TIMESTAMP,
    PRIMARY KEY (user_id, metric_type, timestamp)
);
```

**Aggregated Scorecards Table (Pre-computed):**
```sql
CREATE TABLE scorecards (
    user_id INT,
    period_start DATE,
    period_end DATE,
    total_tasks INT,
    total_bugs_fixed INT,
    total_score INT,
    PRIMARY KEY (user_id, period_start)
);
```

### Key Trade-offs
1.  **Real-time vs Batch:**
    *   Real-time: Lower latency but more complex (stream processing).
    *   Batch: Simpler, but data may be stale (e.g., updated once per hour).
2.  **Raw Events vs Aggregated:**
    *   Store raw events for flexibility (can recalculate scores with new rules).
    *   Store aggregated data for fast queries.
    *   **Hybrid Approach:** Store both; use aggregated for queries, raw for re-processing.

### Interviewer Tips
*   Start with functional requirements, then move to non-functional (scale, latency).
*   Discuss **data retention policies** (e.g., keep raw events for 30 days, aggregated data for 1 year).
*   Mention **data pipeline tools** (Kafka, Flink, Airflow).

---

## 12. Metro Station System / Transportation Network
**Frequency:** Low
**Core Concept:** Graph Modeling, Shortest Path, Procedural Design

### Problem Description
Design a system to model a metro/subway network.
*   **Features:**
    *   Add stations and routes (connections between stations).
    *   Find the shortest path between two stations.
    *   Calculate fare based on distance/number of stops.
    *   Handle different lines (e.g., Red Line, Blue Line) with transfer stations.

### Data Model
**Graph Representation:**
*   **Nodes:** Stations
*   **Edges:** Routes (connections) with weights (distance or time)

**Schema:**
```sql
Stations: (station_id, name, line_id)
Routes: (route_id, from_station_id, to_station_id, distance, time)
Lines: (line_id, name, color)
```

### Key Algorithms
1.  **Shortest Path:** Dijkstra's or A* algorithm.
2.  **Fare Calculation:** Based on number of stops or distance.
3.  **Transfer Handling:** Some stations are on multiple lines; model as separate nodes with zero-cost edges between them.

### Procedural Programming Approach
*   Focus on functions/procedures rather than OOP classes.
*   Example:
    ```python
    def add_station(name, line_id):
        # Add station to database
    
    def add_route(from_station, to_station, distance):
        # Add route to database
    
    def find_shortest_path(start_station, end_station):
        # Run Dijkstra's algorithm
        return path, total_distance
    
    def calculate_fare(path):
        # Calculate fare based on distance or stops
    ```

### Interviewer Tips
*   Discuss how to handle **bidirectional routes** (most metro lines go both ways).
*   Mention **graph traversal optimizations** (pre-compute all-pairs shortest paths using Floyd-Warshall if the network is small).
*   For large networks, consider **caching** frequently queried routes.

---
