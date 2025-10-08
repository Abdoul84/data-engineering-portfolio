-- ====================================================================
-- Incremental Data Load Script
-- Merge new data into existing tables using MERGE statement
-- ====================================================================

USE DATABASE PRESIDENTIAL_ANALYTICS;
USE SCHEMA PUBLIC;

-- ====================================================================
-- 1. Create staging tables for new data
-- ====================================================================

CREATE OR REPLACE TEMPORARY TABLE stage_presidents (
    president_id INT,
    president_name VARCHAR(100),
    party VARCHAR(50),
    start_date DATE,
    end_date DATE,
    terms INT,
    tenure_days INT,
    is_current BOOLEAN,
    key_policies TEXT,
    ingestion_timestamp TIMESTAMP
);

CREATE OR REPLACE TEMPORARY TABLE stage_economic_facts (
    observation_date DATE,
    series_id VARCHAR(50),
    series_name VARCHAR(200),
    metric_value DECIMAL(20, 4),
    president_id INT,
    president_name VARCHAR(100),
    party VARCHAR(50),
    ingestion_timestamp TIMESTAMP
);

-- ====================================================================
-- 2. Load data from S3 to staging tables
-- ====================================================================

-- Note: Update these paths to match your S3 bucket structure
-- Example for loading from S3:

/*
COPY INTO stage_presidents
FROM @presidential_data_stage/presidents/
FILE_FORMAT = (TYPE = 'PARQUET')
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

COPY INTO stage_economic_facts
FROM @presidential_data_stage/economic/
FILE_FORMAT = (TYPE = 'PARQUET')
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;
*/

-- ====================================================================
-- 3. Merge Presidents Data (SCD Type 2)
-- ====================================================================

MERGE INTO presidents_dim target
USING (
    SELECT 
        president_id,
        president_name,
        party,
        start_date,
        end_date,
        terms,
        tenure_days,
        is_current,
        key_policies,
        CURRENT_DATE() as effective_date
    FROM stage_presidents
) source
ON target.president_id = source.president_id 
   AND target.is_active = TRUE

-- When there's a change in existing president data
WHEN MATCHED AND (
    target.president_name != source.president_name OR
    target.party != source.party OR
    target.end_date != source.end_date OR
    target.is_current != source.is_current OR
    target.key_policies != source.key_policies
) THEN UPDATE SET
    target.is_active = FALSE,
    target.expiration_date = CURRENT_DATE(),
    target.updated_at = CURRENT_TIMESTAMP()

-- When there's no match, insert new record
WHEN NOT MATCHED THEN INSERT (
    president_id,
    president_name,
    party,
    start_date,
    end_date,
    terms,
    tenure_days,
    is_current,
    key_policies,
    effective_date,
    expiration_date,
    is_active
) VALUES (
    source.president_id,
    source.president_name,
    source.party,
    source.start_date,
    source.end_date,
    source.terms,
    source.tenure_days,
    source.is_current,
    source.key_policies,
    source.effective_date,
    NULL,
    TRUE
);

-- Insert new versions of changed records
INSERT INTO presidents_dim (
    president_id,
    president_name,
    party,
    start_date,
    end_date,
    terms,
    tenure_days,
    is_current,
    key_policies,
    effective_date,
    expiration_date,
    is_active
)
SELECT 
    s.president_id,
    s.president_name,
    s.party,
    s.start_date,
    s.end_date,
    s.terms,
    s.tenure_days,
    s.is_current,
    s.key_policies,
    CURRENT_DATE() as effective_date,
    NULL as expiration_date,
    TRUE as is_active
FROM stage_presidents s
WHERE EXISTS (
    SELECT 1 
    FROM presidents_dim t
    WHERE t.president_id = s.president_id
      AND t.is_active = FALSE
      AND t.expiration_date = CURRENT_DATE()
);

-- ====================================================================
-- 4. Merge Economic Facts (Simple Upsert)
-- ====================================================================

MERGE INTO economic_facts target
USING stage_economic_facts source
ON target.observation_date = source.observation_date 
   AND target.series_id = source.series_id

-- Update if values changed
WHEN MATCHED AND (
    target.metric_value != source.metric_value OR
    target.president_id != source.president_id
) THEN UPDATE SET
    target.metric_value = source.metric_value,
    target.series_name = source.series_name,
    target.president_id = source.president_id,
    target.president_name = source.president_name,
    target.party = source.party,
    target.updated_at = CURRENT_TIMESTAMP()

-- Insert new records
WHEN NOT MATCHED THEN INSERT (
    observation_date,
    series_id,
    series_name,
    metric_value,
    president_id,
    president_name,
    party,
    data_source,
    ingestion_timestamp
) VALUES (
    source.observation_date,
    source.series_id,
    source.series_name,
    source.metric_value,
    source.president_id,
    source.president_name,
    source.party,
    'FRED',
    source.ingestion_timestamp
);

-- ====================================================================
-- 5. Data Quality Checks
-- ====================================================================

-- Check for data loaded
SELECT 
    'Presidents' as table_name,
    COUNT(*) as record_count
FROM presidents_dim
WHERE is_active = TRUE

UNION ALL

SELECT 
    'Economic Facts' as table_name,
    COUNT(*) as record_count
FROM economic_facts;

-- Check date ranges
SELECT 
    'Economic Facts Date Range' as check_name,
    MIN(observation_date) as min_date,
    MAX(observation_date) as max_date,
    COUNT(DISTINCT series_id) as series_count
FROM economic_facts;

-- ====================================================================
-- 6. Cleanup staging tables
-- ====================================================================

DROP TABLE IF EXISTS stage_presidents;
DROP TABLE IF EXISTS stage_economic_facts;

-- Print completion message
SELECT 'Incremental load completed successfully at ' || CURRENT_TIMESTAMP() as status;

