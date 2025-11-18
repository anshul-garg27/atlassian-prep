# 🎯 KARAT SCREENING ROUND - Complete Guide

**Duration:** 60 minutes
**Format:** 20 min System Design Rapid Fire + 40 min DSA Coding
**Difficulty:** Medium
**Can Retry:** Yes (One free retry if you fail)

---

## 📋 Round Structure

```
┌─────────────────────────────────────────────────┐
│ PART 1: SYSTEM DESIGN RAPID FIRE (20 minutes)  │
│ ├─ 5 scenario-based questions                  │
│ ├─ ~4 minutes per question                     │
│ └─ Focus: Quick thinking & trade-offs          │
├─────────────────────────────────────────────────┤
│ PART 2: DSA CODING (40 minutes)                │
│ ├─ 1-2 Medium level problems                   │
│ ├─ Must pass all test cases                    │
│ └─ Follow-up questions expected                │
└─────────────────────────────────────────────────┘
```

---

## 🔥 PART 1: SYSTEM DESIGN RAPID FIRE QUESTIONS

### Question Bank (Most Frequently Asked)

---

### ⭐⭐⭐ **Q1: Music Streaming with Consistent Hashing**

**Problem Statement:**
> You're working on a music streaming and uploading service. The system uses consistent hashing to distribute load across servers. Load is equally distributed based on the number of files on each server. Do you see any concerns with this architecture?

**Expected Discussion Points:**

1. **Hot Files Problem**
   - Popular songs get more requests than others
   - Equal file distribution ≠ Equal load distribution
   - Some files might be accessed 1000x more than others

2. **Storage vs Load Mismatch**
   - Large files (high quality) vs small files (low quality)
   - File count doesn't reflect actual load

3. **Read vs Write Pattern**
   - Most files are read-heavy (streaming)
   - New uploads might cause rebalancing

**Optimal Answer:**
```
Concerns:
1. Hot content - Popular songs create hotspots on certain servers
2. File size variation - Equal file count doesn't mean equal load
3. Read/Write imbalance - Streaming is read-heavy

Improvements:
- Use request count or bandwidth for distribution, not file count
- Implement caching layer (CDN) for hot content
- Replicate popular content across multiple servers
- Monitor per-server load and dynamically rebalance
```

**Follow-up:** How would you improve this system?

---

### ⭐⭐⭐ **Q2: Crossword Puzzle Game - Hints Strategy**

**Problem Statement:**
> You're building a crossword puzzle gaming application that provides hints to users. What are the advantages and disadvantages of these two approaches:
> 1. Fetching hints from server on-demand
> 2. Preloading all hints on the device when game starts

**Expected Analysis:**

| Aspect | Server Fetch | Preload |
|--------|-------------|---------|
| **Network Usage** | 🟢 Low (only when needed) | 🔴 High (all hints upfront) |
| **Latency** | 🔴 Network delay per hint | 🟢 Instant access |
| **Storage** | 🟢 Minimal device storage | 🔴 More device storage |
| **Cheating** | 🟢 Can't see all hints | 🔴 Easy to extract all hints |
| **Offline Mode** | 🔴 Requires internet | 🟢 Works offline |
| **Updates** | 🟢 Easy to update hints | 🔴 Need app update |
| **Cost** | 🔴 Server API costs | 🟢 One-time download |

**Optimal Answer:**
```
Server Fetch Pros:
- Low network usage (pay-as-you-go)
- Better security (can't cheat easily)
- Easy to update hints server-side
- Analytics on which hints are used

Server Fetch Cons:
- Requires active internet connection
- Latency for each hint request
- Server costs for API calls

Preload Pros:
- Works offline
- Instant hint access (better UX)
- Fewer server API calls

Preload Cons:
- Large initial download
- More device storage needed
- Security issue - users can extract all hints
- Hard to update hints

Best Approach: Hybrid
- Preload first 3 hints for each puzzle
- Fetch additional hints on-demand
- Cache fetched hints locally
```

---

### ⭐⭐ **Q3: Large XML File Processing**

