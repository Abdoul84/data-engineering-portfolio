-- ====================================================================
-- Economic Facts Table
-- Stores economic indicators over time
-- ====================================================================

USE DATABASE PRESIDENTIAL_ANALYTICS;
USE SCHEMA PUBLIC;

-- Drop if exists (for development)
-- DROP TABLE IF EXISTS economic_facts;

-- Economic Facts Table
CREATE TABLE IF NOT EXISTS economic_facts (
    economic_fact_key INT AUTOINCREMENT PRIMARY KEY,
    observation_date DATE NOT NULL,
    series_id VARCHAR(50) NOT NULL,
    series_name VARCHAR(200),
    metric_value DECIMAL(20, 4),
    president_id INT,
    president_name VARCHAR(100),
    party VARCHAR(50),
    
    -- Data quality fields
    is_estimated BOOLEAN DEFAULT FALSE,
    data_source VARCHAR(100) DEFAULT 'FRED',
    data_quality_score DECIMAL(3, 2),
    
    -- Audit fields
    ingestion_timestamp TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    
    -- Composite unique constraint
    CONSTRAINT uk_economic_obs UNIQUE (observation_date, series_id)
);

-- Clustering for query optimization (partition by date)
ALTER TABLE economic_facts CLUSTER BY (observation_date, series_id);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_economic_date ON economic_facts(observation_date);
CREATE INDEX IF NOT EXISTS idx_economic_series ON economic_facts(series_id);
CREATE INDEX IF NOT EXISTS idx_economic_president ON economic_facts(president_id);
CREATE INDEX IF NOT EXISTS idx_economic_party ON economic_facts(party);

-- Comment the table
COMMENT ON TABLE economic_facts IS 'Fact table storing time-series economic indicators from FRED API';

-- Column comments
COMMENT ON COLUMN economic_facts.series_id IS 'FRED series identifier (e.g., GDP, UNRATE)';
COMMENT ON COLUMN economic_facts.metric_value IS 'The actual economic metric value';
COMMENT ON COLUMN economic_facts.data_quality_score IS 'Score from 0-1 indicating data quality';

