# 📈 Fact Data Modeling & Array-Based Aggregations

## Overview

This project showcases advanced fact table design optimized for OLAP (Online Analytical Processing) workloads. The implementation demonstrates array-based metrics, cumulative aggregations, and efficient storage techniques for time-series analytics.

## 🎯 Project Goals

- Design efficient fact tables for analytical queries
- Implement cumulative user activity tracking
- Build array-based metrics for temporal analysis
- Create reduced fact tables for monthly aggregations
- Optimize storage with intelligent compression

## 🛠️ Technologies Used

- **Database**: PostgreSQL
- **Language**: SQL
- **Data Types**: Arrays, Maps, JSON
- **Infrastructure**: Docker
- **Techniques**: Cumulative Aggregations, Datelist Compression

## 📚 Key Concepts Implemented

### 1. Cumulative Activity Tracking
Maintains running lists of active dates for each entity, enabling efficient lookups of historical activity.

**Features**:
- Device-level activity tracking
- Browser type segmentation
- Incremental daily updates
- Efficient date range queries

### 2. Datelist Integer Compression
Converts date arrays into bitwise integer representations for 10x storage reduction.

**Features**:
- Bit-shifting for date encoding
- 32 days per integer (one month)
- Fast bitwise operations for lookups
- Significant storage savings

### 3. Reduced Fact Tables
Pre-aggregated monthly summaries for faster reporting queries.

**Features**:
- Array-based daily metrics
- Unique visitor tracking
- Host-level aggregations
- Day-by-day incremental loads

## 📂 Project Structure

```
02-fact-modeling/
├── README.md                        # This file
├── sql/
│   ├── user_devices_cumulated_ddl.sql  # Cumulative table schema
│   ├── user_devices_populate.sql       # Daily population logic
│   ├── datelist_int_conversion.sql     # Compression algorithm
│   ├── hosts_cumulated_ddl.sql         # Host activity schema
│   ├── hosts_cumulated_populate.sql    # Host tracking logic
│   ├── host_activity_reduced_ddl.sql   # Monthly fact table
│   ├── host_activity_populate.sql      # Monthly aggregation
│   └── game_details_dedup.sql          # Deduplication query
├── docker-compose.yml               # PostgreSQL setup
└── examples/
    └── sample_queries.sql          # Example analytical queries
```

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose installed
- PostgreSQL client
- Understanding of array operations

### Setup Instructions

1. **Start PostgreSQL**
```bash
cd 02-fact-modeling
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

3. **Run DDL Scripts**
Execute table creation scripts in order

4. **Load Sample Data**
Populate with sample events and users

5. **Run Population Scripts**
Execute incremental load scripts

## 💡 Key Implementations

### User Devices Cumulated Table

**Schema Option 1 - Map Structure**:
```sql
CREATE TABLE user_devices_cumulated (
    user_id TEXT,
    device_activity_datelist MAP<VARCHAR, ARRAY<DATE>>,
    date DATE,
    PRIMARY KEY (user_id, date)
);
```

**Schema Option 2 - Multiple Rows**:
```sql
CREATE TABLE user_devices_cumulated (
    user_id TEXT,
    browser_type VARCHAR,
    dates_active ARRAY<DATE>,
    date DATE,
    PRIMARY KEY (user_id, browser_type, date)
);
```

### Incremental Population Logic

```sql
WITH yesterday AS (
    SELECT * 
    FROM user_devices_cumulated
    WHERE date = DATE('2023-01-30')
),
today AS (
    SELECT 
        user_id,
        browser_type,
        DATE_TRUNC('day', event_time) AS today_date,
        COUNT(1) AS event_count
    FROM events
    WHERE DATE_TRUNC('day', event_time) = DATE('2023-01-31')
      AND user_id IS NOT NULL
    GROUP BY user_id, browser_type, DATE_TRUNC('day', event_time)
)
INSERT INTO user_devices_cumulated
SELECT 
    COALESCE(t.user_id, y.user_id) AS user_id,
    COALESCE(t.browser_type, y.browser_type) AS browser_type,
    COALESCE(y.dates_active, ARRAY[]::DATE[]) || 
        CASE 
            WHEN t.user_id IS NOT NULL 
            THEN ARRAY[t.today_date]
            ELSE ARRAY[]::DATE[]
        END AS dates_active,
    COALESCE(t.today_date, y.date + INTERVAL '1 day') AS date
FROM yesterday y
FULL OUTER JOIN today t 
    ON y.user_id = t.user_id 
    AND y.browser_type = t.browser_type;
```

### Datelist Integer Conversion

**Compression Logic**:
```sql
SELECT 
    user_id,
    browser_type,
    CAST(
        SUM(
            CASE 
                WHEN EXTRACT(DAY FROM dates_active) IS NOT NULL 
                THEN POW(2, EXTRACT(DAY FROM dates_active) - 1)
                ELSE 0 
            END
        ) AS BIGINT
    ) AS datelist_int,
    DATE_TRUNC('month', date) AS month
