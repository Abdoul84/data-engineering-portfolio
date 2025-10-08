-- ====================================================================
-- Development Indicators Facts Table
-- Stores World Bank development indicators for Senegal over time
-- ====================================================================

USE DATABASE SENEGAL_ANALYTICS;
USE SCHEMA PUBLIC;

-- Drop if exists (for development)
-- DROP TABLE IF EXISTS economic_facts;

-- Development Indicators Facts Table
CREATE TABLE IF NOT EXISTS development_facts (
    fact_key INT AUTOINCREMENT PRIMARY KEY,
    year INT NOT NULL,
    indicator_code VARCHAR(50) NOT NULL,
    indicator_name VARCHAR(200),
    value DECIMAL(20, 4),
    president_id INT,
    president_name VARCHAR(100),
    party VARCHAR(100),
    
    -- Country metadata
    country VARCHAR(100) DEFAULT 'Senegal',
    country_code VARCHAR(10) DEFAULT 'SN',
    
    -- Data quality fields
    is_estimated BOOLEAN DEFAULT FALSE,
    data_source VARCHAR(100) DEFAULT 'World Bank',
    data_quality_score DECIMAL(3, 2),
    
    -- Audit fields
    ingestion_timestamp TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    
    -- Composite unique constraint
    CONSTRAINT uk_development_obs UNIQUE (year, indicator_code)
);

-- Clustering for query optimization (partition by year)
ALTER TABLE development_facts CLUSTER BY (year, indicator_code);

-- Comment the table
COMMENT ON TABLE development_facts IS 'Fact table storing time-series development indicators from World Bank API for Senegal (1960-present)';

-- Column comments
COMMENT ON COLUMN development_facts.indicator_code IS 'World Bank indicator code (e.g., NY.GDP.MKTP.KD.ZG for GDP growth)';
COMMENT ON COLUMN development_facts.value IS 'The actual indicator value';
COMMENT ON COLUMN development_facts.data_quality_score IS 'Score from 0-1 indicating data quality';

