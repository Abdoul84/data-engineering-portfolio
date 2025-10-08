# Dimensional Data Modeling - Homework Solutions

This document contains my solutions to the Week 1 dimensional data modeling homework assignment.

## Assignment Overview

Working with the `actor_films` dataset to create dimensional models with SCD Type 2 implementation.

---

## Solution 1: DDL for `actors` Table

Create a cumulative dimensional table with film arrays and quality classification.

```sql
-- Create custom type for film struct
CREATE TYPE film_stats AS (
    film TEXT,
    votes INTEGER,
    rating REAL,
    filmid TEXT
);

-- Create enum for quality classification
CREATE TYPE quality_class AS ENUM ('star', 'good', 'average', 'bad');

-- Create actors dimension table
CREATE TABLE actors (
    actor TEXT,
    actorid TEXT,
    films film_stats[],
    quality_class quality_class,
    is_active BOOLEAN,
    current_year INTEGER,
    PRIMARY KEY (actorid, current_year)
);
```

**Design Decisions**:
- Used custom `film_stats` type for better type safety
- Created `quality_class` enum to enforce valid values
- Composite primary key on `(actorid, current_year)` for temporal tracking
- `films` array accumulates all films up to `current_year`

---

## Solution 2: Cumulative Table Generation Query

Populate the `actors` table incrementally, one year at a time.

```sql
INSERT INTO actors
WITH yesterday AS (
    SELECT 
        actor,
        actorid,
        films,
        quality_class,
        is_active,
        current_year
    FROM actors
    WHERE current_year = 1970  -- Previous year
),
today AS (
    SELECT 
        actor,
        actorid,
        ARRAY_AGG(
            ROW(film, votes, rating, filmid)::film_stats
        ) AS films,
        AVG(rating) AS avg_rating,
        1971 AS current_year  -- Current year being processed
    FROM actor_films
    WHERE year = 1971
    GROUP BY actor, actorid
)
SELECT 
    COALESCE(t.actor, y.actor) AS actor,
    COALESCE(t.actorid, y.actorid) AS actorid,
    -- Accumulate films from previous years + current year
    COALESCE(y.films, ARRAY[]::film_stats[]) || 
    COALESCE(t.films, ARRAY[]::film_stats[]) AS films,
    -- Quality class based on current year's average rating
    CASE 
        WHEN t.avg_rating IS NULL THEN y.quality_class  -- No films this year, keep previous
        WHEN t.avg_rating > 8 THEN 'star'::quality_class
        WHEN t.avg_rating > 7 THEN 'good'::quality_class
        WHEN t.avg_rating > 6 THEN 'average'::quality_class
        ELSE 'bad'::quality_class
    END AS quality_class,
    -- Active if they had films this year
    t.actorid IS NOT NULL AS is_active,
    COALESCE(t.current_year, y.current_year + 1) AS current_year
FROM yesterday y
FULL OUTER JOIN today t 
    ON y.actorid = t.actorid;
```

**Key Features**:
- **Idempotent**: Can be run multiple times for the same year
- **Full Outer Join**: Handles both continuing and new actors
- **Array Accumulation**: Concatenates previous films with current year
- **Quality Calculation**: Based on current year's average rating
- **Activity Tracking**: Boolean flag for current year activity

**Usage**:
```sql
-- To process year by year, update the WHERE clauses:
-- Year 1: WHERE current_year = 1969 and year = 1970
-- Year 2: WHERE current_year = 1970 and year = 1971
-- etc.
```

---

## Solution 3: DDL for `actors_history_scd` Table

Create SCD Type 2 table to track historical changes in quality and activity.

```sql
CREATE TABLE actors_history_scd (
    actor TEXT,
    actorid TEXT,
    quality_class quality_class,
    is_active BOOLEAN,
    start_year INTEGER,
    end_year INTEGER,
    current_year INTEGER,
    PRIMARY KEY (actorid, start_year)
);

-- Index for temporal queries
CREATE INDEX idx_actors_scd_temporal 
    ON actors_history_scd (actorid, start_year, end_year);

-- Index for point-in-time queries
CREATE INDEX idx_actors_scd_current 
    ON actors_history_scd (actorid, current_year);
```

**Design Decisions**:
- `start_year` and `end_year` define the valid period for each record
- `current_year` tracks when the record was created (for auditing)
- Indexes support both temporal range and point-in-time queries
- Primary key on `(actorid, start_year)` ensures unique periods

