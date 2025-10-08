# 📊 Advanced Analytical Patterns

## Overview

This project demonstrates sophisticated analytical frameworks used in product analytics, including growth accounting, cohort retention, funnel analysis, and window-based calculations. These patterns power data-driven decision making at top tech companies.

## 🎯 Project Goals

- Implement growth accounting frameworks
- Build cohort retention analysis
- Create multi-step conversion funnels
- Develop window-based trend analysis
- Calculate product engagement metrics
- Design actionable analytics for stakeholders

## 🛠️ Technologies Used

- **Database**: PostgreSQL
- **Language**: SQL
- **Techniques**: Window Functions, CTEs, Grouping Sets
- **Analysis**: Growth Metrics, Retention, Funnels

## 📚 Key Concepts Implemented

### 1. Growth Accounting
Categorizes users into lifecycle states to understand business health.

**User States**:
- **New**: First-time active users
- **Retained**: Active in previous and current period
- **Resurrected**: Previously churned, now active again
- **Churned**: Previously active, now inactive

### 2. Cohort Retention Analysis
Tracks how groups of users engage over time.

**Features**:
- Day 0 through Day 30+ retention
- Cohort comparison across time periods
- Multi-dimensional analysis (platform, country, etc.)
- Visual retention curves

### 3. Funnel Analysis
Measures conversion through sequential steps.

**Features**:
- Multi-step conversion tracking
- Drop-off rate identification
- Time-to-convert analysis
- Segmented funnel comparison

## 📂 Project Structure

```
05-analytical-patterns/
├── README.md                        # This file
├── sql/
│   ├── growth_accounting.sql       # User lifecycle analysis
│   ├── retention_analysis.sql      # Cohort retention queries
│   ├── funnel_analysis.sql         # Conversion funnel logic
│   ├── window_based_analysis.sql   # Trend analysis
│   └── grouping_sets.sql           # Multi-dimensional aggregations
├── tables/
│   └── user_growth_accounting.sql  # DDL for growth table
└── examples/
    ├── sample_queries.sql          # Example analytics
    └── dashboard_queries.sql       # Production dashboard queries
```

## 🚀 Getting Started

### Prerequisites

- PostgreSQL 12+
- Sample events/users data
- Understanding of basic SQL

### Setup Instructions

1. **Create Analytics Tables**
```bash
psql -h localhost -U postgres -d postgres -f tables/user_growth_accounting.sql
```

2. **Load Sample Data**
```sql
-- Ensure you have events table populated
SELECT COUNT(*) FROM events;
```

3. **Run Analytical Queries**
```sql
-- Execute queries from sql/ folder
\i sql/growth_accounting.sql
```

## 💡 Key Implementations

### 1. Growth Accounting Framework

**DDL**:
```sql
CREATE TABLE user_growth_accounting (
    user_id TEXT,
    date DATE,
    status user_status_enum,
    PRIMARY KEY (user_id, date)
);

CREATE TYPE user_status_enum AS ENUM (
    'new',
    'retained', 
    'resurrected',
    'churned'
);
```

**Classification Logic**:
```sql
WITH user_activity AS (
    SELECT 
        user_id,
        DATE(event_time) AS activity_date
    FROM events
    GROUP BY user_id, DATE(event_time)
),
yesterday_users AS (
    SELECT DISTINCT user_id
    FROM user_activity
    WHERE activity_date = CURRENT_DATE - INTERVAL '1 day'
),
today_users AS (
    SELECT DISTINCT user_id
    FROM user_activity
    WHERE activity_date = CURRENT_DATE
),
historical_users AS (
    SELECT DISTINCT user_id
    FROM user_activity
    WHERE activity_date < CURRENT_DATE - INTERVAL '1 day'
)
INSERT INTO user_growth_accounting
SELECT 
    t.user_id,
    CURRENT_DATE AS date,
    CASE
        -- New: Active today, never active before
        WHEN h.user_id IS NULL AND y.user_id IS NULL THEN 'new'
        
        -- Retained: Active yesterday and today
        WHEN y.user_id IS NOT NULL THEN 'retained'
        
        -- Resurrected: Active today, was active historically but not yesterday
        WHEN h.user_id IS NOT NULL AND y.user_id IS NULL THEN 'resurrected'
        
        -- Churned: Active yesterday but not today
        WHEN y.user_id IS NOT NULL AND t.user_id IS NULL THEN 'churned'
    END AS status
FROM today_users t
FULL OUTER JOIN yesterday_users y USING (user_id)
LEFT JOIN historical_users h ON t.user_id = h.user_id;
```

**Growth Metrics**:
```sql
SELECT 
    date,
    COUNT(CASE WHEN status = 'new' THEN 1 END) AS new_users,
    COUNT(CASE WHEN status = 'retained' THEN 1 END) AS retained_users,
    COUNT(CASE WHEN status = 'resurrected' THEN 1 END) AS resurrected_users,
    COUNT(CASE WHEN status = 'churned' THEN 1 END) AS churned_users,
    -- Net growth
    COUNT(CASE WHEN status IN ('new', 'resurrected') THEN 1 END) -
    COUNT(CASE WHEN status = 'churned' THEN 1 END) AS net_growth,
    -- Total active
    COUNT(CASE WHEN status IN ('new', 'retained', 'resurrected') THEN 1 END) AS total_active
FROM user_growth_accounting
GROUP BY date
ORDER BY date;
```

