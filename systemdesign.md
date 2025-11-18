# 4. SYSTEM DESIGN ROUNDS

## 📊 Overview
- **Duration:** 60 minutes
- **Focus:** High-level architecture, scalability
- **Depth:** Not too deep, breadth is important
- **Topics:** API design, database, caching, scaling

---

## 🎯 Commonly Asked System Design Problems

### Design #1: Web Scraping System ⭐

```
PROBLEM: Design Web Scraping System

Requirements:
1. Accept list of URLs
2. Scrape each URL and extract image URLs
3. Track job status
4. Return results

APIs to Design:
1. POST /jobs
   Request: { "urls": ["abc.com", "amazon.com"] }
   Response: { "job_id": "1234" }

2. GET /jobs/{job_id}/status
   Response: { "completed": 1, "in_progress": 1, "failed": 0 }

3. GET /jobs/{job_id}/results
   Response: {
     "https://abc.com": ["abc.com/img1.jpg", "abc.com/img2.jpg"],
     "https://amazon.com": ["amazon.com/img1.jpg"]
   }

Key Components to Design:
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  API Server │ ← Handle requests, create jobs
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Job Queue  │ ← Redis/RabbitMQ for task queue
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Workers    │ ← Multiple workers scraping URLs
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Database   │ ← Store job status & results
└─────────────┘
       │
       ▼
┌─────────────┐
│  S3/Storage │ ← Store scraped images (optional)
└─────────────┘

Discussion Points:
1. Task Queue:
   - Use message queue (Redis, RabbitMQ, SQS)
   - Job states: PENDING, IN_PROGRESS, COMPLETED, FAILED
   - Retry logic for failed URLs

2. Workers:
   - Multiple worker processes
   - Rate limiting per domain
   - Timeout handling
   - Respect robots.txt

3. Database Schema:
   jobs table:
   - job_id, created_at, total_urls, completed_urls
   
   url_tasks table:
   - task_id, job_id, url, status, result, error
   
4. Scalability:
   - Horizontal scaling of workers
   - Partition by domain
   - Caching for repeated URLs
   - CDN for serving images

5. Error Handling:
   - Invalid URLs
   - Timeout
   - Network errors
   - Rate limiting by websites

6. Monitoring:
   - Job completion rate
   - Average scraping time
   - Error rates
   - Queue depth
```

---

### Design #2: Twitter Hashtag System

```
PROBLEM: Design Twitter Hashtag System

Requirements:
1. Track hashtags in tweets
2. Get trending hashtags
3. Get tweets by hashtag
4. Real-time updates

Key Focus Areas (per interview feedback):
- API Design ⭐ Most important
- Database Optimization (Sharding, Indexing) ⭐ Critical
- Caching strategy
- Real-time processing

API Design:
1. POST /tweets
   Request: { "content": "Hello #world #tech" }
   → Extract hashtags, update counters

2. GET /hashtags/trending
   Response: [
     { "tag": "world", "count": 12500, "trend_score": 95 },
     { "tag": "tech", "count": 8900, "trend_score": 87 }
   ]

3. GET /hashtags/{tag}/tweets
   Response: { "tweets": [...], "total": 5000 }

Database Design:
tweets table:
- tweet_id, user_id, content, created_at

hashtags table:
- hashtag_id, tag, total_count, created_at

tweet_hashtags (junction):
- tweet_id, hashtag_id, created_at

hashtag_stats (time-series):
- hashtag_id, hour_bucket, count

Optimizations:

1. Indexing:
   - Index on hashtag_id for fast lookup
   - Composite index (hashtag_id, created_at) for time-range queries
   - Index on trend_score for trending page

2. Sharding Strategy:
   - Shard tweets by tweet_id (consistent hashing)
   - Replicate hashtag_stats for read scalability
   - Use Redis for hot hashtags

3. Caching:
   - Cache trending hashtags (update every 5 min)
   - Cache popular hashtag → tweets mapping
   - Use CDN for static hashtag pages

4. Real-time Processing:
   - Kafka/Kinesis for tweet stream
   - Spark Streaming for trend calculation
   - Update counters in Redis

Architecture:
┌─────────┐
│  Tweet  │
└────┬────┘
     │
     ▼
┌─────────────┐
│ Kafka Queue │ ← Real-time tweet stream
└──────┬──────┘
       │
       ├─────────────┐
       │             │
       ▼             ▼
┌─────────┐   ┌──────────────┐
│ Storage │   │ Trend Engine │ ← Calculate trends
│ Service │   └──────┬───────┘
└─────────┘          │
                     ▼
              ┌──────────────┐
              │ Redis Cache  │ ← Hot data
              └──────────────┘
```

---

### Design #3: Rate Limiting System

```
PROBLEM: Design Rate Limiter

Requirements:
- Limit requests per user/API key
- Different limits for different tiers
- Distributed system

Algorithms:
1. Token Bucket
2. Leaky Bucket
3. Fixed Window
4. Sliding Window

Implementation Focus:
- Use Redis for distributed rate limiting
- Atomic operations
- TTL for cleanup
```

---

### Design #4: URL Shortener

```
PROBLEM: Design URL Shortener (like bit.ly)

Requirements:
1. Shorten long URL
2. Redirect short URL to original
3. Analytics (click count)
4. Custom aliases

Key Discussions:
- Base62 encoding
- Collision handling
- Database design
- Caching strategy
- Scalability
```

