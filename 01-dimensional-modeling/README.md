# 📊 Dimensional Data Modeling Project

## Overview

This project demonstrates advanced dimensional data modeling techniques, focusing on building slowly changing dimensions (SCD Type 2) with incremental processing capabilities. The implementation showcases production-ready approaches to historical data tracking and temporal analytics.

## 🎯 Project Goals

- Design efficient dimensional models for analytical workloads
- Implement SCD Type 2 for historical tracking
- Build incremental, idempotent data pipelines
- Create graph-based data structures for network analysis
- Optimize queries for time-series analysis

## 🛠️ Technologies Used

- **Database**: PostgreSQL
- **Language**: SQL
- **Infrastructure**: Docker, Docker Compose
- **Techniques**: CTEs, Window Functions, Array Aggregations

## 📚 Key Concepts Implemented

### 1. Slowly Changing Dimensions (SCD Type 2)
Tracks historical changes in dimensional attributes with start and end dates, enabling point-in-time analysis.

**Features**:
- Automatic change detection using window functions
- Efficient streak identification for grouping consecutive periods
- Start/end date tracking for valid time ranges
- Quality class categorization based on performance metrics

### 2. Incremental Cumulative Tables
Processes data incrementally, one period at a time, ensuring idempotency and efficient updates.

**Features**:
- Day-by-day processing with full outer joins
- Array-based accumulation of historical data
- Activity tracking with boolean flags
- Efficient backfill capabilities

### 3. Graph Data Structures
Models relationships as edges and vertices for network analysis.

**Features**:
- Player-to-player relationship tracking
- Team vertices with aggregated statistics
- Graph traversal optimization
- Network metrics calculation

## 📂 Project Structure

```
01-dimensional-modeling/
├── README.md                    # This file
├── sql/
│   ├── actors_table_ddl.sql    # Actors dimension table schema
│   ├── actors_cumulative.sql   # Incremental population logic
│   ├── actors_scd_ddl.sql      # SCD Type 2 table schema
│   ├── actors_scd_backfill.sql # Historical data backfill
│   ├── actors_scd_incremental.sql # Daily SCD updates
│   ├── players_scd.sql         # Player dimension with SCD
│   ├── graph_edges.sql         # Graph edge definitions
│   └── graph_vertices.sql      # Graph vertex definitions
├── docker-compose.yml          # PostgreSQL setup
└── data/
    └── sample_data.sql         # Sample dataset for testing
```

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose installed
- Database client (DBeaver, DataGrip, or psql)
- Basic SQL knowledge

### Setup Instructions

1. **Start PostgreSQL**
```bash
cd 01-dimensional-modeling
docker-compose up -d
```

2. **Connect to Database**
```
Host: localhost
Port: 5432
Database: postgres
Username: postgres
Password: postgres
```

3. **Load Sample Data**
```bash
psql -h localhost -U postgres -d postgres -f data/sample_data.sql
```

4. **Run SQL Scripts**
Execute the SQL files in order:
- DDL scripts first (create tables)
- Population scripts second (load data)
- Query scripts last (analyze data)

## 💡 Key Implementations

### Actors Dimension Table

**Schema**:
```sql
CREATE TABLE actors (
    actor_id TEXT,
    actor_name TEXT,
    films STRUCT<
        film VARCHAR,
        votes INTEGER,
        rating REAL,
        filmid VARCHAR
    >[],
    quality_class quality_class_enum,
    is_active BOOLEAN,
    current_year INTEGER,
    PRIMARY KEY (actor_id, current_year)
);
```

**Quality Classification**:
- `star`: Average rating > 8
- `good`: Average rating > 7 and ≤ 8
- `average`: Average rating > 6 and ≤ 7
- `bad`: Average rating ≤ 6

### SCD Type 2 Implementation

**Streak Detection Logic**:
```sql
WITH streak_started AS (
    SELECT 
        actor_id,
        current_year,
        quality_class,
        LAG(quality_class) OVER (
            PARTITION BY actor_id 
            ORDER BY current_year
        ) <> quality_class AS did_change
    FROM actors
),
streak_identified AS (
    SELECT 
        actor_id,
        quality_class,
        current_year,
        SUM(CASE WHEN did_change THEN 1 ELSE 0 END) 
            OVER (PARTITION BY actor_id ORDER BY current_year) 
            AS streak_identifier
    FROM streak_started
)
SELECT 
    actor_id,
    quality_class,
    MIN(current_year) AS start_date,
    MAX(current_year) AS end_date
FROM streak_identified
GROUP BY actor_id, quality_class, streak_identifier;
```

### Incremental Processing Pattern