**Problem Statement:**
> Your service needs to process a very large XML file. The default hardware doesn't have enough RAM to hold the entire file in memory. Give some approaches to optimize this.

**Expected Solutions:**

**Approach 1: Streaming Parser (SAX/StAX)**
```python
# Don't load entire file into memory
# Process element by element

import xml.sax

class XMLHandler(xml.sax.ContentHandler):
    def startElement(self, name, attrs):
        # Process element
        pass

    def characters(self, content):
        # Process content
        pass

# Reads file in chunks, never loads full file
parser = xml.sax.make_parser()
parser.setContentHandler(XMLHandler())
parser.parse("large_file.xml")
```

**Approach 2: Chunking with Parallel Processing**
```
1. Split XML into logical chunks (by top-level elements)
2. Process each chunk separately
3. Use distributed processing (MapReduce)
4. Aggregate results at the end
```

**Approach 3: Database-Backed Processing**
```
1. Stream XML and store in database (insert as you read)
2. Process data in database (SQL queries)
3. Avoids keeping everything in memory
```

**Optimal Answer:**
```
Solutions:
1. Use streaming XML parser (SAX, not DOM)
   - Reads file sequentially
   - Process element-by-element
   - Memory usage: O(1) per element

2. Split file into chunks
   - Logical splitting at element boundaries
   - Parallel processing with MapReduce
   - Memory usage: O(chunk_size)

3. External memory algorithm
   - Stream to database/disk as you parse
   - Query from disk instead of RAM
   - Trade memory for I/O time

4. Upgrade hardware (if budget allows)
   - Increase RAM
   - Use specialized parsing machines

Best: Streaming parser with database backing
```

---

### ⭐⭐⭐ **Q4: Smart URL Engine - Budget Planning**

**Problem Statement:**
> You're building a smart engine service that takes URLs from users and processes them to extract useful data. You need to plan the budget for this project. What things will you take into consideration?

**Expected Discussion:**

**Capacity Estimation Parameters to Ask:**

1. **Traffic Metrics**
   - Expected number of users?
   - URLs processed per day/month?
   - Peak vs average traffic ratio?

2. **Processing Metrics**
   - Average URL processing time?
   - Size of typical webpage?
   - How much data extracted per URL?

3. **Storage Requirements**
   - Store original HTML? Just extracted data?
   - Retention period for data?
   - Growth rate?

4. **Geographic Distribution**
   - Single region or global?
   - Latency requirements?

**Budget Components:**

```
1. Compute Costs
   - Server instances for processing
   - Scaling requirements (auto-scaling)
   - CPU/Memory requirements per URL

2. Storage Costs
   - Database (RDS, DynamoDB)
   - Object storage (S3) for raw HTML
   - Backup and archival

3. Network Costs
   - Bandwidth for fetching URLs
   - Data transfer between services
   - CDN if caching results

4. Third-party Costs
   - ML model API calls (if using external)
   - Proxy services (to avoid IP blocking)
   - Monitoring and logging tools

5. Development & Maintenance
   - Engineering hours
   - DevOps and monitoring
   - On-call support
```

**Sample Calculation:**
```
Assumptions:
- 1M URLs/day
- Average processing: 5 seconds/URL
- Data extracted: 10KB/URL

Compute:
- Need: (1M URLs * 5 sec) / (24 * 3600) = ~58 parallel workers
- Cost: 60 EC2 instances * $0.1/hour * 720 hours = $4,320/month

Storage:
- 1M * 10KB * 30 days = 300GB/month
- Cost: 300GB * $0.023/GB = $7/month

Network:
- Fetching 1M pages * 500KB avg = 500GB/day
- Cost: 15TB/month * $0.09/GB = $1,350/month

Total: ~$5,700/month
```

---

### ⭐⭐⭐ **Q5: Social Media App - Scaling Internationally**

**Problem Statement:**
> You have a social media app for college students that's successfully running in the US. How would you scale it to release worldwide?

**Expected Discussion:**

**Technical Challenges:**

1. **Latency & Regional Distribution**
```
Challenge: Users in Asia accessing US servers = High latency

Solution:
- Deploy to multiple AWS/GCP regions
- Route users to nearest region (GeoDNS)
- CDN for static content (images, videos)
- Edge caching for frequently accessed data
```

