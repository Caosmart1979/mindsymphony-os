---
name: database-schema-architect
description: Expert database schema design and optimization guidance. Use this skill when designing database schemas, creating ER diagrams, optimizing queries, normalizing data, implementing indexes, planning migrations, choosing between SQL/NoSQL, or working with ORMs and data modeling.
license: Apache-2.0
interop_metadata:
  skill_id: skills.database_schema_architect
  api_version: v1
  authentication: none
  rate_limit:
    requests_per_minute: 30
---

# Database Schema Architect

Expert guidance for designing efficient, scalable, and maintainable database schemas.

## Core Design Principles

**Database Selection:**
- **Relational (SQL)**: Structured data, ACID transactions, complex relationships (PostgreSQL, MySQL)
- **Document (NoSQL)**: Flexible schema, hierarchical data (MongoDB, CouchDB)
- **Key-Value**: High-performance caching, simple lookups (Redis, DynamoDB)
- **Graph**: Complex relationships, social networks (Neo4j)
- **Time-Series**: Metrics, IoT data (InfluxDB, TimescaleDB)

**Schema Design Rules:**
1. Start with normalization, denormalize for performance
2. Use appropriate data types to save space
3. Index columns used in WHERE, JOIN, ORDER BY clauses
4. Design for query patterns, not just data storage
5. Plan for scaling from day one

## Normalization Levels

**First Normal Form (1NF):**
- Eliminate repeating groups
- Each column should contain atomic values
- Each row should be unique

**Second Normal Form (2NF):**
- Meet 1NF
- Remove partial dependencies
- All non-key columns depend on the entire primary key

**Third Normal Form (3NF):**
- Meet 2NF
- Remove transitive dependencies
- Non-key columns depend only on the primary key

**Example Denormalization (for read performance):**
```sql
-- Normalized (3NF)
Users (id, name, email)
Orders (id, user_id, total, created_at)
OrderItems (id, order_id, product_id, quantity, price)

-- Denormalized for read performance
Orders (id, user_id, user_name, total, created_at)
```

## Indexing Strategy

**Primary Types:**
- **B-Tree**: Default, good for range queries
- **Hash**: Exact match lookups
- **GIN**: Arrays, JSONB, full-text search
- **Partial**: Index filtered subset of data

**When to Index:**
```sql
-- Columns in WHERE clauses
CREATE INDEX idx_users_email ON users(email);

-- Foreign keys
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- Composite indexes for multi-column queries
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);

-- Partial index for common queries
CREATE INDEX idx_active_users ON users(id) WHERE status = 'active';
```

**Index DON'Ts:**
- Don't index low-cardinality columns (e.g., boolean with 50/50 split)
- Don't over-index - slows down writes
- Don't index columns not used in queries

## Common Schema Patterns

**Users and Authentication:**
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  last_login_at TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created ON users(created_at);
```

**Many-to-Many Relationships:**
```sql
-- Students and Courses
CREATE TABLE students (id SERIAL PRIMARY KEY, name VARCHAR(255));
CREATE TABLE courses (id SERIAL PRIMARY KEY, name VARCHAR(255));

-- Junction table
CREATE TABLE enrollments (
  student_id INTEGER REFERENCES students(id),
  course_id INTEGER REFERENCES courses(id),
  enrolled_at TIMESTAMP DEFAULT NOW(),
  PRIMARY KEY (student_id, course_id)
);
```

**Soft Deletes:**
```sql
CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255),
  content TEXT,
  deleted_at TIMESTAMP NULL,
  is_deleted BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_posts_deleted ON posts(is_deleted, deleted_at);
