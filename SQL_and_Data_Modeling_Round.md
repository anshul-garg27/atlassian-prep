
# SQL & Data Modeling Round - Atlassian Interview Guide

This document covers the SQL and Data Modeling rounds, which are particularly common for **Data Engineering** and **Backend Engineering** roles. Some candidates have reported a dedicated SQL/Data Modeling round separate from coding rounds.

---

## Round Structure

### When This Round Occurs
*   **Data Engineering Roles:** Almost always included
*   **Backend Roles (P4+):** Sometimes included as a separate round
*   **Duration:** 45-60 minutes
*   **Format:** Two phases typically
    1. SQL questions (3-5 questions)
    2. Data modeling exercise

### Interviewer Style
Candidates report this as one of the **best rounds** with very knowledgeable and supportive interviewers who guide you through the problem.

---

## Phase 1: SQL Questions

### Difficulty Distribution
*   **Mix of Medium and Hard problems**
*   Questions are often **inter-related** (building on previous queries)
*   Focus on real-world scenarios (not just textbook queries)

### Common SQL Topics

#### 1. Window Functions
**Most Frequently Asked**

**Common Problems:**
*   Calculate running totals
*   Rank employees by salary within departments
*   Find first/last occurrence of an event per user
*   Moving averages

**Example:**
```sql
-- Find the 2nd highest salary in each department
SELECT department_id, salary
FROM (
    SELECT department_id, salary,
           ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) as rn
    FROM employees
) ranked
WHERE rn = 2;
```

**Key Functions to Know:**
*   `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`
*   `LEAD()`, `LAG()`
*   `FIRST_VALUE()`, `LAST_VALUE()`
*   `SUM() OVER()`, `AVG() OVER()`

---

#### 2. Joins (All Types)
**Expected to know all join types and when to use them**

**Common Scenarios:**
*   **INNER JOIN:** Standard joining of related tables
*   **LEFT JOIN:** Include all records from left table even if no match
*   **CROSS JOIN:** Cartesian product (e.g., generate all combinations)
*   **SELF JOIN:** Joining table to itself (e.g., employee-manager relationships)

**Example (CROSS JOIN):**
```sql
-- Generate all possible pairs of products for recommendation
SELECT p1.product_id as product_1, p2.product_id as product_2
FROM products p1
CROSS JOIN products p2
WHERE p1.product_id < p2.product_id;
```

---

#### 3. Date/Time Functions
**Very Common in Real-World Queries**

**Typical Problems:**
*   Calculate days between events
*   Group by month/quarter/year
*   Find active users in last 30 days
*   Time zone conversions

**Example:**
```sql
-- Find users who logged in at least once in each of the last 3 months
SELECT user_id
FROM logins
WHERE login_date >= DATE_SUB(CURDATE(), INTERVAL 3 MONTH)
GROUP BY user_id
HAVING COUNT(DISTINCT DATE_FORMAT(login_date, '%Y-%m')) = 3;
```

**Key Functions:**
*   `DATE_ADD()`, `DATE_SUB()`, `DATEDIFF()`
*   `DATE_FORMAT()`, `YEAR()`, `MONTH()`, `QUARTER()`
*   `NOW()`, `CURDATE()`, `TIMESTAMP()`

---

#### 4. Aggregations & GROUP BY
**Must Handle Complex Grouping**

**Common Patterns:**
*   Group by multiple columns
*   Aggregations with HAVING clause
*   Nested aggregations (subqueries)

**Example:**
```sql
-- Find departments where average salary > 50000 and employee count > 10
SELECT department_id, AVG(salary) as avg_sal, COUNT(*) as emp_count
FROM employees
GROUP BY department_id
HAVING AVG(salary) > 50000 AND COUNT(*) > 10;
```

---

#### 5. Subqueries & CTEs (Common Table Expressions)
**Expected for Complex Queries**

**When to Use:**
*   Break down complex logic into readable parts
*   Reuse intermediate results
*   Recursive queries (organizational hierarchies)

**Example (CTE):**
```sql
WITH MonthlyRevenue AS (
    SELECT 
        DATE_FORMAT(order_date, '%Y-%m') as month,
        SUM(amount) as revenue
    FROM orders
    GROUP BY DATE_FORMAT(order_date, '%Y-%m')
)
SELECT month, revenue,
       revenue - LAG(revenue) OVER (ORDER BY month) as growth
FROM MonthlyRevenue;
```