2. **Data Residency & Compliance**
```
Challenge: GDPR (Europe), data localization laws

Solution:
- Store EU user data in EU region
- Implement data export/deletion APIs
- Privacy-compliant analytics
- Per-region encryption keys
```

3. **Database Strategy**
```
Challenge: Global data consistency vs availability

Options:
A. Multi-region database with replication
   - Write to primary, replicate globally
   - Eventual consistency for reads

B. Sharding by geography
   - US users → US database
   - EU users → EU database
   - Cross-region queries when needed

C. Hybrid approach
   - User data sharded by region
   - Global data (trending posts) replicated everywhere
```

4. **Content Moderation & Localization**
```
- Multiple languages (i18n)
- Cultural sensitivity (content guidelines vary)
- Local regulations (censorship in some countries)
- Time zones for notifications
```

5. **Payment & Currency**
```
- Multiple payment gateways
- Currency conversion
- Tax compliance per country
```

**Optimal Answer:**
```
Scaling Strategy:

1. Infrastructure:
   - Deploy to 3-5 major regions (US-East, EU-West, Asia-Pacific)
   - Use CDN for static assets
   - GeoDNS for intelligent routing

2. Data Strategy:
   - Shard user data by region
   - Replicate global content (trending) with eventual consistency
   - Local caching for frequently accessed data

3. Compliance:
   - GDPR compliance for Europe
   - Data residency laws for China, Russia
   - Privacy policies per region

4. Application:
   - Internationalization (i18n) for 10+ languages
   - Localized content moderation policies
   - Regional payment gateways

5. Monitoring:
   - Per-region performance metrics
   - Multi-region alerting
   - Cost optimization per region

Rollout:
Phase 1: Canada, UK, Australia (similar regulations)
Phase 2: Europe (GDPR compliance)
Phase 3: Asia-Pacific
Phase 4: Rest of world
```

---

## 💻 PART 2: DSA CODING QUESTIONS

---

### ⭐⭐⭐ **DSA Q1: Text Justification / Word Wrap**