```

**Audit Trail:**
```sql
CREATE TABLE audit_logs (
  id SERIAL PRIMARY KEY,
  table_name VARCHAR(255) NOT NULL,
  record_id INTEGER NOT NULL,
  action VARCHAR(50) NOT NULL,
  old_data JSONB,
  new_data JSONB,
  changed_by INTEGER REFERENCES users(id),
  changed_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_audit_table_record ON audit_logs(table_name, record_id);
CREATE INDEX idx_audit_changed_at ON audit_logs(changed_at);
```

## Query Optimization

**EXPLAIN ANALYZE:**
```sql
EXPLAIN ANALYZE
SELECT u.name, COUNT(o.id)
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id;
```

**Common Optimizations:**
- Use JOINs instead of subqueries
- Avoid SELECT * - specify columns
- Use LIMIT for large result sets
- Use connection pooling
- Batch inserts/updates

**Before (slow):**
```sql
SELECT * FROM users WHERE id IN (
  SELECT user_id FROM orders WHERE total > 100
);
```

**After (fast):**
```sql
SELECT DISTINCT u.* FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.total > 100;
```

## Migration Best Practices

**Version Control:**
```
migrations/
  001_initial_schema.sql
  002_add_users_table.sql
  003_add_index_on_email.sql
  004_add_soft_deletes.sql
```

**Safe Migration Steps:**
1. Write backward-compatible changes
2. Add new columns (nullable)
3. Deploy code changes
4. Migrate data
5. Make columns NOT NULL (if needed)
6. Remove old columns in separate migration

**Example Migration:**
```sql
-- Step 1: Add new column (nullable)
ALTER TABLE users ADD COLUMN username VARCHAR(100);

-- Step 2: Backfill data (separate migration)
UPDATE users SET username = LOWER(SUBSTRING(email, 1, POSITION('@' IN email) - 1));

-- Step 3: Add constraint (separate migration)
ALTER TABLE users ALTER COLUMN username SET NOT NULL;
ALTER TABLE users ADD CONSTRAINT username_unique UNIQUE (username);
```

## Data Integrity

**Constraints:**
```sql
-- NOT NULL
ALTER TABLE users ALTER COLUMN email SET NOT NULL;

-- UNIQUE
ALTER TABLE users ADD CONSTRAINT email_unique UNIQUE (email);

-- CHECK
ALTER TABLE products ADD CONSTRAINT price_positive CHECK (price >= 0);

-- FOREIGN KEY
ALTER TABLE orders ADD CONSTRAINT user_fk 
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
```

**Transactions:**
```sql
BEGIN;
  INSERT INTO orders (user_id, total) VALUES (1, 100);
  INSERT INTO order_items (order_id, product_id, quantity) 
    VALUES (currval('orders_id_seq'), 5, 2);
COMMIT;
-- ROLLBACK on error
```

## Scaling Strategies

**Vertical Scaling:**
- Larger server, more RAM, faster storage
- Simpler architecture
- Eventually hits limits

**Horizontal Scaling:**
- Read replicas for read-heavy workloads
- Sharding by customer/region
- Partitioning large tables

**Caching:**
- Redis for frequently accessed data
- Materialized views for complex queries
- Application-level caching

## ORM vs Raw SQL

**Use ORM (ActiveRecord, Sequelize, Prisma) when:**
- Simple CRUD operations
- Rapid prototyping
- Type safety is important
- Database-agnostic code needed

**Use Raw SQL when:**
- Complex queries with multiple JOINs
- Performance-critical paths
- Bulk operations
- Database-specific features needed

## Schema Review Checklist

**Design:**
- [ ] Is the data normalized appropriately?
- [ ] Are indexes properly placed?
- [ ] Are foreign keys defined?
- [ ] Are constraints defined?
- [ ] Is there a migration strategy?

**Performance:**
- [ ] Have slow queries been identified?
- [ ] Are JOINs using indexes?
- [ ] Is N+1 query problem avoided?
- [ ] Is connection pooling configured?

**Security:**
- [ ] Are sensitive data encrypted at rest?
- [ ] Is least-privilege access configured?
- [ ] Are SQL injection prevented?
- [ ] Is audit logging configured?

## Working with This Skill

Provide:
1. Database type (PostgreSQL, MySQL, MongoDB, etc.)
2. Data requirements and relationships
3. Query patterns and access patterns
4. Expected scale and growth
5. Specific constraints or requirements

This skill will help you design an efficient, scalable database schema.
