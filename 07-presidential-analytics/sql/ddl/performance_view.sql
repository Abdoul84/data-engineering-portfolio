-- ====================================================================
-- Presidential Performance Aggregated View
-- Provides summary metrics by president for dashboard
-- ====================================================================

USE DATABASE PRESIDENTIAL_ANALYTICS;
USE SCHEMA PUBLIC;

CREATE OR REPLACE VIEW presidential_performance AS
WITH president_metrics AS (
    SELECT 
        p.president_id,
        p.president_name,
        p.party,
        p.start_date,
        p.end_date,
        p.tenure_days,
        e.series_id,
        e.series_name,
        
        -- Aggregate metrics for each president's term
        AVG(e.metric_value) as avg_value,
        MIN(e.metric_value) as min_value,
        MAX(e.metric_value) as max_value,
        STDDEV(e.metric_value) as stddev_value,
        COUNT(e.metric_value) as observation_count,
        
        -- First and last values for trend
        FIRST_VALUE(e.metric_value) OVER (
            PARTITION BY p.president_id, e.series_id 
            ORDER BY e.observation_date
        ) as starting_value,
        LAST_VALUE(e.metric_value) OVER (
            PARTITION BY p.president_id, e.series_id 
            ORDER BY e.observation_date
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) as ending_value
        
    FROM presidents_dim p
    INNER JOIN economic_facts e 
        ON e.president_id = p.president_id
    WHERE p.is_active = TRUE
    GROUP BY 
        p.president_id, p.president_name, p.party, 
        p.start_date, p.end_date, p.tenure_days,
        e.series_id, e.series_name
)
SELECT 
    president_id,
    president_name,
    party,
    start_date,
    end_date,
    tenure_days,
    series_id,
    series_name,
    avg_value,
    min_value,
    max_value,
    stddev_value,
    observation_count,
    starting_value,
    ending_value,
    
    -- Calculate change metrics
    (ending_value - starting_value) as absolute_change,
    CASE 
        WHEN starting_value != 0 THEN 
            ((ending_value - starting_value) / starting_value * 100)
        ELSE NULL 
    END as percent_change,
    
    -- Calculate trend direction
    CASE 
        WHEN ending_value > starting_value THEN 'Increasing'
        WHEN ending_value < starting_value THEN 'Decreasing'
        ELSE 'Stable'
    END as trend_direction

FROM president_metrics;

-- Comment the view
COMMENT ON VIEW presidential_performance IS 'Aggregated economic performance metrics by president for analysis and visualization';

