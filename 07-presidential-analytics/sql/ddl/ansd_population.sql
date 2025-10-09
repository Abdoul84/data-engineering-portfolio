-- ====================================================================
-- ANSD Population Data Table
-- Official Senegal population statistics from National Agency for Statistics and Demography
-- ====================================================================

USE DATABASE SENEGAL_ANALYTICS;
USE SCHEMA PUBLIC;

-- ANSD Population Statistics Table
CREATE TABLE IF NOT EXISTS ansd_population (
    population_key INT AUTOINCREMENT PRIMARY KEY,
    year INT NOT NULL,
    total_population NUMBER(12, 0),
    urban_population NUMBER(12, 0),
    rural_population NUMBER(12, 0),
    urban_percentage DECIMAL(5, 2),
    rural_percentage DECIMAL(5, 2),
    population_growth_rate DECIMAL(4, 2),
    age_0_14 NUMBER(12, 0),
    age_15_64 NUMBER(12, 0),
    age_65_plus NUMBER(12, 0),
    
    -- Country metadata
    country VARCHAR(100) DEFAULT 'Senegal',
    country_code VARCHAR(10) DEFAULT 'SN',
    
    -- Data source
    data_source VARCHAR(100) DEFAULT 'ANSD Senegal',
    
    -- Audit fields
    ingestion_timestamp TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- ANSD Demographic Indicators Table
CREATE TABLE IF NOT EXISTS ansd_demographics (
    demo_key INT AUTOINCREMENT PRIMARY KEY,
    period_start INT NOT NULL,
    period_end INT NOT NULL,
    president VARCHAR(100),
    party VARCHAR(100),
    avg_population_growth DECIMAL(4, 2),
    urbanization_rate_change DECIMAL(4, 2),
    youth_dependency_ratio DECIMAL(4, 2),
    total_fertility_rate DECIMAL(4, 2),
    life_expectancy_start DECIMAL(4, 1),
    life_expectancy_end DECIMAL(4, 1),
    
    -- Country metadata
    country VARCHAR(100) DEFAULT 'Senegal',
    country_code VARCHAR(10) DEFAULT 'SN',
    
    -- Data source
    data_source VARCHAR(100) DEFAULT 'ANSD Senegal',
    
    -- Audit fields
    ingestion_timestamp TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Comment the tables
COMMENT ON TABLE ansd_population IS 'Official Senegal population statistics from ANSD (National Agency for Statistics and Demography)';
COMMENT ON TABLE ansd_demographics IS 'Demographic indicators by presidential period from ANSD';

-- Column comments
COMMENT ON COLUMN ansd_population.total_population IS 'Total population in Senegal';
COMMENT ON COLUMN ansd_population.urban_percentage IS 'Percentage of population living in urban areas';
COMMENT ON COLUMN ansd_population.population_growth_rate IS 'Annual population growth rate (%)';
COMMENT ON COLUMN ansd_demographics.youth_dependency_ratio IS 'Ratio of population under 15 to working age population';
COMMENT ON COLUMN ansd_demographics.total_fertility_rate IS 'Average number of children per woman';