**Daily Update Logic**:
```sql
WITH yesterday AS (
    SELECT * FROM actors
    WHERE current_year = 2020
),
today AS (
    SELECT 
        actor_id,
        actor_name,
        ARRAY_AGG(STRUCT(film, votes, rating, filmid)) AS films,
        AVG(rating) AS avg_rating
    FROM actor_films
    WHERE year = 2021
    GROUP BY actor_id, actor_name
)
INSERT INTO actors
SELECT 
    COALESCE(t.actor_id, y.actor_id),
    COALESCE(t.actor_name, y.actor_name),
    COALESCE(y.films, ARRAY[]::film_struct[]) || COALESCE(t.films, ARRAY[]::film_struct[]),
    CASE 
        WHEN t.avg_rating > 8 THEN 'star'
        WHEN t.avg_rating > 7 THEN 'good'
        WHEN t.avg_rating > 6 THEN 'average'
        ELSE 'bad'
    END AS quality_class,
    t.actor_id IS NOT NULL AS is_active,
    COALESCE(t.year, y.current_year + 1) AS current_year
FROM yesterday y
FULL OUTER JOIN today t ON y.actor_id = t.actor_id;
```

## 📊 Sample Queries

### Find All Quality Changes for an Actor
```sql
SELECT 
    actor_name,
    quality_class,
    start_date,
    end_date,
    end_date - start_date + 1 AS duration_years
FROM actors_scd
WHERE actor_name = 'Tom Hanks'
ORDER BY start_date;
```

### Identify Currently Active Star Actors
```sql
SELECT 
    actor_name,
    CARDINALITY(films) AS total_films,
    quality_class
FROM actors
WHERE current_year = 2021
  AND is_active = TRUE
  AND quality_class = 'star'
ORDER BY CARDINALITY(films) DESC;
```

### Point-in-Time Analysis
```sql
SELECT 
    actor_name,
    quality_class
FROM actors_scd
WHERE start_date <= 2015
  AND end_date >= 2015
  AND quality_class = 'star';
```

## 🎓 Learning Outcomes

After completing this project, you will understand:

✅ **Dimensional Modeling**: Kimball methodology and star schema design  
✅ **Temporal Data**: Managing historical changes with SCD Type 2  
✅ **Incremental Processing**: Building idempotent daily pipelines  
✅ **Complex SQL**: CTEs, window functions, array operations  
✅ **Graph Structures**: Modeling relationships as edges and vertices  
✅ **Performance Optimization**: Indexing, partitioning, query tuning  

## 🔍 Key Insights

### Design Patterns
1. **Full Outer Join Pattern**: Handles both new and existing records
2. **Streak Identification**: Groups consecutive periods with same attributes
3. **Array Accumulation**: Efficiently stores historical metrics
4. **Change Detection**: Uses LAG window function for comparison

### Best Practices
- Always include idempotency checks
- Process data incrementally for efficiency
- Use appropriate data types (arrays for lists, enums for categories)
- Maintain audit columns (created_at, updated_at)
- Index on frequently joined columns

### Performance Considerations
- Partition large tables by year/month
- Use appropriate indexes (B-tree for equality, BRIN for time-series)
- Consider materialized views for complex aggregations
- Batch inserts instead of row-by-row

## 🚧 Challenges Solved

1. **Historical Tracking**: Implemented SCD Type 2 to track all changes over time
2. **Incremental Updates**: Built idempotent pipelines that can run daily
3. **Quality Classification**: Automated categorization based on performance metrics
4. **Graph Relationships**: Modeled complex player networks as graph structures

## 📈 Real-World Applications

This dimensional modeling approach is used in:
- **E-commerce**: Customer and product dimensions with historical tracking
- **Finance**: Account status changes and transaction categorization
- **Healthcare**: Patient journey tracking and status changes
- **Gaming**: Player stats and achievement tracking
- **Social Networks**: User relationships and activity patterns

## 🔗 Related Projects

- [Fact Data Modeling](../02-fact-modeling/) - Complement with fact tables
- [Analytical Patterns](../05-analytical-patterns/) - Use dimensions for analysis
- [Spark Pipelines](../03-spark-pipelines/) - Scale with distributed processing

## 📚 Resources

- [Kimball Dimensional Modeling](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/)
- [SCD Type 2 Explained](https://en.wikipedia.org/wiki/Slowly_changing_dimension)
- [PostgreSQL Window Functions](https://www.postgresql.org/docs/current/tutorial-window.html)

---

**Next Steps**: Explore [Fact Data Modeling](../02-fact-modeling/) to complement these dimensions with aggregated metrics.