### 2. Cohort Retention Analysis

**Cohort Definition**:
```sql
WITH user_first_activity AS (
    SELECT 
        user_id,
        MIN(DATE(event_time)) AS cohort_date
    FROM events
    GROUP BY user_id
),
user_activity AS (
    SELECT 
        e.user_id,
        DATE(e.event_time) AS activity_date,
        f.cohort_date,
        DATE(e.event_time) - f.cohort_date AS days_since_signup
    FROM events e
    JOIN user_first_activity f ON e.user_id = f.user_id
)
SELECT 
    cohort_date,
    COUNT(DISTINCT CASE WHEN days_since_signup = 0 THEN user_id END) AS day_0,
    COUNT(DISTINCT CASE WHEN days_since_signup = 1 THEN user_id END) AS day_1,
    COUNT(DISTINCT CASE WHEN days_since_signup = 7 THEN user_id END) AS day_7,
    COUNT(DISTINCT CASE WHEN days_since_signup = 14 THEN user_id END) AS day_14,
    COUNT(DISTINCT CASE WHEN days_since_signup = 30 THEN user_id END) AS day_30,
    -- Retention percentages
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN days_since_signup = 1 THEN user_id END) / 
          NULLIF(COUNT(DISTINCT CASE WHEN days_since_signup = 0 THEN user_id END), 0), 2) AS day_1_retention,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN days_since_signup = 7 THEN user_id END) / 
          NULLIF(COUNT(DISTINCT CASE WHEN days_since_signup = 0 THEN user_id END), 0), 2) AS day_7_retention,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN days_since_signup = 30 THEN user_id END) / 
          NULLIF(COUNT(DISTINCT CASE WHEN days_since_signup = 0 THEN user_id END), 0), 2) AS day_30_retention
FROM user_activity
GROUP BY cohort_date
ORDER BY cohort_date DESC;
```

### 3. Funnel Analysis

**Multi-Step Conversion**:
```sql
WITH user_events AS (
    SELECT 
        user_id,
        event_name,
        event_time,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_time) AS event_sequence
    FROM events
    WHERE event_name IN ('page_view', 'add_to_cart', 'checkout', 'purchase')
),
funnel AS (
    SELECT 
        user_id,
        MAX(CASE WHEN event_name = 'page_view' THEN 1 ELSE 0 END) AS viewed,
        MAX(CASE WHEN event_name = 'add_to_cart' THEN 1 ELSE 0 END) AS added_to_cart,
        MAX(CASE WHEN event_name = 'checkout' THEN 1 ELSE 0 END) AS checked_out,
        MAX(CASE WHEN event_name = 'purchase' THEN 1 ELSE 0 END) AS purchased
    FROM user_events
    GROUP BY user_id
)
SELECT 
    SUM(viewed) AS step_1_page_view,
    SUM(added_to_cart) AS step_2_add_to_cart,
    SUM(checked_out) AS step_3_checkout,
    SUM(purchased) AS step_4_purchase,
    -- Conversion rates
    ROUND(100.0 * SUM(added_to_cart) / NULLIF(SUM(viewed), 0), 2) AS view_to_cart_rate,
    ROUND(100.0 * SUM(checked_out) / NULLIF(SUM(added_to_cart), 0), 2) AS cart_to_checkout_rate,
    ROUND(100.0 * SUM(purchased) / NULLIF(SUM(checked_out), 0), 2) AS checkout_to_purchase_rate,
    ROUND(100.0 * SUM(purchased) / NULLIF(SUM(viewed), 0), 2) AS overall_conversion_rate
FROM funnel;
```

### 4. Window-Based Trend Analysis

**Moving Averages & Trends**:
```sql
WITH daily_metrics AS (
    SELECT 
        DATE(event_time) AS date,
        COUNT(DISTINCT user_id) AS dau,
        COUNT(*) AS total_events
    FROM events
    GROUP BY DATE(event_time)
)
SELECT 
    date,
    dau,
    total_events,
    -- 7-day moving average
    AVG(dau) OVER (
        ORDER BY date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS dau_7d_ma,
    -- Week-over-week growth
    ROUND(100.0 * (dau - LAG(dau, 7) OVER (ORDER BY date)) / 
          NULLIF(LAG(dau, 7) OVER (ORDER BY date), 0), 2) AS wow_growth_pct,
    -- Month-over-month
    ROUND(100.0 * (dau - LAG(dau, 30) OVER (ORDER BY date)) / 
          NULLIF(LAG(dau, 30) OVER (ORDER BY date), 0), 2) AS mom_growth_pct,
    -- Cumulative users
    SUM(dau) OVER (ORDER BY date) AS cumulative_users
FROM daily_metrics
ORDER BY date DESC;
```