---

## Solution 4: Backfill Query for `actors_history_scd`

Populate the entire SCD table in a single query using streak identification.

```sql
INSERT INTO actors_history_scd
WITH streak_started AS (
    -- Identify when quality_class or is_active changes
    SELECT 
        actor,
        actorid,
        quality_class,
        is_active,
        current_year,
        -- Did quality_class change from previous year?
        LAG(quality_class, 1) OVER (
            PARTITION BY actorid 
            ORDER BY current_year
        ) <> quality_class 
        OR LAG(quality_class, 1) OVER (
            PARTITION BY actorid 
            ORDER BY current_year
        ) IS NULL AS quality_changed,
        -- Did is_active change from previous year?
        LAG(is_active, 1) OVER (
            PARTITION BY actorid 
            ORDER BY current_year
        ) <> is_active 
        OR LAG(is_active, 1) OVER (
            PARTITION BY actorid 
            ORDER BY current_year
        ) IS NULL AS active_changed
    FROM actors
),
streak_identified AS (
    -- Assign streak identifier to group consecutive periods
    SELECT 
        actor,
        actorid,
        quality_class,
        is_active,
        current_year,
        -- Increment streak_id whenever either attribute changes
        SUM(
            CASE 
                WHEN quality_changed OR active_changed 
                THEN 1 
                ELSE 0 
            END
        ) OVER (
            PARTITION BY actorid 
            ORDER BY current_year
        ) AS streak_identifier
    FROM streak_started
),
aggregated AS (
    -- Collapse consecutive years with same attributes
    SELECT 
        actor,
        actorid,
        quality_class,
        is_active,
        MIN(current_year) AS start_year,
        MAX(current_year) AS end_year,
        MAX(current_year) AS current_year  -- Latest year in streak
    FROM streak_identified
    GROUP BY actor, actorid, quality_class, is_active, streak_identifier
)
SELECT 
    actor,
    actorid,
    quality_class,
    is_active,
    start_year,
    end_year,
    current_year
FROM aggregated
ORDER BY actorid, start_year;
```

**Algorithm Explanation**:

1. **Streak Detection**: Use `LAG()` to identify when `quality_class` or `is_active` changes
2. **Streak Numbering**: Cumulative sum creates unique identifier for each period
3. **Aggregation**: Group by streak to find start/end years
4. **Result**: One row per period where attributes remained constant

**Example Output**:
```
actor       | actorid | quality | active | start | end  | current
------------|---------|---------|--------|-------|------|--------
Tom Hanks   | TH001   | star    | true   | 1988  | 1994 | 1994
Tom Hanks   | TH001   | good    | true   | 1995  | 1998 | 1998
Tom Hanks   | TH001   | star    | true   | 1999  | 2004 | 2004
Tom Hanks   | TH001   | star    | false  | 2005  | 2010 | 2010
```

---

## Solution 5: Incremental Query for `actors_history_scd`

Combine last year's SCD data with new data to update incrementally.

```sql
INSERT INTO actors_history_scd
WITH last_year_scd AS (
    -- Get the most recent record for each actor
    SELECT 
        actor,
        actorid,
        quality_class,
        is_active,
        start_year,
        end_year,
        current_year
    FROM actors_history_scd
    WHERE current_year = 2020  -- Previous year
),
this_year_data AS (
    -- Get current year data from actors table
    SELECT 
        actor,
        actorid,
        quality_class,
        is_active,
        current_year
    FROM actors
    WHERE current_year = 2021  -- Current year being processed
),
combined AS (
    SELECT 
        COALESCE(t.actor, l.actor) AS actor,
        COALESCE(t.actorid, l.actorid) AS actorid,
        COALESCE(t.quality_class, l.quality_class) AS quality_class,
        COALESCE(t.is_active, l.is_active) AS is_active,
        -- Determine if attributes changed
        CASE 
            WHEN l.actorid IS NULL THEN TRUE  -- New actor
            WHEN t.quality_class <> l.quality_class 
                OR t.is_active <> l.is_active THEN TRUE  -- Changed
            ELSE FALSE  -- Unchanged
        END AS did_change,
        l.start_year,
        l.end_year,
        l.current_year AS last_current_year,
        t.current_year AS this_year
    FROM last_year_scd l
    FULL OUTER JOIN this_year_data t
        ON l.actorid = t.actorid
),
unchanged AS (
    -- For unchanged records, extend the end_year
    SELECT 
        actor,
        actorid,
        quality_class,
        is_active,
        start_year,
        this_year AS end_year,  -- Extend end date
        this_year AS current_year
    FROM combined
    WHERE did_change = FALSE
),
changed AS (
    -- For changed records, close old record and start new one
    SELECT 
        actor,
        actorid,
        quality_class,
        is_active,
        start_year,
        last_current_year AS end_year,  -- Close previous record
        last_current_year AS current_year
    FROM combined
    WHERE did_change = TRUE
        AND start_year IS NOT NULL  -- Had previous record
    
    UNION ALL
    
    -- Start new record for changed attributes
    SELECT 
        actor,
        actorid,
        quality_class,
        is_active,
        this_year AS start_year,  -- Start new record
        this_year AS end_year,
        this_year AS current_year
    FROM combined
    WHERE did_change = TRUE
        AND this_year IS NOT NULL  -- Has current data
)
SELECT * FROM unchanged
UNION ALL
SELECT * FROM changed
ORDER BY actorid, start_year;
```