---

### Inter-Related Questions Pattern
Atlassian often gives a series of questions that build on each other:

**Example Series:**
1. Query 1: Find all users who made a purchase in January 2024.
2. Query 2: From those users, find who purchased Product X.
3. Query 3: Calculate the average order value for those specific users.
4. Query 4: Compare this average to the overall average and find percentage difference.

---

## Phase 2: Data Modeling

### What to Expect
*   Given a real-world scenario (e.g., e-commerce, social network, project management)
*   Design the **database schema** (tables, columns, relationships)
*   Discuss **normalization** and **denormalization** trade-offs
*   Write queries to demonstrate the schema works

### Common Scenarios

#### 1. Confluence/Jira-like System
**Design schema for:**
*   Pages/Issues with tags
*   User permissions
*   Comments and attachments
*   Activity tracking (likes, views)

**Example Schema:**
```sql
Users: (user_id, username, email, created_at)
Pages: (page_id, title, content, author_id, space_id, created_at, updated_at)
Tags: (tag_id, name)
PageTags: (page_id, tag_id)  -- Many-to-Many
Comments: (comment_id, page_id, user_id, content, created_at)
Likes: (like_id, page_id, user_id, created_at)
PageViews: (view_id, page_id, user_id, viewed_at)
```

---

#### 2. E-Commerce System
**Design schema for:**
*   Products, Orders, Customers
*   Inventory management
*   Shipping and payments

---

#### 3. Social Network
**Design schema for:**
*   Users, Posts, Comments
*   Friend relationships (bidirectional)
*   Likes and shares

---

### Key Questions to Address in Data Modeling

1.  **Normalization:**
    *   Is the schema in 3NF (Third Normal Form)?
    *   Any redundant data?
    *   Trade-off: Normalized (integrity) vs Denormalized (performance)

2.  **Indexes:**
    *   Which columns should be indexed?
    *   Primary keys, foreign keys, and frequently queried columns

3.  **Scalability:**
    *   How will this schema handle millions of records?
    *   Partitioning strategies (e.g., by date, by user_id)

4.  **Constraints:**
    *   Foreign key constraints
    *   Unique constraints
    *   Check constraints (e.g., `rating >= 1 AND rating <= 5`)

5.  **Sample Queries:**
    *   Be prepared to write 2-3 queries demonstrating the schema
    *   Example: "Get all pages tagged with 'backend' that have more than 10 likes"

---

## Theoretical Concepts (Asked Frequently)

### 1. OLTP vs OLAP
*   **OLTP (Online Transaction Processing):**
    *   High volume of short transactions (INSERT, UPDATE, DELETE)
    *   Examples: Banking systems, e-commerce checkout
    *   Focus: Low latency, ACID compliance
    *   Database: MySQL, PostgreSQL

*   **OLAP (Online Analytical Processing):**
    *   Complex queries, aggregations, reporting
    *   Examples: Data warehouses, BI tools
    *   Focus: Fast reads, large scans
    *   Database: Redshift, BigQuery, Snowflake

**When to Use:**
*   Use OLTP for transactional data (user actions, orders)
*   Use OLAP for analytics (reports, dashboards)
*   Often: ETL pipeline from OLTP → OLAP

---

### 2. Snowflake vs Star Schema
*   **Star Schema:**
    *   Central **Fact Table** surrounded by **Dimension Tables**
    *   Denormalized dimensions for fast queries
    *   Example: Sales (Fact) with Product, Customer, Time (Dimensions)

*   **Snowflake Schema:**
    *   Normalized version of Star Schema
    *   Dimensions are further normalized into sub-dimensions
    *   Saves space but increases join complexity

**When to Use:**
*   **Star:** Simpler queries, better for most data warehouses
*   **Snowflake:** When storage is expensive, or dimensions are very large

---

### 3. Indexing Strategies
*   **B-Tree Index:** Default for most databases, good for range queries
*   **Hash Index:** Fast for equality checks, not for ranges
*   **Composite Index:** Index on multiple columns (order matters!)
*   **Covering Index:** Index contains all columns needed for a query (no table lookup)

**Example:**
```sql
-- Composite index for queries like: WHERE user_id = X AND created_at > Y
CREATE INDEX idx_user_created ON orders(user_id, created_at);
```

---

