# Fact Data Modeling - Homework Solutions

This document contains my complete solutions to the Week 2 fact data modeling homework assignment, demonstrating advanced SQL techniques for cumulative aggregations and array-based metrics.

## Assignment Overview

Working with `devices`, `events`, and `game_details` datasets to create efficient fact tables with cumulative tracking and reduced aggregations.

---

## Solution 1: Deduplicate `game_details`

Remove duplicates from the game_details table to ensure data quality.

```sql
-- Deduplication query using ROW_NUMBER() to keep first occurrence
WITH ranked_game_details AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (
            PARTITION BY game_id, team_id, player_id 
            ORDER BY created_at  -- Or any timestamp column
        ) AS row_num
    FROM game_details
)
SELECT 
    game_id,
    team_id,
    player_id,
    player_name,
    -- All other columns
    pts,
    reb,
    ast
    -- ... other stats
FROM ranked_game_details
WHERE row_num = 1;

-- Alternative: Create deduped table
CREATE TABLE game_details_deduped AS
SELECT DISTINCT ON (game_id, team_id, player_id)
    game_id,
    team_id,
    player_id,
    player_name,
    pts,
    reb,
    ast,
    fg3m,
    fg3a,
    ftm,
    fta
FROM game_details
ORDER BY game_id, team_id, player_id, created_at DESC;

-- Verification query
SELECT 
    COUNT(*) AS original_count,
    COUNT(DISTINCT (game_id, team_id, player_id)) AS unique_combinations,
    COUNT(*) - COUNT(DISTINCT (game_id, team_id, player_id)) AS duplicates_removed
FROM game_details;
```

**Why This Matters**: Duplicates skew aggregations and analytics. This ensures clean data.

---

## Solution 2: DDL for `user_devices_cumulated` Table

Track user activity by device/browser type with cumulative date arrays.

```sql
-- Create user_devices_cumulated table
CREATE TABLE user_devices_cumulated (
    user_id TEXT,
    browser_type TEXT,
    dates_active DATE[],
    date DATE,  -- Current processing date
    PRIMARY KEY (user_id, browser_type, date)
);

-- Create index for efficient lookups
CREATE INDEX idx_user_devices_date 
    ON user_devices_cumulated(date);

CREATE INDEX idx_user_devices_user 
    ON user_devices_cumulated(user_id);

-- Alternative schema using MAP type (if supported)
CREATE TABLE user_devices_cumulated_map (
    user_id TEXT,
    device_activity_datelist MAP<TEXT, DATE[]>,  -- browser_type -> array of dates
    date DATE,
    PRIMARY KEY (user_id, date)
);
```

**Design Choices**:
- Chose multi-row approach (browser_type as column) for better PostgreSQL compatibility
- `dates_active` array accumulates all active dates for each user+browser combination
- `date` tracks when the record was created/updated

---

## Solution 3: Cumulative Query to Generate `device_activity_datelist`

Build cumulative activity tracking incrementally, day by day.

```sql
INSERT INTO user_devices_cumulated
WITH yesterday AS (
    -- Get previous day's cumulative data
    SELECT 
        user_id,
        browser_type,
        dates_active,
        date
    FROM user_devices_cumulated
    WHERE date = DATE('2023-01-30')
),
today AS (
    -- Get today's activity from events
    SELECT 
        user_id,
        browser_type,
        DATE(event_time) AS event_date,
        COUNT(1) AS event_count
    FROM events
    WHERE DATE(event_time) = DATE('2023-01-31')
        AND user_id IS NOT NULL
        AND browser_type IS NOT NULL
    GROUP BY user_id, browser_type, DATE(event_time)
)
SELECT 
    COALESCE(t.user_id, y.user_id) AS user_id,
    COALESCE(t.browser_type, y.browser_type) AS browser_type,
    -- Accumulate previous dates + today's date (if active)
    CASE 
        WHEN y.dates_active IS NULL THEN ARRAY[t.event_date]
        WHEN t.user_id IS NOT NULL THEN y.dates_active || ARRAY[t.event_date]
        ELSE y.dates_active
    END AS dates_active,
    COALESCE(t.event_date, y.date + INTERVAL '1 day') AS date
FROM yesterday y
FULL OUTER JOIN today t 
    ON y.user_id = t.user_id 
    AND y.browser_type = t.browser_type;
```