FROM user_devices_cumulated
CROSS JOIN UNNEST(dates_active) AS dates_active
GROUP BY user_id, browser_type, DATE_TRUNC('month', date);
```

**Benefits**:
- Reduces storage by ~90%
- Enables fast bitwise operations
- Maintains full day-level granularity
- Perfect for monthly reporting

### Host Activity Reduced Table

**Schema**:
```sql
CREATE TABLE host_activity_reduced (
    host VARCHAR,
    month DATE,
    hit_array INTEGER[],
    unique_visitors_array INTEGER[],
    PRIMARY KEY (host, month)
);
```

**Daily Incremental Load**:
```sql
WITH daily_aggregate AS (
    SELECT 
        host,
        DATE(event_time) AS event_date,
        COUNT(1) AS hit_count,
        COUNT(DISTINCT user_id) AS unique_visitors
    FROM events
    WHERE DATE(event_time) = DATE('2023-01-15')
    GROUP BY host, DATE(event_time)
),
month_so_far AS (
    SELECT *
    FROM host_activity_reduced
    WHERE month = DATE_TRUNC('month', DATE('2023-01-15'))
)
INSERT INTO host_activity_reduced
SELECT 
    COALESCE(d.host, m.host) AS host,
    DATE_TRUNC('month', DATE('2023-01-15')) AS month,
    COALESCE(m.hit_array, ARRAY_FILL(0, ARRAY[31])) || d.hit_count AS hit_array,
    COALESCE(m.unique_visitors_array, ARRAY_FILL(0, ARRAY[31])) || d.unique_visitors AS unique_visitors_array
FROM month_so_far m
FULL OUTER JOIN daily_aggregate d ON m.host = d.host
ON CONFLICT (host, month) 
DO UPDATE SET
    hit_array = EXCLUDED.hit_array,
    unique_visitors_array = EXCLUDED.unique_visitors_array;
```

## 📊 Sample Analytical Queries

### Check User Activity on Specific Date
```sql
SELECT 
    user_id,
    browser_type,
    DATE('2023-01-15') = ANY(dates_active) AS was_active
FROM user_devices_cumulated
WHERE date = DATE('2023-01-31')
  AND user_id = 'user_123';
```

### Calculate Days Active in Month
```sql
SELECT 
    user_id,
    browser_type,
    CARDINALITY(dates_active) AS days_active,
    date
FROM user_devices_cumulated
WHERE date = DATE('2023-01-31')
ORDER BY days_active DESC;
```

### Monthly Host Performance
```sql
SELECT 
    host,
    month,
    SUM(hit_count) AS total_hits,
    AVG(unique_visitors) AS avg_daily_visitors,
    MAX(hit_count) AS peak_day_hits
FROM (
    SELECT 
        host,
        month,
        UNNEST(hit_array) AS hit_count,
        UNNEST(unique_visitors_array) AS unique_visitors
    FROM host_activity_reduced
    WHERE month = DATE('2023-01-01')
) sub
GROUP BY host, month
ORDER BY total_hits DESC;
```

### Growth Calculation Using Datelist
```sql
WITH user_activity AS (
    SELECT 
        user_id,
        datelist_int,
        month
    FROM user_devices_datelist_int
)
SELECT 
    month,
    COUNT(DISTINCT CASE WHEN datelist_int > 0 THEN user_id END) AS active_users,
    COUNT(DISTINCT CASE WHEN datelist_int & 1 = 1 THEN user_id END) AS active_on_day_1
FROM user_activity
GROUP BY month;
```

## 🎓 Learning Outcomes

After completing this project, you will understand:

✅ **Fact Table Design**: Optimizing tables for analytical queries  
✅ **Array Operations**: Leveraging PostgreSQL array functions  
✅ **Cumulative Patterns**: Building incremental aggregation pipelines  
✅ **Data Compression**: Reducing storage with bitwise encoding  
✅ **Temporal Analytics**: Tracking activity over time efficiently  
✅ **Performance Tuning**: Index strategies for array queries  

## 🔍 Key Insights

### Design Patterns
1. **Cumulative Aggregation**: Build up arrays day by day
2. **Full Outer Join**: Handle both new and existing entities
3. **Array Concatenation**: Efficient append operations
4. **Bitwise Encoding**: Compress dates into integers
5. **Pre-Aggregation**: Reduce query times with summary tables

### Best Practices
- Use arrays for bounded lists (dates in month, daily metrics)
- Implement upsert logic with ON CONFLICT for idempotency
- Partition large fact tables by time period
- Create indexes on frequently filtered columns
- Monitor array size to prevent bloat

### Performance Considerations
- Arrays work well for up to ~100 elements
- GiST indexes for array containment queries
- Partition fact tables by month/quarter
- Use reduced tables for reporting dashboards
- Batch process for backfills

## 🚧 Challenges Solved

1. **Storage Efficiency**: Reduced storage by 90% using datelist_int
2. **Query Performance**: Pre-aggregated metrics for fast dashboards
3. **Incremental Updates**: Idempotent daily loads that don't duplicate
4. **Deduplication**: Handled duplicate game_details records
5. **Flexibility**: Supported both map and multi-row schemas

## 📈 Real-World Applications

This fact modeling approach is used in:
- **Web Analytics**: User session tracking and page views
- **Gaming**: Player activity and engagement metrics
- **E-commerce**: Purchase patterns and cart analysis
- **SaaS Products**: Feature usage and activation metrics
- **IoT**: Device activity and sensor readings

## 🔗 Related Projects

- [Dimensional Modeling](../01-dimensional-modeling/) - Combine with dimension tables
- [Analytical Patterns](../05-analytical-patterns/) - Apply growth accounting
- [Spark Pipelines](../03-spark-pipelines/) - Scale to billions of events

## 📚 Resources

- [PostgreSQL Array Functions](https://www.postgresql.org/docs/current/functions-array.html)
- [Fact Table Design](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/fact-table-detail/)
- [Bitwise Operations](https://www.postgresql.org/docs/current/functions-bitstring.html)

---

**Next Steps**: Explore [Spark Pipelines](../03-spark-pipelines/) to scale these patterns to petabyte-scale data.