### 4. Normalization (1NF, 2NF, 3NF)
*   **1NF:** Atomic values, no repeating groups
*   **2NF:** 1NF + No partial dependencies (all non-key attributes depend on entire primary key)
*   **3NF:** 2NF + No transitive dependencies (non-key attributes depend only on primary key)

**Denormalization:**
*   Deliberately introduce redundancy for performance
*   Example: Store `total_likes` in Pages table instead of counting from Likes table every time

---

## Preparation Tips

### 1. Practice SQL Platforms
*   **LeetCode SQL:** Solve 50-60 medium/hard problems
*   **HackerRank SQL:** Complete SQL certification
*   **Mode Analytics:** Real-world SQL tutorials
*   **SQLZoo:** Interactive exercises

### 2. Key SQL Patterns to Master
*   Running totals with window functions
*   Self-joins (employee-manager, friend relationships)
*   Date range queries (last 7 days, month-over-month)
*   Complex aggregations with HAVING
*   Pivot tables (rows to columns)
*   Finding gaps and islands (consecutive sequences)

### 3. Data Modeling Practice
*   Design schema for popular apps (Twitter, Instagram, Uber)
*   Practice normalization and denormalization trade-offs
*   Think about indexes and query patterns
*   Consider scalability (sharding, partitioning)

### 4. Theoretical Knowledge
*   Read about OLTP vs OLAP
*   Understand Star vs Snowflake schema
*   Know different types of indexes
*   Study normalization forms

---

## Common Mistakes to Avoid

1.  **Not Using Window Functions:**
    *   Many candidates try to solve ranking problems with self-joins instead of `ROW_NUMBER()`
    *   Window functions are more efficient and readable

2.  **Forgetting Edge Cases:**
    *   NULL values (use `IS NULL`, not `= NULL`)
    *   Empty result sets (use `LEFT JOIN` carefully)
    *   Duplicate records (use `DISTINCT` or `GROUP BY` appropriately)

3.  **Over-Normalization in Data Modeling:**
    *   Don't normalize everything to 3NF if it hurts performance
    *   Discuss trade-offs with the interviewer

4.  **Not Considering Indexes:**
    *   Always mention which columns should be indexed
    *   Explain why (frequently queried, join keys, sort keys)

5.  **Poor Query Readability:**
    *   Use CTEs for complex queries instead of nested subqueries
    *   Alias tables clearly (`users u`, not `users t1`)
    *   Indent and format SQL properly

---

## Sample Interview Flow

### Typical 45-Minute Round

**0-5 min:** Introductions and warm-up

**5-25 min:** SQL Questions (Phase 1)
*   Interviewer gives a scenario (e.g., "We have a users table and orders table...")
*   You write queries for 3-4 progressively harder problems
*   Explain your approach before writing SQL

**25-35 min:** Data Modeling (Phase 2)
*   Interviewer describes a system (e.g., "Design a blogging platform...")
*   You draw schema on whiteboard/shared doc
*   Discuss normalization, indexes, scalability

**35-40 min:** Sample Queries on Your Schema
*   Interviewer asks: "Write a query to get top 10 most commented posts"
*   You write SQL based on your schema

**40-45 min:** Questions for interviewer

---

## Red Flags (What NOT to Do)

1.  **Cannot write window functions:** This is a must-know for Atlassian
2.  **Unfamiliar with JOINs:** Should be second nature
3.  **Over-complicating queries:** Simpler is better; avoid 5-level nested subqueries if a CTE works
4.  **No consideration for performance:** Always think about indexes, query optimization
5.  **Silent coding:** Explain your thought process as you write

---

## Success Checklist

- [ ] Mastered window functions (ROW_NUMBER, RANK, LAG, LEAD)
- [ ] Comfortable with all join types (INNER, LEFT, CROSS, SELF)
- [ ] Proficient with date/time functions
- [ ] Can write complex aggregations with GROUP BY and HAVING
- [ ] Use CTEs for readable queries
- [ ] Understand OLTP vs OLAP
- [ ] Know Star and Snowflake schemas
- [ ] Can design normalized schemas (up to 3NF)
- [ ] Can discuss denormalization trade-offs
- [ ] Can identify where to add indexes
- [ ] Practiced on LeetCode SQL (50+ problems)
- [ ] Can explain query execution plans (EXPLAIN command)

---

**Final Note:** Atlassian values clear communication. Even if you don't get the perfect query on the first try, explaining your approach and reasoning can still lead to a positive outcome. The interviewer often guides you if you're on the right track.