**Key Features**:
- **Idempotent**: Can rerun for same day
- **Full Outer Join**: Handles both continuing and new users
- **Array Accumulation**: Efficiently stores all active dates
- **NULL Handling**: Gracefully handles missing data

**Sample Output**:
```
user_id | browser_type | dates_active                    | date
--------|--------------|--------------------------------|------------
user_1  | Chrome       | {2023-01-15, 2023-01-20, ...} | 2023-01-31
user_1  | Safari       | {2023-01-25, 2023-01-31}      | 2023-01-31
user_2  | Firefox      | {2023-01-31}                  | 2023-01-31
```

---

## Solution 4: `datelist_int` Conversion Query

Convert date arrays to integer bitwise representation for 10x storage reduction.

```sql
-- Create datelist_int table
CREATE TABLE user_devices_datelist_int (
    user_id TEXT,
    browser_type TEXT,
    datelist_int BIGINT,  -- Bitwise representation of dates
    month DATE,
    PRIMARY KEY (user_id, browser_type, month)
);

-- Conversion query
INSERT INTO user_devices_datelist_int
SELECT 
    user_id,
    browser_type,
    -- Convert array of dates to integer using bit shifting
    SUM(
        POWER(2, EXTRACT(DAY FROM date_active) - 1)::BIGINT
    ) AS datelist_int,
    DATE_TRUNC('month', date) AS month
FROM user_devices_cumulated
CROSS JOIN UNNEST(dates_active) AS date_active
WHERE DATE_TRUNC('month', date) = DATE('2023-01-01')  -- Process one month
GROUP BY user_id, browser_type, DATE_TRUNC('month', date);
```

**Bitwise Encoding Explanation**:
- Day 1 → Bit 0 → 2^0 = 1
- Day 2 → Bit 1 → 2^1 = 2  
- Day 3 → Bit 2 → 2^2 = 4
- Day 15 → Bit 14 → 2^14 = 16384
- Day 31 → Bit 30 → 2^30 = 1073741824

**Example**:
```
Active on days: 1, 3, 15, 31
Binary: 01000000000000100000000000000101
Decimal: 1073758213
```

**Query Active Days**:
```sql
-- Check if user was active on day 15
SELECT 
    user_id,
    browser_type,
    (datelist_int & POWER(2, 14)::BIGINT) > 0 AS was_active_day_15
FROM user_devices_datelist_int;

-- Count total active days in month
SELECT 
    user_id,
    browser_type,
    -- Count number of set bits
    BIT_COUNT(datelist_int) AS days_active_in_month
FROM user_devices_datelist_int;
```

**Benefits**:
- 90% storage reduction (array of 31 dates → single 8-byte integer)
- Fast bitwise operations
- Maintains day-level granularity

---

## Solution 5: DDL for `hosts_cumulated` Table

Track which dates each host experiences activity.

```sql
CREATE TABLE hosts_cumulated (
    host TEXT,
    host_activity_datelist DATE[],
    date DATE,
    PRIMARY KEY (host, date)
);

-- Indexes for performance
CREATE INDEX idx_hosts_date ON hosts_cumulated(date);
CREATE INDEX idx_hosts_host ON hosts_cumulated(host);
```

**Purpose**: Similar to user tracking but at host level for infrastructure monitoring.

---

## Solution 6: Incremental Query for `host_activity_datelist`

Generate host activity tracking incrementally.

```sql
INSERT INTO hosts_cumulated
WITH yesterday AS (
    SELECT 
        host,
        host_activity_datelist,
        date
    FROM hosts_cumulated
    WHERE date = DATE('2023-01-30')
),
today AS (
    SELECT 
        host,
        DATE(event_time) AS event_date,
        COUNT(1) AS event_count,
        COUNT(DISTINCT user_id) AS unique_visitors
    FROM events
    WHERE DATE(event_time) = DATE('2023-01-31')
        AND host IS NOT NULL
    GROUP BY host, DATE(event_time)
)
SELECT 
    COALESCE(t.host, y.host) AS host,
    CASE 
        WHEN y.host_activity_datelist IS NULL THEN ARRAY[t.event_date]
        WHEN t.host IS NOT NULL THEN y.host_activity_datelist || ARRAY[t.event_date]
        ELSE y.host_activity_datelist
    END AS host_activity_datelist,
    COALESCE(t.event_date, y.date + INTERVAL '1 day') AS date
FROM yesterday y
FULL OUTER JOIN today t ON y.host = t.host;
```