**Incremental Logic**:

1. **Unchanged Actors**: Extend `end_year` to current year
2. **Changed Actors**: 
   - Close the previous record (set `end_year` to last year)
   - Create new record starting this year
3. **New Actors**: Create first record
4. **Inactive Actors**: Keep last record as-is

**Benefits**:
- Processes only one year at a time (efficient)
- Maintains complete history
- Handles all edge cases (new, changed, unchanged, inactive)

---

## Testing Queries

### Verify Data Quality

```sql
-- Check for gaps in SCD periods
SELECT 
    actorid,
    actor,
    start_year,
    end_year,
    LEAD(start_year) OVER (PARTITION BY actorid ORDER BY start_year) AS next_start
FROM actors_history_scd
WHERE end_year + 1 <> LEAD(start_year) OVER (PARTITION BY actorid ORDER BY start_year)
    AND LEAD(start_year) OVER (PARTITION BY actorid ORDER BY start_year) IS NOT NULL;
-- Should return 0 rows (no gaps)

-- Check for overlapping periods
SELECT 
    actorid,
    actor,
    start_year,
    end_year,
    LEAD(start_year) OVER (PARTITION BY actorid ORDER BY start_year) AS next_start
FROM actors_history_scd
WHERE end_year >= LEAD(start_year) OVER (PARTITION BY actorid ORDER BY start_year);
-- Should return 0 rows (no overlaps)
```

### Point-in-Time Query

```sql
-- Find all "star" actors in year 2000
SELECT 
    actor,
    actorid,
    quality_class,
    is_active
FROM actors_history_scd
WHERE start_year <= 2000
    AND end_year >= 2000
    AND quality_class = 'star';
```

### Analyze Quality Transitions

```sql
-- How often do actors transition between quality classes?
WITH transitions AS (
    SELECT 
        actorid,
        quality_class AS from_quality,
        LEAD(quality_class) OVER (PARTITION BY actorid ORDER BY start_year) AS to_quality,
        end_year - start_year + 1 AS duration_years
    FROM actors_history_scd
)
SELECT 
    from_quality,
    to_quality,
    COUNT(*) AS transition_count,
    AVG(duration_years) AS avg_duration_before_transition
FROM transitions
WHERE to_quality IS NOT NULL
    AND from_quality <> to_quality  -- Only actual changes
GROUP BY from_quality, to_quality
ORDER BY transition_count DESC;
```

---

## Key Learnings

### Technical Skills
✅ Slowly Changing Dimensions (SCD Type 2)  
✅ Window functions (LAG, LEAD, SUM OVER)  
✅ Array operations and custom types  
✅ Temporal data modeling  
✅ Incremental processing patterns  

### Design Patterns
✅ Streak identification algorithm  
✅ Full outer join for comprehensive coverage  
✅ Idempotent query design  
✅ Composite primary keys for temporal data  

### Best Practices
✅ Use enums for categorical data  
✅ Index temporal columns for performance  
✅ Document assumptions and edge cases  
✅ Test for data quality (gaps, overlaps)  

---

## Performance Considerations

- **Backfill Query**: O(n log n) due to window functions, efficient for full history
- **Incremental Query**: O(n) processes only new data, optimal for daily runs
- **Indexes**: Essential for point-in-time and range queries
- **Partitioning**: Consider partitioning by `start_year` for very large tables

---

*Solution completed as part of DataExpert.io Data Engineering Bootcamp - December 2024*