**Problem:** [LeetCode 68 - Text Justification](https://leetcode.com/problems/text-justification/)

**Atlassian Variation:**
> Given a list of words and an integer `maxLen`, wrap the words into lines separated by '-'. If line length exceeds `maxLen`, start a new line.

**Example 1:**
```python
words = ["Hello", "Sir", "Please", "Upvote", "If", "You", "Like", "My", "Post"]
maxLen = 10

Output = ["Hello-Sir", "Please", "Upvote-If", "You-Like", "My-Post"]

Explanation:
"Hello-Sir" = 5 + 1 + 3 = 9 ≤ 10 ✓
"Please" = 6 ≤ 10 ✓
"Upvote-If" = 6 + 1 + 2 = 9 ≤ 10 ✓
```

**Solution:**
```python
def word_wrap(words, maxLen):
    result = []
    current_line = []
    current_length = 0

    for word in words:
        word_len = len(word)

        # Check if adding this word exceeds maxLen
        # Need to account for dashes between words
        needed_length = current_length + word_len
        if current_line:
            needed_length += 1  # for the dash

        if needed_length <= maxLen:
            current_line.append(word)
            current_length = needed_length
        else:
            # Start new line
            result.append('-'.join(current_line))
            current_line = [word]
            current_length = word_len

    # Add last line
    if current_line:
        result.append('-'.join(current_line))

    return result

# Time: O(n) where n = number of words
# Space: O(n) for output
```

**Follow-up:** Justified text with exact length

**Problem:**
> Given sentences and `exactLen`, create lines of exactly `exactLen` by distributing extra spaces evenly. Last line doesn't need padding.

**Example:**
```python
sentences = [
    "The day began as still as the",
    "night abruptly lighted with",
    "brilliant flame"
]
exactLen = 24

Output = [
    "The--day--began-as-still",  # 24 chars
    "as--the--night--abruptly",  # 24 chars
    "lighted--with--brilliant",  # 24 chars
    "flame"                       # No padding (last line)
]
```

**Solution:**
```python
def justify_text(sentences, exactLen):
    # First, extract all words
    words = []
    for sentence in sentences:
        words.extend(sentence.split())

    result = []
    current_line_words = []
    current_length = 0

    for word in words:
        needed = current_length + len(word)
        if current_line_words:
            needed += 1  # space/dash

        if needed <= exactLen:
            current_line_words.append(word)
            current_length = needed
        else:
            # Justify current line
            line = justify_line(current_line_words, exactLen)
            result.append(line)

            current_line_words = [word]
            current_length = len(word)

    # Last line - no justification
    if current_line_words:
        result.append('-'.join(current_line_words))

    return result

def justify_line(words, exactLen):
    if len(words) == 1:
        # Single word - no padding
        return words[0]

    # Calculate total word length
    total_word_len = sum(len(w) for w in words)
    total_spaces = exactLen - total_word_len
    gaps = len(words) - 1

    # Distribute spaces evenly
    spaces_per_gap = total_spaces // gaps
    extra_spaces = total_spaces % gaps

    result = []
    for i, word in enumerate(words):
        result.append(word)
        if i < len(words) - 1:  # Not last word
            # Add spaces
            result.append('-' * spaces_per_gap)
            if i < extra_spaces:
                result.append('-')

    return ''.join(result)

# Time: O(n) where n = total words
# Space: O(n)
```

**Test Cases:**
```python
# Test 1
assert word_wrap(["Hello", "World"], 10) == ["Hello", "World"]

# Test 2
assert word_wrap(["a", "b", "c"], 3) == ["a-b", "c"]

# Test 3
assert word_wrap(["ThisIsALongWord"], 5) == ["ThisIsALongWord"]  # Exceeds maxLen

# Edge cases to discuss:
# - What if single word > maxLen?
# - Empty input?
# - maxLen = 0?
```

---

### ⭐⭐ **DSA Q2: Find Words That Can Be Formed**

**Problem:** [LeetCode 1160](https://leetcode.com/problems/find-words-that-can-be-formed-by-characters/)

**Atlassian Variation:**
> Given a dictionary of words and a word with letters jumbled, check if any word in the dictionary can be formed from the jumbled letters.

**Example:**
```python
words = ["cat", "dada", "dog", "baby"]
jumbled = "ctay"

Output: "cat"  # Can form "cat" from "ctay"

jumbled = "dad"
Output: -1  # Cannot form any word
```

**Solution:**
```python
from collections import Counter

def find_formable_word(words, jumbled):
    jumbled_count = Counter(jumbled)

    for word in words:
        word_count = Counter(word)

        # Check if all characters in word are available
        if all(word_count[ch] <= jumbled_count[ch] for ch in word_count):
            return word

    return -1

# Time: O(n * m) where n = len(words), m = avg word length
# Space: O(k) where k = alphabet size (26)

# Better approach using Counter subtraction
def find_formable_word_v2(words, jumbled):
    jumbled_count = Counter(jumbled)

    for word in words:
        word_count = Counter(word)

        # Try subtracting - if any negative, not possible
        remaining = jumbled_count.copy()
        remaining.subtract(word_count)

        if all(count >= 0 for count in remaining.values()):
            return word

    return -1
```

**Follow-up:** Return ALL formable words, not just first one

```python
def find_all_formable_words(words, jumbled):
    jumbled_count = Counter(jumbled)
    result = []

    for word in words:
        word_count = Counter(word)
        if all(word_count[ch] <= jumbled_count[ch] for ch in word_count):
            result.append(word)

    return result
```

---

### ⭐⭐ **DSA Q3: Badge In/Out Violations**

**Problem:**
> You have two lists:
> - `entry`: timestamp-sorted list of names who badged IN
> - `exit`: timestamp-sorted list of names who badged OUT
>
> Find people who forgot to badge in OR forgot to badge out.

**Example:**
```python
entry = ["Alice", "Bob", "Alice", "Charlie"]
exit = ["Alice", "Alice", "Bob"]

Output: {
    "forgot_badge_in": ["Alice"],   # Exited but never entered first time
    "forgot_badge_out": ["Charlie"]  # Entered but never exited
}
```

**Solution:**
```python
from collections import defaultdict

def find_badge_violations(entry, exit):
    # Track state: 0 = outside, 1 = inside
    person_state = defaultdict(int)  # 0 by default

    forgot_in = set()
    forgot_out = set()

    entry_idx = 0
    exit_idx = 0

    # Process in chronological order
    # Since both are timestamp sorted, we need to merge

    # Simplified: Process all entries, then exits
    for person in entry:
        if person_state[person] == 1:
            # Already inside - forgot to badge out last time
            forgot_out.add(person)
        person_state[person] = 1  # Now inside

    for person in exit:
        if person_state[person] == 0:
            # Outside, but exiting - forgot to badge in
            forgot_in.add(person)
        person_state[person] = 0  # Now outside

    # After all events, anyone still inside forgot to badge out
    for person, state in person_state.items():
        if state == 1:
            forgot_out.add(person)

    return {
        "forgot_badge_in": list(forgot_in),
        "forgot_badge_out": list(forgot_out)
    }

# Time: O(n + m) where n = len(entry), m = len(exit)
# Space: O(unique people)
```

**Better Solution with Timestamps:**
```python
def find_violations_with_time(entries, exits):
    # entries = [(timestamp, name), ...]
    # exits = [(timestamp, name), ...]

    # Merge both lists and sort by timestamp
    events = []
    for ts, name in entries:
        events.append((ts, name, 'entry'))
    for ts, name in exits:
        events.append((ts, name, 'exit'))

    events.sort()  # Sort by timestamp

    person_state = {}
    forgot_in = set()
    forgot_out = set()

    for ts, name, event_type in events:
        if event_type == 'entry':
            if name in person_state and person_state[name] == 'inside':
                forgot_out.add(name)
            person_state[name] = 'inside'
        else:  # exit
            if name not in person_state or person_state[name] == 'outside':
                forgot_in.add(name)
            person_state[name] = 'outside'

    # Check final states
    for name, state in person_state.items():
        if state == 'inside':
            forgot_out.add(name)

    return list(forgot_in), list(forgot_out)
```

---

### ⭐⭐ **DSA Q4: Robot Parts Assembly**

**Problem:**
> Given available parts and robot requirements, return which robots can be fully built.

**Example:**
```python
parts = [
    "Rosie_claw", "Rosie_sensors", "Rosie_case", "Rosie_wheels",
    "Dustie_case", "Dustie_case", "Dustie_case", "Dustie_arms",
    "Dustie_speaker",
    "Optimus_sensors", "Optimus_speaker", "Optimus_case",
    "Optimus_wheels", "Optimus_wheels",
    "Rust_sensors", "Rust_case", "Rust_claw", "Rust_legs"
]

requirements = {
    "Rosie": ["claw", "sensors", "case", "wheels"],
    "Dustie": ["case", "arms", "speaker"],
    "Optimus": ["sensors", "speaker", "case", "wheels"],
    "Rust": ["sensors", "case", "claw", "legs"]
}

Output: ["Rosie", "Dustie", "Optimus", "Rust"]
```

**Solution:**
```python
from collections import Counter

def find_buildable_robots(parts, requirements):
    # Count available parts per robot
    available = {}
    for part in parts:
        robot_name, part_name = part.split('_')
        if robot_name not in available:
            available[robot_name] = Counter()
        available[robot_name][part_name] += 1

    buildable = []
    for robot, needed_parts in requirements.items():
        if robot not in available:
            continue

        # Check if all required parts are available
        needed_count = Counter(needed_parts)
        can_build = True

        for part, count in needed_count.items():
            if available[robot][part] < count:
                can_build = False
                break

        if can_build:
            buildable.append(robot)

    return buildable

# Time: O(p + r*k) where p=parts, r=robots, k=parts per robot
# Space: O(p + r)
```

---

### ⭐ **DSA Q5: Delivery Cart Routes (Graph)**

**Problem:**
> Given directed paths that carts take, identify all start locations and their possible end locations.

**Example:**
```python
paths = [
    ["A", "B"], ["A", "C"],
    ["B", "K"], ["C", "K"], ["C", "G"],
    ["E", "F"], ["E", "L"],
    ["F", "G"],
    ["J", "M"],
    ["G", "H"], ["G", "I"]
]

"""
Graph:
   A          E      J
  / \        / \      \
 B   C      F   L      M
  \ / \    /
   K   G
      / \
     H   I
"""

Output: {
    "A": ["K", "H", "I"],
    "E": ["H", "L", "I"],
    "J": ["M"]
}
```

**Solution:**
```python
from collections import defaultdict, deque

def find_all_destinations(paths):
    # Build adjacency list
    graph = defaultdict(list)
    all_nodes = set()
    has_incoming = set()

    for src, dest in paths:
        graph[src].append(dest)
        all_nodes.add(src)
        all_nodes.add(dest)
        has_incoming.add(dest)

    # Find start nodes (no incoming edges)
    start_nodes = all_nodes - has_incoming

    result = {}

    for start in start_nodes:
        # BFS to find all reachable destinations
        destinations = set()
        queue = deque([start])
        visited = {start}

        while queue:
            node = queue.popleft()

            # If no outgoing edges, it's a destination
            if node not in graph:
                destinations.add(node)
            else:
                for neighbor in graph[node]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)

        result[start] = sorted(destinations)

    return result

# Time: O(V + E) for BFS from each start node
# Space: O(V + E) for graph storage
```

---

## 🎯 Key Takeaways for Karat Round

### ✅ Success Tips

1. **System Design Rapid Fire**
   - Ask clarifying questions (even if time-limited)
   - Think about trade-offs (not just one answer)
   - Consider scale, cost, and latency
   - Use real-world examples

2. **DSA Coding**
   - MUST pass all test cases
   - Clean, readable code
   - Handle edge cases
   - Explain time/space complexity
   - Be ready for follow-ups

3. **Time Management**
   - Don't spend > 5 min per SD question
   - If stuck on DSA, ask for hints
   - Test your code thoroughly

### ❌ Common Mistakes

1. **System Design**
   - ❌ Not asking clarifying questions
   - ❌ Giving only one solution without alternatives
   - ❌ Ignoring scale/cost considerations

2. **Coding**
   - ❌ Not testing code before submitting
   - ❌ Missing edge cases (empty input, single element)
   - ❌ Poor variable naming
   - ❌ Not explaining approach first

### 🎓 Preparation Strategy

**Week 1-2: System Design**
- [ ] Read "Designing Data-Intensive Applications"
- [ ] Practice explaining trade-offs verbally
- [ ] Study common patterns: caching, sharding, replication

**Week 1-2: DSA**
- [ ] Master these patterns:
  - Two pointers
  - HashMap/Counter
  - Greedy algorithms
  - Basic graph traversal (BFS)
- [ ] Practice 20 medium LeetCode problems
- [ ] Focus on string manipulation

**Mock Practice:**
- [ ] 5 rapid-fire system design questions (20 min total)
- [ ] 2 DSA problems (40 min total)
- [ ] Simulate real pressure

---

## 📚 Additional Practice Problems

### System Design Rapid Fire

1. Design URL shortener - what are the scaling concerns?
2. Video streaming service - caching strategy?
3. Ride-sharing app - driver matching algorithm considerations?
4. E-commerce - inventory management at scale?
5. Chat application - message delivery guarantees?

### DSA Problems (Similar Difficulty)

1. [LeetCode 49 - Group Anagrams](https://leetcode.com/problems/group-anagrams/)
2. [LeetCode 56 - Merge Intervals](https://leetcode.com/problems/merge-intervals/)
3. [LeetCode 271 - Encode and Decode Strings](https://leetcode.com/problems/encode-and-decode-strings/)
4. [LeetCode 347 - Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/)

---

**Next:** [02_Data_Structures_Round.md](./02_Data_Structures_Round.md) - Deep dive into pure DSA round

**Back to:** [README.md](./README.md)