### 5. Grouping Sets for Multi-Dimensional Analysis

**Roll-Up Aggregations**:
```sql
SELECT 
    country,
    platform,
    device_type,
    COUNT(DISTINCT user_id) AS active_users,
    SUM(revenue) AS total_revenue,
    AVG(session_duration) AS avg_session_duration
FROM user_sessions
GROUP BY GROUPING SETS (
    (country, platform, device_type),  -- Full detail
    (country, platform),               -- By country and platform
    (country),                         -- By country only
    (platform, device_type),           -- By platform and device
    ()                                 -- Grand total
)
ORDER BY country, platform, device_type;
```

## 📊 Sample Insights

### Growth Accounting Results
```
Date       | New | Retained | Resurrected | Churned | Net Growth | Total Active
-----------|-----|----------|-------------|---------|------------|-------------
2024-01-15 | 150 |   1,200  |      80     |   100   |    +130    |   1,430
2024-01-14 | 120 |   1,150  |      50     |   120   |     +50    |   1,320
2024-01-13 | 180 |   1,100  |      70     |   130   |    +120    |   1,350
```

### Cohort Retention
```
Cohort     | Day 0 | Day 1 | Day 7 | Day 30 | D1 Ret% | D7 Ret% | D30 Ret%
-----------|-------|-------|-------|--------|---------|---------|----------
2024-01-01 | 1000  |  420  |  280  |  150   |  42.0%  |  28.0%  |  15.0%
2024-01-08 | 1200  |  510  |  350  |  190   |  42.5%  |  29.2%  |  15.8%
2024-01-15 |  950  |  410  |  270  |   -    |  43.2%  |  28.4%  |    -
```

### Funnel Conversion
```
Step                | Users  | Conversion Rate
--------------------|--------|----------------
1. Page View        | 10,000 |    100.0%
2. Add to Cart      |  2,500 |     25.0%
3. Checkout         |  1,250 |     50.0% (of step 2)
4. Purchase         |    875 |     70.0% (of step 3)
Overall Conversion  |        |      8.75%
```

## 🎓 Learning Outcomes

After completing this project, you will understand:

✅ **Growth Metrics**: User lifecycle and business health indicators  
✅ **Retention Analysis**: Cohort-based engagement tracking  
✅ **Funnel Optimization**: Identifying conversion bottlenecks  
✅ **Trend Analysis**: Moving averages and growth rates  
✅ **Multi-Dimensional**: Roll-up aggregations with GROUPING SETS  
✅ **Product Analytics**: Translating data into actionable insights  

## 🔍 Key Insights

### When to Use Each Pattern

**Growth Accounting**:
- Daily/weekly business reviews
- Product health dashboards
- Churn prediction
- Engagement monitoring

**Cohort Retention**:
- Product-market fit assessment
- Feature impact analysis
- User lifecycle understanding
- Benchmark tracking

**Funnel Analysis**:
- Conversion optimization
- UX improvement identification
- A/B test analysis
- User journey mapping

**Window Functions**:
- Trend identification
- Anomaly detection
- Forecasting support
- Performance tracking

### Best Practices
1. **Define clear time windows** (daily, weekly, monthly)
2. **Segment analysis** by meaningful dimensions
3. **Track leading indicators** not just lagging
4. **Automate refresh** for real-time dashboards
5. **Validate logic** with known test cases
6. **Document calculations** for stakeholder trust

### Common Pitfalls
❌ Mixing processing and event time  
❌ Not handling timezones correctly  
❌ Ignoring data quality issues  
❌ Over-segmenting (small sample sizes)  
❌ Confusing correlation with causation  

## 🚧 Challenges Solved

1. **User State Classification**: Accurately categorizing user lifecycle
2. **Cohort Comparability**: Normalizing cohorts for fair comparison
3. **Funnel Sequencing**: Ensuring proper step ordering
4. **Window Calculations**: Efficient moving average computation
5. **Multi-Dimensional**: Handling sparse data in roll-ups

## 📈 Real-World Applications

These patterns are used by:
- **Social Networks**: User engagement and retention
- **E-commerce**: Purchase funnel optimization
- **SaaS Products**: Feature adoption and churn prevention
- **Gaming**: Player lifecycle management
- **Marketplaces**: Supply/demand balancing

## 🔗 Related Projects

- [Fact Modeling](../02-fact-modeling/) - Build cumulative activity tables
- [Experimentation](../06-experimentation/) - Test hypotheses from insights
- [Dimensional Modeling](../01-dimensional-modeling/) - Historical context

## 📚 Resources

- [Amplitude Growth Accounting](https://amplitude.com/blog/growth-accounting)
- [Mixpanel Retention Analysis](https://mixpanel.com/blog/retention-analysis/)
- [PostgreSQL Window Functions](https://www.postgresql.org/docs/current/tutorial-window.html)
- [SQL for Data Analysis Book](https://www.oreilly.com/library/view/sql-for-data/9781492088776/)

---

**Next Steps**: Apply these insights to [KPI Design & Experimentation](../06-experimentation/) for hypothesis-driven product development.


