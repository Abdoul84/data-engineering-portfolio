-- ====================================================================
-- Presidents Dimension Table (SCD Type 2)
-- Tracks Senegalese Presidents and their administrations
-- ====================================================================

CREATE DATABASE IF NOT EXISTS SENEGAL_ANALYTICS;
USE DATABASE SENEGAL_ANALYTICS;

CREATE SCHEMA IF NOT EXISTS PUBLIC;
USE SCHEMA PUBLIC;

-- Drop if exists (for development)
-- DROP TABLE IF EXISTS presidents_dim;

-- Presidents Dimension Table
CREATE TABLE IF NOT EXISTS presidents_dim (
    president_key INT AUTOINCREMENT PRIMARY KEY,
    president_id INT NOT NULL,
    president_name VARCHAR(100) NOT NULL,
    party VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    terms INT,
    tenure_days INT,
    is_current BOOLEAN,
    key_policies TEXT,
    
    -- SCD Type 2 fields
    effective_date DATE NOT NULL,
    expiration_date DATE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    
    -- Audit fields
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Comment the table
COMMENT ON TABLE presidents_dim IS 'Dimension table tracking Senegalese Presidents with SCD Type 2 for historical changes (1960-present)';

-- Column comments
COMMENT ON COLUMN presidents_dim.president_key IS 'Surrogate key for SCD Type 2';
COMMENT ON COLUMN presidents_dim.president_id IS 'Official president number (e.g., 45 for Trump)';
COMMENT ON COLUMN presidents_dim.effective_date IS 'When this record became effective';
COMMENT ON COLUMN presidents_dim.expiration_date IS 'When this record expired (NULL if current)';
COMMENT ON COLUMN presidents_dim.is_active IS 'Is this the current active record?';