**Use Case**: Track which days each host (website/API) had traffic for uptime monitoring and SLA tracking.

---

## Solution 7: DDL for `host_activity_reduced` Monthly Fact Table

Pre-aggregate daily metrics by host for efficient monthly reporting.

```sql
CREATE TABLE host_activity_reduced (
    host TEXT,
    month DATE,
    hit_array INTEGER[],  -- Array of daily hit counts (length 31)
    unique_visitors_array INTEGER[],  -- Array of daily unique visitors (length 31)
    PRIMARY KEY (host, month)
);

-- Index for time-range queries
CREATE INDEX idx_host_reduced_month ON host_activity_reduced(month);
```

**Schema Design**:
- `month`: First day of month (2023-01-01)
- `hit_array[1]`: Hit count on day 1
- `hit_array[31]`: Hit count on day 31
- Same pattern for `unique_visitors_array`

---

## Solution 8: Incremental Load for `host_activity_reduced`

Load monthly fact table day by day.

```sql
INSERT INTO host_activity_reduced
WITH daily_aggregate AS (
    -- Calculate today's metrics
    SELECT 
        host,
        DATE(event_time) AS event_date,
        COUNT(1) AS hit_count,
        COUNT(DISTINCT user_id) AS unique_visitors
    FROM events
    WHERE DATE(event_time) = DATE('2023-01-15')  -- Processing day 15
    GROUP BY host, DATE(event_time)
),
month_so_far AS (
    -- Get existing month data
    SELECT 
        host,
        month,
        hit_array,
        unique_visitors_array
    FROM host_activity_reduced
    WHERE month = DATE_TRUNC('month', DATE('2023-01-15'))
)
SELECT 
    COALESCE(d.host, m.host) AS host,
    DATE_TRUNC('month', DATE('2023-01-15')) AS month,
    -- Update array at position for current day
    CASE 
        WHEN m.host IS NULL THEN 
            -- New month, initialize array
            ARRAY_FILL(0, ARRAY[31])::INTEGER[] || ARRAY[d.hit_count]
        ELSE 
            -- Update existing month
            m.hit_array[:EXTRACT(DAY FROM d.event_date)::INTEGER - 1] 
            || ARRAY[d.hit_count]::INTEGER[]
            || m.hit_array[EXTRACT(DAY FROM d.event_date)::INTEGER + 1:]
    END AS hit_array,
    CASE 
        WHEN m.host IS NULL THEN 
            ARRAY_FILL(0, ARRAY[31])::INTEGER[] || ARRAY[d.unique_visitors]
        ELSE 
            m.unique_visitors_array[:EXTRACT(DAY FROM d.event_date)::INTEGER - 1] 
            || ARRAY[d.unique_visitors]::INTEGER[]
            || m.unique_visitors_array[EXTRACT(DAY FROM d.event_date)::INTEGER + 1:]
    END AS unique_visitors_array
FROM month_so_far m
FULL OUTER JOIN daily_aggregate d ON m.host = d.host
ON CONFLICT (host, month) 
DO UPDATE SET
    hit_array = EXCLUDED.hit_array,
    unique_visitors_array = EXCLUDED.unique_visitors_array;
```

**Advanced Features**:
- **Array Slicing**: Updates specific day in array
- **Upsert Logic**: `ON CONFLICT` for idempotency
- **Month Initialization**: Creates 31-element array for new months

**Query Monthly Stats**:
```sql
-- Get total hits for January
SELECT 
    host,
    SUM(hits) AS total_hits,
    AVG(hits) AS avg_daily_hits,
    MAX(hits) AS peak_day_hits
FROM (
    SELECT 
        host,
        UNNEST(hit_array) AS hits
    FROM host_activity_reduced
    WHERE month = '2023-01-01'
) sub
GROUP BY host
ORDER BY total_hits DESC;

-- Find peak day for each host
SELECT 
    host,
    month,
    GREATEST(hit_array[1], hit_array[2], ..., hit_array[31]) AS peak_hits,
    ARRAY_POSITION(hit_array, GREATEST(hit_array[1], ...)) AS peak_day
FROM host_activity_reduced;
```

---

## Complete Pipeline Example