---

# 5. CODE DESIGN ROUNDS

## 📊 Overview
- **Duration:** 60 minutes
- **Focus:** OOP design, design patterns, clean architecture
- **Expectations:** Working code with good design principles

---

## 🎯 Common Problems

### Problem #1: Friend Recommendation System

```python
"""
PROBLEM: Design Friend Recommendation System

Requirements:
- Store friendships
- Recommend friends (friends of friends)
- Find mutual friends
- Search friends

Focus on:
- Clean class design
- SOLID principles
- Efficient data structures
"""

from collections import defaultdict, deque

class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

class Friendship:
    def __init__(self, user1_id, user2_id, created_at):
        self.user1_id = user1_id
        self.user2_id = user2_id
        self.created_at = created_at

class FriendRecommendationSystem:
    def __init__(self):
        self.users = {}  # user_id -> User
        self.friendships = defaultdict(set)  # user_id -> set of friend_ids
    
    def add_user(self, user_id, name):
        if user_id not in self.users:
            self.users[user_id] = User(user_id, name)
    
    def add_friendship(self, user1_id, user2_id):
        # Bidirectional friendship
        self.friendships[user1_id].add(user2_id)
        self.friendships[user2_id].add(user1_id)
    
    def get_friends(self, user_id):
        return self.friendships.get(user_id, set())
    
    def get_mutual_friends(self, user1_id, user2_id):
        friends1 = self.friendships.get(user1_id, set())
        friends2 = self.friendships.get(user2_id, set())
        return friends1 & friends2
    
    def recommend_friends(self, user_id, limit=10):
        """
        Recommend friends based on mutual friends
        Algorithm: Friends of friends who are not already friends
        """
        if user_id not in self.friendships:
            return []
        
        current_friends = self.friendships[user_id]
        recommendations = defaultdict(int)  # candidate -> mutual friend count
        
        # For each friend, look at their friends
        for friend_id in current_friends:
            for friend_of_friend in self.friendships.get(friend_id, set()):
                # Don't recommend existing friends or self
                if friend_of_friend != user_id and friend_of_friend not in current_friends:
                    recommendations[friend_of_friend] += 1
        
        # Sort by mutual friend count
        sorted_recommendations = sorted(
            recommendations.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [user_id for user_id, count in sorted_recommendations[:limit]]
    
    def find_connection_path(self, user1_id, user2_id):
        """
        Find shortest connection path between two users (BFS)
        """
        if user1_id == user2_id:
            return [user1_id]
        
        visited = set([user1_id])
        queue = deque([(user1_id, [user1_id])])
        
        while queue:
            current_user, path = queue.popleft()
            
            for friend in self.friendships.get(current_user, set()):
                if friend == user2_id:
                    return path + [friend]
                
                if friend not in visited:
                    visited.add(friend)
                    queue.append((friend, path + [friend]))
        
        return []  # No connection found
```

---

### Problem #2: Server Load Balancer

```python
"""
PROBLEM: Design Load Balancer

Given: List of servers with latency information

Requirements:
- Select best server based on latency
- Handle server failures
- Different load balancing strategies

Focus: Clean OOP design with strategy pattern
"""

from abc import ABC, abstractmethod
import random
from typing import List

class Server:
    def __init__(self, server_id, host, latency_ms):
        self.server_id = server_id
        self.host = host
        self.latency_ms = latency_ms
        self.is_healthy = True
        self.current_load = 0

class LoadBalancingStrategy(ABC):
    @abstractmethod
    def select_server(self, servers: List[Server]) -> Server:
        pass

class RoundRobinStrategy(LoadBalancingStrategy):
    def __init__(self):
        self.current_index = 0
    
    def select_server(self, servers):
        healthy_servers = [s for s in servers if s.is_healthy]
        if not healthy_servers:
            return None
        
        server = healthy_servers[self.current_index % len(healthy_servers)]
        self.current_index += 1
        return server

class LeastLatencyStrategy(LoadBalancingStrategy):
    def select_server(self, servers):
        healthy_servers = [s for s in servers if s.is_healthy]
        if not healthy_servers:
            return None
        
        return min(healthy_servers, key=lambda s: s.latency_ms)

class LeastConnectionsStrategy(LoadBalancingStrategy):
    def select_server(self, servers):
        healthy_servers = [s for s in servers if s.is_healthy]
        if not healthy_servers:
            return None
        
        return min(healthy_servers, key=lambda s: s.current_load)

class LoadBalancer:
    def __init__(self, strategy: LoadBalancingStrategy):
        self.servers = []
        self.strategy = strategy
    
    def add_server(self, server: Server):
        self.servers.append(server)
    
    def remove_server(self, server_id):
        self.servers = [s for s in self.servers if s.server_id != server_id]
    
    def set_strategy(self, strategy: LoadBalancingStrategy):
        self.strategy = strategy
    
    def get_next_server(self) -> Server:
        return self.strategy.select_server(self.servers)
    
    def mark_server_unhealthy(self, server_id):
        for server in self.servers:
            if server.server_id == server_id:
                server.is_healthy = False
    
    def health_check(self):
        # Implement health check logic
        for server in self.servers:
            # Ping server, update is_healthy
            pass
```