```sql
-- Day 1: Initialize base table
INSERT INTO user_devices_cumulated
SELECT 
    user_id,
    browser_type,
    ARRAY[DATE('2023-01-01')] AS dates_active,
    DATE('2023-01-01') AS date
FROM events
WHERE DATE(event_time) = DATE('2023-01-01')
GROUP BY user_id, browser_type;

-- Day 2: Incremental update (run solution 3)
-- Day 3: Incremental update
-- ... continue daily

-- End of month: Convert to datelist_int (run solution 4)
-- Result: Compressed storage for fast analytics
```

---

## Performance Optimizations

### Index Strategy
```sql
-- Composite index for common queries
CREATE INDEX idx_events_time_user 
    ON events(event_time, user_id) 
    WHERE user_id IS NOT NULL;

-- GIN index for array containment queries
CREATE INDEX idx_user_devices_dates_gin 
    ON user_devices_cumulated USING GIN(dates_active);

-- Query using index
SELECT user_id, browser_type
FROM user_devices_cumulated
WHERE dates_active @> ARRAY[DATE('2023-01-15')]::DATE[];
```

### Partitioning Strategy
```sql
-- Partition cumulated table by month
CREATE TABLE user_devices_cumulated_partitioned (
    user_id TEXT,
    browser_type TEXT,
    dates_active DATE[],
    date DATE
) PARTITION BY RANGE (date);

-- Create monthly partitions
CREATE TABLE user_devices_202301 
    PARTITION OF user_devices_cumulated_partitioned
    FOR VALUES FROM ('2023-01-01') TO ('2023-02-01');

CREATE TABLE user_devices_202302 
    PARTITION OF user_devices_cumulated_partitioned
    FOR VALUES FROM ('2023-02-01') TO ('2023-03-01');
```

---

## Testing & Validation

### Data Quality Checks
```sql
-- Verify no duplicate dates in arrays
SELECT 
    user_id,
    browser_type,
    CARDINALITY(dates_active) AS array_length,
    CARDINALITY(ARRAY(SELECT DISTINCT UNNEST(dates_active))) AS unique_dates
FROM user_devices_cumulated
WHERE CARDINALITY(dates_active) <> 
      CARDINALITY(ARRAY(SELECT DISTINCT UNNEST(dates_active)));
-- Should return 0 rows

-- Verify datelist_int accuracy
WITH test_data AS (
    SELECT 
        user_id,
        browser_type,
        dates_active,
        datelist_int
    FROM user_devices_cumulated
    JOIN user_devices_datelist_int USING (user_id, browser_type)
    WHERE month = DATE_TRUNC('month', date)
)
SELECT 
    user_id,
    CARDINALITY(dates_active) AS actual_days,
    BIT_COUNT(datelist_int) AS encoded_days
FROM test_data
WHERE CARDINALITY(dates_active) <> BIT_COUNT(datelist_int);
-- Should return 0 rows
```

---

## Key Learnings

### Technical Skills Demonstrated
✅ **Cumulative Aggregations**: Building running totals over time  
✅ **Array Operations**: Concatenation, unnesting, array_agg  
✅ **Bitwise Encoding**: Compression with bit manipulation  
✅ **Incremental Processing**: Efficient day-by-day updates  
✅ **Data Deduplication**: Multiple strategies (DISTINCT, ROW_NUMBER)  
✅ **Upsert Patterns**: ON CONFLICT for idempotency  

### Design Patterns
✅ Full outer join for comprehensive coverage  
✅ COALESCE for NULL handling  
✅ Array slicing for targeted updates  
✅ Window functions for ranking  

### Real-World Applications
- **User Analytics**: Track engagement patterns
- **Infrastructure Monitoring**: Host uptime and traffic
- **Growth Metrics**: Active user calculations
- **Storage Optimization**: Reduce costs with compression

---

## Storage Comparison

```
Scenario: 1M users, 30 days, 3 browser types

Approach 1: Row per user-day-browser
- Rows: 90M (1M × 30 × 3)
- Storage: ~7.2 GB

Approach 2: Cumulative array
- Rows: 3M (1M × 3)
- Storage: ~450 MB (94% reduction)

Approach 3: Datelist integer
- Rows: 3M (1M × 3)
- Storage: ~48 MB (99% reduction!)
```

**Winner**: Datelist integer for monthly reporting at scale.

---

*Solutions completed as part of DataExpert.io Data Engineering Bootcamp - December 2024*


